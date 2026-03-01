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

## 快速上手

### 1. 安装 Skill

将 horseclaw 复制到 OpenClaw skills 目录：

```bash
cp -r horseclaw ~/.openclaw/skills/
```

### 2. 触发运行

```bash
# 告诉 OpenClaw 主 Agent：
"用 HorseClaw 优化 horseclaw-didadi 项目"
```

### 3. 工作流程

```
用户 → 主 Agent → Spawn 4 个 Subagents → Git Push → 汇报结果
```

---

## 核心规则

### 极端原子 Commit

每一次 commit 只做一件事：
- 修复一个 bug
- 添加一个测试
- 重构一个函数
- 优化一处性能

### 无人值守 Loop

```
发现 → 修复 → 测试 → 审查 → 提交
   ↑                      ↓
   ←←←←← 失败则循环 ←←←←
```

### 100% 通过才 Push

本地测试必须全部通过才能推送代码。

---

## 多 Agent 协作

| Agent | 职责 |
|-------|------|
| **BugFixer** | 修复编译/测试错误 |
| **FeatureWriter** | 添加新功能 |
| **DocWriter** | 更新文档 |
| **TestWriter** | 补充测试 |

---

## 马年彩蛋

- 每次启动显示 "🐎 马力全开！"
- 连续 10 次成功 commit 显示 "🎉 马到成功！"
- 修复 critical bug 显示 "🦞 bug 哪里跑！"

---

## 文档

- [horseclaw001](docs/horseclaw001-openclow-based.md) - 初始架构
- [horseclaw002](docs/horseclaw002-openclow-demo.md) - Demo 自动化
- [horseclaw003](docs/horseclaw003-openclow-skill.md) - OpenClaw Skill 架构

---

🦞 *HorseClaw - 马力全开，爪到成功！*
