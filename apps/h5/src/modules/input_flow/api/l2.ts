import type { SourceOfTruthFactRequest, SourceOfTruthFactResponse } from '../../facts_view/types';
import { requestJSON } from './client';

const L2_FACT_CREATION_REQUEST_PATH = "/api/v1/l2/source-of-truth/facts";

/**
 * 前端只发起“确认后请求入链”。
 * 后端必须重新校验 governance_id、review_id、candidate_id、raw_input_id 和来源链。
 * 前端不得把本函数视为事实裁决能力，也不得自行伪造 fact_created。
 */
export async function requestFactCreationAfterConfirmation(
  payload: SourceOfTruthFactRequest,
): Promise<SourceOfTruthFactResponse> {
  return requestJSON<SourceOfTruthFactResponse>(L2_FACT_CREATION_REQUEST_PATH, {
    method: "POST",
    body: payload,
    errorMessage: "正式事实入链请求失败",
  });
}

// 兼容旧页面调用名；后续任务可逐步迁移到 requestFactCreationAfterConfirmation。
export const createSourceOfTruthFact = requestFactCreationAfterConfirmation;
