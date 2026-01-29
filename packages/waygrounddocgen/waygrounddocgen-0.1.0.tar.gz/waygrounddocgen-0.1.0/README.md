# waygrounddocgen

A language-agnostic CLI tool that leverages Cursor AI to automatically discover modules in any codebase and generate comprehensive documentation for each module in parallel.

## Features

- 🔍 **Auto-Discovery**: Uses Cursor AI to identify logical modules/components in any language
- 📝 **Parallel Generation**: Runs multiple Cursor tasks simultaneously for faster documentation
- 🌐 **Language Agnostic**: Works with TypeScript, Python, Go, Java, Rust, and more
- 📋 **Customizable Prompts**: Built-in prompt templates with support for customization
- 📊 **Progress Tracking**: Clear output showing progress and results

## Prerequisites

1. **Python 3.8+** installed
2. **Cursor CLI** installed and available in PATH
   ```bash
   curl https://cursor.com/install -fsS | bash
   ```
   Or from GUI: Cursor → Settings → General → Command Line → Install

## Installation

### From PyPI (Recommended)

```bash
pip install waygrounddocgen
```

### From Source

```bash
git clone https://github.com/gauravmadan/waygrounddocgen.git
cd waygrounddocgen
pip install -e .
```

## Quick Start

```bash
# Check if Cursor CLI is available
waygrounddocgen check

# Discover modules in a repository
waygrounddocgen discover /path/to/your/repo

# Generate documentation (discover + generate)
waygrounddocgen generate /path/to/your/repo
```

## Usage

### Discover Modules

Analyze a repository to identify its logical modules/components:

```bash
waygrounddocgen discover /path/to/repo
waygrounddocgen discover /path/to/repo --output modules.json
```

Output is a JSON file with discovered modules:

```json
{
  "repo_path": "/path/to/repo",
  "language": "typescript",
  "framework": "express",
  "modules": [
    {
      "name": "auth",
      "path": "src/services/auth",
      "description": "Authentication and authorization service",
      "type": "service",
      "files": ["auth.service.ts", "auth.guard.ts"],
      "entry_points": ["AuthService", "authenticate"]
    }
  ]
}
```

### Generate Documentation

Generate documentation for all discovered modules:

```bash
# Full pipeline (discover + generate)
waygrounddocgen generate /path/to/repo

# With custom parallelism
waygrounddocgen generate /path/to/repo --parallel 8

# From existing modules.json
waygrounddocgen generate /path/to/repo --modules modules.json

# Only specific modules
waygrounddocgen generate /path/to/repo --filter auth,users,payments

# Custom output directory
waygrounddocgen generate /path/to/repo --output ./docs/api
```

### Options

| Option | Short | Description |
|--------|-------|-------------|
| `--modules` | `-m` | Path to existing modules.json file |
| `--output` | `-o` | Output directory for documentation |
| `--parallel` | `-p` | Number of parallel Cursor tasks (default: 4) |
| `--filter` | `-f` | Comma-separated list of module names |
| `--template` | `-t` | Prompt template: `generate_doc` (default) or `comprehensive` |
| `--quiet` | `-q` | Suppress streaming output (hide Cursor's thinking) |

## Output Structure

```
docs/generated/
├── README.md           # Index of all modules
├── auth.md            # Auth module documentation
├── users.md           # Users module documentation
├── payments.md        # Payments module documentation
└── ...
```

## Example Workflow

```bash
# 1. Navigate to your repository
cd /path/to/your/project

# 2. Discover modules
waygrounddocgen discover . --output modules.json

# 3. Review discovered modules
cat modules.json | jq '.modules[].name'

# 4. Generate documentation
waygrounddocgen generate . --modules modules.json

# 5. View generated docs
open docs/generated/README.md
```

## Troubleshooting

### Cursor CLI not found

```bash
# Check if cursor is in PATH
which cursor

# If not, install from Cursor:
# Settings → General → Command Line → Install
```

### No modules discovered

1. Check if the repository has a recognizable structure
2. Verify the prompts match your project patterns
3. Run discovery manually and review output

### Parallel tasks timing out

Reduce parallelism or increase timeout:

```bash
# Use fewer parallel tasks
waygrounddocgen generate /path/to/repo --parallel 2
```

## Development

### Install for Development

```bash
git clone https://github.com/gauravmadan/waygrounddocgen.git
cd waygrounddocgen
pip install -e ".[dev]"
```

### Build and Publish

```bash
# Build the package
python -m build

# Upload to PyPI
twine upload dist/*
```

## License

MIT License - see [LICENSE](LICENSE) for details.
