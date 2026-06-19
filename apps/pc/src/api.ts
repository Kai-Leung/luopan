export type RuntimeContext = {
  context_id: string;
  user_id: string;
  user_display_name: string;
  organization_id: string;
  organization_name: string;
  role_names: string[];
  allowed_actions: string[];
  context_source: 'controlled_claim' | 'development_baseline';
};

export type GovernanceStatus =
  | 'auto_pass'
  | 'needs_completion'
  | 'needs_confirmation'
  | 'blocked';

export type PendingConfirmation = {
  pending_id: string;
  input_session_id: string;
  raw_input_id: string;
  candidate_id: string;
  governance_id: string;
  governance_status: GovernanceStatus;
  fact_type: string;
  fact_payload: Record<string, unknown>;
  display_text: string;
  required_permission?: string;
  created_at: string;
};

export type FactListItem = {
  fact_id: string;
  fact_type: string;
  fact_payload_summary: string;
  source_type: string;
  fact_status: 'active_fact';
  created_at: string;
};

export type FactList = {
  items: FactListItem[];
  total: number;
};

type ReviewAction = 'confirm' | 'return_for_completion' | 'reject';

type ReviewResponse = {
  review_id: string;
  governance_id: string;
  review_status:
    | 'confirmed_candidate'
    | 'returned_for_completion'
    | 'rejected_candidate';
};

const RUNTIME_HEADERS = {
  'X-Compass-User-Id': 'user_compass_owner',
  'X-Compass-Organization-Id': 'org_compass_default',
  'X-Compass-Role': 'owner',
};

function apiUrl(path: string): string {
  const base = (import.meta.env.VITE_API_BASE || '').trim().replace(/\/+$/, '');
  return base ? `${base}${path}` : path;
}

async function requestJson<T>(
  path: string,
  options: { method?: 'GET' | 'POST'; body?: unknown } = {},
): Promise<T> {
  const headers: Record<string, string> = { ...RUNTIME_HEADERS };
  if (options.body !== undefined) {
    headers['Content-Type'] = 'application/json';
  }
  const response = await fetch(apiUrl(path), {
    method: options.method ?? 'GET',
    headers,
    ...(options.body !== undefined
      ? { body: JSON.stringify(options.body) }
      : {}),
  });
  if (!response.ok) {
    throw new Error(await readError(response));
  }
  return response.json() as Promise<T>;
}

async function readError(response: Response): Promise<string> {
  try {
    const body = await response.json() as { detail?: unknown };
    if (typeof body.detail === 'string') {
      return body.detail;
    }
  } catch {
    // The status code remains the stable fallback for non-JSON failures.
  }
  return `请求失败（HTTP ${response.status}）`;
}

export function fetchRuntimeContext(): Promise<RuntimeContext> {
  return requestJson('/api/v1/s1/runtime-context/current');
}

export async function fetchPendingConfirmations(): Promise<PendingConfirmation[]> {
  const response = await requestJson<{ items: PendingConfirmation[] }>(
    '/api/v1/manual-confirmation/pending',
  );
  return response.items;
}

export function fetchFacts(keyword = ''): Promise<FactList> {
  const query = keyword.trim()
    ? `?keyword=${encodeURIComponent(keyword.trim())}`
    : '';
  return requestJson(`/api/v1/l3/facts${query}`);
}

export async function reviewPending(
  item: PendingConfirmation,
  action: ReviewAction,
  confirmedBy: string,
): Promise<void> {
  const review = await requestJson<ReviewResponse>(
    '/api/v1/manual-confirmation/review',
    {
      method: 'POST',
      body: {
        pending_id: item.pending_id,
        governance_id: item.governance_id,
        governance_status: item.governance_status,
        review_action: action,
        required_permission: item.required_permission,
        confirmed_by: confirmedBy,
      },
    },
  );

  if (review.review_status !== 'confirmed_candidate') {
    return;
  }

  await requestJson('/api/v1/l2/source-of-truth/facts', {
    method: 'POST',
    body: {
      raw_input_id: item.raw_input_id,
      candidate_id: item.candidate_id,
      governance_id: item.governance_id,
      review_id: review.review_id,
      review_status: review.review_status,
      fact_type: item.fact_type,
      fact_payload: item.fact_payload,
    },
  });
}
