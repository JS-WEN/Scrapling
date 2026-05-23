# Scrapling Skill for Trae MCP Mode

This directory contains the official Scrapling skill for AI coding assistants, optimized for use with Trae's MCP mode.

## Overview

Scrapling is an adaptive Web Scraping framework that provides:
- Anti-bot bypass (Cloudflare Turnstile)
- Stealth headless browsing
- Spiders framework for large-scale crawls
- Adaptive parsing that survives website design changes
- JavaScript rendering with Playwright
- MCP server for AI integration

## Quick Start

### 1. Installation

```bash
# Create virtual environment (recommended)
python -m venv scrapling-env
source scrapling-env/bin/activate  # Linux/Mac
# or: scrapling-env\Scripts\activate  # Windows

# Install Scrapling with all features
pip install "scrapling[all]>=0.4.8"

# Download browser dependencies
scrapling install --force
```

### 2. MCP Server Setup

Start the MCP server for AI integration:

```bash
scrapling mcp
```

Or use Docker:

```bash
docker run -i --rm pyd4vinci/scrapling mcp
```

### 3. Using in Trae MCP Mode

When Trae MCP is configured, you can:
- Use CLI commands: `scrapling extract get/post/fetch/stealthy-fetch`
- Write Python scripts using the scrapling library
- Leverage MCP tools for AI-assisted scraping

## Directory Structure

```
Scrapling-Skill/
├── SKILL.md                    # Main skill documentation
├── examples/                   # Example scripts
│   ├── 01_fetcher_session.py  # Basic HTTP scraping
│   ├── 02_dynamic_session.py  # Browser automation
│   ├── 03_stealthy_session.py # Stealth browser
│   ├── 04_spider.py           # Spider framework
│   └── README.md              # Examples guide
├── references/                # Detailed documentation
│   ├── mcp-server.md         # MCP server tools
│   ├── parsing/              # HTML parsing
│   ├── fetching/             # Web fetching
│   ├── spiders/              # Spider framework
│   └── migrating_from_beautifulsoup.md
└── LICENSE.txt               # License
```

## Key Features

### 1. Three Scraping Levels

Start with the fastest option and escalate only if needed:

```
Fetcher (HTTP)
  └─ DynamicFetcher (Browser)
       └─ StealthyFetcher (Anti-bot)
```

### 2. MCP Server Tools

The MCP server provides 10 tools:

| Tool | Purpose |
|------|---------|
| `get` | Fast HTTP GET with fingerprinting |
| `bulk_get` | Concurrent HTTP requests |
| `fetch` | Browser fetch with JS rendering |
| `bulk_fetch` | Concurrent browser fetch |
| `stealthy_fetch` | Anti-bot bypass (Cloudflare) |
| `bulk_stealthy_fetch` | Concurrent stealth fetch |
| `open_session` | Persistent browser sessions |
| `close_session` | Close sessions |
| `list_sessions` | List active sessions |
| `screenshot` | Page screenshots |

### 3. Spider Framework

Full crawling framework with:
- Concurrent request handling
- Multi-session support
- Pause/resume with checkpoints
- Robots.txt compliance
- Streaming mode
- Proxy rotation

## Usage Examples

### CLI Commands

```bash
# Basic HTTP request
scrapling extract get "https://example.com" content.md

# Browser fetch with JS rendering
scrapling extract fetch "https://example.com" page.md

# Stealth fetch for protected sites
scrapling extract stealthy-fetch "https://example.com" content.md --solve-cloudflare

# With CSS selector
scrapling extract get "https://example.com" articles.md --css-selector "article"
```

### Python Scripts

**Basic HTTP:**
```python
from scrapling.fetchers import Fetcher

page = Fetcher.get('https://quotes.toscrape.com/')
quotes = page.css('.quote .text::text').getall()
```

**Browser Automation:**
```python
from scrapling.fetchers import DynamicSession

with DynamicSession() as session:
    page = session.fetch('https://example.com')
    data = page.css('.content').getall()
```

**Spider Framework:**
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

## Documentation

- **SKILL.md** - Complete skill documentation with examples
- **references/mcp-server.md** - Detailed MCP server usage
- **references/parsing/** - HTML parsing documentation
- **references/fetching/** - Web fetching guides
- **references/spiders/** - Spider framework docs
- **examples/** - Ready-to-use example scripts

## Important Notes

### Security & Ethics
- Only scrape authorized content
- Respect robots.txt and Terms of Service
- Add delays for large crawls
- Never scrape personal/sensitive data

### CLI Security
- Always use `--ai-targeted` flag with CLI commands to prevent prompt injection
- This also enables automatic ad blocking

### Anti-bot Bypass
- Cloudflare solving uses automation (no solvers needed)
- Proxy usage is optional and user-provided
- All arguments are validated internally

## Version

**Version: 0.4.8**
**Requires: Python 3.10+**

## License

See LICENSE.txt for full license details.

## Links

- [Documentation](https://scrapling.readthedocs.io/)
- [GitHub Repository](https://github.com/D4Vinci/Scrapling)
- [Discord Community](https://discord.gg/EMgGbDceNQ)
- [Official Docs](https://github.com/D4Vinci/Scrapling/tree/main/docs)
