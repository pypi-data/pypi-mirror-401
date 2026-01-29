#!/bin/bash
# Installation script for state changes and state views
#
# Usage:
#   ./install.sh --list                          # List available components
#   ./install.sh state-change <name>             # Install specific state change
#   ./install.sh state-view <name>               # Install specific state view
#   ./install.sh state-change <n1> state-view <n2>  # Install multiple
#   ./install.sh --all-state-changes             # Install all state changes (with confirmation)
#   ./install.sh --all-state-views               # Install all state views (with confirmation)
#   ./install.sh --all                           # Install everything (with confirmation)

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Configuration
BASE_URL="${EVIDENTSOURCE_URL:-http://localhost:3000}"
DATABASE="${EVIDENTSOURCE_DATABASE:-{{database_name}}}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Automatically discover available components by listing directories
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

# Discover state changes and state views from directories
AVAILABLE_STATE_CHANGES=($(discover_components "state_changes"))
AVAILABLE_STATE_VIEWS=($(discover_components "state_views"))

# Function to list available components
list_components() {
    echo "Available components:"
    echo ""
    echo "State Changes:"
    for sc in "${AVAILABLE_STATE_CHANGES[@]}"; do
        echo "  - $sc"
    done
    echo ""
    echo "State Views:"
    for sv in "${AVAILABLE_STATE_VIEWS[@]}"; do
        echo "  - $sv"
    done
    echo ""
    echo "Usage examples:"
    echo "  ./install.sh state-change {{first_state_change}}"
    echo "  ./install.sh state-view {{first_state_view}}"
    echo "  ./install.sh state-change {{first_state_change}} state-view {{first_state_view}}"
}

# Function to check if WASM file exists
check_wasm_file() {
    local name=$1
    local wasm_file="dist/${name}.wasm"

    if [ ! -f "$wasm_file" ]; then
        echo -e "${RED}Error: $wasm_file not found${NC}"
        echo "Run ./build_all.sh first"
        return 1
    fi
    echo "$wasm_file"
}

# Function to check if metadata.json exists
check_metadata_file() {
    local type=$1
    local name=$2
    local metadata_file

    if [ "$type" = "state-change" ]; then
        metadata_file="state_changes/${name}/metadata.json"
    else
        metadata_file="state_views/${name}/metadata.json"
    fi

    if [ ! -f "$metadata_file" ]; then
        echo -e "${RED}Error: $metadata_file not found${NC}"
        return 1
    fi
    echo "$metadata_file"
}

# Function to upload a state change
upload_state_change() {
    local name=$1

    echo -en "  Uploading state change ${GREEN}$name${NC}... "

    local wasm_file metadata_file
    wasm_file=$(check_wasm_file "$name") || return 1
    metadata_file=$(check_metadata_file "state-change" "$name") || return 1

    local response
    response=$(curl -s -w "\n%{http_code}" -X POST "${BASE_URL}/api/v1/db/${DATABASE}/state-changes" \
         -F "metadata=<${metadata_file};type=application/json" \
         -F "wasm=@${wasm_file};type=application/wasm")

    local http_code=$(echo "$response" | tail -n1)
    if [ "$http_code" = "200" ] || [ "$http_code" = "201" ] || [ "$http_code" = "303" ]; then
        echo -e "${GREEN}ok${NC}"
    else
        echo -e "${RED}error (HTTP $http_code)${NC}"
        local response_body=$(echo "$response" | sed '$d')
        echo "Response: $response_body"
        return 1
    fi
}

# Function to upload a state view
upload_state_view() {
    local name=$1

    echo -en "  Uploading state view ${GREEN}$name${NC}... "

    local wasm_file metadata_file
    wasm_file=$(check_wasm_file "$name") || return 1
    metadata_file=$(check_metadata_file "state-view" "$name") || return 1

    local response
    response=$(curl -s -w "\n%{http_code}" -X POST "${BASE_URL}/api/v1/db/${DATABASE}/state-views" \
         -F "metadata=<${metadata_file};type=application/json" \
         -F "wasm=@${wasm_file};type=application/wasm")

    local http_code=$(echo "$response" | tail -n1)
    if [ "$http_code" = "200" ] || [ "$http_code" = "201" ] || [ "$http_code" = "303" ]; then
        echo -e "${GREEN}ok${NC}"
    else
        echo -e "${RED}error (HTTP $http_code)${NC}"
        local response_body=$(echo "$response" | sed '$d')
        echo "Response: $response_body"
        return 1
    fi
}

# Function to confirm action
confirm() {
    local prompt=$1
    echo -en "${YELLOW}$prompt [y/N]${NC} "
    read -r response
    case "$response" in
        [yY][eE][sS]|[yY])
            return 0
            ;;
        *)
            return 1
            ;;
    esac
}

# Main script logic
if [ $# -eq 0 ]; then
    echo "Error: No arguments provided"
    echo ""
    list_components
    exit 1
fi

echo "Installing to: $BASE_URL/api/v1/db/$DATABASE"
echo ""

# Parse arguments
while [ $# -gt 0 ]; do
    case "$1" in
        --list)
            list_components
            exit 0
            ;;
        --all)
            if confirm "Install ALL components (state changes AND state views)?"; then
                echo ""
                for sc in "${AVAILABLE_STATE_CHANGES[@]}"; do
                    upload_state_change "$sc"
                done
                for sv in "${AVAILABLE_STATE_VIEWS[@]}"; do
                    upload_state_view "$sv"
                done
            else
                echo "Installation cancelled"
                exit 0
            fi
            shift
            ;;
        --all-state-changes)
            if confirm "Install all state changes?"; then
                echo ""
                for sc in "${AVAILABLE_STATE_CHANGES[@]}"; do
                    upload_state_change "$sc"
                done
            else
                echo "Installation cancelled"
                exit 0
            fi
            shift
            ;;
        --all-state-views)
            if confirm "Install all state views?"; then
                echo ""
                for sv in "${AVAILABLE_STATE_VIEWS[@]}"; do
                    upload_state_view "$sv"
                done
            else
                echo "Installation cancelled"
                exit 0
            fi
            shift
            ;;
        state-change)
            if [ -z "$2" ]; then
                echo -e "${RED}Error: state-change requires a component name${NC}"
                exit 1
            fi
            upload_state_change "$2"
            shift 2
            ;;
        state-view)
            if [ -z "$2" ]; then
                echo -e "${RED}Error: state-view requires a component name${NC}"
                exit 1
            fi
            upload_state_view "$2"
            shift 2
            ;;
        *)
            echo -e "${RED}Error: Unknown argument: $1${NC}"
            echo ""
            list_components
            exit 1
            ;;
    esac
done

echo ""
echo -e "${GREEN}Installation complete!${NC}"
