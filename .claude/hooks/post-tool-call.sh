#!/bin/bash
# Claude Code hook: post-tool-call
# Checks file size limits after Edit/Write operations on Python files

# Exit codes:
# 0 = success (no issues or not applicable)
# 1 = error (hard limit exceeded)
# Note: Warnings are printed but still exit 0

# Read hook input from stdin
INPUT=$(cat)

# Extract tool name and file path from the JSON input
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name // empty')
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

# Only check Edit and Write tool calls
if [[ "$TOOL_NAME" != "Edit" && "$TOOL_NAME" != "Write" ]]; then
    exit 0
fi

# Only check Python files
if [[ ! "$FILE_PATH" =~ \.py$ ]]; then
    exit 0
fi

# Check if file exists
if [[ ! -f "$FILE_PATH" ]]; then
    exit 0
fi

# Count lines in the file
LINE_COUNT=$(wc -l < "$FILE_PATH")

# Define limits
SOFT_LIMIT=300
HARD_LIMIT=500

# Check against limits
if [[ $LINE_COUNT -gt $HARD_LIMIT ]]; then
    echo "ERROR: File '$FILE_PATH' has $LINE_COUNT lines (hard limit: $HARD_LIMIT)"
    echo "ACTION REQUIRED: Split this file into smaller modules"
    exit 1
elif [[ $LINE_COUNT -gt $SOFT_LIMIT ]]; then
    echo "WARNING: File '$FILE_PATH' has $LINE_COUNT lines (soft limit: $SOFT_LIMIT)"
    echo "Consider splitting this file into smaller modules"
    exit 0
fi

exit 0
