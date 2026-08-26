# dsh-model-manager

![CI](https://github.com/XucroYuri/dsh-model-manager/actions/workflows/ci.yml/badge.svg) ![License](https://img.shields.io/github/license/XucroYuri/dsh-model-manager)

Manage enabled model allowlists in DeepSeek Harness to keep model pickers clean.

> Status: Stable

## Features

- List enabled models
- Enable/disable models
- Search models
- Write to llm-pi-ai provider models
- Native Cordis command plugin

## Requirements

- DeepSeek Harness (DSH) 0.1.1+
- OpenCode CLI (optional, for sync/catalog/bridge features)
- Node.js 22+
- Python 3.12+ (only for fallback CLI tests)

## Installation

Add the plugin to your DSH profile:

```bash
cd ~/.dsh/profiles/tools
npm install @xucroyuri/dsh-model-manager
```

Then add to `cordis.patch.yml`:

```yaml
- insert:
    - id: model-manager
      name: '@xucroyuri/dsh-model-manager'
```

## Usage

```bash
dsh --profile tools models list
dsh --profile tools models enable deepseek/deepseek-v4-flash
dsh --profile tools models disable deepseek/deepseek-v4-flash
dsh --profile tools models search glm
```

## Development

```bash
node --check src/index.js
PYTHONPATH=src python3 -m unittest discover -s tests -p 'test_*.py' -v
```

## License

MIT
