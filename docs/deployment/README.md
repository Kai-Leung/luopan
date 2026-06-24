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
- CI workflow：`.github/workflows/ci.yml`
- 部署 workflow：`.github/workflows/deploy.yml`
- Pull Request 和开发分支只运行 CI，不部署。
- `main` push 必须先通过 repository-policy、frontend、contracts、backend 和 integration。
- 仅运行代码路径变化时，CI 才自动调用 reusable deploy workflow。
- README、`docs/**` 和纯 Markdown 变更默认不部署。
- `workflow_dispatch` 保留手动部署能力。
- 生产部署使用通过 CI 的 commit SHA、`git fetch`、`git merge --ff-only`、后端重启及 `/health` 校验。
- 更新前后均检查 tracked、staged 和未跟踪文件；工作区不干净时立即失败，不执行 reset、clean、stash 或服务重启。
- 更新后 `git rev-parse HEAD` 必须严格等于部署目标 SHA。

## 当前部署真实性

当前 workflow 的生产动作只有：

1. 确认 `/root/compass` 是有效且干净的 Git 工作区。
2. 将 `/root/compass` 快进到指定 commit SHA，并核对最终 HEAD。
3. 重启 `compass-backend`。
4. 验证 `/health` 返回 `status=ok` 且 `service=Compass`。

仓库中没有 H5/PC build 产物复制到 `/www/wwwroot/82.156.128.251` 的自动化步骤。
因此当前受控自动部署仅能确认后端更新；H5/PC 静态发布仍是集成验收前缺口，
不得描述为已经自动部署。本治理任务没有实际触发部署。

## 已知限制

1. HTTP（非 HTTPS），浏览器原生语音识别不可用
2. 后端 ASR 未配置（预留讯飞接口）
3. 无域名绑定，仅通过 IP 访问
4. 前端为静态 H5，无 SSR
5. 自动部署仍使用 root + password；后续应改为专用 deploy 用户、SSH key、最小权限、release 目录和自动回滚
