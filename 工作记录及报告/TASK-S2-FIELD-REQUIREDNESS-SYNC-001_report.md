# TASK-S2-FIELD-REQUIREDNESS-SYNC-001 Report

## Status

Completed with verification deferred to executor/user.

## Goal

Align current S2 governance with the field-rule intent: do not block ordinary records on overly detailed fields after H5 has already collected project context.

## Basis Read

- `02_development_basis/.../30_标准治理/02_字段规范总表.md` discovered as the formal field standard source.
- `02_development_basis/.../30_标准治理/08_校验规则口径.md` discovered as validation basis.
- `02_development_basis/.../50_系统业务运行规则/03_横向治理运行规则/02_校验闸门运行规则.md` discovered as S2 governance basis.
- Current implementation files under `standard_governance/rules/field_rules.py` and `s2_governance_gate/policy.py`.

## Files Modified

- `01_arch_dir/compass/services/api/app/modules/standard_governance/rules/field_rules.py`
- `01_arch_dir/compass/services/api/tests/s2_governance_gate/test_governance.py`
- `01_arch_dir/compass/services/api/tests/standard_governance/test_rules.py`
- `01_arch_dir/compass/apps/h5/src/modules/standard_governance/fieldRules.ts`
- `05_reports/TASK-S2-FIELD-REQUIREDNESS-SYNC-001_report.md`

## Required / Conditional Handling

- Global required fields now keep only `primary_project_id`.
- `primary_subject_id` and `occurred_at` are no longer global blockers for ordinary records.
- Existing conditional rules remain active:
  - `object_asset_name` for construction / waterproof / site-related context.
  - `evidence_refs` and `confirmation_scope` for high-risk or blocking-risk contexts.
  - `source_record_id` for uploaded or external source types.
  - material/supplier-related fields for material and purchase contexts.

## Governance Sync

- S2 normalization now treats collected `project_name` as satisfying `primary_project_id`.
- S2 normalization now treats collected `subject_name` as satisfying `primary_subject_id`.
- This prevents the frontend from collecting usable project/person context while S2 still reports the standard field as missing.

## Tests Updated

- Updated standard governance required-field expectations.
- Updated S2 missing-field expectation for generic records to only require project.
- Added coverage that `project_name` satisfies the required project field and allows ordinary records to proceed to confirmation.

## Boundaries

- L2 rule not modified.
- S2 confirmation/manual review rule not modified.
- manual_confirmation rule not modified.
- `.env` / `data` / `storage` not modified.
- git add/commit/push not run.

## Verification

- `pytest -q`: not run; current AGENTS/custom instructions reserve pytest execution for executor/user.
- `npm run check`: not run; current AGENTS/custom instructions reserve npm verification for executor/user.
- `npm run build`: not run; current AGENTS/custom instructions forbid Codex build execution.

## Risk

Medium. This intentionally reduces blocking for ordinary records. High-risk, source-specific, construction-specific, and material-specific conditional checks remain in place.

## Next Suggested Task

Run executor verification. Then continue to upload entry/file-original handling.
