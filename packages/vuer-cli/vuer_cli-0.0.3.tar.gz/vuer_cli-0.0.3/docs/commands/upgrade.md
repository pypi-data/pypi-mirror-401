# vuer upgrade

Upgrade a named environment to the latest version available in the backend.

## Usage

```bash
vuer upgrade some-environment-name
```

## Behavior

1. Read `environment.json` and locate the dependency by name.
2. Call backend `/environments/latest-by-name?name=<name>` to fetch latest
   `versionId`.
3. If the latest version differs, update `environment.json` and trigger `vuer sync`.


