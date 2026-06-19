# Compass 部署文档

## 服务器信息

| 项目 | 值 |
|---|---|
| IP | 82.156.128.251 |
| 云厂商 | 腾讯云 |
| OS | OpenCloudOS 9.4 (x86_64) |
| RAM | 1.9 GiB |
| 磁盘 | 40 GiB（已用 8 GiB） |
| 架构 | x86_64 |

## 部署路径

| 项目 | 路径 |
|---|---|
| 项目根目录 | `/root/compass` |
| 后端代码 | `/root/compass/services/api` |
| Python venv | `/root/compass/services/api/.venv` |
| 前端静态文件 | `/www/wwwroot/82.156.128.251` |
| 数据目录 | `/root/compass/data/dev` |
| 日志目录 | `/www/wwwlogs/` |

## 服务

| 服务 | 说明 |
|---|---|
| `compass-backend.service` | FastAPI 后端（systemd 管理） |
| nginx | 宝塔面板管理（`/www/server/nginx/`） |

## 端口

| 端口 | 指向 | 说明 |
|---|---|---|
| 80 | nginx → 127.0.0.1:8000 (api) / 静态文件 (其他) | 公网访问 |
| 8000 | 后端 uvicorn (0.0.0.0) | API 内部 |
| 888 | 宝塔 phpMyAdmin | 仅内网 |
| 22 | SSH | 远程连接 |

## nginx 代理配置

- 主站点配置：`/www/server/panel/vhost/nginx/82.156.128.251.conf`
- `/api/` 前缀 → 反向代理到 `http://127.0.0.1:8000`
- 其他路径 → 静态文件 `root /www/wwwroot/82.156.128.251`
- SPA fallback：`try_files $uri $uri/ /index.html`

## systemd 服务配置

- 文件：`/etc/systemd/system/compass-backend.service`
- 启动命令：`systemctl {start|stop|restart|status} compass-backend`
- 工作目录：`/root/compass/services/api`
- 启动命令：
  ```
  /root/compass/services/api/.venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
  ```

## API 验证端点

```
http://82.156.128.251/api/v1/l3/facts
```

## 环境版本对照

| 工具/包 | 本地 (macOS 26.5) | 服务器 (OpenCloudOS 9.4) | 一致 |
|---|---|---|---|
| Python | 3.12.13 | 3.12.12+ | ✅ (仅小版本差) |
| Node.js | v22.16.0 | v22.14.0 | ✅ |
| npm | 11.16.0 | 10.9.2 | ✅ |
| FastAPI | 0.136.3 | 0.136.3 | ✅ 完全一致 |
| uvicorn | 0.48.0 | 0.48.0 | ✅ 完全一致 |
| SQLAlchemy | 2.0.50 | 2.0.50 | ✅ 完全一致 |
| Pydantic | 2.13.4 | 2.13.4 | ✅ 完全一致 |
| pytest | 9.0.3 | — | — |
| httpx | 0.28.1 | — | — |
| nginx | — | 1.26.3 (宝塔) | — |

> Python 版本本地 3.12.13，服务器 3.12.12+，都是 3.12 系列，兼容。

## 环境变量（`.env`）

```
DATABASE_URL=sqlite:///./data/dev/compass_dev.sqlite3
STORAGE_PATH=./storage/dev
RAW_STORE_PATH=./data/dev/raw_store
VITE_API_BASE_URL=http://localhost:8000
```

> 当前服务器 `.env` 文件在 `/root/compass/services/api/` 目录。

## 前端开发服务器

| 项目 | 值 |
|---|---|
| 开发服务器 | 0.0.0.0:5173 |
| 预览服务器 | 0.0.0.0:4173 |
| 开发 API 代理 | /api → http://127.0.0.1:8000 |

## Git / CI

- 仓库：`git@github.com:Kai-Leung/luopan.git`
- 部署方式：SCP 打包上传 / 未来 GitHub Actions 自动部署
- Workflow 文件：`.github/workflows/deploy.yml`

## 已知限制

1. HTTP（非 HTTPS），浏览器原生语音识别不可用
2. 后端 ASR 未配置（预留讯飞接口）
3. 无域名绑定，仅通过 IP 访问
4. 前端为静态 H5，无 SSR
