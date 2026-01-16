"""
CLI module for qlookz.

Provides entry points for:
    - qq: Run command and cache output
    - ql: Look up cached output
    - qlookz: Main CLI with subcommands
"""

import subprocess
import sys
import time
from typing import NoReturn

from .cache import Cache, CacheEntry, get_cache


# ANSI color codes for terminal output
class Colors:
    HEADER = "\033[95m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RESET = "\033[0m"


def _supports_color() -> bool:
    """Check if terminal supports color output."""
    if not sys.stdout.isatty():
        return False
    import os
    return os.environ.get("TERM") != "dumb"


def _colorize(text: str, color: str) -> str:
    """Apply color to text if terminal supports it."""
    if _supports_color():
        return f"{color}{text}{Colors.RESET}"
    return text


def _print_header(message: str, cached_at: str = "", duration: float = 0) -> None:
    """Print a styled header for cached output."""
    border = "─" * 60
    
    print(_colorize(border, Colors.DIM))
    print(_colorize(f"📦 {message}", Colors.CYAN + Colors.BOLD))
    if cached_at:
        print(_colorize(f"   Cached: {cached_at}", Colors.DIM))
    if duration > 0:
        print(_colorize(f"   Original duration: {duration:.2f}s", Colors.DIM))
    print(_colorize(border, Colors.DIM))


def _print_not_found(command: str) -> None:
    """Print message when command is not in cache."""
    print(_colorize(f"❌ No cached output found for: {command}", Colors.YELLOW), file=sys.stderr)
    print(_colorize("   Run with 'qq' first to cache the output.", Colors.DIM), file=sys.stderr)


def _get_command_from_args(args: list[str]) -> str:
    """Join command arguments into a single string."""
    return " ".join(args)


def run_and_cache() -> NoReturn:
    """
    Entry point for 'qq' command.
    
    Runs the given command and caches its output.
    """
    if len(sys.argv) < 2:
        print(_colorize("Usage: qq <command> [args...]", Colors.YELLOW), file=sys.stderr)
        print(_colorize("Example: qq ls -la", Colors.DIM), file=sys.stderr)
        sys.exit(1)
    
    command_args = sys.argv[1:]
    command_str = _get_command_from_args(command_args)
    
    # Run the command
    start_time = time.time()
    try:
        result = subprocess.run(
            command_str,
            shell=True,
            capture_output=True,
            text=True,
        )
        duration = time.time() - start_time
        
        # Store in cache
        entry = CacheEntry(
            command=command_str,
            stdout=result.stdout,
            stderr=result.stderr,
            exit_code=result.returncode,
            timestamp=time.time(),
            duration=duration,
        )
        
        cache = get_cache()
        cache_path = cache.store(entry)
        
        # Print output
        if result.stdout:
            print(result.stdout, end="")
        if result.stderr:
            print(result.stderr, end="", file=sys.stderr)
        
        # Print cache confirmation
        print(_colorize(f"✓ Cached ({duration:.2f}s)", Colors.GREEN + Colors.DIM), file=sys.stderr)
        
        sys.exit(result.returncode)
        
    except Exception as e:
        print(_colorize(f"Error running command: {e}", Colors.RED), file=sys.stderr)
        sys.exit(1)


def lookup_cache() -> NoReturn:
    """
    Entry point for 'ql' command.
    
    Looks up and displays cached output for the given command.
    """
    if len(sys.argv) < 2:
        print(_colorize("Usage: ql <command> [args...]", Colors.YELLOW), file=sys.stderr)
        print(_colorize("Example: ql ls -la", Colors.DIM), file=sys.stderr)
        sys.exit(1)
    
    command_args = sys.argv[1:]
    command_str = _get_command_from_args(command_args)
    
    cache = get_cache()
    entry = cache.lookup(command_str)
    
    if entry is None:
        _print_not_found(command_str)
        sys.exit(1)
    
    # Print header
    _print_header(
        "CACHED OUTPUT",
        cached_at=entry.created_at,
        duration=entry.duration,
    )
    
    # Print cached output
    if entry.stdout:
        print(entry.stdout, end="")
    if entry.stderr:
        print(entry.stderr, end="", file=sys.stderr)
    
    sys.exit(entry.exit_code)


def cmd_list(cache: Cache) -> int:
    """List all cached commands."""
    entries = cache.list_entries()
    
    if not entries:
        print(_colorize("No cached commands found.", Colors.DIM))
        return 0
    
    print(_colorize(f"📦 Cached commands ({len(entries)}):", Colors.CYAN + Colors.BOLD))
    print()
    
    for entry in entries:
        age_str = _format_age(entry.age_seconds)
        status = _colorize("✓", Colors.GREEN) if entry.exit_code == 0 else _colorize("✗", Colors.RED)
        print(f"  {status} {_colorize(entry.command, Colors.BOLD)}")
        print(f"      {_colorize(f'Cached {age_str} ago | Duration: {entry.duration:.2f}s', Colors.DIM)}")
        print()
    
    return 0


def _format_age(seconds: float) -> str:
    """Format age in human-readable format."""
    if seconds < 60:
        return f"{int(seconds)}s"
    elif seconds < 3600:
        return f"{int(seconds / 60)}m"
    elif seconds < 86400:
        return f"{int(seconds / 3600)}h"
    else:
        return f"{int(seconds / 86400)}d"


def cmd_clear(cache: Cache) -> int:
    """Clear all cached commands."""
    count = cache.clear()
    print(_colorize(f"✓ Cleared {count} cached entries.", Colors.GREEN))
    return 0


def cmd_delete(cache: Cache, command: str) -> int:
    """Delete a specific cached command."""
    if cache.delete(command):
        print(_colorize(f"✓ Deleted cache for: {command}", Colors.GREEN))
        return 0
    else:
        print(_colorize(f"❌ No cache found for: {command}", Colors.YELLOW), file=sys.stderr)
        return 1


def cmd_prune(cache: Cache, max_age: str) -> int:
    """Prune old cached entries."""
    # Parse age string (e.g., "1h", "7d", "30m")
    try:
        unit = max_age[-1].lower()
        value = int(max_age[:-1])
        
        multipliers = {"s": 1, "m": 60, "h": 3600, "d": 86400}
        if unit not in multipliers:
            raise ValueError(f"Unknown time unit: {unit}")
        
        seconds = value * multipliers[unit]
    except (ValueError, IndexError) as e:
        print(_colorize(f"Invalid age format: {max_age}", Colors.RED), file=sys.stderr)
        print(_colorize("Use format like: 1h, 7d, 30m, 3600s", Colors.DIM), file=sys.stderr)
        return 1
    
    count = cache.prune(seconds)
    print(_colorize(f"✓ Pruned {count} entries older than {max_age}.", Colors.GREEN))
    return 0


def print_usage() -> None:
    """Print main CLI usage."""
    print(_colorize("qlookz", Colors.CYAN + Colors.BOLD) + _colorize(" - Quick Look Zsh", Colors.DIM))
    print()
    print(_colorize("Quick commands:", Colors.BOLD))
    print(f"  {_colorize('qq <command>', Colors.GREEN)}  Run command and cache output")
    print(f"  {_colorize('ql <command>', Colors.GREEN)}  Look up cached output")
    print()
    print(_colorize("Management:", Colors.BOLD))
    print(f"  {_colorize('qlookz list', Colors.GREEN)}           List all cached commands")
    print(f"  {_colorize('qlookz clear', Colors.GREEN)}          Clear all cached commands")
    print(f"  {_colorize('qlookz delete <cmd>', Colors.GREEN)}   Delete specific cache entry")
    print(f"  {_colorize('qlookz prune <age>', Colors.GREEN)}    Remove entries older than age (e.g., 1h, 7d)")
    print()
    print(_colorize("Examples:", Colors.BOLD))
    print(f"  {_colorize('qq curl https://api.example.com/data', Colors.DIM)}")
    print(f"  {_colorize('ql curl https://api.example.com/data', Colors.DIM)}")
    print(f"  {_colorize('qlookz prune 7d', Colors.DIM)}")


def main() -> NoReturn:
    """
    Main entry point for 'qlookz' command.
    
    Provides subcommands for cache management.
    """
    cache = get_cache()
    
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(0)
    
    subcommand = sys.argv[1].lower()
    
    if subcommand in ("help", "-h", "--help"):
        print_usage()
        sys.exit(0)
    
    elif subcommand == "list":
        sys.exit(cmd_list(cache))
    
    elif subcommand == "clear":
        sys.exit(cmd_clear(cache))
    
    elif subcommand == "delete":
        if len(sys.argv) < 3:
            print(_colorize("Usage: qlookz delete <command>", Colors.YELLOW), file=sys.stderr)
            sys.exit(1)
        command = " ".join(sys.argv[2:])
        sys.exit(cmd_delete(cache, command))
    
    elif subcommand == "prune":
        if len(sys.argv) < 3:
            print(_colorize("Usage: qlookz prune <age>", Colors.YELLOW), file=sys.stderr)
            print(_colorize("Example: qlookz prune 7d", Colors.DIM), file=sys.stderr)
            sys.exit(1)
        sys.exit(cmd_prune(cache, sys.argv[2]))
    
    elif subcommand == "version":
        from . import __version__
        print(f"qlookz {__version__}")
        sys.exit(0)
    
    else:
        print(_colorize(f"Unknown command: {subcommand}", Colors.RED), file=sys.stderr)
        print()
        print_usage()
        sys.exit(1)


if __name__ == "__main__":
    main()
