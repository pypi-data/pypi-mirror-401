#!/usr/bin/env python3
"""EnvLock CLI - Main entry point for the command-line interface."""

import sys
from envlock.utils import colors, log_intro, log_box
from envlock import __version__


def main():
    """Main CLI entry point."""
    command = sys.argv[1] if len(sys.argv) > 1 else None

    if not command:
        log_intro("ENVLOCK CLI")
        print("Securely manage your environment variables with ease.\n")

        log_box([
            "Usage: envlock <command>",
            "",
            "Commands:",
            "  init     Initialize envlock in your project",
            "  encrypt  Encrypt a .env file",
            "  decrypt  Decrypt a .env.enc file",
            "  version  Show version information",
            "",
            f"Version: {__version__}",
        ])
        sys.exit(1)

    if command == "init":
        from envlock.init import init_envlock
        init_envlock()
    elif command == "encrypt":
        from envlock.encrypt import encrypt_env
        encrypt_env()
    elif command == "decrypt":
        from envlock.decrypt import decrypt_env
        decrypt_env()
    elif command in ["version", "--version", "-v"]:
        print(f"envlock version {colors.fg.green}{__version__}{colors.reset}")
    else:
        print(f"{colors.fg.red}Unknown command: {command}{colors.reset}")
        print(f"Run {colors.fg.cyan}envlock{colors.reset} for help.")
        sys.exit(1)


if __name__ == "__main__":
    main()
