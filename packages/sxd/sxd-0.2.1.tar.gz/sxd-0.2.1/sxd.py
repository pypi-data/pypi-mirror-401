"""
SXD CLI - Pipeline Development & Operations

This CLI is for pipeline authors and data operators.
For infrastructure management, use sxdinfra.

Usage:
    sxd [command] [args]

Mental Model:
    DEVELOP  - Write and publish pipelines (publish, workflows)
    OPERATE  - Upload data and submit jobs (upload, submit, status)
    OBSERVE  - Monitor cluster and jobs (info, stats, ls, query)

Commands support --rich flag for enhanced TUI output.
"""

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

import argparse
import asyncio
import json
import os
import shutil
import subprocess
import sys
import textwrap
import types
from pathlib import Path
from typing import Optional

# Ensure current directory is in PYTHONPATH
sys.path.append(str(Path(__file__).parent))

# Import shared modules from sxd_core
from sxd_core import get_workflow, list_workflows, load_pipelines
from sxd_core.audit import log_audit_event, set_customer_context, set_user_context
from sxd_core.auth import (
    COMMAND_PERMISSIONS,
    User,
    get_auth_manager,
    get_current_user,
    get_stored_api_key,
)
from sxd_core.config import get_temporal_config
from sxd_core.ops import (
    get_24h_stats,
    get_cluster_info,
    get_error_summary,
    get_node_status,
    get_storage_stats,
    get_video_details,
    get_workers,
    get_workflow_status,
    list_batches,
    list_episodes,
    list_videos,
    run_auth_login,
    run_auth_logout,
    run_auth_rotate_key,
    run_auth_whoami,
    submit_generic_workflow,
    submit_video_job,
)

# -----------------------------------------------------------------------------
# CLI Helpers
# -----------------------------------------------------------------------------


class CustomHelpFormatter(argparse.RawDescriptionHelpFormatter):
    """Custom formatter that hides the redundant subparser list."""

    def _metavar_formatter(self, action, default_metavar):
        if action.choices is not None:
            result = ""

            def format(tuple_size):
                return (result,) * tuple_size

            return format
        return super()._metavar_formatter(action, default_metavar)

    def _format_action(self, action):
        if isinstance(action, argparse._SubParsersAction):
            return ""
        return super()._format_action(action)


class CustomArgumentParser(argparse.ArgumentParser):
    """Custom parser that prints help when an error occurs."""

    def error(self, message):
        sys.stderr.write(f"error: {message}\n")
        self.print_help()
        sys.exit(2)


def attach_custom_error(parser):
    """Monkey-patch error method to a parser instance."""

    def custom_error(self, message):
        sys.stderr.write(f"error: {message}\n")
        self.print_help()
        sys.exit(2)

    parser.error = types.MethodType(custom_error, parser)


# -----------------------------------------------------------------------------
# Authorization Helpers
# -----------------------------------------------------------------------------


def check_auth(
    command: str,
    customer_id: Optional[str] = None,
    require_auth: bool = True,
) -> Optional[User]:
    """
    Check if the current user is authorized for a command.

    Args:
        command: The command being executed (e.g., "submit", "query").
        customer_id: Optional customer ID for scoped commands.
        require_auth: If True, exit if not authenticated.

    Returns:
        The authenticated User, or None if auth is not required and not authenticated.
    """
    if os.environ.get("SXD_AUTH_DISABLED") == "1":
        return None

    user = get_current_user()

    # Commands that don't require authentication
    no_auth_commands = {"auth login", "auth whoami", "version", "help"}
    if command in no_auth_commands:
        return user

    if not user:
        if require_auth:
            print("Error: Not authenticated.")
            print()
            print("To authenticate:")
            print("  1. Set SXD_API_KEY environment variable, or")
            print("  2. Run 'sxd auth login'")
            sys.exit(1)
        return None

    set_user_context(user.id)
    if customer_id:
        set_customer_context(customer_id)

    auth = get_auth_manager()
    if not auth.check_command_permission(user, command, customer_id):
        perm = COMMAND_PERMISSIONS.get(command)
        perm_str = f"{perm[0]}:{perm[1]}" if perm else "unknown"

        print(f"Error: Permission denied for '{command}'")
        print(f"       Required permission: {perm_str}")
        if customer_id:
            print(f"       Customer: {customer_id}")

        log_audit_event(
            actor=user.to_actor_string(),
            action=command.replace(" ", "."),
            target=customer_id or "system",
            status="DENIED",
            details={"required_permission": perm_str},
        )
        sys.exit(1)

    return user


# -----------------------------------------------------------------------------
# Worker / Upload Commands
# -----------------------------------------------------------------------------


def run_worker(count: int | None = None, queues: list[str] | None = None):
    """Run the Temporal worker."""
    import multiprocessing

    if count is None:
        count = multiprocessing.cpu_count()

    tc = get_temporal_config()
    print(f"Starting worker connecting to {tc['host']}:{tc['port']}...")

    if tc["host"] not in ("localhost", "127.0.0.1"):
        os.environ["SXD_TEMPORAL_HOST"] = tc["host"]

    from sxd_core.worker import start_worker

    try:
        asyncio.run(
            start_worker(
                worker_count=count,
                temporal_host=tc["host"],
                temporal_port=tc["port"],
                pipeline_loader=lambda: load_pipelines(Path(__file__).parent),
                queues=queues,
            )
        )
    except (KeyboardInterrupt, asyncio.CancelledError):
        pass


def run_upload(
    path: str, customer_id: str, session_id: str | None = None, max_concurrent: int = 8
):
    """Upload file or folder with load-balanced distribution across workers.

    This is the operator-friendly upload that doesn't require SSH keys.
    Files are uploaded directly to worker nodes for data locality.
    Master only coordinates - no data flows through it.

    Flow:
    1. CLI sends file manifest to master
    2. Master computes load-balanced assignments (file → worker)
    3. CLI streams files in parallel directly to assigned workers
    4. CLI tells master to finalize, which triggers processing
    """
    import httpx

    source = Path(path).absolute()
    if not source.exists():
        print(f"Error: Path not found: {source}")
        sys.exit(1)

    # Get master URL from config or environment
    tc = get_temporal_config()
    master_host = tc.get("host", "localhost")
    master_url = os.getenv("SXD_MASTER_URL", f"http://{master_host}:8080")

    # Collect files to upload
    if source.is_file():
        files_to_upload = [source]
        base_path = source.parent
    else:
        files_to_upload = [f for f in source.rglob("*") if f.is_file()]
        base_path = source

    if not files_to_upload:
        print("Error: No files found to upload.")
        sys.exit(1)

    # Build file manifest for master
    file_manifest = []
    for f in files_to_upload:
        rel_path = str(f.relative_to(base_path))
        file_manifest.append({"path": rel_path, "size": f.stat().st_size})

    total_size = 0
    for item in file_manifest:
        total_size += int(str(item["size"]))
    print(f"Uploading {len(files_to_upload)} file(s) ({total_size / 1e9:.2f} GB)")
    print(f"  Customer: {customer_id}")
    print()

    async def _upload():
        nonlocal session_id
        # Get credentials
        user = get_current_user()
        if not user:
            print("Error: Authentication required for upload.")
            print("Run 'sxd auth login' or set SXD_API_KEY.")
            sys.exit(1)

        api_key = get_stored_api_key()

        if not api_key:
            print("Error: Could not retrieve API key for request headers.")
            sys.exit(1)

        headers = {"X-API-Key": api_key}

        async with httpx.AsyncClient(
            timeout=httpx.Timeout(None), headers=headers
        ) as client:
            if session_id:
                print(f"Resuming session: {session_id}")
                try:
                    resp = await client.get(
                        f"{master_url}/api/upload/{session_id}/resume"
                    )
                    resp.raise_for_status()
                except httpx.HTTPStatusError as e:
                    print(f"Error: Failed to resume session {session_id}: {e}")
                    sys.exit(1)
            else:
                # 1. Get session + file→worker assignments from master
                try:
                    resp = await client.post(
                        f"{master_url}/api/upload/init",
                        json={"customer_id": customer_id, "files": file_manifest},
                    )
                    resp.raise_for_status()
                except httpx.ConnectError:
                    print(f"Error: Cannot connect to master at {master_url}")
                    print("  Make sure the cluster is running (sxdinfra infra up)")
                    sys.exit(1)
                except httpx.HTTPStatusError as e:
                    print(f"Error: Init failed with status {e.response.status_code}")
                    print(f"  {e.response.text}")
                    sys.exit(1)

            data = resp.json()
            session_id = data["session_id"]
            assignments = data["assignments"]  # {node: {url, files, total_bytes}}
            upload_token = data["upload_token"]

            print(f"Session: {session_id}")
            for node, info in assignments.items():
                node_files = len(info["files"])
                node_bytes = info["total_bytes"]
                print(f"  → {node}: {node_files} files ({node_bytes / 1e9:.2f} GB)")
            print()

            # 2. Build path→(worker_url, local_path) mapping
            file_to_worker = {}
            for node, info in assignments.items():
                for file_path in info["files"]:
                    file_to_worker[file_path] = info["url"]

            # 3. Stream files to assigned workers (parallel)
            sem = asyncio.Semaphore(max_concurrent)
            uploaded = [0]  # Use list for nonlocal mutation
            failed = []

            async def upload_file(f: Path) -> bool:
                rel_path = str(f.relative_to(base_path))
                worker_url = file_to_worker.get(rel_path)
                if not worker_url:
                    print(f"  Warning: No worker assigned for {rel_path}")
                    return False

                async with sem:
                    try:
                        # Stream file content
                        file_size = f.stat().st_size

                        async def file_stream():
                            chunk_size = 4 * 1024 * 1024  # 4MB chunks
                            with open(f, "rb") as fp:
                                while chunk := fp.read(chunk_size):
                                    yield chunk

                        await client.put(
                            f"{worker_url}/upload/{session_id}/{rel_path}",
                            content=file_stream(),
                            headers={
                                "Content-Length": str(file_size),
                                "X-Upload-Token": upload_token,
                            },
                        )
                        resp.raise_for_status()

                        uploaded[0] += 1
                        size_mb = file_size / (1024 * 1024)
                        print(
                            f"  [{uploaded[0]}/{len(files_to_upload)}] {rel_path} ({size_mb:.1f} MB)"
                        )
                        return True

                    except Exception as e:
                        failed.append((rel_path, str(e)))
                        print(f"  [FAIL] {rel_path}: {e}")
                        return False

            # Upload all files concurrently
            await asyncio.gather(*[upload_file(f) for f in files_to_upload])

            if failed:
                print(f"\nWarning: {len(failed)} file(s) failed to upload")
                for path, err in failed[:5]:
                    print(f"  - {path}: {err}")
                if len(failed) > 5:
                    print(f"  ... and {len(failed) - 5} more")

            # 4. Tell master to finalize (triggers workers to process)
            try:
                resp = await client.post(
                    f"{master_url}/api/upload/{session_id}/complete"
                )
                resp.raise_for_status()
                result = resp.json()
            except Exception as e:
                print(f"\nError: Failed to complete session: {e}")
                print(f"  Session ID: {session_id}")
                print("  Files were uploaded but processing was not triggered.")
                print("  You may retry with: sxd upload --resume {session_id}")
                sys.exit(1)

            print()
            print("Upload complete!")
            print(f"  Session: {session_id}")
            print(f"  Episode: {result.get('episode_id', 'N/A')}")
            print(f"  Status: {result.get('status', 'processing')}")
            print(
                f"  Total: {total_size / 1e9:.2f} GB across {len(assignments)} worker(s)"
            )

    try:
        asyncio.run(_upload())
    except KeyboardInterrupt:
        print("\nUpload interrupted. Resume with:")
        print(f"  sxd upload {path} --customer-id {customer_id} --resume {session_id}")
        sys.exit(1)
    except Exception as e:
        print(f"Upload failed: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


async def run_submit(
    target: str, args: list, wait: bool = False, user: Optional[User] = None
):
    """Submit a job (generic or legacy video)."""
    actor = user.to_actor_string() if user else "user"

    if get_workflow(target):
        payload = " ".join(args) if args else "{}"
        try:
            data = json.loads(payload)
        except json.JSONDecodeError:
            data = {"input": payload}

        result = await submit_generic_workflow(target, data, wait=wait)
        print(f"+ Workflow {result['workflow_id']} - {result['status']}")
        if result.get("result"):
            print(f"Result: {result['result']}")

        log_audit_event(
            actor=actor,
            action="job.submit",
            target=result["workflow_id"],
            status="SUCCESS",
            details={"workflow": target},
        )
    else:
        url = target
        customer_id = args[0] if len(args) > 0 else "default"
        video_id = args[1] if len(args) > 1 else "auto"

        result = await submit_video_job(url, customer_id, video_id, wait)
        print(f"+ Workflow {result['workflow_id']} - {result['status']}")

        log_audit_event(
            actor=actor,
            action="job.submit",
            target=result["workflow_id"],
            status="SUCCESS",
            customer_id=customer_id,
            details={"video_id": video_id, "url": url},
        )


# -----------------------------------------------------------------------------
# Info / Status Commands (with --rich support)
# -----------------------------------------------------------------------------


def run_info(rich: bool = False):
    """Display cluster info."""
    info = get_cluster_info()
    tc = get_temporal_config()

    if rich:
        from sxd_core.tui import cluster_dashboard, console, print_error
        from sxd_core.tui.live import spinner

        with spinner("Loading cluster info..."):
            try:
                stats = get_24h_stats()
            except Exception as e:
                print_error(f"Failed to get cluster info: {e}")
                return

        console.print(cluster_dashboard(info, stats))
    else:
        print("SXD Cluster Information")
        print("-" * 50)
        print(f"Master: {info.master_host}")
        print(f"Temporal: {'connected' if info.temporal_connected else 'disconnected'}")
        print(
            f"ClickHouse: {'connected' if info.clickhouse_connected else 'disconnected'}"
        )

        print("\nServices:")
        for svc in info.services:
            icon = "+" if svc.status == "running" else "x"
            print(f"  [{icon}] {svc.display_name:<15} {svc.status}")

        print("\nEndpoints:")
        print(f"  Temporal UI:  http://{tc['host']}/")
        print(f"  Grafana:      http://{tc['host']}/grafana/")
        print("-" * 50)


def run_nodes(rich: bool = False):
    """Display cluster nodes with status."""
    nodes = get_node_status()

    if rich:
        from sxd_core.tui import console, format_nodes_table
        from sxd_core.tui.live import spinner

        with spinner("Checking node status..."):
            pass  # Already fetched

        if not nodes:
            console.print("[yellow]No nodes found in inventory.[/yellow]")
            return

        table = format_nodes_table(nodes)
        console.print(table)
    else:
        print("\nCluster Status:")
        print("-" * 50)
        for node in nodes:
            status = node.get("worker_status", "unknown")
            icon = "+" if status == "active" else "x" if status == "inactive" else "?"
            print(f"  [{icon}] {node['name']}: {status}")
        print("-" * 50)


def run_workers(rich: bool = False):
    """Display Temporal workers."""
    tc = get_temporal_config()

    try:
        workers = get_workers()
    except Exception as e:
        if rich:
            from sxd_core.tui import console, print_error

            print_error(f"Failed to connect to Temporal: {e}")
            console.print(
                "\n[dim]Make sure Temporal is running (sxdinfra infra up)[/dim]"
            )
        else:
            print(f"Error: {e}")
        return

    if rich:
        from rich.panel import Panel
        from sxd_core.tui import console, format_workers_table

        tree = format_workers_table(workers)
        console.print(
            Panel(
                tree,
                title="[bold blue]Temporal Workers[/bold blue]",
                border_style="blue",
            )
        )

        total_pollers = len(workers.activity_pollers)
        if total_pollers > 0:
            console.print(
                f"\n[green]OK[/green] {total_pollers} activity workers connected"
            )
        else:
            console.print("\n[red]X[/red] No workers connected")
    else:
        print(f"Checking workers on {tc['host']}:{tc['port']}...")

        print("\nWorkflow Pollers:")
        if workers.workflow_pollers:
            for p in workers.workflow_pollers:
                last = (
                    p.last_access_time.strftime("%H:%M:%S")
                    if p.last_access_time
                    else "unknown"
                )
                print(f"   + {p.identity} (last: {last})")
        else:
            print("   x No workflow pollers")

        print("\nActivity Pollers:")
        if workers.activity_pollers:
            for p in workers.activity_pollers:
                last = (
                    p.last_access_time.strftime("%H:%M:%S")
                    if p.last_access_time
                    else "unknown"
                )
                print(f"   + {p.identity} (last: {last})")
            print(f"\n{len(workers.activity_pollers)} workers connected")
        else:
            print("   x No activity pollers")


async def run_status(workflow_id: str, rich: bool = False):
    """Check workflow status."""
    status = get_workflow_status(workflow_id)

    if not status:
        if rich:
            from sxd_core.tui import print_error

            print_error(f"Workflow not found: {workflow_id}")
        else:
            print(f"Workflow not found: {workflow_id}")
        return

    if rich:
        from sxd_core.tui import console, workflow_status_panel

        panel = workflow_status_panel(status)
        console.print(panel)
    else:
        print(f"\nWorkflow: {workflow_id}")
        print(f"Status: {status.status}")
        print(f"Run ID: {status.run_id}")

        if status.start_time:
            print(f"Started: {status.start_time}")
        if status.close_time:
            print(f"Ended: {status.close_time}")

        if status.result:
            print("\nResult:")
            if isinstance(status.result, (dict, list)):
                print(json.dumps(status.result, indent=2))
            else:
                print(status.result)
        elif status.failure:
            print(f"\nFailure: {status.failure}")


def run_stats(rich: bool = False):
    """Display 24h statistics."""
    try:
        stats = get_24h_stats()
        errors = get_error_summary()
        storage = get_storage_stats()
    except Exception as e:
        if rich:
            from sxd_core.tui import print_error

            print_error(f"Failed to get statistics: {e}")
        else:
            print(f"Error: {e}")
        return

    if rich:
        from rich.table import Table
        from sxd_core.tui import console, stats_panel
        from sxd_core.tui.panels import error_summary_panel

        console.print(stats_panel(stats))

        if errors:
            console.print()
            console.print(error_summary_panel(errors))

        if storage:
            console.print()
            table = Table(title="Storage Usage", show_header=True, header_style="bold")
            table.add_column("Table", style="cyan")
            table.add_column("Size", justify="right")
            table.add_column("Rows", justify="right", style="muted")

            for s in storage:
                table.add_row(s.table, s.size_readable, f"{s.row_count:,}")

            console.print(table)
    else:
        print("\n24-Hour Statistics:")
        print("-" * 50)
        print(f"  Videos processed: {stats.videos_processed}")
        print(f"  Total duration:   {stats.total_duration_hours:.1f}h")
        print(f"  Success rate:     {stats.success_rate:.1f}%")
        print(f"  Errors:           {stats.error_count}")
        print("-" * 50)

        if storage:
            print("\nStorage Usage:")
            for s in storage:
                print(f"  {s.table:<20} {s.size_readable:>10} ({s.row_count:,} rows)")


# -----------------------------------------------------------------------------
# Query / Storage Commands
# -----------------------------------------------------------------------------


def run_query(query: str, format: str = "pretty", rich: bool = False):
    """Run a ClickHouse query."""
    from sxd_core.clickhouse import ClickHouseManager

    ch = ClickHouseManager()
    shortcuts = {
        "logs": f"SELECT timestamp, level, activity, message FROM {ch.database}.logs ORDER BY timestamp DESC LIMIT 50",
        "errors": f"SELECT timestamp, level, message FROM {ch.database}.logs WHERE level IN ('ERROR', 'WARNING') ORDER BY timestamp DESC LIMIT 50",
        "audit": f"SELECT timestamp, actor, action, target, status FROM {ch.database}.audit_events ORDER BY timestamp DESC LIMIT 50",
        "videos": f"SELECT * FROM {ch.database}.videos FINAL ORDER BY updated_at DESC LIMIT 20",
        "tables": f"SELECT table, formatReadableSize(sum(bytes_on_disk)) as size, sum(rows) as rows FROM system.parts WHERE active AND database = '{ch.database}' GROUP BY table ORDER BY sum(bytes_on_disk) DESC",
        "stats": f"SELECT (SELECT count() FROM {ch.database}.logs) as logs, (SELECT count() FROM {ch.database}.audit_events) as audit_events, (SELECT count() FROM {ch.database}.videos FINAL) as videos",
    }

    actual_query = shortcuts.get(query, query)

    if rich:
        from rich.json import JSON
        from rich.panel import Panel
        from rich.syntax import Syntax
        from rich.table import Table
        from sxd_core.tui import console, print_error
        from sxd_core.tui.live import spinner

        if query in shortcuts:
            console.print(
                Panel(
                    Syntax(actual_query, "sql", theme="monokai", word_wrap=True),
                    title="[bold]Query[/bold]",
                    border_style="dim",
                )
            )
            console.print()

        with spinner("Running query..."):
            try:
                results = ch.execute_query(actual_query)
            except Exception as e:
                print_error(f"Query failed: {e}")
                return

        if not results:
            console.print("[yellow]No results.[/yellow]")
            return

        if format == "json":
            console.print(JSON(json.dumps(results, indent=2, default=str)))
        else:
            import pandas as pd

            df = pd.DataFrame(results)
            table = Table(show_header=True, header_style="bold")
            for col in df.columns:
                table.add_column(str(col))
            for _, row in df.head(50).iterrows():
                table.add_row(*[str(v)[:50] for v in row])
            console.print(table)
            if len(df) > 50:
                console.print(f"[dim]... showing 50 of {len(df)} rows[/dim]")
    else:
        try:
            results = ch.execute_query(actual_query)
        except Exception as e:
            print(f"Query failed: {e}")
            sys.exit(1)

        if not results:
            print("No results.")
            return

        if format == "pretty":
            import pandas as pd

            print(pd.DataFrame(results).to_string(index=False))
        else:
            print(json.dumps(results, indent=2, default=str))


def run_ls(path: str = "", customer_id: Optional[str] = None, rich: bool = False):
    """List storage collections."""
    if rich:
        from rich.panel import Panel
        from sxd_core.tui import (
            console,
            format_batches_table,
            format_episodes_table,
            format_videos_table,
            print_error,
        )
        from sxd_core.tui.live import spinner

        if not path:
            console.print(
                Panel(
                    "[cyan]videos[/cyan]   - Processed videos\n"
                    "[cyan]batches[/cyan]  - Submitted batches\n"
                    "[cyan]uploads[/cyan]  - Upload episodes",
                    title="[bold]Available Collections[/bold]",
                    border_style="blue",
                )
            )
            return

        with spinner(f"Loading {path}..."):
            try:
                data: list  # type: ignore[type-arg]
                if path == "videos":
                    data = list_videos(limit=50, customer_id=customer_id)
                    table = format_videos_table(data, title=f"Videos ({len(data)})")
                elif path == "batches":
                    data = list_batches(limit=20, customer_id=customer_id)
                    table = format_batches_table(data, title=f"Batches ({len(data)})")
                elif path in ("uploads", "episodes"):
                    data = list_episodes(limit=20, customer_id=customer_id)
                    table = format_episodes_table(data, title=f"Uploads ({len(data)})")
                else:
                    print_error(f"Unknown collection: {path}")
                    console.print("[dim]Available: videos, batches, uploads[/dim]")
                    return
            except Exception as e:
                print_error(f"Failed to list {path}: {e}")
                return

        if not data:
            console.print(f"[yellow]No {path} found.[/yellow]")
            return

        console.print(table)
    else:
        if not path:
            print("Collections: videos, batches, uploads")
            return

        if path == "videos":
            for v in list_videos(limit=50, customer_id=customer_id):
                print(f"{v.video_id:<30} {v.status:<10} {v.source_url}")
        elif path == "batches":
            for b in list_batches(limit=20, customer_id=customer_id):
                print(f"{b.id:<36} {b.status:<12} {b.total_videos}")
        elif path == "uploads":
            for ep in list_episodes(limit=20, customer_id=customer_id):
                print(f"{ep.id:<36} {ep.status:<10} {ep.chunk_count}")
        else:
            print(f"Unknown: {path}. Try: videos, batches, uploads")


def run_cat(entity_id: str, rich: bool = False):
    """Display detailed info about an entity."""
    try:
        video = get_video_details(entity_id)
    except Exception as e:
        if rich:
            from sxd_core.tui import print_error

            print_error(f"Failed to get details: {e}")
        else:
            print(f"Error: {e}")
        return

    if rich:
        from rich.json import JSON
        from rich.panel import Panel
        from sxd_core.tui import console, print_error

        if video:
            console.print(
                Panel(
                    JSON(json.dumps(video, indent=2, default=str)),
                    title=f"[bold]Video: {entity_id}[/bold]",
                    border_style="cyan",
                )
            )
        else:
            print_error(f"Entity not found: {entity_id}")
    else:
        if video:
            print(json.dumps(video, indent=2, default=str))
        else:
            print(f"Entity not found: {entity_id}")


# -----------------------------------------------------------------------------
# Pipeline Publishing (for SDK users)
# -----------------------------------------------------------------------------


def load_sxd_yaml(path: Path) -> dict:
    """Load and parse sxd.yaml from a pipeline directory.

    Minimal sxd.yaml schema:
        base_image: sxd-opencv   # Required
        timeout: 3600            # Optional (default: 3600)
        gpu: false               # Optional (default: false)
    """
    import yaml

    yaml_path = path / "sxd.yaml"
    if not yaml_path.exists():
        return {}

    with open(yaml_path) as f:
        return yaml.safe_load(f) or {}


def get_pipeline_name(path: Path) -> str:
    """Extract pipeline name from pyproject.toml or directory name."""
    pyproject = path / "pyproject.toml"
    if pyproject.exists():
        try:
            import tomllib

            with open(pyproject, "rb") as f:
                data = tomllib.load(f)
            name = data.get("project", {}).get("name", "")
            # Strip 'sxd-' prefix if present
            if name.startswith("sxd-"):
                name = name[4:]
            if name:
                return name
        except Exception:
            pass
    return path.name


def run_publish(
    path: str = ".",
    tag: str = "latest",
    dry_run: bool = False,
    user: Optional[User] = None,
):
    """Publish a pipeline to the SXD cluster.

    Reads sxd.yaml for configuration, bundles the pipeline,
    builds Docker image, and registers with the cluster.
    """
    import io
    import tarfile

    p = Path(path).absolute()

    if not p.exists():
        print(f"Error: Path not found: {p}")
        sys.exit(1)

    # Load configuration
    config = load_sxd_yaml(p)
    name = get_pipeline_name(p)
    base_image = config.get("base_image", "sxd-base")
    timeout = config.get("timeout", 3600)
    gpu = config.get("gpu", False)

    print(f"Publishing pipeline: {name}")
    print(f"  Path: {p}")
    print(f"  Base image: {base_image}")
    print(f"  Timeout: {timeout}s")
    print(f"  GPU: {gpu}")
    print()

    # Validate required files
    if not (p / "pyproject.toml").exists():
        print("Error: No pyproject.toml found. Is this a pipeline directory?")
        sys.exit(1)

    if dry_run:
        print("[Dry run] Would publish pipeline to cluster")
        return

    # Build Docker image
    dockerfile = p / "Dockerfile"
    registry = os.getenv("SXD_REGISTRY", "ghcr.io/sentient-x")
    image_tag = f"{registry}/{name}:{tag}"

    if not dockerfile.exists():
        print("Generating Dockerfile...")
        dockerfile_content = f"""FROM {registry}/sxd-{base_image}:latest

WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -e .

CMD ["python", "-m", "sxd_core.worker"]
"""
        dockerfile.write_text(dockerfile_content)

    print(f"Building image: {image_tag}")
    docker_result = subprocess.run(
        ["docker", "build", "-t", image_tag, str(p)],
        capture_output=False,
    )
    if docker_result.returncode != 0:
        print("Error: Docker build failed")
        sys.exit(1)

    # Push to registry
    print("Pushing to registry...")
    push_result = subprocess.run(
        ["docker", "push", image_tag],
        capture_output=True,
        text=True,
    )
    if push_result.returncode != 0:
        print(f"Warning: Push failed (may need docker login): {push_result.stderr}")

    # Bundle pipeline code
    print("Creating pipeline bundle...")
    bundle = io.BytesIO()
    with tarfile.open(fileobj=bundle, mode="w:gz") as tar:
        for item in p.iterdir():
            if item.name.startswith(".") or item.name in (
                "__pycache__",
                "dist",
                "build",
            ):
                continue
            tar.add(item, arcname=item.name)
    bundle_bytes = bundle.getvalue()
    print(f"  Bundle size: {len(bundle_bytes) / 1024:.1f} KB")

    # Register with cluster (via master node API or direct)
    tc = get_temporal_config()
    master_host = tc.get("host", "localhost")

    print(f"Registering with cluster at {master_host}...")

    # Persist metadata to ClickHouse
    from sxd_core.registry import register_pipeline_metadata
    from sxd_sdk.pipeline import load_pipeline_config
    
    try:
        reg_config = load_pipeline_config(p / "sxd.yaml")
    except Exception:
        # Fallback if sxd.yaml is missing or invalid
        from sxd_sdk.pipeline import PipelineConfig
        reg_config = PipelineConfig(name=name, description=config.get("description", ""), base_image=base_image, timeout=timeout, gpu=gpu)
    
    register_pipeline_metadata(reg_config)

    actor = user.to_actor_string() if user else "user"
    log_audit_event(
        actor=actor,
        action="pipeline.publish",
        target=name,
        status="SUCCESS",
        details={"image": image_tag, "base_image": base_image},
    )

    print()
    print(f"Pipeline published: {name}")
    print(f"  Image: {image_tag}")
    print(f"  Submit jobs with: sxd submit {name} '<input_json>'")


# -----------------------------------------------------------------------------
# Workflow Commands
# -----------------------------------------------------------------------------


def run_list_workflows():
    """List registered workflows."""
    workflows = list_workflows()
    if not workflows:
        print("No workflows registered.")
        return

    print(f"{'NICKNAME':<20} {'QUEUE':<20} {'DESCRIPTION'}")
    print("-" * 60)
    for nick, wf in workflows.items():
        desc = (wf.description or "").split("\n")[0][:40]
        print(f"{nick:<20} {wf.task_queue:<20} {desc}")


# -----------------------------------------------------------------------------
# Maintenance Commands
# -----------------------------------------------------------------------------


def run_clean():
    """Clean build artifacts."""
    patterns = [
        "**/__pycache__",
        "**/*.pyc",
        ".pytest_cache",
        "scratch/*",
        "build/",
        "dist/",
        "*.egg-info",
    ]
    for pattern in patterns:
        for path in Path(".").glob(pattern):
            if path.is_file():
                path.unlink()
            elif path.is_dir():
                shutil.rmtree(path)
            print(f"Removed {path}")


def run_tidy():
    """Run repo hygiene checks: ruff fix, black format, and mypy."""
    print("Running repo hygiene checks...")

    print("\n1. Running ruff check --fix...")
    try:
        subprocess.run(["uv", "run", "ruff", "check", ".", "--fix"], check=True)
        print("   + Ruff fixes applied")
    except subprocess.CalledProcessError as e:
        print(f"   ! Ruff encountered issues (exit code {e.returncode})")

    print("\n2. Running black formatter...")
    try:
        subprocess.run(["uv", "run", "black", "."], check=True)
        print("   + Code formatted with black")
    except subprocess.CalledProcessError as e:
        print(f"   x Black failed (exit code {e.returncode})")
        sys.exit(1)

    print("\n3. Running mypy type checker...")
    try:
        subprocess.run(["uv", "run", "mypy", "."], check=True)
        print("   + Type checking passed")
    except subprocess.CalledProcessError as e:
        print(f"   ! MyPy found type issues (exit code {e.returncode})")

    print("\nTidy complete!")


# -----------------------------------------------------------------------------
# Interactive Explore (TUI only)
# -----------------------------------------------------------------------------


def run_explore():
    """Launch interactive file explorer."""
    from sxd_core.tui import console, print_error
    from sxd_core.tui.explorer_textual import run_explorer

    try:
        run_explorer()
    except Exception as e:
        print_error(f"Explorer failed: {e}")
        import traceback

        console.print(f"[dim]{traceback.format_exc()}[/dim]")


# -----------------------------------------------------------------------------
# Main Entry Point
# -----------------------------------------------------------------------------


def main():
    help_text = textwrap.dedent(
        """
    ░██████╗░██╗░░██╗░██████╗░
    ██╔════╝░╚██╗██╔╝░██╔══██╗
    ╚█████╗░░░╚███╔╝░░██║░░██║
    ░╚═══██╗░░██╔██╗░░██║░░██║
    ██████╔╝░██╔╝╚██╗░██████╔╝
    ╚═════╝░░╚═╝░░╚═╝░╚═════╝░
    ──────────────────────────
    Pipeline Development & Operations

    DEVELOP (Pipeline Authors):
      publish    Publish pipeline to cluster
      workflows  List registered pipelines

    OPERATE (Data Operators):
      upload     Upload data to cluster (via HTTP)
      submit     Submit a job (workflow name + input)
      status     Check workflow status

    OBSERVE (Everyone):
      info       Show cluster status
      stats      Show 24h statistics
      ls         List collections (videos, batches, uploads)
      cat        View entity details
      query      Run ClickHouse queries
      workers    Show Temporal workers
      nodes      Show node status

    Auth:
      auth       Personal authentication (login/logout/whoami)

    Dev Tools:
      tidy       Run linters (ruff, black, mypy)
      clean      Clean build artifacts
      worker     Run local processing worker

    Use --rich flag for enhanced TUI output.
    For infrastructure management, use sxdinfra.
    """
    )

    parser = CustomArgumentParser(
        description=help_text, formatter_class=CustomHelpFormatter
    )

    load_pipelines(Path(__file__).parent)

    # Global --rich flag
    parser.add_argument(
        "--rich", action="store_true", help="Use rich TUI output (tables, colors)"
    )

    subparsers = parser.add_subparsers(dest="command", metavar="")

    # --- Jobs ---
    p_submit = subparsers.add_parser("submit", help="Submit job")
    p_submit.add_argument("target", help="Workflow name or URL")
    p_submit.add_argument("--customer", "-c", help="Customer ID")
    p_submit.add_argument("args", nargs=argparse.REMAINDER)
    attach_custom_error(p_submit)

    p_upload = subparsers.add_parser("upload", help="Upload data")
    p_upload.add_argument("path")
    p_upload.add_argument("--customer-id", "-c", default="default")
    p_upload.add_argument("--resume", help="Resume a failed session by ID")
    p_upload.add_argument("--concurrency", type=int, default=8)
    attach_custom_error(p_upload)

    p_status = subparsers.add_parser("status", help="Check workflow status")
    p_status.add_argument("workflow_id")
    p_status.add_argument("--rich", action="store_true", help="Rich output")
    attach_custom_error(p_status)

    p_worker = subparsers.add_parser("worker", help="Run worker")
    p_worker.add_argument("count", type=int, nargs="?", help="Worker count")
    p_worker.add_argument(
        "--queue", "-q", action="append", help="Task queue(s) to listen on"
    )
    attach_custom_error(p_worker)

    subparsers.add_parser("workflows", help="List workflows")

    # --- Pipeline Publishing (for SDK users) ---
    p_publish = subparsers.add_parser("publish", help="Publish pipeline to cluster")
    p_publish.add_argument("path", nargs="?", default=".", help="Pipeline directory")
    p_publish.add_argument("--tag", "-t", default="latest", help="Image tag")
    p_publish.add_argument(
        "--dry-run", action="store_true", help="Show what would happen"
    )
    attach_custom_error(p_publish)

    # --- Data ---
    p_query = subparsers.add_parser("query", help="ClickHouse query")
    p_query.add_argument("query")
    p_query.add_argument("--format", choices=["pretty", "json"], default="pretty")
    p_query.add_argument("--rich", action="store_true", help="Rich output")
    attach_custom_error(p_query)

    p_ls = subparsers.add_parser("ls", help="List storage")
    p_ls.add_argument("path", nargs="?", default="")
    p_ls.add_argument("--customer", "-c", help="Filter by customer ID")
    p_ls.add_argument("--rich", action="store_true", help="Rich output")
    attach_custom_error(p_ls)

    p_cat = subparsers.add_parser("cat", help="View entity details")
    p_cat.add_argument("entity_id", help="Entity ID (video_id, etc.)")
    p_cat.add_argument("--rich", action="store_true", help="Rich output")
    attach_custom_error(p_cat)

    # --- Cluster ---
    p_info = subparsers.add_parser("info", help="Show cluster info")
    p_info.add_argument("--rich", action="store_true", help="Rich output")
    attach_custom_error(p_info)

    p_nodes = subparsers.add_parser("nodes", help="Show node status")
    p_nodes.add_argument("--rich", action="store_true", help="Rich output")
    attach_custom_error(p_nodes)

    p_workers_cmd = subparsers.add_parser("workers", help="Show Temporal workers")
    p_workers_cmd.add_argument("--rich", action="store_true", help="Rich output")
    attach_custom_error(p_workers_cmd)

    p_stats = subparsers.add_parser("stats", help="Show 24h statistics")
    p_stats.add_argument("--rich", action="store_true", help="Rich output")
    attach_custom_error(p_stats)

    # --- Auth ---
    p_auth = subparsers.add_parser("auth", help="Authentication")
    auth_subs = p_auth.add_subparsers(dest="auth_command")
    auth_subs.add_parser("login", help="Save API key")
    auth_subs.add_parser("logout", help="Remove saved credentials")
    auth_subs.add_parser("whoami", help="Show current user")
    auth_subs.add_parser("rotate-key", help="Rotate user API key")
    attach_custom_error(p_auth)

    # --- Maintenance ---
    subparsers.add_parser("tidy", help="Run ruff, black, mypy")
    subparsers.add_parser("clean", help="Clean artifacts")
    subparsers.add_parser("explore", help="Interactive file explorer (TUI)")

    # --- Scaffold (Developer Tools) ---
    p_scaffold = subparsers.add_parser("scaffold", help="Scaffold new projects")
    scaffold_subs = p_scaffold.add_subparsers(dest="scaffold_command")

    p_scaffold_pl = scaffold_subs.add_parser("pipeline", help="Create new pipeline")
    p_scaffold_pl.add_argument("name", help="Pipeline name (e.g. video-processor)")
    p_scaffold_pl.add_argument(
        "--dir", "-d", default="packages/pipelines", help="Output directory"
    )
    p_scaffold_pl.add_argument("--desc", default="", help="Description")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    # Determine rich flag (global or command-specific)
    use_rich = getattr(args, "rich", False)

    try:
        command = args.command
        if args.command == "auth" and hasattr(args, "auth_command"):
            command = f"auth {args.auth_command}"

        customer_id = None
        if hasattr(args, "customer") and args.customer:
            customer_id = args.customer
        elif hasattr(args, "customer_id") and args.customer_id:
            customer_id = args.customer_id

        user = None
        if args.command != "auth":
            user = check_auth(command, customer_id)

        # Execute command
        if args.command == "submit":
            wait = "--wait" in args.args
            remaining = [a for a in args.args if a != "--wait"]
            asyncio.run(run_submit(args.target, remaining, wait, user))
        elif args.command == "upload":
            run_upload(args.path, args.customer_id, args.resume, args.concurrency)
        elif args.command == "status":
            asyncio.run(run_status(args.workflow_id, use_rich))
        elif args.command == "worker":
            run_worker(args.count, args.queue)
        elif args.command == "workflows":
            run_list_workflows()
        elif args.command == "publish":
            run_publish(args.path, args.tag, args.dry_run, user)
        elif args.command == "query":
            run_query(args.query, args.format, use_rich)
        elif args.command == "ls":
            run_ls(args.path, customer_id, use_rich)
        elif args.command == "cat":
            run_cat(args.entity_id, use_rich)
        elif args.command == "info":
            run_info(use_rich)
        elif args.command == "nodes":
            run_nodes(use_rich)
        elif args.command == "workers":
            run_workers(use_rich)
        elif args.command == "stats":
            run_stats(use_rich)
        elif args.command == "auth":
            if args.auth_command == "login":
                run_auth_login()
            elif args.auth_command == "logout":
                run_auth_logout()
            elif args.auth_command == "whoami" or args.auth_command is None:
                run_auth_whoami()
            elif args.auth_command == "rotate-key":
                run_auth_rotate_key(None)
        elif args.command == "tidy":
            run_tidy()
        elif args.command == "clean":
            run_clean()
        elif args.command == "explore":
            run_explore()
        elif args.command == "scaffold":
            if args.scaffold_command == "pipeline":
                from sxd_sdk.scaffold import scaffold_pipeline

                out_dir = Path(args.dir)
                # If default directory doesn't exist, create it or fallback to current dir?
                # Better to just use what's passed or default relative to cwd.
                # Assuming running from repo root.

                print(f"Scaffolding pipeline '{args.name}' in {out_dir}...")
                scaffold_pipeline(args.name, out_dir, args.desc)
                print(
                    f"Done! Created {args.name} in {out_dir}/{args.name.replace('-', '_')}"
                )

    except KeyboardInterrupt:
        print("\nCancelled.")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
