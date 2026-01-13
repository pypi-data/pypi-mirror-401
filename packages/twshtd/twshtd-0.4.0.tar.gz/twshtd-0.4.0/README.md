# twshtd

Git repository synchronization tool for managing multiple repositories.

## Installation

```bash
# Install with uv
uv tool install twshtd

# Or install from source
uv tool install -e .
```

## Usage

```bash
twshtd [OPTIONS] COMMAND [ARGS]
```

### Commands

| Command   | Description                                              |
|-----------|----------------------------------------------------------|
| `push`    | Commit and push all configured repositories              |
| `pull`    | Commit local changes and pull from remotes               |
| `status`  | Show status of all configured repositories               |
| `list`    | List all configured repositories                         |
| `dirty`   | Show dirty/behind/ahead status for repos in directories  |

### Options

| Option           | Description                |
|------------------|----------------------------|
| `-v, --verbose`  | Enable debug logging       |
| `-V, --version`  | Show version               |

### Push Command

```bash
twshtd push [OPTIONS]
```

Commits all changes and pushes to remote for each configured repository.

| Option              | Description                    |
|---------------------|--------------------------------|
| `-c, --config`      | Config file path               |
| `--skip-anki-check` | Skip Anki process check        |
| `--skip-rplc`       | Skip rplc swap-out             |
| `-n, --dry-run`     | Show what would be done        |

### Pull Command

```bash
twshtd pull [OPTIONS]
```

Commits local changes and pulls from remotes. Supports two modes per repository:
- `pull`: Full git pull (default)
- `fetch`: Only fetch, showing what changed

| Option           | Description             |
|------------------|-------------------------|
| `-c, --config`   | Config file path        |
| `-n, --dry-run`  | Show what would be done |

### Dirty Command

```bash
twshtd dirty [OPTIONS]
```

Scans configured directories for git repositories and shows their status.

| Option           | Description                           |
|------------------|---------------------------------------|
| `-c, --config`   | Config file path                      |
| `--no-fetch`     | Skip git fetch before checking status |

## Configuration

Config file location (in order of precedence):
1. `TWSHTD_CONFIG` environment variable
2. `~/.config/twshtd/repos.toml`

### Example Configuration

```toml
[settings]
workers = 1  # parallel workers (1 = sequential)

[[repos]]
path = "~/dev/project1"
pull_mode = "pull"          # "pull" or "fetch"
pre_command = "make clean"  # optional command before push
post_command = "make build" # optional command after pull
enabled = true

[[repos]]
path = "$PROJECTS/project2"
pull_mode = "fetch"

[[repos]]
path = "~/dev/disabled-repo"
enabled = false

# Directories to scan with 'dirty' command
[[dirty]]
path = "~/dev"
enabled = true

[[dirty]]
path = "$WORK/repos"
```

### Path Resolution

Paths support:
- Home directory expansion (`~`)
- Environment variables (`$VAR` or `${VAR}`)

## Features

### Pre-Command / Post-Command

Each repository can define:
- `pre_command`: runs before git operations during `push`
- `post_command`: runs after successful git operations during `pull`

```toml
[[repos]]
path = "~/dev/myproject"
pre_command = "make clean"   # before push
post_command = "make build"  # after pull
```

Commands run in the repository directory. If a command fails, the repository is skipped.

### Commit Message

When committing changes, twshtd uses `git status --porcelain` output as the commit message,
providing a clear record of what changed.

### Anki Integration

The `push` command checks if Anki is running and refuses to proceed if it is.
This prevents conflicts when syncing Anki-related repositories. Use `--skip-anki-check` to bypass.

### rplc Integration

For repositories using [rplc](https://github.com/sysid/rplc), twshtd automatically swaps out
files before committing. Use `--skip-rplc` to bypass.

## Development

```bash
# Install dev dependencies
uv sync

# Run tests
make test

# Lint and format
make static-analysis
```

## License

MIT
