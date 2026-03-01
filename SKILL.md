---
name: horseclaw
description: "AI-driven Java project automation - 马力全开，爪到成功"
metadata:
  openclaw:
    emoji: 🐎
    capabilities:
      - spawn_subagents
      - execute_commands
      - git_operations
---

# HorseClaw 🐎🦞

马力全开，爪到成功

OpenClaw Skill: 自动化 Java 项目开发 Agent

## 触发方式

用户输入：
- "用 HorseClaw 优化 xxx 项目"
- "HorseClaw，帮我改 xxx"
- "horseclaw run"

## 工作流程

### 1. 分析任务
- 理解用户需求
- 确定目标项目
- 制定任务计划

### 2. 克隆项目
```bash
git clone https://github.com/{owner}/{repo}.git
cd {repo}
```

### 3. Spawn Subagents (并行)
- **BugFixer**: 修复编译/测试错误
- **FeatureWriter**: 添加新功能
- **DocWriter**: 更新文档
- **TestWriter**: 补充测试

### 4. 合并结果
- 检查 Git 状态
- 处理冲突
- 运行 mvn verify

### 5. 提交推送
```bash
git add .
git commit -m "feat: ..."
git push
```

### 6. 汇报结果
- 汇总提交记录
- 发送给用户

## Subagents

### BugFixer
- 职责：修复编译/测试错误
- 工具：exec, read, write

### FeatureWriter
- 职责：实现新功能
- 工具：exec, read, write

### DocWriter
- 职责：更新文档
- 工具：exec, read, write

### TestWriter
- 职责：补充单元测试
- 工具：exec, read, write

## 配置

### 默认参数
```yaml
project_path: /tmp/target-project
interval_minutes: 3
max_commits_per_hour: 50
commit_threshold: 1
```

## 使用示例

```
用户: "用 HorseClaw 优化 horseclawdidadi 项目"

HorseClaw:
1. 克隆 https://github.com/lbsha/horseclawdidadi
2. 分析代码结构
3. Spawn 4 个 subagents
4. 合并结果
5. git push
6. 汇报完成
```

## 注意

- 确保 mvn verify 100% 通过才提交
- 避免并发冲突
- 控制提交频率
