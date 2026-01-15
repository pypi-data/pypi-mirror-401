# docmood

A Python tool that checks the grammatical mood consistency of your function and method docstrings.

## What it does

`docmood` scans your Python project and verifies that all function/method docstrings follow a consistent grammatical style:

- **Imperative mood**: "Return the value", "Get the user", "Calculate the sum"
- **Third-person mood**: "Returns the value", "Gets the user", "Calculates the sum"

## Installation

From PyPI:

```bash
pip install docmood
```

## Usage

Run in your project directory:

```bash
docmood .
```

Or as a module:

```bash
python -m docmood /path/to/project
```

### Example Output

```
[docmood] Checking that all method docstrings use imperative mood

[docmood] Found 15 method docs: 13/15 passed (87%)

Failed docstrings:
  src/example.py:42 (detected: imperative, expected: third person)
  src/foo_bar.py:98 (detected: imperative, expected: third person)
```

## Configuration

`docmood` can be configured via `pyproject.toml` or `docmood.ini` in your project root.

### Option 1: pyproject.toml (recommended)

Add a `[tool.docmood]` section:

```toml
[tool.docmood]
# Expected mood for all docstrings
# Options: "imperative" or "third_person"
# Default: "imperative"
mood = "imperative"

# Whether to allow docstrings with unknown/undetectable mood
# If true, unknown mood is counted as passed (with a warning)
# If false, unknown mood is counted as failed
# Default: true
allow_unknown = true

# Additional directory names to skip during scanning (added to defaults)
# Default dirs always skipped: .git, .hg, .svn, .mypy_cache, .pytest_cache, 
#   .ruff_cache, .tox, .nox, __pycache__, build, dist, site-packages, venv, .venv
# Example: skip_dirs = ["node_modules", "coverage"] will skip the defaults PLUS node_modules and coverage
skip_dirs = ["node_modules", "coverage"]
```

### Option 2: docmood.ini

Create a `docmood.ini` file in your project root:

```ini
[docmood]
mood = imperative
allow_unknown = true
skip_dirs = node_modules,coverage
```

See `docmood.ini.example` for a complete example with comments.

### Configuration Options

| Option | Values | Default | Description |
|--------|--------|---------|-------------|
| `mood` | `imperative`, `third_person` | `imperative` | Expected grammatical mood for docstrings |
| `allow_unknown` | `true`, `false` | `true` | Whether to treat undetectable mood as passed |
| `skip_dirs` | List of directory names | `[]` (empty) | **Additional** directories to skip (added to defaults) |

**Directories always skipped by default**: `.git`, `.hg`, `.svn`, `.mypy_cache`, `.pytest_cache`, `.ruff_cache`, `.tox`, `.nox`, `__pycache__`, `build`, `dist`, `site-packages`, `venv`, `.venv`

**Note**: The `skip_dirs` option is **additive**. If you specify `skip_dirs = ["node_modules"]`, the tool will skip all default directories PLUS `node_modules`.

## Exit Codes

- `0`: All docstrings passed
- `1`: One or more docstrings failed validation

## Development

Development instructions live in `CONTRIBUTING.md`.

## License

MIT
