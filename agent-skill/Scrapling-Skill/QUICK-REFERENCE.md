# 🎯 Scrapling MCP 快速参考卡

## ✅ 配置状态

- [x] MCP 配置文件：✅ 已创建 (~/.config/trae/mcp_servers.json)
- [x] Python 版本：✅ 3.14.4
- [x] uvx 工具：✅ 已安装
- [x] Scrapling：✅ 已安装
- [x] MCP 服务器：✅ 已就绪

## 🚀 立即使用

1. **重启 Trae IDE**
2. **在聊天中直接使用：**
   ```
   帮我抓取 https://example.com 的内容
   使用 scrapling 获取这个页面的所有链接
   抓取 quotes.toscrape.com 的所有引言
   ```

## 📝 MCP 工具速查表

### 🌐 简单任务
| 工具 | 用途 | 示例 |
|------|------|------|
| `get` | 静态网页 | `get(url="https://example.com")` |
| `bulk_get` | 批量静态页面 | `bulk_get(urls=["url1", "url2"])` |

### 🎨 动态页面
| 工具 | 用途 | 示例 |
|------|------|------|
| `fetch` | JS 渲染页面 | `fetch(url="https://spa.com", network_idle=True)` |
| `bulk_fetch` | 批量 JS 页面 | `bulk_fetch(urls=[...])` |

### 🛡️ 受保护网站
| 工具 | 用途 | 示例 |
|------|------|------|
| `stealthy_fetch` | Cloudflare 绕过 | `stealthy_fetch(url, solve_cloudflare=True)` |

### 💾 会话管理
| 工具 | 用途 | 示例 |
|------|------|------|
| `open_session` | 创建持久会话 | `open_session(session_type="dynamic")` |
| `screenshot` | 页面截图 | `screenshot(url, session_id)` |
| `close_session` | 关闭会话 | `close_session(session_id="xxx")` |

## 💻 CLI 命令

```bash
# 基本抓取
scrapling extract get "https://example.com" content.md

# JS 渲染
scrapling extract fetch "https://example.com" page.md --network-idle

# 绕过反爬
scrapling extract stealthy-fetch "https://example.com" content.md --solve-cloudflare

# 带 CSS 选择器
scrapling extract get "URL" output.md --css-selector "article"
```

## 🐍 Python 脚本示例

**简单抓取：**
```python
from scrapling.fetchers import Fetcher

page = Fetcher.get('https://example.com')
data = page.css('.content::text').getall()
```

**浏览器自动化：**
```python
from scrapling.fetchers import DynamicSession

with DynamicSession() as session:
    page = session.fetch('https://example.com')
    data = page.css('.content').getall()
```

**蜘蛛爬虫：**
```python
from scrapling.spiders import Spider, Response

class MySpider(Spider):
    name = "demo"
    start_urls = ["https://example.com"]
    
    async def parse(self, response: Response):
        for item in response.css('.item'):
            yield {"title": item.css('h2::text').get()}

MySpider().start()
```

## 📚 文档资源

- **主文档**：/workspace/agent-skill/Scrapling-Skill/SKILL.md
- **快速入门**：/workspace/agent-skill/Scrapling-Skill/QUICKSTART.md
- **示例代码**：/workspace/agent-skill/Scrapling-Skill/examples/

## ⚠️ 重要提示

1. **安全标志**：CLI 命令使用 `--ai-targeted`
   ```bash
   scrapling extract get "URL" content.md --ai-targeted
   ```

2. **遵循规则**：
   - ✅ 只抓取授权内容
   - ✅ 遵守 robots.txt
   - ✅ 添加适当延迟
   - ❌ 不绕过付费墙
   - ❌ 不抓取敏感信息

3. **遇到问题**：
   - 查看文档：/workspace/agent-skill/Scrapling-Skill/QUICKSTART.md
   - 运行测试：bash /workspace/agent-skill/Scrapling-Skill/test-mcp-config.sh

## 🎉 恭喜！

Scrapling MCP 现在已完全配置并可以使用！

在 Trae 中直接问我任何网页抓取相关的问题，我会使用这些工具来帮助您！

---
*版本：Scrapling v0.4.8*
*配置日期：2024年*
