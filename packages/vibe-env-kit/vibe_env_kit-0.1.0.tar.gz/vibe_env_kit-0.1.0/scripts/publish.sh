#!/bin/bash
# Vibe Tools 快速发布脚本

set -e

echo "🚀 Vibe Tools 发布助手"
echo "================================"

# 检查是否有待发布的文件
if [ ! -d "dist" ] || [ -z "$(ls -A dist 2>/dev/null)" ]; then
    echo "❌ 没有找到待发布的包，请先运行: python -m build"
    exit 1
fi

echo "📦 找到以下包文件:"
ls -la dist/

echo ""
echo "📋 选择发布选项:"
echo "1. 发布到 TestPyPI (测试)"
echo "2. 发布到正式 PyPI"
echo "3. 仅检查包质量"
echo "4. 退出"

read -p "请选择 (1-4): " choice

case $choice in
    1)
        echo "🧪 发布到 TestPyPI..."
        echo "请确保您已设置环境变量:"
        echo "export TWINE_USERNAME=__token__"
        echo "export TWINE_PASSWORD=your-pypi-token"
        echo ""
        read -p "按回车继续，或 Ctrl+C 退出..." -r
        twine upload --repository testpypi dist/*
        echo ""
        echo "✅ 发布到 TestPyPI 完成！"
        echo "🧪 测试安装:"
        echo "pip install --index-url https://test.pypi.org/simple/ vibe-tools"
        ;;
    2)
        echo "🚀 发布到正式 PyPI..."
        echo "⚠️  警告：这将发布到正式 PyPI！"
        echo "请确保您已设置环境变量:"
        echo "export TWINE_USERNAME=__token__"
        echo "export TWINE_PASSWORD=your-pypi-token"
        echo ""
        read -p "确认发布到正式 PyPI? (y/N): " -r confirm
        if [[ $confirm =~ ^[Yy]$ ]]; then
            twine upload dist/*
            echo ""
            echo "✅ 发布到正式 PyPI 完成！"
            echo "🎯 用户现在可以使用:"
            echo "  uvx vibe-tools"
            echo "  pip install vibe-tools"
        else
            echo "❌ 发布已取消"
        fi
        ;;
    3)
        echo "🔍 检查包质量..."
        twine check dist/*
        echo "✅ 包质量检查完成"
        ;;
    4)
        echo "👋 退出发布助手"
        exit 0
        ;;
    *)
        echo "❌ 无效选择"
        exit 1
        ;;
esac

echo ""
echo "📊 发布后状态:"
echo "  - TestPyPI: https://test.pypi.org/project/vibe-tools/"
echo "  - 正式 PyPI: https://pypi.org/project/vibe-tools/"