"""CLI 主入口 - 使用 Click 框架实现命令行界面"""

import sys
from typing import Optional

import click
from rich.console import Console

from . import __version__

# 全局 Rich Console 实例
console = Console()


def print_version(ctx: click.Context, param: click.Parameter, value: bool) -> None:
    """显示版本信息并退出"""
    if value:
        console.print(f"vibe-tools version [bold green]{__version__}[/bold green]")
        ctx.exit()


@click.group()
@click.option(
    "--version",
    is_flag=True,
    callback=print_version,
    expose_value=False,
    is_eager=True,
    help="显示版本信息并退出",
)
@click.option(
    "--verbose", "-v",
    is_flag=True,
    help="启用详细输出模式",
)
@click.option(
    "--config",
    type=click.Path(exists=True, dir_okay=False, readable=True),
    help="指定配置文件路径",
)
@click.option(
    "--dry-run",
    is_flag=True,
    help="预览模式，不执行实际操作",
)
@click.pass_context
def cli(ctx: click.Context, verbose: bool, config: Optional[str], dry_run: bool) -> None:
    """
    🛠️  Vibe Tools - 零配置开发环境管理器
    
    现代化的 CLI 环境配置工具，通过 uvx 运行，提供交互式菜单界面。
    
    支持各种开发工具的自动安装和配置，包括 Python、Node.js、Git、Docker 等。
    """
    # 确保上下文对象存在
    ctx.ensure_object(dict)
    
    # 存储全局选项
    ctx.obj["verbose"] = verbose
    ctx.obj["config"] = config
    ctx.obj["dry_run"] = dry_run
    
    if verbose:
        console.print("🚀 [bold blue]Vibe Tools[/bold blue] 启动中...")
        if config:
            console.print(f"📄 使用配置文件: {config}")
        if dry_run:
            console.print("🔍 [yellow]预览模式[/yellow] - 不会执行实际操作")


@cli.command()
@click.pass_context
def init(ctx: click.Context) -> None:
    """初始化开发环境配置"""
    console.print("🔧 [bold blue]初始化开发环境配置[/bold blue]")
    
    # TODO: 实现初始化逻辑
    console.print("⚠️  功能开发中...")


@cli.command()
@click.argument("tools", nargs=-1, required=False)
@click.option(
    "--interactive", "-i",
    is_flag=True,
    default=True,
    help="启动交互式工具选择界面",
)
@click.pass_context
def install(ctx: click.Context, tools: tuple, interactive: bool) -> None:
    """安装开发工具"""
    if interactive and not tools:
        # TODO: 启动交互式菜单
        console.print("🎯 [bold blue]启动交互式工具选择界面[/bold blue]")
        console.print("⚠️  功能开发中...")
    elif tools:
        console.print(f"📦 安装工具: {', '.join(tools)}")
        # TODO: 实现直接安装逻辑
        console.print("⚠️  功能开发中...")
    else:
        console.print("❌ 请指定要安装的工具或使用交互式模式")
        sys.exit(1)


@cli.command()
@click.pass_context
def update(ctx: click.Context) -> None:
    """更新已安装的工具"""
    console.print("🔄 [bold blue]更新已安装的工具[/bold blue]")
    # TODO: 实现更新逻辑
    console.print("⚠️  功能开发中...")


@cli.command()
@click.pass_context
def list(ctx: click.Context) -> None:
    """列出已安装的工具"""
    console.print("📋 [bold blue]已安装的工具列表[/bold blue]")
    # TODO: 实现列表逻辑
    console.print("⚠️  功能开发中...")


@cli.command()
@click.option(
    "--global", "global_config",
    is_flag=True,
    help="编辑全局配置",
)
@click.pass_context
def config(ctx: click.Context, global_config: bool) -> None:
    """配置工具设置"""
    if global_config:
        console.print("⚙️  [bold blue]编辑全局配置[/bold blue]")
    else:
        console.print("⚙️  [bold blue]编辑项目配置[/bold blue]")
    
    # TODO: 实现配置逻辑
    console.print("⚠️  功能开发中...")


@cli.command()
@click.pass_context
def status(ctx: click.Context) -> None:
    """显示系统状态和环境信息"""
    console.print("📊 [bold blue]系统状态和环境信息[/bold blue]")
    
    # TODO: 实现状态检查逻辑
    console.print("⚠️  功能开发中...")


def main() -> None:
    """主入口函数 - 如果没有参数，默认启动交互式菜单"""
    try:
        # 如果没有提供任何参数，启动交互式菜单
        if len(sys.argv) == 1:
            from .ui.menu import show_main_menu
            
            while True:
                choice = show_main_menu(console)
                if choice in ['q', 'Q']:
                    console.print("👋 [yellow]退出 Vibe Tools[/yellow]")
                    break
                elif choice:
                    from .ui.menu import handle_menu_selection
                    handle_menu_selection(choice, console)
        else:
            # 有参数时，正常执行 CLI 命令
            cli()
            
    except KeyboardInterrupt:
        console.print("\n👋 [yellow]操作已取消[/yellow]")
        sys.exit(1)
    except Exception as e:
        console.print(f"❌ [red]错误: {e}[/red]")
        # 如果是详细模式，显示堆栈
        if len(sys.argv) > 1 and ("-v" in sys.argv or "--verbose" in sys.argv):
            import traceback
            console.print(traceback.format_exc())
        sys.exit(1)


if __name__ == "__main__":
    main()