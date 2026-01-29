#!/bin/bash
# Build all state change and state view components

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Create dist directory
mkdir -p dist

echo "Building all components..."
echo ""

# Automatically discover components by listing directories
discover_components() {
    local dir=$1
    local components=()

    if [ -d "$dir" ]; then
        for component_dir in "$dir"/*; do
            if [ -d "$component_dir" ] && [ -f "$component_dir/__init__.py" ]; then
                components+=("$(basename "$component_dir")")
            fi
        done
    fi

    echo "${components[@]}"
}

# Build state changes
echo "Building state changes..."
STATE_CHANGES=($(discover_components "state_changes"))

if [ ${#STATE_CHANGES[@]} -eq 0 ]; then
    echo "  No state changes found"
else
    for CHANGE in "${STATE_CHANGES[@]}"; do
        echo "  - $CHANGE"
        componentize-py \
            -d ./interface/decider.wit \
            -w state-change \
            componentize \
            -o "dist/${CHANGE}.wasm" \
            "state_changes.${CHANGE}"
    done
fi

echo ""

# Build state views
echo "Building state views..."
STATE_VIEWS=($(discover_components "state_views"))

if [ ${#STATE_VIEWS[@]} -eq 0 ]; then
    echo "  No state views found"
else
    for VIEW in "${STATE_VIEWS[@]}"; do
        echo "  - $VIEW"
        componentize-py \
            -d ./interface/decider.wit \
            -w state-view \
            componentize \
            -o "dist/${VIEW}.wasm" \
            "state_views.${VIEW}"
    done
fi

echo ""
echo "All components built successfully!"
echo ""
echo "WASM files are in dist/"
echo ""
echo "To install components to the server, run:"
echo "  ./install.sh --list              # List available components"
echo "  ./install.sh state-change <name> # Install specific state change"
echo "  ./install.sh state-view <name>   # Install specific state view"
