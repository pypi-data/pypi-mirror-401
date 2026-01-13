# Linksopen

`linksopen` is a lightweight command-line tool installed locally
into your user environment. It is designed to be simple, portable,
and shell-friendly, without relying on system-wide package managers.

The project ships with an installer and uninstaller that manage
everything inside `~/.local/bin`.

---

## Features

- Local user installation (no root required)
- Automatic PATH configuration
- Supports Bash, Zsh, and Fish
- Clean uninstall process
- Zero external Python dependencies

---

## Requirements

- Unix-like system (Linux, macOS, WSL)
- Python **3.14+**
- A POSIX-compatible shell (`bash`, `zsh`, or `fish`)

---

## Install

### Via pipx

```bash
pipx install linksopen
```

### Option 2: Manual

Clone the repository and from the project root, run:

```bash
./install.sh
```

## Usage

Once installed, you can run linksopen directly from your terminal. Example usage:

```bash
# Open text file links with default browser.
linksopen textfile_with_link.txt

# It can handle multiple urls.
linksopen my_links.md
```

## Uninstall

```bash
./uninstall.sh
```

This deletes the executable from ~/.local/bin and leaves
shell configuration files untouched.

Restart your shell after uninstalling.

## Project Structure

```
├── linksopen.py        # Main Python executable
├── install.sh          # Installer script
├── uninstall.sh        # Uninstaller script
├── pyproject.toml      # Project metadata
├── README.md           # Documentation
└── LICENSE             # MIT License
```

### Python Metadata

```toml
[project]
name = "linksopen"
version = "0.1.0"
description = "Handle gracefully openning links that are inside text files. Simple as that."
readme = "README.md"
requires-python = ">=3.14"
dependencies = []
```

The project currently has no external dependencies.

### Notes on Implementation

- PATH entries are added only if missing for bash, zsh and fish.
Others posix compliant shells must add ~/.local/bin/ to path manually.

## License

MIT License

Copyright (c) 2026 Rodolfo Souza

Permission is granted to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software.

The Software is provided “as is”, without warranty of any kind.
