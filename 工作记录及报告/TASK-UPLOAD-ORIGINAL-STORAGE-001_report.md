# TASK-UPLOAD-ORIGINAL-STORAGE-001 Report

## Status

Completed with verification deferred to executor/user.

## Files Modified

- `01_arch_dir/compass/services/api/app/modules/upload/api.py`
- `01_arch_dir/compass/services/api/app/modules/upload/schemas.py`
- `01_arch_dir/compass/services/api/app/modules/upload/service.py`
- `01_arch_dir/compass/services/api/app/api/router.py`
- `01_arch_dir/compass/services/api/tests/upload/test_upload_original_storage.py`
- `01_arch_dir/compass/apps/h5/src/modules/upload/api.ts`
- `01_arch_dir/compass/apps/h5/src/modules/upload/index.ts`
- `01_arch_dir/compass/apps/h5/src/modules/upload/types.ts`
- `01_arch_dir/compass/apps/h5/src/pages/H5MainPage.tsx`
- `01_arch_dir/compass/packages/contracts/schemas/upload.schema.json`
- `01_arch_dir/compass/packages/shared-types/index.ts`
- `05_reports/TASK-UPLOAD-ORIGINAL-STORAGE-001_report.md`

## Upload Interface

- `POST /api/v1/upload/files`
- Request: `multipart/form-data`, file field name `file`
- Response fields:
  - `upload_id`
  - `filename`
  - `content_type`
  - `file_size`
  - `storage_path`
  - `saved = true`

## Storage Directory

- Runtime save path: `storage/dev/uploads/`
- The route creates this directory only when an upload request is handled.
- This task did not write upload files into `storage/`.

## Upload Limits

- Allowed extensions: `jpg`, `jpeg`, `png`, `pdf`
- Maximum file size: `10MB`
- Oversize files return HTTP `413`.
- Unsupported file types return HTTP `415`.

## Frontend Handling

- H5 upload sheet keeps separate entries for camera, album, and file.
- Camera is not opened directly from the central input plus button; the choice sheet is shown first.
- After selecting a file, H5 uploads the original file to the backend.
- Success shows a saved-file message and inserts upload id into the central input for business note completion.
- Failure shows an upload failure message and toast.

## Tests Added

- JPG upload succeeds and saved file exists.
- PDF upload succeeds and saved file exists.
- File over 10MB is rejected.
- Unsupported file type is rejected.

## Verification

- `pytest -q`: not run; AGENTS.md forbids Codex from executing pytest.
- `npm run check`: not run; AGENTS.md forbids Codex from executing npm verification.
- `npm run build`: not run; AGENTS.md forbids Codex from executing build.

## Boundaries

- `.env` not modified.
- `data/` not modified.
- Existing `storage/` files not modified.
- L0/L1/L2/L3/L4/L5/L6/L7 not modified.
- S1/S2/S3/standard_governance not modified.
- git add/commit/push not run.

## Risk

Medium. The backend uses a minimal internal multipart parser to avoid adding dependencies; executor verification should confirm multipart compatibility in the local environment.

## Next Suggested Step

Executor/user runs backend and frontend verification, then checks one real upload from H5.
