# Rename Documentation Format
**Date: June 30, 2025**
**Type: Process/Standards**

## Overview
Renamed all documentation files to follow the new date-time-filename format: `YYYY-MM-DD-HHMM-description.md`

## Changes Made

### 1. File Renames
Renamed all existing documentation files from old format to new format:

| Old Filename | New Filename |
|-------------|--------------|
| project-restructure-2025-01-30.md | 2025-01-30-1000-project-restructure.md |
| documentation-process.md | 2025-01-30-1015-documentation-process.md |
| running-instructions-2025-01-30.md | 2025-01-30-1030-running-instructions.md |
| component-separation-2025-01-30.md | 2025-01-30-1100-component-separation.md |
| cleanup-unnecessary-files-2025-01-30.md | 2025-01-30-1130-cleanup-unnecessary-files.md |
| installation-guide-2025-01-30.md | 2025-01-30-1200-installation-guide.md |

### 2. Updated References
Updated all references to documentation files in:
- `INDEX.md` - All file links updated
- `README.md` - Installation guide reference updated
- `INSTALL.md` - Installation guide reference updated
- `2025-01-30-1015-documentation-process.md` - Updated examples and guidelines

### 3. New Naming Convention
Format: `YYYY-MM-DD-HHMM-description.md`

**Benefits:**
- **Chronological sorting** - Files naturally sort by creation time
- **Unique identifiers** - Date and time prevent naming conflicts
- **Easy tracking** - Can see when documentation was created at a glance
- **Consistent format** - All files follow the same pattern

**Guidelines:**
- Use 24-hour format for time (e.g., 1430 not 2:30 PM)
- Keep descriptions concise but descriptive
- Use hyphens to separate words in description
- Always use current date/time when creating new documentation

## Examples

```bash
# Creating new documentation
2025-06-30-1415-feature-user-auth.md
2025-06-30-1530-bugfix-memory-leak.md
2025-06-30-1645-refactor-api-endpoints.md
```

## Impact

This change affects:
1. Future documentation creation - Must follow new format
2. Existing links - All have been updated
3. Documentation process - Guidelines updated to reflect new format

## Notes

- The INDEX.md file keeps its name (no date prefix) as it's a special index file
- Time should reflect when the documentation is created, not when the work was done
- This format makes it easier to find recent changes and track project evolution