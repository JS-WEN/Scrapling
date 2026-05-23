#!/usr/bin/env python3
"""
Scrapling 演示脚本
抓取名人名言网站并保存到 JSON 文件
"""

from scrapling.fetchers import Fetcher

def scrape_quotes():
    print("🚀 开始抓取 https://quotes.toscrape.com/")
    
    # 使用 Fetcher 抓取页面
    page = Fetcher.get('https://quotes.toscrape.com/')
    
    # 检查是否成功
    print(f"✅ 状态码: {page.status}")
    
    # 提取名言
    quotes = page.css('.quote .text::text').getall()
    authors = page.css('.author::text').getall()
    
    # 组合数据
    results = []
    for quote, author in zip(quotes, authors):
        results.append({
            "quote": quote,
            "author": author
        })
    
    # 保存到 JSON
    import json
    with open('quotes.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"📝 成功抓取 {len(results)} 条名言！")
    print(f"💾 已保存到 quotes.json")
    
    # 显示前 3 条
    print("\n🎉 前 3 条名言：")
    for i, item in enumerate(results[:3], 1):
        print(f"\n{i}. \"{item['quote']}\"")
        print(f"   — {item['author']}")

if __name__ == "__main__":
    scrape_quotes()

