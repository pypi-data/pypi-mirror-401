# Publishing & Pulling

This page documents the `envs-publish` and `envs-pull` commands. Each command
section below is self-contained with usage examples and behavior notes.

## envs-publish

Package and publish a local environment directory (which must contain
`environment.json`) to Vuer Hub.

### Usage

```bash
# Publish directly in current directory (containing environment.json)
vuer envs-publish

# Or specify a directory containing environment.json
vuer envs-publish --directory ./my-environment
```

### Behavior

1. Read metadata: the command looks for `environment.json` in the specified
   directory (defaults to current directory) and parses the following fields:
    - `name` (required)
    - `version` (required)
    - `description` (optional)
    - `visibility` (optional, default `PUBLIC`)
    - `env-type` / `env_type` (optional)

   The command fails if `name` or `version` is missing.

2. Validate dependencies (optional): if `environment.json` has a
   `dependencies` block, the CLI extracts those into a `name/version` list and
   calls the backend `/environments/dependencies` endpoint to validate them.
   If validation fails, publishing aborts with an error.

3. Package directory: all files in the directory (including `environment.json`)
   are packaged into a `.tgz` archive named:

   ```text
   {name}-{version}.tgz
   ```

   The archive is written to the system temporary directory and its path is
   printed in the log.

4. Dry-run vs real publish:
    - In dry-run mode (`VUER_CLI_DRY_RUN` enabled or `--dry-run`):
        - No network calls are made; the process simulates upload and prints
          progress and final success messages annotated with `(dry-run)`.
    - In real mode:
        - `VUER_HUB_URL` and `VUER_AUTH_TOKEN` must be configured; otherwise
          the
          command fails.
        - The archive is uploaded to the Hub and the response is reported.

### Examples

```bash
# Dry-run publish
VUER_CLI_DRY_RUN=1 vuer envs-publish --directory ./my-environment

# Real publish (requires env vars)
VUER_HUB_URL=https://hub.example.com VUER_AUTH_TOKEN=... vuer envs-publish
```

## envs-pull

Download an environment package from Vuer Hub by numeric ID or `name/version`.

### Usage

```bash
# Pull by environment ID
vuer envs-pull --flag 252454509945688064

# Pull by name/version
vuer envs-pull --flag my-environment/v3.0.10

# Specify output directory and custom archive name
vuer envs-pull --flag my-environment/v3.0.10 --output ./downloads
```

### Behavior

- `--flag` (required): environment identifier; either a Hub numeric ID or a
  `name/version` string.
- `--output`: target directory (default `./downloads`).
- `--timeout`: request timeout (seconds).
- `--skip-progress`: skip interactive progress output.

Dry-run behavior:

- In dry-run mode the CLI does not call the network. Instead it creates a
  subdirectory named after the provided flag inside the output directory and
  writes a simple `README.txt` to simulate a downloaded environment. This is
  useful for CI and local testing.

Real download behavior:

- The CLI downloads the archive (default filename `<env_flag>.tgz` or the file
  name from `Content-Disposition`) and writes it to the output directory.
- If the archive is a tar/tgz, the CLI extracts it into the nested layout
  `output/<name>/<version>/` for `name/version` flags and removes the original
  archive after extraction.

### Examples

```bash
# Dry-run pull
VUER_CLI_DRY_RUN=1 vuer envs-pull --flag my-env/v1.2.3 --output ./downloads

# Real pull
VUER_HUB_URL=https://hub.example.com VUER_AUTH_TOKEN=... \
  vuer envs-pull --flag my-env/v1.2.3 --output ./downloads
```

For more conceptual information about environment layout, lockfile and the
dependency model, see the `concepts` and `commands/sync` pages.


