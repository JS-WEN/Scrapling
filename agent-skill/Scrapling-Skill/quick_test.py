#!/usr/bin/env python3
"""
快速测试 - 只爬取1页看看效果
"""

from scrapling.fetchers import Fetcher

print("="*60)
print("快速测试 - 爬取第1页")
print("="*60)

url = "https://www.rrdynb.com/movie/"
print(f"\n正在获取: {url}")

page = Fetcher.get(url, impersonate="chrome")
print(f"状态码: {page.status}")

movies = page.css("li.pure-g.shadow")
print(f"找到 {len(movies)} 部电影")

print(f"\n{'='*60}")
print("电影列表:")
print("="*60)

all_movies = []

for idx, movie in enumerate(movies, 1):
    # 电影标题和链接
    title_links = movie.css("div.intro h2 a")
    title = ""
    movie_url = ""
    
    if title_links:
        title_link = title_links[0]
        title = title_link.css("::text").get("").strip()
        title = title.replace("免费电影下载", "").strip()
        
        # 获取href属性
        if hasattr(title_link, 'attrib'):
            movie_url = title_link.attrib.get("href", "")
        elif hasattr(title_link, 'attributes'):
            movie_url = title_link.attributes.get("href", "")
    
    # 评分
    douban_elems = movie.css("div.dou b")
    douban = douban_elems.css("::text").get("") if douban_elems else ""
    
    imdb_elems = movie.css("div.imdb b")
    imdb = imdb_elems.css("::text").get("") if imdb_elems else ""
    
    movie_data = {
        "index": idx,
        "title": title,
        "url": movie_url,
        "douban_score": douban,
        "imdb_score": imdb
    }
    
    all_movies.append(movie_data)
    
    print(f"\n{idx}. {title}")
    if douban:
        print(f"   豆瓣: {douban}")
    if imdb:
        print(f"   IMDB: {imdb}")
    print(f"   链接: {movie_url}")

print(f"\n{'='*60}")
print(f"总共: {len(all_movies)} 部电影")
print("="*60)

# 保存结果
import json
with open("quick_test.json", "w", encoding="utf-8") as f:
    json.dump(all_movies, f, ensure_ascii=False, indent=2)

print("\n结果已保存到: quick_test.json")
