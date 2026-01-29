# blendconf

A powerful CLI tool for merging and converting configuration files across different formats.

## Features

- 🔀 **Merge multiple config files** - Combine configurations from different sources
- 🔄 **Format conversion** - Convert between JSON, YAML, TOML, and ENV formats
- 📤 **Flexible output** - Write to file or print to stdout
- 🎯 **Simple CLI** - Easy to use command-line interface

## Supported Formats

- JSON (`.json`)
- YAML (`.yaml`, `.yml`)
- TOML (`.toml`)
- ENV (`.env`)

## Installation

We recommend using [uv](https://github.com/astral-sh/uv) for the best experience, [alternative install methods are available here](https://docs.astral.sh/uv/getting-started/installation/).:

```bash
# Install uv (if you haven't already)
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Then, you can run blendconf directly without installation:

```
# Run blendconf directly with uvx (no installation needed!)
uvx blendconf --help
```

## Usage

### Merge Configuration Files

Merge multiple config files and save the result:

```bash
uvx blendconf config1.json config2.json -o merged.json
```

Merge configs and print to stdout:

```bash
uvx blendconf config1.toml config2.toml
```

The output format is determined by the first input file when printing to stdout, or by the output file extension when using `-o`.

### Convert Between Formats

Convert a JSON file to TOML:

```bash
uvx blendconf config.json -o config.toml
```

Convert YAML to JSON:

```bash
uvx blendconf settings.yaml -o settings.json
```

Print converted file to stdout (uses input file format by default):

```bash
uvx blendconf config.json  # outputs as JSON
```

### Merge Strategy

You can specify how configs should be merged using the `--strategy` or `-s` option:

```bash
uvx blendconf base.yaml overrides.yaml -o final.yaml --strategy replace
```

Available strategies:
- `replace` (default): Later values replace earlier ones
- `append`: Lists are concatenated, dictionaries are merged

## Examples

Check out the [examples](examples/) directory for sample configuration files:

```bash
# Merge two JSON configs
uvx blendconf examples/config1.json examples/config2.json -o merged.json

# Convert JSON to TOML
uvx blendconf examples/config1.json -o config.toml

# Merge YAML and TOML (prints as YAML)
uvx blendconf examples/settings.yaml examples/overrides.toml

# Merge and convert to different format
uvx blendconf examples/settings.yaml examples/overrides.toml -o final.json
```

### Example: Merging Configs

**config1.json:**
```json
{
  "database": {
    "host": "localhost",
    "port": 5432
  },
  "logging": {
    "level": "INFO"
  }
}
```

**config2.json:**
```json
{
  "database": {
    "host": "production.db.example.com",
    "username": "admin"
  },
  "api": {
    "timeout": 30
  }
}
```

**Result:**
```bash
$ uvx blendconf config1.json config2.json
{
    "database": {
        "host": "production.db.example.com",
        "port": 5432,
        "username": "admin"
    },
    "logging": {
        "level": "INFO"
    },
    "api": {
        "timeout": 30
    }
}
```

## Library Usage

While blendconf is primarily designed as a CLI tool, you can also use it as a Python library:

```python
from pathlib import Path
from blendconf import merge_configs, dump_file, MergeStrategy

# Merge configs
merged = merge_configs(
    [Path("config1.json"), Path("config2.json")],
    MergeStrategy.REPLACE
)

# Save result
dump_file(merged, Path("output.yaml"), "yaml")
```

**Note:** The library currently has dependencies on `typer` and `rich` (used by the CLI). If you want to use blendconf as a library-only package without these dependencies, PRs are welcome! 🙏

## Development

```bash
# Clone the repository
git clone https://github.com/hwmrocker/blendconf.git
cd blendconf

# Install dependencies with uv
uv sync

# Run tests
uv run pytest

# Run the CLI locally
uv run blendconf --help
```

## Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests
- Improve documentation

Especially welcome: **PRs to make the library usable without CLI dependencies!**

## License

See [LICENSE](LICENSE) file for details.
