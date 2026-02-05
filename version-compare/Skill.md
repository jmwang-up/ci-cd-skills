---
name: version-compare
description: 当用户想要比较项目两个版本之间的差异时使用此技能。包括比较配置更改、依赖更新、源代码修改、Git 提交、分支或标签。当用户询问"版本之间有什么变化？"、"比较 v1 和 v2"、"显示差异"、需要评估升级影响、在部署前审查更改，或生成任意两个版本标识符（标签、分支、提交哈希）之间的比较报告时使用此技能。
license: MIT
---

# 版本比较指南

## 概述

本指南涵盖了操作系统项目两个版本之间的差异比较。该技能分析配置更改、依赖更新和源代码修改，生成详细的比较报告，帮助开发人员和运维人员了解版本升级的影响。

## 快速开始

```bash
# 比较两个 Git 标签
python src/version_compare.py v1.0.0 v2.0.0

# 使用 JSON 输出格式比较
python src/version_compare.py v1.0.0 v2.0.0 --format json

# 仅比较特定部分
python src/version_compare.py v1.0.0 v2.0.0 --sections config,dependencies
```

## 基本比较

### 比较 Git 标签

```bash
python src/version_compare.py v1.0.0 v2.0.0
```

输出：
```
版本比较报告
=========================

比较 v1.0.0 → v2.0.0

配置更改：
- 版本从 1.0.0 更新到 2.0.0
- 新增配置选项 'enable_new_feature'

依赖更改：
- 内核依赖从 5.4 更新到 5.10
- 新增依赖：libssl 1.1.1

代码更改：
- 24 个文件已更改，456 行插入(+)，123 行删除(-)
```

### 比较分支

```bash
python src/version_compare.py main develop
```

输出：
```
版本比较报告
=========================

比较 main → develop

代码更改：
- 12 个文件已更改，234 行插入(+)，56 行删除(-)
- develop 分支中的新功能：
  * 增强的日志系统
  * 性能优化
```

### 比较提交哈希

```bash
python src/version_compare.py a1b2c3d e4f5g6h
```

## 输出格式

### 文本格式（默认）

```bash
python src/version_compare.py v1.0.0 v2.0.0 --format text
```

### JSON 格式

```bash
python src/version_compare.py v1.0.0 v2.0.0 --format json
```

输出：
```json
{
  "versions": {
    "from": "v1.0.0",
    "to": "v2.0.0"
  },
  "changes": {
    "configuration": [
      {
        "type": "modified",
        "item": "version",
        "from": "1.0.0",
        "to": "2.0.0"
      },
      {
        "type": "added",
        "item": "enable_new_feature",
        "value": true
      }
    ],
    "dependencies": [
      {
        "type": "updated",
        "dependency": "kernel",
        "from": "5.4",
        "to": "5.10"
      },
      {
        "type": "added",
        "dependency": "libssl",
        "version": "1.1.1"
      }
    ],
    "code": {
      "summary": "24 个文件已更改，456 行插入(+)，123 行删除(-)",
      "files_changed": 24,
      "insertions": 456,
      "deletions": 123
    }
  }
}
```

### HTML 格式

```bash
python src/version_compare.py v1.0.0 v2.0.0 --format html --output-file report.html
```

## 比较部分

### 仅配置更改

```bash
python src/version_compare.py v1.0.0 v2.0.0 --sections config
```

输出：
```
配置更改：
- 版本从 1.0.0 更新到 2.0.0
- 新增配置选项 'enable_new_feature'
- 配置选项 'debug_mode' 从 true 更改为 false
```

### 仅依赖更改

```bash
python src/version_compare.py v1.0.0 v2.0.0 --sections dependencies
```

输出：
```
依赖更改：
- 内核依赖从 5.4 更新到 5.10
- 新增依赖：libssl 1.1.1
- 移除依赖：legacy-lib 0.9
```

### 仅代码更改

```bash
python src/version_compare.py v1.0.0 v2.0.0 --sections code
```

输出：
```
代码更改：
- 24 个文件已更改，456 行插入(+)，123 行删除(-)
- 修改的文件：
  * src/kernel/memory.c
  * src/network/tcp.c
  * include/system.h
```

### 所有部分

```bash
python src/version_compare.py v1.0.0 v2.0.0 --sections all
```

## Python API 使用

### 基本比较

```python
from version_compare import VersionCompare

# 初始化
vc = VersionCompare()

# 比较两个版本
result = vc.compare('v1.0.0', 'v2.0.0')

print(f"文件更改数: {result['code']['files_changed']}")
print(f"配置更改数: {len(result['configuration'])}")
```

### 高级比较

```python
from version_compare import VersionCompare

# 比较特定部分
vc = VersionCompare()
result = vc.compare(
    'v1.0.0',
    'v2.0.0',
    sections=['config', 'dependencies']
)

# 访问配置更改
for change in result['configuration']:
    print(f"{change['item']}: {change['from']} → {change['to']}")

# 访问依赖更改
for dep in result['dependencies']:
    print(f"{dep['dependency']}: {dep['type']}")
```

### 生成报告

```python
from version_compare import VersionCompare

vc = VersionCompare()

# 生成并保存报告
report = vc.generate_report(
    'v1.0.0',
    'v2.0.0',
    format='html',
    output_file='comparison_report.html'
)
```

## 常见用例

### 部署前验证

```bash
#!/bin/bash
# 比较生产版本与预发布版本
PROD_VERSION=$(git describe --tags --abbrev=0)
STAGING_VERSION="develop"

python src/version_compare.py ${PROD_VERSION} ${STAGING_VERSION} \
    --format json \
    --output-file deployment-changes.json

# 审查破坏性更改
cat deployment-changes.json | jq '.changes.code.details.breaking'
```

### 发布说明生成

```bash
#!/bin/bash
# 从版本比较生成发布说明
PREV_VERSION="v1.2.0"
NEW_VERSION="v1.3.0"

python src/version_compare.py ${PREV_VERSION} ${NEW_VERSION} \
    --format text \
    --output-file RELEASE_NOTES_${NEW_VERSION}.txt
```

### CI/CD 集成

```bash
#!/bin/bash
# 比较 PR 分支与主分支
BASE_BRANCH="main"
PR_BRANCH=$(git rev-parse --abbrev-ref HEAD)

python src/version_compare.py ${BASE_BRANCH} ${PR_BRANCH} \
    --sections code \
    --format json > pr-changes.json

# 如果更改太多则失败
CHANGES=$(cat pr-changes.json | jq '.changes.code.files_changed')
if [ "$CHANGES" -gt 50 ]; then
    echo "错误：更改的文件过多 ($CHANGES > 50)"
    exit 1
fi
```

### 依赖审计

```bash
#!/bin/bash
# 检查版本之间的依赖更新
python src/version_compare.py v2.0.0 v2.1.0 \
    --sections dependencies \
    --format json | jq '.changes.dependencies[] | select(.type=="updated")'
```

## Detailed Change Analysis

### Breaking Changes Detection

```python
from version_compare import VersionCompare

vc = VersionCompare()
result = vc.compare('v1.0.0', 'v2.0.0')

# Check for breaking changes
if 'breaking' in result['code']['details']:
    print("Warning: Breaking changes detected!")
    for change in result['code']['details']['breaking']:
        print(f"  - {change}")
```

### File-Level Diff

```bash
# Get detailed file changes
python src/version_compare.py v1.0.0 v2.0.0 --sections code --verbose
```

Output:
```
Code Changes:

Modified Files:
  src/kernel/memory.c
    - 45 insertions(+), 12 deletions(-)
    - Functions modified: allocate_memory, free_memory

  src/network/tcp.c
    - 120 insertions(+), 34 deletions(-)
    - New function: tcp_optimize_window
    - Modified function: tcp_send_packet

Added Files:
  src/utils/cache.c (234 lines)
  include/cache.h (45 lines)

Deleted Files:
  src/legacy/old_memory.c
```

## Error Handling

### Invalid Version Identifier

```bash
python src/version_compare.py invalid-tag v2.0.0
```

Error output:
```
Error: Version identifier 'invalid-tag' not found
Available tags: v1.0.0, v1.1.0, v2.0.0
Suggestion: Use 'git tag' to list available tags
```

### Missing Git Repository

```bash
python src/version_compare.py v1.0.0 v2.0.0
```

Error output:
```
Error: Not a git repository
Current directory: /path/to/project
Suggestion: Run this command inside a git repository
```

### Permission Issues

```bash
python src/version_compare.py v1.0.0 v2.0.0
```

Error output:
```
Error: Permission denied reading config file
File: /etc/system/config.json
Suggestion: Run with appropriate permissions or check file ownership
```

## Quick Reference

| Task | Command | Output |
|------|---------|--------|
| Compare tags | `python src/version_compare.py v1.0.0 v2.0.0` | Full comparison report |
| Compare branches | `python src/version_compare.py main develop` | Branch differences |
| JSON output | `python src/version_compare.py v1.0.0 v2.0.0 --format json` | Machine-readable JSON |
| Config only | `python src/version_compare.py v1.0.0 v2.0.0 --sections config` | Configuration changes |
| Dependencies only | `python src/version_compare.py v1.0.0 v2.0.0 --sections dependencies` | Dependency updates |
| Code only | `python src/version_compare.py v1.0.0 v2.0.0 --sections code` | Source code changes |
| Save to file | `python src/version_compare.py v1.0.0 v2.0.0 --output-file report.txt` | Save report to file |
| HTML report | `python src/version_compare.py v1.0.0 v2.0.0 --format html` | HTML formatted report |

## Options Summary

| Option | Values | Default | Description |
|--------|--------|---------|-------------|
| `version1` | tag/branch/commit | required | First version to compare |
| `version2` | tag/branch/commit | required | Second version to compare |
| `--format` | `text`, `json`, `html` | `text` | Output format |
| `--sections` | `config`, `dependencies`, `code`, `all` | `all` | Sections to compare |
| `--output-file` | file path | stdout | Save output to file |
| `--verbose` | flag | false | Include detailed file-level changes |

## Dependencies

- **Git**: Required for version comparison
- **Python 3.6+**: For running the script
- **Git repository**: Must be run inside a Git repository
- **Read permissions**: For accessing configuration and source files