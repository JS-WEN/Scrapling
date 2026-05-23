#!/bin/bash

# Scrapling MCP 配置验证脚本

echo "🔍 正在验证 Scrapling MCP 配置..."
echo ""

# 1. 检查配置文件
echo "1️⃣ 检查 MCP 配置文件..."
if [ -f ~/.config/trae/mcp_servers.json ]; then
    echo "✅ MCP 配置文件已创建"
    cat ~/.config/trae/mcp_servers.json
else
    echo "❌ MCP 配置文件不存在"
    exit 1
fi
echo ""

# 2. 检查 Python 版本
echo "2️⃣ 检查 Python 版本..."
python3 --version
echo ""

# 3. 检查 uvx 是否可用
echo "3️⃣ 检查 uvx..."
which uvx && echo "✅ uvx 已安装" || echo "❌ uvx 未找到"
echo ""

# 4. 测试 Scrapling 安装
echo "4️⃣ 测试 Scrapling MCP 服务器..."
echo "   正在启动 MCP 服务器（5秒超时测试）..."
timeout 5 uvx --from "scrapling[all]" scrapling mcp --help > /dev/null 2>&1
if [ $? -eq 0 ] || [ $? -eq 124 ]; then
    echo "✅ Scrapling MCP 服务器已准备就绪"
else
    echo "❌ Scrapling MCP 服务器启动失败"
    exit 1
fi
echo ""

# 5. 显示使用说明
echo "5️⃣ 配置完成！"
echo ""
echo "📋 使用方法："
echo ""
echo "   1. 重启 Trae IDE"
echo "   2. 在 Trae 中打开设置"
echo "   3. 找到 MCP Servers 设置"
echo "   4. 应该能看到 'scrapling' 服务器"
echo "   5. 如果需要，点击启用按钮"
echo ""
echo "💡 可用的 MCP 工具："
echo "   • get          - 快速 HTTP 请求"
echo "   • bulk_get     - 批量 HTTP 请求"
echo "   • fetch        - 浏览器渲染"
echo "   • bulk_fetch   - 批量浏览器渲染"
echo "   • stealthy_fetch - 反爬虫绕过"
echo "   • bulk_stealthy_fetch - 批量反爬虫绕过"
echo "   • open_session - 创建持久会话"
echo "   • close_session - 关闭会话"
echo "   • list_sessions - 列出活跃会话"
echo "   • screenshot   - 页面截图"
echo ""
echo "📖 详细文档位于："
echo "   /workspace/agent-skill/Scrapling-Skill/SKILL.md"
echo ""
echo "🎉 恭喜！Scrapling Skill 已成功配置！"
