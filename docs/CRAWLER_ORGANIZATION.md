# Crawl4AI 爬虫脚本组织方案

本文档说明 Crawl4AI 项目中爬虫脚本的组织结构和管理规范。

## 📝 概述

为了更好地管理针对不同网站的爬虫脚本，我们建立了一套完整的组织方案：

- **统一的目录结构**：所有爬虫放在 `crawl4ai/crawlers/` 目录下
- **标准化的开发模板**：提供 `_template` 模板快速创建新爬虫
- **完善的开发规范**：统一的命名、代码和文档规范
- **详细的文档支持**：从快速开始到深入指南

## 📁 目录结构

```
crawl4ai/crawlers/
│
├── README.md                    # 目录说明和开发规范概述
├── QUICK_START.md              # 快速开始指南（30秒创建新爬虫）
├── .gitkeep                    # 确保目录被 git 跟踪
│
├── _template/                   # 新爬虫模板（必须保留）
│   ├── __init__.py             # 类导出模板
│   ├── crawler.py              # 爬虫主逻辑模板
│   ├── README.md               # 文档模板
│   ├── config.json             # 配置文件模板
│   └── script.js               # JavaScript 脚本模板
│
├── amazon_product/             # 示例：Amazon 产品爬虫
│   ├── __init__.py
│   └── crawler.py
│
├── google_search/              # 示例：Google 搜索爬虫
│   ├── __init__.py
│   ├── crawler.py
│   └── script.js
│
└── [new_site]/                 # 新增网站爬虫
    ├── __init__.py             # 必需
    ├── crawler.py              # 必需
    ├── README.md               # 必需
    ├── config.json             # 可选
    ├── script.js               # 可选
    └── utils.py                # 可选
```

## 📚 文档体系

### 1. 快速参考
- **`crawl4ai/crawlers/README.md`**
  - 目录说明
  - 基本规范
  - 提交检查清单

- **`crawl4ai/crawlers/QUICK_START.md`**
  - 30秒创建新爬虫
  - 常用功能速查
  - 快速命名参考

### 2. 详细指南
- **`docs/CRAWLER_DEVELOPMENT_GUIDE.md`**
  - 完整的开发规范
  - 最佳实践
  - 测试与调试
  - 部署与维护
  - 故障排查

### 3. 项目规则
- **`.cursorrules`**
  - 项目级别的规范
  - AI 助手行为准则
  - 自动化工作流

- **`.cursor/crawler_rules.md`**
  - 爬虫开发专用规则
  - 详细的技术规范

## 🎯 核心规范

### 命名规范

| 类型 | 规则 | 示例 |
|------|------|------|
| **文件夹** | 小写+下划线 | `amazon_product`, `google_search`, `twitter_posts` |
| **类名** | PascalCase+Crawler | `AmazonProductCrawler`, `GoogleSearchCrawler` |
| **方法** | 小写+下划线 | `run`, `_extract_data`, `_validate_data` |
| **配置文件** | 小写+扩展名 | `config.json`, `script.js`, `utils.py` |

### 必需文件

每个爬虫文件夹必须包含：

1. **`__init__.py`** - 导出爬虫类
   ```python
   from .crawler import YourCrawler
   __all__ = ["YourCrawler"]
   ```

2. **`crawler.py`** - 爬虫主逻辑
   - 继承 `BaseCrawler`
   - 定义 `__meta__`
   - 实现 `run` 方法

3. **`README.md`** - 使用文档
   - 功能描述
   - 参数说明
   - 使用示例
   - 注意事项

### 代码结构

```python
from crawl4ai.hub import BaseCrawler
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig
import json

class YourCrawler(BaseCrawler):
    # 1. 元数据
    __meta__ = {
        "version": "1.0.0",
        "tested_on": ["site.com"],
        "rate_limit": "10 RPM",
        "description": "功能描述"
    }
    
    # 2. 初始化
    def __init__(self):
        super().__init__()
        # 加载配置、脚本等
    
    # 3. 主方法
    async def run(self, url: str, **kwargs) -> str:
        """爬取逻辑"""
        try:
            # 实现爬取
            return json.dumps({"success": True, "data": data})
        except Exception as e:
            return json.dumps({"error": str(e)})
    
    # 4. 辅助方法
    def _extract_data(self, result):
        """数据提取"""
        pass
```

## 🚀 使用模板创建新爬虫

### 步骤 1: 复制模板

```bash
cd crawl4ai/crawlers
cp -r _template your_site_name
cd your_site_name
```

### 步骤 2: 修改文件

#### `__init__.py`
```python
from .crawler import YourSiteNameCrawler

__all__ = ["YourSiteNameCrawler"]
```

#### `crawler.py`
- 重命名类：`TemplateCrawler` → `YourSiteNameCrawler`
- 更新 `__meta__` 信息
- 实现 `run` 方法和数据提取逻辑
- 删除模板中的 TODO 注释

#### `README.md`
- 更新项目名称和描述
- 填写参数说明
- 添加使用示例
- 更新测试状态

### 步骤 3: 测试

```python
from crawl4ai.crawlers.your_site_name import YourSiteNameCrawler
import asyncio

async def main():
    crawler = YourSiteNameCrawler()
    result = await crawler.run(url="https://yoursite.com")
    print(result)

asyncio.run(main())
```

## 🔧 常见使用场景

### 场景 1: 简单静态页面爬取

只需实现基本的 `run` 方法和数据提取：

```python
class SimpleCrawler(BaseCrawler):
    async def run(self, url: str, **kwargs) -> str:
        async with AsyncWebCrawler() as crawler:
            result = await crawler.arun(url=url)
            data = self._extract_data(result)
            return json.dumps({"data": data})
```

### 场景 2: 需要 JavaScript 交互

添加 `script.js` 文件处理页面交互：

```python
class JSCrawler(BaseCrawler):
    def __init__(self):
        super().__init__()
        self.js_script = (Path(__file__).parent / "script.js").read_text()
    
    async def run(self, url: str, **kwargs) -> str:
        config = CrawlerRunConfig(js_code=self.js_script)
        # ...
```

### 场景 3: 复杂配置管理

使用 `config.json` 管理选择器和配置：

```python
class ConfigurableCrawler(BaseCrawler):
    def __init__(self):
        super().__init__()
        config_file = Path(__file__).parent / "config.json"
        self.config = json.load(open(config_file))
    
    def _extract_data(self, result):
        selectors = self.config["selectors"]
        # 使用配置中的选择器
```

## ✅ 质量保证

### 提交前检查清单

- [ ] **命名规范**
  - [ ] 文件夹：小写+下划线
  - [ ] 类名：PascalCase+Crawler

- [ ] **代码质量**
  - [ ] 继承自 `BaseCrawler`
  - [ ] 包含完整的 `__meta__`
  - [ ] 实现了 `run` 方法
  - [ ] 添加了错误处理
  - [ ] 添加了日志记录
  - [ ] 添加了类型注解
  - [ ] 添加了文档字符串

- [ ] **文件完整性**
  - [ ] `__init__.py` 正确导出
  - [ ] `crawler.py` 实现完整
  - [ ] `README.md` 文档齐全

- [ ] **测试**
  - [ ] 编写了测试用例
  - [ ] 测试通过
  - [ ] 在目标网站测试成功

### 代码审查要点

1. **安全性**
   - 是否处理了敏感信息？
   - 是否有 SQL 注入风险？
   - 是否验证了用户输入？

2. **性能**
   - 是否有不必要的等待？
   - 是否可以使用缓存？
   - 是否会造成内存泄漏？

3. **可维护性**
   - 代码是否易读？
   - 是否有充足的注释？
   - 是否遵循了规范？

## 🤖 AI 助手集成

通过 `.cursorrules` 文件，AI 助手可以：

1. **自动创建爬虫**
   - 用户："创建一个爬取 Twitter 的爬虫"
   - AI：自动复制模板、修改文件、生成文档

2. **代码生成**
   - 遵循项目规范
   - 包含完整的错误处理
   - 自动添加类型注解

3. **文档生成**
   - 自动生成 README
   - 提供使用示例
   - 更新检查清单

## 📊 项目统计

当前爬虫数量：
- ✅ `amazon_product` - Amazon 产品爬虫
- ✅ `google_search` - Google 搜索爬虫
- 📦 `_template` - 模板（不计入统计）

## 🔄 维护计划

### 定期检查
- [ ] 每月检查爬虫是否仍然有效
- [ ] 更新失效的选择器
- [ ] 更新文档和示例
- [ ] 检查依赖版本

### 版本管理
- 遵循语义化版本
- 在 `__meta__["version"]` 中记录
- 在 README.md 的更新日志中记录

## 📝 贡献指南

### 添加新爬虫

1. 使用模板创建
2. 完整实现功能
3. 编写测试
4. 编写文档
5. 提交 Pull Request

### 改进现有爬虫

1. 创建 Issue 说明问题
2. Fork 项目
3. 修改代码
4. 更新文档
5. 提交 Pull Request

## 🎓 学习路径

### 初学者
1. 阅读 `QUICK_START.md`
2. 复制模板创建简单爬虫
3. 参考 `amazon_product` 示例

### 进阶者
1. 阅读 `CRAWLER_DEVELOPMENT_GUIDE.md`
2. 学习 `google_search` 的 JS 集成
3. 实现复杂的数据提取逻辑

### 高级用户
1. 优化性能和缓存
2. 处理反爬虫机制
3. 贡献通用工具函数

## 🔗 相关资源

### 项目文档
- [项目 README](../README.md)
- [快速开始](../QUICK_START.txt)
- [开发指南](../QUICKSTART_DEV.md)

### API 文档
- [BaseCrawler](../crawl4ai/hub.py)
- [AsyncWebCrawler](../crawl4ai/async_webcrawler.py)
- [配置选项](../crawl4ai/async_configs.py)

### 外部资源
- [Playwright 文档](https://playwright.dev/python/)
- [BeautifulSoup 文档](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Asyncio 文档](https://docs.python.org/3/library/asyncio.html)

---

## 总结

这套爬虫组织方案提供了：

✅ **清晰的结构** - 每个网站一个文件夹，易于管理
✅ **标准化模板** - 快速创建新爬虫
✅ **完善的文档** - 从快速开始到深入指南
✅ **统一的规范** - 保证代码质量和一致性
✅ **AI 助手集成** - 自动化开发流程

通过遵循这些规范，可以确保项目的可维护性和扩展性！

---

*最后更新: 2025-10-20*

