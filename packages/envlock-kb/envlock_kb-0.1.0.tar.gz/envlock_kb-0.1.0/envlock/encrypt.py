"""Encrypt .env files."""

import os
import json
import sys
from pathlib import Path
from envlock.crypto import encrypt_data
from envlock.utils import (
    prompt_hidden, find_env_files, select_file, colors,
    log_intro, log_step, log_success, log_error
)


def encrypt_env() -> None:
    """Encrypt a .env file with a password."""
    log_intro("ENCRYPT ENVIRONMENT")

    env_files = find_env_files()

    if len(env_files) == 0:
        log_error("No .env files found")
        sys.exit(1)

    log_step(1, "Selecting file...")
    target_env = select_file(env_files, "Select a file to encrypt: ")

    env_path = Path.cwd() / target_env
    suffix = target_env.replace(".env", "")
    enc_file = f".env.enc{suffix}"
    enc_path = Path.cwd() / enc_file

    log_step(2, "Encrypting...")
    
    try:
        plain_env = env_path.read_text(encoding='utf-8')
    except Exception as e:
        log_error(f"Failed to read {target_env}: {e}")
        sys.exit(1)

    password = prompt_hidden("Enter encryption password: ")
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
        
        log_success(f"{target_env} encrypted → {enc_file}")
    except Exception as e:
        log_error(f"Encryption failed: {e}")
        sys.exit(1)
