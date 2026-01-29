# 🔐 EnvLock

**Secure environment variable management for teams**

EnvLock is a command-line tool that encrypts and decrypts `.env` files using military-grade AES-256-GCM encryption. Share encrypted environment files safely with your team through version control without exposing sensitive credentials.

[![PyPI version](https://badge.fury.io/py/envlock-kb.svg)](https://badge.fury.io/py/envlock-kb)
[![Python](https://img.shields.io/pypi/pyversions/envlock-kb.svg)](https://pypi.org/project/envlock-kb/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🚀 Quick Start

### Installation

```bash
pip install envlock-kb
```

### Basic Usage

```bash
# Initialize envlock in your project
envlock init

# Encrypt your .env file
envlock encrypt

# Decrypt the .env.enc file
envlock decrypt

# Check version
envlock version
```

## ✨ Features

- 🔒 **AES-256-GCM Encryption** - Military-grade authenticated encryption
- 🔑 **Password-Based Security** - Uses scrypt key derivation (NIST recommended)
- 📁 **Auto .gitignore Setup** - Automatically configures git to ignore sensitive files
- 🎯 **Multiple Environment Support** - Handle dev, staging, production environments
- 🛡️ **Secure Permissions** - Creates files with restricted permissions (0o600)
- ✅ **Tamper Detection** - Authentication tags detect any file modifications
- 🚫 **Zero Dependencies** - Only requires `cryptography` library

## 📖 How It Works

1. **Initialize** (`envlock init`): Sets up `.gitignore` and creates your first encrypted `.env.enc` file
2. **Encrypt** (`envlock encrypt`): Converts `.env` → `.env.enc` with password protection
3. **Decrypt** (`envlock decrypt`): Recovers `.env` from `.env.enc` using your password

The encrypted files (`.env.enc*`) can be safely committed to version control.  
**⚠️ Never commit unencrypted `.env` files!**

## 🔐 Security

EnvLock implements industry-standard security practices:

- **AES-256-GCM**: Authenticated encryption with associated data (AEAD)
- **Scrypt KDF**: Password-based key derivation (N=2^14, r=8, p=1)
- **Random Salt & IV**: Unique values for each encryption operation
- **Authentication Tags**: Cryptographic verification to detect tampering
- **Secure File Permissions**: Restricts file access to owner only (Unix mode 600)

## 💡 Use Cases

- **Team Collaboration**: Share encrypted configs safely via Git
- **CI/CD Pipelines**: Store encrypted secrets in repositories
- **Multi-Environment**: Manage dev, staging, prod credentials separately
- **Backup & Recovery**: Securely backup environment configurations

## 📋 Requirements

- Python >= 3.8
- cryptography >= 41.0.0

## 📝 Example Workflow

```bash
# 1. Create your environment variables
echo "DATABASE_URL=postgresql://localhost/mydb" > .env
echo "API_KEY=secret123" >> .env

# 2. Encrypt the file
envlock encrypt
# Enter password: ****

# 3. Commit the encrypted file
git add .env.enc
git commit -m "Add encrypted environment variables"

# 4. Team members can decrypt
envlock decrypt
# Enter password: ****
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🔗 Links

- **GitHub**: https://github.com/kukilbharadwaj/envlock
- **PyPI**: https://pypi.org/project/envlock-kb/
- **Issues**: https://github.com/kukilbharadwaj/envlock/issues

## ⚠️ Security Notice

- Always use strong, unique passwords for encryption
- Store your password securely (password manager recommended)
- Never commit unencrypted `.env` files to version control
- Regularly rotate sensitive credentials
