"""Terminal UI utilities for plajira.

Provides:
- ANSI color codes
- Formatted output helpers
- Interactive prompts
"""

from __future__ import annotations

import os
import sys


# Check if we should use colors
def _supports_color() -> bool:
    """Check if the terminal supports ANSI colors."""
    # Respect NO_COLOR environment variable
    if os.environ.get("NO_COLOR"):
        return False

    # Check if stdout is a TTY
    if not hasattr(sys.stdout, "isatty") or not sys.stdout.isatty():
        return False

    # Check TERM
    term = os.environ.get("TERM", "")
    if term == "dumb":
        return False

    return True


USE_COLOR = _supports_color()


# ANSI color codes
class Colors:
    """ANSI escape codes for terminal colors."""

    RESET = "\033[0m" if USE_COLOR else ""
    BOLD = "\033[1m" if USE_COLOR else ""
    DIM = "\033[2m" if USE_COLOR else ""
    UNDERLINE = "\033[4m" if USE_COLOR else ""

    # Foreground colors
    RED = "\033[31m" if USE_COLOR else ""
    GREEN = "\033[32m" if USE_COLOR else ""
    YELLOW = "\033[33m" if USE_COLOR else ""
    BLUE = "\033[34m" if USE_COLOR else ""
    MAGENTA = "\033[35m" if USE_COLOR else ""
    CYAN = "\033[36m" if USE_COLOR else ""
    WHITE = "\033[37m" if USE_COLOR else ""

    # Bright foreground colors
    BRIGHT_RED = "\033[91m" if USE_COLOR else ""
    BRIGHT_GREEN = "\033[92m" if USE_COLOR else ""
    BRIGHT_YELLOW = "\033[93m" if USE_COLOR else ""
    BRIGHT_BLUE = "\033[94m" if USE_COLOR else ""
    BRIGHT_MAGENTA = "\033[95m" if USE_COLOR else ""
    BRIGHT_CYAN = "\033[96m" if USE_COLOR else ""


# Convenience aliases
c = Colors


def success(text: str) -> str:
    """Format text as success (green)."""
    return f"{c.GREEN}{text}{c.RESET}"


def error(text: str) -> str:
    """Format text as error (red)."""
    return f"{c.RED}{text}{c.RESET}"


def warning(text: str) -> str:
    """Format text as warning (yellow)."""
    return f"{c.YELLOW}{text}{c.RESET}"


def info(text: str) -> str:
    """Format text as info (cyan)."""
    return f"{c.CYAN}{text}{c.RESET}"


def dim(text: str) -> str:
    """Format text as dim."""
    return f"{c.DIM}{text}{c.RESET}"


def bold(text: str) -> str:
    """Format text as bold."""
    return f"{c.BOLD}{text}{c.RESET}"


def header(text: str) -> str:
    """Format text as a header (bold + underline)."""
    return f"{c.BOLD}{c.UNDERLINE}{text}{c.RESET}"


def check_mark() -> str:
    """Return a green checkmark."""
    return f"{c.GREEN}\u2713{c.RESET}"


def cross_mark() -> str:
    """Return a red X."""
    return f"{c.RED}\u2717{c.RESET}"


def warning_mark() -> str:
    """Return a yellow warning symbol."""
    return f"{c.YELLOW}\u26a0{c.RESET}"


def bullet() -> str:
    """Return a bullet point."""
    return "\u2022"


def print_success(message: str) -> None:
    """Print a success message."""
    print(f"{check_mark()} {message}")


def print_error(message: str) -> None:
    """Print an error message."""
    print(f"{cross_mark()} {error(message)}")


def print_warning(message: str) -> None:
    """Print a warning message."""
    print(f"{warning_mark()} {warning(message)}")


def print_info(message: str) -> None:
    """Print an info message."""
    print(f"{info(message)}")


def print_header(title: str, char: str = "=") -> None:
    """Print a section header."""
    print(f"\n{bold(title)}")
    print(char * len(title))


def print_subheader(title: str) -> None:
    """Print a subsection header."""
    print(f"\n{c.BOLD}{title}{c.RESET}")


def prompt(message: str, default: str = "") -> str:
    """Prompt for user input.

    Args:
        message: Prompt message
        default: Default value (shown in brackets)

    Returns:
        User input or default if empty
    """
    if default:
        full_prompt = f"{message} [{default}]: "
    else:
        full_prompt = f"{message}: "

    try:
        response = input(full_prompt).strip()
        return response if response else default
    except EOFError:
        return default


def prompt_choices(
    message: str,
    choices: list[tuple[str, str]],
    default: str = "",
) -> str:
    """Prompt user to select from choices.

    Args:
        message: Prompt message
        choices: List of (key, description) tuples
        default: Default choice key

    Returns:
        Selected choice key
    """
    print(f"\n{message}")
    for key, desc in choices:
        marker = "*" if key == default else " "
        print(f"  {c.BOLD}[{key}]{c.RESET} {desc}")

    keys = [key for key, _ in choices]
    default_hint = f" [{default}]" if default else ""

    while True:
        try:
            response = input(f"\nChoice{default_hint}: ").strip().lower()
        except EOFError:
            response = ""

        if not response and default:
            return default
        if response in keys:
            return response

        print(f"{error('Invalid choice.')} Please enter one of: {', '.join(keys)}")


def prompt_yes_no(message: str, default: bool | None = None) -> bool:
    """Prompt for yes/no response.

    Args:
        message: Prompt message
        default: Default value (None means no default)

    Returns:
        True for yes, False for no
    """
    if default is True:
        hint = "[Y/n]"
    elif default is False:
        hint = "[y/N]"
    else:
        hint = "[y/n]"

    while True:
        try:
            response = input(f"{message} {hint}: ").strip().lower()
        except EOFError:
            response = ""

        if not response and default is not None:
            return default
        if response in ("y", "yes"):
            return True
        if response in ("n", "no"):
            return False

        print(f"{error('Invalid response.')} Please enter y or n.")


def prompt_confirm(message: str, confirm_text: str = "yes") -> bool:
    """Prompt for explicit confirmation by typing a specific word.

    Args:
        message: Prompt message
        confirm_text: Text user must type to confirm

    Returns:
        True if confirmed, False otherwise
    """
    print(f"\n{warning(message)}")
    try:
        response = input(f"Type '{confirm_text}' to confirm: ").strip().lower()
    except EOFError:
        response = ""

    return response == confirm_text.lower()


def prompt_select_numbers(
    message: str,
    max_num: int,
    default: str = "all",
) -> list[int] | None:
    """Prompt user to select numbers from a list.

    Args:
        message: Prompt message
        max_num: Maximum valid number
        default: Default selection ("all", "none", or comma-separated numbers)

    Returns:
        List of selected 1-indexed numbers, or None for 'none'
    """
    hint = f"[1-{max_num}, 'all', 'none']"
    default_hint = f" (default: {default})"

    while True:
        try:
            response = input(f"{message} {hint}{default_hint}: ").strip().lower()
        except EOFError:
            response = ""

        if not response:
            response = default

        if response == "all":
            return list(range(1, max_num + 1))
        if response == "none":
            return None

        try:
            numbers = []
            for part in response.split(","):
                num = int(part.strip())
                if 1 <= num <= max_num:
                    numbers.append(num)
                else:
                    raise ValueError(f"Number out of range: {num}")
            if numbers:
                return sorted(set(numbers))
        except ValueError:
            pass

        print(f"{error('Invalid selection.')} Enter numbers separated by commas, 'all', or 'none'.")


def format_issue_key(key: str) -> str:
    """Format a Jira issue key."""
    return f"{c.CYAN}{key}{c.RESET}"


def format_status(status: str) -> str:
    """Format a status with appropriate color."""
    status_lower = status.lower()
    if status_lower in ("done", "closed", "resolved"):
        return f"{c.GREEN}{status}{c.RESET}"
    elif status_lower in ("in progress", "in review"):
        return f"{c.BLUE}{status}{c.RESET}"
    elif status_lower in ("blocked", "won't do", "wont do"):
        return f"{c.RED}{status}{c.RESET}"
    elif status_lower in ("backlog", "to do", "open"):
        return f"{c.YELLOW}{status}{c.RESET}"
    else:
        return status


def format_marker(marker: str) -> str:
    """Format a .plan marker character."""
    colors = {
        "*": c.GREEN,
        "?": c.BLUE,
        "!": c.YELLOW,
        "+": c.GREEN,
        "~": c.RED,
    }
    color = colors.get(marker, "")
    return f"{color}{marker}{c.RESET}"


def truncate(text: str, max_len: int = 50) -> str:
    """Truncate text with ellipsis if too long."""
    if len(text) <= max_len:
        return text
    return text[:max_len - 3] + "..."
