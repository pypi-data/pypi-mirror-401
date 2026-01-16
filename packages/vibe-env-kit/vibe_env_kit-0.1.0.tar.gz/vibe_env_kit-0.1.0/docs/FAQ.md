# Vibe Tools 常见问题解答

> "快速解决您遇到的每个问题" - Vibe Tools FAQ 汇总

## 🚀 安装和使用

### Q: `uvx vibe-tools` 找不到包

**问题**: 
```bash
uvx vibe-tools
× No solution found when resolving tool dependencies:
╰─▶ Because vibe-tools was not found in the package registry...
```

**解决方案**:
1. **发布前使用本地安装**：
   ```bash
   git clone https://github.com/your-username/vibe-tools.git
   cd vibe-tools
   python -m venv .venv
   source .venv/bin/activate
   pip install -e .
   vibe-tools
   ```

2. **使用 pipx 替代**：
   ```bash
   pipx install --editable .
   pipx vibe-tools
   ```

3. **从源码直接运行**：
   ```bash
   git clone https://github.com/your-username/vibe-tools.git
   cd vibe-tools
   pip install click rich toml requests packaging
   python -m src.vibe_tools.cli
   ```

### Q: 安装后找不到依赖

**问题**: 
```
ModuleNotFoundError: No module named 'click'
```

**解决方案**:
```bash
# 方法1：安装到虚拟环境
python -m venv .venv
source .venv/bin/activate
pip install click rich toml requests packaging
vibe-tools

# 方法2：使用用户安装
pip install --user click rich toml requests packaging

# 方法3：使用 uv 包管理器
uv add click rich toml requests packaging
uv run vibe-tools
```

### Q: Windows 上运行问题

**问题**: 在 Windows 上出现权限或路径问题

**解决方案**:
```powershell
# 使用 PowerShell
git clone https://github.com/your-username/vibe-tools.git
cd vibe-tools
python -m venv venv
.\venv\Scripts\activate
pip install -e .
python -m vibe_tools.cli

# 或使用 pipx
pipx install --editable .
pipx vibe-tools
```

### Q: 无法使用中文界面

**问题**: 界面显示乱码或不支持中文

**解决方案**:
```bash
# 检查终端编码
export LANG=zh_CN.UTF-8
export LC_ALL=zh_CN.UTF-8

# 或在配置中设置语言
vibe-tools config language zh-CN
```

## 🛠️ 工具安装

### Q: 工具安装失败

**问题**: 
```
❌ uv 安装失败: Permission denied
```

**解决方案**:
```bash
# 方法1：使用用户级安装
vibe-tools install --user uv

# 方法2：手动设置权限
sudo chown -R $USER:$USER ~/.local

# 方法3：使用管理员权限
sudo vibe-tools install uv
```

### Q: 工具版本冲突

**问题**: 新安装的版本与现有工具不兼容

**解决方案**:
```bash
# 查看版本冲突
vibe-tools diagnose uv

# 强制使用特定版本
vibe-tools install uv --version 0.2.10

# 卸载后重装
vibe-tools uninstall uv
vibe-tools install uv
```

### Q: 环境变量未生效

**问题**: 安装后工具找不到路径

**解决方案**:
```bash
# 方法1：重启终端
exec $SHELL

# 方法2：手动加载环境变量
source ~/.bashrc  # bash/zsh
source ~/.zshrc   # zsh
source ~/.profile  # 通用

# 方法3：检查配置
echo $PATH | grep -o "[^:]*"
vibe-tools config show shell
```

## ⚙️ 配置管理

### Q: 配置文件无效

**问题**: 
```
Error: Invalid configuration file format
```

**解决方案**:
1. **验证 TOML 语法**：
   ```bash
   python -c "import toml; print(toml.load(open('config.toml')))"
   ```

2. **使用默认配置**：
   ```bash
   rm ~/.vibe-tools/config.toml
   vibe-tools  # 会创建默认配置
   ```

3. **检查文件权限**：
   ```bash
   ls -la ~/.vibe-tools/config.toml
   chmod 644 ~/.vibe-tools/config.toml
   ```

### Q: 配置重置

**问题**: 配置混乱，需要重置到默认状态

**解决方案**:
```bash
# 完全重置
vibe-tools config reset --all

# 重置特定配置
vibe-tools config reset tools
vibe-tools config reset ui

# 重置到默认语言
vibe-tools config language en-US
```

## 🔍 系统检测

### Q: 系统信息不准确

**问题**: 显示错误的操作系统或版本信息

**解决方案**:
```bash
# 更新系统信息
vibe-tools diagnose --refresh-system

# 手动指定系统
vibe-tools --system macos arm64
vibe-tools --system linux x86_64
vibe-tools --system windows amd64
```

### Q: 工具检测失败

**问题**: 无法检测已安装的工具

**解决方案**:
```bash
# 详细诊断
vibe-tools diagnose --verbose uv

# 手动指定工具路径
vibe-tools config tools uv.path /usr/local/bin/uv

# 强制重新检测
vibe-tools diagnose --force-detect
```

### Q: 权限不足

**问题**: 
```
PermissionError: [Errno 13] Permission denied
```

**解决方案**:
```bash
# 检查当前用户权限
vibe-tools diagnose --permissions

# 使用用户级安装
vibe-tools install --user-all

# 创建用户目录
mkdir -p ~/.local/bin ~/.local/lib
export PATH=$HOME/.local/bin:$PATH
```

## 🚀 高级使用

### Q: 如何创建自定义工具

**问题**: 希望添加 Vibe Tools 不支持的工具

**解决方案**:
```python
# 创建自定义工具插件
# my_custom_tool.py
from vibe_tools.core.installer import BaseTool, InstallResult
from rich.console import Console

class MyCustomTool(BaseTool):
    def __init__(self, console: Console):
        super().__init__(console)
        self.name = "my-custom-tool"
        self.description = "我的自定义工具"
        self.install_commands = ["brew install my-custom-tool"]
        self.verify_commands = ["my-custom-tool --version"]
    
    def detect(self) -> bool:
        return shutil.which("my-custom-tool") is not None
    
    def install(self) -> InstallResult:
        # 实现安装逻辑
        if self.detect():
            return InstallResult(True, "MyCustomTool 已安装")
        
        # 安装逻辑
        self.console.print("安装 MyCustomTool...")
        return InstallResult(True, "MyCustomTool 安装成功")
    
    def verify(self) -> bool:
        return self.detect()

# 注册工具
from vibe_tools.tools import register_tool
register_tool(MyCustomTool)
```

### Q: 如何配置团队环境

**问题**: 团队需要统一的开发环境配置

**解决方案**:
```bash
# 导出团队配置
vibe-tools config export --team > team-config.json

# 分享配置文件
git add team-config.json
git commit -m "Add team development config"
git push origin main

# 其他成员导入
git clone repo
cd repo
vibe-tools config import --team team-config.json
```

### Q: 如何在 CI/CD 中使用

**问题**: 在持续集成环境中自动化环境设置

**解决方案**:
```yaml
# .github/workflows/setup.yml
name: Setup Development Environment

on: [push, pull_request]

jobs:
  setup:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install Vibe Tools
      run: |
        curl -sSL https://raw.githubusercontent.com/your-username/vibe-tools/main/install.sh | bash
    
    - name: Configure Environment
      run: |
        vibe-tools install uv poetry git --non-interactive
        vibe-tools config set team.enabled true
    
    - name: Verify Installation
      run: |
        vibe-tools status
        uv --version
        poetry --version
        git --version
```

## 🔧 故障排除

### Q: 启动速度很慢

**问题**: 工具启动需要很长时间

**解决方案**:
```bash
# 检查启动性能
vibe-tools --debug start

# 禁用动画和高级功能
vibe-tools --no-animations --compact-mode

# 使用缓存
vibe-tools config set cache.enabled true
vibe-tools config set cache.ttl 3600
```

### Q: 内存使用过高

**问题**: 运行时占用大量内存

**解决方案**:
```bash
# 内存使用诊断
vibe-tools diagnose --memory

# 限制并发任务
vibe-tools config set max-concurrent-tasks 2

# 清理缓存
vibe-tools clean --cache --logs
```

### Q: 网络连接问题

**问题**: 无法下载工具或检查更新

**解决方案**:
```bash
# 使用镜像源
vibe-tools --mirror https://pypi.tuna.tsinghua.edu.cn/simple/

# 设置代理
vibe-tools --proxy http://proxy.example.com:8080

# 离线模式
vibe-tools --offline
vibe-tools sync --when-online
```

## 📞 获取帮助

### 自助资源

1. **文档**: [在线文档](https://vibe-tools.readthedocs.io/)
2. **GitHub Issues**: [报告问题](https://github.com/your-username/vibe-tools/issues)
3. **GitHub Discussions**: [社区讨论](https://github.com/your-username/vibe-tools/discussions)
4. **更新日志**: [CHANGELOG.md](CHANGELOG.md)

### 联系方式

- **Bug 报告**: [创建 Issue](https://github.com/your-username/vibe-tools/issues/new?template=bug_report.md)
- **功能请求**: [创建 Issue](https://github.com/your-username/vibe-tools/issues/new?template=feature_request.md)
- **安全问题**: [安全报告](mailto:security@vibe-tools.dev)

### 调试模式

```bash
# 启用详细调试
vibe-tools --debug --verbose --log-file debug.log

# 生成诊断报告
vibe-tools diagnose --full --report > system-report.json
cat system-report.json
```

---

如果您的问题没有在这里找到答案，请：

1. **检查在线文档** - 可能已有最新解决方案
2. **搜索 GitHub Issues** - 类似问题可能已解决
3. **创建新的 Issue** - 详细描述问题和环境
4. **加入社区讨论** - 其他用户可能遇到过类似问题

我们持续改进 Vibe Tools，感谢您的使用！🚀