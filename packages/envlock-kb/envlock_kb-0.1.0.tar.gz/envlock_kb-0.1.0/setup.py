from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="envlock-kb",
    version="0.1.0",
    author="Kukil Bharadwaj",
    author_email="kukilbharadwaj@example.com",
    description="Secure environment variable management - Encrypt and decrypt .env files with AES-256-GCM",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kukilbharadwaj/envlock",
    project_urls={
        "Bug Tracker": "https://github.com/kukilbharadwaj/envlock/issues",
        "Documentation": "https://github.com/kukilbharadwaj/envlock#readme",
        "Source Code": "https://github.com/kukilbharadwaj/envlock",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Security :: Cryptography",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Systems Administration",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Environment :: Console",
    ],
    python_requires=">=3.8",
    install_requires=[
        "cryptography>=41.0.0",
    ],
    entry_points={
        "console_scripts": [
            "envlock=envlock.cli:main",
        ],
    },
    keywords=["env", "dotenv", "secrets", "encryption", "cli", "security", "aes", "environment-variables", "configuration"],
    license="MIT",
)
