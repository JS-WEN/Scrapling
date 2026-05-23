#!/usr/bin/env python3
"""
抓取搜狐网页上的图片 - 增强版
处理防盗链和重定向问题
"""

import os
import urllib.request
import urllib.parse
import http.cookiejar
from urllib.parse import urljoin, urlparse
from scrapling.fetchers import Fetcher

class ImageDownloader:
    def __init__(self):
        self.cookie_jar = http.cookiejar.CookieJar()
        self.opener = urllib.request.build_opener(
            urllib.request.HTTPCookieProcessor(self.cookie_jar),
            urllib.request.HTTPSHandler()
        )
        
    def download_image(self, url, folder, index):
        """下载图片到本地"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Referer': 'https://www.sohu.com/',
                'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
            }
            
            req = urllib.request.Request(url, headers=headers)
            
            with self.opener.open(req, timeout=15) as response:
                content_type = response.headers.get('Content-Type', '')
                
                # 检查是否是 HTML（防盗链重定向）
                if 'text/html' in content_type or response.url != url:
                    print(f"⚠️  遇到防盗链，跳过: {url[:50]}...")
                    return None
                
                # 获取内容
                data = response.read()
                
                # 检查文件头
                if len(data) < 1000 or data[:5] in (b'<!DOC', b'<html', b'<HTML'):
                    print(f"⚠️  内容无效，跳过: {url[:50]}...")
                    return None
                
                # 确定文件扩展名
                ext = self.get_extension(content_type, url)
                filename = f"image_{index:03d}{ext}"
                filepath = os.path.join(folder, filename)
                
                with open(filepath, 'wb') as f:
                    f.write(data)
                
                size = len(data) / 1024  # KB
                print(f"✅ 下载成功: {filename} ({size:.1f} KB)")
                return filepath
                
        except urllib.error.HTTPError as e:
            print(f"❌ HTTP错误 {e.code}: {url[:50]}...")
        except Exception as e:
            print(f"❌ 下载异常: {url[:50]}...")
        return None
    
    def get_extension(self, content_type, url):
        """获取文件扩展名"""
        # 从 Content-Type 获取
        if 'jpeg' in content_type or 'jpg' in content_type:
            return '.jpg'
        elif 'png' in content_type:
            return '.png'
        elif 'gif' in content_type:
            return '.gif'
        elif 'webp' in content_type:
            return '.webp'
        
        # 从 URL 获取
        path = urlparse(url).path
        ext = os.path.splitext(path)[1].lower()
        if ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp']:
            return ext
        
        return '.jpg'  # 默认

def scrape_images(url):
    print(f"🚀 开始抓取: {url}")
    print("=" * 60)
    
    # 创建图片保存目录
    images_folder = 'sohu_images_fixed'
    if not os.path.exists(images_folder):
        os.makedirs(images_folder)
    
    # 抓取页面
    print("📡 正在获取页面内容...")
    page = Fetcher.get(url)
    print(f"✅ 状态码: {page.status}")
    
    # 先获取页面 HTML 保存下来
    html_file = os.path.join(images_folder, 'page_source.html')
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(str(page.body))
    print(f"📝 页面源码已保存: {html_file}")
    
    # 提取所有图片
    print("\n🔍 正在查找图片...")
    
    img_selectors = [
        'img::attr(src)',
        'img::attr(data-src)',
        'img::attr(data-original)',
        'img::attr(data-url)',
        'img::attr(lazy-src)',
    ]
    
    all_images = []
    seen = set()
    
    for selector in img_selectors:
        images = page.css(selector).getall()
        for img_url in images:
            if img_url and img_url not in seen:
                # 过滤掉小图标和跟踪像素
                if any(skip in img_url.lower() for skip in ['icon', 'logo', 'pixel', 'tracking', '1x1', 'spacer']):
                    continue
                seen.add(img_url)
                all_images.append(img_url)
    
    print(f"🎯 找到 {len(all_images)} 个图片 URL")
    
    # 显示前几个 URL
    print("\n📋 前 5 个图片 URL:")
    for i, img_url in enumerate(all_images[:5], 1):
        print(f"   {i}. {img_url[:70]}...")
    
    # 下载图片
    print(f"\n📥 开始下载图片到 {images_folder}/...")
    print("=" * 60)
    
    downloader = ImageDownloader()
    downloaded = []
    
    for i, img_url in enumerate(all_images, 1):
        # 处理相对 URL
        if not img_url or img_url == '#' or img_url.startswith('javascript'):
            continue
            
        if img_url.startswith('//'):
            img_url = 'https:' + img_url
        elif img_url.startswith('/'):
            img_url = urljoin(url, img_url)
        elif not img_url.startswith(('http://', 'https://')):
            img_url = urljoin(url, img_url)
        
        print(f"\n[{i}/{len(all_images)}] 正在处理...")
        
        filepath = downloader.download_image(img_url, images_folder, len(downloaded) + 1)
        if filepath:
            downloaded.append({
                'index': len(downloaded) + 1,
                'url': img_url,
                'path': filepath
            })
    
    # 显示结果
    print("\n" + "=" * 60)
    print(f"✨ 下载完成！")
    print(f"✅ 成功下载: {len(downloaded)}/{len(all_images)} 张图片")
    print(f"📂 保存位置: {os.path.abspath(images_folder)}")
    
    # 保存图片列表
    import json
    result_file = 'downloaded_images_list.json'
    with open(result_file, 'w', encoding='utf-8') as f:
        json.dump(downloaded, f, ensure_ascii=False, indent=2)
    
    print(f"📝 图片列表已保存到: {result_file}")
    
    # 显示成功下载的图片
    if downloaded:
        print(f"\n🎉 成功下载的图片:")
        for img in downloaded[:10]:
            filename = os.path.basename(img['path'])
            size = os.path.getsize(img['path']) / 1024
            print(f"   [{img['index']}] {filename} ({size:.1f} KB)")
        if len(downloaded) > 10:
            print(f"   ... 还有 {len(downloaded) - 10} 张图片")
    else:
        print("\n⚠️  没有成功下载任何图片")
        print("💡 建议：尝试使用浏览器渲染模式（fetch）来获取图片")
    
    return downloaded

if __name__ == "__main__":
    target_url = "https://www.sohu.com/a/810141508_121984121"
    scrape_images(target_url)

