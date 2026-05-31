import { buildRequestUrl } from '../input_flow/api/client';
import type { UploadFileStoredResponse } from './types';

const UPLOAD_FILE_PATH = '/api/v1/upload/files';

export async function uploadOriginalFile(file: File): Promise<UploadFileStoredResponse> {
  const formData = new FormData();
  formData.append('file', file);

  const response = await fetch(buildRequestUrl(UPLOAD_FILE_PATH), {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    throw new Error(await readSafeUploadError(response));
  }

  return response.json();
}

async function readSafeUploadError(response: Response): Promise<string> {
  try {
    const body = await response.json() as { detail?: unknown };
    if (typeof body.detail === 'string' && body.detail.trim()) {
      return body.detail.trim();
    }
  } catch {
    // ignore non-JSON response bodies
  }
  return `上传失败（HTTP ${response.status}）`;
}
