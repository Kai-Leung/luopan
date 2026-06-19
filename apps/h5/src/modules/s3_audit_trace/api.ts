import { requestJSON } from '../input_flow/api/client';
import type { S3TraceSummaryRequest, S3TraceSummaryResponse } from './types';

const S3_TRACE_SUMMARY_PATH = '/api/v1/s3/trace/summary';

export async function getS3TraceSummary(
  payload: S3TraceSummaryRequest,
): Promise<S3TraceSummaryResponse> {
  const query = new URLSearchParams();
  if (payload.source_fact_id) query.set('source_fact_id', payload.source_fact_id);
  if (payload.trace_ref) query.set('trace_ref', payload.trace_ref);
  const suffix = query.toString();
  return requestJSON<S3TraceSummaryResponse>(`${S3_TRACE_SUMMARY_PATH}${suffix ? `?${suffix}` : ''}`, {
    method: 'GET',
    errorMessage: '来源追溯摘要加载失败',
  });
}
