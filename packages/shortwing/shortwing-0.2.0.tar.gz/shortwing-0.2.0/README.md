# Shortwing

Lightweight CLI wrapper for Dimensions DSL queries via dimcli.

## Installation

```bash
uv pip install .
```

## Usage

```bash
# Query as argument
shortwing "search grants for \"malaria\" return researchers"

# Query from stdin
echo 'search grants for "malaria"' | shortwing

# With subcommand
shortwing query "search grants return grants"

# Compact JSON output
shortwing --compact "search grants"

# Use a specific instance from dsl.ini
shortwing --instance test "search grants"
```

## Configuration

Credentials are loaded in the following order of priority:

1. **CLI flags** (`--key`, `--endpoint`)
2. **Environment variables** (`DIMENSIONS_KEY`, `DIMENSIONS_ENDPOINT`)
3. **dsl.ini file** (default)

### Using dsl.ini (Recommended)

Shortwing uses the same `dsl.ini` configuration file as dimcli. Create the file at `~/.dimensions/dsl.ini`:

```ini
[instance.live]
url=https://app.dimensions.ai
login=
password=
key=your-api-key
```

You can define multiple instances and select them with `--instance`:

```ini
[instance.live]
url=https://app.dimensions.ai
key=your-live-key

[instance.test]
url=https://test.dimensions.ai
key=your-test-key
```

```bash
shortwing --instance test "search grants"
```

### Using Environment Variables

```bash
export DIMENSIONS_KEY=your-api-key
export DIMENSIONS_ENDPOINT=https://app.dimensions.ai  # optional
```

### Using CLI Flags

```bash
shortwing --key your-api-key "search grants"
shortwing --key your-api-key --endpoint https://custom.endpoint.com "search grants"
```

## Exit Codes

- 0: Success
- 1: Query/API error
- 2: Configuration/authentication error
