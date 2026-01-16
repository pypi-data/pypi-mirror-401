# vuer remove

Remove an environment dependency from `environment.json` and run `sync`.

## Usage

```bash
vuer remove some-environment/1.2.3
```

## Behavior

- Requires `name/version` argument.
- Only removes the dependency entry if the name and version exactly match the
  current `environment.json` entry for that name.
- Triggers `vuer sync` to reconcile local cache.

If removing the last version directory for an environment, `sync` will also
remove the empty parent `vuer_environments/<name>/` directory.


