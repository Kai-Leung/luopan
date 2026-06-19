import { useCallback, useEffect, useState } from 'react';
import type { Dispatch, SetStateAction } from 'react';
import type { H5ProjectContext } from '../s1_runtime_context/types';
import { SourceType } from '../standard_governance/enums';
import {
  checkGovernance,
  createCandidate,
  createPendingConfirmation,
  getL3FactView,
  listPendingConfirmations,
  requestFactCreationAfterConfirmation,
  reviewManualConfirmation,
  sendL0RawInput,
} from './api';
import {
  formatCandidateGovernanceItem,
  formatGovernanceResult,
  getActionFromTextIntent,
  getCandidateSummary,
  resolveTextInputIntent,
} from './h5Interaction';
import type {
  CandidateGovernanceItem,
  InteractionAction,
  InteractionMessage,
} from './h5Interaction';
import type {
  L1CandidateItem,
  PendingConfirmationItem,
  S2GovernanceCheckResponse,
} from './types';

type AppendMessage = (message: Omit<InteractionMessage, 'id' | 'createdAt'>) => void;
type ProjectResolution = {
  project: H5ProjectContext;
  isNew: boolean;
  shouldApply: boolean;
} | null;

export type InputFlowState = {
  pendingItems: PendingConfirmationItem[];
  setPendingItems: Dispatch<SetStateAction<PendingConfirmationItem[]>>;
  candidateItems: CandidateGovernanceItem[];
  setCandidateItems: Dispatch<SetStateAction<CandidateGovernanceItem[]>>;
  handledPendingIds: string[];
  setHandledPendingIds: Dispatch<SetStateAction<string[]>>;
  resetInputFlowState: () => void;
};

export function useInputFlowState(): InputFlowState {
  const [pendingItems, setPendingItems] = useState<PendingConfirmationItem[]>([]);
  const [candidateItems, setCandidateItems] = useState<CandidateGovernanceItem[]>([]);
  const [handledPendingIds, setHandledPendingIds] = useState<string[]>([]);

  const resetInputFlowState = useCallback(() => {
    setPendingItems([]);
    setCandidateItems([]);
    setHandledPendingIds([]);
  }, []);

  return {
    pendingItems,
    setPendingItems,
    candidateItems,
    setCandidateItems,
    handledPendingIds,
    setHandledPendingIds,
    resetInputFlowState,
  };
}

type UseInputFlowOptions = {
  inputText: string;
  setInputText: Dispatch<SetStateAction<string>>;
  selectedProject: H5ProjectContext | null;
  pendingOpen: boolean;
  inputFlowState: InputFlowState;
  appendMessage: AppendMessage;
  showToast: (message: string) => void;
  openPending: () => void;
  queryExistingFacts: (keyword: string) => Promise<void>;
  openFactAnalysis: (keyword: string) => void;
  resolveProjectContextForRecord: (value: string) => ProjectResolution;
  promptProjectContext: (
    recordText: string,
    submitProjectRecord: (recordText: string, project: H5ProjectContext) => void,
  ) => void;
  applyProjectContext: (project: H5ProjectContext, isNew: boolean) => void;
  formatTextWithProjectContext: (value: string, project: H5ProjectContext | null) => string;
};

export function useInputFlow({
  inputText,
  setInputText,
  selectedProject,
  pendingOpen,
  inputFlowState,
  appendMessage,
  showToast,
  openPending,
  queryExistingFacts,
  openFactAnalysis,
  resolveProjectContextForRecord,
  promptProjectContext,
  applyProjectContext,
  formatTextWithProjectContext,
}: UseInputFlowOptions) {
  const {
    pendingItems,
    setPendingItems,
    candidateItems,
    setCandidateItems,
    handledPendingIds,
    setHandledPendingIds,
  } = inputFlowState;

  const refreshPendingConfirmations = useCallback(async () => {
    try {
      const response = await listPendingConfirmations();
      setPendingItems(response.items.filter((item) => !handledPendingIds.includes(item.pending_id)));
    } catch {
      showToast('待确认列表加载失败');
    }
  }, [handledPendingIds, setPendingItems, showToast]);

  useEffect(() => {
    if (pendingOpen) void refreshPendingConfirmations();
  }, [pendingOpen, refreshPendingConfirmations]);

  async function submitInput(action: InteractionAction = '录入') {
    const value = inputText.trim();
    if (!value) {
      showToast('请输入内容。');
      return;
    }
    setInputText('');
    const resolvedAction = action === '录入'
      ? getActionFromTextIntent(resolveTextInputIntent(value))
      : action;
    await submitText(value, resolvedAction);
  }

  async function submitText(
    value: string,
    action: InteractionAction = '录入',
    options: { skipProjectContextCheck?: boolean; projectContext?: H5ProjectContext | null } = {},
  ) {
    appendMessage({ type: 'text', action, content: value });
    if (action === '查') {
      await queryExistingFacts(value);
      return;
    }
    if (action === '问') {
      openFactAnalysis(value);
      return;
    }
    if (action !== '录入') {
      const message = `${action}暂时还不能处理，请先用文字记录或查询已有记录。`;
      appendMessage({ type: 'status', action, content: message });
      showToast(message);
      return;
    }

    let projectContext = options.projectContext ?? selectedProject;
    if (!options.skipProjectContextCheck && !options.projectContext) {
      const resolution = resolveProjectContextForRecord(value);
      if (!resolution) {
        promptProjectContext(value, (recordText, project) => {
          void submitText(recordText, '录入', { skipProjectContextCheck: true, projectContext: project });
        });
        return;
      }
      projectContext = resolution.project;
      if (resolution.shouldApply) {
        applyProjectContext(resolution.project, resolution.isNew);
      }
    }
    if (!projectContext) {
      promptProjectContext(value, (recordText, project) => {
        void submitText(recordText, '录入', { skipProjectContextCheck: true, projectContext: project });
      });
      return;
    }

    try {
      const valueWithProject = formatTextWithProjectContext(value, projectContext);
      const rawInput = await sendL0RawInput({
        text: valueWithProject,
        idempotency_key: `h5_${Date.now()}_${Math.random().toString(36).slice(2, 10)}`,
        source_type: SourceType.MANUAL_INPUT,
      });
      const candidate = await createCandidate({
        raw_input_id: rawInput.raw_input_id,
        input_session_id: rawInput.input_session_id,
        raw_payload: { text: valueWithProject, project_name: projectContext.displayName },
        source_type: SourceType.MANUAL_INPUT,
      });
      const candidates = candidate.candidates?.length > 0 ? candidate.candidates : [candidate];
      if (candidates.length > 1) {
        appendMessage({
          type: 'status',
          action: '录入',
          content: `我看出这里有 ${candidates.length} 件事，会分开整理，方便你逐条确认。`,
        });
      }
      await runGovernanceForCandidates(candidates, rawInput.raw_input_id);
    } catch {
      showToast('提交失败，请稍后再试。');
    }
  }

  async function runGovernanceForCandidates(candidates: L1CandidateItem[], rawInputId: string) {
    const nextCandidateItems: CandidateGovernanceItem[] = [];
    const statusLines: string[] = [];
    const pendingResults: PendingConfirmationItem[] = [];
    for (const item of candidates) {
      const governance = await checkGovernance({
        candidate_id: item.candidate_id,
        input_session_id: item.input_session_id,
        candidate_status: item.candidate_status,
        candidate_payload: item.candidate_payload,
      });
      nextCandidateItems.push(formatCandidateGovernanceItem(item, governance));
      const pendingItem = await maybeCreatePendingConfirmation(item, governance, rawInputId);
      if (pendingItem) pendingResults.push(pendingItem);
      statusLines.push(formatStatusLine(governance, Boolean(pendingItem)));
    }
    setCandidateItems(nextCandidateItems);
    if (pendingResults.length > 0) {
      setPendingItems((previous) => [
        ...pendingResults,
        ...previous.filter((item) => !pendingResults.some((pending) => pending.pending_id === item.pending_id)),
      ]);
      openPending();
    }
    appendMessage({ type: 'status', action: '录入', content: statusLines.join('\n\n') });
  }

  async function maybeCreatePendingConfirmation(
    item: L1CandidateItem,
    governance: S2GovernanceCheckResponse,
    rawInputId: string,
  ) {
    if (governance.next_action !== 'need_confirm') return null;
    const factRecordType = getCandidateFactRecordType(item);
    if (!factRecordType) {
      showToast('这条内容还没看出类型，请补充一句说明。');
      return null;
    }
    return createPendingConfirmation({
      raw_input_id: rawInputId,
      input_session_id: item.input_session_id,
      candidate_id: item.candidate_id,
      governance_id: governance.governance_id,
      governance_status: governance.governance_status,
      fact_type: factRecordType,
      fact_payload: item.candidate_payload,
      display_text: getCandidateSummary(item),
    });
  }

  async function confirmPendingItem(item: PendingConfirmationItem) {
    try {
      const review = await reviewManualConfirmation({
        governance_id: item.governance_id,
        governance_status: item.governance_status,
        review_action: 'confirm',
        pending_id: item.pending_id,
      });
      const fact = await requestFactCreationAfterConfirmation({
        raw_input_id: item.raw_input_id,
        candidate_id: item.candidate_id,
        governance_id: item.governance_id,
        review_id: review.review_id,
        review_status: review.review_status,
        fact_type: item.fact_type,
        fact_payload: item.fact_payload,
      });
      const factView = await getL3FactView(fact.fact_id);
      const factText = typeof factView.fact_payload.text === 'string'
        ? factView.fact_payload.text
        : item.display_text;
      setHandledPendingIds((previous) => [...previous, item.pending_id]);
      setPendingItems((previous) => previous.filter((pending) => pending.pending_id !== item.pending_id));
      appendMessage({ type: 'status', action: '录入', content: `已确认并保存。\n${factText}` });
      showToast('已保存，可以在查询里看到。');
    } catch (error) {
      showToast(error instanceof Error && error.message.trim() ? error.message.trim() : '待确认处理失败');
    }
  }

  return {
    pendingItems,
    candidateItems,
    handledPendingIds,
    submitInput,
    submitText,
    confirmPendingItem,
    refreshPendingConfirmations,
  };
}

function getCandidateFactRecordType(item: L1CandidateItem): string | null {
  const factRecordType = item.candidate_payload.fact_record_type;
  return typeof factRecordType === 'string' && factRecordType.trim() ? factRecordType.trim() : null;
}

function formatStatusLine(governance: S2GovernanceCheckResponse, pendingCreated: boolean) {
  if (governance.next_action === 'blocked') {
    return formatGovernanceResult('这条内容暂时不能保存，请先处理下面的提醒。', governance);
  }
  if (governance.next_action === 'ask_more') {
    return formatGovernanceResult('还差一点关键信息，补上后我再帮你整理。', governance);
  }
  if (governance.next_action === 'ready_to_chain') {
    return formatGovernanceResult('内容已经基本清楚，请确认后保存。', governance);
  }
  if (!pendingCreated) {
    return formatGovernanceResult('这条内容还没看出是什么类型，请再补一句说明。', governance);
  }
  return formatGovernanceResult('我整理好了，确认后再保存为正式记录。', governance);
}
