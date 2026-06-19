import type { L0RawInputRequest, L0RawInputResponse } from '../types';
import { requestJSON } from './client';

const L0_PATH = "/api/v1/l0/raw-input";

export async function sendL0RawInput(
  payload: L0RawInputRequest,
): Promise<L0RawInputResponse> {
  return requestJSON<L0RawInputResponse>(L0_PATH, {
    method: "POST",
    body: payload,
    errorMessage: "原始输入提交失败",
  });
}
