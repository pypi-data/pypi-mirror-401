# Introduction

**vuer-cli** is a command-line tool for managing physical simulation
environments.
It works with Vuer Hub to version-control and distribute environments the same
way you manage software packages.

## Installation

```bash
pip install vuer-cli==0.0.2
```

## Quick start

Before running commands that contact the Vuer Hub (for example `sync`, `add`,
`remove`, `upgrade`, `envs-pull`, `envs-publish`), you should configure the
required environment variables or use dry-run mode for testing. Required env
vars for real (non-dry-run) operations:

- `VUER_HUB_URL` — Base URL of the Vuer Hub API
- `VUER_AUTH_TOKEN` — JWT token for API authentication

If you prefer to try commands locally without making network calls, enable
dry-run mode:

```bash
# Dry-run example (no network calls)
VUER_CLI_DRY_RUN=1 vuer sync
```

Or run a real command with env vars set inline:

```bash
# Real run example (requires valid token and hub URL)
VUER_HUB_URL=https://hub.example.com VUER_AUTH_TOKEN=... vuer sync
```

Then typical quick-start commands:

```bash
# Edit environment.json, fill in initial dependencies
vuer sync

# Add an environment and sync
vuer add my-environment/1.0.0

# Remove an environment and sync
vuer remove my-environment/1.0.0

# Upgrade an environment to the latest version
vuer upgrade my-environment
