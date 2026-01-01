#!/bin/bash
# Link Checker Script
# Checks for broken markdown links in backlog files

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Default paths
BACKLOG_DIR="${1:-project-management/backlog}"
BASE_DIR="${2:-.}"

echo "Checking markdown links..."
echo "----------------------------------------"

ERRORS=0
WARNINGS=0

# Find all markdown files
FILES=$(find "$BACKLOG_DIR" -name "*.md" 2>/dev/null || true)

if [ -z "$FILES" ]; then
    echo -e "${YELLOW}⚠ No markdown files found in $BACKLOG_DIR${NC}"
    exit 0
fi

# Function to check if a file exists
check_link() {
    local link="$1"
    local source_file="$2"
    local source_dir=$(dirname "$source_file")
    
    # Remove markdown link syntax
    link=$(echo "$link" | sed 's/.*(\(.*\))/\1/')
    
    # Handle relative paths
    if [[ "$link" == /* ]]; then
        # Absolute path
        target="$BASE_DIR$link"
    else
        # Relative path
        target="$source_dir/$link"
    fi
    
    # Check if file exists
    if [ -f "$target" ]; then
        return 0
    else
        return 1
    fi
}

# Check each file
echo "$FILES" | while read -r file; do
    if [ -z "$file" ]; then
        continue
    fi
    
    echo "Checking: $file"
    
    # Extract markdown links
    LINKS=$(grep -o "\[.*\]([^)]*)" "$file" 2>/dev/null || true)
    
    if [ -z "$LINKS" ]; then
        continue
    fi
    
    # Check each link
    echo "$LINKS" | while read -r link; do
        if [ -z "$link" ]; then
            continue
        fi
        
        # Skip external links (http/https)
        if echo "$link" | grep -q "http"; then
            continue
        fi
        
        # Check if link target exists
        if check_link "$link" "$file"; then
            echo -e "  ${GREEN}✓ $link${NC}"
        else
            echo -e "  ${RED}✗ Broken link: $link (in $file)${NC}"
            ((ERRORS++))
        fi
    done
done

# Summary
echo "----------------------------------------"
if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}✓ Link check passed!${NC}"
    exit 0
else
    echo -e "${RED}✗ Found $ERRORS broken link(s)${NC}"
    exit 1
fi

