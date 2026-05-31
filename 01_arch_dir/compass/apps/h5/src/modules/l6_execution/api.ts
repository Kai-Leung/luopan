import { requestJSON } from '../input_flow/api/client';
import type { L6ExecutionResponseRequest, L6ExecutionResponseResponse } from './types';

const L6_EXECUTION_RESPONSES_PATH = '/api/v1/l6/execution-responses';

export async function createL6ExecutionResponse(
  payload: L6ExecutionResponseRequest,
): Promise<L6ExecutionResponseResponse> {
  return requestJSON<L6ExecutionResponseResponse>(L6_EXECUTION_RESPONSES_PATH, {
    method: 'POST',
    body: payload,
    errorMessage: '执行响应记录失败',
  });
}
