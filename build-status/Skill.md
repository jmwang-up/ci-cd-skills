---
name: build-status
description: 当用户想要检查项目的 CI/CD 构建状态时使用此技能。包括查询当前构建状态、查看构建历史、检查构建日志、监控 CI 流水线，或验证构建是否通过或失败。当用户询问"构建状态如何？"、"构建通过了吗？"、"检查 CI 状态"、"监控构建"、需要验证 PR 检查、确认部署就绪，或想要实时构建监控时使用此技能。支持 GitHub Actions、GitLab CI、Jenkins 和其他 CI 系统。
license: MIT
---

# 构建状态检查指南

## 概述

本指南涵盖了跨多种 CI 系统（包括 GitHub Actions、GitLab CI 和 Jenkins）检查操作系统项目的 CI 构建状态。该技能提供当前状态、详细构建信息、历史趋势和实时监控功能。

## 快速开始

```bash
# 检查当前分支的构建状态
python src/build_status.py

# 通过 ID 检查特定构建
python src/build_status.py 12345

# 实时监控构建
python src/build_status.py --watch
```

## 基本状态检查

### 检查当前分支

```bash
python src/build_status.py
```

输出:
```
构建状态报告
===================

项目: MyOS
分支: main

当前构建:
- 状态: 成功 ✓
- 触发者: john.doe
- 开始时间: 2026-02-04 10:15:30 UTC
- 持续时间: 15m 23s
- 提交: a1b2c3d4e5f6 "Add network stack improvements"
```

### 检查特定构建

```bash
python src/build_status.py 12345
```

输出:
```
构建状态报告
===================

构建 ID: 12345
状态: 成功 ✓

详情:
- 分支: main
- 提交: a1b2c3d4e5f6
- 触发者: john.doe
- 开始时间: 2026-02-04 10:15:30 UTC
- 持续时间: 15m 23s
- 测试: 127 通过, 0 失败
```

### 检查特定分支

```bash
python src/build_status.py --branch develop
```

输出:
```
构建状态报告
===================

项目: MyOS
分支: develop

当前构建:
- 状态: 进行中 ⟳
- 开始时间: 2026-02-04 11:30:15 UTC
- 已用时间: 5m 12s
- 进度: 正在运行测试 (3/5 阶段)
```

## CI 系统集成

### GitHub Actions

```bash
# 检查 GitHub Actions 状态
python src/build_status.py --ci github

# 检查特定工作流
python src/build_status.py --ci github --workflow "CI Pipeline"
```

输出:
```
GitHub Actions 状态
=====================

仓库: myorg/myos
工作流: CI Pipeline

最新运行:
- 状态: 成功 ✓
- 运行 #234
- 触发者: 推送到 main
- 持续时间: 12m 45s
- 所有作业成功完成
```

### GitLab CI

```bash
# 检查 GitLab CI 状态
python src/build_status.py --ci gitlab

# 检查特定流水线
python src/build_status.py --ci gitlab --pipeline 456789
```

输出:
```
GitLab CI 状态
================

项目: myorg/myos
流水线 #456789

状态: 通过 ✓
- 构建: 成功
- 测试: 成功
- 部署: 成功

持续时间: 18m 32s
```

### Jenkins

```bash
# 检查 Jenkins 构建状态
python src/build_status.py --ci jenkins

# 检查特定作业
python src/build_status.py --ci jenkins --job "myos-build"
```

输出:
```
Jenkins 构建状态
====================

作业: myos-build
构建 #123

状态: 成功 ✓
- 持续时间: 22m 15s
- 测试: 245 通过
- 控制台输出: 可用
```

## 构建历史

### 查看最近构建

```bash
# 显示最近 5 次构建
python src/build_status.py --limit 5
```

输出:
```
最近构建
=============

1. #12345 成功 ✓ (15m 23s) - 2026-02-04 10:30:53
   main: "Add network stack improvements"

2. #12344 失败 ✗ (12m 45s) - 2026-02-04 09:15:20
   main: "Update kernel module"

3. #12343 成功 ✓ (16m 12s) - 2026-02-03 15:20:10
   develop: "Fix memory leak"

4. #12342 成功 ✓ (14m 55s) - 2026-02-03 12:05:33
   main: "Optimize network performance"

5. #12341 成功 ✓ (15m 40s) - 2026-02-03 08:22:45
   main: "Update dependencies"
```

### 包含详细信息的构建历史

```bash
python src/build_status.py --limit 10 --verbose
```

## 输出格式

### 文本格式（默认）

```bash
python src/build_status.py --format text
```

### JSON 格式

```bash
python src/build_status.py --format json
```

输出:
```json
{
  "project": "MyOS",
  "branch": "main",
  "taskId": "12345",
  "currentBuild": {
    "status": "success",
    "triggeredBy": "john.doe",
    "started": "2026-02-04T10:15:30Z",
    "duration": 923,
    "commit": {
      "hash": "a1b2c3d4e5f6",
      "message": "Add network stack improvements"
    },
    "tests": {
      "passed": 127,
      "failed": 0,
      "skipped": 3
    }
  },
  "history": [
    {
      "id": "12345",
      "status": "success",
      "duration": 923,
      "date": "2026-02-04T10:30:53Z"
    },
    {
      "id": "12344",
      "status": "failed",
      "duration": 765,
      "date": "2026-02-04T09:27:05Z"
    }
  ]
}
```

### 简短格式（仅状态）

```bash
python src/build_status.py --format short
```

输出:
```
success
```

## 实时监控

### 监控构建进度

```bash
python src/build_status.py --watch
```

输出（实时更新）:
```
监控构建 #12345
=====================

状态: 进行中 ⟳
已用时间: 3m 45s

当前阶段: 运行测试
- 单元测试: 已完成 ✓
- 集成测试: 运行中... (45%)
- 系统测试: 待处理

按 Ctrl+C 停止监控
```

### 监控特定分支

```bash
python src/build_status.py --branch develop --watch
```

## Python API 使用

### 基本状态检查

```python
from build_status import BuildStatus

# 初始化
bs = BuildStatus(ci_system='github')

# 获取当前构建状态
status = bs.get_current_status()
print(f"状态: {status['status']}")
print(f"持续时间: {status['duration']}s")
```

### 检查构建历史

```python
from build_status import BuildStatus

bs = BuildStatus()

# 获取构建历史
history = bs.get_history(limit=10, branch='main')

for build in history:
    print(f"#{build['id']}: {build['status']} ({build['duration']}s)")
```

### 监控构建进度

```python
from build_status import BuildStatus

bs = BuildStatus()

# 使用回调监控构建
def on_status_change(status):
    print(f"构建状态: {status['stage']}")

bs.watch_build(build_id='12345', callback=on_status_change)
```

### 多个 CI 系统

```python
from build_status import BuildStatus

# 检查 GitHub Actions
github_bs = BuildStatus(ci_system='github', token='github_token')
gh_status = github_bs.get_current_status()

# 检查 GitLab CI
gitlab_bs = BuildStatus(ci_system='gitlab', token='gitlab_token')
gl_status = gitlab_bs.get_current_status()

# 比较状态
print(f"GitHub: {gh_status['status']}")
print(f"GitLab: {gl_status['status']}")
```

## 常见用例

### 部署前检查

```bash
#!/bin/bash
# 部署前验证所有构建通过

STATUS=$(python src/build_status.py --format short)

if [ "$STATUS" != "success" ]; then
    echo "错误: 构建未成功，无法部署"
    exit 1
fi

echo "所有构建通过，继续部署"
```

### PR 验证

```bash
#!/bin/bash
# 检查 PR 构建是否完成且成功

PR_BRANCH="feature/new-feature"
STATUS=$(python src/build_status.py --branch ${PR_BRANCH} --format json)

# 提取状态
BUILD_STATUS=$(echo $STATUS | jq -r '.currentBuild.status')

if [ "$BUILD_STATUS" != "success" ]; then
    echo "PR 构建失败或未完成"
    echo "状态: $BUILD_STATUS"
    exit 1
fi

echo "PR 构建成功"
```

### 构建失败通知

```bash
#!/bin/bash
# 监控构建并在失败时发送通知

python src/build_status.py --watch | while read line; do
    if echo "$line" | grep -q "Failed"; then
        # 发送通知（邮件、Slack 等）
        echo "构建失败!" | mail -s "构建失败警报" team@example.com
    fi
done
```

### CI 仪表板

```python
from build_status import BuildStatus
import time

# 创建简单仪表板
bs = BuildStatus()

while True:
    status = bs.get_current_status()
    history = bs.get_history(limit=5)

    print("\033[2J\033[H")  # 清屏
    print("=== CI 构建仪表板 ===")
    print(f"当前: {status['status']}")
    print(f"持续时间: {status.get('duration', 'N/A')}s")
    print("\n最近构建:")

    for build in history:
        print(f"  #{build['id']}: {build['status']}")

    time.sleep(30)  # 每 30 秒刷新
```

## 构建日志和详情

### 查看构建日志

```bash
# 获取构建日志
python src/build_status.py 12345 --logs
```

输出:
```
构建日志 - #12345
===================

[阶段 1/5] 检出代码... 完成
[阶段 2/5] 安装依赖... 完成
[阶段 3/5] 构建项目...
  - 编译内核模块... 完成
  - 构建用户空间工具... 完成
[阶段 4/5] 运行测试...
  - 单元测试: 127 通过
  - 集成测试: 45 通过
[阶段 5/5] 打包产物... 完成

构建在 15m 23s 内成功完成
```

### 详细构建信息

```bash
python src/build_status.py 12345 --verbose
```

输出:
```
构建详情 - #12345
======================

状态: 成功 ✓
分支: main
提交: a1b2c3d4e5f6
作者: john.doe
消息: "Add network stack improvements"

时间戳:
- 入队: 2026-02-04 10:15:00 UTC
- 开始: 2026-02-04 10:15:30 UTC
- 完成: 2026-02-04 10:30:53 UTC
- 持续时间: 15m 23s

测试结果:
- 总计: 130 个测试
- 通过: 127
- 失败: 0
- 跳过: 3

产物:
- myos-kernel.img (45.2 MB)
- myos-tools.tar.gz (12.8 MB)
- test-results.xml (234 KB)
```

## 错误处理

### 构建未找到

```bash
python src/build_status.py 99999
```

错误输出:
```
错误: 构建 #99999 未找到
可用最近构建: 12345, 12344, 12343
建议: 使用 --limit 查看更多构建
```

### 身份验证失败

```bash
python src/build_status.py --ci github
```

错误输出:
```
错误: GitHub Actions 身份验证失败
缺少或无效的令牌
建议: 设置 GITHUB_TOKEN 环境变量或使用 --token 选项
```

### 网络问题

```bash
python src/build_status.py
```

错误输出:
```
错误: 无法连接到 CI 系统
30 秒后网络超时
建议: 检查网络连接和 CI 系统可用性
```

## 快速参考

| 任务 | 命令 | 输出 |
|------|---------|--------|
| 当前构建状态 | `python src/build_status.py` | 当前分支构建状态 |
| 特定构建 | `python src/build_status.py 12345` | 构建 #12345 的详情 |
| 特定分支 | `python src/build_status.py --branch develop` | develop 分支构建状态 |
| 构建历史 | `python src/build_status.py --limit 10` | 最近 10 次构建 |
| JSON 输出 | `python src/build_status.py --format json` | 机器可读 JSON |
| 简短状态 | `python src/build_status.py --format short` | 仅成功/失败/运行中 |
| 监控构建 | `python src/build_status.py --watch` | 实时监控 |
| GitHub Actions | `python src/build_status.py --ci github` | GitHub 特定状态 |
| 构建日志 | `python src/build_status.py 12345 --logs` | 查看构建日志 |

## 选项总结

| 选项 | 可选值 | 默认值 | 说明 |
|--------|--------|---------|-------------|
| `task-id` | 构建 ID | 当前 | 要检查的特定构建 |
| `--ci` | `github`, `gitlab`, `jenkins` | 自动检测 | 要查询的 CI 系统 |
| `--branch` | 分支名称 | 当前 | 要检查的特定分支 |
| `--limit` | 数字 | 5 | 历史记录中的构建数量 |
| `--watch` | 标志 | false | 实时监控构建 |
| `--format` | `text`, `json`, `short` | `text` | 输出格式 |
| `--logs` | 标志 | false | 包含构建日志 |
| `--verbose` | 标志 | false | 显示详细信息 |

## 身份验证

### 环境变量

```bash
# GitHub Actions
export GITHUB_TOKEN="your_github_token"

# GitLab CI
export GITLAB_TOKEN="your_gitlab_token"

# Jenkins
export JENKINS_USER="your_username"
export JENKINS_TOKEN="your_api_token"
```

### 配置文件

创建 `~/.build-status-config.json`:
```json
{
  "github": {
    "token": "your_github_token"
  },
  "gitlab": {
    "token": "your_gitlab_token",
    "url": "https://gitlab.example.com"
  },
  "jenkins": {
    "url": "https://jenkins.example.com",
    "user": "your_username",
    "token": "your_api_token"
  }
}
```

## 依赖项

- **CI 系统 API 访问**: 需要身份验证令牌
- **网络连接**: 用于访问 CI 系统 API
- **Python 3.6+**: 用于运行脚本
- **Git**（可选）: 用于自动检测当前分支