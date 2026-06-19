import type { L1CandidateRequest, L1CandidateResponse } from '../types';
import { requestJSON } from './client';

const L1_PATH = "/api/v1/l1/candidates";

export async function createL1Candidate(
  payload: L1CandidateRequest,
): Promise<L1CandidateResponse> {
  return requestJSON<L1CandidateResponse>(L1_PATH, {
    method: "POST",
    body: payload,
    errorMessage: "候选生成失败",
  });
}

export const createCandidate = createL1Candidate;
