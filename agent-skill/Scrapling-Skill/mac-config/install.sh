#!/bin/bash
# Scrapling Skill Mac 安装脚本

echo "=========================================="
echo "  Scrapling Skill 安装脚本 (Mac)"
echo "=========================================="
echo ""

# 检查 Python 版本
echo "🔍 检查 Python 版本..."
if ! python3 --version | grep -E "3\.1[0-9]" >/dev/null 2>&1; then
    echo "❌ 需要 Python 3.10 或更高版本"
    echo "请先安装 Python 3.10+：https://www.python.org/downloads/"
    exit 1
fi
echo "✅ Python 版本检查通过"
python3 --version
echo ""

# 安装 Scrapling
echo "📦 安装 Scrapling..."
pip3 install "scrapling[all]>=0.4.8"
if [ $? -ne 0 ]; then
    echo "❌ 安装失败"
    exit 1
fi
echo "✅ Scrapling 安装成功"
echo ""

# 安装浏览器依赖
echo "🌐 安装浏览器依赖..."
scrapling install --force
if [ $? -ne 0 ]; then
    echo "⚠️  浏览器依赖安装可能有问题，请手动运行：scrapling install --force"
else
    echo "✅ 浏览器依赖安装完成"
fi
echo ""

# 查找 Trae 配置文件
echo "🔍 查找 Trae 配置文件..."
TRAE_CONFIG=""
CONFIG_PATHS=(
    "$HOME/Library/Application Support/trae/mcp-servers.json"
    "$HOME/.config/trae/mcp-servers.json"
)

for path in "${CONFIG_PATHS[@]}"; do
    if [ -f "$path" ]; then
        TRAE_CONFIG="$path"
        break
    fi
done

if [ -z "$TRAE_CONFIG" ]; then
    echo "⚠️  未找到现有的 Trae 配置文件"
    echo "请检查 Trae 设置中的 MCP 配置位置"
    echo ""
    echo "📝 默认配置文件已创建在：$(dirname "$0")/mcp-servers.json"
    echo "请复制到 Trae 的 MCP 配置目录"
else
    echo "✅ 找到配置文件：$TRAE_CONFIG"
    echo ""
    
    # 备份现有配置
    if [ -f "$TRAE_CONFIG" ]; then
        BACKUP="$TRAE_CONFIG.backup.$(date +%Y%m%d%H%M%S)"
        cp "$TRAE_CONFIG" "$BACKUP"
        echo "📋 已备份现有配置到：$BACKUP"
    fi
    
    # 合并配置
    echo "🔧 更新配置文件..."
    if [ -f "$TRAE_CONFIG" ]; then
        # 检查是否已存在 scrapling 配置
        if grep -q "scrapling" "$TRAE_CONFIG"; then
            echo "⚠️  scrapling 配置已存在，跳过更新"
        else
            # 合并配置
            TEMP=$(mktemp)
            jq '.mcpServers.scrapling = {"command": "scrapling", "args": ["mcp"], "description": "Scrapling Web Scraping - Adaptive scraping with anti-bot bypass and browser automation"}' "$TRAE_CONFIG" > "$TEMP" && mv "$TEMP" "$TRAE_CONFIG"
            echo "✅ 配置已更新"
        fi
    else
        # 创建新配置
        cp "$(dirname "$0")/mcp-servers.json" "$TRAE_CONFIG"
        echo "✅ 新配置文件已创建"
    fi
fi

echo ""
echo "=========================================="
echo "  🎉 安装完成！"
echo "=========================================="
echo ""
echo "📋 下一步："
echo "1. 完全关闭并重新打开 Trae IDE"
echo "2. 检查 Trae 设置 → MCP，应该能看到 'scrapling' 服务器"
echo "3. 在聊天中测试：帮我抓取 https://example.com 的页面标题"
echo ""
echo "📚 参考文档："
echo "- 主文档：./SKILL.md"
echo "- 快速参考：./QUICK-REFERENCE.md"
echo ""
