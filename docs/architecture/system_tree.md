# 系统目录树

本页只描述当前仓库可验证的目录职责，不代表目录内能力已经通过业务验收。

```text
.
├── apps/
│   ├── h5/                 React/Vite H5 主交互应用
│   ├── pc/                 React/Vite PC 治理工作台
│   └── mobile-shell/       Capacitor 原生壳配置
├── services/
│   └── api/                FastAPI、SQLAlchemy 与 pytest
├── packages/
│   ├── contracts/          OpenAPI 快照和 JSON Schema
│   ├── shared-types/       共享 TypeScript 类型
│   ├── shared-utils/       共享工具边界
│   └── native-bridge/      H5 与原生壳协议边界
├── docs/                   架构、开发、部署和运维说明
├── scripts/check/          contracts 与仓库治理检查
├── tests/                  顶层验收目录占位
├── data/                   本地数据库目录，仅跟踪 .gitkeep
├── storage/                本地文件目录，仅跟踪 .gitkeep
├── ops/                    运维目录占位
├── .github/workflows/      CI 与人工部署 workflow
├── package.json            npm workspaces 和统一检查脚本
└── AGENTS.md               仓库执行边界
```

当前 Node workspace 只使用根 `package-lock.json`。后端依赖由
`services/api/requirements.txt` 管理。
