import React, { useEffect, useRef, useState } from 'react';
import {
  ActionBanner,
  CandidateList,
  ConfirmationPanel,
  ConfirmDialog,
  InputBox,
  InteractionPromptDialog,
  MessageStream,
  MockToast,
  SideDrawer,
  TaskRow,
  TodoListSheet,
  UploadChoiceSheet,
} from '../components/h5';
import { Hamburger } from '../components/h5/icons/H5Icons';
import FactQueryPanel from '../components/h5/overlays/FactQueryPanel';
import { listL3Facts } from '../modules/l3_query_view/api';
import type { L3FactListItem } from '../modules/facts_view/types';
import {
  checkGovernance,
  createCandidate,
  createPendingConfirmation,
  requestFactCreationAfterConfirmation,
  getL3FactView,
  listPendingConfirmations,
  reviewManualConfirmation,
  sendL0RawInput,
} from '../modules/input_flow/api';
import type { L1CandidateItem, PendingConfirmationItem, S2GovernanceCheckResponse } from '../modules/input_flow/types';
import {
  buildInteractionHints,
  formatCandidateGovernanceItem,
  formatGovernanceResult,
  getActionFromTextIntent,
  getCandidateSummary,
  loadStoredMessages,
  MESSAGE_STORAGE_KEY,
  resolveTextInputIntent,
} from '../modules/input_flow/h5Interaction';
import {
  H5_PROJECT_CONTEXTS,
  createLocalProjectContext,
  findProjectContextMatches,
} from '../modules/s1_runtime_context/state';
import type { H5ProjectContext } from '../modules/s1_runtime_context/types';
import {
  safeAddEventListener,
  safeClearTimeout,
  safeCreateObjectURL,
  safeGetHistoryState,
  safePushState,
  safeRevokeObjectURL,
  safeSetRenderStage,
  safeSetTimeout,
  safeTrySetItem,
} from '../utils/browserSafe';
import type {
  CandidateGovernanceItem,
  InteractionAction,
  InteractionMessage,
  InteractionPromptState,
} from '../modules/input_flow/h5Interaction';
import { SourceType } from '../modules/standard_governance/enums';
import { finishVoiceCapture, startVoiceCapture } from '../modules/voice_transcription';
import type { VoiceAction, VoiceCaptureSession, VoiceTranscriptionSource } from '../modules/voice_transcription';
import '../styles/h5.css';

type LocalTaskItem = {
  id: string;
  title: string;
  tag?: string;
};

const LOCAL_WEATHER = { icon: '☁', temp: '26°C', city: '上海' };
const LOCAL_DRAWER_PROFILE = { name: '张工', role: 'XX建科 · 项目负责人', companyCount: 1 };
const LOCAL_TASK_ITEMS: LocalTaskItem[] = [];
const LOCAL_DRAWER_MENU_GROUPS = [
  {
    title: '账号与公司',
    items: [
      { id: 'company', label: '切换公司', disabledWhenSingleCompany: true },
      { id: 'account', label: '切换账号' },
    ],
  },
  {
    title: '帮助与模式',
    items: [
      { id: 'guide', label: '新手指南' },
      { id: 'help', label: '使用说明' },
      { id: 'quickReply', label: '快捷回复' },
    ],
  },
  {
    title: '设置与隐私',
    items: [
      { id: 'voice', label: '语音偏好' },
      { id: 'privacy', label: '数据与隐私' },
    ],
  },
];

export default function H5MainPage() {
  safeSetRenderStage('H5MainPage 开始渲染');
  const [toastMsg, setToastMsg] = useState('');
  const [toastVisible, setToastVisible] = useState(false);
  const [uploadOpen, setUploadOpen] = useState(false);
  const [pendingOpen, setPendingOpen] = useState(false);
  const [todoOpen, setTodoOpen] = useState(false);
  const [drawerOpen, setDrawerOpen] = useState(false);
  const [logoutConfirmOpen, setLogoutConfirmOpen] = useState(false);
  const [factQueryOpen, setFactQueryOpen] = useState(false);
  const [recentPhotos, setRecentPhotos] = useState<string[]>([]);
  const [inputText, setInputText] = useState('');
  const [messages, setMessages] = useState<InteractionMessage[]>(loadStoredMessages);
  const [pendingItems, setPendingItems] = useState<PendingConfirmationItem[]>([]);
  const [candidateItems, setCandidateItems] = useState<CandidateGovernanceItem[]>([]);
  const [handledPendingIds, setHandledPendingIds] = useState<string[]>([]);
  const [pressingAction, setPressingAction] = useState<InteractionAction | null>(null);
  const [interactionPrompt, setInteractionPrompt] = useState<InteractionPromptState>(null);
  const [interactionPromptText, setInteractionPromptText] = useState('');
  const [selectedProject, setSelectedProject] = useState<H5ProjectContext | null>(null);
  const [projectContexts, setProjectContexts] = useState<H5ProjectContext[]>(H5_PROJECT_CONTEXTS);
  const [pendingProjectRecordText, setPendingProjectRecordText] = useState('');
  const cameraInputRef = useRef<HTMLInputElement>(null);
  const albumInputRef = useRef<HTMLInputElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);
  const messageEndRef = useRef<HTMLDivElement>(null);
  const touchStartX = useRef(999);
  const toastTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const activePressActionRef = useRef<VoiceAction | null>(null);
  const voiceCaptureRef = useRef<VoiceCaptureSession | null>(null);
  safeSetRenderStage('H5MainPage 状态初始化完成');

  function showToast(msg: string) {
    safeClearTimeout(toastTimerRef.current);
    setToastMsg(msg);
    setToastVisible(true);
    toastTimerRef.current = safeSetTimeout(() => setToastVisible(false), 3800);
  }

  function appendMessage(message: Omit<InteractionMessage, 'id' | 'createdAt'>) {
    const trimmed = message.content.trim();
    if (!trimmed) return;
    setMessages((prev) => [
      ...prev,
      {
        id: `${Date.now()}-${prev.length}`,
        ...message,
        content: trimmed,
        createdAt: new Date().toISOString(),
      },
    ]);
  }

  function appendToCentralInput(text: string) {
    const normalized = text.trim();
    if (!normalized) return;
    setInputText((prev) => (prev.trim() ? `${prev.trim()}\n${normalized}` : normalized));
    inputRef.current?.focus();
  }

  useEffect(() => {
    const stored = safeTrySetItem(MESSAGE_STORAGE_KEY, JSON.stringify(messages));
    if (!stored) {
      const compactMessages = messages.map((message) => (
        message.type === 'image' ? { ...message, dataUrl: undefined } : message
      ));
      safeTrySetItem(MESSAGE_STORAGE_KEY, JSON.stringify(compactMessages));
    }
    messageEndRef.current?.scrollIntoView({ behavior: 'smooth', block: 'end' });
  }, [messages]);

  useEffect(() => {
    function handleKeyDown(event: KeyboardEvent) {
      if (event.key === 'Escape') setDrawerOpen(false);
    }
    return safeAddEventListener('keydown', handleKeyDown);
  }, []);

  useEffect(() => {
    if (!drawerOpen) return;
    const state = { ...(safeGetHistoryState() as Record<string, unknown> || {}), h5Drawer: true };
    safePushState(state, '');
    return safeAddEventListener('popstate', () => setDrawerOpen(false), { once: true });
  }, [drawerOpen]);

  useEffect(() => {
    if (!pendingOpen) return;
    listPendingConfirmations()
      .then((response) => setPendingItems(response.items.filter((item) => !handledPendingIds.includes(item.pending_id))))
      .catch(() => showToast('待确认列表加载失败'));
  }, [pendingOpen, handledPendingIds]);

  useEffect(() => () => {
    recentPhotos.forEach(safeRevokeObjectURL);
  }, [recentPhotos]);

  useEffect(() => () => {
    safeClearTimeout(toastTimerRef.current);
  }, []);

  async function submitInput(action: InteractionAction = '录入') {
    const value = inputText.trim();
    if (!value) {
      showToast('请输入内容。');
      return;
    }
    setInputText('');
    const resolvedAction = action === '录入' ? getActionFromTextIntent(resolveTextInputIntent(value)) : action;
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
    if (!shouldSubmitToL0(action)) {
      const message = getUnavailableActionMessage(action);
      appendMessage({ type: 'status', action, content: message });
      showToast(message);
      return;
    }
    const projectContext = options.projectContext ?? selectedProject;
    if (!options.skipProjectContextCheck && !projectContext) {
      promptProjectContext(value);
      return;
    }
    try {
      const valueWithProject = formatTextWithProjectContext(value, projectContext);
      const rawInput = await sendL0RawInput({ text: valueWithProject, source_type: SourceType.MANUAL_INPUT });
      const candidate = await createCandidate({
        raw_input_id: rawInput.raw_input_id,
        input_session_id: rawInput.input_session_id,
        raw_payload: { text: valueWithProject, project_name: projectContext?.displayName },
        source_type: SourceType.MANUAL_INPUT,
      });
      const candidates = candidate.candidates && candidate.candidates.length > 0 ? candidate.candidates : [candidate];
      if (candidates.length > 1) {
        appendMessage({ type: 'status', action: '录入', content: `我看出这里有 ${candidates.length} 件事，会分开整理，方便你逐条确认。` });
      }
      await runGovernanceForCandidates(candidates, rawInput.raw_input_id);
    } catch {
      showToast('提交失败，请稍后再试。');
    }
  }

  function shouldSubmitToL0(action: InteractionAction): boolean {
    return action === '录入';
  }

  function promptProjectContext(recordText: string) {
    const matches = findProjectContextMatches(recordText, projectContexts);
    setPendingProjectRecordText(recordText);

    if (matches.length === 1) {
      const matchedProject = matches[0].project;
      setSelectedProject(matchedProject);
      appendMessage({
        type: 'status',
        action: '录入',
        content: `我先把这条记录关联到「${matchedProject.displayName}」。如果不对，可以重新输入项目名。`,
      });
      submitText(recordText, '录入', { skipProjectContextCheck: true, projectContext: matchedProject });
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
  }

  function formatTextWithProjectContext(value: string, project: H5ProjectContext | null): string {
    if (!project) return value;
    return `项目：${project.displayName}\n${value}`;
  }

  function getUnavailableActionMessage(action: InteractionAction): string {
    if (action === '问') {
      return '现在还不能直接分析。我可以先帮你查已有记录，或把要记录的情况先整理下来。';
    }
    return `${action}暂时还不能处理，请先用文字记录或查询已有记录。`;
  }

  async function queryExistingFacts(keyword: string) {
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
  }

  function formatReadonlyFactQueryMessage(keyword: string, items: L3FactListItem[], total: number): string {
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
      setPendingItems((prev) => [
        ...pendingResults,
        ...prev.filter((item) => !pendingResults.some((pending) => pending.pending_id === item.pending_id)),
      ]);
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
      const factText = typeof factView.fact_payload.text === 'string' ? factView.fact_payload.text : item.display_text;
      setHandledPendingIds((prev) => [...prev, item.pending_id]);
      setPendingItems((prev) => prev.filter((pending) => pending.pending_id !== item.pending_id));
      appendMessage({ type: 'status', action: '录入', content: `已确认并保存。\n${factText}` });
      showToast('已保存，可以在查询里看到。');
    } catch {
      showToast('待确认处理失败');
    }
  }

  async function beginVoicePress(action: InteractionAction) {
    if (!isVoiceAction(action) || voiceCaptureRef.current) return;
    activePressActionRef.current = action;
    setPressingAction(action);
    try {
      voiceCaptureRef.current = await startVoiceCapture(action);
      showToast('正在听你说话。');
    } catch (error) {
      activePressActionRef.current = null;
      setPressingAction(null);
      showToast(getVoiceErrorMessage(error));
    }
  }

  async function finishVoicePress(action: InteractionAction) {
    if (activePressActionRef.current !== action) return;
    const session = voiceCaptureRef.current;
    voiceCaptureRef.current = null;
    activePressActionRef.current = null;
    setPressingAction(null);
    if (!session) return;

    try {
      showToast('正在整理语音内容。');
      const result = await finishVoiceCapture(session);
      await handleVoiceTranscript(session.action, result.text, result.source);
    } catch (error) {
      showToast(getVoiceErrorMessage(error));
    }
  }

  async function handleVoiceTranscript(action: VoiceAction, text: string, source: VoiceTranscriptionSource) {
    const transcript = text.trim();
    if (!transcript) {
      showToast('语音转写结果为空。');
      return;
    }
    const sourceLabel = formatVoiceSourceLabel(source);
    if (action === '录入') {
      appendMessage({ type: 'status', action: '录入', content: `已识别语音：${sourceLabel}` });
      await submitText(transcript, '录入');
      return;
    }
    if (action === '查') {
      appendMessage({ type: 'status', action: '查', content: `已识别语音：${sourceLabel}\n查询内容：${transcript}` });
      await queryExistingFacts(transcript);
      return;
    }
    appendMessage({ type: 'status', action: '问', content: `已识别语音：${sourceLabel}\n你问的是：${transcript}\n现在还不能直接分析，我可以先帮你查相关记录。` });
    showToast('现在还不能直接分析。');
  }

  function isVoiceAction(action: InteractionAction): action is VoiceAction {
    return action === '查' || action === '录入' || action === '问';
  }

  function getVoiceErrorMessage(error: unknown): string {
    if (error instanceof Error && error.message.trim()) {
      return error.message.trim();
    }
    return '语音转写失败。';
  }

  function formatVoiceSourceLabel(source: VoiceTranscriptionSource): string {
    if (source === 'native_speech') return '本机识别';
    if (source === 'backend_asr') return '服务识别';
    return '不可用';
  }

  function updateRecentPhotos(fileList: FileList | null) {
    if (!fileList || fileList.length === 0) return;
    const imageFiles = Array.from(fileList).filter((file) => file.type.startsWith('image/'));
    if (imageFiles.length === 0) return;
    setRecentPhotos((prev) => {
      prev.forEach(safeRevokeObjectURL);
      return imageFiles
        .slice(-3)
        .map((file) => safeCreateObjectURL(file))
        .filter(Boolean);
    });
  }

  function handleImageInput(fileList: FileList | null) {
    const file = fileList?.[0];
    updateRecentPhotos(fileList);
    setUploadOpen(false);
    if (file) appendToCentralInput(file.name ? `已选择图片：${file.name}。请补充业务说明。` : '已选择图片。请补充业务说明。');
  }

  function handleInteractionAction(action: InteractionAction | string) {
    if (action === '上传图片') return albumInputRef.current?.click();
    if (action === '上传文件') return fileInputRef.current?.click();
    inputRef.current?.focus();
  }

  function submitInteractionPrompt() {
    if (!interactionPrompt) return;
    const value = interactionPromptText.trim();
    if (!value) {
      if (interactionPrompt.kind === 'project') return showToast('请填写项目名。');
      return showToast(interactionPrompt.kind === 'time' ? '请填写时间。' : '请填写人员。');
    }
    if (interactionPrompt.kind === 'project') {
      const project = createLocalProjectContext(value);
      setSelectedProject(project);
      setProjectContexts((prev) => {
        const normalizedProjectName = project.displayName.trim();
        if (prev.some((item) => item.displayName === normalizedProjectName)) return prev;
        return [...prev, project];
      });
      appendMessage({
        type: 'status',
        action: '录入',
        content: `已关联到「${project.displayName}」。这个名字只作为本次记录的项目上下文，不会直接新建正式项目。`,
      });
      const recordText = pendingProjectRecordText;
      setPendingProjectRecordText('');
      setInteractionPrompt(null);
      setInteractionPromptText('');
      if (recordText) {
        submitText(recordText, '录入', { skipProjectContextCheck: true, projectContext: project });
      }
      return;
    }
    appendMessage({ type: 'status', action: '录入', content: `${interactionPrompt.title}：${value}` });
    setInteractionPrompt(null);
    setInteractionPromptText('');
  }

  const interactionHints = buildInteractionHints();
  safeSetRenderStage('H5MainPage 子组件渲染前');

  return (
    <div
      className="h5-shell"
      onTouchStart={(event) => { if (event.touches[0].clientX <= 20) touchStartX.current = event.touches[0].clientX; }}
      onTouchEnd={(event) => {
        if (touchStartX.current <= 20 && event.changedTouches[0].clientX - touchStartX.current > 64) setDrawerOpen(true);
        touchStartX.current = 999;
      }}
    >
      <header className="h5-header">
        <button className="h5-header-btn" onClick={() => setDrawerOpen(true)} aria-label="打开侧边菜单"><Hamburger /></button>
        <h1 className="h5-header-title">罗盘</h1>
        <div className="h5-header-spacer" aria-hidden="true" />
        <button className="h5-header-btn" onClick={() => setFactQueryOpen(true)} title="查询事实">📋</button>
      </header>

      <section className="h5-task-card">
        <div className="h5-task-left">
          <button className="h5-task-title-btn" onClick={() => showToast('今日事项入口：可扩展至事项详情。')}><h2 className="h5-task-title">今日事项</h2></button>
          <ul className="h5-task-list">
            {LOCAL_TASK_ITEMS.map((item) => <TaskRow key={item.id} title={item.title} urgent={item.tag} onClick={() => showToast(`事项详情：${item.title}`)} />)}
          </ul>
          <button className="h5-task-more" onClick={() => setTodoOpen(true)}>查看全部（8）</button>
        </div>
        <button className="h5-task-right" onClick={() => setPendingOpen(true)}>
          <div className="h5-pending-label">待确认</div>
          <div className="h5-pending-num">{pendingItems.length}</div>
        </button>
      </section>

      <section className="h5-project-context-bar" aria-label="当前项目上下文">
        <div>
          <span className="h5-project-context-label">当前项目</span>
          <strong>{selectedProject ? selectedProject.displayName : '未选择'}</strong>
        </div>
        <button
          type="button"
          onClick={() => {
            setPendingProjectRecordText('');
            setInteractionPrompt({
              kind: 'project',
              title: selectedProject ? '切换项目' : '选择或新建项目',
              placeholder: '例如：宝山项目',
            });
          }}
        >
          {selectedProject ? '切换' : '选择/新建'}
        </button>
      </section>

      <section className="h5-main-panel">
        <div className="h5-panel-bg" />
        <div className="h5-weather-widget" aria-hidden="true">
          <span className="h5-weather-icon">{LOCAL_WEATHER.icon}</span>
          <span>{LOCAL_WEATHER.city}</span>
          <strong>{LOCAL_WEATHER.temp}</strong>
        </div>
        <div className="h5-panel-content h5-message-area">
          <ActionBanner hints={interactionHints} />
          <CandidateList items={candidateItems} />
          <MessageStream messages={messages} messageEndRef={messageEndRef} />
          {interactionHints.actions.length > 0 ? (
            <div className="h5-interaction-actions" aria-label="下一步动作提示">
              {interactionHints.actions.map((action) => <button key={action} type="button" onClick={() => handleInteractionAction(action)}>{action}</button>)}
            </div>
          ) : null}
        </div>
      </section>

      <MockToast message={toastMsg} visible={toastVisible} />
      <InputBox
        inputRef={inputRef}
        inputText={inputText}
        uploadOpen={uploadOpen}
        pressingAction={pressingAction}
        onInputChange={setInputText}
        onSubmit={submitInput}
        onToggleUpload={() => setUploadOpen((prev) => !prev)}
        onVoiceStart={beginVoicePress}
        onVoiceEnd={finishVoicePress}
      />
      <UploadChoiceSheet open={uploadOpen} onClose={() => setUploadOpen(false)} recentPhotos={recentPhotos} onOpenCamera={() => cameraInputRef.current?.click()} onOpenAlbum={() => albumInputRef.current?.click()} onOpenFile={() => fileInputRef.current?.click()} />
      <TodoListSheet open={todoOpen} onClose={() => setTodoOpen(false)} onMockAction={showToast} />
      <ConfirmationPanel open={pendingOpen} onClose={() => setPendingOpen(false)} showToast={showToast} items={pendingItems} onConfirmItem={confirmPendingItem} onSupplementItem={(item) => { setPendingOpen(false); appendToCentralInput(`补充待确认事项：${item.display_text}`); showToast('请在中央输入框补充信息后提交。'); }} />
      <SideDrawer open={drawerOpen} onClose={() => setDrawerOpen(false)} onNavigate={(id, label, disabled) => {
        if (disabled) return showToast('当前公司仅一个，无需切换');
        setDrawerOpen(false);
        showToast(id === 'account' ? '账号切换功能即将上线' : `${label}，功能开发中`);
      }} onLogout={() => setLogoutConfirmOpen(true)} profile={LOCAL_DRAWER_PROFILE} menuGroups={LOCAL_DRAWER_MENU_GROUPS} />
      <ConfirmDialog open={logoutConfirmOpen} onCancel={() => setLogoutConfirmOpen(false)} onConfirm={() => { setLogoutConfirmOpen(false); setDrawerOpen(false); showToast('已退出登录'); }} />
      <InteractionPromptDialog prompt={interactionPrompt} value={interactionPromptText} onValueChange={setInteractionPromptText} onCancel={() => setInteractionPrompt(null)} onSubmit={submitInteractionPrompt} />
      <input ref={cameraInputRef} type="file" accept="image/*" capture="environment" className="h5-hidden-input" onChange={(event) => { handleImageInput(event.target.files); event.currentTarget.value = ''; }} />
      <input ref={albumInputRef} type="file" accept="image/*" className="h5-hidden-input" onChange={(event) => { handleImageInput(event.target.files); event.currentTarget.value = ''; }} />
      <input ref={fileInputRef} type="file" className="h5-hidden-input" onChange={(event) => {
        const file = event.target.files?.[0];
        if (file) {
          setUploadOpen(false);
          appendToCentralInput(file.name ? `已选择文件：${file.name}。请补充业务说明。` : '已选择文件。请补充业务说明。');
        }
        event.currentTarget.value = '';
      }} />
      {factQueryOpen && <FactQueryPanel onClose={() => setFactQueryOpen(false)} />}
      <RenderStageMarker stage="H5MainPage 子组件渲染完成" />
    </div>
  );
}

function RenderStageMarker({ stage }: { stage: string }) {
  safeSetRenderStage(stage);
  return null;
}
