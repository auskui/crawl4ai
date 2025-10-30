# Crawl4AI 爬虫开发指南

本指南详细说明如何在 Crawl4AI 项目中开发和管理网站特定的爬虫脚本。

## 📚 目录

- [概述](#概述)
- [快速开始](#快速开始)
- [目录结构](#目录结构)
- [开发规范](#开发规范)
- [最佳实践](#最佳实践)
- [测试与调试](#测试与调试)
- [部署与维护](#部署与维护)

## 概述

Crawl4AI 使用模块化的爬虫架构，每个网站的爬虫放在独立的文件夹中，便于：

- ✅ **模块化管理**: 每个网站独立维护
- ✅ **代码复用**: 基于 `BaseCrawler` 基类
- ✅ **易于扩展**: 遵循统一的接口规范
- ✅ **便于测试**: 独立的测试和配置

## 快速开始

### 1. 创建新爬虫

```bash
# 复制模板文件夹
cd /Users/admin/tao/crawl4ai/crawl4ai/crawlers
cp -r _template your_site_name

# 修改文件
cd your_site_name
# 编辑 crawler.py, __init__.py, README.md
```

### 2. 实现爬虫类

```python
# crawler.py
from crawl4ai.hub import BaseCrawler
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig
import json

class YourSiteCrawler(BaseCrawler):
    __meta__ = {
        "version": "1.0.0",
        "tested_on": ["yoursite.com"],
        "rate_limit": "10 RPM",
        "description": "爬取 YourSite 的数据"
    }
    
    async def run(self, url: str, **kwargs) -> str:
        # 实现爬取逻辑
        browser_config = BrowserConfig(headless=True)
        async with AsyncWebCrawler(config=browser_config) as crawler:
            result = await crawler.arun(url=url)
            
            if not result.success:
                return json.dumps({"error": result.error})
            
            # 提取数据
            data = self._extract_data(result)
            return json.dumps(data, ensure_ascii=False)
    
    def _extract_data(self, result):
        # 数据提取逻辑
        return {"title": "示例"}
```

### 3. 更新 __init__.py

```python
from .crawler import YourSiteCrawler

__all__ = ["YourSiteCrawler"]
```

### 4. 使用爬虫

```python
from crawl4ai.crawlers.your_site_name import YourSiteCrawler
import asyncio

async def main():
    crawler = YourSiteCrawler()
    result = await crawler.run(url="https://yoursite.com")
    print(result)

asyncio.run(main())
```

## 目录结构

```
crawl4ai/crawlers/
│
├── README.md                    # 爬虫目录说明
├── _template/                   # 新爬虫模板
│   ├── __init__.py
│   ├── crawler.py
│   ├── config.json
│   ├── script.js
│   └── README.md
│
├── amazon_product/              # Amazon 产品爬虫
│   ├── __init__.py
│   └── crawler.py
│
├── google_search/               # Google 搜索爬虫
│   ├── __init__.py
│   ├── crawler.py
│   └── script.js
│
└── [new_crawler]/               # 新增爬虫
    ├── __init__.py              # 必需：导出爬虫类
    ├── crawler.py               # 必需：爬虫主逻辑
    ├── README.md                # 必需：使用文档
    ├── config.json              # 可选：配置文件
    ├── script.js                # 可选：JS 脚本
    ├── utils.py                 # 可选：辅助函数
    └── schemas/                 # 可选：数据模式定义
```

## 开发规范

### 命名规范

#### 1. 文件夹命名
- 使用小写字母
- 用下划线分隔单词
- 体现网站或功能名称

✅ **好的命名**:
```
twitter_posts
linkedin_profiles
amazon_product
github_repositories
```

❌ **不好的命名**:
```
TwitterPosts      # 不要用大写
twitter-posts     # 不要用连字符
twitter           # 不够具体
tp                # 不要缩写
```

#### 2. 类命名
- 使用 PascalCase
- 以 `Crawler` 结尾
- 体现功能

✅ **好的命名**:
```python
class TwitterPostsCrawler(BaseCrawler):
class LinkedInProfilesCrawler(BaseCrawler):
class AmazonProductCrawler(BaseCrawler):
```

❌ **不好的命名**:
```python
class twitter_posts(BaseCrawler):     # 不要用小写
class TwitterPosts(BaseCrawler):       # 缺少 Crawler 后缀
class TWCrawler(BaseCrawler):          # 不要缩写
```

### 代码结构

#### 1. 基本结构

```python
from crawl4ai.hub import BaseCrawler
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig
import json
from pathlib import Path
from typing import Dict, Any, Optional

class YourCrawler(BaseCrawler):
    """
    爬虫功能描述
    """
    
    # 1. 元数据定义
    __meta__ = {
        "version": "1.0.0",
        "tested_on": ["site.com"],
        "rate_limit": "10 RPM",
        "description": "功能描述",
        "author": "作者名",
        "tags": ["标签1", "标签2"]
    }
    
    # 2. 初始化方法
    def __init__(self):
        super().__init__()
        # 加载配置、脚本等
    
    # 3. 主爬取方法
    async def run(self, url: str, **kwargs) -> str:
        """主要的爬取逻辑"""
        pass
    
    # 4. 辅助方法（私有方法用 _ 前缀）
    def _extract_data(self, result) -> Dict[str, Any]:
        """数据提取"""
        pass
    
    def _validate_data(self, data: Dict) -> bool:
        """数据验证"""
        pass
```

#### 2. 元数据 `__meta__`

必填字段：
```python
__meta__ = {
    "version": "1.0.0",           # 版本号（语义化版本）
    "tested_on": ["site.com"],    # 测试过的网站列表
    "rate_limit": "10 RPM",       # 请求频率限制
    "description": "功能描述"      # 简短的功能说明
}
```

可选字段：
```python
__meta__ = {
    # ... 必填字段 ...
    "author": "Your Name",              # 作者
    "email": "your@email.com",          # 联系邮箱
    "tags": ["ecommerce", "products"],  # 标签
    "dependencies": ["beautifulsoup4"], # 特殊依赖
    "last_tested": "2025-10-20",       # 最后测试日期
    "notes": "特殊说明"                  # 备注
}
```

#### 3. run 方法签名

```python
async def run(self, url: str = "", **kwargs) -> str:
    """
    执行爬取任务
    
    Args:
        url: 目标URL（根据需求可为空）
        **kwargs: 扩展参数
            - cache_mode: CacheMode - 缓存模式
            - headless: bool - 是否无头模式
            - delay: int - 延迟时间（秒）
            - [自定义参数]
    
    Returns:
        str: JSON格式的结果字符串
        
    Example:
        ```python
        crawler = YourCrawler()
        result = await crawler.run(
            url="https://example.com",
            cache_mode=CacheMode.BYPASS
        )
        ```
    """
```

### 错误处理

#### 1. 基本错误处理

```python
async def run(self, url: str, **kwargs) -> str:
    try:
        # 爬取逻辑
        result = await crawler.arun(url=url)
        
        if not result.success:
            return json.dumps({
                "success": False,
                "error": result.error,
                "metadata": self.__meta__
            })
        
        # 处理数据
        return json.dumps({"success": True, "data": data})
        
    except Exception as e:
        self.logger.error(f"爬取失败: {str(e)}", exc_info=True)
        return json.dumps({
            "success": False,
            "error": str(e),
            "metadata": self.__meta__
        })
```

#### 2. 分层错误处理

```python
# 自定义异常
class CrawlerError(Exception):
    """爬虫基础异常"""
    pass

class DataExtractionError(CrawlerError):
    """数据提取异常"""
    pass

class ValidationError(CrawlerError):
    """数据验证异常"""
    pass

# 使用
try:
    data = self._extract_data(result)
except DataExtractionError as e:
    self.logger.warning(f"数据提取失败: {e}")
    return json.dumps({"error": "data_extraction_failed"})
```

### 日志记录

```python
# 使用继承自 BaseCrawler 的 logger
class YourCrawler(BaseCrawler):
    async def run(self, url: str, **kwargs) -> str:
        # 信息日志
        self.logger.info(f"开始爬取: {url}")
        
        # 调试日志
        self.logger.debug(f"配置参数: {kwargs}")
        
        # 警告日志
        if not data:
            self.logger.warning(f"未提取到数据: {url}")
        
        # 错误日志
        try:
            result = await crawler.arun(url)
        except Exception as e:
            self.logger.error(f"爬取失败: {e}", exc_info=True)
```

## 最佳实践

### 1. 配置管理

#### 使用 config.json

```json
{
  "selectors": {
    "title": "h1.title",
    "price": "span.price",
    "description": "div.desc"
  },
  "browser": {
    "headless": true,
    "viewport": {"width": 1920, "height": 1080}
  },
  "crawler": {
    "delay": 1,
    "timeout": 30,
    "retry_times": 3
  }
}
```

```python
class YourCrawler(BaseCrawler):
    def __init__(self):
        super().__init__()
        config_file = Path(__file__).parent / "config.json"
        with open(config_file) as f:
            self.config = json.load(f)
    
    def _get_selector(self, key: str) -> str:
        return self.config["selectors"].get(key, "")
```

### 2. JavaScript 支持

#### script.js 示例

```javascript
(async () => {
    try {
        // 等待元素加载
        await new Promise(resolve => setTimeout(resolve, 2000));
        
        // 滚动加载更多
        window.scrollTo(0, document.body.scrollHeight);
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        // 点击"加载更多"
        const loadMore = document.querySelector('.load-more');
        if (loadMore) loadMore.click();
        
        return {
            success: true,
            itemsCount: document.querySelectorAll('.item').length
        };
    } catch (error) {
        return {
            success: false,
            error: error.message
        };
    }
})();
```

#### 在爬虫中使用

```python
class YourCrawler(BaseCrawler):
    def __init__(self):
        super().__init__()
        js_file = Path(__file__).parent / "script.js"
        self.js_script = js_file.read_text()
    
    async def run(self, url: str, **kwargs) -> str:
        config = CrawlerRunConfig(
            js_code=self.js_script,
            delay_before_return_html=2
        )
        
        result = await crawler.arun(url=url, config=config)
        
        # 获取 JS 执行结果
        if result.js_execution_result:
            js_result = result.js_execution_result
            if not js_result.get("success"):
                self.logger.warning(f"JS执行失败: {js_result.get('error')}")
```

### 3. 数据提取

#### 使用 BeautifulSoup

```python
from bs4 import BeautifulSoup

def _extract_data(self, result) -> Dict[str, Any]:
    soup = BeautifulSoup(result.html, 'html.parser')
    
    return {
        "title": soup.select_one('h1.title').text.strip(),
        "price": soup.select_one('.price').text.strip(),
        "images": [img['src'] for img in soup.select('img.product-img')],
        "description": soup.select_one('.description').text.strip()
    }
```

#### 使用 JsonCssExtractionStrategy

```python
from crawl4ai import JsonCssExtractionStrategy

def _extract_data(self, result) -> Dict[str, Any]:
    schema = {
        "name": "product",
        "baseSelector": ".product-item",
        "fields": [
            {"name": "title", "selector": "h2.title", "type": "text"},
            {"name": "price", "selector": ".price", "type": "text"},
            {"name": "link", "selector": "a", "type": "attribute", "attribute": "href"}
        ]
    }
    
    strategy = JsonCssExtractionStrategy(schema=schema)
    extracted = strategy.run(url=result.url, sections=[result.html])
    return extracted
```

### 4. 反爬虫处理

#### User-Agent 轮换

```python
from crawl4ai.user_agent_generator import UserAgentGenerator

class YourCrawler(BaseCrawler):
    def __init__(self):
        super().__init__()
        self.ua_generator = UserAgentGenerator()
    
    async def run(self, url: str, **kwargs) -> str:
        browser_config = BrowserConfig(
            user_agent=self.ua_generator.generate()
        )
```

#### 代理支持

```python
from crawl4ai.proxy_strategy import ProxyStrategy

async def run(self, url: str, **kwargs) -> str:
    browser_config = BrowserConfig(
        proxy=kwargs.get("proxy"),  # "http://proxy:port"
        proxy_config={
            "server": "http://proxy:port",
            "username": "user",
            "password": "pass"
        }
    )
```

#### 延迟和重试

```python
import asyncio
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10)
)
async def _crawl_with_retry(self, url: str, config) -> Any:
    async with AsyncWebCrawler(config=self.browser_config) as crawler:
        result = await crawler.arun(url=url, config=config)
        if not result.success:
            raise Exception(f"Crawl failed: {result.error}")
        return result
```

### 5. 数据验证

```python
from typing import Optional
from pydantic import BaseModel, validator

class ProductData(BaseModel):
    title: str
    price: float
    url: str
    description: Optional[str] = None
    
    @validator('price')
    def price_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('价格必须大于0')
        return v
    
    @validator('url')
    def url_must_be_valid(cls, v):
        if not v.startswith('http'):
            raise ValueError('URL必须以http开头')
        return v

# 使用
def _validate_and_parse(self, data: Dict) -> ProductData:
    try:
        return ProductData(**data)
    except Exception as e:
        self.logger.error(f"数据验证失败: {e}")
        raise ValidationError(f"Invalid data: {e}")
```

## 测试与调试

### 1. 单元测试

创建 `tests/crawlers/test_your_crawler.py`:

```python
import pytest
import asyncio
import json
from crawl4ai.crawlers.your_crawler import YourCrawler

@pytest.mark.asyncio
async def test_basic_crawl():
    """测试基本爬取功能"""
    crawler = YourCrawler()
    result = await crawler.run(url="https://example.com")
    data = json.loads(result)
    
    assert data["success"] is True
    assert "data" in data
    assert data["data"]["title"]

@pytest.mark.asyncio
async def test_error_handling():
    """测试错误处理"""
    crawler = YourCrawler()
    result = await crawler.run(url="")
    data = json.loads(result)
    
    assert data["success"] is False
    assert "error" in data

@pytest.mark.asyncio
async def test_with_custom_params():
    """测试自定义参数"""
    crawler = YourCrawler()
    result = await crawler.run(
        url="https://example.com",
        cache_mode=CacheMode.ENABLED,
        delay=2
    )
    data = json.loads(result)
    assert data["success"] is True
```

### 2. 调试技巧

#### 启用详细日志

```python
import logging
logging.basicConfig(level=logging.DEBUG)

crawler = YourCrawler()
```

#### 保存 HTML 快照

```python
async def run(self, url: str, **kwargs) -> str:
    result = await crawler.arun(url=url)
    
    # 调试：保存 HTML
    if kwargs.get("debug"):
        debug_file = f"debug_{int(time.time())}.html"
        Path(debug_file).write_text(result.html)
        self.logger.info(f"HTML已保存到: {debug_file}")
```

#### 使用非无头模式

```python
# 可以看到浏览器操作过程
browser_config = BrowserConfig(
    headless=False,
    verbose=True
)
```

## 部署与维护

### 1. 版本管理

遵循语义化版本：

- `MAJOR.MINOR.PATCH`
- `1.0.0` → 初始版本
- `1.0.1` → Bug 修复
- `1.1.0` → 新功能
- `2.0.0` → 破坏性更新

```python
__meta__ = {
    "version": "1.2.3",  # 更新版本号
    # ...
}
```

### 2. 文档维护

#### README.md 更新检查清单

- [ ] 功能描述准确
- [ ] 参数说明完整
- [ ] 使用示例有效
- [ ] 常见问题更新
- [ ] 测试状态最新
- [ ] 更新日志记录

### 3. 监控与告警

```python
class YourCrawler(BaseCrawler):
    async def run(self, url: str, **kwargs) -> str:
        start_time = time.time()
        
        try:
            result = await crawler.arun(url=url)
            duration = time.time() - start_time
            
            # 记录性能指标
            self.logger.info(f"爬取完成: {url}, 耗时: {duration:.2f}s")
            
            # 如果太慢，记录警告
            if duration > 30:
                self.logger.warning(f"爬取耗时过长: {duration:.2f}s")
            
            return json.dumps({
                "success": True,
                "data": data,
                "metadata": {
                    **self.__meta__,
                    "duration": duration,
                    "timestamp": time.time()
                }
            })
        except Exception as e:
            # 记录错误
            self.logger.error(f"爬取失败: {e}", exc_info=True)
            # 可以在这里添加告警通知
```

### 4. 性能优化

#### 缓存策略

```python
from crawl4ai import CacheMode

# 开启缓存
config = CrawlerRunConfig(
    cache_mode=CacheMode.ENABLED,
    # 只读缓存
    # cache_mode=CacheMode.READ_ONLY,
    # 只写缓存
    # cache_mode=CacheMode.WRITE_ONLY,
)
```

#### 并发爬取

```python
import asyncio

async def crawl_multiple(self, urls: list) -> list:
    """并发爬取多个URL"""
    tasks = [self.run(url) for url in urls]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    return results
```

## 提交检查清单

在提交新爬虫或更新前，请确保：

### 代码质量
- [ ] 继承自 `BaseCrawler`
- [ ] 实现了 `run` 方法
- [ ] 包含完整的 `__meta__` 信息
- [ ] 添加了类型注解
- [ ] 添加了文档字符串
- [ ] 错误处理完善
- [ ] 日志记录规范

### 文件完整性
- [ ] `__init__.py` 正确导出类
- [ ] `crawler.py` 实现完整
- [ ] `README.md` 文档齐全
- [ ] 必要时包含 `config.json`
- [ ] 必要时包含 `script.js`

### 测试
- [ ] 编写了单元测试
- [ ] 所有测试通过
- [ ] 在目标网站测试成功
- [ ] 错误处理测试通过

### 文档
- [ ] README.md 完整
- [ ] 使用示例有效
- [ ] 参数说明清晰
- [ ] 更新了 CHANGELOG

### 规范
- [ ] 命名符合规范
- [ ] 代码格式化（black/flake8）
- [ ] 无明显的安全问题
- [ ] 遵守网站 robots.txt

## 参考资源

- [Crawl4AI 主文档](../README.md)
- [BaseCrawler API](../crawl4ai/hub.py)
- [配置选项](../crawl4ai/async_configs.py)
- [示例爬虫](../crawl4ai/crawlers/)

## 获取帮助

如有问题，请：

1. 查看现有爬虫示例
2. 阅读主项目文档
3. 提交 Issue 到 GitHub
4. 联系项目维护者

---

Happy Crawling! 🚀

