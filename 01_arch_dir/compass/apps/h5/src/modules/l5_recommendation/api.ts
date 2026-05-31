import { requestJSON } from '../input_flow/api/client';
import type { L5RecommendationDraftRequest, L5RecommendationDraftResponse } from './types';

const L5_RECOMMENDATION_DRAFT_PATH = '/api/v1/l5/recommendations/draft';

export async function createL5RecommendationDraft(
  payload: L5RecommendationDraftRequest,
): Promise<L5RecommendationDraftResponse> {
  return requestJSON<L5RecommendationDraftResponse>(L5_RECOMMENDATION_DRAFT_PATH, {
    method: 'POST',
    body: payload,
    errorMessage: '建议草稿生成失败',
  });
}
