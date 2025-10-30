"""
模板爬虫 - 用于快速创建新的网站爬虫

使用说明：
1. 复制整个 _template 文件夹
2. 重命名为目标网站名称（如：twitter_posts）
3. 修改类名和功能实现
4. 更新 __meta__ 信息
"""
from crawl4ai import BrowserConfig, AsyncWebCrawler, CrawlerRunConfig, CacheMode
from crawl4ai.hub import BaseCrawler
from crawl4ai.utils import get_home_folder
from pathlib import Path
import json
import os
from typing import Dict, Any


class TemplateCrawler(BaseCrawler):
    """
    模板爬虫类
    
    TODO: 修改此类的名称和功能描述
    """
    
    __meta__ = {
        "version": "1.0.0",
        "tested_on": ["example.com"],  # TODO: 修改为实际测试的网站
        "rate_limit": "10 RPM",         # TODO: 设置合适的请求频率
        "description": "这是一个模板爬虫",  # TODO: 修改功能描述
        "author": "",                    # TODO: 添加作者信息
        "tags": ["template"],            # TODO: 添加相关标签
    }

    def __init__(self):
        """初始化爬虫"""
        super().__init__()
        
        # 如果需要加载 JavaScript 脚本
        # js_file = Path(__file__).parent / "script.js"
        # if js_file.exists():
        #     self.js_script = js_file.read_text()
        # else:
        #     self.js_script = None
        
        # 如果需要加载配置文件
        # config_file = Path(__file__).parent / "config.json"
        # if config_file.exists():
        #     with open(config_file, 'r', encoding='utf-8') as f:
        #         self.config = json.load(f)
        # else:
        #     self.config = {}

    async def run(self, url: str = "", **kwargs) -> str:
        """
        执行爬取任务
        
        Args:
            url: 目标URL
            **kwargs: 其他参数
                - cache_mode: 缓存模式，默认 CacheMode.BYPASS
                - headless: 无头模式，默认 True
                - delay: 延迟时间（秒），默认 1
                - ... 其他自定义参数
        
        Returns:
            str: JSON格式的结果字符串
        
        示例:
            ```python
            crawler = TemplateCrawler()
            result = await crawler.run(
                url="https://example.com",
                cache_mode=CacheMode.BYPASS
            )
            data = json.loads(result)
            ```
        """
        try:
            # 1. 验证URL
            if not url:
                return json.dumps({
                    "error": "URL is required",
                    "metadata": self.__meta__
                })
            
            self.logger.info(f"开始爬取: {url}")
            
            # 2. 配置浏览器
            browser_config = BrowserConfig(
                headless=kwargs.get("headless", True),
                verbose=kwargs.get("verbose", False),
                # 其他浏览器配置...
            )
            
            # 3. 配置爬取参数
            crawler_config = CrawlerRunConfig(
                cache_mode=kwargs.get("cache_mode", CacheMode.BYPASS),
                delay_before_return_html=kwargs.get("delay", 1),
                # js_code=self.js_script,  # 如果需要执行JS
                # 其他爬取配置...
            )
            
            # 4. 执行爬取
            async with AsyncWebCrawler(config=browser_config) as crawler:
                result = await crawler.arun(url=url, config=crawler_config)
                
                if not result.success:
                    return json.dumps({
                        "error": result.error,
                        "metadata": self.__meta__
                    })
                
                # 5. 处理数据
                # TODO: 根据实际需求提取和处理数据
                extracted_data = self._extract_data(result)
                
                # 6. 返回结果
                return json.dumps({
                    "success": True,
                    "url": url,
                    "data": extracted_data,
                    "metadata": self.__meta__
                }, indent=2, ensure_ascii=False)
                
        except Exception as e:
            self.logger.error(f"爬取失败: {str(e)}", exc_info=True)
            return json.dumps({
                "success": False,
                "error": str(e),
                "metadata": self.__meta__
            }, ensure_ascii=False)

    def _extract_data(self, result) -> Dict[str, Any]:
        """
        从爬取结果中提取数据
        
        Args:
            result: 爬取结果对象
        
        Returns:
            Dict: 提取的数据
        """
        # TODO: 实现数据提取逻辑
        # 可以使用：
        # - result.html: 原始HTML
        # - result.cleaned_html: 清理后的HTML
        # - result.markdown: Markdown格式
        # - result.links: 提取的链接
        # - BeautifulSoup, lxml等解析库
        
        return {
            "title": "",
            "content": "",
            "links": result.links.get("internal", []) if result.links else [],
            # 其他字段...
        }

    def _validate_data(self, data: Dict) -> bool:
        """
        验证提取的数据是否符合要求
        
        Args:
            data: 待验证的数据
        
        Returns:
            bool: 验证结果
        """
        # TODO: 实现数据验证逻辑
        return True


# 使用示例
if __name__ == "__main__":
    import asyncio
    
    async def main():
        crawler = TemplateCrawler()
        result = await crawler.run(url="https://example.com")
        print(result)
    
    asyncio.run(main())

