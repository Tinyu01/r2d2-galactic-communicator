# 🤖 Contributing to the R2-D2 Galactic Communicator

Welcome, Rebel coder! The Rebel Alliance needs your skills to enhance the **R2-D2 Galactic Communicator**. This guide outlines how to contribute to our mission to decode Imperial secrets.

## Getting Started

1. **Fork the Repository**:
   - Fork [r2d2-galactic-communicator](https://github.com/yourusername/r2d2-galactic-communicator).
   - Clone your fork: `git clone https://github.com/yourusername/r2d2-galactic-communicator.git`.

2. **Set Up Development Environment**:
   - Install Python 3.10+ and [Poetry](https://python-poetry.org/).
   - Run `poetry install` and `poetry shell` to set up the virtual environment.

3. **Create a Feature Branch**:
   - Use the naming convention: `feat/description`, `fix/bug-description`, `docs/update-type`, etc.
   - Example: `git checkout -b feat/add-audio-support`.

## Development Workflow

1. **Write Code**:
   - Follow PEP 8 and use type hints.
   - Maintain Star Wars theming (e.g., "Imperial interference" for errors).
   - Update tests to maintain 100% coverage.

2. **Test Changes**:
   - Run `poetry run pytest --cov=r2d2_morse` to ensure tests pass.
   - Add new tests for new features using pytest and Hypothesis.

3. **Commit Changes**:
   - Use [Conventional Commits](https://www.conventionalcommits.org/):
     - `feat`: New features
     - `fix`: Bug fixes
     - `docs`: Documentation updates
     - `test`: Test additions
   - Example: `git commit -m "feat: add emoji translation for Yoda 🧙"`.

4. **Submit a Pull Request**:
   - Push your branch: `git push origin feat/add-audio-support`.
   - Create a PR to the `main` branch with a clear description and reference to the related issue (e.g., `Closes #12`).
   - Ensure all CI checks pass (tests, linting).

5. **Code Review**:
   - Respond to feedback promptly.
   - PRs are merged after passing CI and review.

## Testing Guidelines

- Write unit tests for all new functionality.
- Use Hypothesis for property-based testing of edge cases.
- Ensure 100% code coverage: `poetry run pytest --cov=r2d2_morse --cov-report=html`.
- Test across Python 3.10–3.12 using GitHub Actions.

## Star Wars Theming

- Use terminology like "Rebel Terminal," "Galactic Code Archive," and "Imperial interference."
- Add Star Wars-themed error messages and visuals (e.g., lightsaber colors, R2-D2 ASCII art).
- Suggest new emojis (e.g., 🧙 for Yoda) in the Galactic Code Archive.

## Issue Reporting

- Open an issue for bugs, enhancements, or questions.
- Use labels: `bug`, `enhancement`, `documentation`, etc.
- Provide detailed steps to reproduce bugs and expected behavior.

## Code of Conduct

Be respectful and inclusive, like a true Jedi. Harassment or inappropriate behavior will not be tolerated.

*May the Force be with you!*