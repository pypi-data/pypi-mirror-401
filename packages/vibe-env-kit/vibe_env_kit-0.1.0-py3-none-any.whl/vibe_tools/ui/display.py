"""Rich 显示组件 - 提供美观的终端界面"""

from typing import List, Optional, Tuple
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.layout import Layout
from rich.align import Align
from rich.columns import Columns


class DisplayManager:
    """终端显示管理器"""
    
    def __init__(self, console: Optional[Console] = None):
        self.console = console or Console()
    
    def show_banner(self, title: str, subtitle: str = "") -> None:
        """显示程序标题横幅"""
        banner_text = Text()
        banner_text.append("╔", style="bright_blue")
        banner_text.append("═" * 70, style="bright_blue")
        banner_text.append("╗\n", style="bright_blue")
        banner_text.append("║", style="bright_blue")
        banner_text.append(" " * 28, style="default")
        banner_text.append(title, style="bold blue")
        banner_text.append(" " * (28 - len(title)), style="default")
        banner_text.append("║\n", style="bright_blue")
        
        if subtitle:
            banner_text.append("║", style="bright_blue")
            banner_text.append(" " * (35 - len(subtitle)//2), style="default")
            banner_text.append(subtitle, style="cyan")
            banner_text.append(" " * (35 - len(subtitle)//2), style="default")
            banner_text.append("║\n", style="bright_blue")
        
        banner_text.append("╚", style="bright_blue")
        banner_text.append("═" * 70, style="bright_blue")
        banner_text.append("╝", style="bright_blue")
        
        panel = Panel(
            banner_text,
            border_style="bright_blue",
            padding=(0, 0)
        )
        self.console.print(panel)
    
    def show_main_menu(self, system_info: Optional[dict] = None) -> None:
        """显示主菜单界面"""
        self.show_banner("🛠️  Vibe Tools", "零配置开发环境管理器")
        
        # 创建菜单表格
        table = Table(show_header=False, box=None, expand=True)
        table.add_column("category", style="bold cyan", width=40)
        table.add_column("options", style="white")
        
        # 快速开始
        table.add_row(
            "🚀 快速开始",
            "[bold]1.[/bold] 初始化开发环境\n"
            "[bold]2.[/bold] 导入配置文件\n"
            "[bold]3.[/bold] 检测系统状态"
        )
        
        # 工具管理
        table.add_row(
            "📦 工具管理",
            "[bold]4.[/bold] 安装开发工具\n"
            "[bold]5.[/bold] 更新工具链\n"
            "[bold]6.[/bold] 卸载工具"
        )
        
        # AI 工具
        table.add_row(
            "🤖 AI 工具",
            "[bold]7.[/bold] Claude Code 配置\n"
            "[bold]8.[/bold] GitHub Copilot\n"
            "[bold]9.[/bold] Cursor Editor"
        )
        
        # 系统配置
        table.add_row(
            "⚙️  系统配置",
            "[bold]0.[/bold] Shell 环境配置\n"
            "[bold]S.[/bold] 切换代码工具\n"
            "[bold]C.[/bold] 配置默认模型"
        )
        
        panel = Panel(
            table,
            title="[bold blue]主菜单[/bold blue]",
            border_style="blue",
            padding=(1, 2)
        )
        self.console.print(panel)
        
        # 操作提示
        help_text = "[dim]↑↓ 移动 | Enter 选择 | q 退出 | h 帮助[/dim]"
        self.console.print(Align.center(help_text))
    
    def show_tool_selection(self, category: str, tools: List[dict], 
                          selected: List[bool]) -> None:
        """显示工具选择界面"""
        title = f"📦 {category} 工具选择"
        self.show_banner(title)
        
        # 系统信息
        if category == "开发工具":
            info_text = "🔍 检测到您的系统：macOS + zsh + Python 3.12"
            self.console.print(f"[cyan]{info_text}[/cyan]\n")
        
        # 创建工具选择表格
        table = Table(show_header=True, box=None)
        table.add_column("", width=3)  # 选择框
        table.add_column("工具名称", style="bold", width=25)
        table.add_column("描述", style="dim", width=40)
        table.add_column("状态", width=10)
        
        for i, tool in enumerate(tools):
            checkbox = "✓" if selected[i] else "□"
            name = tool.get("name", "Unknown")
            desc = tool.get("description", "暂无描述")
            status = tool.get("status", "未安装")
            
            status_style = "green" if status == "已安装" else "yellow"
            
            table.add_row(
                f"[bold]{checkbox}[/bold]",
                name,
                desc,
                f"[{status_style}]{status}[/{status_style}]"
            )
        
        panel = Panel(
            table,
            title=f"[bold blue]{category}[/bold blue]",
            border_style="blue",
            padding=(1, 2)
        )
        self.console.print(panel)
        
        # 操作提示
        help_text = "[dim]空格 切换选择 | a 全选 | n 全不选 | Enter 确认 | q 返回[/dim]"
        self.console.print(Align.center(help_text))
    
    def show_status(self, status_data: dict) -> None:
        """显示系统状态"""
        self.show_banner("📊 系统状态", "Environment Information")
        
        # 创建状态表格
        table = Table(title="系统信息", box=None)
        table.add_column("项目", style="bold cyan")
        table.add_column("值", style="white")
        
        # 系统信息
        for key, value in status_data.get("system", {}).items():
            table.add_row(key, str(value))
        
        panel = Panel(
            table,
            title="[bold blue]系统信息[/bold blue]",
            border_style="blue",
            padding=(1, 2)
        )
        self.console.print(panel)
    
    def show_progress(self, message: str, progress: float = None) -> None:
        """显示进度信息"""
        if progress is not None:
            from rich.progress import Progress, BarColumn, TextColumn
            
            with Progress(
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                console=self.console
            ) as progress_bar:
                task = progress_bar.add_task(message, total=100)
                progress_bar.update(task, completed=progress)
        else:
            self.console.print(f"[blue]⏳ {message}...[/blue]")
    
    def show_success(self, message: str) -> None:
        """显示成功消息"""
        self.console.print(f"[bold green]✅ {message}[/bold green]")
    
    def show_error(self, message: str) -> None:
        """显示错误消息"""
        self.console.print(f"[bold red]❌ {message}[/bold red]")
    
    def show_warning(self, message: str) -> None:
        """显示警告消息"""
        self.console.print(f"[bold yellow]⚠️  {message}[/bold yellow]")
    
    def prompt_user(self, question: str) -> str:
        """提示用户输入"""
        return self.console.input(f"[bold blue]❓ {question}[/bold blue]: ")
    
    def confirm(self, question: str) -> bool:
        """确认对话框"""
        return self.console.confirm(f"[bold yellow]{question}[/bold yellow]")