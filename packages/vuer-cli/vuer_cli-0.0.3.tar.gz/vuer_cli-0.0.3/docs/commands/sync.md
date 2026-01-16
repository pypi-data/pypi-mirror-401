# vuer sync

Synchronize `environment.json` dependencies with the local cache (`vuer_environments/`).

## Usage

```bash
vuer sync

# Or specify output directory (optional)
vuer sync --output ./vuer_environments
```

## Behavior

1. Locate `environment.json` in the current working directory. If missing, the
   command fails with an error.

2. Parse `dependencies` and expand transitive dependencies via the backend.

3. Deduplicate and write resolved dependencies to `environments-lock.yaml`.

4. Download missing environments into `vuer_environments/<name>/<version>`.
   Existing version directories listed in the lockfile are skipped.

5. Remove version directories that are no longer present in the new lockfile.

Dry-run mode (`VUER_CLI_DRY_RUN`) simulates validation and downloading without
performing network calls.


