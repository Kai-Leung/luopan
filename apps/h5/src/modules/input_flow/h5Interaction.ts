import type { L1CandidateItem, S2GovernanceCheckResponse } from './types';
import { FACT_RECORD_TYPE_DISPLAY } from '../standard_governance/factRecordTypes';
import { FIELD_DISPLAY_RULES } from '../standard_governance/fieldRules';
import { safeGetJSON } from '../../utils/browserSafe';

export const MESSAGE_STORAGE_KEY = 'compass:h5:interactionMessages';

export type InteractionMessageType = 'text' | 'voice' | 'image' | 'file' | 'status';
export type InteractionAction = '录入' | '查' | '问' | '图片' | '文件';
export type TextInputIntent = 'record' | 'query' | 'analysis';
export type InteractionPromptKind = 'time' | 'person' | 'project';
export type InteractionHintAction = '补充时间' | '补充人员' | '补充项目' | '上传图片' | '上传文件' | '继续输入' | '检查完整性' | '标记待补充';

export type InteractionMessage = {
  id: string;
  type: InteractionMessageType;
  action: InteractionAction;
  content: string;
  fileName?: string;
  fileSize?: number;
  dataUrl?: string;
  createdAt: string;
};

export type CandidateGovernanceItem = {
  candidateId: string;
  inputSessionId: string;
  summary: string;
  typeLabel: string;
  prompts: string[];
  riskLevel: string;
  nextAction: 'ask_more' | 'need_confirm' | 'blocked' | 'ready_to_chain';
};

export type InteractionPromptState = {
  kind: InteractionPromptKind;
  title: string;
  placeholder: string;
} | null;

export type InteractionHints = {
  visible: boolean;
  statusItems: string[];
  missing: string[];
  actions: InteractionHintAction[];
};

type StoredMessage = Partial<InteractionMessage> & {
  source?: 'typed' | 'voice' | 'image' | 'file';
};

export function formatFileSize(size?: number): string {
  if (!size || size <= 0) return '大小未知';
  if (size < 1024) return `${size} B`;
  if (size < 1024 * 1024) return `${(size / 1024).toFixed(1)} KB`;
  return `${(size / 1024 / 1024).toFixed(1)} MB`;
}

export function loadStoredMessages(): InteractionMessage[] {
  try {
    const parsed = safeGetJSON<StoredMessage[]>(MESSAGE_STORAGE_KEY);
    if (!Array.isArray(parsed)) return [];
    return parsed
      .map((item, index) => normalizeStoredMessage(item, index))
      .filter((item): item is InteractionMessage => Boolean(item));
  } catch {
    return [];
  }
}

export function buildInteractionHints(): InteractionHints {
  return {
    visible: false,
    statusItems: [],
    missing: [],
    actions: [],
  };
}

export function resolveTextInputIntent(text: string): TextInputIntent {
  const normalized = text.trim();
  if (!normalized) return 'record';
  if (isAnalysisIntent(normalized)) return 'analysis';
  if (isQueryIntent(normalized)) return 'query';
  return 'record';
}

export function getActionFromTextIntent(intent: TextInputIntent): Extract<InteractionAction, '录入' | '查' | '问'> {
  if (intent === 'query') return '查';
  if (intent === 'analysis') return '问';
  return '录入';
}

function isAnalysisIntent(text: string): boolean {
  return /^(问|请问)/.test(text) || /(分析|判断|风险|建议|怎么办|为什么|原因|是否会|会不会|怎么处理)/.test(text);
}

function isQueryIntent(text: string): boolean {
  return /^(查|查询|查一下|看看|看一下|列一下)/.test(text)
    || /(有没有|哪些|统计|明细|最近.*(记录|事项|付款|收款)|.*记录.*明细)/.test(text);
}

export function getCandidateSummary(candidate: L1CandidateItem): string {
  const payload = candidate.candidate_payload;
  if (typeof payload.candidate_summary === 'string' && payload.candidate_summary.trim()) {
    return payload.candidate_summary.trim();
  }
  if (typeof payload.text === 'string' && payload.text.trim()) {
    return payload.text.trim();
  }
  return '候选事项';
}

export function getCandidateTypeLabel(candidate: L1CandidateItem): string {
  const payload = candidate.candidate_payload;
  if (typeof payload.fact_record_type === 'string') {
    return FACT_RECORD_TYPE_DISPLAY[payload.fact_record_type] || FACT_RECORD_TYPE_DISPLAY.other_fact_record;
  }
  return '候选事项';
}

export function formatCandidateGovernanceItem(
  candidate: L1CandidateItem,
  governance: S2GovernanceCheckResponse,
): CandidateGovernanceItem {
  return {
    candidateId: candidate.candidate_id,
    inputSessionId: candidate.input_session_id,
    summary: getCandidateSummary(candidate),
    typeLabel: getCandidateTypeLabel(candidate),
    prompts: Array.isArray(governance.question_prompts) ? governance.question_prompts : [],
    riskLevel: governance.risk_level || 'none',
    nextAction: governance.next_action,
  };
}

export function getCandidateActionLabel(nextAction: CandidateGovernanceItem['nextAction']): string {
  if (nextAction === 'ask_more') return '待补充';
  if (nextAction === 'need_confirm') return '待确认';
  if (nextAction === 'blocked') return '已阻断';
  return '可继续';
}

export function formatGovernanceResult(
  title: string,
  governance: {
    risk_level?: string;
    missing_fields?: string[];
    question_prompts?: string[];
    risk_hints?: string[];
  },
): string {
  const lines = [title];
  if (governance.risk_level) {
    lines.push(`提示级别：${formatRiskLevel(governance.risk_level)}`);
  }
  if (governance.question_prompts && governance.question_prompts.length > 0) {
    lines.push(`建议补充：${governance.question_prompts.slice(0, 2).join('；')}`);
  } else if (governance.missing_fields && governance.missing_fields.length > 0) {
    const displayNames = governance.missing_fields
      .map((fieldName) => FIELD_DISPLAY_RULES[fieldName])
      .filter(Boolean);
    if (displayNames.length > 0) {
      lines.push(`建议补充：${displayNames.slice(0, 2).join('、')}`);
    }
  }
  if (governance.risk_hints && governance.risk_hints.length > 0) {
    lines.push(`提醒：${governance.risk_hints.slice(0, 2).join('、')}`);
  }
  return lines.join('\n');
}

function formatRiskLevel(riskLevel: string): string {
  if (riskLevel === 'none') return '正常';
  if (riskLevel === 'low') return '低';
  if (riskLevel === 'medium') return '中';
  if (riskLevel === 'high') return '高';
  if (riskLevel === 'blocking') return '需要先处理';
  return riskLevel;
}

function normalizeStoredMessage(item: StoredMessage, index: number): InteractionMessage | null {
  const fallbackType = item.source === 'typed' ? 'text' : item.source;
  const type = item.type || fallbackType;
  if (type !== 'text' && type !== 'voice' && type !== 'image' && type !== 'file' && type !== 'status') return null;
  const content = typeof item.content === 'string' ? item.content : '';
  const createdAt = typeof item.createdAt === 'string' ? item.createdAt : new Date().toISOString();
  return {
    id: typeof item.id === 'string' ? item.id : `stored-${index}`,
    type,
    action: item.action || (type === 'image' ? '图片' : type === 'file' ? '文件' : '录入'),
    content,
    fileName: typeof item.fileName === 'string' ? item.fileName : undefined,
    fileSize: typeof item.fileSize === 'number' ? item.fileSize : undefined,
    dataUrl: typeof item.dataUrl === 'string' ? item.dataUrl : undefined,
    createdAt,
  };
}
