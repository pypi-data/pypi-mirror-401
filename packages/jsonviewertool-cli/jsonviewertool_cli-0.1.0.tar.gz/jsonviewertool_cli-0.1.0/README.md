# jsonviewertool-cli

A lightweight Python CLI for **validating**, **formatting (pretty print)**, **minifying**, and **converting YAML → JSON**.

👉 For advanced online tools like **YAML to JSON**, **JSON Viewer**, and **JSON Formatter**, visit:
- https://jsonviewertool.com
- YAML → JSON: https://jsonviewertool.com/yaml-to-json

---

## Install

```bash
pip install jsonviewertool-cli
```

## Usage

### Pretty format JSON
```bash
jsonviewertool format input.json
# or from stdin
cat input.json | jsonviewertool format
```

### Validate JSON
```bash
jsonviewertool validate input.json
```

### Minify JSON
```bash
jsonviewertool minify input.json
```

### YAML → JSON
```bash
jsonviewertool yaml2json input.yaml
```

---

## Why this exists

This CLI is intentionally small and fast for local workflows (CI pipelines, quick checks, scripts).
If you need a full-featured browser toolset (viewer, formatter, validator, converters), use:

🔗 https://jsonviewertool.com

---

## License

MIT
