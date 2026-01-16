"""Vibe Tools - 零配置开发环境管理器"""

__version__ = "0.1.0"
__author__ = "Vibe Tools Team"
__description__ = "现代化的 CLI 环境配置工具，通过 uvx 运行，提供交互式菜单界面"

from .cli import main

__all__ = ["main", "__version__"]