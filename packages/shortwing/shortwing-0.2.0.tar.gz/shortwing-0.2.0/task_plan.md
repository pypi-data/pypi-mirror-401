Below is a **developer-ready specification** for **Shortwing**, compiled from our full design conversation. This is written so an engineer can immediately begin implementation with minimal ambiguity.

---

# Shortwing CLI – Developer Specification

## 1. Overview

**Shortwing** is a lightweight command-line wrapper around the Python **`dimcli`** package.
Its goal is to preserve the *input ergonomics of the existing `dimcli` CLI* while providing:

* Cleaner, predictable behavior
* Direct execution via `dimcli.Dsl().query(...)`
* Raw JSON output suitable for automation and pipelines

Shortwing is intentionally minimal and script-friendly.

---

## 2. Goals & Non-Goals

### Goals

* Accept DSL queries via **stdin** or **single argument**
* Pass queries **unchanged** to `dimcli.Dsl().query()`
* Return **raw JSON** responses (pretty-printed by default)
* Work seamlessly in Unix pipelines
* Be deterministic and silent on success

### Non-Goals

* No query rewriting or DSL validation
* No interactive UI
* No built-in pagination (v1)
* No result post-processing (tables, summaries, etc.)

---

## 3. CLI Name & Invocation

### Executable

```bash
shortwing
```

### Supported Invocation Forms

```bash
shortwing "search grants for \"malaria\" return researchers"
```

```bash
echo 'search grants for "malaria" return researchers' | shortwing
```

```bash
shortwing query "search grants for \"malaria\" return researchers"
```

```bash
echo 'search grants for "malaria"' | shortwing query --compact
```

---

## 4. Input Handling

### Sources (precedence order)

1. **stdin** (if piped)
2. **positional argument**

If **both stdin and an argument are present**, **stdin wins**.

### Multi-line stdin

* Entire stdin is treated as **one query**
* **Leading and trailing whitespace is trimmed**
* Internal whitespace and newlines are preserved exactly

### DSL Handling

* No prefixing (`dsl`)
* No normalization
* No validation
* Input is passed **verbatim** to:

```python
Dsl().query(query_string)
```

---

## 5. Authentication & Configuration

### Default Authentication

* Environment variables:

  * `DIMENSIONS_KEY` **(required)**
  * `DIMENSIONS_ENDPOINT` (optional)

### Overrides

* CLI flags override environment variables

```bash
shortwing --key abc --endpoint https://app.dimensions.ai
```

### Missing Credentials

* If `DIMENSIONS_KEY` is missing:

  * Print error to **stderr**
  * Exit with **code 2**
  * No stdout output

---

## 6. Command Structure

### Root Command

```bash
shortwing [OPTIONS] [QUERY]
```

### Subcommand

```bash
shortwing query [OPTIONS] [QUERY]
```

* `query` is the only subcommand in v1
* Root invocation behaves as an alias to `query`

---

## 7. Flags (v1)

| Flag         | Description                          |
| ------------ | ------------------------------------ |
| `--key`      | Override `DIMENSIONS_KEY`            |
| `--endpoint` | Override `DIMENSIONS_ENDPOINT`       |
| `--compact`  | Output compact JSON (no indentation) |
| `--pretty`   | Force pretty JSON (default)          |
| `--help`     | CLI help                             |
| `--version`  | Print version                        |

---

## 8. Output Behavior

### Success

* **stdout**: JSON only
* **stderr**: empty
* Exit code: **0**

### Default Formatting

* Pretty-printed JSON (`indent=2`)

### Compact Mode

```bash
shortwing --compact
```

* Single-line JSON (no extra whitespace)

---

## 9. Error Handling

### Authentication Errors

* Missing API key:

  * stderr: clear error message
  * exit code: **2**

### Query / API Errors

* Pass through **raw error JSON** to stdout
* No modification or wrapping
* Exit code: **1**

### Example

```json
{
  "error": {
    "message": "Invalid DSL syntax",
    "code": 400
  }
}
```

---

## 10. Exit Codes

| Code | Meaning                            |
| ---- | ---------------------------------- |
| 0    | Success                            |
| 1    | Query/API error                    |
| 2    | Configuration/authentication error |

---

## 11. Architecture

### Language

* Python 3.9+

### Dependencies

* `dimcli`
* CLI framework (recommended): `click` 
* package manager `uv`

### High-Level Flow

```text
Parse args
↓
Resolve credentials (flags > env)
↓
Read stdin or argument
↓
Trim leading/trailing whitespace
↓
Initialize dimcli login
↓
Execute Dsl().query(query)
↓
Print JSON
↓
Exit
```



## 13. Testing Plan

### Unit Tests

* Argument vs stdin precedence
* Whitespace trimming behavior
* Flag overrides env vars
* Missing key → exit code 2
* Compact vs pretty output

### Integration Tests

* Mock `Dsl().query()`
* Successful query JSON passthrough
* Error JSON passthrough
* Endpoint override behavior

### CLI Tests

* Pipe compatibility
* Large JSON output handling
* Unicode / UTF-8 DSL queries

---

## 14. Future Enhancements (Out of Scope)

* Pagination support
* Streaming output
* JSON schema validation
* Query linting
* Output formatters (CSV, NDJSON, tables)

---

## 15. Summary

**Shortwing** is a:

* Deterministic
* Minimal
* Unix-friendly
* Python-native

CLI that treats **Dimensions DSL as a first-class data interface**, not a human UI.

