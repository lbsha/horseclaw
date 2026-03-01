# HorseClaw 001 - 基于 OpenClaw 的多 Agent 架构

**编号**: horseclaw001  
**状态**: 已归档  
**创建时间**: 2026-03-01

---

## 核心思路

利用 OpenClaw 的 **subagents** 能力，每个 Agent 是一个独立的 OpenClaw session。

---

## 架构设计

```
┌─────────────────────────────────────────┐
│         HorseClaw (主调度)               │
│    Java 程序 + OpenClaw CLI 调用        │
└─────────────────────────────────────────┘
              │
    openclaw sessions_spawn
              │
    ┌──────────┼──────────┬──────────┐
    ▼          ▼          ▼          ▼
┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐
│ bug    │ │feature │ │  doc   │ │refactor│
│ fixer  │ │ writer │ │ writer │ │  agent │
│session │ │session │ │session │ │session │
└────────┘ └────────┘ └────────┘ └────────┘
    │          │          │          │
    └──────────┴──────────┴──────────┘
              │
        Git (共享)
```

---

## Agent 配置

| Agent | 职责 | 触发条件 |
|-------|------|---------|
| **BugFixer** | 修复 bug | lint/test 失败 |
| **FeatureWriter** | 添加功能 | 需求分析 |
| **DocWriter** | 写/更新文档 | 代码变更 |
| **Refactorer** | 代码重构 | 复杂度高 |
| **TestWriter** | 补充测试 | 覆盖率低 |

---

## 每个 Agent 的 Loop

```
while (running) {
    1. 扫描问题 (mvn test, sonar, lint)
    2. 生成修复代码 (MiniMax API)
    3. 本地编译测试 (mvn compile test)
    4. 失败? → 回到步骤 2
    5. 成功 → commit → push
    6. 等待 2-5 分钟
}
```

---

## 技术实现

| 组件 | 技术 |
|------|------|
| **Agent** | OpenClaw sessions (subagent) |
| **LLM** | OpenClaw 内置 MiniMax |
| **Git** | gh CLI |
| **构建** | mvn (本地) |
| **调度** | Java ScheduledExecutor |
| **配置** | YAML |

---

## 文件结构

```
src/main/java/com/horseclaw/
├── HorseClaw.java           # 主入口
├── OpenClawClient.java      # OpenClaw CLI 封装
│                           # 使用 sessions_spawn
├── scheduler/
│   └── AgentScheduler.java # Agent 调度器
├── agent/
│   ├── BugFixerSession.java
│   ├── FeatureWriterSession.java
│   └── DocWriterSession.java
└── config/
    └── AgentConfig.java
```

---

## 核心代码逻辑

```java
// 1. 启动 Agent
SessionsSpawnParams params = SessionsSpawnParams.builder()
    .agentId("default")
    .runtime("subagent")
    .task("修复这个 bug: " + bugDescription)
    .build();

String sessionKey = openclaw.sessions_spawn(params);

// 2. 检查结果
while (running) {
    String result = openclaw.sessions_history(sessionKey);
    if (result.contains("FIXED") && runTests()) {
        git.commit("fix: " + bugId);
    }
    Thread.sleep(intervalMinutes * 60 * 1000);
}
```

---

## 运行方式

```bash
# 方式1: 终端
java -jar horseclaw.jar --agents bugfixer,feature,doc --interval 3

# 方式2: Cron
*/5 * * * * java -jar horseclaw.jar --daemon
```

---

## 优势

| 对比 | 纯 Java | 基于 OpenClaw |
|------|---------|---------------|
| LLM 集成 | 需自己写 | 内置 MiniMax |
| 多 Agent | 需自己实现 | subagents 原生支持 |
| Telegram 通知 | 需自己写 | 内置 message 工具 |
| Skills | 需自己装 | 52+ 官方 Skills 可用 |

---

## 风险控制

| 保护 | 措施 |
|------|------|
| 并发冲突 | Git lock + 重试机制 |
| 过度提交 | 每小时 max 50 commit |
| 破坏构建 | mvn verify 100% 才 push |
| 无限循环 | max iterations 上限 |

---

## 下一步

1. 确认架构 OK
2. 先实现单个 Agent (BugFixer)
3. 再扩展到多 Agent 并行
