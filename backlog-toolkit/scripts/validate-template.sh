#!/bin/bash
# Template Validation Script
# Validates that a backlog item template is complete and properly formatted

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if file is provided
if [ $# -eq 0 ]; then
    echo -e "${RED}Error: No file provided${NC}"
    echo "Usage: $0 <template-file.md>"
    exit 1
fi

FILE="$1"

# Check if file exists
if [ ! -f "$FILE" ]; then
    echo -e "${RED}Error: File not found: $FILE${NC}"
    exit 1
fi

echo "Validating template: $FILE"
echo "----------------------------------------"

ERRORS=0
WARNINGS=0

# Check for required sections in Feature Request
if grep -q "Feature Request" "$FILE"; then
    echo "Checking Feature Request template..."
    
    # Required fields
    REQUIRED_FIELDS=("Status" "Priority" "Story Points" "User Story" "Acceptance Criteria" "Business Value")
    
    for field in "${REQUIRED_FIELDS[@]}"; do
        if ! grep -q "$field" "$FILE"; then
            echo -e "${RED}✗ Missing required field: $field${NC}"
            ((ERRORS++))
        else
            echo -e "${GREEN}✓ Found: $field${NC}"
        fi
    done
    
    # Check for user story format
    if grep -q "As a.*I want.*so that" "$FILE"; then
        echo -e "${GREEN}✓ User story format appears correct${NC}"
    else
        echo -e "${YELLOW}⚠ User story may not follow standard format${NC}"
        ((WARNINGS++))
    fi
    
    # Check for acceptance criteria
    ACCEPTANCE_COUNT=$(grep -c "^- \[ \]" "$FILE" || echo "0")
    if [ "$ACCEPTANCE_COUNT" -ge 3 ]; then
        echo -e "${GREEN}✓ Found $ACCEPTANCE_COUNT acceptance criteria (minimum 3)${NC}"
    else
        echo -e "${YELLOW}⚠ Found only $ACCEPTANCE_COUNT acceptance criteria (recommend at least 3)${NC}"
        ((WARNINGS++))
    fi
fi

# Check for required sections in Bug Fix
if grep -q "Bug Fix" "$FILE"; then
    echo "Checking Bug Fix template..."
    
    # Required fields
    REQUIRED_FIELDS=("Status" "Priority" "Story Points" "Steps to Reproduce" "Expected Behavior" "Actual Behavior" "Environment")
    
    for field in "${REQUIRED_FIELDS[@]}"; do
        if ! grep -q "$field" "$FILE"; then
            echo -e "${RED}✗ Missing required field: $field${NC}"
            ((ERRORS++))
        else
            echo -e "${GREEN}✓ Found: $field${NC}"
        fi
    done
    
    # Check for steps to reproduce
    STEPS_COUNT=$(grep -c "^[0-9]\." "$FILE" || echo "0")
    if [ "$STEPS_COUNT" -ge 3 ]; then
        echo -e "${GREEN}✓ Found $STEPS_COUNT reproduction steps${NC}"
    else
        echo -e "${YELLOW}⚠ Found only $STEPS_COUNT reproduction steps (recommend at least 3)${NC}"
        ((WARNINGS++))
    fi
fi

# Check for markdown links (broken links check)
echo "Checking for markdown links..."
LINK_COUNT=$(grep -o "\[.*\](.*)" "$FILE" | wc -l || echo "0")
if [ "$LINK_COUNT" -gt 0 ]; then
    echo -e "${GREEN}✓ Found $LINK_COUNT markdown links${NC}"
    # Note: Actual link validation would require checking if files exist
    echo -e "${YELLOW}⚠ Manual link validation recommended${NC}"
fi

# Check for placeholder text
PLACEHOLDER_COUNT=$(grep -c "\[.*\]" "$FILE" || echo "0")
if [ "$PLACEHOLDER_COUNT" -gt 5 ]; then
    echo -e "${YELLOW}⚠ Found $PLACEHOLDER_COUNT placeholder brackets - ensure all are filled${NC}"
    ((WARNINGS++))
fi

# Check for status values
if grep -qE "(⭕|⏳|✅)" "$FILE"; then
    echo -e "${GREEN}✓ Status emoji found${NC}"
else
    echo -e "${YELLOW}⚠ No status emoji found${NC}"
    ((WARNINGS++))
fi

# Check for priority levels
if grep -qE "(🔴|🟠|🟡|🟢)" "$FILE"; then
    echo -e "${GREEN}✓ Priority emoji found${NC}"
else
    echo -e "${YELLOW}⚠ No priority emoji found${NC}"
    ((WARNINGS++))
fi

# Summary
echo "----------------------------------------"
if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
    echo -e "${GREEN}✓ Validation passed!${NC}"
    exit 0
elif [ $ERRORS -eq 0 ]; then
    echo -e "${YELLOW}⚠ Validation passed with $WARNINGS warning(s)${NC}"
    exit 0
else
    echo -e "${RED}✗ Validation failed with $ERRORS error(s) and $WARNINGS warning(s)${NC}"
    exit 1
fi

