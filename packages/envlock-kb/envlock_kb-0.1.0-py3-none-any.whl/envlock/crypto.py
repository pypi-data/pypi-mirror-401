"""Cryptographic functions for encrypting and decrypting data."""

import os
import base64
import hashlib
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt


# Constants
KEY_LENGTH = 32  # 256 bits for AES-256
IV_LENGTH = 12   # 96 bits (recommended for GCM)
SALT_LENGTH = 16  # 128 bits


def derive_key(password: str, salt: bytes) -> bytes:
    """
    Derive an encryption key from a password using scrypt.
    
    Args:
        password: The password to derive the key from
        salt: The salt to use for key derivation
        
    Returns:
        The derived key bytes
    """
    kdf = Scrypt(
        salt=salt,
        length=KEY_LENGTH,
        n=2**14,  # CPU/memory cost parameter
        r=8,      # Block size parameter
        p=1,      # Parallelization parameter
        backend=default_backend()
    )
    return kdf.derive(password.encode('utf-8'))


def encrypt_data(plain_text: str, password: str) -> dict:
    """
    Encrypt plain text data with a password.
    
    Args:
        plain_text: The text to encrypt
        password: The encryption password
        
    Returns:
        A dictionary containing the encrypted data and metadata
    """
    # Generate random salt and IV
    salt = os.urandom(SALT_LENGTH)
    iv = os.urandom(IV_LENGTH)
    
    # Derive key from password
    key = derive_key(password, salt)
    
    # Create cipher and encrypt
    aesgcm = AESGCM(key)
    encrypted = aesgcm.encrypt(iv, plain_text.encode('utf-8'), None)
    
    # In GCM mode, the auth tag is appended to the ciphertext
    # We need to split it: last 16 bytes are the tag
    ciphertext = encrypted[:-16]
    auth_tag = encrypted[-16:]
    
    return {
        'version': 1,
        'salt': base64.b64encode(salt).decode('utf-8'),
        'iv': base64.b64encode(iv).decode('utf-8'),
        'authTag': base64.b64encode(auth_tag).decode('utf-8'),
        'data': base64.b64encode(ciphertext).decode('utf-8'),
    }


def decrypt_data(payload: dict, password: str) -> str:
    """
    Decrypt encrypted data with a password.
    
    Args:
        payload: Dictionary containing encrypted data and metadata
        password: The decryption password
        
    Returns:
        The decrypted plain text
        
    Raises:
        Exception: If decryption fails (wrong password or corrupted data)
    """
    # Decode all base64 values
    salt = base64.b64decode(payload['salt'])
    iv = base64.b64decode(payload['iv'])
    auth_tag = base64.b64decode(payload['authTag'])
    ciphertext = base64.b64decode(payload['data'])
    
    # Derive key from password
    key = derive_key(password, salt)
    
    # Create cipher and decrypt
    # AESGCM expects the auth tag appended to the ciphertext
    encrypted_with_tag = ciphertext + auth_tag
    
    aesgcm = AESGCM(key)
    decrypted = aesgcm.decrypt(iv, encrypted_with_tag, None)
    
    return decrypted.decode('utf-8')
