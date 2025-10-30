# Crawlers Directory

这个目录用于存放针对不同网站的专用爬虫脚本，每个网站一个子文件夹。

## 📁 目录结构规范

```
crawlers/
├── README.md                    # 本文件
├── _template/                   # 新爬虫模板
│   ├── __init__.py
│   ├── crawler.py              # 主爬虫类
│   ├── config.json             # 配置文件（可选）
│   ├── script.js               # JS脚本（可选）
│   └── README.md               # 爬虫说明文档
├── amazon_product/             # Amazon产品爬虫
│   ├── __init__.py
│   └── crawler.py
├── google_search/              # Google搜索爬虫
│   ├── __init__.py
│   ├── crawler.py
│   └── script.js
└── [website_name]/             # 新增网站爬虫
    ├── __init__.py
    ├── crawler.py
    ├── config.json (可选)
    ├── script.js (可选)
    └── README.md
```

## 📝 命名规范

### 文件夹命名
- 使用网站名称或功能名称，小写字母，下划线分隔
- 示例：`amazon_product`, `google_search`, `twitter_posts`, `linkedin_profiles`

### 类命名
- 使用 PascalCase，以 `Crawler` 结尾
- 示例：`AmazonProductCrawler`, `GoogleSearchCrawler`, `TwitterPostsCrawler`

## 🏗️ 爬虫开发规范

### 1. 必须继承 `BaseCrawler`

```python
from crawl4ai.hub import BaseCrawler

class YourSiteCrawler(BaseCrawler):
    __meta__ = {
        "version": "1.0.0",
        "tested_on": ["example.com"],
        "rate_limit": "10 RPM",
        "description": "爬虫功能描述",
    }
```

### 2. 必须实现 `run` 方法

```python
async def run(self, url: str, **kwargs) -> str:
    """
    执行爬取任务
    
    Args:
        url: 目标URL
        **kwargs: 其他参数
    
    Returns:
        str: JSON格式的结果字符串
    """
    pass
```

### 3. 元数据 `__meta__` 必填字段

- `version`: 爬虫版本号
- `tested_on`: 测试过的网站列表
- `rate_limit`: 请求频率限制
- `description`: 功能描述

### 4. 必需文件

每个爬虫文件夹必须包含：
- `__init__.py`: 导出爬虫类
- `crawler.py`: 爬虫主逻辑
- `README.md`: 使用说明文档

### 5. 可选文件

根据需求可添加：
- `script.js`: 页面注入的 JavaScript 脚本
- `config.json`: 配置文件（选择器、API endpoints等）
- `utils.py`: 辅助函数
- `schemas/`: 数据提取schema定义

## 🎯 使用示例

```python
from crawl4ai.crawlers.google_search import GoogleSearchCrawler

crawler = GoogleSearchCrawler()
result = await crawler.run(query="Python programming", search_type="text")
```

## ✅ 提交检查清单

在提交新爬虫前，请确保：

- [ ] 文件夹命名符合规范（小写+下划线）
- [ ] 类继承自 `BaseCrawler`
- [ ] 实现了 `run` 方法
- [ ] 包含 `__meta__` 元数据
- [ ] 编写了 `README.md` 说明文档
- [ ] 在 `__init__.py` 中正确导出类
- [ ] 添加了必要的错误处理
- [ ] 添加了日志记录
- [ ] 编写了使用示例
- [ ] 测试通过

## 📚 更多文档

详细的开发指南请参考：`docs/CRAWLER_DEVELOPMENT_GUIDE.md`

