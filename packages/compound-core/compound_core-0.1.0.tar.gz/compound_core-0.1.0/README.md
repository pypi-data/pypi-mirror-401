# compound-core

Core utilities for Compound System agent infrastructure.

## Components

- **types** (`compound_core.types`): Shared dataclasses like `AgentPersona` and `AgentResult`.
- **registry** (`compound_core.registry`): Model resolution and fallback chains.
- **config** (`compound_core.config`): Centralized limit management.
- **cache** (`compound_core.cache`): Caching utilities.
- **paths** (`compound_core.paths`): Path resolution.
- **interfaces** (`compound_core.interfaces`): Protocol definitions for `PersonaProvider`, `AgentExecutor`, etc.

## Installation

```bash
pip install compound-core
```

## Development

```bash
pip install -e ".[dev]"
pytest tests/
```
