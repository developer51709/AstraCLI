# AstraCLI Updater

AstraCLI can update itself using Git.

## How it works

The updater runs a `git pull --ff-only` from the repository root.

## Usage

```bash
astra update
```

If the repository is not installed from git, the updater will report that update is unavailable.
