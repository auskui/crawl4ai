# Output 目录

这个目录用于开发环境中存储Crawl4AI生成的输出文件。

## 目录结构

```
output/
├── screenshots/    # 网页截图（PNG格式）
├── pdfs/          # 生成的PDF文档
└── logs/          # 应用日志文件
```

## 使用说明

当使用 `docker-compose.dev.yml` 启动开发环境时，这些目录会自动映射到容器内的对应路径：

- `./output/screenshots` → `/app/screenshots`
- `./output/pdfs` → `/app/pdfs`
- `./output/logs` → `/app/logs`

## 自动保存

在开发环境中，截图和PDF会自动保存到这些目录：

**截图命名格式**: `{domain}_{timestamp}.png`
- 示例: `www_example_com_1704123456.png`

**PDF命名格式**: `{domain}_{timestamp}.pdf`
- 示例: `www_example_com_1704123456.pdf`

## 注意事项

- 这些文件不会被提交到Git（已在.gitignore中配置）
- 生产环境不会使用这些目录
- 建议定期清理旧文件以释放磁盘空间

## 清理

```bash
# 清空所有输出文件
rm -rf output/screenshots/* output/pdfs/* output/logs/*
```

