# qlookz (quick look zsh)

Quick command output retrieval.

I wanted a tool to remember slow command outputs, and retrieve them without running everything again.
This also persists across shells.

Pretty good for kubernetes outputs.

## Installation

```bash
pip install qlookz
```

## Quick Start

### Cache a command's output

Prefix any command with `qq` to run it and cache the output:

```bash
qq curl https://api.example.com/data
qq ls -la /some/directory
qq kubectl get pods -A
```

### Retrieve cached output

Use `ql` with the same command to instantly retrieve the cached output:

```bash
ql curl https://api.example.com/data
ql ls -la /some/directory
ql kubectl get pods -A
```

The cached output will be displayed with a header showing when it was cached and how long the original command took.

## Commands

| Command | Description |
|---------|-------------|
| `qq <command>` | Run command and cache its output |
| `ql <command>` | Retrieve cached output for the command |
| `qlookz list` | List all cached commands |
| `qlookz clear` | Clear all cached commands |
| `qlookz delete <command>` | Delete a specific cache entry |
| `qlookz prune <age>` | Remove entries older than age (e.g., `1h`, `7d`, `30m`) |
| `qlookz version` | Show version |
| `qlookz help` | Show help |

## Examples

```bash
# Cache a slow API response
qq curl -s https://api.github.com/repos/python/cpython/commits

# Later, in any terminal, retrieve it instantly
ql curl -s https://api.github.com/repos/python/cpython/commits

# List what's cached
qlookz list

# Clean up old entries
qlookz prune 7d

# Clear everything
qlookz clear
```

## How It Works

- Command outputs are stored in `~/.qlookz/cache/`
- Each command is hashed to create a unique cache key
- Both stdout and stderr are captured and cached
- Exit codes are preserved when retrieving from cache
- Cache files are plain JSON for easy inspection

## Cache Location

By default, cache files are stored in:

```
~/.qlookz/cache/
```

Each cached command is stored as a JSON file containing:
- The original command
- stdout and stderr output
- Exit code
- Timestamp
- Duration

## Development

```bash
# Clone the repository
git clone https://github.com/qlookz/qlookz.git
cd qlookz

# Install in development mode
pip install -e .

# Run tests
python -m pytest
```

## License

MIT License - see [LICENSE](LICENSE) for details.
