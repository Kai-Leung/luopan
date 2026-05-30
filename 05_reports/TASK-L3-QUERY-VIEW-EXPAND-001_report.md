# TASK-L3-QUERY-VIEW-EXPAND-001 Report｜L3 查询视图扩展

## 修改文件清单

| 文件 | 操作 | 说明 |
|---|---|---|
| `services/api/app/db/repositories/fact_record_repository.py` | ✅ 新增 `list_fact_records()` | 支持 fact_type/keyword 筛选 + limit/offset 分页 |
| `services/api/app/db/repositories/__init__.py` | ✅ 导出 `list_fact_records` | 对外暴露 |
| `services/api/app/modules/l3_query_view/schemas.py` | ✅ 新增 `L3FactListItem`, `L3FactListQueryParams`, `L3FactListResponse` | 列表查询 schema |
| `services/api/app/modules/l3_query_view/service.py` | ✅ 新增 `_extract_summary()`, `_extract_source_type()`, `list_l3_facts()` | 从 fact_payload 提取摘要/来源 |
| `services/api/app/modules/l3_query_view/router.py` | ✅ 新增 `GET /l3/facts` list 端点 | 支持 fact_type/keyword/limit/offset |
| `services/api/tests/l3_query_view/test_l3_fact_list.py` | ✅ **新增** 6 个测试 | 覆盖无结果、分页、筛选、keyword |
| `apps/h5/src/modules/l3_query_view/api.ts` | ✅ 重写 | 新增 `listL3Facts()`, `getL3FactDetail()` |
| `apps/h5/src/modules/facts_view/types.ts` | ✅ 新增 `L3FactListItem`, `L3FactListResponse` | 前端类型 |
| `apps/h5/src/components/h5/overlays/FactQueryPanel.tsx` | ✅ **新增** 完整事实查询面板 | 筛选、列表、详情弹窗、空状态、加载更多 |
| `apps/h5/src/components/h5/index.ts` | ✅ 导出 `FactQueryPanel` | |
| `apps/h5/src/pages/H5MainPage.tsx` | ✅ 集成事实查询入口 | header 添加 📋 按钮 + 面板渲染 |
| `apps/h5/src/styles/h5.css` | ✅ 追加 200+ 行样式 | 面板布局、列表、筛选、详情弹窗 |
| `packages/contracts/openapi/openapi.json` | ✅ 更新 | 含新 list 端点 + schemas |
| `packages/contracts/schemas/l3_query_view.schema.json` | ✅ 更新 | 含 L3FactListItem + L3FactListResponse |
| `packages/shared-types/index.ts` | ✅ 追加 L3FactListItem + L3FactListResponse | |

## 新增接口说明

| 方法 | 路径 | 参数 | 返回 | 说明 |
|---|---|---|---|---|
| `GET` | `/api/v1/l3/facts` | `fact_type?`, `keyword?`, `limit`(默认20), `offset`(默认0) | `{items: [...], total: int}` | 列表查询，支持筛选 + 分页 |
| `GET` | `/api/v1/l3/facts/{fact_id}` | path | `L3FactViewResponse` | 单条详情（已有，保留） |

## 新增页面/组件说明

| 组件 | 路径 | 功能 |
|---|---|---|
| `FactQueryPanel` | `components/h5/overlays/FactQueryPanel.tsx` | 全屏面板，含筛选栏、只读提示、空状态、事实列表、详情弹窗、"加载更多"按钮 |
| header 📋 按钮 | `pages/H5MainPage.tsx` | 点击打开事实查询面板 |

## contracts/shared-types 修改说明

- `l3_query_view.schema.json`：新增 `L3FactListItem` 和 `L3FactListResponse` 定义
- `shared-types/index.ts`：追加对应 TypeScript 接口定义
- `facts_view/types.ts`：追加对应前端类型

## pytest -q 原文结果

```
........................................................................ [ 42%]
........................................................................ [ 85%]
....................                                                       [100%]
=============================== warnings summary ===============================
... (3 个 FastAPI 弃用警告)
-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
169 passed, 3 warnings in 1.07s
```

## npm run check 原文结果

```
> @compass/h5@0.1.0 check
> tsc -b

退出码: 0
```

## npm run build 原文结果

```
> @compass/h5@0.1.0 build
> tsc -b && vite build

vite v8.0.14 building client environment for production...
✓ built in 144ms

退出码: 0
```

## git diff --stat

```
packages/contracts/openapi/openapi.json                     | 1186 ++++++++++---------
packages/contracts/schemas/l3_query_view.schema.json         |   64 +-
packages/shared-types/index.ts                               |   16 +
services/api/app/db/repositories/__init__.py                 |    6 +-
services/api/app/db/repositories/fact_record_repository.py   |   20 +
services/api/app/modules/l3_query_view/router.py             |   30 +-
services/api/app/modules/l3_query_view/schemas.py            |   28 +-
services/api/app/modules/l3_query_view/service.py           |   62 +-
services/api/tests/l3_query_view/test_l3_fact_list.py        |  127 ++
apps/h5/src/components/h5/index.ts                           |    1 +
apps/h5/src/components/h5/overlays/FactQueryPanel.tsx         |  212 ++++
apps/h5/src/modules/facts_view/types.ts                       |   11 +
apps/h5/src/modules/l3_query_view/api.ts                     |   30 +-
apps/h5/src/pages/H5MainPage.tsx                              |    5 +
apps/h5/src/styles/h5.css                                    |  248 +++++
15 files changed, 1386 insertions(+), 660 deletions(-)
```

## 禁止项检查

| 禁止项 | 状态 |
|---|---|
| 修改 .env / data / storage | ❌ 未修改 |
| 修改 02_development_basis / 03_control / 04_task_cards | ❌ 未修改 |
| 修改 L2 入链规则 / S2 放行规则 | ❌ 未修改 |
| 修改 AI 主链路 | ❌ 未修改 |
| 新增未实现 API | ❌ 均为真实后端端点 |
| git add / commit / push | ❌ 未执行 |

## 阻断项和下一步建议

**无阻断项。** 后端 169 passed，前端 check + build 通过，新 API 验证正常。

**下一步建议：**
1. 给腾讯云服务器上部署（后端 + 前端）；
2. 后续可在 L3 list 基础上增加更丰富的筛选条件（如时间范围）；
3. 可考虑在事实详情中展示来源链（raw_input → candidate → s2 → review → l2）。
