"""交互式菜单界面 - 类似 ZCF 的用户体验"""

import sys
from typing import Dict, List, Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.align import Align

console = Console()


def show_main_menu(console: Console) -> str:
    """显示主菜单并获取用户选择"""
    
    # 清屏
    console.clear()
    
    # 标题横幅
    banner_text = Text()
    banner_text.append("╔", style="bright_blue")
    banner_text.append("═" * 62, style="bright_blue")
    banner_text.append("╗\n", style="bright_blue")
    banner_text.append("║", style="bright_blue")
    banner_text.append(" " * 23, style="default")
    banner_text.append("🛠️  Vibe Tools", style="bold blue")
    banner_text.append(" " * 25, style="default")
    banner_text.append("║\n", style="bright_blue")
    banner_text.append("║", style="bright_blue")
    banner_text.append(" " * 20, style="default")
    banner_text.append("零配置开发环境管理器", style="cyan")
    banner_text.append(" " * 20, style="default")
    banner_text.append("║\n", style="bright_blue")
    banner_text.append("║", style="bright_blue")
    banner_text.append(" " * 16, style="default")
    banner_text.append("Zero-Config Development Environment Manager", style="dim cyan")
    banner_text.append(" " * 13, style="default")
    banner_text.append("║\n", style="bright_blue")
    banner_text.append("╚", style="bright_blue")
    banner_text.append("═" * 62, style="bright_blue")
    banner_text.append("╝", style="bright_blue")
    
    panel = Panel(
        banner_text,
        border_style="bright_blue",
        padding=(0, 0)
    )
    console.print(panel)
    
    # 菜单选项表格
    table = Table(show_header=False, box=None, expand=True)
    table.add_column("category", style="bold cyan", width=35)
    table.add_column("options", style="white")
    
    # 快速开始
    table.add_row(
        "🚀 快速开始",
        "[bold]1.[/bold] 完整初始化 - 安装开发环境 + 导入工作流 + 配置 API\n"
        "[bold]2.[/bold] 导入工作流 - 仅导入/更新工作流相关文件\n"
        "[bold]3.[/bold] 配置 API 或 CCR 代理 - 配置 API URL、认证信息\n"
    )
    
    # 工具管理
    table.add_row(
        "📦 工具管理",
        "[bold]4.[/bold] 安装开发工具 - Python、Node.js、Git、Docker 等\n"
        "[bold]5.[/bold] 更新工具链 - 更新已安装的开发工具\n"
        "[bold]6.[/bold] 卸载工具 - 从系统中移除开发工具\n"
    )
    
    # AI 工具
    table.add_row(
        "🤖 AI 工具",
        "[bold]7.[/bold] Claude Code 配置 - 配置 Claude Code 环境\n"
        "[bold]8.[/bold] GitHub Copilot - 配置 GitHub Copilot CLI\n"
        "[bold]9.[/bold] Cursor Editor - 配置 Cursor 编辑器\n"
    )
    
    # 系统配置
    table.add_row(
        "⚙️  系统配置",
        "[bold]0.[/bold] Shell 环境配置 - 配置 Shell 和环境变量\n"
        "[bold]S.[/bold] 切换代码工具 - 在支持的代码工具间切换\n"
        "[bold]C.[/bold] 配置默认模型 - 设置默认 AI 模型\n"
    )
    
    # 其他选项
    table.add_row(
        "🔧 其他选项",
        "[bold]-.[/bold] 卸载和删除配置 - 从系统删除 Vibe Tools\n"
        "[bold]+.[/bold] 检查更新 - 检查并更新工具版本\n"
        "[bold]Q.[/bold] 退出程序 - 退出 Vibe Tools\n"
    )
    
    menu_panel = Panel(
        table,
        title="[bold blue]请选择功能[/bold blue]",
        border_style="blue",
        padding=(1, 2)
    )
    console.print(menu_panel)
    
    # 操作提示
    help_text = "[dim]请输入选项，回车确认（不区分大小写）[/dim]"
    console.print(Align.center(help_text))
    
    # 获取用户输入
    try:
        choice = console.input("[bold blue]❓ 请选择:[/bold blue] ").strip()
        return choice
    except (KeyboardInterrupt, EOFError):
        return 'q'


def handle_menu_selection(choice: str, console: Console) -> None:
    """处理菜单选择"""
    
    if choice == '1':
        console.print("🚀 [bold blue]完整初始化开发环境[/bold blue]")
        console.print("⚠️  [yellow]功能开发中，敬请期待...[/yellow]")
        
    elif choice == '2':
        console.print("📥 [bold blue]导入工作流配置[/bold blue]")
        console.print("⚠️  [yellow]功能开发中，敬请期待...[/yellow]")
        
    elif choice == '3':
        console.print("🔗 [bold blue]配置 API 或 CCR 代理[/bold blue]")
        console.print("⚠️  [yellow]功能开发中，敬请期待...[/yellow]")
        
    elif choice == '4':
        show_tool_selection_menu(console)
        
    elif choice == '5':
        console.print("🔄 [bold blue]更新工具链[/bold blue]")
        console.print("⚠️  [yellow]功能开发中，敬请期待...[/yellow]")
        
    elif choice == '6':
        console.print("🗑️  [bold blue]卸载工具[/bold blue]")
        console.print("⚠️  [yellow]功能开发中，敬请期待...[/yellow]")
        
    elif choice == '7':
        console.print("🤖 [bold blue]Claude Code 配置[/bold blue]")
        console.print("⚠️  [yellow]功能开发中，敬请期待...[/yellow]")
        
    elif choice == '8':
        console.print("🐙 [bold blue]GitHub Copilot 配置[/bold blue]")
        console.print("⚠️  [yellow]功能开发中，敬请期待...[/yellow]")
        
    elif choice == '9':
        console.print("⚡ [bold blue]Cursor Editor 配置[/bold blue]")
        console.print("⚠️  [yellow]功能开发中，敬请期待...[/yellow]")
        
    elif choice == '0':
        console.print("⚙️  [bold blue]Shell 环境配置[/bold blue]")
        console.print("⚠️  [yellow]功能开发中，敬请期待...[/yellow]")
        
    elif choice.lower() == 's':
        console.print("🔄 [bold blue]切换代码工具[/bold blue]")
        console.print("⚠️  [yellow]功能开发中，敬请期待...[/yellow]")
        
    elif choice.lower() == 'c':
        console.print("🎯 [bold blue]配置默认模型[/bold blue]")
        console.print("⚠️  [yellow]功能开发中，敬请期待...[/yellow]")
        
    elif choice == '-':
        console.print("🗑️  [bold blue]卸载和删除配置[/bold blue]")
        console.print("⚠️  [yellow]功能开发中，敬请期待...[/yellow]")
        
    elif choice == '+':
        console.print("🔍 [bold blue]检查更新[/bold blue]")
        console.print("⚠️  [yellow]功能开发中，敬请期待...[/yellow]")
        
    else:
        console.print(f"❌ [red]未知选项: {choice}[/red]")


def show_tool_selection_menu(console: Console) -> None:
    """显示工具选择菜单"""
    
    console.clear()
    console.print("📦 [bold blue]开发工具安装向导[/bold blue]")
    console.print("━" * 70)
    
    # 实际系统检测
    from ..core.detector import SystemDetector
    from ..core.installer import create_installer
    
    detector = SystemDetector()
    installer = create_installer(console)
    
    # 显示系统信息
    system_summary = detector.get_profile_summary()
    console.print(f"🔍 [cyan]检测到您的系统：{system_summary}[/cyan]")
    console.print()
    
    # 工具选择表格
    table = Table(show_header=True)
    table.add_column("选择", width=6)
    table.add_column("工具名称", style="bold", width=20)
    table.add_column("描述", width=35)
    table.add_column("状态", width=12)
    
    # 获取真实工具状态
    tools_status = installer.list_tools_status()
    tools = [
        ("□", "uv", "现代 Python 包管理器", tools_status.get("uv", "未安装")),
        ("□", "poetry", "Python 依赖管理工具", tools_status.get("poetry", "未安装")),
        ("□", "nodejs", "Node.js 运行环境", tools_status.get("nodejs", "未安装")),
        ("□", "git", "分布式版本控制", tools_status.get("git", "未安装")),
    ]
    
    for checkbox, name, desc, status in tools:
        status_style = "green" if "已安装" in status else "yellow"
        table.add_row(f"[bold]{checkbox}[/bold]", name, desc, f"[{status_style}]{status}[/{status_style}]")
    
    panel = Panel(
        table,
        title="[bold blue]推荐工具包[/bold blue]",
        border_style="blue",
        padding=(1, 2)
    )
    console.print(panel)
    
    # 推荐安装
    missing_tools = [name for name, status in tools if "未安装" in status]
    if missing_tools:
        console.print(f"💡 [dim]推荐安装: {', '.join(missing_tools)}[/dim]")
    
    # 操作提示
    help_text = "[dim][输入工具名] 安装特定工具 | [a 全部安装] [q 返回主菜单][/dim]"
    console.print(Align.center(help_text))
    
    # 获取用户输入
    try:
        choice = console.input("[bold blue]❓ 请选择工具或操作:[/bold blue] ").strip().lower()
        
        if choice.lower() == 'q':
            return
        elif choice.lower() == 'a':
            # 安装所有缺失的工具
            _install_missing_tools(missing_tools, installer, console)
        elif choice in [name for _, name, _, _ in tools]:
            # 安装单个工具
            _install_single_tool(choice, installer, console)
        else:
            console.print(f"❌ [red]未知选择: {choice}[/red]")
            
    except (KeyboardInterrupt, EOFError):
        return


def _install_missing_tools(tool_names: List[str], installer, console: Console) -> None:
    """安装缺失的工具"""
    if not tool_names:
        console.print("✅ [green]所有工具都已安装！[/green]")
        return
    
    console.print(f"🔄 [blue]开始安装: {', '.join(tool_names)}[/blue]")
    console.print()
    
    results = installer.install_tools(tool_names)
    
    console.print("\n📊 [bold]安装结果:[/bold]")
    for tool_name, result in results.items():
        if result.success:
            console.print(f"  ✅ [green]{tool_name}[/green]: {result.message}")
        else:
            console.print(f"  ❌ [red]{tool_name}[/red]: {result.message}")
    
    console.print("\n💡 [dim]请重启终端以使环境变量生效[/dim]")


def _install_single_tool(tool_name: str, installer, console: Console) -> None:
    """安装单个工具"""
    console.print(f"🔄 [blue]开始安装 {tool_name}...[/blue]")
    
    results = installer.install_tools([tool_name])
    result = results[tool_name]
    
    if result.success:
        console.print(f"✅ [green]{tool_name} 安装成功![/green]")
        if result.details:
            console.print(f"   [dim]{result.details}[/dim]")
    else:
        console.print(f"❌ [red]{tool_name} 安装失败:[/red]")
        console.print(f"   [dim]{result.message}[/dim]")
        if result.details:
            console.print(f"   [dim]{result.details}[/dim]")
    
    console.print("\n💡 [dim]请重启终端以使环境变量生效[/dim]")


def pause_and_continue(console: Console) -> None:
    """暂停并等待用户继续"""
    try:
        console.input("\n[dim]按回车键继续...[/dim]")
    except (KeyboardInterrupt, EOFError):
        pass