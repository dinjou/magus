# MAGUS Branching Strategy

## Overview

This project uses a simplified GitFlow branching strategy optimized for solo development while maintaining a stable main branch.

## Branch Structure

```
main (stable, production-ready)
├── develop (integration branch for new features)
    ├── feature/feature-name
    ├── feature/another-feature
    └── release/v2.1.0 (when ready to release)
```

## Branch Purposes

### `main`
- **Purpose**: Stable, production-ready code
- **Rule**: Only merge from `develop` or `release/*` branches
- **Deployment**: This is what users see on the repo page
- **Protection**: Never commit directly to main

### `develop`
- **Purpose**: Integration branch for ongoing development
- **Rule**: Merge feature branches here for testing
- **Workflow**: Features → develop → release → main

### `feature/*`
- **Purpose**: Individual feature development
- **Naming**: `feature/descriptive-name` (e.g., `feature/user-dashboard`)
- **Rule**: Always branch from `develop`
- **Workflow**: develop → feature → develop

### `release/*`
- **Purpose**: Prepare releases from develop
- **Naming**: `release/v2.1.0` or `release/2024.1`
- **Rule**: Only bug fixes and release preparation
- **Workflow**: develop → release → main + develop

## Daily Workflow

### Starting New Work
```bash
# 1. Switch to develop and update
git checkout develop
git pull origin develop

# 2. Create feature branch
git checkout -b feature/your-feature-name

# 3. Work on your feature
# ... make commits ...

# 4. Push feature branch
git push -u origin feature/your-feature-name
```

### Completing a Feature
```bash
# 1. Switch to develop and update
git checkout develop
git pull origin develop

# 2. Merge feature branch
git merge feature/your-feature-name

# 3. Push develop
git push origin develop

# 4. Delete feature branch
git branch -d feature/your-feature-name
git push origin --delete feature/your-feature-name
```

### Creating a Release
```bash
# 1. Create release branch from develop
git checkout develop
git checkout -b release/v2.1.0

# 2. Final testing and bug fixes
# ... make any necessary fixes ...

# 3. Merge to main
git checkout main
git merge release/v2.1.0
git tag v2.1.0
git push origin main --tags

# 4. Merge back to develop
git checkout develop
git merge release/v2.1.0
git push origin develop

# 5. Delete release branch
git branch -d release/v2.1.0
git push origin --delete release/v2.1.0
```

## Benefits

- **Stable Main**: Users always see working code
- **Feature Isolation**: Work on features without breaking main
- **Release Control**: Prepare releases without disrupting development
- **Rollback Safety**: Easy to revert problematic releases
- **CI/CD Ready**: Can set up automated testing on develop

## Quick Reference

| Action | Command |
|--------|---------|
| Start feature | `git checkout develop && git checkout -b feature/name` |
| Finish feature | `git checkout develop && git merge feature/name` |
| Start release | `git checkout develop && git checkout -b release/v2.1.0` |
| Deploy release | `git checkout main && git merge release/v2.1.0` |
| Hotfix | `git checkout main && git checkout -b hotfix/issue` |

## Best Practices

1. **Always branch from develop** for new features
2. **Test thoroughly** before merging to develop
3. **Keep commits atomic** and well-described
4. **Use conventional commit messages** (feat:, fix:, docs:, etc.)
5. **Delete merged branches** to keep repo clean
6. **Tag releases** for easy reference
7. **Never force push** to main or develop