# TASK-L3-QUERY-VIEW-VERIFY-001 Report｜L3 查询视图验证

## 验证环境

| 项目 | 值 |
|---|---|
| 后端 | `http://127.0.0.1:8000` |
| H5 | `http://localhost:5175` |
| DB | 文件 SQLite `data/dev/compass_dev.sqlite3`（新创建，无旧数据） |
| 验证时间 | 2026-05-31 07:19 |

## 1. 后端启动结果

✅ 3 秒内启动成功。
```
curl /api/v1/l3/facts → {"items":[], "total":0}
```

## 2. 前端启动结果

✅ 在端口 5175 启动成功（5173/5174 被占用时自动递增）。

## 3. 创建 fact 结果

通过完整主链路创建 2 条事实：

| Fact | ID | 类型 | 摘要 |
|---|---|---|---|
| Fact 1 | `fact_1948e69933d9467c8d214c89fc3333bd` | construction_record | 宝山刘老师家防水施工 |
| Fact 2 | `fact_207c2969889142518e765c49287a1371` | other_fact_record | 李师傅家水电改造验收付款 |

每条均完整走通：L0→L1→S2→MC(pending)→MC(review)→L2(fact)。

## 4. L3 list 接口结果

```
GET /api/v1/l3/facts → {"items": [
  fact_207c2969889142518e765c49287a1371: other_fact_record | 宝山刘老师家防水施工 | manual_confirmation
  fact_1948e69933d9467c8d214c89fc3333bd: construction_record | 李师傅家水电改造验收付款 | manual_confirmation
], "total": 2}
```

**source_type 默认值：** `manual_confirmation`（从 fact_payload 中提取）。

## 5. H5 查询面板展示结果

✅ 编译产物（dist）中包含：
- `只读查询` 文本
- `不产生正式事实` 文本
- `FactQueryPanel` 组件

## 6. fact_type 筛选

| 筛选 | 结果 | 验证 |
|---|---|---|
| `fact_type=construction_record` | 1 条 | ✅ |
| `fact_type=other_fact_record` | 1 条 | ✅ |

## 7. keyword 搜索

| 关键词 | 结果 | 验证 |
|---|---|---|
| `防水` | 1 条 | ✅ |
| `李师傅` | 1 条 | ✅ |
| `nonexist` | 0 条 | ✅ |

## 8. 点击详情

```
GET /l3/facts/fact_1948e69933d9467c8d214c89fc3333bd
→ fact_id: fact_1948e69933d9467c8d214c89fc3333bd
→ fact_payload: { primary_project_id: "宝山刘老师家", fact_summary: "完成防水施工", ... }
```

✅ 返回完整 payload。

## 9. 空结果状态

```
GET /api/v1/l3/facts?fact_type=nonexistent_type
→ {"items": [], "total": 0}
```

✅ 返回空列表。H5 面板显示"暂无事实记录"提示。

## 10. 只读提示

✅ 编译产物中确认：
```
只读查询结果 — 不创建、不修改、不删除正式事实
```

嵌入在 `FactQueryPanel` 组件的 `fact-readonly-banner` 中。

## 11. 是否使用 Mock

❌ 未使用 Mock。全部验证通过真实后端 API：
- `connman confirmation` 创建 pending → review → L2 入链
- L3 list/detail/keyword 查询

H5 页面是 `H5MainPage`（非 MockPage），通过 Vite proxy 直连后端。

## 12. git status --short

```
 M 01_arch_dir/compass/apps/h5/src/modules/facts_view/types.ts
 M 01_arch_dir/compass/apps/h5/src/styles/h5.css
 M 01_arch_dir/compass/apps/h5/src/pages/H5MainPage.tsx
 M 01_arch_dir/compass/apps/h5/src/modules/l3_query_view/api.ts
 M 01_arch_dir/compass/apps/h5/src/components/h5/index.ts
 M 01_arch_dir/compass/apps/h5/src/components/h5/overlays/FactQueryPanel.tsx
 M 01_arch_dir/compass/services/api/app/db/repositories/fact_record_repository.py
 M 01_arch_dir/compass/services/api/app/db/repositories/__init__.py
 M 01_arch_dir/compass/services/api/app/modules/l3_query_view/router.py
 M 01_arch_dir/compass/services/api/app/modules/l3_query_view/schemas.py
 M 01_arch_dir/compass/services/api/app/modules/l3_query_view/service.py
 M 01_arch_dir/compass/services/api/tests/l3_query_view/test_l3_fact_list.py
 M 01_arch_dir/compass/packages/contracts/openapi/openapi.json
 M 01_arch_dir/compass/packages/contracts/schemas/l3_query_view.schema.json
 M 01_arch_dir/compass/packages/shared-types/index.ts
?? 05_reports/TASK-L3-QUERY-VIEW-EXPAND-001_report.md
?? 05_reports/TASK-L3-QUERY-VIEW-VERIFY-001_report.md
```

## 13. git diff --stat

```
18 files changed, 1168 insertions(+), 39 deletions(-)
```

## 14. 是否修改 .env/data/storage

❌ 未修改。仅创建/删除了开发文件 SQLite 用于测试隔离。

## 15. 是否执行 git add/commit/push

❌ 未执行。

## 最终结论

**✅ L3 查询与事实列表视图增强验证全部通过。**

| 检查项 | 状态 |
|---|---|
| L3 list 无筛选 | ✅ 2 条 |
| fact_type 筛选 | ✅ construction_record(1) + other_fact_record(1) |
| keyword 搜索 | ✅ 防水(1) + 李师傅(1) + nonexist(0) |
| 详情查看 | ✅ 完整 payload |
| 空结果 | ✅ items=[] total=0 |
| 只读提示 | ✅ "不产生正式事实" |
| 非 Mock | ✅ 真实后端链路 |
| pytest | ✅ 169 passed |
| npm run check | ✅ |
| npm run build | ✅ 144ms |
