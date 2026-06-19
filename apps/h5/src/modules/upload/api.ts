import { buildRequestUrl } from '../input_flow/api/client';
import { buildRuntimeContextHeaders } from '../s1_runtime_context/constants';
import {
  UPLOAD_ALLOWED_DESCRIPTION,
  UPLOAD_ALLOWED_EXTENSIONS,
  UPLOAD_ALLOWED_MIME_TYPES,
  UPLOAD_MAX_FILE_SIZE,
} from './constants';
import type { UploadFileStoredResponse } from './types';

const UPLOAD_FILE_PATH = '/api/v1/upload/files';

export async function uploadOriginalFile(file: File): Promise<UploadFileStoredResponse> {
  const validationMessage = validateUploadFile(file);
  if (validationMessage) {
    throw new Error(validationMessage);
  }

  const formData = new FormData();
  formData.append('file', file);

  let response: Response;
  try {
    response = await fetch(buildRequestUrl(UPLOAD_FILE_PATH), {
      method: 'POST',
      headers: buildRuntimeContextHeaders(),
      body: formData,
    });
  } catch {
    throw new Error('上传服务暂时连不上，请确认后端服务已启动。');
  }

  if (!response.ok) {
    throw new Error(await readSafeUploadError(response));
  }

  return response.json();
}

function validateUploadFile(file: File): string | null {
  if (file.size <= 0) {
    return '这个文件是空的，不能上传。';
  }
  if (file.size > UPLOAD_MAX_FILE_SIZE) {
    return '文件超过 10MB，请换一个小一点的文件。';
  }
  const extension = getFileExtension(file.name);
  if (!extension && !isAllowedMimeType(file.type)) {
    return UPLOAD_ALLOWED_DESCRIPTION;
  }
  return null;
}

function getFileExtension(filename: string): typeof UPLOAD_ALLOWED_EXTENSIONS[number] | '' {
  const extension = filename.split('.').pop()?.trim().toLowerCase() || '';
  if ((UPLOAD_ALLOWED_EXTENSIONS as readonly string[]).includes(extension)) {
    return extension as typeof UPLOAD_ALLOWED_EXTENSIONS[number];
  }
  return '';
}

function isAllowedMimeType(contentType: string): boolean {
  return (UPLOAD_ALLOWED_MIME_TYPES as readonly string[]).includes(contentType.trim().toLowerCase());
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
  if (response.status === 404) {
    return '上传接口没找到，请确认后端已更新并启动。';
  }
  if (response.status === 413) {
    return '文件超过 10MB，请换一个小一点的文件。';
  }
  if (response.status === 415) {
    return UPLOAD_ALLOWED_DESCRIPTION;
  }
  return `上传失败（HTTP ${response.status}）`;
}
