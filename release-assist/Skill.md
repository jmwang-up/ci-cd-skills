# 发布协助技能 (release-assist)

## 功能描述
release-assist 是一个协助进行操作系统项目版本发布流程的实用技能。该技能能够自动化执行版本发布的关键步骤，包括版本号更新、变更日志生成、Git标签创建、发布包构建等，确保发布过程的一致性和可靠性。

## 使用场景
1. 新版本发布流程自动化
2. 发布前检查和验证
3. 多环境发布协调
4. 发布回滚和补丁发布

## 实现要点

### 核心功能
- 自动化版本号更新和验证
- 自动生成变更日志(CHANGELOG)
- 创建和推送Git标签
- 构建和验证发布包
- 发布通知和文档更新
- 发布回滚支持

### 技能接口设计
```
命令: /release-assist <version> [options]

参数:
  version               要发布的版本号(如 v2.1.3)
  --dry-run             仅显示将要执行的操作，不实际执行
  --skip-tests          跳过测试步骤
  --skip-build          跳过构建步骤
  --target <targets>    指定发布目标 (github, docker, packages)
  --branch <branch>     指定发布分支
  --pre-release         标记为预发布版本

示例:
  /release-assist v2.1.3
  /release-assist v2.1.3 --dry-run --branch release/v2.1
  /release-assist v2.1.3-rc1 --pre-release
```

### 技术实现要点
1. 版本号格式验证和解析
2. Git操作自动化(提交、标签、推送)
3. 变更日志自动生成(基于Git历史)
4. 构建系统集成和发布包验证
5. 多平台发布目标支持
6. 事务性操作和错误回滚机制

### 依赖要求
- Git命令行工具和仓库访问权限
- 构建工具链和依赖
- 发布目标的认证信息(GitHub Token等)
- 对项目发布流程的完整理解

### 错误处理
- 版本号格式无效
- Git操作冲突或失败
- 构建过程失败
- 发布目标认证失败
- 网络连接问题

## 工作流程

1. 验证版本号格式和唯一性
2. 检查当前工作区状态(确保干净)
3. 更新版本号到配置文件
4. 生成变更日志
5. 提交版本更新和变更日志
6. 创建并推送Git标签
7. 触发构建流程并验证产物
8. 推送发布包到指定目标
9. 发送发布通知

## 输出示例

### 发布流程输出
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
```

### 错误处理输出
```
Release Assistant
=================

Target Version: v2.1.3
Branch: main

[1/9] Validating version... OK
[2/9] Checking workspace... FAILED

Error: Uncommitted changes found in workspace
Please stash or commit your changes before proceeding with the release.

Use --dry-run to see what would be affected.
```