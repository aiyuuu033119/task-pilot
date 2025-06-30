# Git Commands Reference from .claude/commands

Based on the `.claude/commands` folder, here are the git commands you can use for feature, develop, and main branches:

## Feature Branch Commands

```bash
# Start new feature
git-feature-start.md      # Creates feature/name from develop

# Update feature with develop
git-feature-update.md     # Rebases or merges latest develop

# Complete feature
git-feature-finish.md     # Merges to develop, creates PR

# Tag feature
git-feature-tag.md        # Tags completed feature
```

## Develop Branch Commands

```bash
# Version management
git-version-dev-tag.md    # Tags like v1.0.1_dev

# Sync with remote
git-branch-sync.md        # Syncs develop with origin

# Workflow status
git-workflow-status.md    # Shows develop branch state
```

## Main Branch Commands

```bash
# Release from develop
git-merge-no-ff.md        # Merge develop → main preserving history

# Version tagging
git-version-tag.md        # Creates release tags (v1.0.0)

# Hotfix workflow
git-hotfix-start.md       # Creates hotfix from main
git-hotfix-finish.md      # Merges to main & develop
git-hotfix-emergency.md   # Emergency production fixes
```

## General Branch Commands

```bash
# Branch management
git-branch-list.md        # List all branches
git-branch-delete.md      # Delete branches safely
git-branch-rename.md      # Rename branches
git-branch-protect.md     # Set protection rules

# Workflow
git-workflow-init.md      # Initialize main + develop
git-workflow-sync.md      # Sync all workflow branches

# Merging
git-merge-resolve.md      # Resolve conflicts
git-merge-squash.md       # Squash merge commits

# Version increment
git-version-increment.md  # Bump version numbers
```

## Usage Example

```bash
# Feature development flow
.claude/commands/git-feature-start.md new-login
.claude/commands/git-feature-update.md
.claude/commands/git-feature-finish.md

# Release flow
.claude/commands/git-version-tag.md v1.2.0
.claude/commands/git-merge-no-ff.md develop main

# Hotfix flow
.claude/commands/git-hotfix-start.md security-fix
.claude/commands/git-hotfix-finish.md
```

All commands include safety checks, validation, and follow the synchronized versioning strategy outlined in the Git Workflow Management document.

## Available Files in .claude/commands

### Main Workflow Documentation
- **`Git Workflow Management.md`** - Comprehensive guide covering the entire git workflow including:
  - Branch types (main, develop, feature, hotfix)
  - Version management and tagging strategies
  - Workflow examples and best practices
  - Visual flow diagrams

### Feature Branch Commands
- **`git-feature-start.md`** - Creates a new feature branch from develop
- **`git-feature-finish.md`** - Completes feature development and creates a pull request
- **`git-feature-update.md`** - Updates feature branch with latest develop changes
- **`git-feature-tag.md`** - Tags completed features

### Branch Management Commands
- **`git-branch-sync.md`** - Syncs local branch with remote upstream
- **`git-branch-list.md`** - Lists all branches
- **`git-branch-delete.md`** - Deletes branches safely
- **`git-branch-rename.md`** - Renames branches
- **`git-branch-protect.md`** - Sets branch protection

### Workflow Commands
- **`git-workflow-init.md`** - Initializes repository with main and develop branches
- **`git-workflow-status.md`** - Shows workflow status
- **`git-workflow-sync.md`** - Syncs all workflow branches

### Hotfix Commands
- **`git-hotfix-start.md`** - Creates hotfix branch from main/master
- **`git-hotfix-finish.md`** - Completes hotfix and merges to both main and develop
- **`git-hotfix-emergency.md`** - Emergency hotfix procedures

### Merge Commands
- **`git-merge-no-ff.md`** - Merges with --no-ff to preserve branch history
- **`git-merge-squash.md`** - Squash merges for cleaner history
- **`git-merge-resolve.md`** - Helps resolve merge conflicts

### Version Management
- **`git-version-tag.md`** - Creates version tags
- **`git-version-increment.md`** - Increments version numbers
- **`git-version-dev-tag.md`** - Tags development versions

The workflow follows a git-flow model with:
- **main** branch for production code
- **develop** branch for integration
- **feature/** branches for new features (branched from develop)
- **hotfix/** branches for urgent fixes (branched from main)

All commands use consistent naming conventions and include detailed error handling, validation steps, and safety notes.