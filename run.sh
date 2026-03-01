#!/bin/bash
# AI 开发流水线 - 快速开始脚本

set -e

echo "======================================"
echo "  AI 驱动开发流水线"
echo "======================================"

# 1. 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 请先安装 Python 3"
    exit 1
fi

# 2. 安装依赖
echo ""
echo "📦 安装 Python 依赖..."
pip install -r requirements.txt

# 3. 检查 MiniMax API Key
if [ -z "$MINIMAX_API_KEY" ]; then
    echo ""
    echo "⚠️ 未设置 MINIMAX_API_KEY"
    echo "请运行:"
    echo "  export MINIMAX_API_KEY='your-api-key'"
else
    echo "✅ MiniMax API Key 已配置"
fi

# 4. 检查目标仓库
TARGET_REPO="${1:-.}"

if [ ! -d "$TARGET_REPO" ]; then
    echo "❌ 目录不存在: $TARGET_REPO"
    exit 1
fi

if [ ! -d "$TARGET_REPO/.git" ]; then
    echo "❌ 不是 Git 仓库: $TARGET_REPO"
    exit 1
fi

echo ""
echo "📁 目标仓库: $TARGET_REPO"

# 5. 运行流水线
echo ""
echo "🚀 启动流水线..."
echo "按 Ctrl+C 停止"
echo ""

python3 pipeline.py "$TARGET_REPO"
