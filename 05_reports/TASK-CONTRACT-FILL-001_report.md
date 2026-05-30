# TASK-CONTRACT-FILL-001 Report｜Contracts 补全

## 修改文件清单

| 文件 | 操作 | 说明 |
|---|---|---|
| `packages/contracts/openapi/openapi.json` | ✅ 重写 | 精简为 L0-L3 + MC + health 的 OpenAPI 规范 |
| `packages/contracts/schemas/l0_input.schema.json` | ✅ 更新 | RawInputCreate / RawInputReceived 定义 |
| `packages/contracts/schemas/l1_candidate.schema.json` | ✅ 更新 | L1CandidateCreate / L1CandidateItem / L1CandidateResponse |
| `packages/contracts/schemas/s2_governance_gate.schema.json` | ✅ 更新 | S2GovernanceCheckRequest / S2GovernanceCheckResponse |
| `packages/contracts/schemas/manual_confirmation.schema.json` | ✅ **新增** | Pending 创建/列表/审查 Request+Response 全部覆盖 |
| `packages/contracts/schemas/l2_fact.schema.json` | ✅ 更新 | L2FactCreateRequest / L2FactResponse |
| `packages/contracts/schemas/l3_query_view.schema.json` | ✅ 更新 | L3FactViewResponse |
| `packages/shared-types/index.ts` | ✅ **新增** | 全部 TypeScript 类型定义（枚举 + 接口），从真实 OpenAPI 生成 |
| `packages/shared-types/README.md` | ✅ 更新 | 用法说明 + 来源声明 |

## 覆盖的 API

| API | 方法 | Contracts | Shared Types |
|---|---|---|---|
| L0 原始输入 | POST | ✅ | ✅ |
| L1 候选 | POST | ✅ | ✅ |
| S2 治理检查 | POST | ✅ | ✅ |
| MC 创建待确认 | POST | ✅ | ✅ |
| MC 列表待确认 | GET | ✅ | ✅ |
| MC 审查确认 | POST | ✅ | ✅ |
| L2 入链 | POST | ✅ | ✅ |
| L3 查询 | GET | ✅ | ✅ |

## SourceType 统一

所有 contracts 中 SourceType 枚举值包含 `manual_confirmation`，与后端 Pydantic schema 一致。

## 验证结果

| 检查项 | 结果 |
|---|---|
| pytest -q | **163 passed, 3 warnings** ✅ |
| npm run check | **tsc -b 通过** ✅ |
| npm run build | **vite build 136ms 通过** ✅ |

## git diff --stat

```
packages/contracts/openapi/openapi.json                         | 952 ++++++++-------
packages/contracts/schemas/l0_input.schema.json                  |  40 ++--
packages/contracts/schemas/l1_candidate.schema.json              |  64 ++---
packages/contracts/schemas/l2_fact.schema.json                   |  50 ++---
packages/contracts/schemas/l3_query_view.schema.json             |  30 ++--
packages/contracts/schemas/manual_confirmation.schema.json       |  92 ++++++++++
packages/contracts/schemas/s2_governance_gate.schema.json        |  56 ++----
packages/shared-types/README.md                                  |  14 ++-
packages/shared-types/index.ts                                   | 248 ++++++++++++++++++
9 files changed, 997 insertions(+), 549 deletions(-)
```

## 禁止项检查

| 禁止项 | 状态 |
|---|---|
| 修改 apps/h5/ | ❌ 未修改 |
| 修改 services/api/ | ❌ 未修改 |
| 修改 .env/data/storage | ❌ 未修改 |
| git add/commit/push | ❌ 未执行 |
