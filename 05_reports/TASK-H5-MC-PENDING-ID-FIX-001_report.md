# TASK-H5-MC-PENDING-ID-FIX-001_report｜H5 人工确认 pending_id 修补

## 1. 任务结论

本补丁修复 H5 人工确认请求未传 `pending_id` 的 P0 问题。

修补后，H5 在调用：

```text
reviewManualConfirmation()
```

时会传入：

```text
pending_id: item.pending_id
```

使后端能够通过 `pending_id` 找到对应候选，并在确认通过后将：

```text
candidate.status
```

更新为：

```text
confirmed_candidate
```

从而支撑后续 L2 入链。

---

## 2. 修改文件

```text
01_arch_dir/compass/apps/h5/src/modules/input_flow/types.ts
01_arch_dir/compass/apps/h5/src/pages/H5MainPage.tsx
```

---

## 3. 修改内容

### 3.1 ManualConfirmationReviewRequest

新增字段：

```ts
pending_id?: string;
```

### 3.2 confirmPendingItem

调用 `reviewManualConfirmation()` 时新增：

```ts
pending_id: item.pending_id
```

---

## 4. 未修改范围

未修改：

```text
01_arch_dir/compass/services/api/
01_arch_dir/compass/packages/
02_development_basis/
03_control/
04_task_cards/
.env
data/
storage/
```

---

## 5. 验证要求

合并后执行：

```bash
cd 01_arch_dir/compass/apps/h5
npm run check
npm run build
```

如执行 E2E，需确认：

```text
H5 → L0 → L1 → S2 → manual_confirmation → L2 → L3
```

完整跑通。

---

## 6. 预期结果

- `npm run check` 通过；
- `npm run build` 通过；
- H5 端人工确认后，后端能更新 candidate 状态；
- L2 不再因 `only confirmed_candidate can enter L2` 阻断。
