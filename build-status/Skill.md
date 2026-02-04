# 构建状态检查技能 (build-status)

## 功能描述
build-status 是一个用于检查操作系统项目CI构建状态的实用技能。该技能能够与主流CI系统集成，查询指定构建任务的当前状态、历史记录和详细信息，并提供实时状态更新通知功能。

## 使用场景
1. 开发过程中监控构建状态
2. PR提交后验证CI检查结果
3. 发布流程中确认所有构建任务通过
4. 日常运维中监控CI系统健康状态

## 实现要点

### 核心功能
- 查询指定构建任务的当前状态
- 获取构建任务的详细信息(日志、耗时、触发者等)
- 查询构建历史记录和趋势
- 实时状态监控和通知
- 支持多种CI系统(GitHub Actions, GitLab CI, Jenkins等)

### 技能接口设计
```
命令: /build-status [task-id] [options]

参数:
  task-id               构建任务标识符(可选，如未指定则使用当前分支)
  --ci <system>         指定CI系统 (github, gitlab, jenkins)
  --branch <branch>     指定分支名称
  --limit <number>      限制返回的构建历史数量
  --watch               实时监控构建状态
  --format <format>     指定输出格式 (json, text, short)

示例:
  /build-status
  /build-status --branch develop --limit 5
  /build-status 12345 --ci github --watch
```

### 技术实现要点
1. 多种CI系统的API集成
2. 构建状态解析和标准化
3. 实时监控实现(轮询或WebSocket)
4. 身份认证和权限管理
5. 结果缓存和性能优化

### 依赖要求
- 对CI系统的访问权限和认证信息
- 网络连接以访问CI系统API
- 对项目结构和分支模型的理解

### 错误处理
- CI系统认证失败
- 构建任务不存在或无法访问
- 网络连接问题
- API调用频率限制

## 输出示例

### 默认文本格式输出
```
Build Status Report
===================

Project: MyOS
Branch: main
Task ID: 12345

Current Build:
- Status: Success
- Triggered by: john.doe
- Started: 2026-02-04 10:15:30 UTC
- Duration: 15m 23s
- Commit: a1b2c3d4e5f6 "Add network stack improvements"

Recent Builds:
1. #12345 Success (15m 23s) - 2026-02-04
2. #12344 Failed (12m 45s) - 2026-02-04
3. #12343 Success (16m 12s) - 2026-02-03
```

### JSON 格式输出
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
    }
  },
  "history": [
    {
      "id": "12345",
      "status": "success",
      "duration": 923,
      "date": "2026-02-04T10:30:53Z"
    }
  ]
}
```