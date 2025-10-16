# 🚀 快速启动开发环境

## 一键启动

```bash
# 启动开发环境（首次运行会自动构建）
docker-compose -f docker-compose.dev.yml up

# 或后台运行
docker-compose -f docker-compose.dev.yml up -d
```

## 验证服务

```bash
# 检查服务健康
curl http://localhost:11235/health

# 检查 MCP 工具
curl http://localhost:11235/mcp/schema
```

## 代码热重载

修改 `deploy/docker/` 下的任何 Python 文件，保存后服务会自动重启。

观察日志：
```bash
docker-compose -f docker-compose.dev.yml logs -f
```

## 查看生成的文件

```bash
ls -lh output/screenshots/  # 截图
ls -lh output/pdfs/         # PDF
tail -f output/logs/*.log   # 日志
```

## 停止服务

```bash
docker-compose -f docker-compose.dev.yml down
```

## 完整指南

查看详细文档：`QUICKSTART_DEV.md`

---

**提示：** 开发环境使用 `config.dev.yml` 配置，日志级别为 DEBUG，速率限制已禁用。

