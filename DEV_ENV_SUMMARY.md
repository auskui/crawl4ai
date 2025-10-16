# 🛠️ 开发环境配置总结

## ✅ 已完成的配置

### 1. Docker Compose 开发配置
**文件：** `docker-compose.dev.yml`

**关键特性：**
- ✅ 代码卷挂载（`./deploy/docker` → `/app`）
- ✅ 库代码只读挂载（`./crawl4ai` → `/app/crawl4ai:ro`）
- ✅ 输出目录映射（screenshots、pdfs、logs）
- ✅ uvicorn 热重载（`--reload`）
- ✅ 开发环境变量（`PYTHON_ENV=development`）
- ✅ Redis 端口暴露（6379）

### 2. 开发配置文件
**文件：** `deploy/docker/config.dev.yml`

**与生产环境的区别：**
- 日志级别：`DEBUG`（生产为 `INFO`）
- 热重载：启用（生产禁用）
- 速率限制：禁用（开发更快测试）
- 最大页面数：20（生产为 40）
- 空闲超时：600秒（生产为 1800秒）

### 3. 配置加载器更新
**文件：** `deploy/docker/utils.py`

**功能：** 根据 `PYTHON_ENV` 环境变量自动选择配置文件
```python
env = os.getenv("PYTHON_ENV", "production")
config_filename = "config.dev.yml" if env == "development" else "config.yml"
```

### 4. 输出目录结构
```
output/
├── screenshots/   # 网页截图输出
├── pdfs/         # PDF 文档输出
└── logs/         # 应用日志输出
```

## 🎯 使用方式

### 启动开发环境
```bash
# 完整启动（查看日志）
docker-compose -f docker-compose.dev.yml up

# 后台启动
docker-compose -f docker-compose.dev.yml up -d

# 首次启动或强制重建
docker-compose -f docker-compose.dev.yml up --build
```

### 验证服务
```bash
# 健康检查
curl http://localhost:11235/health

# MCP Schema
curl http://localhost:11235/mcp/schema

# 列出所有 MCP 工具
curl http://localhost:11235/mcp/schema | jq '.tools[].name'
```

### 热重载测试
1. 修改 `deploy/docker/server.py` 中的任何代码
2. 保存文件
3. 查看日志：`docker-compose -f docker-compose.dev.yml logs -f`
4. 应该看到：`INFO: Detected file change, reloading...`

### 查看日志
```bash
# 实时日志
docker-compose -f docker-compose.dev.yml logs -f

# 仅应用日志
docker-compose -f docker-compose.dev.yml logs -f crawl4ai-dev

# 容器内日志文件
tail -f output/logs/*.log
```

### 停止和清理
```bash
# 停止服务
docker-compose -f docker-compose.dev.yml down

# 停止并删除卷
docker-compose -f docker-compose.dev.yml down -v

# 重建镜像
docker-compose -f docker-compose.dev.yml build --no-cache
```

## 📝 MCP 工具列表

开发环境支持的 MCP 工具：

1. **`md`** - Markdown 提取
2. **`html`** - HTML 预处理
3. **`screenshot`** - 网页截图
4. **`pdf`** - PDF 生成
5. **`execute_js`** - JavaScript 执行
6. **`crawl`** - 完整爬取
7. **`ask`** - Crawl4AI 文档查询

## 🔧 Cursor MCP 配置

确保 `~/.cursor/mcp.json` 包含：

```json
{
  "mcpServers": {
    "crawl4ai": {
      "url": "http://localhost:11235/mcp/sse"
    }
  }
}
```

重启 Cursor 后即可使用。

## 🐛 故障排除

### 端口冲突
修改 `docker-compose.dev.yml` 中的端口映射：
```yaml
ports:
  - "12345:11235"  # 使用不同端口
```

### 代码修改不生效
1. 确认修改的是 `deploy/docker/` 下的文件
2. 查看日志确认重载信号
3. 手动重启：`docker-compose -f docker-compose.dev.yml restart`

### 权限错误
```bash
chmod -R 777 output/
```

### Redis 连接失败
查看容器日志确认 Redis 是否启动：
```bash
docker-compose -f docker-compose.dev.yml logs | grep redis
```

## 📚 相关文档

- **快速启动：** `START_DEV.md` - 一键启动命令
- **完整指南：** `QUICKSTART_DEV.md` - 详细配置说明
- **MCP 使用：** `CRAWL4AI_MCP_USAGE.md` - MCP 工具说明
- **生产部署：** `部署指南.md` - 生产环境配置

## ✨ 开发体验提升

### 优势
1. **即时反馈** - 代码修改立即生效（1-2秒）
2. **本地文件** - 截图和PDF直接保存到本地
3. **详细日志** - DEBUG 级别日志便于调试
4. **无速率限制** - 快速测试API
5. **Redis 调试** - 端口暴露可直接连接

### 性能对比
| 特性 | 开发环境 | 生产环境 |
|------|---------|---------|
| 启动时间 | ~30秒 | ~40秒 |
| 代码更新 | 自动（1-2秒） | 需重建镜像 |
| 日志级别 | DEBUG | INFO |
| 最大页面 | 20 | 40 |
| Worker | 1 | 多个 |

## 🎉 下一步

1. **启动服务：**
   ```bash
   docker-compose -f docker-compose.dev.yml up
   ```

2. **测试 MCP：**
   - 在 Cursor 中输入："截图 https://www.azazie.com"
   - 查看 `output/screenshots/` 中的结果

3. **修改代码：**
   - 编辑 `deploy/docker/server.py`
   - 观察自动重载

4. **查看文档：**
   - 详细指南：`QUICKSTART_DEV.md`
   - 项目概述：`项目概述.md`

---

**配置完成日期：** 2025-10-16  
**环境版本：** Crawl4AI v1.0.0-dev  
**Docker Compose 版本：** 3.8

