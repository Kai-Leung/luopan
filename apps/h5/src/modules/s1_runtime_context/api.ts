import { requestJSON } from '../input_flow/api/client';
import type { RuntimeContextResponse } from './types';

const CURRENT_CONTEXT_PATH = '/api/v1/s1/runtime-context/current';

export async function fetchRuntimeContext(): Promise<RuntimeContextResponse> {
  return requestJSON<RuntimeContextResponse>(CURRENT_CONTEXT_PATH, {
    method: 'GET',
    errorMessage: '运行上下文加载失败',
  });
}
