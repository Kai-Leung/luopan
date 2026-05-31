export type StandardProcessingDirection =
  | 'readonly'
  | 'draft'
  | 'response'
  | 'candidate'
  | 'blocked'
  | 'need_supplement'
  | 'need_confirmation'
  | 'failed';

export interface StandardErrorResult {
  error_code: string;
  message: string;
  processing_direction: StandardProcessingDirection;
}

export interface StandardSourceRef {
  source_stage: string;
  source_id: string;
}

export interface StandardTraceRef {
  trace_ref: string;
  source_fact_id?: string;
  created_at: string;
}

export interface StandardBoundaryNotice {
  processing_direction: StandardProcessingDirection;
  readonly: boolean;
  no_write_l2: boolean;
  message: string;
}
