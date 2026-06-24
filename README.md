# Compass 罗盘系统 Monorepo

Compass 是围绕可信事实链路构建的前后端 Monorepo。纵向链路使用 L0-L7 表示输入、候选、正式事实、查询、分析、建议、执行响应与反馈；S1、S2、S3 分别承接运行上下文、治理闸门和审计追溯。

目录、路由、类型或骨架存在只说明代码入口存在，不代表功能已完成业务验收。能力状态以代码、自动化结果和独立验收证据共同判断。

## 当前实现状态

- H5：可运行的 React/Vite 应用，承接录入、L3 查询、L4-L7 交互、上传、语音转写入口和人工确认流程。前端不裁决权限、S2 结果或正式事实。
- PC：可运行的 React/Vite 治理工作台，展示运行上下文、待确认事项和正式事实，并调用后端执行人工审核。
- Pending confirmation：数据库保存 active/resolved 生命周期；人工审核完成后保留历史记录，但不再出现在待确认列表。
- Mobile shell：已配置 Capacitor 壳和 H5 构建目录；原生工程生成、签名与真机验收不在仓库基线内。
- API：FastAPI 模块化单体，包含 S1-S3、L0-L7、上传、语音、AI 辅助和外部反馈入口。自动化测试已归零，但尚未完成独立人工业务验收。
- Contracts：保存运行时 OpenAPI 快照和跨模块 JSON Schema，并提供一致性检查脚本。

## 目录结构

```text
apps/
  h5/             H5 主交互应用
  pc/             PC 治理工作台
  mobile-shell/   Capacitor 原生壳配置
services/
  api/            FastAPI 后端与 pytest
packages/
  contracts/      OpenAPI 与 JSON Schema
  shared-types/   共享 TypeScript 类型
  shared-utils/   共享工具边界
  native-bridge/  H5 与原生壳协议边界
docs/             架构、开发、部署和运维说明
scripts/check/    contracts 与仓库治理检查
data/             本地数据库目录，仅跟踪 .gitkeep
storage/          本地文件目录，仅跟踪 .gitkeep
```

## 环境变量

复制 `.env.example` 的字段到本地环境或未跟踪的 `.env` 文件。不要提交真实值。

- `DATABASE_URL`：后端数据库连接；生产环境必须显式配置。
- `STORAGE_PATH`：本地文件存储路径。
- `RAW_STORE_PATH`：原始输入存储路径。
- `VITE_API_BASE_URL`：前端 API 地址；本地 Vite 默认通过 `/api` 代理到 `127.0.0.1:8000`。
- 语音供应商凭据使用后端配置中的对应环境变量，禁止进入仓库。

pytest 默认使用内存 SQLite；普通开发运行在未配置数据库时使用 `data/dev/compass_dev.sqlite3`。

## 安装与本地运行

Node workspace 只使用根锁文件：

```bash
npm ci
```

后端建议使用独立虚拟环境：

```bash
python3 -m venv services/api/.venv
services/api/.venv/bin/python -m pip install -r services/api/requirements.txt
cd services/api
.venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8000
```

启动前端：

```bash
npm run dev --workspace @compass/h5
npm run dev --workspace @compass/pc
```

H5 默认端口为 `5173`，PC 默认端口为 `5174`。

## 检查与构建

```bash
npm run check
npm run build --workspace @compass/h5
npm run build --workspace @compass/pc
npm test --workspace @compass/h5
npm test --workspace @compass/pc
python3 scripts/check/contracts_consistency.py
cd services/api && python3 -m pytest -q
```

- `npm run check` 是 TypeScript、contracts 和仓库策略检查；H5/PC 测试和 pytest 需分别执行。
- build 成功只证明可构建，不代表业务验收完成。
- pytest 失败必须如实记录，不得通过修改业务规则来掩盖。

## Git 与 Pull Request

1. 从最新 `main` 创建任务分支。
2. 只提交任务范围内文件。
3. 运行与改动匹配的检查。
4. push 分支并创建以 `main` 为 base 的 Pull Request。
5. Pull Request 和开发分支只运行 CI，不触发生产部署。
6. `main` 的运行代码变更只有在 repository policy、frontend、contracts、backend 和 integration 全部成功后，才自动调用部署 workflow。
7. 文档或纯 Markdown 变更不触发生产部署；`workflow_dispatch` 保留人工触发能力。
8. 自动部署前后都要求服务器 Git 工作区干净，并校验部署后的 HEAD 等于指定 commit SHA。
9. 未经人工审核不得合并；任何失败检查都不得被部署绕过。

仓库执行边界见 `AGENTS.md`，真实能力状态见 `docs/architecture/capability_entry_matrix.md`。
