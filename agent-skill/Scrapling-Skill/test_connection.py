#!/usr/bin/env python3
"""
简单的测试脚本 - 验证网站是否可以正常访问

在开始完整爬取前，先用这个脚本测试连接是否正常
"""

from scrapling.fetchers import StealthyFetcher, Fetcher

print("="*60)
print("电影网站 - 连接测试")
print("="*60)

url = "https://www.rrdynb.com/movie/"

print(f"\n测试URL: {url}")
print("\n方法1: 使用简单的HTTP请求...")
try:
    page = Fetcher.get(url, timeout=30)
    print(f"✓ 成功！状态码: {page.status}")
    print(f"页面长度: {len(str(page.body))} 字符")
    
    # 检查是否有电影列表
    movies = page.css("li.pure-g.shadow")
    print(f"找到 {len(movies)} 个电影项目")
    
    if movies:
        print("\n前3个电影标题:")
        for i, movie in enumerate(movies[:3], 1):
            title = movie.css("h2 a::text").get("").strip()
            print(f"  {i}. {title[:50]}...")
    
except Exception as e:
    print(f"✗ 失败: {e}")

print("\n" + "="*60)
print("方法2: 使用 stealth 浏览器模式...")
print("注意: 这可能会需要更长时间")
print("="*60)

try:
    page = StealthyFetcher.fetch(
        url,
        headless=True,
        timeout=60000,  # 60秒
        network_idle=True,
        google_search=True
    )
    print(f"✓ 成功！状态码: {page.status}")
    print(f"页面长度: {len(str(page.body))} 字符")
    
    # 检查是否有电影列表
    movies = page.css("li.pure-g.shadow")
    print(f"找到 {len(movies)} 个电影项目")
    
    if movies:
        print("\n前3个电影标题:")
        for i, movie in enumerate(movies[:3], 1):
            title = movie.css("h2 a::text").get("").strip()
            print(f"  {i}. {title[:50]}...")
    
except Exception as e:
    print(f"✗ 失败: {e}")
    import traceback
    print("\n详细错误信息:")
    print(traceback.format_exc())

print("\n" + "="*60)
print("测试完成！")
print("="*60)
