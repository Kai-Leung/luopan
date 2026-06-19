import { useCallback, useState } from 'react';
import type { L3FactListItem } from '../facts_view/types';
import type { InteractionMessage } from '../input_flow/h5Interaction';
import { listL3Facts } from './api';

type AppendMessage = (message: Omit<InteractionMessage, 'id' | 'createdAt'>) => void;

type UseL3QueryViewFlowOptions = {
  appendMessage: AppendMessage;
  showToast: (message: string) => void;
  openFactQueryPanel: () => void;
  closeFactQueryPanel: () => void;
};

export function useL3QueryViewFlow({
  appendMessage,
  showToast,
  openFactQueryPanel,
  closeFactQueryPanel,
}: UseL3QueryViewFlowOptions) {
  const [factQueryKeyword, setFactQueryKeyword] = useState('');

  const queryExistingFacts = useCallback(async (keyword: string) => {
    const normalizedKeyword = keyword.trim();
    if (!normalizedKeyword) {
      appendMessage({ type: 'status', action: '查', content: '想查什么内容？可以直接输入项目、事项或关键词。' });
      return;
    }
    try {
      const response = await listL3Facts({
        keyword: normalizedKeyword,
        limit: 5,
        offset: 0,
      });
      appendMessage({
        type: 'status',
        action: '查',
        content: formatReadonlyFactQueryMessage(normalizedKeyword, response.items, response.total),
      });
      showToast(response.items.length > 0 ? '查到了已有记录。' : '没有查到相关记录。');
    } catch (error) {
      appendMessage({
        type: 'status',
        action: '查',
        content: `这次没有查成功。\n查询内容：${normalizedKeyword}\n只是查询已有记录，不会新增或修改任何内容。`,
      });
      showToast(error instanceof Error && error.message.trim() ? error.message.trim() : '查询失败，请稍后再试。');
    }
  }, [appendMessage, showToast]);

  const openFactAnalysis = useCallback((keyword: string, voiceSourceLabel?: string) => {
    const normalizedKeyword = keyword.trim();
    if (!normalizedKeyword) {
      appendMessage({ type: 'status', action: '问', content: '想分析什么？可以直接输入项目、事项或关键词。' });
      return;
    }
    setFactQueryKeyword(normalizedKeyword);
    openFactQueryPanel();
    appendMessage({
      type: 'status',
      action: '问',
      content: [
        voiceSourceLabel ? `已识别语音：${voiceSourceLabel}` : '',
        `我会先从已有正式事实中查找「${normalizedKeyword}」，并加载匹配记录的分析预览。`,
        '分析预览不产生正式事实；后续建议、执行响应和反馈仍需在详情中人工触发。',
      ].filter(Boolean).join('\n'),
    });
    showToast('正在查找相关事实并加载分析预览。');
  }, [appendMessage, openFactQueryPanel, showToast]);

  const openFactQuery = useCallback(() => {
    setFactQueryKeyword('');
    openFactQueryPanel();
  }, [openFactQueryPanel]);

  const closeFactQuery = useCallback(() => {
    closeFactQueryPanel();
    setFactQueryKeyword('');
  }, [closeFactQueryPanel]);

  return {
    factQueryKeyword,
    queryExistingFacts,
    openFactAnalysis,
    openFactQuery,
    closeFactQuery,
  };
}

function formatReadonlyFactQueryMessage(
  keyword: string,
  items: L3FactListItem[],
  total: number,
): string {
  const header = [
    '我帮你查了已有记录',
    `查询内容：${keyword}`,
    '这只是查看已有内容，不会新增、修改或形成分析结论。',
  ];
  if (items.length === 0) {
    return [...header, '没有找到匹配的记录。'].join('\n');
  }
  const resultLines = items.map((item, index) => {
    const createdAt = new Date(item.created_at).toLocaleString('zh-CN');
    return `${index + 1}. ${item.fact_payload_summary || '这条记录暂时没有摘要'}（${createdAt}）`;
  });
  const tail = total > items.length ? `仅展示前 ${items.length} 条，共 ${total} 条。` : `共 ${total} 条。`;
  return [...header, tail, ...resultLines].join('\n');
}
