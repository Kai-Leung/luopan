import type { L3FactListResponse, L3FactViewResponse } from '../facts_view/types';
import { requestJSON } from '../input_flow/api/client';

const L3_BASE = "/api/v1/l3/facts";

export function buildL3FactListPath(params?: {
  fact_type?: string;
  keyword?: string;
  limit?: number;
  offset?: number;
}): string {
  const query = new URLSearchParams();
  if (params?.fact_type) query.set("fact_type", params.fact_type);
  if (params?.keyword) query.set("keyword", params.keyword);
  if (params?.limit !== undefined) query.set("limit", String(params.limit));
  if (params?.offset !== undefined) query.set("offset", String(params.offset));
  const qs = query.toString();
  return qs ? `${L3_BASE}?${qs}` : L3_BASE;
}

export async function listL3Facts(params?: {
  fact_type?: string;
  keyword?: string;
  limit?: number;
  offset?: number;
}): Promise<L3FactListResponse> {
  return requestJSON<L3FactListResponse>(buildL3FactListPath(params), {
    method: "GET",
    errorMessage: "事实列表加载失败",
  });
}

export async function getL3FactDetail(factId: string): Promise<L3FactViewResponse> {
  return requestJSON<L3FactViewResponse>(`${L3_BASE}/${encodeURIComponent(factId)}`, {
    method: "GET",
    errorMessage: "事实加载失败",
  });
}
