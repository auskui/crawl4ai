# 🏗️ Crawl4AI 开发环境构建指南

## 📋 构建策略：方案 3（推荐）

**特点：** 首次构建慢（5-10分钟），后续启动快（5秒）

### ⏱️ 时间对比

| 操作 | 首次 | 第 2 次 | 第 3 次+ |
|------|------|---------|----------|
| 构建时间 | 5-10 分钟 | 0 秒（跳过） | 0 秒（跳过） |
| 启动时间 | 30 秒 | 5 秒 | 5 秒 |
| **总计** | **6-11 分钟** | **5 秒** | **5 秒** |

### 🎯 为什么后续快？

Docker 会缓存：
- ✅ 基础镜像（python:3.12）
- ✅ 系统依赖（Chromium、Redis）
- ✅ Python 包（Playwright、Crawl4AI）
- ✅ Playwright 浏览器

**只要不改 Dockerfile，镜像永久可用！**

---

## 🚀 完整启动流程

### 步骤 1：启动 Docker Desktop

**手动启动：**
1. 打开 Launchpad 或应用程序文件夹
2. 找到 "Docker" 应用并打开
3. 等待顶部菜单栏 Docker 图标显示为绿色（运行中）

**验证 Docker 运行：**
```bash
docker info
```

如果看到系统信息（而不是错误），说明 Docker 已就绪。

---

### 步骤 2：首次构建（只需一次）

```bash
# 进入项目目录
cd /Users/admin/tao/crawl4ai

# 首次构建（需要 5-10 分钟）
docker-compose -f docker-compose.dev.yml build

# 看到这些表示正在下载和安装：
# [+] Building 345.2s (23/23) FINISHED
# => [internal] load metadata for docker.io/library/python:3.12-slim-bookworm
# => [1/18] FROM docker.io/library/python:3.12-slim-bookworm
# => [2/18] RUN apt-get update && apt-get install -y ...
# ...（很多行）...
# => [18/18] RUN crawl4ai-doctor
# => exporting to image
# => => naming to docker.io/library/crawl4ai-crawl4ai-dev
```

**等待时可以：** ☕️ 喝杯咖啡，看看文档

---

### 步骤 3：启动服务（5 秒）

```bash
# 首次启动
docker-compose -f docker-compose.dev.yml up

# 或后台运行
docker-compose -f docker-compose.dev.yml up -d
```

**成功标志：**
```
✅ crawl4ai-dev  | INFO:     Application startup complete.
✅ crawl4ai-dev  | INFO:     Uvicorn running on http://0.0.0.0:11235
✅ crawl4ai-dev  | MCP server running on 0.0.0.0:11235
```

---

### 步骤 4：验证服务

在**另一个终端**运行：

```bash
# 健康检查
curl http://localhost:11235/health

# 预期输出：
# {"status":"healthy","version":"1.0.0-dev",...}

# MCP Schema
curl http://localhost:11235/mcp/schema

# 预期输出：
# {"tools":[...], "resources":[...], ...}
```

---

## 🔄 后续使用（每天开发）

### 启动服务（5 秒）

```bash
cd /Users/admin/tao/crawl4ai
docker-compose -f docker-compose.dev.yml up
```

**不需要重新构建！** 直接启动即可。

### 停止服务

```bash
# Ctrl+C（如果在前台运行）

# 或者
docker-compose -f docker-compose.dev.yml down
```

### 查看日志

```bash
docker-compose -f docker-compose.dev.yml logs -f
```

---

## 🔥 热重载测试

1. **启动服务后，修改代码：**
   ```bash
   vim deploy/docker/server.py
   # 添加一行注释或修改任何内容
   ```

2. **保存文件，观察日志：**
   ```
   INFO:     Detected file change, reloading...
   INFO:     Started reloader process [PID]
   INFO:     Application startup complete.
   ```

3. **重载时间：1-2 秒** ⚡️

---

## 📦 何时需要重新构建？

**需要重新构建：**
- ✅ 修改了 `Dockerfile`
- ✅ 修改了 `deploy/docker/requirements.txt`
- ✅ 升级了 crawl4ai 库版本

**不需要重新构建：**
- ❌ 修改 `deploy/docker/*.py`（热重载自动生效）
- ❌ 修改 `crawl4ai/*.py`（卷挂载自动同步）
- ❌ 修改配置文件 `config.dev.yml`（挂载自动同步）

**重新构建命令：**
```bash
docker-compose -f docker-compose.dev.yml build --no-cache
docker-compose -f docker-compose.dev.yml up
```

---

## 🎯 优化技巧

### 1. 并行下载加速

编辑 `~/.docker/daemon.json`（需要重启 Docker）：
```json
{
  "max-concurrent-downloads": 10,
  "max-concurrent-uploads": 10
}
```

### 2. 使用国内镜像源（可选）

首次构建前，修改 `Dockerfile`：
```dockerfile
# 在 RUN pip install 之前添加
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

### 3. 清理旧镜像释放空间

```bash
# 查看镜像大小
docker images

# 删除无用镜像
docker image prune -a
```

---

## 📊 构建详情

### 构建过程分解

| 步骤 | 操作 | 时间 | 大小 |
|------|------|------|------|
| 1 | 下载基础镜像 | ~60s | 200MB |
| 2 | 安装系统依赖 | ~120s | 500MB |
| 3 | 安装 Python 包 | ~90s | 300MB |
| 4 | 下载 Playwright 浏览器 | ~60s | 400MB |
| 5 | 运行健康检查 | ~30s | - |
| **总计** | **~6 分钟** | **~1.4GB** |

### 镜像层缓存策略

Docker 从上到下构建，一旦某层改变，后续层全部重建：

```dockerfile
FROM python:3.12-slim        # ← 缓存（很少变）
RUN apt-get install ...      # ← 缓存（很少变）
COPY requirements.txt        # ← 缓存（偶尔变）
RUN pip install ...          # ← 缓存（偶尔变）
COPY . /app                  # ← 不缓存（开发环境用卷挂载代替）
```

**开发环境优势：** 代码用卷挂载，不会触发镜像重建！

---

## 🐛 故障排除

### 问题 1：构建失败 "No space left on device"

**原因：** Docker 磁盘空间不足

**解决：**
```bash
# 清理 Docker 缓存
docker system prune -a --volumes

# 查看磁盘使用
docker system df
```

### 问题 2：下载超时

**原因：** 网络不稳定

**解决：**
```bash
# 重新构建（会从断点继续）
docker-compose -f docker-compose.dev.yml build
```

### 问题 3：Playwright 安装失败

**原因：** ARM 架构兼容性问题（M1/M2 Mac）

**解决：** 在 `docker-compose.dev.yml` 中添加：
```yaml
platform: linux/amd64  # 强制使用 x86 架构
```

---

## 📈 性能监控

### 查看构建进度

```bash
# 详细构建日志
docker-compose -f docker-compose.dev.yml build --progress=plain

# 查看镜像大小
docker images | grep crawl4ai
```

### 启动时间测试

```bash
# 计时启动
time docker-compose -f docker-compose.dev.yml up -d

# 预期：首次 ~30s，后续 ~5s
```

---

## ✅ 验证清单

构建完成后，确认：

- [ ] 镜像已创建：`docker images | grep crawl4ai-dev`
- [ ] 容器可启动：`docker-compose -f docker-compose.dev.yml up -d`
- [ ] 服务健康：`curl http://localhost:11235/health`
- [ ] MCP 可用：`curl http://localhost:11235/mcp/schema`
- [ ] 热重载工作：修改 `server.py` 后观察日志
- [ ] 文件共享：`ls output/screenshots/`

---

## 🎉 总结

| 优势 | 说明 |
|------|------|
| ✅ 首次慢，后续快 | 构建一次，永久使用 |
| ✅ 完整功能 | 所有依赖都在镜像中 |
| ✅ 热重载 | 代码修改 1-2 秒生效 |
| ✅ 本地文件 | 输出直接保存到本地 |
| ✅ 离线可用 | 构建后无需网络 |

**下一步：** 启动 Docker Desktop，然后运行：
```bash
docker-compose -f docker-compose.dev.yml build
```

耐心等待首次构建完成，之后就可以享受秒级启动了！🚀

