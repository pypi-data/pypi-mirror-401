#!/usr/bin/env python3
"""
Vibe Tools 主入口点 - 支持直接运行和 uvx
"""

import sys

def main():
    """主入口函数"""
    try:
        # 导入并运行主模块
        import src.vibe_tools.cli as cli_module
        cli_module.main()
    except ImportError:
        # 如果无法导入模块，尝试相对导入
        sys.path.insert(0, '..')
        try:
            import vibe_tools.cli as cli_module
            cli_module.main()
        except ImportError as e:
            print(f"❌ 无法导入 vibe_tools: {e}")
            print("请确保您在正确的目录中运行或已正确安装")
            sys.exit(1)

if __name__ == "__main__":
    main()