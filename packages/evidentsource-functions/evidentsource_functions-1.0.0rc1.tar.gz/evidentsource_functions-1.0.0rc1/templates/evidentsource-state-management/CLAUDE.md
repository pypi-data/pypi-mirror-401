# CLAUDE.md

This file provides guidance to Claude Code when working with this EvidentSource project.

## Project Overview

**Project:** {{project_name}}
**Database:** {{database_name}}

This project contains State Changes and State Views for the `{{database_name}}` database.

- **State Changes**: Command handlers in `state_changes/` that validate requests and emit events
- **State Views**: Projections in `state_views/` that materialize events into queryable state

## Build Commands

```bash
# Create virtual environment (first time)
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -e .

# Build all WASM components
./build_all.sh

# Run tests
pytest

# Type checking
mypy .

# Linting
ruff check .
ruff format --check .
```

## Installation

```bash
# Set the server URL (default: http://localhost:3000)
export EVIDENTSOURCE_URL=http://your-server:3000

# List available components
./install.sh --list

# Install specific components (recommended for production)
./install.sh state-change {{first_state_change}}
./install.sh state-view {{first_state_view}}

# Install all (with confirmation)
./install.sh --all
```

## Project Structure

```
{{project_name}}/
├── pyproject.toml              # Project configuration
├── domain/                     # Shared types (events, commands, state DTOs)
│   └── __init__.py
├── state_changes/              # WASM components that handle commands
│   └── {{first_state_change}}/
│       ├── metadata.json       # Component metadata
│       └── __init__.py         # decide function implementation
└── state_views/                # WASM components that project events
    └── {{first_state_view}}/
        ├── metadata.json       # Event selector, query temporality
        └── __init__.py         # reduce function implementation
```

## Key Concepts

### State Changes (decide function)

```python
from evidentsource_functions import create_state_change_handler, Database

def decide(
    db: Database,
    request: CommandRequest,
    metadata: CommandMetadata,
) -> tuple[list[CloudEvent], list[AppendCondition]]:
    # Validate command
    # Query state views if needed
    # Return events and constraints
    pass

handler = create_state_change_handler(decide)
```

- Receive commands, validate them, emit events
- Use DCB constraints for optimistic concurrency
- Can query state views for decision-making

### State Views (reduce function)

```python
from evidentsource_functions import StateViewBase

class MyStateView(StateViewBase[MyState]):
    def reduce(self, state: MyState | None, event: Event) -> MyState:
        # Fold event into state
        pass
```

- Fold events into queryable state
- Must be deterministic and side-effect free
- Called for each matching event in sequence

## Adding New Components

### New State Change

1. Create directory: `mkdir -p state_changes/my_command`
2. Create `state_changes/my_command/__init__.py`
3. Create `state_changes/my_command/metadata.json`:
   ```json
   {
     "state_change_name": "my-command",
     "description": "What this command does"
   }
   ```
4. Implement using `create_state_change_handler`

### New State View

1. Create directory: `mkdir -p state_views/my_view`
2. Create `state_views/my_view/__init__.py`
3. Create `state_views/my_view/metadata.json`:
   ```json
   {
     "state_view_name": "my-view",
     "description": "What this view shows",
     "content_type": "application/json",
     "query_temporality": "revision",
     "event_selector": {"equals": {"stream": {"stream": "my-stream"}}}
   }
   ```
4. Implement using `StateViewBase`

## Testing

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Test specific component
pytest state_changes/{{first_state_change}}/
```

Example test:

```python
from evidentsource_functions.testing import MockDatabase

def test_state_change():
    db = MockDatabase("{{database_name}}").with_revision(0)
    # ... test your decide function
```

## Documentation

- **Getting Started**: https://docs.evidentsource.com/sdks/python/getting-started
- **State Changes**: https://docs.evidentsource.com/concepts/state-changes
- **State Views**: https://docs.evidentsource.com/concepts/state-views
- **DCB Constraints**: https://docs.evidentsource.com/concepts/dcb
