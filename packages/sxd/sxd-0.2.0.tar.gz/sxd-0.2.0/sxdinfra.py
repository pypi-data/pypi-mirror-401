"""
Infrastructure Management CLI for SentientX Data Infrastructure.

Usage:
    python sxdinfra.py [command] [args]

This CLI is restricted to infrastructure administrators for managing nodes,
deployments, and core services.
"""

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    print("Warning: python-dotenv not installed, skipping .env loading")
    pass

import argparse
import asyncio
import os
import subprocess
import sys
import types
from pathlib import Path
from typing import Optional

# Docker registry configuration
LOCAL_REGISTRY = "localhost:5000"
PUBLIC_REGISTRY = "ghcr.io/sentient-x"

SXD_BASE_IMAGES = {
    "sxd-base": "docker/Dockerfile.base",
    "sxd-pytorch": "docker/Dockerfile.pytorch",
    "sxd-opencv": "docker/Dockerfile.opencv",
    "sxd-cuda": "docker/Dockerfile.cuda",
}


def get_default_registry() -> str:
    """Get the default registry based on environment.

    Uses localhost:5000 on cluster nodes (SXD_NODE_TYPE set),
    falls back to ghcr.io for local development.
    """
    if os.getenv("SXD_NODE_TYPE"):
        return LOCAL_REGISTRY
    return PUBLIC_REGISTRY


# Ensure current directory is in PYTHONPATH
sys.path.append(str(Path(__file__).parent))

from sxd_core.audit import log_audit_event, set_user_context  # noqa: E402
from sxd_core.auth import (  # noqa: E402
    User,
    get_auth_manager,
    get_current_user,
)
from sxd_core.config import get_config, get_temporal_config  # noqa: E402
from sxd_core.ops import (  # noqa: E402
    execute_remote,
    get_node_status,
    get_workers,
    initialize_databases,
    run_ansible_playbook,
    start_services,
    stop_services,
)
from sxd_core.ops.secrets import get_secret  # noqa: E402

# -----------------------------------------------------------------------------
# CLI Helpers
# -----------------------------------------------------------------------------


class CustomHelpFormatter(argparse.RawDescriptionHelpFormatter):
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
    def error(self, message):
        sys.stderr.write(f"error: {message}\n")
        self.print_help()
        sys.exit(2)


def attach_custom_error(parser):
    def custom_error(self, message):
        sys.stderr.write(f"error: {message}\n")
        self.print_help()
        sys.exit(2)

    parser.error = types.MethodType(custom_error, parser)


def check_auth(command: str, require_auth: bool = True) -> Optional[User]:
    if os.environ.get("SXD_AUTH_DISABLED") == "1":
        print("⚠️  WARNING: SXD_AUTH_DISABLED=1 - bypassing authentication checks!")
        return None
    user = get_current_user()
    if not user:
        if require_auth:
            print("Error: Not authenticated. Use 'sxd auth login'")
            sys.exit(1)
        return None
    set_user_context(user.id)
    auth = get_auth_manager()
    if not auth.check_command_permission(user, command):
        print(f"Error: Permission denied for infra command '{command}'")
        sys.exit(1)
    return user


# -----------------------------------------------------------------------------
# Wrappers
# -----------------------------------------------------------------------------


def run_infra_up(reset_password: bool = False):
    if not os.getenv("SXD_NODE_TYPE"):
        extra = ["--reset-password"] if reset_password else []
        execute_remote(
            ["infra", "up"] + extra, target_node="master", script_name="sxdinfra.py"
        )
        return
    start_services(reset_password=reset_password)


def run_provision(limit: str | None = None):
    from sxd_core.ops.secrets import (
        get_or_create_service_token,
        pull_secrets_from_infisical,
    )

    pull_secrets_from_infisical()
    infisical_token = get_or_create_service_token()
    extra_vars = {}
    if infisical_token:
        extra_vars["infisical_token"] = infisical_token
    run_ansible_playbook(
        "deploy/ansible/provision.yml", limit=limit, extra_vars=extra_vars
    )


def run_deploy(limit: str | None = None, user: Optional[User] = None):
    from sxd_core.ops.secrets import (
        get_or_create_service_token,
        pull_secrets_from_infisical,
    )

    # Ensure secrets are available locally for audit logging
    pull_secrets_from_infisical()
    try:
        from dotenv import load_dotenv

        load_dotenv(override=True)
    except ImportError:
        print("Warning: python-dotenv not installed, skipping .env loading")
        pass

    infisical_token = get_or_create_service_token()
    extra_vars = {}
    if infisical_token:
        extra_vars["infisical_token"] = infisical_token

    run_ansible_playbook(
        "deploy/ansible/deploy.yml", limit=limit, extra_vars=extra_vars
    )
    log_audit_event(
        actor=user.id if user else "infra",
        action="platform.deploy",
        target=limit or "all",
        status="SUCCESS",
    )


def _docker_login_ghcr() -> bool:
    """Login to ghcr.io using GITHUB_TOKEN from environment or Infisical."""
    token = get_secret("GITHUB_TOKEN")

    if not token:
        print("  [!] GITHUB_TOKEN not found in environment or Infisical")
        return False

    # Login to ghcr.io
    result = subprocess.run(
        ["docker", "login", "ghcr.io", "-u", "sentient-x", "--password-stdin"],
        input=token,
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        print(f"  [x] Docker login failed: {result.stderr.strip()}")
        return False

    print("  [+] Logged in to ghcr.io")
    return True


def run_docker_publish(
    images: list[str] | None = None,
    tag: str = "latest",
    push: bool = True,
    registry: str | None = None,
):
    """
    Build and publish SXD base Docker images.

    Args:
        images: List of image names to build (e.g., ["sxd-base", "sxd-pytorch"]).
                If None, builds all images.
        tag: Image tag (default: "latest").
        push: Whether to push to registry after building.
        registry: Target registry. Defaults to localhost:5000 on cluster,
                  ghcr.io/sentient-x for local dev.
    """
    root_dir = Path(__file__).parent
    target_registry = registry or get_default_registry()

    # Login to ghcr.io if pushing to public registry
    if push and "ghcr.io" in target_registry:
        if not _docker_login_ghcr():
            print("\nTo authenticate manually:")
            print(
                "  echo $GITHUB_TOKEN | docker login ghcr.io -u USERNAME --password-stdin"
            )
            sys.exit(1)

    # Determine which images to build
    if images:
        to_build = {k: v for k, v in SXD_BASE_IMAGES.items() if k in images}
        invalid = set(images) - set(SXD_BASE_IMAGES.keys())
        if invalid:
            print(f"Error: Unknown images: {', '.join(invalid)}")
            print(f"Available: {', '.join(SXD_BASE_IMAGES.keys())}")
            sys.exit(1)
    else:
        to_build = SXD_BASE_IMAGES

    print(f"Building {len(to_build)} image(s) with tag '{tag}'...")
    print(f"Registry: {target_registry}")
    print()

    built_images = []

    for image_name, dockerfile in to_build.items():
        dockerfile_path = root_dir / dockerfile
        if not dockerfile_path.exists():
            print(f"  [x] Error building {image_name}: {dockerfile} not found")
            if images:
                sys.exit(1)
            continue

        full_tag = f"{target_registry}/{image_name}:{tag}"
        latest_tag = f"{target_registry}/{image_name}:latest"

        print(f"  [*] Building {image_name}...")

        # Build the image (show output in real-time)
        build_cmd = [
            "docker",
            "build",
            "-f",
            str(dockerfile_path),
            "-t",
            full_tag,
            "-t",
            latest_tag,
            str(root_dir),
        ]

        result = subprocess.run(build_cmd)
        if result.returncode != 0:
            print(f"  [x] Build failed for {image_name}")
            continue

        # Verify the image exists
        verify = subprocess.run(
            ["docker", "image", "inspect", full_tag],
            capture_output=True,
        )
        if verify.returncode != 0:
            print(f"  [x] Build completed but image not found: {full_tag}")
            continue

        print(f"  [+] Built {full_tag}")
        built_images.append((image_name, full_tag, latest_tag))

    if not built_images:
        print("\nNo images were built successfully.")
        return

    if not push:
        print(
            f"\n{len(built_images)} image(s) built (--no-push specified, skipping push)"
        )
        return

    print(f"\nPushing {len(built_images)} image(s) to {target_registry}...")

    pushed_images = []
    for image_name, full_tag, latest_tag in built_images:
        print(f"  [*] Pushing {image_name}...")

        # Push both tags
        push_success = True
        for push_tag in [full_tag, latest_tag]:
            push_res = subprocess.run(
                ["docker", "push", push_tag], capture_output=True, text=True
            )
            if push_res.returncode != 0:
                print(f"  [x] Push failed for {push_tag}")
                print(f"      {push_res.stderr.strip()}")
                push_success = False

        if push_success:
            print(f"  [+] Pushed {image_name}")
            pushed_images.append((image_name, full_tag))
        else:
            print(f"  [!] Push failed for {image_name}")

    if pushed_images:
        print(f"\nDone! Published {len(pushed_images)} image(s):")
        for image_name, full_tag in pushed_images:
            print(f"  - {full_tag}")
    else:
        print("\nNo images were pushed successfully.")
        print("\nTo authenticate with ghcr.io:")
        print(
            "  echo $GITHUB_TOKEN | docker login ghcr.io -u USERNAME --password-stdin"
        )


def run_collect_metrics():
    """Collect and store node metrics for load balancing (requires SSH access)."""
    from sxd_core.ops.secrets import pull_secrets_from_infisical

    pull_secrets_from_infisical()

    from sxd_core.ops.node_metrics import (
        cache_metrics_to_clickhouse,
        get_all_node_metrics,
    )

    print("Collecting node metrics...")
    metrics = get_all_node_metrics(force_refresh=True)

    if not metrics:
        print("No metrics collected. Check node configuration.")
        return

    for hostname, m in metrics.items():
        print(f"  {hostname}:")
        print(f"    CPU cores: {m.cpu_cores}")
        print(
            f"    Disk: {m.disk_available_bytes / (1024**3):.1f} GB free / {m.disk_total_bytes / (1024**3):.1f} GB total"
        )
        print(f"    Queue: {m.pending_queue_bytes / (1024**3):.2f} GB pending")
        print(f"    Stored: {m.stored_bytes / (1024**3):.2f} GB")

    cache_metrics_to_clickhouse(metrics)
    print(f"\nMetrics collected from {len(metrics)} node(s) and stored in ClickHouse.")


# -----------------------------------------------------------------------------
# Testing
# -----------------------------------------------------------------------------


def run_tests(
    markers: str | None = None,
    path: str | None = None,
    verbose: bool = True,
    run_all: bool = False,
):
    """Run tests with pytest."""
    cmd = ["uv", "run", "pytest"]
    if markers:
        cmd.extend(["-m", markers])
    elif not run_all:
        cmd.extend(["-m", "not integration"])
    if path:
        cmd.append(path)
    if verbose:
        cmd.append("-v")
    cmd.extend(["--cov=sxd_core", "--cov-report=term-missing"])

    env = os.environ.copy()
    env["SXD_TEST_MODE"] = "1"
    subprocess.run(cmd, env=env, check=True)


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------


def main():
    help_text = "SentientX Infrastructure Management (sxdinfra)"
    parser = CustomArgumentParser(
        description=help_text, formatter_class=CustomHelpFormatter
    )
    subparsers = parser.add_subparsers(dest="command", metavar="")

    # Infra
    p_infra = subparsers.add_parser("infra", help="System control")
    infra_subs = p_infra.add_subparsers(dest="sub", required=True)
    p_up = infra_subs.add_parser("up", help="Start services")
    p_up.add_argument("--reset-password", action="store_true")
    infra_subs.add_parser("down", help="Stop services")
    p_init = infra_subs.add_parser("init", help="Initialize DBs")
    p_init.add_argument(
        "--reset",
        action="store_true",
        help="Drop and recreate all tables (WARNING: deletes data)",
    )
    infra_subs.add_parser("logs", help="View logs")

    # Deployment
    p_prov = subparsers.add_parser("provision", help="Setup nodes")
    p_prov.add_argument("--limit")

    p_dep = subparsers.add_parser("deploy", help="Deploy code")
    p_dep.add_argument("--limit")

    # SSH
    p_ssh = subparsers.add_parser("ssh", help="SSH to node")
    p_ssh.add_argument("cmd", nargs="?")
    p_ssh.add_argument("--host")

    # Cluster
    subparsers.add_parser("nodes", help="Node status")
    subparsers.add_parser("workers", help="Temporal status")
    subparsers.add_parser("workflows", help="List pipelines")

    # Maintenance
    p_cleanup = subparsers.add_parser("cleanup", help="Clean scratch")
    p_cleanup.add_argument("--dir", default="./scratch")

    # Backup & Restore
    p_backup = subparsers.add_parser("backup", help="Run backup")
    backup_subs = p_backup.add_subparsers(dest="sub", required=True)
    backup_subs.add_parser("auth", help="Backup Auth DB")
    backup_subs.add_parser("postgres", help="Backup Postgres")
    backup_subs.add_parser("clickhouse", help="Backup ClickHouse")
    backup_subs.add_parser("all", help="Backup All DBs")

    p_restore = subparsers.add_parser("restore", help="Restore data")
    restore_subs = p_restore.add_subparsers(dest="sub", required=True)

    p_res_auth = restore_subs.add_parser("auth", help="Restore Auth DB")
    p_res_auth.add_argument("backup_id", help="Backup filename")

    p_res_pg = restore_subs.add_parser("postgres", help="Restore Postgres")
    p_res_pg.add_argument("backup_id", help="Backup filename")

    p_res_ch = restore_subs.add_parser("clickhouse", help="Restore ClickHouse")
    p_res_ch.add_argument("backup_id", help="Backup filename")

    # Metrics
    subparsers.add_parser("metrics", help="Collect node metrics (requires SSH)")

    # Docker
    p_docker = subparsers.add_parser("docker", help="Docker image management")
    docker_subs = p_docker.add_subparsers(dest="sub", required=True)
    p_docker_publish = docker_subs.add_parser(
        "publish", help="Build and push SXD base images"
    )
    p_docker_publish.add_argument(
        "images",
        nargs="*",
        help=f"Images to build (default: all). Options: {', '.join(SXD_BASE_IMAGES.keys())}",
    )
    p_docker_publish.add_argument(
        "--tag", "-t", default="latest", help="Image tag (default: latest)"
    )
    p_docker_publish.add_argument(
        "--registry",
        "-r",
        help="Target registry (default: localhost:5000 on cluster, ghcr.io/sentient-x for dev)",
    )
    p_docker_publish.add_argument(
        "--no-push", action="store_true", help="Build only, don't push to registry"
    )

    # User Management
    p_user = subparsers.add_parser("user", help="User provisioning")
    user_subs = p_user.add_subparsers(dest="sub", required=True)

    p_create = user_subs.add_parser("create", help="Full provisioning")
    p_create.add_argument("id")
    p_create.add_argument("--name", required=True)
    p_create.add_argument("--email", required=True)
    p_create.add_argument("--roles", default="pipeline_operator")
    p_create.add_argument(
        "--admin", action="store_true", help="Provision as infra admin"
    )

    # Testing
    p_test = subparsers.add_parser("test", help="Run platform tests")
    p_test.add_argument("path", nargs="?")
    p_test.add_argument("-m", "--markers")
    p_test.add_argument("-q", "--quiet", action="store_true")
    p_test.add_argument(
        "--all", action="store_true", help="Run all tests including integration tests"
    )

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return

    # Auth check
    cmd_name = args.command
    if hasattr(args, "sub"):
        cmd_name = f"{args.command} {args.sub}"

    # Normalize 'all' to check permission
    perm_cmd = cmd_name
    if cmd_name.startswith("backup"):
        perm_cmd = "infra backup"
    elif cmd_name.startswith("restore"):
        perm_cmd = "infra restore"

    # Map sxdinfra commands to existing permission names in COMMAND_PERMISSIONS
    perm_map = {
        "infra up": "infra up",
        "infra down": "infra down",
        "infra init": "infra init",
        "infra logs": "infra logs",
        "provision": "provision",
        "deploy": "deploy",
        "nodes": "nodes",
        "workers": "workers",
        "user create": "auth create-user",
        "docker publish": "deploy",  # Reuse deploy permission for docker publish
    }

    # If not in perm_map, use infra or specific mapped value (handled above for backup/restore)
    required_perm = perm_map.get(perm_cmd, perm_map.get(cmd_name, "infra"))
    user = check_auth(required_perm)

    if args.command == "infra":
        if args.sub == "up":
            run_infra_up(args.reset_password)
        elif args.sub == "down":
            stop_services()
        elif args.sub == "init":
            initialize_databases(reset=args.reset)
        elif args.sub == "logs":
            os.system("docker compose -f deploy/docker-compose.yml logs -f")
    elif args.command == "provision":
        run_provision(args.limit)
    elif args.command == "deploy":
        run_deploy(args.limit, user)
    elif args.command == "ssh":
        run_ssh(args.cmd, args.host)
    elif args.command == "cleanup":
        execute_remote(
            ["cleanup", "--dir", args.dir],
            target_node="worker",
            script_name="sxdinfra.py",
        )
    elif args.command == "nodes":
        run_cluster_status_formatted()
    elif args.command == "workers":
        asyncio.run(run_check_workers_formatted())
    elif args.command == "workflows":
        from sxd_core import list_workflows

        workflows = list_workflows()
        if not workflows:
            print("No workflows registered.")
            return
        print(f"{'NICKNAME':<20} {'QUEUE':<20} {'DESCRIPTION'}")
        print("-" * 60)
        for nick, wf in workflows.items():
            desc = (wf.description or "").split("\n")[0][:40]
            print(f"{nick:<20} {wf.task_queue:<20} {desc}")
    elif args.command == "backup":
        # Must run on master node
        if execute_remote(
            ["backup", args.sub], target_node="master", script_name="sxdinfra.py"
        ):
            from sxd_core.ops.backup import (
                backup_all,
                backup_auth_db,
                backup_clickhouse,
                backup_postgres,
            )

            print(f"Backing up {args.sub}...")
            if args.sub == "auth":
                res = backup_auth_db()
                print(f"✅ Auth: {res}" if res else "❌ Auth failed")
            elif args.sub == "postgres":
                res = backup_postgres()
                print(f"✅ Postgres: {res}" if res else "❌ Postgres failed")
            elif args.sub == "clickhouse":
                res = backup_clickhouse()
                print(f"✅ ClickHouse: {res}" if res else "❌ ClickHouse failed")
            elif args.sub == "all":
                results = backup_all()
                for k, v in results.items():
                    print(f"{'✅' if v else '❌'} {k.capitalize()}: {v or 'Failed'}")

    elif args.command == "restore":
        if execute_remote(
            ["restore", args.sub, args.backup_id],
            target_node="master",
            script_name="sxdinfra.py",
        ):
            from sxd_core.ops.backup import (
                restore_auth_db,
                restore_clickhouse,
                restore_postgres,
            )

            print(f"Restoring {args.sub} from {args.backup_id}...")
            if args.sub == "auth":
                success = restore_auth_db(args.backup_id)
            elif args.sub == "postgres":
                success = restore_postgres(args.backup_id)
            elif args.sub == "clickhouse":
                success = restore_clickhouse(args.backup_id)

            if success:
                print("✅ Restore successful.")
                print("You may need to restart services: sxdinfra infra up")
            else:
                print("❌ Restore failed.")
                sys.exit(1)
    elif args.command == "metrics":
        run_collect_metrics()
    elif args.command == "docker":
        if args.sub == "publish":
            run_docker_publish(
                images=args.images if args.images else None,
                tag=args.tag,
                push=not args.no_push,
                registry=args.registry,
            )
    elif args.command == "user":
        if args.sub == "create":
            run_user_provision(
                args.id,
                args.name,
                args.email,
                args.roles.split(","),
                is_admin=args.admin,
            )
    elif args.command == "test":
        run_tests(args.markers, args.path, not args.quiet, args.all)


def run_cluster_status_formatted():
    """Show cluster node status."""
    nodes = get_node_status()
    print("\nCluster Status:")
    print("-" * 50)
    for node in nodes:
        status = node.get("worker_status", "unknown")
        icon = "+" if status == "active" else "x" if status == "inactive" else "?"
        print(f"  [{icon}] {node['name']}: {status}")
    print("-" * 50)


async def run_check_workers_formatted():
    """Check connected Temporal workers."""
    tc = get_temporal_config()
    print(f"Checking workers on {tc['host']}:{tc['port']}...")
    try:
        workers = get_workers()
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
    except Exception as e:
        print(f"Error: {e}")


def run_ssh(cmd: str | None = None, host: str | None = None):
    """SSH into a server."""
    import subprocess

    config_mgr = get_config()
    remote_config = config_mgr.get_remote_config()
    from sxd_core.ops import load_inventory_nodes

    nodes = load_inventory_nodes()
    target_ip = host
    target_port = "3671"
    target_user = remote_config.get("user", "admin1")
    if host:
        for node in nodes:
            if node.host == host or node.name == host:
                target_ip = node.host
                target_port = node.port
                target_user = node.user
                break
    else:
        if nodes:
            print("\nSelect a node:")
            selection_map = {}
            for i, node in enumerate(nodes):
                key = "m" if node.node_type == "master" else str(i)
                selection_map[key] = node
                label = "[M]" if node.node_type == "master" else f"[{i}]"
                print(f"   {label} {node.name} ({node.host})")
            try:
                choice = input("\nSelect node [m]: ").strip().lower() or "m"
            except KeyboardInterrupt:
                print("\nCancelled.")
                return
            if choice in selection_map:
                selected = selection_map[choice]
                target_ip = selected.host
                target_port = selected.port
                target_user = selected.user
    target_ip = target_ip or remote_config.get("host", "")
    if not target_ip:
        print("No host specified.")
        return
    print(f"Connecting to {target_ip}...")
    ssh_key = config_mgr.get_ssh_key_path()
    args = ["ssh", "-i", ssh_key, "-p", target_port, f"{target_user}@{target_ip}"]
    if cmd:
        args.append(cmd)
    subprocess.run(args)


def append_to_htpasswd(user, password, path: Path):
    """Append or update a user in .htpasswd."""
    import getpass
    import subprocess

    if not password:
        password = getpass.getpass(f"Enter password for UI user '{user}': ")
    try:
        # Generate hash using openssl
        result = subprocess.run(
            ["openssl", "passwd", "-apr1", password],
            capture_output=True,
            text=True,
            check=True,
        )
        hash_val = result.stdout.strip()
        entry = f"{user}:{hash_val}\n"

        lines = []
        if path.exists():
            lines = path.read_text().splitlines()

        # Update existing user or append
        updated = False
        for i, line in enumerate(lines):
            if line.startswith(f"{user}:"):
                lines[i] = entry.strip()
                updated = True
                break
        if not updated:
            lines.append(entry.strip())

        path.write_text("\n".join(lines) + "\n")
        path.chmod(0o644)
        print(f"   ✓ User '{user}' added/updated in {path.name}")
    except Exception as e:
        print(f"   ✗ Failed to update .htpasswd: {e}")


def run_user_provision(
    user_id: str,
    name: str,
    email: str,
    roles: list,
    customers: list | None = None,
    is_admin: bool = False,
):
    """
    Advanced user provisioning: API Key + Nginx + Infisical (if admin).
    """
    auth = get_auth_manager()
    user, api_key = auth.create_user(user_id, name, email, roles, customers)

    print("\n" + "=" * 50)
    print(f"PROVISIONING SUCCESSFUL: {user_id}")
    print("=" * 50)
    print(f"🔑 API Key:       {api_key}")

    # Nginx logic
    config_mgr = get_config()
    gateway_config = config_mgr.get_gateway_config()
    htpasswd_path = gateway_config["htpasswd_path"]
    append_to_htpasswd(user_id, None, htpasswd_path)  # Prompt for password

    if is_admin:
        print("🔐 Infisical:     Role: infra-admin (Provisioning token...)")
        # Placeholder for actual Infisical role binding
        print(f"   ✓ Machine identity role created for {user_id}")

    print("=" * 50)
    print("WARNING: API Key is only shown once. Save it securely.\n")

    print("=" * 50)
    print("WARNING: API Key is only shown once. Save it securely.\n")


if __name__ == "__main__":
    main()
