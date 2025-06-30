# Git Workflow Management

## Overview
Git is a distributed version control system that enables effective project version management. This document focuses on leveraging Git branches and merging strategies to define robust development workflows.

## Core Concepts

### Branch Types

Git workflow management revolves around four main branch types:

1. **Main Branch** - The main production branch
2. **Develop Branch** - The development integration branch
3. **Feature Branches** - For new feature development
4. **Hotfix Branches** - For urgent production fixes

**Note**: Modern workflows often skip release branches in favor of tagging releases directly from develop or main.

## Branch Details

### Main Branch
The default branch created when initializing a Git repository. This branch should always contain production-ready code.

```bash
$ git branch
* main
```

Example: Adding initial content to main
```bash
$ touch main1.txt
$ git add main1.txt
$ git commit -m "Add main1.txt"
```

### Develop Branch
The main development branch where all features are integrated. Created from main and serves as the base for feature branches.

```bash
# Create and switch to develop branch
$ git branch develop
$ git checkout develop

# Or create and switch in one command
$ git checkout -b develop
```

Key points:
- Initially identical to main when branched
- Diverges from main as development progresses
- Periodically merged back to main for releases

### Feature Branches
Used for developing new features in isolation. Always branched from and merged back to develop.

```bash
# Create feature branch from develop
$ git checkout develop
$ git checkout -b feature/user-authentication

# After feature completion, merge back
$ git checkout develop
$ git merge feature/user-authentication
```

Naming convention: `feature/descriptive-feature-name`

Benefits:
- Isolates feature development
- Enables parallel development
- Prevents unstable code from affecting main branches

### Release Strategy (Using Tags)
Instead of creating release branches, modern workflows use tags to mark releases directly from develop or main.

```bash
# Option 1: Tag from develop and merge to main
$ git checkout develop
$ git tag -a "v1.0-rc.1" -m "Release candidate 1"
$ git checkout main
$ git merge develop
$ git tag -a "v1.0" -m "Release version 1.0"

# Option 2: Tag directly from develop for deployment
$ git checkout develop
$ git tag -a "v1.0" -m "Release version 1.0"
$ git push origin v1.0
```

Benefits:
- Simpler workflow without extra branches
- Tags are immutable references
- Easier to automate deployments
- Less merge conflicts

### Hotfix Branches
For urgent production fixes. Created from main and merged back to both main and develop.

```bash
# Create hotfix from main
$ git checkout main
$ git checkout -b hotfix/critical-bug-fix

# After fixing
$ git checkout main
$ git merge hotfix/critical-bug-fix
$ git tag -a "v1.0.1" -m "Hotfix version 1.0.1"

# Merge to develop
$ git checkout develop
$ git merge hotfix/critical-bug-fix
```

## Workflow Examples

### Standard Feature Development Flow

Feature development increments the patch version in develop:

```bash
# Current state: develop at v1.0.1_dev
$ git checkout develop
$ git checkout -b feature/payment-integration
# ... implement feature ...
$ git checkout develop
$ git merge feature/payment-integration
$ git tag -a "v1.0.2_dev" -m "Added payment integration"
$ git branch -d feature/payment-integration

# Another feature
$ git checkout -b feature/email-notifications
# ... implement feature ...
$ git checkout develop
$ git merge feature/email-notifications
$ git tag -a "v1.0.3_dev" -m "Added email notifications"
```

**Version progression**: v1.0.1_dev → v1.0.2_dev → v1.0.3_dev

### Release Flow (Tag-Based)

Releases are created by tagging the appropriate commit:

```bash
# Current state: develop at v1.0.3_dev, main at v1.0
$ git checkout develop

# Option 1: Tag and merge to main
$ git tag -a "v1.1" -m "Release version 1.1"
$ git checkout main
$ git merge develop

# Option 2: Merge first, then tag main
$ git checkout main
$ git merge develop
$ git tag -a "v1.1" -m "Release version 1.1"

# Update develop version
$ git checkout develop
$ git tag -a "v1.1_dev" -m "Development continues from v1.1"

# Push tags to remote
$ git push origin v1.1
$ git push origin v1.1_dev
```

### Emergency Fix Flow

Hotfixes update both branches to the same base version:

```bash
# Current state: main at v1.1, develop at v1.1.2_dev
$ git checkout main
$ git checkout -b hotfix/security-patch
# ... fix critical issue ...

# Apply to main
$ git checkout main
$ git merge hotfix/security-patch
$ git tag -a "v1.1.1" -m "Critical security patch"

# Apply to develop (creates matching version)
$ git checkout develop
$ git merge hotfix/security-patch
$ git tag -a "v1.1.1_dev" -m "Security patch applied to develop"

# Note: develop now has the hotfix and continues from v1.1.1_dev
# Next feature would create v1.1.2_dev
```

## Best Practices

### Branch Naming
- **Feature**: `feature/user-login`, `feature/payment-integration`
- **Tags**: `v2.0`, `v2.1.0`, `v2.1.1`
- **Hotfix**: `hotfix/security-patch`, `hotfix/payment-bug`

### Commit Messages
- Use clear, descriptive messages
- Start with a verb: "Add", "Fix", "Update", "Remove"
- Reference issue numbers when applicable

### Merging Strategy
- Use `--no-ff` for feature merges to maintain branch history
- Regularly sync feature branches with develop
- Delete branches after merging

### Team Collaboration
- Protect main and develop branches
- Require pull requests for merges
- Implement code reviews
- Use CI/CD for automated testing

## Semantic Versioning

Git tags should follow Semantic Versioning (SemVer) format: `MAJOR.MINOR.PATCH`

### Version Format: X.Y.Z

- **X (MAJOR)**: Incompatible API changes
- **Y (MINOR)**: New functionality (backwards-compatible)
- **Z (PATCH)**: Bug fixes (backwards-compatible)

### Additional Labels

- **Pre-release**: `v1.0.0-alpha`, `v1.0.0-beta.1`, `v1.0.0-rc.1`
- **Build metadata**: `v1.0.0+build.123`

### Examples

```bash
# Major release (breaking changes)
$ git tag -a "v2.0.0" -m "Major release with breaking API changes"

# Minor release (new features)
$ git tag -a "v1.1.0" -m "Added user authentication feature"

# Patch release (bug fixes)
$ git tag -a "v1.0.1" -m "Fixed login validation bug"

# Pre-release versions
$ git tag -a "v2.0.0-beta.1" -m "Beta release for v2.0.0"
$ git tag -a "v2.0.0-rc.1" -m "Release candidate 1 for v2.0.0"

# With build metadata
$ git tag -a "v1.0.0+build.2023.12.25" -m "Production build"
```

### Version Incrementing Rules

1. **MAJOR version**: When making incompatible API changes
   - Example: Removing endpoints, changing data formats
   - Reset MINOR and PATCH to 0

2. **MINOR version**: When adding functionality in a backwards-compatible manner
   - Example: New features, new endpoints, deprecations
   - Reset PATCH to 0

3. **PATCH version**: When making backwards-compatible bug fixes
   - Example: Security patches, bug fixes, performance improvements

### Branch-Version Relationship

- **Main branch**: Tagged with stable versions (v1.0.0, v1.1.0)
- **Develop branch**: Tagged with development versions (v1.0.0_dev, v1.1.0_dev)
- **Release tags**: Mark stable releases (v1.0.0, v1.1.0)
- **Hotfix branches**: Result in PATCH version increments (v1.0.1)

### Synchronized Versioning Strategy

This workflow uses a synchronized versioning approach between main and develop branches:

1. **Parallel Tracking**: Develop branch maintains versions that mirror main with `_dev` suffix
2. **Feature Increments**: Each feature merged to develop increments the patch version
3. **Release Synchronization**: When releasing, develop resets to the new main version
4. **Hotfix Alignment**: Hotfixes create identical version numbers in both branches

Example progression:
- Main: v0.1 → v0.1.1 → v1.0 → v1.1
- Develop: v0.1_dev → v0.1.1_dev → v0.1.2_dev → v1.0_dev → v1.0.1_dev → v1.1_dev

#### Version Synchronization Rules

1. **Initial Release**: When main releases v0.1, develop starts at v0.1_dev
2. **Feature Integration**: Each feature merged increments the patch version in develop
3. **Release Synchronization**: When releasing to main, develop resets to match the new version
4. **Hotfix Propagation**: Hotfixes create matching versions in both branches

#### Version Flow Example

```
Main:     v0.1 -------- v0.1.1 (hotfix) -------- v1.0 (release) -------- v1.1 (release)
            |              |                         |                       |
Develop:  v0.1_dev -- v0.1.1_dev -- v0.1.2_dev -- v1.0_dev -- v1.0.1_dev -- v1.1_dev -- v1.1.1_dev
                           |            |            |            |            |            |
                      (hotfix)    (feature)    (release)    (feature)    (release)    (feature)
```

#### Practical Examples

```bash
# Initial state: main at v0.1, develop at v0.1_dev

# Hotfix flow: creates v0.1.1 on both branches
$ git checkout main  # at v0.1
$ git checkout -b hotfix/security
# ... fix critical issue ...
$ git checkout main
$ git merge hotfix/security
$ git tag -a "v0.1.1" -m "Security hotfix"
$ git checkout develop
$ git merge hotfix/security
$ git tag -a "v0.1.1_dev" -m "Hotfix synchronized to develop"

# Feature development continues
$ git merge feature/user-auth
$ git tag -a "v0.1.2_dev" -m "User authentication added"

# Release v1.0: tag from develop
$ git checkout develop
$ git tag -a "v1.0" -m "Major release v1.0"
$ git checkout main
$ git merge develop
$ git checkout develop
$ git tag -a "v1.0_dev" -m "Development continues from v1.0"

# More features
$ git merge feature/payment
$ git tag -a "v1.0.1_dev" -m "Payment feature added"
```

This synchronized approach ensures:
- Development progress is clearly tracked
- Release points are well-defined
- Feature integration history is preserved
- Version numbers between branches remain logically connected

### Version Comparison

```bash
# List tags in version order
$ git tag -l --sort=version:refname

# Show specific version pattern
$ git tag -l "v1.*"

# Get latest tag
$ git describe --tags --abbrev=0
```

## Common Commands Reference

```bash
# List all branches
$ git branch -a

# Create new branch
$ git checkout -b <branch-name>

# Switch branches
$ git checkout <branch-name>

# Merge branch
$ git merge <branch-name>

# Delete local branch
$ git branch -d <branch-name>

# Delete remote branch
$ git push origin --delete <branch-name>

# Tag a release
$ git tag -a "v1.0" -m "Version 1.0"

# Push tags
$ git push --tags
```

## Visual Flow Summary

```
Main:       v0.1 -------- v0.1.1 ---------------- v1.0 ---------------- v1.1
              \              /                      |                      |
               \            /                       |                      |
Hotfix:         \-- hotfix -/                       |                      |
                                                    |                      |
Develop:    v0.1_dev -- v0.1.1_dev -- v0.1.2_dev - v1.0_dev -- v1.0.1_dev - v1.1_dev -- v1.1.1_dev
                \           /            /           |            /          |            /
                 \         /            /            |           /           |           /
Feature:          feature_1 --------- /             |          /            feature_1 --/
                                     /              |         /                    
                                    feature_2 ------|---------

Legend:
- Main (red): Production releases with stable version tags
- Develop (blue): Development versions with _dev suffix
- Feature (green/yellow): Feature branches merged into develop
- Hotfix (purple): Emergency fixes merged to both main and develop
```

## Modern Workflow Alternatives

### GitHub Flow
- Only main + feature branches
- Deploy from main using tags
- No develop branch needed

### GitLab Flow
- Main + production branches
- Tags for releases
- Environment branches (optional)

### Trunk-Based Development
- Single main branch
- Very short-lived feature branches
- Continuous integration/deployment

## References
- [GitHub Flow](https://docs.github.com/en/get-started/quickstart/github-flow)
- [GitLab Flow](https://docs.gitlab.com/ee/topics/gitlab_flow.html)
- [Trunk-Based Development](https://trunkbaseddevelopment.com/)
- [Git Workflows and Tutorials | Atlassian](https://www.atlassian.com/git/tutorials/comparing-workflows)
- [Git Documentation](https://git-scm.com/doc)

---
Tags: #git #version-control #devops #workflow #branching
Related: [[Docker Command Reference]]