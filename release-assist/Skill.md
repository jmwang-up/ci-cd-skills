---
name: release-assist
description: 当用户想要协助发布项目新版本时使用此技能。包括自动化版本发布、更新版本号、生成变更日志、创建 Git 标签、构建发布包、发布到注册表以及管理整个发布流程。当用户询问"帮我发布版本 X"、"创建发布"、"发布版本"、"自动化发布流程"、需要更新版本和创建标签、生成发布说明、执行发布前检查、发布到 GitHub/Docker/包注册表，或想要发布流程的试运行时使用此技能。
license: MIT
---

# 发布协助指南

## 概述

本指南涵盖了操作系统项目版本发布工作流程的自动化。该技能处理版本号更新、变更日志生成、Git 标签创建、发布包构建、发布到多个目标，并确保整个发布过程的一致性和可靠性。

## 快速开始

```bash
# 发布新版本
python src/release_assist.py v2.1.3

# 试运行以预览操作
python src/release_assist.py v2.1.3 --dry-run

# 预发布版本
python src/release_assist.py v2.1.3-rc1 --pre-release
```

## Basic Release Workflow

### Standard Release

```bash
python src/release_assist.py v2.1.3
```

Output:
```
Release Assistant
=================

Target Version: v2.1.3
Branch: main

[1/9] Validating version... OK
[2/9] Checking workspace... OK
[3/9] Updating version files... OK
[4/9] Generating changelog... OK
[5/9] Committing changes... OK
[6/9] Creating Git tag... OK
[7/9] Building release packages... OK
[8/9] Publishing to targets... OK
[9/9] Sending notifications... OK

Release v2.1.3 completed successfully!

Published to:
- GitHub Releases
- Docker Hub
- Package repositories

Release URL: https://github.com/org/project/releases/tag/v2.1.3
```

### Dry-Run Mode

```bash
python src/release_assist.py v2.1.3 --dry-run
```

Output:
```
Release Assistant (DRY RUN)
===========================

Target Version: v2.1.3
Branch: main

The following actions would be performed:

1. Validate version v2.1.3
   - Check version format: valid
   - Check version uniqueness: no conflicts

2. Check workspace
   - Verify clean working directory
   - Confirm on correct branch (main)

3. Update version files
   - package.json: 2.1.2 → 2.1.3
   - VERSION: 2.1.2 → 2.1.3

4. Generate changelog
   - Analyze commits since v2.1.2
   - Format: CHANGELOG.md

5. Commit changes
   - Message: "Release version v2.1.3"

6. Create Git tag
   - Tag: v2.1.3
   - Message: "Release v2.1.3"

7. Build release packages
   - myos-kernel.img
   - myos-tools.tar.gz

8. Publish to targets
   - GitHub Releases
   - Docker Hub (myos:2.1.3)

9. Send notifications
   - Email team@example.com
   - Slack #releases channel

No changes were made (dry-run mode).
Run without --dry-run to execute.
```

## Pre-Release Versions

### Release Candidate

```bash
python src/release_assist.py v2.1.3-rc1 --pre-release
```

Output:
```
Release Assistant
=================

Target Version: v2.1.3-rc1
Type: Pre-release
Branch: develop

[1/9] Validating version... OK (pre-release format)
[2/9] Checking workspace... OK
[3/9] Updating version files... OK
[4/9] Generating changelog... OK
[5/9] Committing changes... OK
[6/9] Creating Git tag... OK
[7/9] Building release packages... OK
[8/9] Publishing to targets... OK (marked as pre-release)
[9/9] Sending notifications... OK

Pre-release v2.1.3-rc1 completed successfully!

This is a PRE-RELEASE version for testing.
Not recommended for production use.
```

### Beta Release

```bash
python src/release_assist.py v2.2.0-beta.1 --pre-release
```

### Alpha Release

```bash
python src/release_assist.py v3.0.0-alpha.1 --pre-release
```

## Release Targets

### GitHub Releases

```bash
python src/release_assist.py v2.1.3 --target github
```

Output:
```
Publishing to GitHub Releases
==============================

Creating release v2.1.3...
- Title: Release v2.1.3
- Body: Generated from CHANGELOG.md
- Assets:
  ✓ myos-kernel.img (45.2 MB)
  ✓ myos-tools.tar.gz (12.8 MB)
  ✓ checksums.txt (512 bytes)

Release published: https://github.com/org/project/releases/tag/v2.1.3
```

### Docker Hub

```bash
python src/release_assist.py v2.1.3 --target docker
```

Output:
```
Publishing to Docker Hub
========================

Building Docker image...
- Tag: myorg/myos:2.1.3
- Tag: myorg/myos:latest
- Size: 256 MB

Pushing to Docker Hub...
✓ myorg/myos:2.1.3
✓ myorg/myos:latest

Docker image published: https://hub.docker.com/r/myorg/myos
```

### Package Repositories

```bash
python src/release_assist.py v2.1.3 --target packages
```

Output:
```
Publishing to Package Repositories
===================================

Building packages...
✓ myos-2.1.3.deb (Ubuntu/Debian)
✓ myos-2.1.3.rpm (RHEL/CentOS)
✓ myos-2.1.3.tar.gz (Source)

Uploading to repositories...
✓ apt.example.com/pool/main/
✓ yum.example.com/releases/
✓ packages.example.com/source/

Packages published successfully.
```

### Multiple Targets

```bash
python src/release_assist.py v2.1.3 --target github,docker,packages
```

## Selective Steps

### Skip Tests

```bash
python src/release_assist.py v2.1.3 --skip-tests
```

Use this when tests have already been verified or when doing urgent hotfixes.

### Skip Build

```bash
python src/release_assist.py v2.1.3 --skip-build
```

Use this when release packages are already built.

### Custom Branch

```bash
python src/release_assist.py v2.1.3 --branch release/v2.1
```

## Python API Usage

### Basic Release

```python
from release_assist import ReleaseAssist

# Initialize
ra = ReleaseAssist()

# Perform release
result = ra.release(version='v2.1.3')

if result['success']:
    print(f"Released: {result['url']}")
else:
    print(f"Error: {result['error']}")
```

### Dry-Run Release

```python
from release_assist import ReleaseAssist

ra = ReleaseAssist()

# Preview release actions
preview = ra.release(version='v2.1.3', dry_run=True)

print("Actions to be performed:")
for step in preview['steps']:
    print(f"- {step['name']}: {step['description']}")
```

### Custom Configuration

```python
from release_assist import ReleaseAssist

# Initialize with custom config
ra = ReleaseAssist(
    targets=['github', 'docker'],
    branch='main',
    skip_tests=False,
    skip_build=False
)

# Perform release
result = ra.release(version='v2.1.3')
```

### Pre-Release

```python
from release_assist import ReleaseAssist

ra = ReleaseAssist()

# Create pre-release
result = ra.release(
    version='v2.1.3-rc1',
    pre_release=True,
    branch='develop'
)
```

## Changelog Generation

### Automatic Changelog

The skill automatically generates changelogs from Git commit history:

```bash
python src/release_assist.py v2.1.3
```

Generated CHANGELOG.md:
```markdown
# Changelog

## [2.1.3] - 2026-02-04

### Added
- New network stack optimizations
- Enhanced memory management
- Support for new hardware platforms

### Changed
- Updated kernel to version 5.10
- Improved error handling

### Fixed
- Fixed memory leak in network module
- Resolved race condition in scheduler

### Security
- Patched CVE-2026-1234
```

### Custom Changelog

```python
from release_assist import ReleaseAssist

ra = ReleaseAssist()

# Generate with custom sections
changelog = ra.generate_changelog(
    from_version='v2.1.2',
    to_version='v2.1.3',
    sections=['Added', 'Fixed', 'Security']
)
```

## Version Validation

### Version Format Check

The skill validates version numbers according to Semantic Versioning:

Valid formats:
- `v1.2.3`
- `v1.2.3-rc1`
- `v1.2.3-beta.1`
- `v1.2.3-alpha.2`

Invalid formats:
- `1.2` (missing patch)
- `v1.2.3.4` (too many components)
- `version-1.2.3` (invalid prefix)

### Uniqueness Check

```bash
python src/release_assist.py v2.1.3
```

If version already exists:
```
Error: Version v2.1.3 already exists
Existing tag: v2.1.3 (created on 2026-01-15)
Suggestion: Use a different version number or delete the existing tag
```

## Workspace Validation

### Clean Workspace Check

```bash
python src/release_assist.py v2.1.3
```

If uncommitted changes exist:
```
Release Assistant
=================

Target Version: v2.1.3
Branch: main

[1/9] Validating version... OK
[2/9] Checking workspace... FAILED

Error: Uncommitted changes found in workspace

Modified files:
- src/kernel/memory.c
- include/system.h

Please commit or stash your changes before proceeding.
Use --dry-run to see what would be affected.
```

### Branch Verification

Ensures you're on the correct branch:

```bash
python src/release_assist.py v2.1.3 --branch main
```

If on wrong branch:
```
Error: Current branch is 'develop', expected 'main'
Suggestion: Switch to the correct branch with: git checkout main
```

## Rollback Support

### Rollback Last Release

```python
from release_assist import ReleaseAssist

ra = ReleaseAssist()

# Rollback to previous version
result = ra.rollback(version='v2.1.3')

if result['success']:
    print(f"Rolled back to: {result['previous_version']}")
```

### Delete Release Tag

```bash
# Manual rollback
git tag -d v2.1.3
git push origin :refs/tags/v2.1.3
```

## Common Use Cases

### Hotfix Release

```bash
#!/bin/bash
# Quick hotfix release

# Checkout hotfix branch
git checkout -b hotfix/v2.1.4 main

# Make fixes and commit
# ...

# Release hotfix
python src/release_assist.py v2.1.4 \
    --branch hotfix/v2.1.4 \
    --skip-tests

# Merge back to main
git checkout main
git merge hotfix/v2.1.4
```

### Scheduled Release

```bash
#!/bin/bash
# Automated weekly release script

# Get next version
CURRENT=$(git describe --tags --abbrev=0)
NEXT=$(python -c "v='$CURRENT'.split('.'); v[2]=str(int(v[2])+1); print('.'.join(v))")

# Dry-run first
python src/release_assist.py ${NEXT} --dry-run

# Confirm
read -p "Proceed with release ${NEXT}? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    python src/release_assist.py ${NEXT}
fi
```

### Multi-Environment Release

```bash
#!/bin/bash
# Release to staging, then production

VERSION="v2.1.3"

# Stage 1: Staging
echo "Releasing to staging..."
python src/release_assist.py ${VERSION}-staging \
    --target staging \
    --pre-release

# Wait for verification
read -p "Staging verified. Proceed to production? (y/n) " -n 1 -r
echo

if [[ $REPLY =~ ^[Yy]$ ]]; then
    # Stage 2: Production
    echo "Releasing to production..."
    python src/release_assist.py ${VERSION} \
        --target github,docker,packages
fi
```

## Error Handling

### Build Failure

```
Release Assistant
=================

Target Version: v2.1.3
Branch: main

[1/9] Validating version... OK
[2/9] Checking workspace... OK
[3/9] Updating version files... OK
[4/9] Generating changelog... OK
[5/9] Committing changes... OK
[6/9] Creating Git tag... OK
[7/9] Building release packages... FAILED

Error: Build failed with exit code 1
Build output:
  gcc: error: undefined reference to 'missing_function'

Release process aborted.
No tags were pushed. Your workspace is in a clean state.
```

### Publishing Failure

```
Release Assistant
=================

[8/9] Publishing to targets... FAILED

Error: Failed to publish to Docker Hub
Authentication failed: Invalid credentials

Rollback options:
1. Fix credentials and retry: python src/release_assist.py v2.1.3 --target docker
2. Delete tag and start over: git tag -d v2.1.3

Git tag v2.1.3 was created but not pushed.
```

## Quick Reference

| Task | Command | Description |
|------|---------|-------------|
| Standard release | `python src/release_assist.py v2.1.3` | Full release workflow |
| Dry-run | `python src/release_assist.py v2.1.3 --dry-run` | Preview actions without executing |
| Pre-release | `python src/release_assist.py v2.1.3-rc1 --pre-release` | Create pre-release version |
| GitHub only | `python src/release_assist.py v2.1.3 --target github` | Publish to GitHub Releases |
| Docker only | `python src/release_assist.py v2.1.3 --target docker` | Publish to Docker Hub |
| Skip tests | `python src/release_assist.py v2.1.3 --skip-tests` | Skip test step |
| Custom branch | `python src/release_assist.py v2.1.3 --branch release/v2.1` | Release from specific branch |

## Options Summary

| Option | Values | Default | Description |
|--------|--------|---------|-------------|
| `version` | semver | required | Version number to release |
| `--dry-run` | flag | false | Preview actions without executing |
| `--skip-tests` | flag | false | Skip running tests |
| `--skip-build` | flag | false | Skip building packages |
| `--target` | `github`, `docker`, `packages`, `all` | `all` | Where to publish |
| `--branch` | branch name | `main` | Branch to release from |
| `--pre-release` | flag | false | Mark as pre-release version |

## Release Checklist

Before running release-assist, ensure:

- [ ] All tests pass
- [ ] Code is reviewed and merged
- [ ] CHANGELOG is up-to-date (or will be auto-generated)
- [ ] Version number follows semantic versioning
- [ ] Authentication tokens are configured
- [ ] Workspace is clean (no uncommitted changes)
- [ ] On correct branch

## Dependencies

- **Git**: Required for tagging and version control
- **Build tools**: Required for building release packages
- **Python 3.6+**: For running the script
- **Authentication**: Tokens for GitHub/Docker/package registries
- **Network**: For publishing to remote targets