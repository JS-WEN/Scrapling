# Scrapling Skill - Mac 本地安装包

## 📦 下载和安装

### 方式 1：下载整个 Skill 包（推荐）

1. 将 `/workspace/agent-skill/Scrapling-Skill/` 整个目录下载到您的 Mac
2. 在 Mac 上打开下载的目录
3. 运行安装脚本：

```bash
cd /path/to/Scrapling-Skill/mac-config
chmod +x install.sh
./install.sh
```

### 方式 2：手动安装

#### 步骤 1：安装 Scrapling

在 Mac 终端中运行：

```bash
# 安装 Scrapling
pip3 install "scrapling[all]>=0.4.8"

# 安装浏览器依赖
scrapling install --force
```

#### 步骤 2：配置 Trae

1. 找到您的 Mac 上的 Trae MCP 配置文件（通常在：
   - `~/Library/Application Support/trae/mcp-servers.json`
   - 或 `~/.config/trae/mcp-servers.json`

2. 复制 `mac-config/mcp-servers.json` 的内容到配置文件中，或直接复制配置文件。

3. 完全重启 Trae IDE

## 📋 配置文件说明

### `mac-config/mcp-servers.json` - 直接复制到 Trae 配置目录

```json
{
  "mcpServers": {
    "scrapling": {
      "command": "scrapling",
      "args": ["mcp"],
      "description": "Scrapling Web Scraping"
    }
  }
}
```

### `mac-config/install.sh` - 自动安装脚本

一键安装和配置，推荐使用。

## ✅ 验证安装

安装后在 Trae 聊天中输入：

```
帮我抓取 https://example.com 的页面标题
```

## 📚 文档

- **主文档**：[SKILL.md](../SKILL.md)
- **快速参考**：[QUICK-REFERENCE.md](../QUICK-REFERENCE.md)
- **详细入门**：[QUICKSTART.md](../QUICKSTART.md)

## 🎯 完整目录结构

```
Scrapling-Skill/
├── SKILL.md
├── QUICK-REFERENCE.md
├── QUICKSTART.md
├── README.md
├── mac-config/
│   ├── install.sh
│   ├── mcp-servers.json
│   └── README.md (本文件)
├── examples/
└── references/
```
