# 电影网站爬虫 - 使用说明

## 概述

这是一个使用 Scrapling 框架的专业爬虫，专门设计用于爬取电影网站的数据。

## 功能特性

- ✅ **自动处理5秒盾防护** - 使用 stealth 浏览器模式
- ✅ **并发爬取** - 同时处理多个请求，速度更快
- ✅ **智能分页** - 自动识别并爬取10页
- ✅ **完整数据** - 提取标题、链接、图片、评分、简介等
- ✅ **多格式导出** - 支持 JSON 和 CSV 格式
- ✅ **实时统计** - 显示爬取进度和详细信息

## 文件说明

| 文件 | 说明 |
|------|------|
| `scrape_movies.py` | 主要的爬虫脚本 |
| `test_connection.py` | 连接测试脚本（先运行这个） |
| `README.md` | 本文档 |

## 快速开始

### 1. 环境配置

确保你已经按照 Scrapling 官方文档安装好了环境：

```bash
# 安装 Scrapling
pip install "scrapling[all]>=0.4.8"

# 安装浏览器依赖
scrapling install --force
```

### 2. 测试连接

在开始完整爬取之前，建议先测试网站连接：

```bash
python test_connection.py
```

这个脚本会：
- 先用简单HTTP请求尝试连接
- 再用stealth浏览器模式尝试
- 显示找到的电影数量

### 3. 运行爬虫

连接测试通过后，运行主爬虫：

```bash
python scrape_movies.py
```

## 配置说明

### 调整爬取页数

在 `scrape_movies.py` 中修改：

```python
class MovieSpider(Spider):
    pages_to_scrape = 10  # 修改这个数字
```

### 调整并发数

```python
class MovieSpider(Spider):
    concurrent_requests = 5  # 同时处理的请求数
```

### 查看浏览器操作（调试）

如果你想看到浏览器实际操作：

```python
AsyncStealthySession(
    headless=False,  # 改为 False 显示浏览器
    ...
)
```

## 输出文件

爬虫完成后会生成以下文件：

| 文件 | 说明 |
|------|------|
| `movies.json` | 完整的JSON格式数据 |
| `movies.csv` | CSV格式（Excel可直接打开） |

### 数据结构

每条电影数据包含以下字段：

```json
{
  "index": 1,
  "page": 1,
  "title": "电影标题",
  "url": "/movie/xxx.html",
  "image": "图片URL",
  "brief": "简介内容",
  "douban_score": "豆瓣评分",
  "imdb_score": "IMDB评分",
  "update_date": "更新日期"
}
```

## 常见问题

### Q: 被反爬虫阻挡了怎么办？

A: 我们的脚本已经使用了 Scrapling 的 stealth 模式：
- 自动处理 Cloudflare/Turnstile 验证
- 隐藏浏览器指纹
- 设置 Google 来源头
- 绕过 WebRTC 泄漏

如果仍然被阻挡，试试：
1. 增加 `timeout` 时间
2. 降低 `concurrent_requests` 数值
3. 检查是否需要 `solve_cloudflare=True`

### Q: 可以爬取更多页吗？

A: 可以，修改 `pages_to_scrape` 的值即可。但请遵守网站规则，不要过度爬取。

### Q: 爬取的图片打不开怎么办？

A: 很多图片URL有防盗链机制。如果你需要下载图片，建议：
1. 使用浏览器模式访问图片URL
2. 设置正确的 Referer 头

### Q: 如何继续之前被中断的爬取？

A: 使用 checkpoints 功能（参考 Scrapling 文档）：
```python
MovieSpider(crawldir="./crawl_data").start()
```

## 注意事项

1. **合规使用**：仅爬取您有权限访问的内容
2. **合理频率**：不要对网站造成过大压力
3. **遵守规则**：注意查看网站的 robots.txt
4. **隐私保护**：不要爬取个人敏感数据

## 技术细节

### 为什么使用 Stealth 模式？

- 网站有5秒盾防护
- 需要JavaScript执行
- 需要模拟真实用户行为

### 关于并发

- 默认设置5个并发请求
- 使用浏览器标签池复用
- 可以根据电脑配置调整

## 更多资源

- [Scrapling 官方文档](https://scrapling.readthedocs.io/)
- [Skill 文档](./SKILL.md)
- [Spider 文档](./references/spiders/getting-started.md)
- [Stealth 模式](./references/fetching/stealthy.md)

## 故障排除

### 浏览器启动失败

```bash
# 重新安装浏览器驱动
scrapling install --force
```

### 找不到元素

可能网站结构变化了：
1. 打开网站检查HTML结构
2. 修改CSS选择器
3. 查看 `test_connection.py` 输出的页面内容

### 超时问题

增加 timeout 值：
```python
AsyncStealthySession(
    timeout=90000,  # 改为90秒
    ...
)
```

## 技术支持

如有问题，请查看：
1. 控制台输出的错误信息
2. Scrapling 官方文档
3. Skill 目录中的示例代码

祝您爬取愉快！🎬
