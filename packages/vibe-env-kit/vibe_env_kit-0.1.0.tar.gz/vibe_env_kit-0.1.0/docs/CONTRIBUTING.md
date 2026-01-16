# Vibe Tools 贡献指南

> "共建未来，让每个开发者都能享受零配置环境管理" - 欢迎贡献 Vibe Tools

## 🚀 贡献方式

### 快速开始

#### 一键贡献设置

```bash
# 克隆仓库
git clone https://github.com/your-username/vibe-tools.git
cd vibe-tools

# 安装开发依赖
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

# 运行测试
pytest
```

#### 开发环境验证

```bash
# 检查代码格式
black --check src/vibe_tools/

# 运行类型检查
mypy src/vibe_tools/

# 运行所有测试
pytest --cov=vibe_tools

# 验证包构建
python -m build
twine check dist/*
```

## 🏗️ 项目结构

### 目录组织

```
vibe_tools/
├── src/
│   └── vibe_tools/
│       ├── __init__.py           # 包初始化
│       ├── cli.py               # CLI 主入口
│       ├── core/                # 核心业务逻辑
│       │   ├── __init__.py
│       │   ├── detector.py       # 环境检测
│       │   ├── installer.py      # 工具安装
│       │   └── config.py         # 配置管理
│       ├── ui/                  # 用户界面
│       │   ├── __init__.py
│       │   ├── menu.py          # 交互式菜单
│       │   └── display.py       # 显示组件
│       ├── tools/               # 工具集成
│       │   ├── __init__.py
│       │   ├── base.py          # 工具基类
│       │   ├── dev_tools.py     # 开发工具
│       │   └── ai_tools.py      # AI 工具
│       └── utils/              # 工具函数
│           ├── __init__.py
│           ├── shell.py         # Shell 操作
│           └── file_ops.py      # 文件操作
├── tests/                     # 测试代码
│   ├── unit/                  # 单元测试
│   ├── integration/           # 集成测试
│   └── fixtures/             # 测试数据
├── docs/                      # 文档
│   ├── DESIGN.md              # 设计理念
│   ├── ARCHITECTURE.md        # 技术架构
│   ├── USAGE.md               # 使用指南
│   └── API.md                 # API 文档
├── scripts/                   # 脚本工具
│   ├── publish.sh             # 发布脚本
│   └── install.sh             # 安装脚本
└── examples/                  # 示例代码
    ├── custom_tools.py         # 自定义工具示例
    └── workflows/              # 工作流示例
```

### 代码风格

#### 格式化规范

我们使用以下工具确保代码质量：

```bash
# 代码格式化
black src/vibe_tools/
ruff check src/vibe_tools/

# 导入排序
isort src/vibe_tools/

# 类型检查
mypy src/vibe_tools/
```

#### 代码规范

```python
# 好的示例
class ToolInstaller:
    """工具安装器"""
    
    def __init__(self, console: Console) -> None:
        """初始化安装器"""
        self.console = console
        self.tools = {}
    
    def install_tools(self, tool_names: List[str]) -> Dict[str, InstallResult]:
        """批量安装工具
        
        Args:
            tool_names: 要安装的工具名称列表
            
        Returns:
            安装结果字典
        """
        results = {}
        for tool_name in tool_names:
            # 实现安装逻辑
            pass
        return results

# 避免的示例
class toolinstaller:
    def installtools(self, toolnames):
        # 变量名不够清晰
        pass
```

#### 注释规范

```python
# 函数注释 - 使用 docstring
def detect_system() -> Dict[str, str]:
    """检测系统基础信息
    
    Returns:
        包含系统信息的字典
    """
    pass

# 行内注释 - 解释复杂逻辑
if platform.system() == "Darwin":
    # macOS 使用 Homebrew 安装路径
    brew_path = "/opt/homebrew/bin"
else:
    # Linux 使用系统包管理器
    system_packages = ["apt", "yum", "dnf"]

# TODO 注释 - 标记待完成工作
# TODO: 实现 Windows 支持
def install_windows_tool():
    pass
```

## 🐛 问题修复

### Bug 报告流程

#### 报告前检查

1. **搜索现有 Issue** - 避免重复报告
2. **确认 Bug 环境** - 检查版本、系统信息
3. **最小复现** - 提供最小复现步骤
4. **预期行为** - 明确说明期望的结果

#### 报告格式

```markdown
## Bug 报告

### 基本信息
- **Vibe Tools 版本**: 0.1.0
- **操作系统**: macOS 14.0
- **Python 版本**: 3.12.0
- **安装方式**: uvx vibe-tools

### 问题描述
[简要描述遇到的问题]

### 复现步骤
1. 运行 `uvx vibe-tools`
2. 选择 `4` (安装开发工具)
3. 输入 `uv`
4. 观察错误信息

### 预期行为
[描述您期望发生的情况]

### 实际行为
[描述实际发生的情况，包括错误信息]

### 附加信息
[相关的配置文件、日志、截图等]
```

#### Bug 分类

- **P0**: 阻塞性 Bug，无法使用核心功能
- **P1**: 重要 Bug，影响主要工作流
- **P2**: 一般 Bug，有替代方案
- **P3**: 轻微 Bug，不影响主要功能

### 修复流程

```bash
# 1. 创建 Bug 修复分支
git checkout -b fix/installation-error

# 2. 编写测试
pytest tests/test_installer.py::test_installation_error

# 3. 修复 Bug
# 编辑相关文件

# 4. 验证修复
pytest tests/test_installer.py::test_installation_error

# 5. 提交 PR
git add .
git commit -m "fix: 修复安装错误 (#123)"
git push origin fix/installation-error
```

## 🚀 功能开发

### 功能提案

#### 提案模板

```markdown
## 功能提案

### 功能概述
[简要描述要实现的功能]

### 用户故事
**作为** [用户类型]
**我希望** [用户目标]
**以便** [用户价值]

### 详细需求
- [功能需求 1]
- [功能需求 2]
- [功能需求 3]

### 技术考虑
- **依赖**: [需要的外部依赖]
- **兼容性**: [需要考虑的兼容性问题]
- **性能**: [性能要求和限制]

### 验收标准
- [ ] 功能正常工作
- [ ] 测试覆盖率 > 80%
- [ ] 文档已更新
- [ ] 向后兼容
```

#### 开发流程

```bash
# 1. 功能分支
git checkout -b feature/custom-tool-support

# 2. 开发实现
# 编写代码和测试

# 3. 测试验证
pytest tests/feature/custom_tool/
python -m vibe_tools --test-feature custom-tool

# 4. 代码审查
# 自我审查或请求他人审查

# 5. 集成准备
# 确保 CI 通过，文档完整

# 6. 合并主分支
git checkout main
git merge feature/custom-tool-support
git push origin main
```

## 🔧 插件开发

### 插件架构

#### 标准插件接口

```python
# 标准 BaseTool 接口
from abc import ABC, abstractmethod
from typing import Dict, List, Optional

class BaseTool(ABC):
    """所有工具的基类"""
    
    def __init__(self, console: Console) -> None:
        self.console = console
    
    # 基本属性
    name: str = ""
    description: str = ""
    install_commands: List[str] = []
    verify_commands: List[str] = []
    dependencies: List[str] = []
    
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
    
    def get_version(self) -> Optional[str]:
        """获取工具版本"""
        if self.verify_commands:
            try:
                result = subprocess.run(
                    self.verify_commands[0].split(),
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if result.returncode == 0:
                    return self._parse_version(result.stdout)
            except subprocess.TimeoutExpired:
                pass
        return None
```

#### 插件开发示例

```python
# 自定义工具示例：my-custom-tool.py
from vibe_tools.core.installer import BaseTool, InstallResult

class MyCustomTool(BaseTool):
    def __init__(self, console: Console) -> None:
        super().__init__(console)
        self.name = "my-custom-tool"
        self.description = "我的自定义工具，用于特定任务"
        self.install_commands = [
            "curl -L https://github.com/user/tool/releases/latest/download/my-custom-tool -o /tmp/my-custom-tool",
            "chmod +x /tmp/my-custom-tool",
            "sudo mv /tmp/my-custom-tool /usr/local/bin/my-custom-tool"
        ]
        self.verify_commands = ["my-custom-tool --version"]
    
    def detect(self) -> bool:
        return shutil.which("my-custom-tool") is not None
    
    def install(self) -> InstallResult:
        if self.detect():
            return InstallResult(True, "MyCustomTool 已安装")
        
        self.console.print("🔧 安装 MyCustomTool...")
        
        # 执行安装步骤
        for cmd in self.install_commands:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.returncode != 0:
                return InstallResult(False, f"MyCustomTool 安装失败: {result.stderr}")
        
        return InstallResult(True, "MyCustomTool 安装成功")
    
    def verify(self) -> bool:
        return self.detect()
```

#### 插件注册机制

```python
# 自动插件发现
import importlib
import pkg_resources

def discover_plugins():
    plugins = []
    
    # 从 entry points 发现
    for entry_point in pkg_resources.iter_entry_points('vibe_tools.plugins'):
        try:
            plugin_class = entry_point.load()
            if issubclass(plugin_class, BaseTool):
                plugins.append(plugin_class)
        except (ImportError, AttributeError):
            pass
    
    return plugins

# 手动插件注册
AVAILABLE_TOOLS = {}

def register_tool(tool_class):
    """注册工具到全局注册表"""
    if issubclass(tool_class, BaseTool):
        tool_instance = tool_class(console)
        AVAILABLE_TOOLS[tool_instance.name] = tool_instance
```

## 🧪 测试指南

### 测试策略

#### 测试分类

```python
# 单元测试
tests/unit/
├── test_detector.py       # 环境检测测试
├── test_installer.py      # 安装器测试
├── test_menu.py          # 菜单系统测试
├── test_config.py        # 配置管理测试
└── test_utils.py         # 工具函数测试

# 集成测试
tests/integration/
├── test_full_workflow.py   # 完整工作流测试
├── test_tool_installation.py  # 工具安装集成测试
└── test_cli_commands.py   # CLI 命令测试

# 端到端测试
tests/e2e/
├── test_real_installation.py  # 真实环境安装测试
└── test_user_scenarios.py     # 用户场景测试
```

#### 测试编写规范

```python
# 测试类命名
class TestToolInstaller:
    """工具安装器测试"""
    
    def setup_method(self):
        """每个测试前运行"""
        # 设置测试环境
        pass
    
    def teardown_method(self):
        """每个测试后运行"""
        # 清理测试环境
        pass

# 测试方法命名
def test_install_success(self):
    """测试成功安装场景"""
    pass

def test_install_failure(self):
    """测试安装失败场景"""
    pass

def test_install_with_dependencies(self):
    """测试带依赖的安装"""
    pass
```

#### Mock 使用

```python
# Mock 系统调用
import unittest.mock as mock
import pytest

class TestSystemDetector:
    def test_detect_macos_system(self):
        """测试 macOS 系统检测"""
        with mock.patch('platform.system', return_value='Darwin'):
            with mock.patch('platform.version', return_value='14.0'):
                detector = SystemDetector()
                system_info = detector.get_system_info()
                
                assert system_info['os'] == 'Darwin'
                assert system_info['version'] == '14.0'

# Mock 命令执行
def test_tool_installation_success(self):
    """测试工具安装成功"""
    with mock.patch('subprocess.run') as mock_run:
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = "v1.0.0"
        
        tool = UVTool(console)
        result = tool.install()
        
        assert result.success is True
        assert "1.0.0" in result.message
```

### CI/CD 配置

#### GitHub Actions

```yaml
# .github/workflows/test.yml
name: Tests

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
        python-version: [3.8, 3.9, "3.10", "3.11", "3.12"]
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -e ".[dev]"
    
    - name: Run tests
      run: |
        pytest --cov=vibe_tools --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
```

#### 发布流程

```yaml
# .github/workflows/release.yml
name: Release

on:
  push:
    tags:
      - 'v*'

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install build twine
    
    - name: Build package
      run: python -m build
    
    - name: Publish to PyPI
      env:
        TWINE_USERNAME: __token__
        TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
      run: twine upload dist/*
```

## 📖 文档贡献

### 文档类型

#### API 文档

```python
# API 文档示例
def get_system_info() -> Dict[str, str]:
    """获取系统信息
    
    Returns:
        Dict[str, str]: 包含系统信息的字典，包括：
            - 'os': 操作系统名称
            - 'version': 操作系统版本
            - 'shell': 当前 Shell
            - 'python_version': Python 版本
    
    Example:
        >>> detector = SystemDetector()
        >>> info = detector.get_system_info()
        >>> info['os']
        'Darwin'
    """
```

#### 用户文档

```markdown
# 使用指南示例
## 安装工具

### 基础安装
最简单的方式是安装单个工具：

```bash
vibe-tools install uv
```

### 批量安装
一次性安装多个工具：

```bash
vibe-tools install uv poetry git
```

### 交互式安装
使用交互式菜单选择要安装的工具：

```bash
vibe-tools install --interactive
```
```

### 文档更新流程

```bash
# 1. 更新文档
# 编辑 docs/ 目录下的相关文件

# 2. 验证文档
# 检查语法和链接有效性

# 3. 生成文档站点
mkdocs build

# 4. 预览文档
mkdocs serve

# 5. 提交更改
git add docs/
git commit -m "docs: 更新安装指南"
```

## 🏆 社区指南

### 代码审查

#### 审查清单

- [ ] **功能正确性**: 代码实现了预期功能
- [ ] **代码质量**: 遵循代码规范和最佳实践
- [ ] **测试覆盖**: 包含充分的单元测试
- [ ] **文档更新**: 相关文档已更新
- [ ] **性能考虑**: 没有明显的性能问题
- [ ] **安全性**: 没有安全漏洞风险
- [ ] **向后兼容**: 不破坏现有 API

#### 审查流程

1. **自动检查**: CI 会自动运行基本检查
2. **人工审查**: 至少需要一个维护者审查
3. **反馈回复**: 及时回应审查意见
4. **修改迭代**: 根据反馈修改代码
5. **最终确认**: 所有审查通过后合并

### 社区参与

#### 参与方式

- **报告 Bug**: 发现并报告问题
- **功能建议**: 提出新功能想法
- **代码贡献**: 提交 Pull Request
- **文档改进**: 完善文档和示例
- **插件开发**: 开发自定义工具插件
- **推广宣传**: 分享使用经验

#### 行为准则

- **尊重他人**: 保持友善和建设性的沟通
- **技术讨论**: 专注于技术问题而非个人观点
- **学习分享**: 积极学习和分享知识
- **耐心包容**: 理解不同技能水平的贡献者

## 🎉 贡献者荣誉

### 认可方式

- **贡献者列表**: 在 README 中列出所有贡献者
- **发布说明**: 在发布说明中感谢贡献者
- **社区展示**: 优秀的贡献会在社区中展示

### 贡献统计

```bash
# 使用 git 统计贡献
git shortlog -sne --all

# 查看贡献趋势
git log --pretty=format:"%h %an %s" --since="1 year ago"
```

---

## 📞 联系方式

### 获取帮助

- **GitHub Issues**: [项目 Issues 页面]
- **GitHub Discussions**: [项目讨论页面]
- **邮件**: [维护者邮箱]
- **社区群**: [即时通讯群组]

### 问题类型

- **Bug 报告**: 使用 Bug 模板
- **功能请求**: 使用功能请求模板
- **安全问题**: 私密联系维护者
- **一般咨询**: 使用 Discussions

---

感谢您的贡献！每一个贡献都让 Vibe Tools 变得更好。🚀