---
name: version-query
description: 当用户想要查询或检查项目的版本信息时使用此技能。包括从 package.json、VERSION 文件、Git 标签或提交元数据中获取版本号。当用户询问"这是什么版本？"、"检查版本"、"获取版本信息"，需要验证当前版本号，或想要包含构建元数据（如提交哈希和时间戳）时使用此技能。
license: MIT
---

# 版本查询指南

## 概述

本指南介绍如何从操作系统项目中查询和获取版本信息，支持多种来源包括配置文件、Git 标签和构建元数据。该技能支持多种输出格式，并可自动聚合来自不同来源的版本数据。

## 快速开始

```python
# 从自动检测的来源查询版本
python src/version_query.py

# 从指定来源查询并以 JSON 格式输出
python src/version_query.py --source git --format json

# 包含元数据（提交哈希和时间戳）
python src/version_query.py --include-metadata
```

## 版本来源

### 配置文件 (package.json, VERSION)

```bash
# 从配置文件查询
python src/version_query.py --source config

# 输出：
# Version: 1.2.3
# Source: package.json
```

### Git 标签和提交

```bash
# 从 Git 仓库查询
python src/version_query.py --source git

# 输出：
# Version: 1.2.3
# Source: git tag v1.2.3
# Commit: a1b2c3d
```

### 自动检测

```bash
# 先尝试配置文件，再回退到 Git
python src/version_query.py --source auto

# 当未指定来源时，这是默认行为
python src/version_query.py
```

## 输出格式

### 文本格式（默认）

```bash
python src/version_query.py --format text
```

输出：
```
项目版本信息
===========================

版本: 1.2.3
来源: package.json
最后更新: 2026-02-04 10:30:00 UTC
```

### JSON 格式

```bash
python src/version_query.py --format json
```

输出：
```json
{
  "version": "1.2.3",
  "source": "package.json",
  "timestamp": "2026-02-04T10:30:00Z"
}
```

### 简短格式（仅版本号）

```bash
python src/version_query.py --format short
```

输出：
```
1.2.3
```

## 包含元数据

### 构建元数据

```bash
python src/version_query.py --include-metadata
```

输出：
```
项目版本信息
===========================

版本: 1.2.3
来源: git tag v1.2.3
提交哈希: a1b2c3d4e5f6789
构建时间戳: 2026-02-04 10:30:00 UTC
```

### 带元数据的 JSON

```bash
python src/version_query.py --format json --include-metadata
```

输出：
```json
{
  "version": "1.2.3",
  "source": "git",
  "metadata": {
    "commit": "a1b2c3d4e5f6789",
    "timestamp": "2026-02-04T10:30:00Z",
    "branch": "main",
    "tag": "v1.2.3"
  }
}
```

## Python API 使用

### 基础用法

```python
from version_query import VersionQuery

# 初始化
vq = VersionQuery()

# 从自动来源获取版本
version = vq.get_version()
print(f"版本: {version}")

# 从指定来源获取版本
version = vq.get_version(source='git')
print(f"Git 版本: {version}")
```

### 高级用法

```python
from version_query import VersionQuery

# 获取包含元数据的完整版本信息
vq = VersionQuery()
info = vq.get_version_info(include_metadata=True)

print(f"版本: {info['version']}")
print(f"提交: {info['metadata']['commit']}")
print(f"时间戳: {info['metadata']['timestamp']}")
```

### 自定义配置

```python
from version_query import VersionQuery

# 指定自定义配置文件路径
vq = VersionQuery(
    config_files=['VERSION', 'package.json', 'setup.py']
)

version = vq.get_version(source='config')
```

## 常见使用场景

### CI/CD 流水线集成

```bash
#!/bin/bash
# 获取版本用于构建标签
VERSION=$(python src/version_query.py --format short)
docker build -t myapp:${VERSION} .
```

### 发布脚本

```bash
#!/bin/bash
# 发布前验证版本
CURRENT_VERSION=$(python src/version_query.py --format short --source git)
echo "正在发布版本: ${CURRENT_VERSION}"

# 在发布说明中包含构建元数据
python src/version_query.py --format json --include-metadata > release-info.json
```

### 版本验证

```bash
#!/bin/bash
# 比较配置版本和 Git 标签
CONFIG_VERSION=$(python src/version_query.py --source config --format short)
GIT_VERSION=$(python src/version_query.py --source git --format short)

if [ "$CONFIG_VERSION" != "$GIT_VERSION" ]; then
    echo "警告: 版本不匹配!"
    echo "配置: $CONFIG_VERSION"
    echo "Git: $GIT_VERSION"
    exit 1
fi
```

## 支持的版本文件格式

### package.json (Node.js)

```json
{
  "name": "my-project",
  "version": "1.2.3"
}
```

### VERSION 文件

```
1.2.3
```

### setup.py (Python)

```python
setup(
    name='my-project',
    version='1.2.3',
)
```

### Cargo.toml (Rust)

```toml
[package]
name = "my-project"
version = "1.2.3"
```

## 错误处理

### 未找到版本

```bash
python src/version_query.py --source config
```

错误输出：
```
错误: 在配置文件中未找到版本
已搜索: package.json, VERSION, setup.py
建议: 尝试 --source git 或创建 VERSION 文件
```

### 无效的 Git 仓库

```bash
python src/version_query.py --source git
```

错误输出：
```
错误: 不是 git 仓库
当前目录: /path/to/project
建议: 初始化 git 或使用 --source config
```

## 快速参考

| 任务 | 命令 | 输出 |
|------|------|------|
| 获取版本（自动） | `python src/version_query.py` | 文本格式，自动检测来源 |
| 从配置获取版本 | `python src/version_query.py --source config` | 来自 package.json/VERSION 的版本 |
| 从 Git 获取版本 | `python src/version_query.py --source git` | 来自 Git 标签的版本 |
| JSON 输出 | `python src/version_query.py --format json` | JSON 格式输出 |
| 简短输出（仅版本号） | `python src/version_query.py --format short` | 仅显示版本号 |
| 包含元数据 | `python src/version_query.py --include-metadata` | 包含提交哈希和时间戳 |
| 用于 CI/CD 脚本 | `python src/version_query.py --format short` | 仅机器可读版本号 |

## 选项总结

| 选项 | 可选值 | 默认值 | 说明 |
|------|--------|--------|------|
| `--source` | `config`, `git`, `auto` | `auto` | 从哪里查询版本 |
| `--format` | `json`, `text`, `short` | `text` | 输出格式 |
| `--include-metadata` | 标志 | false | 包含提交哈希和构建时间戳 |

## 依赖项

- **Git**: `--source git` 选项需要
- **Python 3.6+**: 运行脚本需要
- **项目结构**: 必须在配置文件或 Git 标签中有版本信息