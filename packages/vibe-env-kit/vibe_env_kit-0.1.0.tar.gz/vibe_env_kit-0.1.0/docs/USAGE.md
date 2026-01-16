# Vibe Tools 使用指南

> "从零到精通，成为开发环境管理大师" - Vibe Tools 完整使用手册

## 🚀 快速开始

### 安装方式

#### 🏃 零配置运行（推荐）

```bash
# 发布后，完全零配置
uvx vibe-tools
```

#### 📦 本地安装

```bash
# 克隆仓库
git clone https://github.com/your-username/vibe-tools.git
cd vibe-tools

# 创建虚拟环境
python3 -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# 安装依赖
pip install -e .

# 运行工具
vibe-tools
```

#### 📥 一键安装脚本

```bash
# 使用我们的安装脚本
curl -sSL https://raw.githubusercontent.com/your-username/vibe-tools/main/install.sh | bash
```

## 🎯 基础使用

### 首次运行体验

当您第一次运行 `vibe-tools` 时，会看到：

```
╔════════════════════════════════════════════════╗
║                       🛠️  Vibe Tools                         ║
║                    零配置开发环境管理器                    ║
║                Zero-Config Development Environment Manager             ║
╚════════════════════════════════════════════════╝

🔍 检测到您的系统：macOS arm64 + zsh + Python 3.12

请选择功能:
  1. 完整初始化 - 安装开发环境 + 导入工作流 + 配置 API
  4. 安装开发工具 - Python、Node.js、Git、Docker 等
  7. Claude Code 配置 - 配置 Claude Code 环境
  Q. 退出程序 - 退出 Vibe Tools
```

### 主菜单导航

#### 🚀 快速开始区域

**1. 完整初始化** - 一键设置完整开发环境
- 自动检测系统环境
- 推荐合适的工具组合
- 批量安装和配置
- 生成项目模板

**2. 导入工作流** - 从模板或现有项目导入
- 支持多种项目类型（Web、AI、数据科学等）
- 智能合并现有配置
- 保留用户自定义设置

**3. 配置 API 或 CCR 代理** - 设置云服务连接
- 支持 Claude API、OpenAI API
- 支持代理服务（302.ai、PackyCode等）
- 自动测试连接有效性

#### 📦 工具管理区域

**4. 安装开发工具** - 核心功能，支持交互式选择
- 实时工具状态显示
- 智能依赖解析
- 并行安装优化
- 详细的安装日志

**5. 更新工具链** - 批量更新已安装工具
- 版本检查和兼容性验证
- 增量更新机制
- 回滚支持

**6. 卸载工具** - 安全清理已安装工具
- 依赖检查和警告
- 配置文件清理
- 环境变量重置

#### 🤖 AI 工具区域

**7. Claude Code 配置** - AI 开发环境设置
- API 密钥配置
- 项目模板导入
- MCP 服务配置
- 个性化设置

**8. GitHub Copilot** - GitHub AI 助手设置
- 认证配置
- 插件管理
- IDE 集成

**9. Cursor Editor** - AI 编辑器配置
- 配置文件生成
- 扩展推荐
- 工作区设置

#### ⚙️ 系统配置区域

**0. Shell 环境配置** - 环境变量和 Shell 设置
- 自动配置 rc 文件
- PATH 管理
- 环境变量同步
- 多 Shell 支持（bash、zsh、fish）

**S. 切换代码工具** - 多工具环境管理
- 工具链切换
- 配置导入导出
- 版本管理
- 并行安装支持

**C. 配置默认模型** - AI 模型和参数设置
- 模型选择和优先级
- 参数调优
- 上下文管理
- 成本控制

## 🛠️ 高级功能

### 命令行接口

#### 完整命令列表

```bash
# 主命令
vibe-tools                    # 启动交互式菜单
vibe-tools --help           # 显示帮助
vibe-tools --version        # 显示版本

# 子命令
vibe-tools init             # 初始化
vibe-tools install           # 安装工具
vibe-tools list              # 列出已安装工具
vibe-tools update            # 更新工具
vibe-tools status            # 显示状态
vibe-tools config            # 配置设置
```

#### 常用选项

```bash
# 详细输出
vibe-tools --verbose install uv

# 预览模式
vibe-tools --dry-run install git

# 指定配置文件
vibe-tools --config /path/to/config.toml

# 非交互式安装
vibe-tools install uv poetry git

# 显示版本
vibe-tools --version
```

### 配置文件管理

#### 配置文件位置

```bash
# 配置文件查找顺序
1. ~/.vibe-tools/config.toml          # 用户配置
2. ./.vibe-tools/config.toml           # 项目配置
3. /etc/vibe-tools/config.toml        # 系统配置
4. --config /custom/path/config.toml   # 命令行指定
```

#### 配置文件结构

```toml
[general]
default_language = "zh-CN"
auto_update = true
telemetry = false
theme = "auto"

[tools]
auto_install_dependencies = true
preferred_versions = { uv = "latest", node = "lts" }
install_timeout = 300
parallel_installs = true

[ai]
default_provider = "anthropic"
model_preferences = { 
    claude = "claude-3-5-sonnet-20241022",
    openai = "gpt-4-turbo"
}
temperature = 0.7
max_tokens = 4096

[ui]
show_tips = true
animations = true
color_scheme = "auto"
compact_mode = false

[advanced]
cache_dir = "~/.vibe-tools/cache"
log_level = "INFO"
backup_configs = true
```

## 🔧 自定义和扩展

### 插件开发

#### 创建自定义工具

```python
# 创建 my_tool.py
from vibe_tools.core.installer import BaseTool, InstallResult

class MyTool(BaseTool):
    def __init__(self, console):
        super().__init__(console)
        self.name = "my-tool"
        self.description = "我的自定义工具"
        self.install_commands = ["brew install my-tool"]
        self.verify_commands = ["my-tool --version"]
    
    def detect(self) -> bool:
        return shutil.which("my-tool") is not None
    
    def install(self) -> InstallResult:
        # 实现安装逻辑
        if self.detect():
            return InstallResult(True, "My Tool 已安装")
        
        # 执行安装
        result = subprocess.run(self.install_commands[0], shell=True)
        if result.returncode == 0:
            return InstallResult(True, "My Tool 安装成功")
        else:
            return InstallResult(False, "My Tool 安装失败", result.stderr)
    
    def verify(self) -> bool:
        return self.detect()

# 注册插件
from vibe_tools.tools import register_tool
register_tool(MyTool)
```

#### 主题自定义

```python
# 创建自定义主题
from vibe_tools.ui.display import DisplayManager

class CustomTheme:
    colors = {
        "primary": "#007ACC",
        "success": "#28A745", 
        "warning": "#FFC107",
        "error": "#DC3545",
        "info": "#17A2B8",
    }
    
    def format_banner(self, title, subtitle=""):
        # 自定义横幅样式
        pass

# 应用主题
display = DisplayManager(theme=CustomTheme())
```

### 脚本集成

#### 项目设置脚本

```bash
#!/bin/bash
# setup-project.sh
echo "🚀 使用 Vibe Tools 设置项目"

# 初始化项目
git init
vibe-tools init python

# 安装推荐工具
vibe-tools install uv poetry pre-commit

# 配置开发环境
vibe-tools config shell --zsh
```

#### CI/CD 集成

```yaml
# .github/workflows/setup.yml
name: Setup Development Environment

jobs:
  setup:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Setup Vibe Tools
      run: |
        curl -sSL https://raw.githubusercontent.com/your-username/vibe-tools/main/install.sh | bash
        
    - name: Install Development Tools
      run: vibe-tools install uv poetry git docker --non-interactive
```

## 🔍 故障排除

### 常见问题解决

#### 安装问题

**问题**: `uvx vibe-tools` 找不到包
```bash
# 解决方案
uvx --index-url https://test.pypi.org/simple/ vibe-tools
# 或
pip install vibe-tools
```

**问题**: 权限不足
```bash
# 解决方案
sudo vibe-tools install git
# 或
vibe-tools install --user git
```

**问题**: 网络连接失败
```bash
# 解决方案
vibe-tools --timeout 600 install uv
# 或
export VIBE_TOOLS_MIRROR=https://pypi.tuna.tsinghua.edu.cn/simple/
vibe-tools install uv
```

#### 配置问题

**问题**: 环境变量未生效
```bash
# 解决方案
source ~/.bashrc
# 重启终端
vibe-tools config shell --reload
```

**问题**: 工具安装失败
```bash
# 解决方案
vibe-tools install --verbose tool-name
# 查看详细错误日志
vibe-tools diagnose tool-name
```

### 调试模式

```bash
# 启用详细日志
vibe-tools --debug install uv

# 显示系统诊断
vibe-tools diagnose --full

# 生成诊断报告
vibe-tools diagnose --report
```

## 📊 性能优化

### 启动优化

#### 快速启动技巧

```bash
# 最小化启动
vibe-tools --no-animations install uv

# 缓存系统检测
vibe-tools --use-cache status

# 跳过网络检查
vibe-tools --offline mode
```

#### 内存优化

```bash
# 紧凑模式
vibe-tools --compact-mode

# 限制并行任务
vibe-tools --max-concurrent 2 install

# 清理缓存
vibe-tools clean --cache
```

### 网络优化

```bash
# 使用镜像
vibe-tools --mirror tsinghua

# 设置代理
vibe-tools --proxy http://proxy.example.com:8080

# 限制带宽
vibe-tools --bandwidth-limit 1m
```

## 🎓 最佳实践

### 工作流建议

#### 新项目设置

```bash
# 1. 创建项目目录
mkdir my-new-project
cd my-new-project

# 2. 初始化 Git 和 Vibe Tools
git init
vibe-tools init python

# 3. 安装开发工具
vibe-tools install uv poetry pre-commit

# 4. 创建虚拟环境
python -m venv .venv
source .venv/bin/activate

# 5. 安装项目依赖
uv pip install -e .

# 6. 启动开发
vibe-tools dev-setup
```

#### 团队协作

```bash
# 导出团队配置
vibe-tools config export --team > team-config.json

# 分享配置
git config vibe-tools.team-url "https://config.example.com/team-config.json"

# 导入团队配置
vibe-tools config import --team team-config.json
```

#### 多环境管理

```bash
# 开发环境
vibe-tools --env dev install uv

# 测试环境  
vibe-tools --env test install uv

# 生产环境
vibe-tools --env prod install uv

# 环境切换
vibe-tools switch --env dev
```

## 🌟 高级特性

### AI 集成

#### 智能工具推荐

```bash
# 基于项目类型推荐
vibe-tools recommend --project-type web-framework
vibe-tools recommend --project-type ai-ml
vibe-tools recommend --project-type data-science

# 基于现有代码推荐
vibe-tools analyze --directory ./src
vibe-tools recommend --based-on-analysis
```

#### 自动化配置

```bash
# 智能配置生成
vibe-tools config --auto --project-type web-app

# 个性化建议
vibe-tools suggest --optimization speed
vibe-tools suggest --optimization memory
vibe-tools suggest --based-on-history
```

### 云端同步

```bash
# 配置同步
vibe-tools sync --upload-config
vibe-tools sync --download-config

# 工具状态同步
vibe-tools sync --tool-status
vibe-tools sync --preferences
```

---

## 📝 结语

Vibe Tools 不仅仅是一个工具管理器，它是您的**开发环境智能助手**。通过这个指南，您应该能够：

1. **快速上手** - 5分钟内完成环境设置
2. **高效工作** - 专注于创造而非配置
3. **灵活定制** - 根据需求调整工具链
4. **智能推荐** - 让 AI 帮助做出最佳选择
5. **无缝集成** - 与现有工作流完美融合

记住：**最好的工具是让你忘记它的存在**。

祝您开发愉快！🚀