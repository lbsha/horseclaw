# HorseClaw 003 - OpenClaw Skill/Workflow 架构

**编号**: horseclaw003  
**状态**: 当前方案  
**创建时间**: 2026-03-01

---

## 核心概念

| 组件 | 定义 |
|------|------|
| **HorseClaw** | OpenClaw Skill/Workflow，不是独立项目 |
| **主 Agent** | OpenClaw 主 session |
| **Sub Agents** | OpenClaw subagent sessions |
| **操作目标** | horseclaw 仓库 (GitHub 上的 Java Maven 项目) |

---

## 架构设计

```
用户 (Telegram)
    │
    ▼
┌─────────────────────────────────────────────────────┐
│           OpenClaw 主 Agent (主 session)             │
│   - 负责任务分发                                    │
│   - spawn subagents                                 │
│   - 汇总结果                                        │
│   - Git 操作                                        │
└─────────────────────────────────────────────────────┘
    │
    │ sessions_spawn
    │
    ├─────────────────────────────────────────────────┤
    │                                                  │
    ▼          ▼          ▼          ▼               │
┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐     │
│BugFixer │ │Feature  │ │  Doc    │ │  Test   │     │
│Subagent │ │ Writer  │ │ Writer  │ │ Writer  │     │
│         │ │Subagent │ │Subagent │ │Subagent │     │
└────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘     │
     │           │           │           │           │
     │           │           │           │           │
     └───────────┴───────────┴───────────┘           │
                    │                               │
                    ▼                               │
         ┌──────────────────────┐                   │
         │    GitHub 仓库       │                   │
         │    horseclaw         │                   │
         │  (Java Maven 项目)   │                   │
         └──────────────────────┘                   │
                                                   │
└───────────────────────────────────────────────────┘
                    │
                    ▼
              git push
```

---

## 角色分工

### HorseClaw (OpenClaw Skill/Workflow)

- **不是独立项目**
- 是一个 **OpenClaw Skill**，包含：
  - `SKILL.md` - Skill 定义
  - `workflow.yaml` - Workflow 编排
  - `prompts/` - 4 个 subagent 的 prompt 模板

### horseclaw (GitHub 仓库)

- 普通的 **Java Maven 项目**
- 是被操作的对象
- 包含：
  - `src/main/java/` - 业务代码
  - `src/test/java/` - 测试代码
  - `pom.xml` - Maven 配置
  - `docs/` - 文档

---

## 工作流程

```
用户输入:
  "HorseClaw，帮我优化 horseclaw 项目"
           │
           ▼
┌─────────────────────────────────────┐
│      OpenClaw 主 Agent              │
│  (session: main)                    │
└─────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────┐
│  1. 分析任务                        │
│     - 扫描 horseclaw 仓库           │
│     - 了解项目结构                   │
│     - 制定任务计划                   │
└─────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────┐
│  2. Spawn Subagents (并行)          │
│     sessions_spawn                  │
│     - BugFixer                     │
│     - FeatureWriter                │
│     - DocWriter                   │
│     - TestWriter                  │
└─────────────────────────────────────┘
           │
    ┌──────┼──────┬──────┐
    ▼      ▼      ▼      ▼
┌────────┐  ... 4 个 subagents 并行工作
│        │
│ 每个 Subagent:
│  - 克隆 horseclaw 到本地
│  - 读取代码
│  - 写代码/测试/文档
│  - 本地测试
│  - git commit
│        │
└────────┘
    │
    ▼
┌─────────────────────────────────────┐
│  3. 汇总结果                        │
│     - 检查各 subagent 结果          │
│     - 处理冲突                       │
│     - git push                      │
└─────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────┐
│  4. 报告                            │
│     - 汇总提交记录                   │
│     - 发送给用户                     │
└─────────────────────────────────────┘
```

---

## Subagent 详细

| Subagent | Prompt 模板 | 操作 |
|----------|-------------|------|
| **BugFixer** | "修复 horseclaw 项目中的编译/测试错误" | 修改 src/main/java |
| **FeatureWriter** | "为 horseclaw 添加新功能: {feature}" | 新增 src/main/java |
| **DocWriter** | "更新 horseclaw 项目的文档" | 修改 docs/ |
| **TestWriter** | "为 horseclaw 补充单元测试" | 新增 src/test/java |

---

## 文件结构

### OpenClaw Skill: horseclaw

```
~/.openclaw/skills/horseclaw/
├── SKILL.md                      # Skill 定义
├── workflow.yaml                 # Workflow 编排
├── config.yaml                   # 配置
└── prompts/
    ├── bugfixer.md              # BugFixer prompt
    ├── feature.md               # FeatureWriter prompt
    ├── doc.md                   # DocWriter prompt
    └── test.md                  # TestWriter prompt
```

### 被操作项目: horseclaw (GitHub)

```
https://github.com/lbsha/horseclaw
├── pom.xml                      # Maven 配置
├── src/
│   ├── main/java/               # 业务代码
│   └── test/java/               # 测试代码
└── docs/                        # 文档
```

---

## 运行方式

### 触发方式

```
方式 A: 用户输入
  用户: "HorseClaw，帮我优化 horseclaw 项目"
  
方式 B: Cron 触发
  */5 * * * * openclaw run horseclaw
```

### 主 Agent Prompt 示例

```
你是 HorseClaw 调度中心。

任务：优化 horseclaw 项目 (https://github.com/lbsha/horseclaw)

请按以下步骤执行：

1. 克隆 horseclaw 项目到本地
2. 分析项目结构
3. Spawn 4 个 subagents 并行工作：
   - BugFixer: 修复发现的 bug
   - FeatureWriter: 添加小功能
   - DocWriter: 更新文档
   - TestWriter: 补充测试
4. 等待所有 subagent 完成
5. 合并结果，运行 mvn verify
6. git push 到 GitHub
7. 汇报结果
```

---

## Subagent Prompt 示例 (BugFixer)

```
你是 BugFixer Agent。

任务：修复 horseclaw 项目中的 bug。

1. 进入项目目录
2. 运行 mvn compile && mvn test
3. 分析错误输出
4. 修复问题
5. 再次运行测试确认修复成功
6. git commit (如果测试通过)

项目目录: /tmp/horseclaw
```

---

## 优势

| 优势 | 说明 |
|------|------|
| **零开发** | HorseClaw 是 OpenClaw Skill，无需写代码 |
| **并行高效** | 4 个 subagent 同时工作 |
| **自包含** | 所有 Agent 由 OpenClaw 管理 |
| **易扩展** | 添加新 Agent 只需加 prompt |
| **可观测** | 每个 subagent 都有独立 session |

---

## 下一步

1. 创建 `~/.openclaw/skills/horseclaw/`
2. 编写 SKILL.md
3. 编写 workflow.yaml
4. 编写 4 个 subagent prompt
5. 测试运行
