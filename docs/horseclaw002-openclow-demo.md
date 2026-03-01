# HorseClaw 002 - 基于 OpenClaw 的 Demo 项目自动化

**编号**: horseclaw002  
**状态**: 当前方案  
**创建时间**: 2026-03-01

---

## 核心概念

| 角色 | 说明 |
|------|------|
| **HorseClaw (调度中心)** | 基于 OpenClaw 的多 Agent 调度系统 |
| **horseclaw (Demo 项目)** | 被操作的目标 Java 项目 |

---

## 架构设计

```
┌─────────────────────────────────────────────────────────┐
│              HorseClaw 调度中心 (OpenClaw)              │
│  ┌─────────────────────────────────────────────────┐   │
│  │  主 Agent: 负责任务分发、结果汇总、Git 管理      │   │
│  └─────────────────────────────────────────────────┘   │
│                         │                               │
│         openclaw sessions_spawn                        │
│                         │                               │
│    ┌────────────┬────────┴────────┬────────────┐      │
│    ▼            ▼                 ▼            ▼      │
│ ┌────────┐  ┌────────┐      ┌────────┐  ┌────────┐    │
│ │ Bug   │  │Feature│      │  Doc   │  │ Test  │    │
│ │Fixer  │  │Writer │      │  Writer│  │Writer │    │
│ │Agent  │  │Agent  │      │  Agent │  │Agent  │    │
│ └───┬───┘  └───┬───┘      └───┬────┘  └───┬───┘    │
│     │          │               │            │         │
│     └──────────┴───────────────┴────────────┘         │
│                         │                               │
│                    Git (本地)                          │
│                         │                               │
│                         ▼                               │
│  ┌─────────────────────────────────────────────────┐   │
│  │          horseclaw (Demo 项目)                  │   │
│  │    Java Maven 项目，被多个 Agent 并行操作        │   │
│  │    - src/main/java/*                            │   │
│  │    - src/test/java/*                            │   │
│  │    - pom.xml                                    │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

---

## 工作流程

```
┌────────────────────────────────────────────────────────┐
│                    HorseClaw 循环                      │
│                   (每 2-5 分钟)                        │
└────────────────────────────────────────────────────────┘
                          │
                          ▼
┌────────────────────────────────────────────────────────┐
│  1. 扫描 horseclaw 项目                                │
│     - mvn compile                                     │
│     - mvn test                                        │
│     - 检测问题                                        │
└──────────────────────────┬─────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────────┐
│  2. 任务分发 (并行)                                   │
│     - BugFixer: 修复编译/测试失败                     │
│     - FeatureWriter: 实现新功能                        │
│     - DocWriter: 更新文档                              │
│     - TestWriter: 补充测试                            │
└──────────────────────────┬─────────────────────────────┘
                           │
            ┌──────────────┼──────────────┐
            ▼              ▼              ▼
       ┌─────────┐   ┌─────────┐   ┌─────────┐
       │ Agent 1 │   │ Agent 2 │   │ Agent 3 │
       │  修复   │   │  写代码 │   │  写测试 │
       └────┬────┘   └────┬────┘   └────┬────┘
            │              │              │
            └──────────────┴──────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────────┐
│  3. Git 合并与提交                                    │
│     - 检测冲突                                         │
│     - mvn verify 100% 通过                            │
│     - git add → git commit → git push                 │
└──────────────────────────┬─────────────────────────────┘
                           │
                           ▼
                    ┌───────────┐
                    │  等待 2-5 │
                    │   分钟    │
                    └───────────┘
```

---

## Agent 职责

| Agent | 任务 | 输入 | 输出 |
|-------|------|------|------|
| **BugFixer** | 修复编译/测试失败 | `mvn test` 输出 | 修改 src/main/java |
| **FeatureWriter** | 实现新功能 | 需求描述 | 新增 src/main/java |
| **DocWriter** | 更新文档 | 代码变更 | 修改 README.md |
| **TestWriter** | 补充测试 | 代码覆盖报告 | 新增 src/test/java |

---

## 技术实现

### 1. OpenClaw 主 Agent

```yaml
# horseclaw 作为 OpenClaw skill
name: horseclaw
description: "AI-driven Java project automation"
capabilities:
  - spawn_subagents
  - execute_commands
  - git_operations
```

### 2. Subagent 配置

```java
// 每个 Agent 是一个 OpenClaw subagent session
SubagentConfig bugFixer = SubagentConfig.builder()
    .name("BugFixer")
    .promptTemplate("修复以下编译/测试错误:\n{error_output}\n项目目录: {project_path}")
    .tools("exec", "read", "write")
    .build();
```

### 3. Git 管理

```java
// 主 Agent 负责 Git 操作
GitManager git = new GitManager(projectPath);

public void commitAndPush(String message) {
    // 1. git add .
    // 2. git diff --cached --stat
    // 3. mvn verify (必须通过)
    // 4. git commit -m "{message}"
    // 5. git push
}
```

---

## 文件结构

```
horseclaw/                          # 被操作的 Demo 项目
├── pom.xml                        # Maven 配置
├── src/
│   ├── main/java/com/horseclaw/  # 业务代码
│   │   ├── HorseClaw.java
│   │   ├── agent/                 # Agent 逻辑
│   │   └── llm/                  # LLM 客户端
│   └── test/java/                # 测试代码
├── docs/                          # 文档
│   └── horseclaw001-*.md          # 历史方案
└── .horseclaw/                   # HorseClaw 配置
    ├── config.yaml
    └── agents.yaml
```

---

## 运行方式

### 方式 1: OpenClaw Session

```
用户: "HorseClaw，帮我优化 horseclaw 项目"
     │
     ▼
OpenClaw 主 Agent
     │
     ├── BugFixer (subagent) → 修复测试
     ├── FeatureWriter (subagent) → 添加功能
     └── DocWriter (subagent) → 更新文档
     │
     ▼
合并结果 → git push
```

### 方式 2: Cron 自动化

```bash
# 每 5 分钟运行一次
*/5 * * * * openclaw run horseclaw --daemon
```

---

## 优势

| 特性 | 说明 |
|------|------|
| **Demo 自闭环** | HorseClaw 自己维护 horseclaw 项目 |
| **并行高效** | 多个 subagent 同时工作 |
| **零配置** | 直接操作 Git 仓库 |
| **可观测** | 每轮结果可追溯 |

---

## 下一步

1. 在 horseclaw 项目中实现 HorseClaw 核心代码
2. 配置 OpenClaw skill
3. 试运行单 Agent
4. 扩展多 Agent 并行
