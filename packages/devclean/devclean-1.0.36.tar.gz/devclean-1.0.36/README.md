# DevClean

**DevClean** — simple CLI tool for cleaning your project from comments and extra spaces. Can be used for preparing code for deployment, minification, or sharing with a client.

## Features

*   **Multi-Language Support:** Supports Python, JS/TS, HTML, CSS, C++, Java, Go, Rust, SQL, Shell, YAML and more.
*   **Smart Cleaning:** Uses advanced RegEx to **not** delete links in strings (e.g., `http://...`) or hashtags in strings.
*   **Git-Aware:** Automatically reads `.gitignore` and skips ignored files (node_modules, venv, etc.).
*   **Work Modes:** Full clean, only comment removal, or only formatting.
*   **Safe:** DevClean will automatically backup modified files before cleaning.

## Installation

```bash
pip install devclean
