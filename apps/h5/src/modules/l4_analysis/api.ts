import { requestJSON } from '../input_flow/api/client';
import type { L4AnalysisPreviewResponse } from './types';

const L4_ANALYSIS_PREVIEW_PATH = '/api/v1/l4/analysis/preview';

export async function getL4AnalysisPreview(factId: string): Promise<L4AnalysisPreviewResponse> {
  const query = new URLSearchParams({ fact_id: factId });
  return requestJSON<L4AnalysisPreviewResponse>(`${L4_ANALYSIS_PREVIEW_PATH}?${query.toString()}`, {
    method: 'GET',
    errorMessage: '分析预览加载失败',
  });
}
