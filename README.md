# HorseClaw 🐎🦞

马力全开，爪到成功

2026 马年限定版自主 coding agent —— 像 Peter Steinberger 一样，一人顶团队，疯狂迭代你的代码。

---

HorseClaw 是为大型 Java/Spring Boot 项目（尤其是金融/证券行业）量身打造的 AI 驱动开发引擎。

它以 **极端原子 commit**、**无人值守 loop**、**多 agent 协作**（Coder → Committer → Reviewer）为核心，追求 **信**（准确无 bug、合规审计）、**达**（马力全开、速达迭代）、**雅**（代码优雅、可维护）三合一境界。

- **一天几百 commit**？它能。
- **本地 mvn verify 100% 通过才 push**？强制。
- **证券风控/审计日志永不遗漏**？内置边界。
- **马年加持**：马上修复 bug，马上加测试，马上优雅重构。

---

灵感来源：OpenClaw 的 claw 狠劲 + 马年"马上""马到成功"的速度与吉祥。

HorseClaw = **马力爪** —— 奔腾如马，撕裂如爪，代码如万马奔腾般前进。

---

[快速上手](#快速上手) | [核心规则](#核心规则) | [多 agent 协作](#多-agent-协作) | [马年彩蛋](#马年彩蛋)

---

> "放自己一马？不，HorseClaw 放的是 bug。" —— ClawFather 精神传承 🐎

---

## 当前状态

🚀 **Alpha**（马年冲刺中）

---

## Star & Fork

如果你也想马力全开！

[![Star](https://img.shields.io/github/stars/lbsha/horseclaw?style=social)](https://github.com/lbsha/horseclaw/stargazers)
[![Fork](https://img.shields.io/github/forks/lbsha/horseclaw?style=social)](https://github.com/lbsha/horseclaw/network)

---

# AI 驱动开发流水线

自动化闭环开发流程：发现问题 → 写代码 → 跑测试 → 修复 → 提交

基于 OpenClaw 作者 Peter 的实践，每分钟可执行多次循环。

---

## 快速开始

### 1. 克隆模板

```bash
git clone https://github.com/yourname/ai-pipeline-template.git
cd ai-pipeline-template
```

### 2. 配置环境变量

```bash
# MiniMax API Key
export MINIMAX_API_KEY="your-api-key"

# 可选配置
export OPENCLAW_TELEGRAM_CHAT_ID="your-chat-id"
```

### 3. 运行

```bash
chmod +x run.sh
./run.sh /path/to/your/project
```

---

## 文件结构

```
ai-pipeline/
├── README.md              # 本文件
├── config.yaml          # 配置文件
├── pipeline.py         # 主程序 (集成 MiniMax)
├── minimax_client.py   # MiniMax API 客户端
├── requirements.txt    # Python 依赖
├── run.sh              # 快速启动脚本
└── alerts.py           # 告警模块
```

---

## 配置说明

### config.yaml

```yaml
pipeline:
  max_iterations: 1000       # 最大循环次数
  commit_threshold: 3        # 连续通过次数才提交
  max_commits_per_hour: 50   # 每小时最多提交

minimax:
  enabled: true
  model: MiniMax-M2.1       # 模型选择
  temperature: 0.7         # 创意程度

alerts:
  telegram:
    enabled: true
    chat_id: "6072206856"
```

---

## MiniMax 模型选择

| 模型 | 速度 | 能力 | 推荐场景 |
|------|------|------|---------|
| MiniMax-M2.1 | 快 | 中等 | 日常修复 |
| MiniMax-M2.5 | 慢 | 强 | 复杂问题 |

---

## 工作流程

```
┌────────────────────────────────────────────┐
│  1. 发现问题 (lint/test/type-check)       │
└──────────────────┬─────────────────────────┘
                   ▼
┌────────────────────────────────────────────┐
│  2. MiniMax 生成修复代码                   │
└──────────────────┬─────────────────────────┘
                   ▼
┌────────────────────────────────────────────┐
│  3. MiniMax 代码审查                       │
└──────────────────┬─────────────────────────┘
                   ▼
┌────────────────────────────────────────────┐
│  4. 应用修复                              │
└──────────────────┬─────────────────────────┘
                   ▼
┌────────────────────────────────────────────┐
│  5. 运行测试                              │
└──────────────────┬─────────────────────────┘
                   ▼
           ┌───────────────┐
           │   通过?       │
           └───────┬───────┘
        ✅通过          ❌失败
         │             │
         ▼             ▼
    自动提交      自动修复
         │        (回到步骤2)
         ▼
      结束循环
```

---

## 效果

| 指标 | 传统开发 | AI 流水线 |
|------|---------|-----------|
| 单次修复 | 30分钟+ | ~2分钟 |
| 每日提交 | 5-10次 | 100+次 |
| 问题发现 | 人工 | 自动 |
| 回归测试 | 手动 | 自动 |

---

## 安全注意

⚠️ **重要提示**：
1. 先在测试仓库运行
2. 设置提交频率上限
3. 启用失败告警
4. 定期检查提交质量

---

## 常见问题

### Q: 修复代码不正确怎么办？
A: 调整 `temperature` 参数（越低越保守），或提高 `commit_threshold`

### Q: API 调用失败怎么办？
A: 检查 `MINIMAX_API_KEY` 是否正确，确保网络畅通

### Q: 如何停止？
A: 按 `Ctrl+C`，流水线会保存状态后优雅退出

---

## 扩展

### 添加更多 LLM

修改 `minimax_client.py`：

```python
# 添加 OpenAI
def call_openai(prompt):
    # 实现...
    pass

# 在 pipeline.py 中切换
LLM_PROVIDER = "openai"  # 或 "minimax"
```

---

## 许可证

MIT License
