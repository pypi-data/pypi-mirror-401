"""Utility functions for the EnvLock CLI."""

import os
import sys
import getpass
from pathlib import Path


class Colors:
    """ANSI color codes for terminal output."""
    reset = "\033[0m"
    bright = "\033[1m"
    dim = "\033[2m"
    underscore = "\033[4m"
    blink = "\033[5m"
    reverse = "\033[7m"
    hidden = "\033[8m"

    class fg:
        """Foreground colors."""
        black = "\033[30m"
        red = "\033[31m"
        green = "\033[32m"
        yellow = "\033[33m"
        blue = "\033[34m"
        magenta = "\033[35m"
        cyan = "\033[36m"
        white = "\033[37m"
        crimson = "\033[38m"

    class bg:
        """Background colors."""
        black = "\033[40m"
        red = "\033[41m"
        green = "\033[42m"
        yellow = "\033[43m"
        blue = "\033[44m"
        magenta = "\033[45m"
        cyan = "\033[46m"
        white = "\033[47m"
        crimson = "\033[48m"


colors = Colors()


def log_intro(title: str) -> None:
    """
    Display a formatted introduction banner.
    
    Args:
        title: The title text to display
    """
    width = 50
    line = "═" * width
    padding = " " * max(0, (width - len(title)) // 2)
    print(f"\n{colors.fg.magenta}{line}")
    print(f"{padding}{colors.bright}{title}{colors.reset}{colors.fg.magenta}{padding}")
    print(f"{line}{colors.reset}\n")


def log_step(step: int, description: str) -> None:
    """
    Display a formatted step message.
    
    Args:
        step: The step number
        description: Description of the step
    """
    print(f"{colors.fg.blue}{colors.bright}[Step {step}]{colors.reset} {description}")


def log_success(message: str) -> None:
    """
    Display a success message.
    
    Args:
        message: The success message
    """
    print(f"\n{colors.fg.green}✔ SUCCESS:{colors.reset} {message}")


def log_error(message: str) -> None:
    """
    Display an error message.
    
    Args:
        message: The error message
    """
    print(f"\n{colors.fg.red}✖ ERROR:{colors.reset} {message}", file=sys.stderr)


def log_info(message: str) -> None:
    """
    Display an info message.
    
    Args:
        message: The info message
    """
    print(f"{colors.fg.cyan}ℹ INFO:{colors.reset} {message}")


def log_box(lines: list) -> None:
    """
    Display text in a bordered box.
    
    Args:
        lines: List of strings to display in the box
    """
    width = max(len(line) for line in lines) + 4
    top = "┌" + "─" * width + "┐"
    bottom = "└" + "─" * width + "┘"

    print(colors.dim + top + colors.reset)
    for line in lines:
        padding = " " * (width - len(line) - 3)
        print(f"{colors.dim}│{colors.reset} {line}{padding} {colors.dim}│{colors.reset}")
    print(colors.dim + bottom + colors.reset)


def prompt_hidden(question: str) -> str:
    """
    Prompt the user for input without displaying what they type (for passwords).
    
    Args:
        question: The prompt text to display
        
    Returns:
        The user's input
    """
    try:
        return getpass.getpass(f"{colors.fg.cyan}{question}{colors.reset}")
    except (KeyboardInterrupt, EOFError):
        print()
        sys.exit(0)


def prompt(question: str) -> str:
    """
    Prompt the user for input.
    
    Args:
        question: The prompt text to display
        
    Returns:
        The user's input (trimmed)
    """
    try:
        response = input(f"{colors.fg.cyan}{question}{colors.reset}")
        return response.strip()
    except (KeyboardInterrupt, EOFError):
        print()
        sys.exit(0)


def find_env_files() -> list:
    """
    Find all .env files in the current directory, excluding encrypted ones.
    
    Returns:
        List of .env filenames
    """
    cwd = Path.cwd()
    files = []
    
    for file in cwd.iterdir():
        if file.is_file() and file.name.startswith(".env") and not file.name.startswith(".env.enc"):
            files.append(file.name)
    
    return sorted(files)


def select_file(files: list, message: str = "Select a file: ") -> str:
    """
    Helper to handle file selection when multiple files are available.
    
    Args:
        files: List of available files
        message: Prompt message for selection
        
    Returns:
        The selected filename
    """
    if len(files) == 0:
        return None
    
    if len(files) == 1:
        return files[0]

    print(f"{colors.fg.yellow}Multiple files found:{colors.reset}")
    for i, f in enumerate(files, 1):
        print(f"{colors.fg.green}{i}.{colors.reset} {f}")

    choice = prompt(message)
    
    try:
        index = int(choice) - 1
        if 0 <= index < len(files):
            return files[index]
    except ValueError:
        pass
    
    print(f"{colors.fg.red}❌ Invalid selection{colors.reset}")
    sys.exit(1)
