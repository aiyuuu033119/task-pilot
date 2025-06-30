#!/bin/bash

# Documentation Creation Script
# Creates a new documentation file with current date and time

if [ $# -eq 0 ]; then
    echo "Usage: ./create-doc.sh <description>"
    echo "Example: ./create-doc.sh feature-user-auth"
    exit 1
fi

# Get current date and time
DATE=$(date '+%Y-%m-%d')
TIME=$(date '+%H%M')
DESCRIPTION=$1

# Create filename
FILENAME="${DATE}-${TIME}-${DESCRIPTION}.md"

# Create file with template
cat > "$FILENAME" << EOF
# ${DESCRIPTION}
**Date: $(date '+%B %d, %Y')**
**Type: [Feature/Bugfix/Refactor/Configuration/Other]**

## Overview
[Brief description of what was accomplished]

## Changes Made

### 1. [Category of changes]
- [Specific change 1]
- [Specific change 2]

## Files Modified
- \`path/to/file1\` - [What was changed]
- \`path/to/file2\` - [What was changed]

## Notes
- [Any important considerations]
EOF

echo "Created documentation file: $FILENAME"
echo "Please edit the file to fill in the details."