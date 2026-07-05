# Platform Setup Guides

This page explains how to set up AstraCLI on common platforms: Android (Termux), Windows, Linux, and macOS.

Android (Termux)
- Install Termux from F-Droid, then in Termux:
  ```bash
  pkg update && pkg upgrade
  pkg install python git
  git clone <repo-url> && cd AstraCLI
  pip install -r requirements.txt
  python -m astra
  ```

Windows
- Install Python 3.10+ from python.org. Ensure `pip` and `python` are on PATH.
  ```powershell
  git clone <repo-url>
  cd AstraCLI
  python -m pip install -r requirements.txt
  python -m astra
  ```

Linux
- Install system Python and Git (distribution package manager). Example for Debian/Ubuntu:
  ```bash
  sudo apt update
  sudo apt install python3 python3-venv python3-pip git
  git clone <repo-url>
  cd AstraCLI
  python3 -m pip install --user -r requirements.txt
  python3 -m astra
  ```

macOS
- Use Homebrew or the official Python installer. Example with Homebrew:
  ```bash
  brew install python git
  git clone <repo-url>
  cd AstraCLI
  python3 -m pip install --user -r requirements.txt
  python3 -m astra
  ```

Notes
- On devices without `git`, download the ZIP from GitHub and extract.
- For offline use with local models, ensure model files are placed in `astra/models/` and set the active model via `astra models set <name>`.
