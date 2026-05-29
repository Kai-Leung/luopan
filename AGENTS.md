# AGENTS.md

## 0. Code root rule

Actual code workspace root:

```text
01_arch_dir/compass
```

All task-card paths such as `apps/`, `services/`, `packages/`, `docs/`, `tests/`, `scripts/`, and `ops/` are relative to this code root unless the task card explicitly refers to package-level folders such as `03_control/`, `04_task_cards/`, or `05_reports/`.

Do not edit compressed archives. `01_arch_dir/` must contain extracted directories, not zip files.

---

## 1. Role and scope

This repository is the Compass / 罗盘系统 development workspace.

Codex must work as a controlled coding assistant, not as a free developer.

Codex must only execute the current task card. Do not infer or implement unrelated features.

---

## 2. Required reading order

Before making changes, read these files in order:

1. `03_control/02_任务卡索引与读取规则.md`
2. The current task card in `04_task_cards/task_cards/`
3. `03_control/01_开发依据与目录映射总表.md`
4. `03_control/03_技术选型摘要.md` and `03_control/04_环境基线摘要.md` when the task involves environment, build, tests, or baseline checks
5. The development-basis files explicitly named by the current task card
5. Only the code directories allowed by the current task card

If a file or directory is missing, stop and report the missing item. Do not guess.

---

## 3. Task-card rule

Every change must be tied to one task card.

A task card must define:

- task id
- task objective
- required basis
- allowed paths
- forbidden paths
- technical constraints
- acceptance focus
- report requirements

If the requested change is not covered by the current task card, stop and report:

`NEEDS_NEW_TASK_CARD`

---

## 4. Repository layout

Expected ARCH_DIR version: `ARCH_DIR_v0.1.0`.

Main paths:

- `apps/h5/` — H5 main interaction app
- `apps/pc/` — PC management app, currently reserved unless a task card allows it
- `apps/mobile-shell/` — Android / iOS shell, currently reserved unless a task card allows it
- `services/api/` — FastAPI backend service
- `packages/contracts/` — OpenAPI and JSON Schema contracts
- `packages/shared-types/` — shared types and enums
- `packages/shared-utils/` — shared non-business utilities
- `packages/native-bridge/` — H5/native bridge protocol
- `docs/architecture/` — architecture and module mapping
- `docs/development/` or `03_control/` — development control files
- `docs/acceptance/` — acceptance rules
- `tests/` — E2E, integration, acceptance tests
- `scripts/check/` — boundary and safety checks
- `scripts/build/` — build scripts
- `scripts/test/` — test scripts
- `data/` — local data placeholder only
- `storage/` — local file-storage placeholder only
- `05_reports/` — task execution reports

---

## 5. Development-basis mapping rule

Do not implement a feature just because a directory exists.

Before editing any directory, confirm that the directory is mapped in:

`03_control/01_开发依据与目录映射总表.md`

If a feature is not supported by the mapping table and the task card, do not implement it.

---

## 6. Architecture rules

The system follows these controlled chains:

- S1 / `pre_run_context`: identity, organization, role, project scope, access scope
- L0 / `l0_input`: raw input
- L1 / `l1_candidate`: candidate content
- S2 / `s2_validation`, `supplement`, `confirmation`: governance gate, supplement, confirmation, blocking
- L2 / `l2_fact`: official fact source of truth
- L3 / `l3_query_view`: query and view, read-only from L2
- L4 / `l4_analysis`: analysis
- L5 / `l5_recommendation`: recommendation
- L6 / `l6_execution`: execution
- L7 / `l7_feedback`: feedback
- S3 / current `governance/trace_minimal`: minimal source trace and audit, reserved for later strengthening

Do not bypass this chain.

---

## 7. Source-of-truth rules

L2 is the only official fact entry point.

The following must not directly create or overwrite official facts:

- frontend pages
- AI output
- upload results
- external collaboration input
- query results
- analysis results
- recommendations
- execution receipts
- feedback records
- storage files
- raw inputs
- candidates

L3/L4/L5/L6/L7 must not write back to L2 unless a task card explicitly defines a governed path through S2/L2.

---

## 8. Frontend rules

Frontend code may:

- collect input
- call backend APIs
- show candidate content
- show S2 status
- show supplement and confirmation prompts
- show official facts returned by backend
- show query results
- show source summaries
- show permission and blocking messages

Frontend code must not:

- decide final permission
- decide S2 validation
- create official facts
- fake `fact_created`
- hide `blocked`, `need_supplement`, or `need_confirmation`
- treat HTTP 200 as business success
- access database or storage directly

---

## 9. Backend rules

Backend modules must follow the mapped module responsibility.

Do not create generic modules such as:

- `crm`
- `erp`
- `workflow_engine`
- `auth-center`
- `file-center`
- `flow-engine`
- `message-center`
- `webhook`
- `worker`

unless the current task card explicitly requires them and cites supporting development basis.

For `ARCH_DIR_v0.1.0`, external callbacks and external collaboration belong under:

`services/api/app/modules/external_collaboration/`

unless a later task card changes the architecture.

---

## 10. Contracts rule

Contracts must stay aligned with backend schemas and frontend types.

Use:

- `packages/contracts/openapi/`
- `packages/contracts/schemas/`
- `packages/shared-types/`

Do not create request or response fields only in frontend or only in backend when a contract should exist.

Do not use `any` or unstructured payloads to avoid the contract.

---

## 11. Technology constraints

Use the existing project stack only:

- frontend: TypeScript + React + Vite
- backend: Python + FastAPI
- current database: SQLite
- ORM / database access: SQLAlchemy if already used or required by task card
- tests: pytest for backend; existing frontend test tool if present
- scripts: shell or Python only when appropriate

Do not introduce new frameworks, languages, package managers, database engines, queues, or runtimes unless the current task card explicitly requires them.

Do not use `latest` dependency versions.

Do not delete lock files to avoid dependency conflicts.

---

## 12. Protected paths

Never modify or create real content in:

- `.env`
- `.env.*`
- `data/dev/`
- `data/test/`
- `storage/dev/`
- `storage/test/`
- real database files
- real Raw Store files
- real uploaded files
- logs containing secrets or customer data

Only `.gitkeep` placeholder files are allowed in `data/` and `storage/`.

Never expose or write API keys, tokens, secrets, database passwords, customer data, or production environment values.

---

## 13. Git rule

Do not run:

- `git add`
- `git commit`
- `git push`

unless the current task card or user explicitly authorizes it.

You may inspect Git state with read-only commands.

---

## 14. Test and verification rule

Run the tests or checks requested by the task card.

If the required test command is unknown, inspect the repo for existing scripts and report what you found.

If tests cannot be run, report:

- command attempted
- reason it failed or was not run
- affected risk

Do not claim success without evidence.

---

## 15. Report rule

After each task, write or return a task report with:

- task id
- execution status
- files read
- files modified
- files added
- files deleted
- contracts changed
- data models changed
- tests/checks run
- test results
- tests not run and reason
- whether `.env` was modified
- whether `data/` was modified
- whether `storage/` was modified
- whether git add/commit/push was run
- risks
- blockers

If the repo has `05_reports/`, write the report there using:

`05_reports/<TASK_ID>_report.md`

---

## 16. Stop conditions

Stop and report instead of continuing if:

- the task card is missing
- the mapping table is missing
- the required development-basis file is missing
- the requested change is outside allowed paths
- the task requires editing forbidden paths
- the task requires changing `.env`
- the task requires real database or real storage operations
- the task requires bypassing S2 or directly writing L2
- the task requires a new unapproved module
- the task conflicts with the technology baseline
- the task is too broad for one execution

Use one of these markers:

- `NEEDS_TASK_CARD`
- `NEEDS_BASIS`
- `NEEDS_USER_DECISION`
- `OUT_OF_SCOPE`
- `BLOCKED_BY_FORBIDDEN_PATH`
- `TASK_TOO_LARGE`

---

## 17. Default execution style

Be conservative.

Prefer small, reviewable changes.

Preserve existing working code.

Do not rewrite large areas unless the task card explicitly requests it.

Do not remove files unless the task card explicitly requests it.

Do not invent product scope.

Do not turn Compass into a generic CRM, ERP, workflow platform, AI tool, document system, or project-management platform.
