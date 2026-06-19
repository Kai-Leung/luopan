import type {
  ManualConfirmationReviewRequest,
  ManualConfirmationReviewResponse,
  PendingConfirmationCreateRequest,
  PendingConfirmationItem,
  PendingConfirmationListResponse,
} from '../types';
import { requestJSON } from './client';

const MC_PATH = "/api/v1/manual-confirmation/review";
const MC_PENDING_PATH = "/api/v1/manual-confirmation/pending";

export async function reviewManualConfirmation(
  payload: ManualConfirmationReviewRequest,
): Promise<ManualConfirmationReviewResponse> {
  return requestJSON<ManualConfirmationReviewResponse>(MC_PATH, {
    method: "POST",
    body: payload,
    errorMessage: "人工确认处理失败",
  });
}

export async function createPendingConfirmation(
  payload: PendingConfirmationCreateRequest,
): Promise<PendingConfirmationItem> {
  return requestJSON<PendingConfirmationItem>(MC_PENDING_PATH, {
    method: "POST",
    body: payload,
    errorMessage: "待确认创建失败",
  });
}

export async function listPendingConfirmations(): Promise<PendingConfirmationListResponse> {
  return requestJSON<PendingConfirmationListResponse>(MC_PENDING_PATH, {
    method: "GET",
    errorMessage: "待确认列表加载失败",
  });
}
