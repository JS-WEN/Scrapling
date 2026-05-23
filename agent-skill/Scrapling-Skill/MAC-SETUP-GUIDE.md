# Scrapling Skill for Mac 本地配置

## 📦 方式 1：完整下载 Skill 到 Mac

1. 复制 `/workspace/agent-skill/Scrapling-Skill/` 整个目录到您的 Mac
2. 在 Mac 上的 Trae 配置中使用这些文件

## 🚀 方式 2：直接安装并配置（推荐）

### 步骤 1：在 Mac 上安装 Scrapling

打开 Mac 终端，运行：

```bash
# 安装 Scrapling
pip install "scrapling[all]>=0.4.8"

# 安装浏览器依赖
scrapling install --force
```

### 步骤 2：找到 Mac 上的 Trae 配置文件

Mac 上可能的位置：
- `~/Library/Application Support/trae/mcp-servers.json`
- `~/.config/trae/mcp-servers.json`
- 或者查看 Trae 设置中的 MCP 配置位置

### 步骤 3：编辑配置文件

在配置文件中添加：

```json
{
  "mcpServers": {
    "scrapling": {
      "command": "uvx",
      "args": ["--from", "scrapling[all]", "scrapling", "mcp"],
      "description": "Scrapling Web Scraping - Adaptive scraping with anti-bot bypass and browser automation"
    }
  }
}
```

如果没有 uvx，也可以直接使用：

```json
{
  "mcpServers": {
    "scrapling": {
      "command": "scrapling",
      "args": ["mcp"],
      "description": "Scrapling Web Scraping - Adaptive scraping with anti-bot bypass and browser automation"
    }
  }
}
```

### 步骤 4：重启 Trae

完全关闭并重新打开 Mac 上的 Trae。

### 步骤 5：验证

在 Trae 的 MCP 设置中应该能看到 "scrapling" 服务器已启用。

## 💡 快速测试

安装配置完成后，在 Trae 聊天中输入：

```
帮我抓取 https://example.com 的页面标题
```

## 📚 参考文档

- 主 SKILL 文件：[SKILL.md](file:///workspace/agent-skill/Scrapling-Skill/SKILL.md)
- 快速参考：[QUICK-REFERENCE.md](file:///workspace/agent-skill/Scrapling-Skill/QUICK-REFERENCE.md)

## ⚠️ 重要提示

确保您的 Mac 上安装了 Python 3.10+ 版本。
