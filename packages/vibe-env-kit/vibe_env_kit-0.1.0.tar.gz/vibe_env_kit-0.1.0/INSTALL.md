# 🚀 Vibe Tools 安装指南

## 问题解决：uvx 无法找到 vibe-tools

您遇到的错误是因为工具还未发布到 PyPI。以下是几种使用方法：

---

## 📦 方法1：本地开发安装（推荐用于测试）

### 在您的电脑上：

```bash
# 1. 克隆仓库
git clone https://github.com/your-username/vibe-tools.git
cd vibe-tools

# 2. 创建虚拟环境
python3 -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate  # Windows

# 3. 安装依赖
pip install click rich toml requests packaging

# 4. 运行工具
python bin/vibe-tools
```

---

## 📦 方法2：从源码直接运行

```bash
# 1. 克隆仓库
git clone https://github.com/your-username/vibe-tools.git
cd vibe-tools

# 2. 安装依赖（如果已有Python环境）
pip install click rich toml requests packaging

# 3. 直接运行
python -m src.vibe_tools.cli
```

---

## 📦 方法3：使用 pipx 安装（类 uvx）

如果您想用 `pipx`（类似 uvx）：

```bash
# 1. 安装 pipx
brew install pipx  # macOS
# 或: sudo apt install pipx  # Ubuntu

# 2. 从本地源码安装
pipx install --editable .
```

---

## 📦 方法4：打包发布后使用 uvx（最终目标）

**发布到 PyPI 后**，用户可以直接：

```bash
# 完全零配置！
uvx vibe-tools
```

---

## 🔧 修复 pyproject.toml 以支持本地安装

确保您的 `pyproject.toml` 正确配置：

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "vibe-tools"
version = "0.1.0"
description = "现代化的 CLI 环境配置工具"
dependencies = [
    "click>=8.0.0",
    "rich>=13.0.0",
    "toml>=0.10.2",
    "requests>=2.25.0",
    "packaging>=21.0",
]

[project.scripts]
vibe-tools = "vibe_tools.cli:main"

[tool.hatch.build.targets.wheel]
packages = ["src/vibe_tools"]
```

---

## 🧪 测试本地安装

在任何新电脑上测试：

```bash
# 1. 下载源码
git clone https://github.com/your-username/vibe-tools.git
cd vibe-tools

# 2. 验证结构
ls -la
# 应该看到: bin/, src/, pyproject.toml, README.md 等

# 3. 安装测试
python3 -m venv test-env
source test-env/bin/activate
pip install -e .

# 4. 测试命令
vibe-tools --help
vibe-tools  # 应该启动交互式菜单

# 5. 测试 uvx 兼容（发布后）
uvx vibe-tools
```

---

## 📤 发布到 PyPI 的步骤

当您准备好发布时：

```bash
# 1. 安装发布工具
pip install build twine

# 2. 构建包
python -m build

# 3. 检查包
twine check dist/*

# 4. 上传到测试 PyPI
twine upload --repository testpypi dist/*

# 5. 测试 PyPI 安装
pip install --index-url https://test.pypi.org/simple/ vibe-tools

# 6. 正式发布
twine upload dist/*
```

发布成功后，任何人都可以：

```bash
uvx vibe-tools  # 完全零配置！
```

---

## 🚨 当前推荐的使用方式

**对于其他电脑用户，现在推荐使用方法1：**

```bash
git clone https://github.com/your-username/vibe-tools.git
cd vibe-tools
python3 -m venv .venv
source .venv/bin/activate
pip install click rich toml requests packaging
python bin/vibe-tools
```

这样可以立即使用所有功能！