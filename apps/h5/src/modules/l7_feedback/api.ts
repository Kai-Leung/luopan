import { requestJSON } from '../input_flow/api/client';
import type { L7FeedbackRequest, L7FeedbackResponse } from './types';

const L7_FEEDBACK_PATH = '/api/v1/l7/feedback';

export async function createL7FeedbackCandidate(
  payload: L7FeedbackRequest,
): Promise<L7FeedbackResponse> {
  return requestJSON<L7FeedbackResponse>(L7_FEEDBACK_PATH, {
    method: 'POST',
    body: payload,
    errorMessage: '反馈候选提交失败',
  });
}
