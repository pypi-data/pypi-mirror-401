# {{project_name}}

State management (state changes and state views) for the {{database_name}} database.

## Getting Started

### Prerequisites

- Python 3.12 or later
- componentize-py for WASM compilation
- Access to an EvidentSource server

### Setup

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -e .
```

### Building

Build all components (state changes and state views):

```bash
./build_all.sh
```

This will compile all components to WASM and place them in `dist/`.

### Installing to Server

The install script provides targeted deployment to avoid accidentally creating new versions.

```bash
# Set the server URL (default: http://localhost:3000)
export EVIDENTSOURCE_URL=http://your-server:3000

# List available components
./install.sh --list

# Install specific components (recommended for production)
./install.sh state-change {{first_state_change}}
./install.sh state-view {{first_state_view}}

# Install multiple components at once
./install.sh state-change {{first_state_change}} state-view {{first_state_view}}

# Install all state changes (with confirmation)
./install.sh --all-state-changes

# Install all state views (with confirmation)
./install.sh --all-state-views

# Install everything (with confirmation)
./install.sh --all
```

**Important:** Each deployment creates a new version. Use targeted installation in production.

## Project Structure

```
{{project_name}}/
├── pyproject.toml          # Project configuration
├── README.md
├── build_all.sh            # Build all components
├── install.sh              # Targeted installation script
├── domain/                 # Shared domain types, commands, and events
│   └── __init__.py
├── state_changes/          # State change components (command handlers)
│   └── {{first_state_change}}/
│       ├── __init__.py
│       └── metadata.json   # Component metadata for deployment
├── state_views/            # State view components (materialized views)
│   └── {{first_state_view}}/
│       ├── __init__.py
│       └── metadata.json   # Event selector, query temporality, etc.
└── interface/              # WIT interface (symlink)
    └── decider.wit
```

## Adding New Components

### Adding a State Change

1. Create a new directory in `state_changes/`:

```bash
mkdir -p state_changes/my_new_command
```

2. Create `state_changes/my_new_command/metadata.json`:

```json
{
  "state_change_name": "my-new-command",
  "description": "Description of what this state change does"
}
```

3. Create `state_changes/my_new_command/__init__.py`:

```python
from dataclasses import dataclass
from evidentsource_functions import (
    StateChangeError,
    Command,
    StateChangeMetadata,
    DatabaseAccess,
    ProspectiveEvent,
    StringEventData,
)
from domain import MyCommand
import json
import uuid


def decide(
    db: DatabaseAccess,
    command: MyCommand,
    metadata: StateChangeMetadata,
) -> tuple[list[ProspectiveEvent], list]:
    # Implement your business logic here
    ...
```

4. Update `build_all.sh` to add `"my_new_command"` to the `STATE_CHANGES` array

### Adding a State View

1. Create a new directory in `state_views/`:

```bash
mkdir -p state_views/my_new_view
```

2. Create `state_views/my_new_view/metadata.json`:

```json
{
  "state_view_name": "my-new-view",
  "description": "Description of what this state view does",
  "content_type": "application/json",
  "query_temporality": "revision",
  "event_selector": {
    "equals": {
      "stream": { "stream": "my-stream" }
    }
  }
}
```

**Event Selector Patterns:**

- **Singleton view** (all events on a stream): `{"equals": {"stream": {"stream": "todos"}}}`
- **Entity view** (by subject parameter): `{"equals": {"subject": {"parameter": "account_id"}}}`
- **Complex selectors**: Use `"or"` and `"and"` to combine conditions

**Query Temporality Options:**
- `"revision"`: Query by database revision (OCC consistency)
- `"effective_timestamp"`: Query by time (bi-temporal)

3. Create `state_views/my_new_view/__init__.py`:

```python
from dataclasses import dataclass
from evidentsource_functions import StateViewBase, Event
import json


@dataclass
class MyNewView(StateViewBase):
    # Define your view state fields
    count: int = 0

    def evolve_event(self, event: Event) -> None:
        # Update state based on event
        ...

    def to_dict(self) -> dict:
        return {"count": self.count}

    @classmethod
    def from_dict(cls, data: dict) -> "MyNewView":
        return cls(count=data.get("count", 0))
```

4. Update `build_all.sh` to add `"my_new_view"` to the `STATE_VIEWS` array

## Development

### Running Tests

```bash
pytest
```

### Type Checking

```bash
mypy domain state_changes state_views
```

### Formatting

```bash
ruff format .
ruff check --fix .
```

## Using the EvidentSource SDK

This project uses the EvidentSource Python SDK to reduce boilerplate:

- **StateViewBase**: Abstract base class for state views
- **StateChangeError**: Structured error types for validation, conflict, etc.
- **ProspectiveEvent**: Event builder for state changes
- **Content Negotiation**: Automatic JSON serialization/deserialization
- **Type Conversions**: WIT type utilities

See the SDK documentation for more details.

## License

[Your License Here]
