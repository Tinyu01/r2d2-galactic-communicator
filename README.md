# 🤖 R2-D2 Galactic Communicator

*"This is R2-D2, your trusted Astromech Droid, ready to assist with all your covert communications."*

A professional-grade Morse code translator built in Python 3.10+ with Star Wars theming. Features bidirectional translation between text and International Morse Code, custom emoji mappings for Rebel transmissions, and a rich CLI interface.

## ✨ Features

- **Core Translation Engine**: Bidirectional text ↔ Morse code conversion with emoji support
- **Rebel Terminal (CLI)**: Rich-powered interface with R2-D2 ASCII art and lightsaber-colored outputs
- **Galactic Code Archive**: JSON-based storage for Morse mappings and user preferences
- **Comprehensive Testing**: 100% code coverage with pytest and Hypothesis
- **Deployment Ready**: Packaged for PyPI, PyInstaller executables, and Docker containers
- **Star Wars Theming**: Custom emoji mappings (⚡ for Force lightning, 🚀 for X-Wing, etc.)

## 🛠️ Installation

### Prerequisites

- Python 3.10+
- [Poetry](https://python-poetry.org/) for dependency management
- Git

### Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/r2d2-galactic-communicator.git
cd r2d2-galactic-communicator

# Install dependencies
poetry install

# Activate virtual environment
poetry shell
```

## 🚀 Usage

Run `morse-cli --help` for complete command reference.

### Encode Text to Morse

```bash
morse-cli encode "MAY THE FORCE BE WITH YOU"
```

**Output:**
```
🤖 R2-D2 Galactic Communicator: Ready for Transmission!
┌──────────┬───────────────────────────────────────────────┐
│ Type     │ Content                                       │
├──────────┼───────────────────────────────────────────────┤
│ 📝 Original │ MAY THE FORCE BE WITH YOU                  │
│ 📡 Morse Code │ -- .- -.-- / - .... . / ..-. --- .-. -.-. . / -... . / .-- .. - .... / -.-- --- ..- │
└──────────┴───────────────────────────────────────────────┘
✅ Successfully encoded 21 characters into Morse code.
```

### Decode Morse to Text

```bash
morse-cli decode "-- .- -.-- / - .... . / ..-. --- .-. -.-. . / -... . / .-- .. - .... / -.-- --- ..-"
```

### Batch Processing

```bash
morse-cli batch input.txt --direction encode --output secret_morse.txt
```

### View Supported Characters

```bash
morse-cli chars
```

## 📁 Project Structure

```
r2d2-galactic-communicator/
├── src/
│   └── r2d2_morse/
│       ├── __init__.py
│       ├── galactic_morse.py    # Core translation logic
│       ├── cli.py              # CLI interface
│       └── storage.py          # JSON storage handler
├── tests/
│   └── test_galactic_morse.py  # Test suite
├── data/
│   ├── morse_dictionary.json   # Morse code mappings
│   ├── user_preferences.json   # User settings
│   └── sample_messages.json    # Star Wars examples
├── docs/                       # Documentation
├── .github/workflows/          # CI/CD pipelines
├── pyproject.toml              # Poetry configuration
├── README.md
├── CHANGELOG.md
└── LICENSE
```

## 🧪 Testing

The project maintains 100% test coverage with comprehensive testing:

- **Unit Tests**: Full coverage using pytest
- **Property-Based Tests**: Hypothesis generates random inputs for validation
- **Integration Tests**: CLI workflows and file I/O validation
- **CI/CD**: GitHub Actions across Python 3.10–3.12 on multiple platforms

```bash
# Run tests with coverage
poetry run pytest --cov=r2d2_morse
```

## 🤝 Contributing

1. Fork the repository and create a feature branch (`feat/add-new-feature`)
2. Develop and test changes (maintain 100% coverage)
3. Use conventional commits (e.g., `feat: add emoji support`)
4. Submit a pull request

See `CONTRIBUTING.md` for detailed guidelines.

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

## 📞 Contact

- Open an issue on [GitHub](https://github.com/yourusername/r2d2-galactic-communicator/issues)
- Email: your.email@example.com

---

*May the Force be with you!* ⭐