#!/bin/bash
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMPLATE_DIR="$SCRIPT_DIR/evidentsource-state-management"

usage() {
    echo "Create a new EvidentSource Python project from template"
    echo ""
    echo "Usage: $0 <project_name> [database_name] [first_state_change] [first_state_view]"
    echo ""
    echo "Arguments:"
    echo "  project_name        Name of the project (e.g., my_app)"
    echo "  database_name       Name of the database (default: project_name)"
    echo "  first_state_change  Name of the first state change (default: open_account)"
    echo "  first_state_view    Name of the first state view (default: active_accounts)"
    echo ""
    echo "Example:"
    echo "  $0 savings_account savings open_account active_accounts"
}

if [ -z "$1" ]; then
    usage
    exit 1
fi

PROJECT_NAME="$1"
DATABASE_NAME="${2:-$PROJECT_NAME}"
FIRST_STATE_CHANGE="${3:-open_account}"
FIRST_STATE_VIEW="${4:-active_accounts}"

# Convert to Python-safe names (underscores)
PROJECT_NAME_SAFE=$(echo "$PROJECT_NAME" | tr '-' '_')
FIRST_STATE_CHANGE_SAFE=$(echo "$FIRST_STATE_CHANGE" | tr '-' '_')
FIRST_STATE_VIEW_SAFE=$(echo "$FIRST_STATE_VIEW" | tr '-' '_')

# Target directory
TARGET_DIR="$(pwd)/$PROJECT_NAME_SAFE"

if [ -d "$TARGET_DIR" ]; then
    echo -e "${RED}Error: Directory '$TARGET_DIR' already exists${NC}"
    exit 1
fi

echo -e "${GREEN}Creating EvidentSource Python project: $PROJECT_NAME_SAFE${NC}"
echo "  Database: $DATABASE_NAME"
echo "  First State Change: $FIRST_STATE_CHANGE_SAFE"
echo "  First State View: $FIRST_STATE_VIEW_SAFE"
echo ""

# Copy template
cp -r "$TEMPLATE_DIR" "$TARGET_DIR"

# Rename state change directory
if [ -d "$TARGET_DIR/state_changes/{{first_state_change}}" ]; then
    mv "$TARGET_DIR/state_changes/{{first_state_change}}" "$TARGET_DIR/state_changes/$FIRST_STATE_CHANGE_SAFE"
fi

# Rename state view directory
if [ -d "$TARGET_DIR/state_views/{{first_state_view}}" ]; then
    mv "$TARGET_DIR/state_views/{{first_state_view}}" "$TARGET_DIR/state_views/$FIRST_STATE_VIEW_SAFE"
fi

# Replace template variables in all files
find "$TARGET_DIR" -type f \( -name "*.py" -o -name "*.json" -o -name "*.md" -o -name "*.toml" -o -name "*.sh" \) -print0 | while IFS= read -r -d '' file; do
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        sed -i '' \
            -e "s/{{project_name}}/$PROJECT_NAME_SAFE/g" \
            -e "s/{{database_name}}/$DATABASE_NAME/g" \
            -e "s/{{first_state_change}}/$FIRST_STATE_CHANGE_SAFE/g" \
            -e "s/{{first_state_view}}/$FIRST_STATE_VIEW_SAFE/g" \
            "$file"
    else
        # Linux
        sed -i \
            -e "s/{{project_name}}/$PROJECT_NAME_SAFE/g" \
            -e "s/{{database_name}}/$DATABASE_NAME/g" \
            -e "s/{{first_state_change}}/$FIRST_STATE_CHANGE_SAFE/g" \
            -e "s/{{first_state_view}}/$FIRST_STATE_VIEW_SAFE/g" \
            "$file"
    fi
done

# Make scripts executable
chmod +x "$TARGET_DIR/build_all.sh" 2>/dev/null || true
chmod +x "$TARGET_DIR/install.sh" 2>/dev/null || true

echo ""
echo -e "${GREEN}Project created successfully!${NC}"
echo ""
echo "Next steps:"
echo "  cd $PROJECT_NAME_SAFE"
echo "  python3 -m venv .venv"
echo "  source .venv/bin/activate"
echo "  pip install -e ."
echo "  ./build_all.sh        # Build WASM components"
echo "  ./install.sh --list   # List components"
echo "  ./install.sh --all    # Install all components"
