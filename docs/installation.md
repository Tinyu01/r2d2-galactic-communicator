# 📜 Installation: Preparing for Your Mission

This guide walks you through setting up the **R2-D2 Galactic Communicator** on your system, styled as a Rebel mission briefing.

## Prerequisites

- **Python 3.10+**: Ensure Python is installed. Check with `python --version`.
- **Poetry**: Dependency management tool. Install via `curl -sSL https://install.python-poetry.org | python -`.
- **Git**: For cloning the repository. Install via your package manager (e.g., `apt install git` on Ubuntu).

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/r2d2-galactic-communicator.git
cd r2d2-galactic-communicator
```

### 2. Install Dependencies

```bash
poetry install
```

### 3. Activate Virtual Environment

```bash
poetry shell
```

### 4. Verify Installation

```bash
morse-cli --help
```

**Expected output:**

```text
🤖 R2-D2 Galactic Communicator: Ready for Transmission!
...
🟢 All systems operational. Awaiting your orders, Commander.
```

## Troubleshooting

- **Poetry not found**: Ensure Poetry is installed and added to your PATH (`export PATH="$HOME/.local/bin:$PATH"`).
- **Dependency errors**: Run `poetry install --no-cache` to refresh dependencies.
- **Imperial interference**: For other issues, open a GitHub issue with details.

---

*May the Force be with you!*