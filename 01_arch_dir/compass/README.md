# Compass 罗盘系统 Monorepo

目录架构版本：ARCH_DIR_v0.1.0

当前代码根目录已经采用 `apps/`、`services/`、`packages/` 的 Monorepo 结构，不再使用 `frontend/`、`backend/` 旧目录。

核心口径：
- S1/S2/S3 = 横向架构。
- L0-L7 = 纵向业务链路。
- `apps/h5` 为 H5 主交互应用。
- `apps/pc` 为 PC 治理工作台。
- `apps/mobile-shell` 为 Capacitor 原生壳。
- `services/api` 为 FastAPI 后端主系统。
- `packages/contracts` 约束前后端字段与处理方向。
- `packages/shared-types`、`packages/shared-utils`、`packages/native-bridge` 承接共享边界。
- `data/`、`storage/` 不纳入真实业务数据和文件。

前端 workspace 依赖统一在代码根目录安装，不在子项目生成独立锁文件：

```bash
npm ci
```

统一静态检查：

```bash
npm run check
```
