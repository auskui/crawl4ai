# 🛠️ Crawl4AI 开发环境快速启动指南

本指南帮助你快速启动支持 **代码热重载** 和 **文件共享** 的 Crawl4AI MCP 开发环境。

## 📋 前置要求

- Docker 和 Docker Compose 已安装
- 至少 4GB 可用内存
- （可选）API 密钥用于 LLM 功能

## 🚀 快速启动

### 1. 启动开发环境

```bash
# 首次启动（构建镜像）
docker-compose -f docker-compose.dev.yml up --build

# 后续启动（使用缓存镜像）
docker-compose -f docker-compose.dev.yml up

# 后台运行
docker-compose -f docker-compose.dev.yml up -d
```

### 2. 验证服务

```bash
# 检查健康状态
curl http://localhost:11235/health

# 验证 MCP 端点
curl http://localhost:11235/mcp/schema

# 查看可用工具列表
curl http://localhost:11235/mcp/schema | jq '.tools[].name'
```

### 3. 在 Cursor 中使用

确保 `~/.cursor/mcp.json` 包含以下配置：

```json
{
  "mcpServers": {
    "crawl4ai": {
      "url": "http://localhost:11235/mcp/sse"
    }
  }
}
```

然后在 Cursor 对话中直接使用：
- "截图 https://www.azazie.com"
- "爬取这个网站的数据"
- "把这个页面转成markdown"

## 🔥 开发工作流

### 代码热重载

修改以下文件会自动触发服务重启：
- `deploy/docker/server.py` - 主服务器文件
- `deploy/docker/mcp_bridge.py` - MCP 桥接层
- `deploy/docker/api.py` - API 处理逻辑
- `deploy/docker/schemas.py` - 数据模型
- `deploy/docker/*.py` - 任何 Python 文件

**示例：** 修改 `server.py` 后保存，观察日志：
```bash
docker-compose -f docker-compose.dev.yml logs -f
```

你会看到：
```
INFO:     Detected file change, reloading...
INFO:     Application startup complete.
```

### 查看生成的文件

所有生成的文件会自动保存到本地 `output/` 目录：

```bash
# 查看截图
ls -lh output/screenshots/

# 查看 PDF
ls -lh output/pdfs/

# 查看日志
tail -f output/logs/*.log
```

### 实时调试

```bash
# 查看实时日志
docker-compose -f docker-compose.dev.yml logs -f

# 仅查看应用日志（过滤 Redis）
docker-compose -f docker-compose.dev.yml logs -f crawl4ai-dev | grep -v redis

# 进入容器调试
docker-compose -f docker-compose.dev.yml exec crawl4ai-dev bash
```

## 📂 目录结构说明

```
crawl4ai/
├── deploy/docker/          # 应用代码（挂载到容器 /app，支持热重载）
│   ├── server.py          # FastAPI 主服务器
│   ├── mcp_bridge.py      # MCP 桥接层
│   ├── config.dev.yml     # 开发环境配置
│   └── ...
├── crawl4ai/              # 库代码（挂载到容器 /app/crawl4ai，只读）
├── output/                # 输出文件（与容器共享）
│   ├── screenshots/       # 网页截图
│   ├── pdfs/             # PDF 文档
│   └── logs/             # 应用日志
└── docker-compose.dev.yml # 开发环境配置
```

## ⚙️ 配置说明

### 环境变量

开发环境特定的环境变量在 `docker-compose.dev.yml` 中定义：

```yaml
environment:
  - PYTHON_ENV=development  # 触发加载 config.dev.yml
  - OPENAI_API_KEY=...      # LLM API 密钥
```

### API 密钥配置

方法 1：创建 `.llm.env` 文件（推荐）

```bash
# 复制示例文件
cp .llm.env.example .llm.env

# 编辑添加你的 API 密钥
vim .llm.env
```

方法 2：直接设置环境变量

```bash
export OPENAI_API_KEY=sk-...
docker-compose -f docker-compose.dev.yml up
```

### 开发配置 vs 生产配置

| 配置项 | 开发环境 | 生产环境 |
|--------|---------|---------|
| 配置文件 | `config.dev.yml` | `config.yml` |
| 日志级别 | DEBUG | INFO |
| 热重载 | 启用 | 禁用 |
| 速率限制 | 禁用 | 启用 |
| Worker 数 | 1 | 多个 |
| 最大页面数 | 20 | 40 |

## 🔧 常见问题

### 代码修改不生效

**原因：** 可能修改的是 `crawl4ai/` 库代码（只读挂载）

**解决：** 
- 确认修改的是 `deploy/docker/` 下的文件
- 检查日志确认 uvicorn 是否检测到文件变化
- 手动重启：`docker-compose -f docker-compose.dev.yml restart`

### 文件权限错误

**原因：** 容器内以 root 运行（开发环境默认）

**解决：** 
```bash
# 给予输出目录写权限
chmod -R 777 output/
```

### 端口冲突

**问题：** 端口 11235 已被占用

**解决：** 修改 `docker-compose.dev.yml` 中的端口映射：
```yaml
ports:
  - "12345:11235"  # 映射到本地 12345 端口
```

然后更新 `~/.cursor/mcp.json` 中的 URL。

### Redis 连接失败

**解决：** 开发环境在容器启动时自动启动 Redis，确认命令正确：
```bash
# 检查容器日志
docker-compose -f docker-compose.dev.yml logs crawl4ai-dev | grep redis

# 应该看到：
# Redis server started...
```

### MCP 工具无法调用

**验证步骤：**
1. 检查服务健康：`curl http://localhost:11235/health`
2. 检查 MCP schema：`curl http://localhost:11235/mcp/schema`
3. 重启 Cursor
4. 查看容器日志是否有错误

## 🎯 测试 MCP 功能

### 1. 测试截图工具

```bash
curl -X POST http://localhost:11235/screenshot \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://www.azazie.com",
    "screenshot_wait_for": 2
  }'
```

检查：`ls -lh output/screenshots/`

### 2. 测试 Markdown 提取

```bash
curl -X POST http://localhost:11235/md \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://www.azazie.com",
    "f": "fit",
    "c": "0"
  }'
```

### 3. 测试爬取功能

```bash
curl -X POST http://localhost:11235/crawl \
  -H "Content-Type: application/json" \
  -d '{
    "urls": ["https://www.azazie.com"]
  }'
```

## 📊 性能监控

### Prometheus 指标

访问：http://localhost:11235/metrics

### 健康检查

访问：http://localhost:11235/health

返回示例：
```json
{
  "status": "healthy",
  "version": "1.0.0-dev",
  "timestamp": "2025-01-16T12:00:00Z"
}
```

## 🛑 停止和清理

### 停止服务

```bash
# 停止但保留容器
docker-compose -f docker-compose.dev.yml stop

# 停止并删除容器
docker-compose -f docker-compose.dev.yml down

# 删除容器和卷（清理所有数据）
docker-compose -f docker-compose.dev.yml down -v
```

### 重建镜像

```bash
# 强制重建
docker-compose -f docker-compose.dev.yml build --no-cache

# 重建并启动
docker-compose -f docker-compose.dev.yml up --build
```

## 📚 相关文档

- [完整使用指南](CRAWL4AI_MCP_USAGE.md) - MCP 工具详细说明
- [生产部署指南](部署指南.md) - 生产环境配置
- [项目概述](项目概述.md) - 架构和设计

---

**祝开发愉快！** 🎉

如有问题，请检查容器日志：
```bash
docker-compose -f docker-compose.dev.yml logs -f
```
