# packages/contracts

OpenAPI 与 JSON Schema 契约。

契约真源规则：

1. 后端 Pydantic Schema 与 FastAPI 路由是运行时 API 真源。
2. `openapi/openapi.json` 必须由运行时 OpenAPI 完整导出，不允许只保留局部路径。
3. `schemas/` 承接跨模块治理、页面动作和非单一接口 JSON Schema。
4. `packages/shared-types/index.ts` 与 H5 中保留的关键枚举镜像必须和后端一致。
5. 字段或状态变化后，执行：

```text
python3 scripts/check/contracts_consistency.py --write-openapi
python3 scripts/check/contracts_consistency.py
```

检查器只校验契约一致性，不代表业务验收或阶段准出。
