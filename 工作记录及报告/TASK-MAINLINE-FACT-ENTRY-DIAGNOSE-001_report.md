# TASK-MAINLINE-FACT-ENTRY-DIAGNOSE-001 Report

## Status

Completed with verification deferred to executor/user.

## Goal

Diagnose and minimally repair the H5 to L2/L3 mainline so a normal material purchase record can become a pending confirmation item, be manually confirmed, enter L2, and be queried from L3.

## Files Modified

- `01_arch_dir/compass/apps/h5/src/pages/H5MainPage.tsx`
- `01_arch_dir/compass/apps/h5/src/modules/input_flow/api/client.ts`
- `01_arch_dir/compass/services/api/app/modules/l1_candidate/extractor.py`
- `01_arch_dir/compass/services/api/app/modules/l1_candidate/segmenter.py`
- `01_arch_dir/compass/services/api/app/modules/standard_governance/rules/field_rules.py`
- `01_arch_dir/compass/services/api/tests/l1_candidate/test_candidate.py`
- `01_arch_dir/compass/services/api/tests/e2e/test_l0_l3_mainline.py`
- `05_reports/TASK-MAINLINE-FACT-ENTRY-DIAGNOSE-001_report.md`

## Diagnosis

- L1 text segmentation treated amount fragments such as `花了3200元` as a separate candidate after punctuation split. This could create an orphan candidate instead of one complete purchase record.
- L1 field extraction was too broad for project and subject. It could extract `今天张师傅在宝山项目` as project and `今天张师傅` as subject.
- H5 created pending confirmations but did not open the pending confirmation panel automatically, making the mainline feel disconnected.
- H5 API error handling hid backend error details, making confirmation/L2 failures hard to diagnose.

## Fixes

- Kept amount continuations such as `花了3200元` with the preceding material purchase sentence.
- Added extraction support for ordinary Chinese names before purchase/construction verbs.
- Added extraction support for material and quantity fields.
- Cleaned project and subject extraction values.
- Automatically opens the pending confirmation panel when new pending items are created.
- Shows backend error details in H5 API failures.

## Expected Mainline

Example input:

`宝山项目张三买了500袋水泥，花了3200元`

Expected flow:

L0 raw input -> L1 one purchase candidate -> S2 auto pass -> pending confirmation -> manual confirm -> L2 fact -> L3 keyword query `水泥`.

## Tests Added/Updated

- Updated L1 extraction tests for clean project/subject extraction.
- Added L1 coverage that material purchase amount continuation stays in one candidate.
- Added E2E coverage for material purchase entering L2 and appearing in L3 query.

## Verification

- `pytest -q`: not run; AGENTS.md forbids Codex from executing pytest.
- `npm run check`: not run; AGENTS.md forbids Codex from executing npm verification.
- `npm run build`: not run; AGENTS.md forbids Codex from executing build.

## Boundaries

- No AI integration added.
- L2 entry rule not relaxed.
- S2/manual confirmation rule not bypassed.
- `.env` not modified.
- `data/` not modified.
- `storage/` not modified.
- git add/commit/push not run.

## Risk

Medium-low. The fix improves deterministic L1 parsing and H5 linkage without changing the formal S2/L2 gate. Executor verification is required.
