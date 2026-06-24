import { beforeEach, describe, expect, it, vi } from 'vitest';

import { fetchFacts, fetchPendingConfirmations, fetchRuntimeContext, reviewPending } from '../src/api';

const pending = {
  pending_id: 'pending_001',
  input_session_id: 'session_001',
  raw_input_id: 'raw_001',
  candidate_id: 'cand_001',
  governance_id: 'gov_001',
  governance_status: 'auto_pass' as const,
  fact_type: 'construction_record',
  fact_payload: { text: '完成防水' },
  display_text: '完成防水',
  created_at: '2026-06-22T00:00:00Z',
};

describe('PC API flow', () => {
  beforeEach(() => {
    vi.restoreAllMocks();
  });

  it('loads runtime context, pending items, and facts', async () => {
    const fetchMock = vi.spyOn(globalThis, 'fetch')
      .mockResolvedValueOnce(new Response(JSON.stringify({ context_id: 'ctx' }), { status: 200 }))
      .mockResolvedValueOnce(new Response(JSON.stringify({ items: [pending] }), { status: 200 }))
      .mockResolvedValueOnce(new Response(JSON.stringify({ items: [], total: 0 }), { status: 200 }));

    await expect(fetchRuntimeContext()).resolves.toMatchObject({ context_id: 'ctx' });
    await expect(fetchPendingConfirmations()).resolves.toEqual([pending]);
    await expect(fetchFacts()).resolves.toEqual({ items: [], total: 0 });
    expect(fetchMock).toHaveBeenCalledTimes(3);
  });

  it('creates L2 only after a confirmed review', async () => {
    const fetchMock = vi.spyOn(globalThis, 'fetch')
      .mockResolvedValueOnce(new Response(JSON.stringify({
        review_id: 'review_001',
        governance_id: pending.governance_id,
        review_status: 'confirmed_candidate',
      }), { status: 200 }))
      .mockResolvedValueOnce(new Response(JSON.stringify({ fact_id: 'fact_001' }), { status: 200 }));

    await reviewPending(pending, 'confirm', 'user_001');

    expect(fetchMock).toHaveBeenCalledTimes(2);
    expect(fetchMock.mock.calls[0][0]).toBe('/api/v1/manual-confirmation/review');
    expect(fetchMock.mock.calls[1][0]).toBe('/api/v1/l2/source-of-truth/facts');
  });

  it.each(['return_for_completion', 'reject'] as const)('%s does not create L2', async (action) => {
    const fetchMock = vi.spyOn(globalThis, 'fetch').mockResolvedValue(
      new Response(JSON.stringify({
        review_id: 'review_001',
        governance_id: pending.governance_id,
        review_status: action === 'reject' ? 'rejected_candidate' : 'returned_for_completion',
      }), { status: 200 }),
    );

    await reviewPending(pending, action, 'user_001');

    expect(fetchMock).toHaveBeenCalledOnce();
    expect(fetchMock.mock.calls[0][0]).toBe('/api/v1/manual-confirmation/review');
  });

  it('surfaces backend API errors', async () => {
    vi.spyOn(globalThis, 'fetch').mockResolvedValue(
      new Response(JSON.stringify({ detail: '待确认加载失败' }), { status: 500 }),
    );

    await expect(fetchPendingConfirmations()).rejects.toThrow('待确认加载失败');
  });
});
