"""Decrypt .env.enc files."""

import os
import json
import sys
from pathlib import Path
from envlock.crypto import decrypt_data
from envlock.utils import (
    prompt_hidden, prompt, select_file, colors,
    log_intro, log_step, log_success, log_error, log_info
)


def decrypt_env() -> None:
    """Decrypt a .env.enc file with a password."""
    log_intro("DECRYPT ENVIRONMENT")

    cwd = Path.cwd()
    files = sorted([f.name for f in cwd.iterdir() if f.is_file() and f.name.startswith(".env.enc")])

    if len(files) == 0:
        log_error("No .env.enc files found")
        sys.exit(1)

    log_step(1, "Selecting file...")
    enc_file = select_file(files, "Select a file to decrypt: ")

    suffix = enc_file.replace(".env.enc", "")
    env_file = f".env{suffix}"
    env_path = cwd / env_file

    if env_path.exists():
        answer = prompt(f"{colors.fg.yellow}⚠️  {env_file} already exists. Replace it? (y/N): {colors.reset}")

        if answer.lower() != "y":
            log_error("Aborted")
            sys.exit(0)

    log_step(2, "Decrypting...")
    
    try:
        encrypted_payload = json.loads((cwd / enc_file).read_text(encoding='utf-8'))
    except Exception as e:
        log_error("Failed to read or parse encrypted file. It might be corrupted.")
        sys.exit(1)

    password = prompt_hidden("Enter decryption password: ")

    try:
        decrypted_env = decrypt_data(encrypted_payload, password)

        # Write decrypted file with restricted permissions
        env_path.write_text(decrypted_env, encoding='utf-8')
        
        # Set file permissions to 600 (owner read/write only)
        if os.name != 'nt':  # Unix-like systems
            os.chmod(env_path, 0o600)

        log_success(f"{env_file} created.")
        log_info("Do NOT commit this file.")
    except Exception as e:
        log_error("Decryption failed. Wrong password or corrupted file.")
        sys.exit(1)
