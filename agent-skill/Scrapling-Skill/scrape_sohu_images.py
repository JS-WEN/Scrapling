#!/usr/bin/env python3
"""
抓取搜狐网页上的图片
"""

import os
import urllib.request
from urllib.parse import urljoin, urlparse
from scrapling.fetchers import Fetcher

def download_image(url, folder, index):
    """下载图片到本地"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        req = urllib.request.Request(url, headers=headers)
        
        with urllib.request.urlopen(req, timeout=10) as response:
            if response.status == 200:
                # 获取文件扩展名
                ext = os.path.splitext(urlparse(url).path)[1]
                if not ext or len(ext) > 5:
                    ext = '.jpg'
                
                filename = f"image_{index}{ext}"
                filepath = os.path.join(folder, filename)
                
                with open(filepath, 'wb') as f:
                    f.write(response.read())
                
                print(f"✅ 下载成功: {filename}")
                return filepath
            else:
                print(f"❌ 下载失败 (状态码 {response.status}): {url}")
    except Exception as e:
        print(f"❌ 下载异常: {url[:80]}...")
        print(f"   错误: {type(e).__name__}")
    return None

def scrape_images(url):
    print(f"🚀 开始抓取: {url}")
    
    # 创建图片保存目录
    images_folder = 'sohu_images'
    if not os.path.exists(images_folder):
        os.makedirs(images_folder)
    
    # 抓取页面
    print("📡 正在获取页面内容...")
    page = Fetcher.get(url)
    print(f"✅ 状态码: {page.status}")
    
    # 提取所有图片
    print("🔍 正在查找图片...")
    
    # 使用不同的 CSS 选择器查找图片
    img_selectors = [
        'img::attr(src)',
        'img::attr(data-src)',
        'img::attr(data-original)',
    ]
    
    all_images = []
    for selector in img_selectors:
        images = page.css(selector).getall()
        if images:
            all_images.extend(images)
    
    # 去重
    all_images = list(set(all_images))
    print(f"🎯 找到 {len(all_images)} 张图片")
    
    # 下载图片
    print(f"\n📥 开始下载图片到 {images_folder}/...")
    
    downloaded = []
    for i, img_url in enumerate(all_images, 1):
        # 处理相对 URL
        if not img_url:
            continue
            
        if img_url.startswith('//'):
            img_url = 'https:' + img_url
        elif img_url.startswith('/'):
            img_url = urljoin(url, img_url)
        elif not img_url.startswith(('http://', 'https://')):
            img_url = urljoin(url, img_url)
        
        print(f"\n[{i}/{len(all_images)}] {img_url[:60]}...")
        
        filepath = download_image(img_url, images_folder, i)
        if filepath:
            downloaded.append({
                'index': i,
                'url': img_url,
                'path': filepath
            })
    
    # 显示结果
    print(f"\n✨ 下载完成！")
    print(f"✅ 成功下载: {len(downloaded)}/{len(all_images)} 张图片")
    print(f"📂 保存位置: {os.path.abspath(images_folder)}")
    
    # 保存图片列表到 JSON
    import json
    result_file = 'sohu_images_list.json'
    with open(result_file, 'w', encoding='utf-8') as f:
        json.dump(downloaded, f, ensure_ascii=False, indent=2)
    
    print(f"📝 图片列表已保存到: {result_file}")
    
    # 显示前几张
    print(f"\n🎉 下载的图片:")
    for img in downloaded[:8]:
        print(f"   [{img['index']}] {os.path.basename(img['path'])}")
    if len(downloaded) > 8:
        print(f"   ... 还有 {len(downloaded) - 8} 张图片")
    
    return downloaded

if __name__ == "__main__":
    target_url = "https://www.sohu.com/a/810141508_121984121"
    scrape_images(target_url)

