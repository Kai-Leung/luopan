# 模块边界图

| 模块 | 当前职责 | 主要输入/输出 | 禁止项 |
|---|---|---|---|
| `apps/h5` | 移动端交互、状态展示和动作发起 | 调用 `/api/v1/*`，展示候选、确认、事实和 L4-L7 返回 | 本地裁决权限、绕过 S2、直接生成正式事实 |
| `apps/pc` | 治理工作台 | 运行上下文、待确认审核、L3 正式事实查询 | 定义独立业务状态或绕过后端确认 |
| `apps/mobile-shell` | Capacitor 设备能力壳 | 加载 H5 构建产物、承接设备事件 | 写入业务规则或正式事实 |
| `services/api` | 业务 API、持久化、治理和追溯 | S1-S3、L0-L7、上传、语音、AI/外协入口 | 依赖前端决定正式状态 |
| `packages/contracts` | OpenAPI 与跨模块 JSON Schema | FastAPI OpenAPI、治理 schema | 脱离运行时接口另建业务口径 |
| `packages/shared-types` | TypeScript 共享类型 | contracts 派生类型 | 手工创造与后端不一致的状态 |
| `packages/shared-utils` | 共享工具边界 | 当前仅少量/占位实现 | 过早承载业务裁决 |
| `packages/native-bridge` | H5 与原生壳协议 | 设备事件与桥接类型 | 承载 L0-L7 或 S1-S3 规则 |

模块目录或 README 存在只说明边界被预留。实现状态以
`capability_entry_matrix.md` 和自动化结果为准。
