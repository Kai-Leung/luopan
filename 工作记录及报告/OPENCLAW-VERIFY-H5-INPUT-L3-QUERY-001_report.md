# OPENCLAW-VERIFY-H5-INPUT-L3-QUERY-001 Report

## 1. git diff --stat

```
01_arch_dir/compass/apps/h5/src/modules/l3_query_view/api.ts  | 16 +++++--
01_arch_dir/compass/apps/h5/src/pages/H5MainPage.tsx          | 55 +++++++++++++++++++++-
2 files changed, 65 insertions(+), 6 deletions(-)
```

## 2. git status

```
 M apps/h5/src/modules/l3_query_view/api.ts
 M apps/h5/src/pages/H5MainPage.tsx
?? apps/h5/tests/
```

仅 2 个修改文件 + 1 个新增测试目录，符合范围。

## 3. 实际执行命令

```
npm run check   → tsc -b                    退出码: 0
npm run build   → tsc -b && vite build      退出码: 0
```

## 4. 构建/检查结果

| 命令 | 结果 |
|---|---|
| `npm run check` (tsc -b) | ✅ 通过 |
| `npm run build` | ✅ 通过（56 modules, 138ms） |
| 编译产物大小 | `H5MainPage-CoQZKCYk.js` 51.84kB（之前 50.29kB，+1.55kB 符合预期） |

## 5. 测试结果

测试文件 `apps/h5/tests/h5-input-l3-query.verify.ts` 因 `tsconfig.json` 的 `include: ["src"]` 不在 tsc 范围内，无法通过命令行直接执行（Node ESM 不支持 Bundler moduleResolution）。

该测试文件为纯逻辑验证（不涉及 DOM/React），可挂载到 vitest/jest 后运行。当前项目无正式 H5 测试框架。

## 6. 是否触碰禁止目录

❌ 未触碰 `.env`、`data/`、`storage/`、`Raw Store`、密钥文件。

## 7. Codex 代码问题检查

### ✅ 正确项

| 检查点 | 结果 |
|---|---|
| **query 分支不进入 L0** | ✅ `submitText()` 中 `action === '查'` 在第 208 行提前 `return`，不经过 `shouldSubmitToL0()` 和 L0 API 调用 |
| **语音 query 分支不进入 L0** | ✅ 语音回调中 `action === '查'` 在第 425 行直接调用 `queryExistingFacts()` 并 `return` |
| **record 保留原链路** | ✅ `shouldSubmitToL0('录入')` 返回 `true`，正常走 L0→L1→S2 |
| **analysis 仍提示待接入** | ✅ text submit 中 `shouldSubmitToL0('问')` 返回 `false`，显示"分析能力待接入，未进入 L0"；语音中同理 |
| **api.ts 工具函数拆分** | ✅ `buildL3FactListPath()` 抽出，`listL3Facts()` 保留原名不变，测试文件可复用 `buildL3FactListPath` |
| **L3FactListItem 类型匹配** | ✅ `created_at` 字段在 `facts_view/types.ts` 中已定义（`created_at: string`） |
| **导入路径正确** | ✅ `api.ts` 从 `'../facts_view/types'` 导入类型；`H5MainPage.tsx` 从 `'../modules/l3_query_view/api'` 和 `'../modules/facts_view/types'` 导入 |
| **requestJSON 调用** | ✅ `listL3Facts()` 复用已有的 `requestJSON` 包装器，带有 `errorMessage` |
| **查询结果只读提示** | ✅ `formatReadonlyFactQueryMessage()` 显示"本次为 L3 只读查询，不产生正式事实，不写入 L0/L1/L2，不作为 AI 分析结论" |
| **查询失败处理** | ✅ 捕获异常后显示"本次查询不产生正式事实，不写入 L0/L1/L2，也不作为 AI 分析结论" |

### ⚠️ 潜在问题

| 问题 | 严重度 | 说明 |
|---|---|---|
| `resolveTextInputIntent` 默认行为 | 低 | 当 text 不匹配 `isQueryIntent` 和 `isAnalysisIntent` 时默认返回 `'record'`。用户输入"查防水"→query ✅，但"防水记录有哪些" 也可能触发 `isAnalysisIntent`（含"哪些"关键词）。这是现有 `h5Interaction.ts` 的逻辑，非本次改动引起。 |
| 测试文件不可直接运行 | 低 | `tsconfig.json` 的 `include: ["src"]` 不包含 `tests/` 目录。测试文件需配合 vitest/jest 或修改 tsconfig 才能运行。Codex 需要确认测试文件是给人阅读还是需要自动化执行。 |
| `source_type` 字段 | 低 | `L3FactListItem.source_type` 默认 `"manual_confirmation"`（从 fact_payload 提取），查询结果中展示的 source_type 可能与 L2 实际 source_type 不符。但这是后端逻辑，非前端改动问题。 |

## 8. 是否建议退回 Codex 修补

**否。** 本次改动干净、范围可控、构建通过。无阻断性问题。

建议：
1. 如果测试文件需要自动执行，需在 `tsconfig.json` 新增 `"include": ["src", "tests"]` 或配置 vitest
2. 后续可在 `resolveTextInputIntent` 的 `isQueryIntent` 中增加更多中文前缀匹配（如"搜索"、"找一下"）
