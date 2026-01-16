"""系统环境检测器 - 检测操作系统、Shell、已安装工具等"""

import os
import platform
import shutil
import subprocess
from typing import Dict, List, Optional, Tuple


class SystemDetector:
    """系统环境检测器"""
    
    def __init__(self):
        self.system_info = {}
        self.installed_tools = {}
        self._detect_system()
        self._detect_tools()
    
    def _detect_system(self) -> None:
        """检测系统基础信息"""
        self.system_info = {
            "os": platform.system(),
            "version": platform.version(),
            "arch": platform.machine(),
            "python_version": platform.python_version(),
            "shell": self._detect_shell(),
            "home_dir": os.path.expanduser("~"),
        }
    
    def _detect_shell(self) -> str:
        """检测当前 Shell"""
        shell = os.environ.get("SHELL", "")
        if shell:
            return shell.split("/")[-1]
        
        # Windows 检测
        if platform.system() == "Windows":
            return os.environ.get("COMSPEC", "cmd.exe")
        
        return "unknown"
    
    def _detect_tools(self) -> None:
        """检测已安装的开发工具"""
        tools_to_check = [
            # Python 工具
            ("python", "python --version"),
            ("pip", "pip --version"),
            ("uv", "uv --version"),
            ("poetry", "poetry --version"),
            ("pre-commit", "pre-commit --version"),
            ("ruff", "ruff --version"),
            
            # Node.js 工具
            ("node", "node --version"),
            ("npm", "npm --version"),
            ("nvm", "nvm --version"),
            ("pnpm", "pnpm --version"),
            ("yarn", "yarn --version"),
            
            # Git 工具
            ("git", "git --version"),
            ("git-lfs", "git lfs version"),
            ("gh", "gh --version"),
            
            # 容器化工具
            ("docker", "docker --version"),
            ("docker-compose", "docker-compose --version"),
            
            # 编辑器
            ("code", "code --version"),
            ("cursor", "cursor --version"),
            ("nvim", "nvim --version"),
            ("vim", "vim --version"),
            
            # 其他工具
            ("make", "make --version"),
            ("curl", "curl --version"),
            ("wget", "wget --version"),
        ]
        
        for tool_name, version_cmd in tools_to_check:
            self.installed_tools[tool_name] = self._check_tool(tool_name, version_cmd)
    
    def _check_tool(self, tool_name: str, version_cmd: str) -> Dict[str, str]:
        """检查单个工具是否安装并获取版本"""
        if not shutil.which(tool_name):
            return {"installed": False, "version": "", "path": ""}
        
        try:
            result = subprocess.run(
                version_cmd.split(),
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                version_output = result.stdout.strip() or result.stderr.strip()
                return {
                    "installed": True,
                    "version": self._parse_version(version_output),
                    "path": shutil.which(tool_name) or "",
                }
        except (subprocess.TimeoutExpired, subprocess.SubprocessError):
            pass
        
        return {
            "installed": True,
            "version": "unknown",
            "path": shutil.which(tool_name) or "",
        }
    
    def _parse_version(self, output: str) -> str:
        """解析版本信息"""
        # 简单的版本解析，提取第一个版本号模式
        import re
        
        version_patterns = [
            r'\d+\.\d+\.\d+',  # x.y.z
            r'\d+\.\d+',        # x.y
            r'v\d+\.\d+\.\d+', # vx.y.z
            r'version\s+\d+',    # version x
        ]
        
        for pattern in version_patterns:
            match = re.search(pattern, output, re.IGNORECASE)
            if match:
                return match.group()
        
        # 如果没有找到版本号，返回前几个词
        words = output.split()[:3]
        return " ".join(words)
    
    def get_system_info(self) -> Dict[str, str]:
        """获取系统信息"""
        return self.system_info
    
    def get_installed_tools(self) -> Dict[str, Dict[str, str]]:
        """获取已安装工具信息"""
        return self.installed_tools
    
    def is_tool_installed(self, tool_name: str) -> bool:
        """检查工具是否安装"""
        return self.installed_tools.get(tool_name, {}).get("installed", False)
    
    def get_missing_tools(self, required_tools: List[str]) -> List[str]:
        """获取缺失的工具列表"""
        return [tool for tool in required_tools if not self.is_tool_installed(tool)]
    
    def get_tool_recommendations(self) -> Dict[str, List[str]]:
        """获取工具推荐"""
        recommendations = {
            "python": ["uv", "poetry", "pre-commit", "ruff"],
            "nodejs": ["nvm", "npm", "pnpm"],
            "git": ["git", "git-lfs", "gh"],
            "containers": ["docker", "docker-compose"],
            "editors": ["code", "cursor"],
        }
        
        missing_by_category = {}
        for category, tools in recommendations.items():
            missing = self.get_missing_tools(tools)
            if missing:
                missing_by_category[category] = missing
        
        return missing_by_category
    
    def check_permissions(self) -> Dict[str, bool]:
        """检查系统权限"""
        return {
            "can_write_to_home": os.access(os.path.expanduser("~"), os.W_OK),
            "can_execute_commands": os.access("/bin", os.X_OK) if os.path.exists("/bin") else True,
            "internet_available": self._check_internet(),
        }
    
    def _check_internet(self) -> bool:
        """检查网络连接"""
        try:
            import urllib.request
            urllib.request.urlopen("https://pypi.org", timeout=3)
            return True
        except:
            return False
    
    def get_profile_summary(self) -> str:
        """获取系统配置摘要"""
        info = self.system_info
        tools_summary = sum(1 for tool in self.installed_tools.values() if tool["installed"])
        total_tools = len(self.installed_tools)
        
        return f"{info['os']} {info.get('arch', '')} + {info['shell']} + Python {info['python_version']}"
    
    def format_for_display(self) -> Dict[str, str]:
        """格式化信息用于显示"""
        return {
            "操作系统": f"{self.system_info['os']} {self.system_info['arch']}",
            "Shell": self.system_info['shell'],
            "Python版本": self.system_info['python_version'],
            "已安装工具": f"{sum(1 for t in self.installed_tools.values() if t['installed'])}/{len(self.installed_tools)}",
            "用户目录": self.system_info['home_dir'],
        }


def quick_scan() -> Dict[str, str]:
    """快速系统扫描"""
    detector = SystemDetector()
    return detector.format_for_display()


def detect_missing_tools(tool_list: List[str]) -> List[str]:
    """检测缺失的工具"""
    detector = SystemDetector()
    return detector.get_missing_tools(tool_list)