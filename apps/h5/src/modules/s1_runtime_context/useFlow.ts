import { useCallback, useEffect, useState } from 'react';
import type { Dispatch, SetStateAction } from 'react';
import type {
  InteractionMessage,
  InteractionPromptState,
} from '../input_flow/h5Interaction';
import { safeGetItem, safeTrySetItem } from '../../utils/browserSafe';
import { fetchRuntimeContext } from './api';
import { setRuntimeProjectId } from './constants';
import {
  H5_PROJECT_CONTEXTS,
  createLocalProjectContext,
  extractProjectContextFromText,
  findProjectContextMatches,
} from './state';
import type { H5ProjectContext, RuntimeContextResponse } from './types';

type AppendMessage = (message: Omit<InteractionMessage, 'id' | 'createdAt'>) => void;
type SubmitProjectRecord = (recordText: string, project: H5ProjectContext) => void;

type UseS1RuntimeContextFlowOptions = {
  appendMessage: AppendMessage;
  clearMessages: () => void;
  resetInputFlowState: () => void;
  showToast: (message: string) => void;
};

export function useS1RuntimeContextFlow({
  appendMessage,
  clearMessages,
  resetInputFlowState,
  showToast,
}: UseS1RuntimeContextFlowOptions) {
  const [runtimeContext, setRuntimeContext] = useState<RuntimeContextResponse | null>(null);
  const [selectedProject, setSelectedProject] = useState<H5ProjectContext | null>(null);
  const [projectContexts, setProjectContexts] = useState<H5ProjectContext[]>(H5_PROJECT_CONTEXTS);
  const [pendingProjectRecordText, setPendingProjectRecordText] = useState('');
  const [interactionPrompt, setInteractionPrompt] = useState<InteractionPromptState>(null);
  const [interactionPromptText, setInteractionPromptText] = useState('');

  useEffect(() => {
    fetchRuntimeContext()
      .then((context) => {
        const previousContextId = safeGetItem('runtime_context_id');
        if (previousContextId !== context.context_id) {
          clearMessages();
          resetInputFlowState();
        }
        safeTrySetItem('runtime_context_id', context.context_id);
        setRuntimeContext(context);
        setProjectContexts(context.project_scope.map((project) => ({
          projectId: project.project_id,
          displayName: project.display_name,
          aliases: project.aliases,
        })));
      })
      .catch((error) => {
        const message = error instanceof Error && error.message.trim()
          ? error.message.trim()
          : '运行上下文加载失败';
        showToast(message);
      });
  }, [clearMessages, resetInputFlowState, showToast]);

  const closeInteractionPrompt = useCallback(() => setInteractionPrompt(null), []);

  const applyProjectContext = useCallback((project: H5ProjectContext, isNew: boolean) => {
    const alreadySelected = selectedProject?.displayName === project.displayName;
    const projectChanged = Boolean(selectedProject && selectedProject.projectId !== project.projectId);
    if (projectChanged) {
      clearMessages();
      resetInputFlowState();
      setInteractionPrompt(null);
      setInteractionPromptText('');
    }
    setSelectedProject(project);
    setRuntimeProjectId(project.projectId);
    if (isNew) {
      setProjectContexts((previous) => {
        if (previous.some((item) => item.displayName === project.displayName)) return previous;
        return [...previous, project];
      });
    }
    if (alreadySelected && !isNew) return;
    appendMessage({
      type: 'status',
      action: '录入',
      content: isNew
        ? `已按「${project.displayName}」记录项目上下文，不会直接新建正式项目。`
        : `已关联到「${project.displayName}」。`,
    });
  }, [appendMessage, clearMessages, resetInputFlowState, selectedProject]);

  const promptProjectContext = useCallback((
    recordText: string,
    submitProjectRecord: SubmitProjectRecord,
  ) => {
    const matches = findProjectContextMatches(recordText, projectContexts);
    setPendingProjectRecordText(recordText);

    if (matches.length === 1) {
      const matchedProject = matches[0].project;
      applyProjectContext(matchedProject, false);
      submitProjectRecord(recordText, matchedProject);
      return;
    }

    const extractedProject = extractProjectContextFromText(recordText, projectContexts);
    if (extractedProject) {
      applyProjectContext(extractedProject.project, extractedProject.isNew);
      submitProjectRecord(recordText, extractedProject.project);
      return;
    }

    const hint = matches.length > 1
      ? `我找到了几个可能的项目：${matches.map((match) => match.project.displayName).join('、')}。请先输入这条记录属于哪个项目。`
      : '这条记录需要先关联项目。请输入项目名；如果还没有项目，我会先按这个名字作为本次记录的项目上下文。';
    appendMessage({ type: 'status', action: '录入', content: hint });
    setInteractionPrompt({
      kind: 'project',
      title: '这条记录属于哪个项目？',
      placeholder: '例如：宝山项目',
    });
    showToast('请先补充项目名。');
  }, [appendMessage, applyProjectContext, projectContexts, showToast]);

  const submitProjectPrompt = useCallback((submitProjectRecord: SubmitProjectRecord) => {
    if (!interactionPrompt) return;
    const value = interactionPromptText.trim();
    if (!value) {
      if (interactionPrompt.kind === 'project') {
        showToast('请填写项目名。');
      } else {
        showToast(interactionPrompt.kind === 'time' ? '请填写时间。' : '请填写人员。');
      }
      return;
    }
    if (interactionPrompt.kind === 'project') {
      const project = createLocalProjectContext(value);
      applyProjectContext(project, true);
      const recordText = pendingProjectRecordText;
      setPendingProjectRecordText('');
      setInteractionPrompt(null);
      setInteractionPromptText('');
      if (recordText) submitProjectRecord(recordText, project);
      return;
    }
    appendMessage({ type: 'status', action: '录入', content: `${interactionPrompt.title}：${value}` });
    setInteractionPrompt(null);
    setInteractionPromptText('');
  }, [
    appendMessage,
    applyProjectContext,
    interactionPrompt,
    interactionPromptText,
    pendingProjectRecordText,
    showToast,
  ]);

  const formatTextWithProjectContext = useCallback((value: string, project: H5ProjectContext | null) => (
    project ? `项目：${project.displayName}\n${value}` : value
  ), []);

  const resolveProjectContextForRecord = useCallback((value: string) => {
    const matches = findProjectContextMatches(value, projectContexts);
    if (matches.length > 1) return null;
    const extractedProject = extractProjectContextFromText(value, projectContexts);
    if (extractedProject) {
      return { ...extractedProject, shouldApply: true };
    }
    return selectedProject
      ? { project: selectedProject, isNew: false, shouldApply: false }
      : null;
  }, [projectContexts, selectedProject]);

  const openProjectPrompt = useCallback(() => {
    setPendingProjectRecordText('');
    setInteractionPrompt({
      kind: 'project',
      title: selectedProject ? '切换项目' : '选择或新建项目',
      placeholder: '例如：宝山项目',
    });
  }, [selectedProject]);

  return {
    runtimeContext,
    selectedProject,
    projectContexts,
    pendingProjectRecordText,
    interactionPrompt,
    interactionPromptText,
    setInteractionPrompt: setInteractionPrompt as Dispatch<SetStateAction<InteractionPromptState>>,
    setInteractionPromptText,
    closeInteractionPrompt,
    promptProjectContext,
    applyProjectContext,
    formatTextWithProjectContext,
    resolveProjectContextForRecord,
    submitProjectPrompt,
    openProjectPrompt,
  };
}
