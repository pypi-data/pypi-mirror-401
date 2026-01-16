# Core concepts

This page explains the main concepts used by Vuer CLI.

## Environment Configuration File: `environment.json`

Maintain an `environment.json` file in your project root directory to declare
the list of environments your project depends on, similar to `package.json` in
Node.js.

**Example:**

```json
{
  "dependencies": {
    "some-dependency": "^1.2.3",
    "another-dependency": "~4.5.6",
    "new-dependency": "0.1.0"
  }
}
```

**`dependencies` field:**

- **Key**: Environment name (e.g., `some-dependency`)
- **Value**: Version expression (e.g., `^1.2.3`, `~4.5.6`, etc.)

## Local cache: `vuer_environments/`

`vuer sync` downloads direct and transitive dependencies into the
`vuer_environments/` directory in the project root. Each environment uses a
nested directory layout `vuer_environments/<name>/<version>`.

Downloaded environment directories may contain their own `environment.json`;
the CLI preserves these per-version metadata files.

## Dependency index: `environments-lock.yaml`

`vuer sync` generates `environments-lock.yaml` (next to `vuer_environments/`)
as a system-maintained lockfile that records resolved and deduplicated
environment dependencies. Do not edit it manually.

Minimal example:

```yaml
environments:
  - "some-dependency/^1.2.3"
  - "another-dependency/~4.5.6"
```

## Environment variables

- `VUER_HUB_URL` — Base URL of Vuer Hub API (required in non-dry-run)
- `VUER_AUTH_TOKEN` — JWT token for API access (required in non-dry-run)
- `VUER_CLI_DRY_RUN` — Enable dry-run mode (any non-"0"/"false" value enables
  it)


