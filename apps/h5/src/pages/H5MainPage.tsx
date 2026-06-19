import React, { useRef, useState } from 'react';
import {
  ActionBanner,
  CandidateList,
  ConfirmationPanel,
  ConfirmDialog,
  InputBox,
  InteractionPromptDialog,
  MessageStream,
  SideDrawer,
  TaskRow,
  Toast,
  TodoListSheet,
  UploadChoiceSheet,
} from '../components/h5';
import { Hamburger } from '../components/h5/icons/H5Icons';
import FactQueryPanel from '../components/h5/overlays/FactQueryPanel';
import { useH5NativeBack } from '../app/useH5NativeBack';
import { useH5ShellState } from '../app/useH5ShellState';
import { useH5Toast } from '../app/useH5Toast';
import { buildInteractionHints } from '../modules/input_flow/h5Interaction';
import type { H5ProjectContext } from '../modules/s1_runtime_context/types';
import { useInputFlow, useInputFlowState } from '../modules/input_flow/useFlow';
import { useInteractionMessages } from '../modules/input_flow/useInteractionMessages';
import { useL3QueryViewFlow } from '../modules/l3_query_view/useFlow';
import { useS1RuntimeContextFlow } from '../modules/s1_runtime_context/useFlow';
import { useUploadFlow } from '../modules/upload/useFlow';
import { useVoiceTranscriptionFlow } from '../modules/voice_transcription/useFlow';
import { safeSetRenderStage } from '../utils/browserSafe';
import '../styles/h5.css';

type LocalTaskItem = { id: string; title: string; tag?: string };

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
  const inputRef = useRef<HTMLTextAreaElement>(null);
  const cameraInputRef = useRef<HTMLInputElement>(null);
  const albumInputRef = useRef<HTMLInputElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [inputText, setInputText] = useState('');
  const toast = useH5Toast();
  const shell = useH5ShellState();
  const messages = useInteractionMessages({ inputRef, setInputText });
  const inputFlowState = useInputFlowState();
  const runtime = useS1RuntimeContextFlow({
    appendMessage: messages.appendMessage,
    clearMessages: messages.clearMessages,
    resetInputFlowState: inputFlowState.resetInputFlowState,
    showToast: toast.showToast,
  });
  const query = useL3QueryViewFlow({
    appendMessage: messages.appendMessage,
    showToast: toast.showToast,
    openFactQueryPanel: shell.openFactQuery,
    closeFactQueryPanel: shell.closeFactQuery,
  });
  const inputFlow = useInputFlow({
    inputText,
    setInputText,
    selectedProject: runtime.selectedProject,
    pendingOpen: shell.pendingOpen,
    inputFlowState,
    appendMessage: messages.appendMessage,
    showToast: toast.showToast,
    openPending: shell.openPending,
    queryExistingFacts: query.queryExistingFacts,
    openFactAnalysis: query.openFactAnalysis,
    resolveProjectContextForRecord: runtime.resolveProjectContextForRecord,
    promptProjectContext: runtime.promptProjectContext,
    applyProjectContext: runtime.applyProjectContext,
    formatTextWithProjectContext: runtime.formatTextWithProjectContext,
  });
  const upload = useUploadFlow({
    appendMessage: messages.appendMessage,
    appendToCentralInput: messages.appendToCentralInput,
    showToast: toast.showToast,
    closeUpload: shell.closeUpload,
  });
  const voice = useVoiceTranscriptionFlow({
    appendMessage: messages.appendMessage,
    showToast: toast.showToast,
    submitText: inputFlow.submitText,
    queryExistingFacts: query.queryExistingFacts,
    openFactAnalysis: query.openFactAnalysis,
  });

  useH5NativeBack({
    ...shell,
    interactionPrompt: runtime.interactionPrompt,
    closeFactQuery: query.closeFactQuery,
    closeInteractionPrompt: runtime.closeInteractionPrompt,
  });
  safeSetRenderStage('H5MainPage 状态初始化完成');

  const submitProjectRecord = (recordText: string, project: H5ProjectContext) => {
    void inputFlow.submitText(recordText, '录入', { skipProjectContextCheck: true, projectContext: project });
  };
  const handleInteractionAction = (action: string) => {
    if (action === '上传图片') albumInputRef.current?.click();
    else if (action === '上传文件') fileInputRef.current?.click();
    else inputRef.current?.focus();
  };
  const interactionHints = buildInteractionHints();
  safeSetRenderStage('H5MainPage 子组件渲染前');

  return (
    <div
      className="h5-shell"
      onTouchStart={(event) => shell.onShellTouchStart(event.touches[0].clientX)}
      onTouchEnd={(event) => shell.onShellTouchEnd(event.changedTouches[0].clientX)}
    >
      <header className="h5-header">
        <button className="h5-header-btn" onClick={shell.openDrawer} aria-label="打开侧边菜单"><Hamburger /></button>
        <h1 className="h5-header-title">罗盘</h1>
        <div className="h5-header-spacer" aria-hidden="true" />
        <button className="h5-header-btn" onClick={query.openFactQuery} title="查询事实">📋</button>
      </header>

      <section className="h5-task-card">
        <div className="h5-task-left">
          <button className="h5-task-title-btn" onClick={() => toast.showToast('今日事项入口：可扩展至事项详情。')}><h2 className="h5-task-title">今日事项</h2></button>
          <ul className="h5-task-list">
            {LOCAL_TASK_ITEMS.map((item) => <TaskRow key={item.id} title={item.title} urgent={item.tag} onClick={() => toast.showToast(`事项详情：${item.title}`)} />)}
          </ul>
          <button className="h5-task-more" onClick={shell.openTodo}>查看全部（{LOCAL_TASK_ITEMS.length}）</button>
        </div>
        <button className="h5-task-right" onClick={shell.openPending}>
          <div className="h5-pending-label">待确认</div>
          <div className="h5-pending-num">{inputFlow.pendingItems.length}</div>
        </button>
      </section>

      <section className="h5-project-context-bar" aria-label="当前项目上下文">
        <div>
          <span className="h5-project-context-label">
            {runtime.runtimeContext
              ? `${runtime.runtimeContext.organization_name} · ${runtime.runtimeContext.role_names.join('、')}`
              : '运行上下文加载中'}
          </span>
          <strong>{runtime.selectedProject ? runtime.selectedProject.displayName : '未选择'}</strong>
        </div>
        <button type="button" onClick={runtime.openProjectPrompt}>
          {runtime.selectedProject ? '切换' : '选择/新建'}
        </button>
      </section>

      <section className="h5-main-panel">
        <div className="h5-panel-bg" />
        <div className="h5-panel-content h5-message-area">
          <ActionBanner hints={interactionHints} />
          <CandidateList items={inputFlow.candidateItems} />
          <MessageStream messages={messages.messages} messageEndRef={messages.messageEndRef} />
          {interactionHints.actions.length > 0 ? (
            <div className="h5-interaction-actions" aria-label="下一步动作提示">
              {interactionHints.actions.map((action) => <button key={action} type="button" onClick={() => handleInteractionAction(action)}>{action}</button>)}
            </div>
          ) : null}
        </div>
      </section>

      <Toast message={toast.toastMsg} visible={toast.toastVisible} />
      <InputBox
        inputRef={inputRef}
        inputText={inputText}
        uploadOpen={shell.uploadOpen}
        pressingAction={voice.pressingAction}
        onInputChange={setInputText}
        onSubmit={inputFlow.submitInput}
        onToggleUpload={shell.toggleUpload}
        onVoiceStart={voice.beginVoicePress}
        onVoiceEnd={voice.finishVoicePress}
      />
      <UploadChoiceSheet
        open={shell.uploadOpen}
        onClose={shell.closeUpload}
        onOpenCamera={() => cameraInputRef.current?.click()}
        onOpenAlbum={() => albumInputRef.current?.click()}
        onOpenFile={() => fileInputRef.current?.click()}
      />
      <TodoListSheet open={shell.todoOpen} onClose={shell.closeTodo} items={LOCAL_TASK_ITEMS} onSelect={(item) => toast.showToast(`事项详情：${item.title}`)} />
      <ConfirmationPanel
        open={shell.pendingOpen}
        onClose={shell.closePending}
        showToast={toast.showToast}
        items={inputFlow.pendingItems}
        onConfirmItem={inputFlow.confirmPendingItem}
        onSupplementItem={(item) => {
          shell.closePending();
          messages.appendToCentralInput(`补充待确认事项：${item.display_text}`);
          toast.showToast('请在中央输入框补充信息后提交。');
        }}
      />
      <SideDrawer
        open={shell.drawerOpen}
        onClose={shell.closeDrawer}
        onNavigate={(id, label, disabled) => {
          if (disabled) return toast.showToast('当前公司仅一个，无需切换');
          shell.closeDrawer();
          toast.showToast(id === 'account' ? '账号切换功能即将上线' : `${label}，功能开发中`);
        }}
        onLogout={shell.openLogoutConfirm}
        profile={{
          name: runtime.runtimeContext?.user_display_name || '未识别用户',
          role: runtime.runtimeContext
            ? `${runtime.runtimeContext.organization_name} · ${runtime.runtimeContext.role_names.join('、')}`
            : '运行上下文加载中',
          companyCount: runtime.runtimeContext ? 1 : 0,
        }}
        menuGroups={LOCAL_DRAWER_MENU_GROUPS}
      />
      <ConfirmDialog
        open={shell.logoutConfirmOpen}
        onCancel={shell.closeLogoutConfirm}
        onConfirm={() => {
          shell.closeLogoutConfirm();
          shell.closeDrawer();
          toast.showToast('已退出登录');
        }}
      />
      <InteractionPromptDialog
        prompt={runtime.interactionPrompt}
        value={runtime.interactionPromptText}
        onValueChange={runtime.setInteractionPromptText}
        onCancel={runtime.closeInteractionPrompt}
        onSubmit={() => runtime.submitProjectPrompt(submitProjectRecord)}
      />
      <input ref={cameraInputRef} type="file" accept="image/jpeg,image/png,image/heic,image/heif,.jpg,.jpeg,.png,.heic,.heif" capture="environment" className="h5-hidden-input" onChange={(event) => { void upload.handleImageInput(event.target.files); event.currentTarget.value = ''; }} />
      <input ref={albumInputRef} type="file" accept="image/jpeg,image/png,image/heic,image/heif,.jpg,.jpeg,.png,.heic,.heif" className="h5-hidden-input" onChange={(event) => { void upload.handleImageInput(event.target.files); event.currentTarget.value = ''; }} />
      <input ref={fileInputRef} type="file" accept=".jpg,.jpeg,.png,.heic,.heif,.pdf,image/jpeg,image/png,image/heic,image/heif,application/pdf" className="h5-hidden-input" onChange={(event) => { void upload.handleFileInput(event.target.files); event.currentTarget.value = ''; }} />
      {shell.factQueryOpen ? (
        <FactQueryPanel
          initialKeyword={query.factQueryKeyword}
          autoAnalyzeFirstMatch={Boolean(query.factQueryKeyword)}
          onClose={query.closeFactQuery}
        />
      ) : null}
      <RenderStageMarker stage="H5MainPage 子组件渲染完成" />
    </div>
  );
}

function RenderStageMarker({ stage }: { stage: string }) {
  safeSetRenderStage(stage);
  return null;
}
