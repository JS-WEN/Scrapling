# Quick Start Guide for Trae MCP Mode

## Prerequisites

- Python 3.10+
- Trae IDE with MCP support

## Installation Steps

### 1. Install Scrapling

```bash
# Create and activate virtual environment
python -m venv scrapling-env
source scrapling-env/bin/activate  # Linux/Mac
# or: scrapling-env\Scripts\activate  # Windows

# Install with all features
pip install "scrapling[all]>=0.4.8"

# Download browser dependencies
scrapling install --force
```

### 2. Configure Trae MCP

Copy the appropriate config file to your Trae MCP configuration:

**Option A: Using uvx (recommended)**
```bash
cp trae-mcp-config.json ~/.config/trae/mcp_servers.json
```

**Option B: Using Docker**
```bash
cp trae-mcp-config-docker.json ~/.config/trae/mcp_servers.json
```

Or manually add to your MCP configuration:
```json
{
  "mcpServers": {
    "scrapling": {
      "command": "uvx",
      "args": ["scrapling", "mcp"]
    }
  }
}
```

### 3. Restart Trae

After configuring, restart Trae to load the MCP server.

## Usage Patterns

### Pattern 1: Simple HTTP Requests

For static websites without JavaScript or bot protection:

```
Use: `scrapling extract get` or MCP `get` tool
```

Example:
```bash
scrapling extract get "https://quotes.toscrape.com/" quotes.md
```

### Pattern 2: JavaScript-Rendered Pages

For SPAs and dynamic content:

```
Use: `scrapling extract fetch` or MCP `fetch` tool
```

Example:
```bash
scrapling extract fetch "https://example.com" content.md --network-idle
```

### Pattern 3: Protected Sites (Cloudflare)

For sites with anti-bot protection:

```
Use: `scrapling extract stealthy-fetch` or MCP `stealthy_fetch` tool
```

Example:
```bash
scrapling extract stealthy-fetch "https://example.com" content.md --solve-cloudflare
```

### Pattern 4: Large-Scale Crawling

For multi-page crawls with pause/resume:

```
Use: Python Spider framework
```

Example script:
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

## MCP Tools Reference

### For Quick Tasks

| Task | Tool | Example |
|------|------|---------|
| Single static page | `get` | `get(url="https://example.com")` |
| Multiple static pages | `bulk_get` | `bulk_get(urls=[...])` |
| Single dynamic page | `fetch` | `fetch(url="https://example.com")` |
| Multiple dynamic pages | `bulk_fetch` | `bulk_fetch(urls=[...])` |

### For Protected Sites

| Task | Tool | Example |
|------|------|---------|
| Cloudflare bypass | `stealthy_fetch` | `stealthy_fetch(url, solve_cloudflare=true)` |
| Multiple protected | `bulk_stealthy_fetch` | `bulk_stealthy_fetch(urls, ...)` |

### For Sessions

| Task | Tool | Example |
|------|------|---------|
| Create session | `open_session` | `open_session(session_type="dynamic")` |
| Close session | `close_session` | `close_session(session_id="abc123")` |
| List sessions | `list_sessions` | `list_sessions()` |
| Screenshot | `screenshot` | `screenshot(url, session_id)` |

## Common Use Cases

### 1. Extract Article Content

```bash
scrapling extract get "https://blog.example.com/post" article.md \
  --css-selector "article.content" \
  --ai-targeted
```

### 2. Scrape Product Listings

```python
from scrapling.fetchers import Fetcher

page = Fetcher.get('https://shop.example.com/products')
products = []

for item in page.css('.product-card'):
    products.append({
        "name": item.css('.title::text').get(),
        "price": item.css('.price::text').get(),
        "url": item.css('a::attr(href)').get()
    })
```

### 3. Multi-Page Crawl with Checkpoints

```python
from scrapling.spiders import Spider, Response

class ProductSpider(Spider):
    name = "products"
    start_urls = ["https://shop.example.com"]
    concurrent_requests = 5
    robots_txt_obey = True
    
    async def parse(self, response: Response):
        for product in response.css('.product'):
            yield {
                "name": product.css('.title::text').get(),
                "price": product.css('.price::text').get()
            }
        
        # Follow pagination
        next_page = response.css('.next a')
        if next_page:
            yield response.follow(next_page[0])

# Run with checkpointing
ProductSpider(crawldir="./crawl_data").start()
# Press Ctrl+C to pause gracefully
```

### 4. Stealth Browsing with Proxy

```python
from scrapling.fetchers import StealthySession

with StealthySession(
    headless=True,
    solve_cloudflare=True,
    proxy="http://user:pass@proxy.example.com:8080"
) as session:
    page = session.fetch('https://protected.example.com')
    data = page.css('.content').getall()
```

## Best Practices

### 1. Start Simple
- Begin with `get` for static pages
- Only escalate to `fetch` if needed
- Use `stealthy_fetch` only for protected sites

### 2. Respect Website Policies
- Always check robots.txt
- Add delays between requests
- Don't scrape personal data
- Respect rate limits

### 3. Use CSS Selectors
- Narrow down content with selectors to save tokens
- Example: `--css-selector "article.content"` instead of getting entire page

### 4. Handle Errors Gracefully
```python
from scrapling.fetchers import Fetcher

try:
    page = Fetcher.get('https://example.com', timeout=30, retries=3)
    data = page.css('.content').getall()
except Exception as e:
    print(f"Error: {e}")
```

### 5. Enable AI-targeted for CLI
- Always use `--ai-targeted` flag to prevent prompt injection
- This also enables ad blocking automatically

## Troubleshooting

### Issue: Browser not found

```bash
scrapling install --force
```

### Issue: Timeout errors

```python
page = Fetcher.get('https://example.com', timeout=60)
```

Or with CLI:
```bash
scrapling extract get "https://example.com" content.md --timeout 60
```

### Issue: Blocked by Cloudflare

```python
from scrapling.fetchers import StealthyFetcher

page = StealthyFetcher.fetch('https://example.com', solve_cloudflare=True)
```

### Issue: JavaScript not loaded

```python
page = DynamicFetcher.fetch('https://example.com', network_idle=True)
```

Or with CLI:
```bash
scrapling extract fetch "https://example.com" content.md --network-idle
```

## Next Steps

1. Read **SKILL.md** for complete documentation
2. Check **examples/** directory for ready-to-use scripts
3. Review **references/** for detailed guides
4. Join the [Discord community](https://discord.gg/EMgGbDceNQ) for help

## Version

**Scrapling v0.4.8**
**Last Updated: 2024**

For more information, visit:
- [Documentation](https://scrapling.readthedocs.io/)
- [GitHub Repository](https://github.com/D4Vinci/Scrapling)
