# HorseClaw 004 - 生产级架构：独立智能体

**编号**: horseclaw004  
**状态**: 生产级方案  
**创建时间**: 2026-03-01

---

## 核心概念

基于 OpenClaw 多智能体架构，创建**独立的 HorseClaw 智能体**，实现：
- 完全隔离的工作区
- 独立的认证配置
- 24/7 无人值守运行
- 不干扰主 Agent (main)

---

## 架构设计

```
┌─────────────────────────────────────────────────────────────┐
│                    OpenClaw Gateway                         │
│                        (同一服务器)                          │
└─────────────────────────────────────────────────────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        ▼                  ▼                  ▼
┌───────────────┐  ┌───────────────┐  ┌───────────────┐
│   main        │  │   horseclaw   │  │   other       │
│   智能体       │  │   智能体      │  │   智能体      │
│               │  │               │  │               │
│ 个人助理       │  │ 项目自动化    │  │   其他任务     │
└───────────────┘  └───────────────┘  └───────────────┘
        │                  │                  │
        ▼                  ▼                  ▼
   workspace          workspace-         workspace-
                      horseclaw          other
```

---

## OpenClaw 配置

### 配置项说明

| 配置项 | 说明 |
|--------|------|
| `id` | 智能体唯一标识 |
| `name` | 显示名称 |
| `workspace` | 工作区目录 |
| `agentDir` | 状态目录（认证配置） |
| `model` | 使用的模型 |
| `default` | 是否为默认智能体 |

### 配置文件

**文件位置**: `~/.openclaw/openclaw.json`

```json
{
  "agents": {
    "list": [
      {
        "id": "main",
        "name": "Personal Assistant",
        "default": true,
        "workspace": "~/.openclaw/workspace",
        "agentDir": "~/.openclaw/agents/main/agent",
        "model": "minimax-cn/MiniMax-M2.5"
      },
      {
        "id": "horseclaw",
        "name": "HorseClaw",
        "workspace": "~/.openclaw/workspace-horseclaw",
        "agentDir": "~/.openclaw/agents/horseclaw/agent",
        "model": "minimax-cn/MiniMax-M2.5",
        "groupChat": {
          "mentionPatterns": ["@horseclaw", "horseclaw"]
        },
        "sandbox": {
          "mode": "off"
        },
        "tools": {
          "allow": [
            "exec",
            "read",
            "write",
            "edit",
            "git",
            "sessions_spawn",
            "sessions_list",
            "sessions_history"
          ],
          "deny": []
        }
      }
    ],
    "bindings": [
      {
        "agentId": "horseclaw",
        "match": {
          "channel": "telegram",
          "peer": {
            "kind": "dm",
            "id": "6072206856"
          }
        }
      },
      {
        "agentId": "main",
        "match": {
          "channel": "telegram"
        }
      }
    ]
  }
}
```

---

## 工作区结构

### 主智能体 (main)

```
~/.openclaw/workspace/           # 原有用法不变
├── AGENTS.md
├── SOUL.md
├── USER.md
├── MEMORY.md
├── skills/
├── docs/
└── ...
```

### HorseClaw 智能体

```
~/.openclaw/workspace-horseclaw/
├── AGENTS.md                    # HorseClaw 人设
├── SOUL.md
├── USER.md
├── memory/                      # HorseClaw 记忆
├── projects/                    # 被操作的项目
│   └── horseclaw-didadi/       # 克隆的项目
├── skills/                     # HorseClaw 专用 skills
│   └── horseclaw/
└── logs/                       # 运行日志
```

---

## 消息路由规则

### 绑定优先级

1. **精确匹配** (peer id)
2. **渠道匹配** (channel)
3. **默认智能体** (default)

### 路由示例

| 消息来源 | 路由到 | 说明 |
|---------|-------|------|
| Telegram DM 6072206856 | horseclaw | 自动化任务 |
| Telegram 群组 | main | 日常对话 |
| 其他 Telegram | main | 默认 |

### 触发方式

```
用户发给 horseclaw (DM):
  → 6072206856

路由规则匹配:
  channel: telegram
  peer.id: 6072206856
  → horseclaw 智能体
```

---

## HorseClaw 智能体配置

### AGENTS.md

```markdown
# HorseClaw Agent

你是 HorseClaw，AI 驱动的 Java 项目自动化开发引擎。

## 职责

- 优化指定的项目
- 修复 bug
- 添加功能
- 补充测试
- 更新文档

## 触发方式

- 收到任务请求
- 定时任务触发

## 工作流程

1. 克隆目标项目
2. Spawn 4 个 subagent (BugFixer, FeatureWriter, DocWriter, TestWriter)
3. 汇总结果
4. git push

## 规则

- mvn verify 100% 通过才能 commit
- 极端原子 commit
- 提交信息格式: feat/fix/docs/test: 描述
```

### USER.md

```markdown
# HorseClaw User

- 用途: Java 项目自动化开发
- 目标项目: horseclaw-didadi
- 运行间隔: 5 分钟
- 最大提交: 50 次/小时
```

---

## 定时任务配置

### Cron 配置

```bash
# HorseClaw 定时任务
*/5 * * * * openclaw run horseclaw --target lbsha/horseclaw-didadi
```

### 配置示例

```yaml
# ~/.openclaw/cron/horseclaw-daily.json
{
  "id": "horseclaw-daily",
  "name": "HorseClaw Daily",
  "schedule": "0 9 * * *",
  "agentId": "horseclaw",
  "task": "优化 horseclaw-didadi 项目",
  "enabled": true
}
```

---

## 独立运行方式

### 方式 1: Telegram DM

```
直接发消息给 bot:
  /horseclaw 优化 horseclaw-didadi
```

### 方式 2: Cron 自动

```bash
# 每小时运行一次
0 * * * * openclaw run horseclaw
```

### 方式 3: 手动触发

```bash
openclaw run horseclaw --target lbsha/horseclaw-didadi
```

---

## 资源隔离

### 对比

| 资源 | main | horseclaw |
|------|------|-----------|
| 工作区 | workspace | workspace-horseclaw |
| 认证 | main/agent | horseclaw/agent |
| 会话 | main sessions | horseclaw sessions |
| Skills | 共享 | 独立安装 |
| Cron | 原有 | 独立配置 |

### 隔离效果

- **不影响**: main Agent 运行
- **独立**: horseclaw 智能体完全独立
- **并行**: 两者可以同时运行

---

## 部署步骤

### 1. 创建工作区

```bash
mkdir -p ~/.openclaw/workspace-horseclaw
cp ~/.openclaw/workspace/AGENTS.md ~/.openclaw/workspace-horseclaw/
cp ~/.openclaw/workspace/USER.md ~/.openclaw/workspace-horseclaw/
```

### 2. 修改配置

```bash
# 编辑 openclaw.json
nano ~/.openclaw/openclaw.json
```

添加 horseclaw 智能体配置。

### 3. 重启 Gateway

```bash
openclaw gateway restart
```

### 4. 验证

```bash
openclaw agents list --bindings
```

### 5. 测试

```
发送消息给 bot:
  "优化 horseclaw-didadi"
```

---

## 监控

### 查看 horseclaw 状态

```bash
# 查看智能体列表
openclaw agents list

# 查看 horseclaw 会话
openclaw sessions list --agent horseclaw

# 查看日志
tail -f ~/.openclaw/agents/horseclaw/logs/*.log
```

---

## 备份与恢复

### 备份

```bash
# 备份 horseclaw 工作区
tar -czvf horseclaw-workspace.tar.gz ~/.openclaw/workspace-horseclaw/

# 备份配置
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.bak
```

### 恢复

```bash
# 恢复工作区
tar -xzvf horseclaw-workspace.tar.gz -C ~/

# 恢复配置
cp ~/.openclaw/openclaw.json.bak ~/.openclaw/openclaw.json
```

---

## 优势

| 特性 | 说明 |
|------|------|
| **完全隔离** | 不干扰主 Agent |
| **独立运行** | 24/7 无人值守 |
| **灵活配置** | 可自定义模型、工具 |
| **消息路由** | 支持精确匹配 |
| **并行工作** | main + horseclaw 同时运行 |

---

## 风险控制

| 风险 | 措施 |
|------|------|
| 过度提交 | 每小时 max 50 commit |
| 破坏构建 | mvn verify 强制检查 |
| Token 耗尽 | 监控使用量 |
| 并发冲突 | Git lock + 重试 |

---

## 下一步

1. 创建 workspace-horseclaw 目录
2. 修改 openclaw.json
3. 重启 Gateway
4. 测试运行
