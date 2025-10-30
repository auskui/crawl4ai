# 🚀 爬虫开发快速开始

## 30秒创建新爬虫

### 1️⃣ 复制模板
```bash
cd crawl4ai/crawlers
cp -r _template my_site
```

### 2️⃣ 修改 `__init__.py`
```python
from .crawler import MySiteCrawler
__all__ = ["MySiteCrawler"]
```

### 3️⃣ 修改 `crawler.py`
```python
from crawl4ai.hub import BaseCrawler
from crawl4ai import AsyncWebCrawler, BrowserConfig
import json

class MySiteCrawler(BaseCrawler):
    __meta__ = {
        "version": "1.0.0",
        "tested_on": ["mysite.com"],
        "rate_limit": "10 RPM",
        "description": "爬取 MySite 数据"
    }
    
    async def run(self, url: str, **kwargs) -> str:
        try:
            browser_config = BrowserConfig(headless=True)
            async with AsyncWebCrawler(config=browser_config) as crawler:
                result = await crawler.arun(url=url)
                
                if not result.success:
                    return json.dumps({"error": result.error})
                
                # TODO: 提取数据
                data = {"title": "示例"}
                
                return json.dumps({
                    "success": True,
                    "data": data
                }, ensure_ascii=False)
        except Exception as e:
            self.logger.error(f"错误: {e}", exc_info=True)
            return json.dumps({"error": str(e)})
```

### 4️⃣ 使用
```python
from crawl4ai.crawlers.my_site import MySiteCrawler
import asyncio

async def main():
    crawler = MySiteCrawler()
    result = await crawler.run(url="https://mysite.com")
    print(result)

asyncio.run(main())
```

## 📋 命名速查表

| 类型 | 格式 | 示例 |
|------|------|------|
| 文件夹 | 小写+下划线 | `amazon_product`, `google_search` |
| 类名 | PascalCase+Crawler | `AmazonProductCrawler` |
| 方法 | 小写+下划线 | `run`, `_extract_data` |

## 🔧 常用功能

### 加载 JavaScript
```python
def __init__(self):
    super().__init__()
    js_file = Path(__file__).parent / "script.js"
    self.js_script = js_file.read_text()

async def run(self, url: str, **kwargs) -> str:
    config = CrawlerRunConfig(js_code=self.js_script)
```

### 加载配置
```python
def __init__(self):
    super().__init__()
    config_file = Path(__file__).parent / "config.json"
    with open(config_file) as f:
        self.config = json.load(f)
```

### 数据提取（BeautifulSoup）
```python
from bs4 import BeautifulSoup

def _extract_data(self, result):
    soup = BeautifulSoup(result.html, 'html.parser')
    return {
        "title": soup.select_one('h1').text.strip(),
        "price": soup.select_one('.price').text.strip()
    }
```

### 错误处理
```python
try:
    result = await crawler.arun(url=url)
    if not result.success:
        return json.dumps({"error": result.error})
except Exception as e:
    self.logger.error(f"错误: {e}", exc_info=True)
    return json.dumps({"error": str(e)})
```

## ✅ 提交检查

- [ ] 文件夹名：小写+下划线
- [ ] 类名：PascalCase+Crawler
- [ ] 继承 `BaseCrawler`
- [ ] 定义 `__meta__`
- [ ] 实现 `run` 方法
- [ ] 错误处理完善
- [ ] 编写 `README.md`

## 📚 详细文档

- **完整指南**: `docs/CRAWLER_DEVELOPMENT_GUIDE.md`
- **模板**: `crawl4ai/crawlers/_template/`
- **示例**: `crawl4ai/crawlers/google_search/`

---

**提示**: 始终从 `_template` 开始，不要从零编写！

