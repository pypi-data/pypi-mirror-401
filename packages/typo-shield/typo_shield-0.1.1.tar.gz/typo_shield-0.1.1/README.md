# typo-shield 🛡️

[![PyPI version](https://img.shields.io/pypi/v/typo-shield.svg)](https://pypi.org/project/typo-shield/)
[![Python versions](https://img.shields.io/pypi/pyversions/typo-shield.svg)](https://pypi.org/project/typo-shield/)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://www.apache.org/licenses/LICENSE-2.0)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)](https://github.com/kszmigiel/typo-shield/actions)

**Security guard against typosquatting in Python dependencies**

A CLI tool and pre-commit hook that detects suspicious package names and imports in your git diff to protect against supply chain attacks.

## 🚀 Quick Start

```bash
# Install
pip install typo-shield

# Scan staged changes
typo-shield scan

# Scan commit range
typo-shield scan --diff-range main...feature

# JSON output for CI
typo-shield scan --format json
```

## 📋 Features

- ✅ Detects typosquatting in dependencies (Levenshtein distance)
- ✅ Scans Python imports (AST-based)
- ✅ Parses `requirements.txt` and `pyproject.toml` (PEP 621 + Poetry)
- ✅ Identifies missing dependencies
- ✅ Pre-commit hook support
- ✅ JSON output for CI/CD
- ✅ Configurable via `.typo-shield.toml`

## 📦 Installation

**Requirements:** Python 3.10 or newer

```bash
pip install typo-shield
```

**Development installation:**

```bash
git clone https://github.com/kszmigiel/typo-shield
cd typo-shield
pip install -e ".[dev]"
```

## 🔍 Usage

### Basic scanning

```bash
# Scan staged changes (default)
typo-shield scan

# Scan specific commit range
typo-shield scan --diff-range main...feature

# Strict mode (fail on unknown imports)
typo-shield scan --strict-imports

# Fail on warnings too
typo-shield scan --fail-on warn
```

### Output formats

```bash
# Human-readable text (default)
typo-shield scan

# JSON for CI/CD
typo-shield scan --format json
```

### Exclude patterns

```bash
# Exclude test files
typo-shield scan --exclude "tests/**" --exclude "*.pyc"
```

## 🪝 Pre-commit Hook

Integrate typo-shield with [pre-commit](https://pre-commit.com/) to automatically check your dependencies on every commit.

Add to your `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/kszmigiel/typo-shield
    rev: v0.1.0  # Use the latest version
    hooks:
      - id: typo-shield
```

For stricter checking (fail on warnings too):

```yaml
repos:
  - repo: https://github.com/kszmigiel/typo-shield
    rev: v0.1.0
    hooks:
      - id: typo-shield-strict
```

Then install the pre-commit hook:

```bash
pre-commit install
```

Now typo-shield will run automatically before each commit! 🎉

**Note:** Pre-commit hooks run on staged changes only. If you want to scan a specific commit range, use the CLI directly.

## ⚙️ Configuration

Create `.typo-shield.toml` in your repository root:

```toml
[policy]
fail_on = "fail"
strict_imports = false

[allow]
deps = ["internal-lib", "private-package"]
modules = ["internalpkg"]

[exclude]
paths = ["tests/**", "docs/**"]
```

## 🚦 Exit Codes

- `0` - No issues found
- `1` - Security issues detected (FAIL or WARN based on `--fail-on`)
- `2` - Tool error (git not found, invalid config, etc.)

## 📊 Example Output

```
🔍 typo-shield scan

Summary: 1 FAIL, 2 WARN, 5 INFO

❌ FAILURES (1)
──────────────────────────────────────────────────────
[TS001] Suspected typosquat
  File: requirements.txt:12
  Package: reqeusts
  Reason: Very similar to popular package "requests" (distance: 1)
  Suggestion: Did you mean "requests"?

⚠️  WARNINGS (2)
──────────────────────────────────────────────────────
[TS101] Import without declared dependency
  File: app.py:5
  Module: numpy
  Suggestion: Add "numpy" to your dependencies

Result: FAILED (exit code 1)
```

## 🛠️ Development

```bash
# Install with dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run tests with coverage
pytest --cov

# Linting
ruff check .

# Type checking
mypy typo_shield/
```

## 📜 License

Apache License 2.0 - see [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 🔗 Links

- **Repository**: https://github.com/kszmigiel/typo-shield
- **Issues**: https://github.com/kszmigiel/typo-shield/issues
- **PyPI**: https://pypi.org/project/typo-shield/

## ⚠️ Status

**Alpha (v0.1.0)** - Under active development. API may change.

---

**Made with ❤️ to protect the Python ecosystem from supply chain attacks.**
