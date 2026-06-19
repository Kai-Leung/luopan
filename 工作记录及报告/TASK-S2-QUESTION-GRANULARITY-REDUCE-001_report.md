# TASK-S2-QUESTION-GRANULARITY-REDUCE-001 Report

## Status

Completed with verification deferred to executor/user.

## Goal

Reduce S2 over-questioning after project context is present, so ordinary low-risk records do not keep asking for non-essential construction object, material, or supplier details.

## Files Modified

- `01_arch_dir/compass/services/api/app/modules/standard_governance/rules/field_rules.py`
- `01_arch_dir/compass/services/api/tests/s2_governance_gate/test_governance.py`
- `01_arch_dir/compass/services/api/tests/standard_governance/test_rules.py`
- `01_arch_dir/compass/apps/h5/src/modules/standard_governance/fieldRules.ts`
- `05_reports/TASK-S2-QUESTION-GRANULARITY-REDUCE-001_report.md`

## Governance Adjustment

- Removed low-risk construction detail blocking for `object_asset_name`.
- Removed ordinary material/purchase blocking for `material_asset_id` and `related_subject_ids`.
- Kept global required field as `primary_project_id`.
- Kept high-risk conditional fields:
  - `evidence_refs`
  - `confirmation_scope`
- Kept source/document conditional fields:
  - `source_record_id`
  - `document_asset_type`

## Expected User Behavior

- If a user has not selected or provided a project, S2 still asks for project.
- If the project is present, ordinary construction/material text should proceed to confirmation instead of repeatedly asking for location, object, supplier, or material details.
- High-risk payment/change/risk content can still ask for evidence and confirmation scope.
- Uploaded or external-source content can still require source record details.

## Tests Updated

- Updated S2 governance tests so low-risk construction without project asks only for project.
- Updated material/purchase tests so supplier/material details no longer block ordinary records.
- Updated standard governance rule test so waterproof/construction detail absence does not block when project exists.

## Boundaries

- L2 entry rule not modified.
- S2 confirmation/manual review rule not modified.
- manual_confirmation rule not modified.
- `.env` / `data` / `storage` not modified.
- git add/commit/push not run.

## Verification

- `pytest -q`: not run; current AGENTS/custom instructions reserve pytest execution for executor/user.
- `npm run check`: not run; current AGENTS/custom instructions reserve npm verification for executor/user.
- `npm run build`: not run; current AGENTS/custom instructions forbid Codex build execution.

## Risk

Medium-low. This reduces S2 friction for ordinary records while retaining blockers for missing project, high-risk fields, uploaded/external source records, and document records.
