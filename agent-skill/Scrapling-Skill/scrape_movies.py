#!/usr/bin/env python3
"""
电影网站爬虫 - 使用 Scrapling 框架

功能：
- 支持两种模式：简单HTTP模式 和 Stealth浏览器模式
- 多线程/并发爬取
- 爬取10页电影列表
- 保存为JSON格式
- 包含完整的电影信息

网站：https://www.rrdynb.com/movie/
"""

from scrapling.spiders import Spider, Response
from scrapling.fetchers import FetcherSession, AsyncStealthySession

# 配置 - 可修改
USE_STEALTH_MODE = False  # 设为 True 使用浏览器模式（需要浏览器驱动）
PAGES_TO_SCRAPE = 10      # 爬取页数
CONCURRENT_REQUESTS = 5   # 并发数


class MovieSpider(Spider):
    name = "movie_spider"
    start_urls = ["https://www.rrdynb.com/movie/"]
    concurrent_requests = CONCURRENT_REQUESTS
    pages_to_scrape = PAGES_TO_SCRAPE
    current_page = 0

    def configure_sessions(self, manager):
        """配置会话"""
        if USE_STEALTH_MODE:
            print("使用 Stealth 浏览器模式...")
            manager.add(
                "stealth",
                AsyncStealthySession(
                    headless=True,
                    solve_cloudflare=False,
                    block_webrtc=True,
                    hide_canvas=True,
                    google_search=True,
                    timeout=60000,
                    max_pages=5,
                ),
                default=True,
            )
        else:
            print("使用快速 HTTP 模式...")
            manager.add(
                "http",
                FetcherSession(
                    impersonate="chrome",
                    stealthy_headers=True
                ),
                default=True,
            )

    async def parse(self, response: Response):
        """解析电影列表页面"""
        self.current_page += 1
        print(f"\n{'='*60}")
        print(f"正在处理第 {self.current_page} 页")
        print(f"URL: {response.url}")
        print(f"状态码: {response.status}")
        print(f"{'='*60}")

        # 找到所有电影项目
        movie_items = response.css("li.pure-g.shadow")

        if not movie_items:
            print("警告：没有找到电影项目！页面结构可能已改变")
            print("\n页面内容预览:")
            print(response.body[:1000])

        for idx, movie in enumerate(movie_items, 1):
            # 提取电影信息
            movie_data = self.extract_movie_data(movie, idx)
            yield movie_data

        # 打印当前页统计
        print(f"\n第 {self.current_page} 页完成！提取到 {len(movie_items)} 部电影")

        # 分页处理
        if self.current_page < self.pages_to_scrape:
            next_url = self.get_next_page_url(response)
            if next_url:
                print(f"\n准备访问下一页: {next_url}")
                yield response.follow(next_url, callback=self.parse)
            else:
                print("\n没有找到下一页链接，提前结束")
        else:
            print(f"\n已完成 {self.pages_to_scrape} 页的爬取！")

    def extract_movie_data(self, movie_element, index):
        """从电影元素中提取完整信息"""
        # 电影标题和链接
        title_links = movie_element.css("div.intro h2 a")
        title = ""
        movie_url = ""
        
        if title_links:
            title_link = title_links[0]
            title = title_link.css("::text").get("").strip()
            title = title.replace("免费电影下载", "").strip()
            
            # 使用 ::attr(href) 获取链接
            movie_url = title_link.css("::attr(href)").get("")

        # 电影图片
        img_elements = movie_element.css("img.pure-img")
        img_src = ""
        if img_elements:
            img = img_elements[0]
            img_src = img.css("::attr(data-original)").get("")
            if not img_src:
                img_src = img.css("::attr(src)").get("")

        # 电影简介
        brief_elements = movie_element.css("div.brief")
        brief_text = ""
        if brief_elements:
            brief_text = brief_elements[0].get_all_text(strip=True)

        # 评分信息
        douban_elements = movie_element.css("div.dou b")
        douban_score = ""
        if douban_elements:
            douban_score = douban_elements.css("::text").get("")

        imdb_elements = movie_element.css("div.imdb b")
        imdb_score = ""
        if imdb_elements:
            imdb_score = imdb_elements.css("::text").get("")

        # 更新时间
        tags_elements = movie_element.css("div.tags")
        update_date = ""
        if tags_elements:
            tag_texts = tags_elements.css("::text").getall()
            for t in tag_texts:
                t = t.strip()
                if t and "-" in t:
                    update_date = t
                    break

        return {
            "index": index,
            "page": self.current_page,
            "title": title,
            "url": movie_url,
            "image": img_src,
            "brief": brief_text,
            "douban_score": douban_score,
            "imdb_score": imdb_score,
            "update_date": update_date,
        }

    def get_next_page_url(self, response):
        """获取下一页的URL"""
        # 尝试找到下一页链接
        page_links = response.css("div.pagea a")

        # 策略1: 查找有"下一页"文字的链接
        for link in page_links:
            link_text = link.css("::text").get("").strip()
            if "下一页" in link_text:
                return link.css("::attr(href)").get("")

        # 策略2: 根据页码找下一个
        current_page_num = -1
        page_numbers = response.css("div.pagea li")
        for li in page_numbers:
            if "thisclass" in li.css("::attr(class)").get(""):
                num_text = li.css("::text").get("").strip()
                if num_text.isdigit():
                    current_page_num = int(num_text)
                    break

        if current_page_num > 0:
            next_num = current_page_num + 1
            for link in page_links:
                href = link.css("::attr(href)").get("")
                if href and str(next_num) in href:
                    return href

        # 策略3: 从select下拉菜单中找
        select_options = response.css("select[name='sldd'] option")
        for opt in select_options:
            opt_text = opt.css("::text").get("").strip()
            if opt_text.isdigit():
                opt_num = int(opt_text)
                if opt_num == self.current_page + 1:
                    return opt.css("::attr(value)").get("")

        return ""


if __name__ == "__main__":
    print("="*60)
    print("电影网站爬虫 - Scrapling 版本")
    print("="*60)
    print(f"目标网站: https://www.rrdynb.com/movie/")
    print(f"模式: {'Stealth浏览器' if USE_STEALTH_MODE else '快速HTTP'}")
    print(f"爬取页数: {PAGES_TO_SCRAPE}")
    print(f"并发数: {CONCURRENT_REQUESTS}")
    print("="*60)
    print("\n开始爬取...\n")

    # 运行爬虫
    result = MovieSpider().start()

    # 打印结果统计
    print(f"\n{'='*60}")
    print("爬取完成统计")
    print(f"{'='*60}")
    print(f"电影数量: {result.stats.items_scraped}")
    print(f"请求次数: {result.stats.requests_count}")
    print(f"用时: {result.stats.elapsed_seconds:.2f}秒")
    print(f"速度: {result.stats.requests_per_second:.2f} 请求/秒")
    print(f"{'='*60}")

    # 显示前10个结果
    print("\n前10个电影数据:")
    print("-"*60)
    for i, item in enumerate(result.items[:10], 1):
        print(f"\n{i}. {item['title']}")
        print(f"   页面: 第{item['page']}页")
        if item['douban_score']:
            print(f"   豆瓣评分: {item['douban_score']}")
        if item['imdb_score']:
            print(f"   IMDB评分: {item['imdb_score']}")
        if item['update_date']:
            print(f"   更新时间: {item['update_date']}")
        print(f"   链接: {item['url']}")

    if len(result.items) > 10:
        print(f"\n...还有 {len(result.items) - 10} 部电影")

    # 导出数据
    output_file = "movies.json"
    result.items.to_json(output_file, indent=True)
    print(f"\n数据已保存到: {output_file}")

    # 保存CSV格式
    try:
        csv_file = "movies.csv"
        import csv
        with open(csv_file, "w", encoding="utf-8-sig", newline="") as f:
            if result.items:
                fieldnames = list(result.items[0].keys())
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(result.items)
        print(f"CSV格式已保存到: {csv_file}")
    except Exception as e:
        print(f"CSV保存失败: {e}")

    print("\n完成！")
