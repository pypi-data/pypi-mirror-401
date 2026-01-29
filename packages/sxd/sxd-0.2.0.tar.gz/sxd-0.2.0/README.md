# sxd: sentientx data infra

A **unified data platform** for multi-modal robotics data, orchestrated by **Temporal** and powered by a modular monorepo.

**Status**: v1.6 (Pure Infisical)

> **User CLI**: `sxd` for automation, scripting, and interactive exploration.
> **Admin CLI**: `sxdinfra` for infrastructure provisioning, deployment, and cluster management.

---

## Quick Start (Developers)

```bash
# 1. Clone and install
git clone <repo-url> && cd sxd
uv sync

# 2. Login to Infisical (Required for secrets/SSH)
infisical login

# 3. Authenticate with SXD
sxd auth login
sxd auth
```

### For Cluster Admins (First-Time Setup)

```bash
# 1. Initialize Infisical Workspace
# Ensure you have access to the 'dev' environment in Infisical

# 2. Provision nodes
# This auto-extracts SSH keys and injects dynamic machine tokens
sxdinfra provision

# 3. Start Infrastructure (on master)
sxdinfra infra up
sxdinfra infra init

# 4. Deploy code (to all nodes)
sxdinfra deploy
```

### For Pipeline Developers

```bash
# Create a new pipeline
sxd scaffold pipeline my-pipeline

# Install and test
uv sync
sxd test packages/pipelines/my-pipeline/

# Submit a job
sxd submit my-pipeline '{"input": "value"}'
```

---

## Prerequisites

| Dependency | Purpose | Install |
|:-----------|:--------|:--------|
| **uv** | Python package manager | `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| **FFmpeg** | Video processing (optional) | `brew install ffmpeg` / `apt install ffmpeg` |

---

## Authentication & Authorization

SXD uses API key authentication with role-based access control.

### Roles

| Role | Access |
|:-----|:-------|
| `super_admin` | Full system access |
| `infra_admin` | Infrastructure, SSH, deployment |
| `pipeline_operator` | Submit jobs, view data (customer-scoped) |
| `developer` | Pipeline ops + debugging |
| `viewer` | Read-only access |

### Auth Commands

```bash
# Personal
sxd auth                  # Show current user and permissions
sxd auth login            # Save API key to ~/.sxd/credentials
sxd auth logout           # Remove saved credentials

# User management (admin only)
sxd auth users            # List all users
sxd auth create-user --id <id> --name "Name" --email "email" --roles role1,role2
sxd auth update-user <id> --roles new_role
sxd auth disable-user <id>
sxd auth rotate-key [id]  # Rotate API key

# Roles
sxd auth roles            # List available roles
sxd auth role <name>      # Show role details
```

---

## CLI Reference

### `sxd` - User & Pipeline CLI

| Category | Command | Description |
|:---------|:--------|:------------|
| **Auth** | `sxd auth` | Show current user |
| | `sxd auth login` | Save API key |
| **Workflows** | `sxd submit <name>` | Submit a workflow |
| | `sxd workflows` | List all pipelines |
| | `sxd status <id>` | Check workflow status |
| **Data** | `sxd upload <path>` | Upload datasets |
| | `sxd ls [path]` | List files in storage |
| | `sxd query <sql>` | Run ClickHouse queries |
| **Dev** | `sxd scaffold pipeline <name>` | Generate pipeline boilerplate |
| | `sxd test` | Run tests |
| | `sxd tidy` | Run linters |
| **TUI** | `sxd explore` | Interactive file explorer |

### `sxdinfra` - Infrastructure & Admin CLI

| Category | Command | Description |
|:---------|:--------|:------------|
| **Auth** | `sxdinfra auth create-user` | Create new user (admin) |
| **Cluster** | `sxdinfra info` | Show services and endpoints |
| | `sxdinfra nodes` | Show cluster node status |
| | `sxdinfra workers` | List active Temporal workers |
| **Ops** | `sxdinfra deploy` | Deploy code to cluster |
| | `sxdinfra ssh` | SSH into nodes |
| | `sxdinfra infra up` | Start infrastructure |
| | `sxdinfra provision` | Provision nodes (Ansible) |


---

## Architecture

### Unified Worker System

The cluster runs a **single generic worker image** that:
1. **Auto-Discovers** pipelines from `packages/pipelines/*`
2. **Registers** all Workflows and Activities dynamically
3. **Polls** all relevant Task Queues

To add a new pipeline, run `sxd scaffold pipeline <name>` and deploy.

- **Authentication**: API keys (SHA-256 hashed in `config/users.yaml`)
- **Authorization**: Role-based with customer scoping
- **Audit**: All actions logged to ClickHouse with user identity
- **Secrets**: **Pure Infisical** - Zero sensitive files in repo. Secrets injected into process memory via Infisical CLI.

---

## Project Structure

```
sxd/
├── sxd.py                  # CLI entrypoint
├── config/
│   ├── settings.yaml       # Platform configuration
│   ├── roles.yaml          # Role definitions
│   └── users.yaml          # User accounts (hashed keys)
├── packages/
│   ├── sxd-core/           # Core library
│   ├── sxd-master/         # Master service logic
│   └── sxd-sdk/            # Pipeline SDK
├── deploy/
│   ├── ansible/            # Provisioning & Deployment (Infisical-integrated)
│   └── docker-compose.yml  # Infrastructure services
├── scripts/
│   └── setup-admin.py      # Initial admin setup
└── docs-site/              # VitePress documentation
```

---

## Documentation

### Interactive Docs

Served at `http://your-server/docs/` after deployment.

**Local Development:**
```bash
cd docs-site && npm install && npm run docs:dev
```

### Key Docs

- **[Getting Started](docs-site/guide/getting-started.md)** - Role-based setup guide
- **[Creating Pipelines](docs-site/pipelines/custom.md)** - Build custom pipelines
- **[Architecture](docs-site/guide/architecture.md)** - System design
- **[SECURITY.md](docs-site/technical-specs/SECURITY.md)** - Security policies

---

Built for SentientX.
