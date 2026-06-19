import type { L3FactViewResponse } from '../../facts_view/types';
import { requestJSON } from './client';

const L3_FACT_VIEW_PATH = "/api/v1/l3/facts";

export async function getL3FactView(factId: string): Promise<L3FactViewResponse> {
  return requestJSON<L3FactViewResponse>(`${L3_FACT_VIEW_PATH}/${encodeURIComponent(factId)}`, {
    method: "GET",
    errorMessage: "事实读取失败",
  });
}
