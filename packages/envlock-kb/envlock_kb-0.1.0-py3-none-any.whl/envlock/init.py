"""Initialize EnvLock in a project."""

import os
import json
import sys
from pathlib import Path
from envlock.crypto import encrypt_data
from envlock.utils import (
    prompt_hidden, find_env_files, select_file,
    log_intro, log_step, log_success, log_info, log_error
)


def ensure_gitignore() -> None:
    """
    Ensure .gitignore is configured to ignore .env files but not .env.enc files.
    """
    gitignore_path = Path.cwd() / ".gitignore"
    ignore_lines = [".env*", "!.env.enc*"]

    content = ""
    if gitignore_path.exists():
        content = gitignore_path.read_text(encoding='utf-8')

    updated = False
    for line in ignore_lines:
        if line not in content:
            if content and not content.endswith("\n"):
                content += "\n"
            content += f"{line}\n"
            updated = True

    if updated:
        gitignore_path.write_text(content, encoding='utf-8')
        log_success("Updated .gitignore to ignore .env files")
    else:
        log_info(".gitignore already configured")


def init_envlock() -> None:
    """Initialize EnvLock in the current project."""
    log_intro("INITIALIZE ENVLOCK")

    log_step(1, "Checking environment...")
    env_files = find_env_files()

    if len(env_files) == 0:
        log_error("No .env files found to initialize")
        sys.exit(1)

    log_step(2, "Configuring gitignore...")
    ensure_gitignore()

    log_step(3, "Selecting file to encrypt...")
    target_env = select_file(env_files, "Select a file to initialize: ")

    suffix = target_env.replace(".env", "")
    enc_file = f".env.enc{suffix}"
    enc_path = Path.cwd() / enc_file

    if enc_path.exists():
        log_info(f"{enc_file} already exists. Skipping encryption.")
        sys.exit(0)

    log_step(4, "Setting up encryption...")
    
    try:
        plain_env = (Path.cwd() / target_env).read_text(encoding='utf-8')
    except Exception as e:
        log_error(f"Failed to read {target_env}: {e}")
        sys.exit(1)

    password = prompt_hidden("Create encryption password: ")
    confirm = prompt_hidden("Confirm password: ")

    if not password or password != confirm:
        log_error("Passwords do not match or are empty")
        sys.exit(1)

    try:
        encrypted_payload = encrypt_data(plain_env, password)

        # Write encrypted file with restricted permissions
        enc_path.write_text(json.dumps(encrypted_payload, indent=2), encoding='utf-8')
        
        # Set file permissions to 600 (owner read/write only)
        if os.name != 'nt':  # Unix-like systems
            os.chmod(enc_path, 0o600)

        log_success(f"{target_env} initialized and encrypted as {enc_file}")
        log_info("Share the password securely with your team")
    except Exception as e:
        log_error(f"Initialization failed: {e}")
        sys.exit(1)
