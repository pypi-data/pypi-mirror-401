"""工具安装器 - 负责各种开发工具的安装逻辑"""

import os
import subprocess
import shutil
from typing import Dict, List, Optional, Callable, Any
from abc import ABC, abstractmethod
from dataclasses import dataclass

from rich.console import Console
from rich.progress import Progress, BarColumn, TextColumn, TaskID


@dataclass
class InstallResult:
    """安装结果"""
    success: bool
    message: str
    details: Optional[str] = None


class BaseTool(ABC):
    """工具基类 - 所有工具安装器的基础类"""
    
    def __init__(self, console: Console):
        self.console = console
        self.name = ""
        self.description = ""
        self.install_commands = []
        self.verify_commands = []
        self.dependencies = []
    
    @abstractmethod
    def detect(self) -> bool:
        """检测工具是否已安装"""
        pass
    
    @abstractmethod
    def install(self) -> InstallResult:
        """安装工具"""
        pass
    
    @abstractmethod
    def verify(self) -> bool:
        """验证安装是否成功"""
        pass
    
    def get_status(self) -> str:
        """获取安装状态"""
        if self.detect():
            version = self._get_version()
            return f"已安装 ({version})" if version else "已安装"
        return "未安装"
    
    def _get_version(self) -> Optional[str]:
        """获取工具版本"""
        if not self.verify_commands:
            return None
        
        try:
            result = subprocess.run(
                self.verify_commands[0].split(),
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                return self._parse_version(result.stdout.strip() or result.stderr.strip())
        except (subprocess.TimeoutExpired, subprocess.SubprocessError):
            pass
        
        return None
    
    def _parse_version(self, output: str) -> str:
        """解析版本信息"""
        import re
        match = re.search(r'(\d+\.\d+(?:\.\d+)?)', output)
        return match.group(1) if match else "unknown"


class UVTool(BaseTool):
    """UV 包管理器"""
    
    def __init__(self, console: Console):
        super().__init__(console)
        self.name = "uv"
        self.description = "现代 Python 包管理器"
        self.install_commands = [
            "curl -LsSf https://astral.sh/uv/install.sh | sh",
        ]
        self.verify_commands = ["uv --version"]
    
    def detect(self) -> bool:
        return shutil.which("uv") is not None
    
    def install(self) -> InstallResult:
        if self.detect():
            return InstallResult(True, "UV 已安装")
        
        try:
            self.console.print("📦 [blue]安装 UV Python 包管理器...[/blue]")
            
            result = subprocess.run(
                self.install_commands[0],
                shell=True,
                capture_output=True,
                text=True,
                timeout=300  # 5分钟超时
            )
            
            if result.returncode == 0:
                # 添加到 PATH
                self._add_to_path("$HOME/.cargo/bin")
                return InstallResult(True, "UV 安装成功！请重启终端或运行 source ~/.bashrc")
            else:
                return InstallResult(False, "UV 安装失败", result.stderr)
                
        except subprocess.TimeoutExpired:
            return InstallResult(False, "UV 安装超时")
        except Exception as e:
            return InstallResult(False, f"UV 安装出错: {str(e)}")
    
    def verify(self) -> bool:
        return shutil.which("uv") is not None
    
    def _add_to_path(self, path: str) -> None:
        """添加路径到环境变量"""
        shell_files = [
            os.path.expanduser("~/.bashrc"),
            os.path.expanduser("~/.zshrc"),
            os.path.expanduser("~/.profile"),
        ]
        
        for shell_file in shell_files:
            if os.path.exists(shell_file):
                with open(shell_file, "r") as f:
                    content = f.read()
                
                if f"export PATH={path}" not in content:
                    with open(shell_file, "a") as f:
                        f.write(f"\nexport PATH={path}:$PATH\n")


class PoetryTool(BaseTool):
    """Poetry 依赖管理器"""
    
    def __init__(self, console: Console):
        super().__init__(console)
        self.name = "poetry"
        self.description = "Python 依赖管理工具"
        self.install_commands = [
            "curl -sSL https://install.python-poetry.org | python3 -",
        ]
        self.verify_commands = ["poetry --version"]
    
    def detect(self) -> bool:
        return shutil.which("poetry") is not None
    
    def install(self) -> InstallResult:
        if self.detect():
            return InstallResult(True, "Poetry 已安装")
        
        try:
            self.console.print("📦 [blue]安装 Poetry 依赖管理器...[/blue]")
            
            result = subprocess.run(
                self.install_commands[0],
                shell=True,
                capture_output=True,
                text=True,
                timeout=300
            )
            
            if result.returncode == 0:
                return InstallResult(True, "Poetry 安装成功！请重启终端")
            else:
                return InstallResult(False, "Poetry 安装失败", result.stderr)
                
        except subprocess.TimeoutExpired:
            return InstallResult(False, "Poetry 安装超时")
        except Exception as e:
            return InstallResult(False, f"Poetry 安装出错: {str(e)}")
    
    def verify(self) -> bool:
        return shutil.which("poetry") is not None


class NodeTool(BaseTool):
    """Node.js 版本管理器 (通过 nvm)"""
    
    def __init__(self, console: Console):
        super().__init__(console)
        self.name = "nodejs"
        self.description = "JavaScript 运行时环境"
        self.install_commands = [
            "curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash",
            "source ~/.bashrc",
            "nvm install --lts",
        ]
        self.verify_commands = ["node --version", "npm --version"]
    
    def detect(self) -> bool:
        return (shutil.which("node") is not None) and (shutil.which("npm") is not None)
    
    def install(self) -> InstallResult:
        if self.detect():
            return InstallResult(True, "Node.js 已安装")
        
        try:
            self.console.print("📦 [blue]安装 Node.js (通过 NVM)...[/blue]")
            
            # 安装 NVM
            result1 = subprocess.run(
                self.install_commands[0],
                shell=True,
                capture_output=True,
                text=True,
                timeout=300
            )
            
            if result1.returncode != 0:
                return InstallResult(False, "NVM 安装失败", result1.stderr)
            
            # 安装 Node.js LTS
            result2 = subprocess.run(
                "bash -c 'source ~/.bashrc && nvm install --lts'",
                shell=True,
                capture_output=True,
                text=True,
                timeout=600
            )
            
            if result2.returncode == 0:
                return InstallResult(True, "Node.js 安装成功！请重启终端")
            else:
                return InstallResult(False, "Node.js 安装失败", result2.stderr)
                
        except subprocess.TimeoutExpired:
            return InstallResult(False, "Node.js 安装超时")
        except Exception as e:
            return InstallResult(False, f"Node.js 安装出错: {str(e)}")
    
    def verify(self) -> bool:
        return (shutil.which("node") is not None) and (shutil.which("npm") is not None)


class GitTool(BaseTool):
    """Git 版本控制"""
    
    def __init__(self, console: Console):
        super().__init__(console)
        self.name = "git"
        self.description = "分布式版本控制系统"
        self.install_commands = self._get_install_command()
        self.verify_commands = ["git --version"]
    
    def _get_install_command(self) -> List[str]:
        """根据操作系统获取安装命令"""
        system = os.uname().sysname.lower()
        
        if system == "darwin":
            # macOS 使用 Homebrew
            return ["brew install git"]
        elif system == "linux":
            # Linux 使用包管理器
            if shutil.which("apt-get"):
                return ["sudo apt-get update && sudo apt-get install -y git"]
            elif shutil.which("yum"):
                return ["sudo yum install -y git"]
            elif shutil.which("dnf"):
                return ["sudo dnf install -y git"]
            else:
                return ["sudo apt-get update && sudo apt-get install -y git"]
        else:
            # Windows 或其他系统
            return ["echo '请从 https://git-scm.com 下载安装 Git'"]
    
    def detect(self) -> bool:
        return shutil.which("git") is not None
    
    def install(self) -> InstallResult:
        if self.detect():
            return InstallResult(True, "Git 已安装")
        
        try:
            self.console.print("📦 [blue]安装 Git 版本控制系统...[/blue]")
            
            cmd = self.install_commands[0]
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=300
            )
            
            if result.returncode == 0:
                return InstallResult(True, "Git 安装成功！")
            else:
                return InstallResult(False, "Git 安装失败", result.stderr)
                
        except subprocess.TimeoutExpired:
            return InstallResult(False, "Git 安装超时")
        except Exception as e:
            return InstallResult(False, f"Git 安装出错: {str(e)}")
    
    def verify(self) -> bool:
        return shutil.which("git") is not None


class ToolInstaller:
    """工具安装器管理器"""
    
    def __init__(self, console: Console):
        self.console = console
        self.tools = {
            "uv": UVTool(console),
            "poetry": PoetryTool(console),
            "nodejs": NodeTool(console),
            "git": GitTool(console),
        }
    
    def get_available_tools(self) -> Dict[str, BaseTool]:
        """获取可用工具列表"""
        return self.tools
    
    def get_tool_status(self, tool_name: str) -> str:
        """获取工具状态"""
        if tool_name not in self.tools:
            return "未知工具"
        return self.tools[tool_name].get_status()
    
    def install_tools(self, tool_names: List[str]) -> Dict[str, InstallResult]:
        """批量安装工具"""
        results = {}
        
        for tool_name in tool_names:
            if tool_name not in self.tools:
                results[tool_name] = InstallResult(False, f"未知工具: {tool_name}")
                continue
            
            tool = self.tools[tool_name]
            
            # 检查是否已安装
            if tool.detect():
                results[tool_name] = InstallResult(True, f"{tool_name} 已安装")
                continue
            
            # 执行安装
            with Progress(
                TextColumn(f"[progress.description]{tool_name} 安装..."),
                BarColumn(),
                console=self.console,
                transient=True
            ) as progress:
                task = progress.add_task(f"安装 {tool_name}...", total=100)
                
                results[tool_name] = tool.install()
                
                progress.update(task, completed=100)
        
        return results
    
    def get_recommendations(self) -> Dict[str, List[str]]:
        """获取工具推荐"""
        return {
            "Python 开发": ["uv", "poetry"],
            "Web 开发": ["nodejs", "git"],
            "基础开发": ["git", "uv"],
            "全栈开发": ["uv", "poetry", "nodejs", "git"],
        }
    
    def list_tools_status(self) -> Dict[str, str]:
        """列出所有工具状态"""
        return {name: tool.get_status() for name, tool in self.tools.items()}


def create_installer(console: Console) -> ToolInstaller:
    """创建安装器实例"""
    return ToolInstaller(console)