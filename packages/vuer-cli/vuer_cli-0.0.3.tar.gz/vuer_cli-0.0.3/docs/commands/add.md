# vuer add

Add an environment dependency to `environment.json` and run `sync`.

## Usage

```bash
vuer add some-environment/1.2.3
```

## Behavior

- Validates argument format `name/version`.
- If `environments-lock.yaml` already contains the exact entry, the command
  returns success without modifying `environment.json`.
- Otherwise, it writes or updates `environment.json` and triggers `vuer sync`.


