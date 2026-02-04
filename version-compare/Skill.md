# 版本比较技能 (version-compare)

## 功能描述
version-compare 是一个用于比较操作系统项目不同版本间差异的实用技能。该技能能够比较两个版本的配置、依赖、源代码变更等信息，并生成详细的差异报告，帮助开发者和运维人员了解版本升级的影响。

## 使用场景
1. 版本升级前评估变更影响
2. CI/CD 流程中验证版本变更内容
3. 生产环境部署前确认变更范围
4. 代码审查时比较分支差异

## 实现要点

### 核心功能
- 比较两个版本的配置文件差异
- 比较两个版本的依赖变更
- 比较两个版本的源代码变更(Git Diff)
- 生成结构化的差异报告
- 支持多种输出格式

### 技能接口设计
```
命令: /version-compare <version1> <version2> [options]

参数:
  version1              要比较的第一个版本(标签、分支或提交哈希)
  version2              要比较的第二个版本(标签、分支或提交哈希)
  --format <format>     指定输出格式 (json, text, html)
  --sections <items>    指定要比较的部分 (config, dependencies, code, all)
  --output-file <file>  将结果输出到文件

示例:
  /version-compare v1.0.0 v2.0.0
  /version-compare v1.0.0 v2.0.0 --format json --sections code
  /version-compare main develop --sections config,dependencies
```

### 技术实现要点
1. 版本标识符解析(Git 标签、分支、提交哈希)
2. 多维度差异比较实现
3. 差异数据结构化处理
4. Git 命令调用和差异解析
5. 报告生成和格式化

### 依赖要求
- Git 命令行工具
- 对项目 Git 仓库的访问权限
- 读取项目配置文件的权限

### 错误处理
- 版本标识符无效或不存在
- Git 命令执行失败
- 项目结构不一致
- 权限不足无法访问某些文件

## 输出示例

### 默认文本格式输出
```
Version Comparison Report
=========================

Comparing v1.0.0 → v2.0.0

Configuration Changes:
- Version updated from 1.0.0 to 2.0.0
- New config option 'enable_new_feature' added

Dependency Changes:
- Updated kernel dependency from 5.4 to 5.10
- Added new dependency: libssl 1.1.1

Code Changes:
- 24 files changed, 456 insertions(+), 123 deletions(-)
- Major features added:
  * Memory management improvements
  * Network stack enhancements
- Breaking changes:
  * Deprecated syscall removed
```

### JSON 格式输出
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
      }
    ],
    "dependencies": [
      {
        "type": "updated",
        "dependency": "kernel",
        "from": "5.4",
        "to": "5.10"
      }
    ],
    "code": {
      "summary": "24 files changed, 456 insertions(+), 123 deletions(-)",
      "details": {
        "features": ["Memory management improvements", "Network stack enhancements"],
        "breaking": ["Deprecated syscall removed"]
      }
    }
  }
}
```