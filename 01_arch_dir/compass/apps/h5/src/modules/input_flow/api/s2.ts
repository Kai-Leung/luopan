import type { S2GovernanceCheckRequest, S2GovernanceCheckResponse } from '../types';
import { requestJSON } from './client';

const S2_PATH = "/api/v1/s2/governance/check";

export async function checkS2Governance(
  payload: S2GovernanceCheckRequest,
): Promise<S2GovernanceCheckResponse> {
  return requestJSON<S2GovernanceCheckResponse>(S2_PATH, {
    method: "POST",
    body: payload,
    errorMessage: "治理校验失败",
  });
}

export const checkGovernance = checkS2Governance;
