# Crawl4AI MCP 使用指南

## 🎉 部署完成！

Crawl4AI Docker服务已成功启动，MCP已配置到Cursor。

## 📊 服务状态

- **Docker容器**: crawl4ai (运行中)
- **服务地址**: http://localhost:11235
- **MCP端点**: http://localhost:11235/mcp/sse
- **配置文件**: ~/.cursor/mcp.json

## 🛠️ 可用的MCP工具

### 1. `screenshot` - 网页截图
捕获网页的完整截图（已测试 ✅）

**示例用法（在Cursor对话中）：**
- "截图 https://www.azazie.com"
- "给我azazie首页的截图"
- "截取这个网页的图片"

**测试结果：**
- ✅ azazie.com截图成功
- 文件大小：13MB
- 保存位置：/tmp/azazie_screenshot.png

### 2. `md` - Markdown提取
将网页转换为干净的Markdown格式（已测试 ✅）

**示例用法：**
- "把azazie.com转换成markdown"
- "提取这个页面的文本内容"
- "获取网页的markdown格式"

**测试结果：**
- ✅ azazie.com提取成功
- 内容长度：55,145字符
- 过滤模式：fit（智能过滤）

### 3. `crawl` - 完整爬取
获取网页的HTML、链接、媒体等完整数据（已测试 ✅）

**示例用法：**
- "爬取azazie.com的所有信息"
- "获取这个页面的完整数据"
- "分析这个网站的结构"

**测试结果：**
- ✅ azazie.com爬取成功
- HTML长度：44,235字符
- 包含：链接、媒体、元数据

### 4. `pdf` - PDF生成
将网页导出为PDF文档

**示例用法：**
- "生成azazie.com的PDF"
- "把这个页面保存为PDF"

### 5. `execute_js` - JavaScript执行
在网页上执行自定义JavaScript代码

**示例用法：**
- "在azazie.com上执行JavaScript获取产品价格"
- "用JS提取这个页面的特定数据"

### 6. `html` - HTML预处理
获取经过预处理的HTML，用于schema提取

**示例用法：**
- "获取azazie.com的干净HTML"
- "预处理这个页面的HTML结构"

### 7. `ask` - Crawl4AI文档查询
查询Crawl4AI库的使用文档和代码示例

**示例用法：**
- "如何提取网页中的表格数据？"
- "Crawl4AI怎么处理动态内容？"

## 🚀 快速开始

### 在Cursor中使用

1. **重启Cursor**（首次配置后需要）
2. 在对话中直接说出你的需求，例如：
   - "截图azazie.com"
   - "爬取这个网站的数据"
   - "把这个页面转成markdown"

### 直接API调用（可选）

```bash
# 截图
curl -X POST http://localhost:11235/screenshot \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.azazie.com", "screenshot_wait_for": 2}'

# Markdown提取
curl -X POST http://localhost:11235/md \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.azazie.com", "f": "fit", "c": "0"}'

# 完整爬取
curl -X POST http://localhost:11235/crawl \
  -H "Content-Type: application/json" \
  -d '{"urls": ["https://www.azazie.com"]}'
```

## 📦 Docker管理

### 生产环境

#### 查看容器状态
```bash
docker ps | grep crawl4ai
```

#### 查看日志
```bash
docker logs -f crawl4ai
```

#### 停止服务
```bash
docker stop crawl4ai
```

#### 重启服务
```bash
docker start crawl4ai
```

#### 完全移除
```bash
docker stop crawl4ai && docker rm crawl4ai
```

### 开发环境 🛠️

#### 启动开发环境
使用 `docker-compose.dev.yml` 配置文件启动开发环境，支持代码热重载和文件共享。

```bash
# 首次启动（构建镜像）
docker-compose -f docker-compose.dev.yml up --build

# 后续启动
docker-compose -f docker-compose.dev.yml up

# 后台运行
docker-compose -f docker-compose.dev.yml up -d

# 查看日志
docker-compose -f docker-compose.dev.yml logs -f

# 停止服务
docker-compose -f docker-compose.dev.yml down
```

#### 文件映射说明
开发环境会自动映射以下目录：

- **应用代码**: `./deploy/docker` → `/app` (可读写，支持热重载)
- **库代码**: `./crawl4ai` → `/app/crawl4ai` (只读)
- **截图输出**: `./output/screenshots` → `/app/screenshots`
- **PDF输出**: `./output/pdfs` → `/app/pdfs`
- **日志文件**: `./output/logs` → `/app/logs`

#### 开发工作流
1. 修改 `deploy/docker/` 下的任何文件（server.py, schemas.py等）
2. 服务会自动检测文件变化并重新加载
3. 查看日志确认重载成功
4. 生成的截图和PDF会自动保存到本地 `output/` 目录

#### 查看生成的文件
```bash
# 查看截图
ls -lh output/screenshots/

# 查看PDF
ls -lh output/pdfs/

# 查看日志
tail -f output/logs/*.log
```

#### 开发环境特性
- ✅ 代码热重载：修改即生效
- ✅ 文件共享：截图/PDF自动保存到本地
- ✅ 实时调试：可查看详细日志
- ✅ Redis调试：暴露6379端口

## 🔧 故障排除

### MCP连接失败
1. 确认Docker容器正在运行：`docker ps | grep crawl4ai`
2. 测试服务健康：`curl http://localhost:11235/health`
3. 检查MCP端点：`curl http://localhost:11235/mcp/schema`
4. 重启Cursor

**常见问题：Cursor绕过MCP直接用HTTP调用**
- **原因**：MCP schema生成失败，导致Cursor无法识别工具
- **解决**：使用本项目最新的 `mcp_bridge.py` 修复
- **验证**：访问 `http://localhost:11235/mcp/schema` 应该能看到正确的工具列表和schema

### 截图/爬取失败
- 检查容器日志：`docker logs crawl4ai`
- 确认网址可访问
- 增加等待时间（screenshot_wait_for）

### 开发环境问题
**文件权限错误**
```bash
# 确保output目录有写权限
chmod -R 777 output/
```

**代码修改不生效**
- 检查日志确认uvicorn是否检测到文件变化
- 确认修改的是 `deploy/docker/` 下的文件
- 手动重启：`docker-compose -f docker-compose.dev.yml restart`

**卷映射问题（Mac M1/M2）**
- 确保Docker Desktop已启用文件共享
- 检查 Docker Desktop → Settings → Resources → File Sharing

### 端口冲突
如果11235端口已被占用，修改docker run命令：
```bash
docker run -d -p 12345:11235 --name crawl4ai --shm-size=1g unclecode/crawl4ai:0.7.0-r1
```
然后更新 ~/.cursor/mcp.json 中的URL。

## 📚 进阶功能

### 自定义浏览器配置
```json
{
  "browser_config": {
    "headless": true,
    "viewport_width": 1920,
    "viewport_height": 1080
  }
}
```

### LLM驱动的数据提取
需要配置API密钥，参考项目文档。

### 批量爬取
```json
{
  "urls": [
    "https://example1.com",
    "https://example2.com",
    "https://example3.com"
  ]
}
```

## 🎯 最佳实践

1. **截图功能**：适合需要视觉验证或存档的场景
2. **Markdown提取**：适合文本分析、内容提取
3. **完整爬取**：适合需要结构化数据、链接分析的场景
4. **PDF生成**：适合文档存档、打印需求

## 🌐 支持的网站

- ✅ 静态网站（HTML直接渲染）
- ✅ 动态网站（JavaScript渲染）
- ✅ SPA应用（Single Page Applications）
- ✅ 需要等待加载的网站（可配置等待时间）
- ⚠️ 需要登录的网站（需要额外配置session/cookies）

## 📖 相关资源

- Playground界面：http://localhost:11235/playground
- API文档：项目的 deploy/docker/README.md
- 官方文档：https://docs.crawl4ai.com/

---

**享受无脚本的网页爬取体验！** 🎉

