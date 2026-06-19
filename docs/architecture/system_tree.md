# 系统目录树

本文记录当前 `Kai-Leung/luopan` 工程仓库的正式目录边界。

> 目录或模块存在，不代表对应业务能力已经完成生产验收。实际完成度以代码、测试、联调和阶段验收结果为准。

## 根目录

```text
.
├── .github/
│   └── workflows/          # CI/CD 工作流
├── apps/
│   ├── h5/                 # H5 主交互端
│   ├── pc/                 # PC 治理工作台
│   └── mobile-shell/       # Capacitor 移动端壳
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
│   └── check/              # 契约与一致性检查
├── data/                   # 本地开发、测试数据占位
├── storage/                # 本地上传与存储占位
├── .env.example
├── .gitignore
├── README.md
├── package.json
└── package-lock.json
```

## 前端目录

### `apps/h5`

H5 是当前主交互端，负责输入、查询、上传、语音和待确认等用户交互。

主要结构：

```text
apps/h5/src/
├── app/                    # 页面壳状态、返回键、Toast 等应用级 hook
├── components/h5/          # H5 展示组件和弹层
├── modules/                # 按业务能力划分的 flow、API、类型和状态
├── native/                 # 原生桥接运行时
├── pages/                  # 页面组装层
├── styles/                 # 页面样式
└── utils/                  # 浏览器安全工具
```

`H5MainPage.tsx` 应保持为页面组装层。L0–L3、S1、上传和语音流程应由对应模块承接，不得重新集中堆入页面文件。

### `apps/pc`

PC 当前承接待处理中心、正式事实查询和权限范围展示，后续按治理工作台路线扩展。

### `apps/mobile-shell`

移动端壳使用 Capacitor 承接 Android 容器和原生插件，不复制前后端业务规则。

## 后端目录

```text
services/api/app/
├── api/                    # 总路由装配
├── core/                   # 配置与基础能力
├── db/                     # SQLAlchemy 模型、会话和仓储
└── modules/                # L0–L7、S1–S3 及扩展模块
```

后端负责权限、治理、确认、正式事实、持久化和审计追踪，是最终业务状态的执行端。

## 契约目录

`packages/contracts` 承接：

- 运行时 OpenAPI 导出；
- 跨模块 JSON Schema；
- 前后端关键字段和状态的一致性检查。

后端 Pydantic Schema 与 FastAPI 路由是运行时 API 真源。字段或状态变化后必须同步执行契约检查。

## 数据与仓库边界

`data/` 和 `storage/` 只保留目录占位，不提交真实开发数据库、上传原件和运行数据。

以下内容不得进入当前源码树：

```text
工作记录及报告/
02_development_basis/
03_control/
04_task_cards/
05_reports/
node_modules/
.venv/
dist/
build/
数据库文件
编译缓存
```

开发依据、任务卡和执行报告应保存在仓库外部的开发档案目录，或使用独立的文档管理方式。
