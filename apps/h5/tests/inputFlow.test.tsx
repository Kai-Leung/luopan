import { act, renderHook } from '@testing-library/react';
import { beforeEach, describe, expect, it, vi } from 'vitest';

import {
  checkGovernance,
  createCandidate,
  createPendingConfirmation,
  getL3FactView,
  requestFactCreationAfterConfirmation,
  reviewManualConfirmation,
  sendL0RawInput,
} from '../src/modules/input_flow/api';
import { getActionFromTextIntent, resolveTextInputIntent } from '../src/modules/input_flow/h5Interaction';
import { useInputFlow, useInputFlowState } from '../src/modules/input_flow/useFlow';

vi.mock('../src/modules/input_flow/api', () => ({
  checkGovernance: vi.fn(),
  createCandidate: vi.fn(),
  createPendingConfirmation: vi.fn(),
  getL3FactView: vi.fn(),
  listPendingConfirmations: vi.fn().mockResolvedValue({ items: [] }),
  requestFactCreationAfterConfirmation: vi.fn(),
  reviewManualConfirmation: vi.fn(),
  sendL0RawInput: vi.fn(),
}));

const project = { id: 'project_001', displayName: '宝山项目' };
const candidate = {
  candidate_id: 'cand_001',
  input_session_id: 'session_001',
  candidate_status: 'new_candidate',
  candidate_payload: {
    text: '宝山项目完成防水',
    candidate_summary: '完成防水',
    fact_record_type: 'construction_record',
  },
};
const governance = {
  governance_id: 'gov_001',
  candidate_id: candidate.candidate_id,
  input_session_id: candidate.input_session_id,
  governance_status: 'auto_pass',
  missing_fields: [],
  risk_level: 'none',
  question_prompts: [],
  validation_hints: [],
  risk_hints: [],
  required_permission: null,
  next_action: 'need_confirm',
  message: 'ready',
} as const;
const pending = {
  pending_id: 'pending_001',
  input_session_id: candidate.input_session_id,
  raw_input_id: 'raw_001',
  candidate_id: candidate.candidate_id,
  governance_id: governance.governance_id,
  governance_status: governance.governance_status,
  fact_type: 'construction_record',
  fact_payload: candidate.candidate_payload,
  display_text: '完成防水',
  created_at: '2026-06-22T00:00:00Z',
};

function renderInputFlow(overrides: Record<string, unknown> = {}) {
  const appendMessage = vi.fn();
  const showToast = vi.fn();
  const openPending = vi.fn();
  const queryExistingFacts = vi.fn().mockResolvedValue(undefined);
  const openFactAnalysis = vi.fn();
  const promptProjectContext = vi.fn();
  const result = renderHook(() => {
    const inputFlowState = useInputFlowState();
    return useInputFlow({
      inputText: '',
      setInputText: vi.fn(),
      selectedProject: project,
      pendingOpen: false,
      inputFlowState,
      appendMessage,
      showToast,
      openPending,
      queryExistingFacts,
      openFactAnalysis,
      resolveProjectContextForRecord: vi.fn(() => ({ project, isNew: false, shouldApply: false })),
      promptProjectContext,
      applyProjectContext: vi.fn(),
      formatTextWithProjectContext: vi.fn((value: string) => value),
      ...overrides,
    });
  });
  return {
    ...result,
    appendMessage,
    showToast,
    openPending,
    queryExistingFacts,
    openFactAnalysis,
    promptProjectContext,
  };
}

describe('H5 input flow', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    vi.mocked(sendL0RawInput).mockResolvedValue({
      raw_input_id: 'raw_001',
      input_session_id: 'session_001',
      status: 'received_only',
      message: 'received',
    });
    vi.mocked(createCandidate).mockResolvedValue({ ...candidate, candidates: [candidate] });
    vi.mocked(checkGovernance).mockResolvedValue(governance);
    vi.mocked(createPendingConfirmation).mockResolvedValue(pending);
  });

  it('routes record, query, and analysis intents', () => {
    expect(getActionFromTextIntent(resolveTextInputIntent('今天完成防水'))).toBe('录入');
    expect(getActionFromTextIntent(resolveTextInputIntent('查防水记录'))).toBe('查');
    expect(getActionFromTextIntent(resolveTextInputIntent('问这个项目有什么风险'))).toBe('问');
  });

  it('runs L0, L1, S2, then creates pending only for need_confirm', async () => {
    const flow = renderInputFlow();
    await act(() => flow.result.current.submitText('今天完成防水', '录入'));

    expect(sendL0RawInput).toHaveBeenCalledOnce();
    expect(createCandidate).toHaveBeenCalledOnce();
    expect(checkGovernance).toHaveBeenCalledOnce();
    expect(createPendingConfirmation).toHaveBeenCalledOnce();
    expect(flow.result.current.pendingItems).toHaveLength(1);
    expect(flow.openPending).toHaveBeenCalledOnce();
  });

  it('does not create pending or L2 when S2 blocks', async () => {
    vi.mocked(checkGovernance).mockResolvedValue({
      ...governance,
      governance_status: 'blocked',
      next_action: 'blocked',
      risk_level: 'blocking',
    });
    const flow = renderInputFlow();
    await act(() => flow.result.current.submitText('禁止入链', '录入'));

    expect(createPendingConfirmation).not.toHaveBeenCalled();
    expect(requestFactCreationAfterConfirmation).not.toHaveBeenCalled();
  });

  it('asks for project context before calling L0 when no project is selected', async () => {
    const flow = renderInputFlow({
      selectedProject: null,
      resolveProjectContextForRecord: vi.fn(() => null),
    });
    await act(() => flow.result.current.submitText('今天完成防水', '录入'));

    expect(flow.promptProjectContext).toHaveBeenCalledOnce();
    expect(sendL0RawInput).not.toHaveBeenCalled();
  });

  it('keeps query read-only and opens analysis for question action', async () => {
    const flow = renderInputFlow();
    await act(() => flow.result.current.submitText('查防水记录', '查'));
    await act(() => flow.result.current.submitText('问防水风险', '问'));

    expect(flow.queryExistingFacts).toHaveBeenCalledWith('查防水记录');
    expect(flow.openFactAnalysis).toHaveBeenCalledWith('问防水风险');
    expect(sendL0RawInput).not.toHaveBeenCalled();
  });

  it('confirms pending before L2 creation and then reads L3', async () => {
    vi.mocked(reviewManualConfirmation).mockResolvedValue({
      review_id: 'review_001',
      governance_id: governance.governance_id,
      review_status: 'confirmed_candidate',
      policy_decision: 'manual_review_required',
      message: 'reviewed',
    });
    vi.mocked(requestFactCreationAfterConfirmation).mockResolvedValue({
      fact_id: 'fact_001',
      fact_status: 'active_fact',
      fact_payload: pending.fact_payload,
      raw_input_id: pending.raw_input_id,
      candidate_id: pending.candidate_id,
      governance_id: pending.governance_id,
      review_id: 'review_001',
      message: 'created',
    });
    vi.mocked(getL3FactView).mockResolvedValue({
      fact_id: 'fact_001',
      fact_type: pending.fact_type,
      fact_payload: pending.fact_payload,
      fact_status: 'active_fact',
      created_at: '2026-06-22T00:00:00Z',
    });
    const flow = renderInputFlow();
    await act(() => flow.result.current.confirmPendingItem(pending));

    expect(reviewManualConfirmation).toHaveBeenCalledOnce();
    expect(requestFactCreationAfterConfirmation).toHaveBeenCalledOnce();
    expect(getL3FactView).toHaveBeenCalledWith('fact_001');
    expect(vi.mocked(reviewManualConfirmation).mock.invocationCallOrder[0])
      .toBeLessThan(vi.mocked(requestFactCreationAfterConfirmation).mock.invocationCallOrder[0]);
    expect(vi.mocked(requestFactCreationAfterConfirmation).mock.invocationCallOrder[0])
      .toBeLessThan(vi.mocked(getL3FactView).mock.invocationCallOrder[0]);
  });
});
