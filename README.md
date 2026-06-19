# 罗盘（Compass）

罗盘是面向小型装修、工程和项目型企业的经营执行与事实治理系统。

系统围绕“原始输入 → 候选事实 → 治理校验 → 人工确认 → 正式事实 → 查询、分析、建议、执行与反馈”组织前后端能力，用于解决项目经营信息分散、事实来源不清、上下文缺失、确认责任不明确以及状态不可追溯等问题。

> 当前仓库处于持续开发和验收阶段。目录、路由或模块已经存在，不代表对应业务能力已经全部完成生产验收。

## 核心原则

- **L2 正式事实是真源**：页面和汇总视图只消费正式事实，不自行创造事实。
- **S2 校验与人工确认不可绕过**：候选内容经过治理后，只有满足条件并完成人工确认，才能请求写入正式事实。
- **前端不决定最终状态**：H5 和 PC 只发起动作、承接状态和展示结果，最终权限、治理和入链规则由后端执行。
- **AI 只提供辅助能力**：AI 可以整理输入、转写语音、提取候选、生成分析或建议预览，但不代替治理裁决和人工确认。
- **来源链可追溯**：从原始输入、候选、治理结果、确认记录到正式事实保留关联关系。

## 主业务链路

```text
S1 运行上下文
      ↓
L0 原始输入
      ↓
L1 候选提取
      ↓
S2 治理校验
      ↓
人工确认 / 待补 / 驳回
      ↓
L2 正式事实
      ↓
L3 查询与视图
      ↓
L4 分析
      ↓
L5 建议
      ↓
L6 执行响应
      ↓
L7 反馈回流

S3 审计追踪横向贯穿关键动作
```

当前后端已经注册 L0–L7、S1–S3，以及上传、语音转写、AI 辅助和外部协同等路由。各模块实际完成度以测试、接口联调和阶段验收结果为准。

## 仓库结构

```text
.
├── apps/
│   ├── h5/                 # H5 主交互端
│   ├── pc/                 # PC 治理工作台
│   └── mobile-shell/       # Capacitor Android 移动端壳
├── services/
│   └── api/                # FastAPI 后端主服务
├── packages/
│   ├── contracts/          # OpenAPI 与 JSON Schema 契约
│   ├── shared-types/       # 共享类型
│   ├── shared-utils/       # 共享工具
│   └── native-bridge/      # 原生能力桥接
├── docs/
│   └── architecture/       # 必要架构说明
├── scripts/
│   └── check/              # 一致性检查脚本
├── data/                   # 本地开发与测试数据目录
├── storage/                # 上传原件等本地存储目录
├── .github/workflows/      # CI/CD 工作流
├── .env.example
├── package.json
└── package-lock.json
```

## 应用说明

### H5 主交互端

`apps/h5` 当前承接：

- 文本输入和“录入 / 查 / 问”分流；
- L0 → L1 → S2 → 待确认主链路；
- 人工确认后的 L2 入链请求；
- L3 正式事实只读查询；
- 项目运行上下文；
- 图片、PDF 等原件上传；
- 语音录入和查询；
- 待确认面板、消息流和移动端交互壳。

H5 采用页面组装层 + flow/hook 的结构。跨模块业务流程应保留在对应模块中，不应重新集中堆回 `H5MainPage.tsx`。

### PC 治理工作台

`apps/pc` 当前主要承接：

- 待处理中心；
- 人工确认、待补和驳回；
- 正式事实列表与查询；
- 当前用户、组织、角色和允许动作的运行范围展示。

PC 仍处于逐步完善阶段，不应将目录占位或页面入口描述为已完成能力。

### 移动端壳

`apps/mobile-shell` 使用 Capacitor 承接 Android 壳层和原生能力。移动端壳只负责容器、原生插件和 WebView 接入，不复制业务规则。

### 后端 API

`services/api` 基于 FastAPI，负责：

- 运行上下文和权限边界；
- 输入、候选、治理、确认和正式事实；
- L3 查询及 L4–L7 模块；
- 上传原件、语音转写和扩展能力；
- 数据持久化、状态校验和审计追踪。

API 默认前缀：

```text
/api/v1
```

健康检查：

```text
GET /health
```

## 技术栈

### 前端

- React 19
- TypeScript 6
- Vite 8
- npm workspaces
- Capacitor 8

### 后端

- Python 3.11+
- FastAPI
- SQLAlchemy
- Pydantic
- Pytest
- SQLite（开发环境默认）

## 快速启动

### 1. 安装前端依赖

仓库使用根级 npm workspace 和唯一根锁文件：

```bash
npm ci
```

不要在 `apps/*` 或 `packages/*` 下生成子级 `package-lock.json`。

### 2. 创建 Python 虚拟环境

```bash
python3 -m venv services/api/.venv
source services/api/.venv/bin/activate
pip install -r services/api/requirements.txt
```

### 3. 配置环境变量

```bash
cp .env.example .env
```

不要提交真实 `.env`、密钥、数据库或上传原件。

开发环境未显式配置数据库时，后端默认使用：

```text
data/dev/compass_dev.sqlite3
```

### 4. 启动后端

```bash
cd services/api
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

常用地址：

```text
健康检查：http://127.0.0.1:8000/health
OpenAPI 文档：http://127.0.0.1:8000/docs
```

### 5. 启动 H5

```bash
npm run dev --workspace @compass/h5
```

默认地址：

```text
http://127.0.0.1:5173
```

### 6. 启动 PC

```bash
npm run dev --workspace @compass/pc
```

默认地址：

```text
http://127.0.0.1:5174
```

H5 和 PC 开发服务器均将 `/api` 代理到 `http://127.0.0.1:8000`。

## 检查与测试

### 前端与契约总检查

```bash
npm run check
```

当前包括：

- H5 TypeScript 检查；
- PC TypeScript 检查；
- contracts 一致性检查。

### 前端构建

```bash
npm run build --workspace @compass/h5
npm run build --workspace @compass/pc
```

### 后端测试

```bash
cd services/api
pytest -q
```

### 契约更新与校验

后端路由或 Pydantic Schema 变化后：

```bash
python3 scripts/check/contracts_consistency.py --write-openapi
python3 scripts/check/contracts_consistency.py
```

契约检查通过只代表结构一致，不代表业务链路完成验收。

## 数据与 Git 边界

以下内容不应提交到 Git：

```text
.env
node_modules/
.venv/
dist/
build/
*.db
*.sqlite
*.sqlite3
*.tsbuildinfo
__pycache__/
.pytest_cache/
logs/
工作记录及报告/
02_development_basis/
03_control/
04_task_cards/
05_reports/
```

上传原件和开发数据库应保存在 `storage/`、`data/` 的开发或测试目录中，不作为源码提交。

## 开发约束

1. 不绕过 S2 治理和人工确认直接写入 L2。
2. 查询和汇总视图不得创造或修改正式事实。
3. 前端不得自行决定权限、治理结果和最终状态。
4. 不把 Mock、占位模块或预留接口描述成已完成能力。
5. 不在页面文件中重新集中堆放跨模块业务流程。
6. 不修改 `.env`、开发数据库和上传原件来伪造验收结果。
7. 状态、字段或接口变化必须同步检查 contracts。

## Git 工作流

建议使用独立分支完成开发和验收：

```bash
git switch -c feat/<task-name>
```

提交前至少执行：

```bash
git status --short --untracked-files=all
npm run check
```

涉及后端时还应执行：

```bash
cd services/api && pytest -q
```

当前 `main` 是稳定集成和部署分支。未经检查和人工确认，不应直接向 `main` 推送代码。

## 当前阶段说明

当前仓库已经具备：

- Monorepo 基础结构；
- H5、PC、移动端壳、后端和 contracts 分层；
- L0–L7、S1–S3 模块和后端路由；
- H5 主交互与 L0–L3 核心链路承接；
- PC 待确认、正式事实和权限范围工作台；
- OpenAPI 与 JSON Schema 一致性检查；
- GitHub Actions 部署工作流。

仍需持续通过测试、联调和页面验收确认的内容包括：

- L4–L7 的完整业务闭环；
- PC 全量治理能力；
- 移动端壳与原生能力完整集成；
- 权限、审计、外部协同和生产部署加固；
- 架构文档与实际代码状态持续同步。

## 使用范围

该仓库为私有业务系统代码。未经授权，不得复制、公开或用于其他项目。
