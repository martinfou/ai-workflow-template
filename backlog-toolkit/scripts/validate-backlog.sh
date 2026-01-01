#!/bin/bash
# Backlog Validation Script
# Validates backlog structure, file naming, and cross-references

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Default paths (can be overridden)
BACKLOG_DIR="${1:-project-management/backlog}"
FEATURES_DIR="${BACKLOG_DIR}/features"
BUGS_DIR="${BACKLOG_DIR}/bugs"
PRODUCT_BACKLOG="${BACKLOG_DIR}/product-backlog.md"

echo "Validating backlog structure..."
echo "----------------------------------------"

ERRORS=0
WARNINGS=0

# Check if directories exist
if [ ! -d "$BACKLOG_DIR" ]; then
    echo -e "${RED}✗ Backlog directory not found: $BACKLOG_DIR${NC}"
    echo "  Create it with: mkdir -p $BACKLOG_DIR/{features,bugs}"
    ((ERRORS++))
    exit 1
fi

if [ ! -d "$FEATURES_DIR" ]; then
    echo -e "${YELLOW}⚠ Features directory not found: $FEATURES_DIR${NC}"
    ((WARNINGS++))
fi

if [ ! -d "$BUG_FIXES_DIR" ]; then
    echo -e "${YELLOW}⚠ Bug fixes directory not found: $BUG_FIXES_DIR${NC}"
    ((WARNINGS++))
fi

# Check for product backlog file
if [ ! -f "$PRODUCT_BACKLOG" ]; then
    echo -e "${YELLOW}⚠ Product backlog file not found: $PRODUCT_BACKLOG${NC}"
    ((WARNINGS++))
else
    echo -e "${GREEN}✓ Product backlog file found${NC}"
fi

# Validate file naming conventions
echo ""
echo "Checking file naming conventions..."

# Check feature request files
if [ -d "$FEATURES_DIR" ]; then
    FEATURE_FILES=$(find "$FEATURES_DIR" -name "*.md" 2>/dev/null || true)
    FEATURE_COUNT=$(echo "$FEATURE_FILES" | grep -v "^$" | wc -l || echo "0")
    
    if [ "$FEATURE_COUNT" -gt 0 ]; then
        echo -e "${GREEN}✓ Found $FEATURE_COUNT feature request file(s)${NC}"
        
        # Check naming pattern (FR-XXX-*.md)
        INVALID_NAMES=$(echo "$FEATURE_FILES" | grep -v "FR-[0-9]\+-" || true)
        if [ -n "$INVALID_NAMES" ]; then
            echo -e "${YELLOW}⚠ Some feature files don't follow FR-XXX-name.md pattern:${NC}"
            echo "$INVALID_NAMES" | while read -r file; do
                echo "  - $file"
            done
            ((WARNINGS++))
        fi
    else
        echo -e "${YELLOW}⚠ No feature request files found${NC}"
    fi
fi

# Check bug fix files
if [ -d "$BUGS_DIR" ]; then
    BUG_FILES=$(find "$BUGS_DIR" -name "*.md" 2>/dev/null || true)
    BUG_COUNT=$(echo "$BUG_FILES" | grep -v "^$" | wc -l || echo "0")
    
    if [ "$BUG_COUNT" -gt 0 ]; then
        echo -e "${GREEN}✓ Found $BUG_COUNT bug fix file(s)${NC}"
        
        # Check naming pattern (BF-XXX-*.md)
        INVALID_NAMES=$(echo "$BUG_FILES" | grep -v "BF-[0-9]\+-" || true)
        if [ -n "$INVALID_NAMES" ]; then
            echo -e "${YELLOW}⚠ Some bug files don't follow BF-XXX-name.md pattern:${NC}"
            echo "$INVALID_NAMES" | while read -r file; do
                echo "  - $file"
            done
            ((WARNINGS++))
        fi
    else
        echo -e "${YELLOW}⚠ No bug fix files found${NC}"
    fi
fi

# Validate product backlog table
if [ -f "$PRODUCT_BACKLOG" ]; then
    echo ""
    echo "Checking product backlog table..."
    
    # Check for table structure
    if grep -q "| ID |" "$PRODUCT_BACKLOG"; then
        echo -e "${GREEN}✓ Product backlog table structure found${NC}"
    else
        echo -e "${YELLOW}⚠ Product backlog table structure may be missing${NC}"
        ((WARNINGS++))
    fi
    
    # Count entries
    FEATURE_ENTRIES=$(grep -c "\[FR-" "$PRODUCT_BACKLOG" || echo "0")
    BUG_ENTRIES=$(grep -c "\[BF-" "$PRODUCT_BACKLOG" || echo "0")
    
    echo -e "${GREEN}✓ Found $FEATURE_ENTRIES feature request entries${NC}"
    echo -e "${GREEN}✓ Found $BUG_ENTRIES bug fix entries${NC}"
    
    # Check for broken links (basic check)
    echo ""
    echo "Checking for potential broken links..."
    
    # Extract links from product backlog
    LINKS=$(grep -o "\[FR-[0-9]\+\]([^)]*)" "$PRODUCT_BACKLOG" 2>/dev/null || true)
    LINKS="$LINKS $(grep -o "\[BF-[0-9]\+\]([^)]*)" "$PRODUCT_BACKLOG" 2>/dev/null || true)"
    
    if [ -n "$LINKS" ]; then
        LINK_COUNT=$(echo "$LINKS" | wc -w || echo "0")
        echo -e "${GREEN}✓ Found $LINK_COUNT link(s) in product backlog${NC}"
        echo -e "${YELLOW}⚠ Manual link validation recommended${NC}"
    fi
fi

# Summary
echo ""
echo "----------------------------------------"
if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
    echo -e "${GREEN}✓ Backlog validation passed!${NC}"
    exit 0
elif [ $ERRORS -eq 0 ]; then
    echo -e "${YELLOW}⚠ Backlog validation passed with $WARNINGS warning(s)${NC}"
    exit 0
else
    echo -e "${RED}✗ Backlog validation failed with $ERRORS error(s) and $WARNINGS warning(s)${NC}"
    exit 1
fi

