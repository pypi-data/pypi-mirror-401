# EvidentSource State Management Template Guide (Python)

## Overview

The `evidentsource-state-management` template provides a complete starting point for building both state changes and state views using the EvidentSource Python SDK with componentize-py.

## Prerequisites

- Python 3.12 or later
- componentize-py (for WASM compilation)
- Access to an EvidentSource server

## Using the Template

### Quick Start

```bash
# Create a new project using the script
./create-project.sh my_app my_database open_account active_accounts

# Navigate to the project
cd my_app

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -e .

# Build all components
./build_all.sh

# Install to EvidentSource server
./install.sh --all
```

### Manual Setup

1. Copy the template directory to your project location
2. Find/replace template variables:
   - `{{project_name}}` -> your project name (e.g., `my_app`)
   - `{{database_name}}` -> your database name
   - `{{first_state_change}}` -> your first state change name (e.g., `open_account`)
   - `{{first_state_view}}` -> your first state view name (e.g., `active_accounts`)

## Generated Structure

```
my_app/
├── pyproject.toml                      # Project configuration with all dependencies
├── README.md                           # Project documentation
├── build_all.sh                        # Build all components
├── install.sh                          # Targeted deployment script
│
├── domain/                             # Shared domain types
│   └── __init__.py                     # Commands, events, domain logic
│
├── state_changes/                      # State change components (command handlers)
│   └── open_account/
│       └── __init__.py                 # Uses create_state_change_handler
│
├── state_views/                        # State view components (materialized views)
│   └── active_accounts/
│       └── __init__.py                 # Uses StateViewBase
│
└── interface/                          # Symlink to WIT interface
    └── decider.wit
```

## Key Features

### 1. Organized Structure

- **domain/** - Shared types used by both state changes and views
- **state_changes/** - One directory per command handler
- **state_views/** - One directory per materialized view

### 2. Targeted Deployment

The `install.sh` script provides safe, targeted deployment:

```bash
# List what's available
./install.sh --list

# Install specific components (recommended)
./install.sh state-change open_account
./install.sh state-view active_accounts

# Install multiple at once
./install.sh state-change open_account state-view active_accounts

# Install all with confirmation
./install.sh --all-state-changes  # Requires confirmation
./install.sh --all-state-views    # Requires confirmation
./install.sh --all                # Requires confirmation
```

### 3. SDK Integration

Both example components use the EvidentSource SDK:

**State Change Example** (`state_changes/open_account/__init__.py`):
- Uses `create_state_change_handler`
- SDK ProspectiveEvent builders
- SDK constraint builders
- Simplified error handling with `StateChangeError`

**State View Example** (`state_views/active_accounts/__init__.py`):
- Uses `StateViewBase` abstract class
- Helper methods for serialization
- Event data parsing utilities

## Adding Components

### Add a State Change

1. Create directory: `state_changes/my_command/`
2. Create `__init__.py` with your implementation
3. Update `build_all.sh` STATE_CHANGES array
4. Update `install.sh` AVAILABLE_STATE_CHANGES array

### Add a State View

1. Create directory: `state_views/my_view/`
2. Create `__init__.py` with your implementation
3. Update `build_all.sh` STATE_VIEWS array
4. Update `install.sh` AVAILABLE_STATE_VIEWS array

## Workflow

### Development

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -e .

# Build everything
./build_all.sh

# Run tests
pytest
```

### Deployment

```bash
# Set server URL
export EVIDENTSOURCE_URL=https://your-server:3000

# List available components
./install.sh --list

# Deploy specific components (safe, recommended)
./install.sh state-change my_command

# Or deploy multiple at once
./install.sh state-change cmd1 state-change cmd2 state-view view1
```

## Safety Features

The install script includes multiple safety features:

1. **Explicit component names required** - No accidental "install everything"
2. **WASM file existence checks** - Fails early if build is missing
3. **Confirmation prompts** - For bulk operations (--all-*)
4. **Clear error messages** - Explains what went wrong
5. **HTTP status checking** - Reports failed uploads

## Best Practices

### Production Deployment

Each deployment creates a new version - Use targeted deployment:

```bash
# Good: Deploy only what changed
./install.sh state-change updated_command

# Avoid: Deploying everything unnecessarily
./install.sh --all  # Only when you mean it!
```

### Testing Before Deployment

```bash
# Build and test locally first
./build_all.sh
pytest

# Verify WASM files exist
ls -lh dist/*.wasm

# Deploy one component at a time
./install.sh state-change my_command
# Test it works
./install.sh state-view my_view
# Test it works
```

### Domain Types

Keep shared types in `domain/`:
- Command dataclasses
- Event definitions
- Common business logic
- Serialization helpers

Both state changes and state views can import domain types.

## Template Customization

After copying the template:

1. **Update domain/__init__.py** with your actual domain types
2. **Implement state changes** in state_changes/*/
3. **Implement state views** in state_views/*/
4. **Update build and install scripts** as you add components
5. **Update README.md** with project-specific information

## Example: Complete Workflow

```bash
# 1. Copy template to your project
cp -r templates/evidentsource-state-management my_app
cd my_app

# 2. Replace template variables
# Edit files to replace {{project_name}}, etc.

# 3. Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 4. Install dependencies
pip install -e .

# 5. Define domain types
# Edit domain/__init__.py

# 6. Implement first state change
# Edit state_changes/open_account/__init__.py

# 7. Implement first state view
# Edit state_views/active_accounts/__init__.py

# 8. Build
./build_all.sh

# 9. Test locally (if you have a local server)
export EVIDENTSOURCE_URL=http://localhost:3000
./install.sh state-change open_account
./install.sh state-view active_accounts

# 10. Add more components as needed
mkdir -p state_changes/another_command
# ... implement, update scripts

# 11. Deploy to production (carefully!)
export EVIDENTSOURCE_URL=https://production:3000
./install.sh state-change open_account  # Only what's ready!
```

## Troubleshooting

### Build Errors

```bash
# Check Python version
python3 --version  # Should be 3.12+

# Check componentize-py is installed
pip show componentize-py

# Verify virtual environment is activated
which python3
```

### Installation Errors

```bash
# Verify WASM file exists
ls -lh dist/my_component.wasm

# Check server connectivity
curl -v $EVIDENTSOURCE_URL/api/v1/catalog

# Try with verbose curl output
# (Edit install.sh, add -v to curl commands)
```

## Support

- SDK Documentation: See `evidentsource-functions` package
- Example Implementation: See repository examples
- WIT Interface: `interface/decider.wit`
