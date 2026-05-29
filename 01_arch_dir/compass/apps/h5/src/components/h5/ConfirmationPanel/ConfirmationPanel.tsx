import React, { useRef, useState } from 'react';
import type { PendingConfirmationItem } from '../../../modules/input_flow/types';
import { ConfirmTypeIcon, VoiceSupplementIcon } from '../icons/H5Icons';

export function ConfirmationPanel({
  open,
  onClose,
  showToast,
  items,
  onConfirmItem,
  onSupplementItem,
}: {
  open: boolean;
  onClose: () => void;
  showToast: (message: string) => void;
  items: PendingConfirmationItem[];
  onConfirmItem: (item: PendingConfirmationItem) => void;
  onSupplementItem: (item: PendingConfirmationItem) => void;
}) {
  const [shakeId, setShakeId] = useState('');
  const [reasonState, setReasonState] = useState<{ itemId: string; mode: 'reject' | 'supplement' } | null>(null);
  const [reasonText, setReasonText] = useState('');
  const touchStartY = useRef(0);
  const reasonTitle = reasonState?.mode === 'reject' ? '填写驳回原因' : '填写补充说明';
  const reasonPlaceholder = reasonState?.mode === 'reject' ? '请输入驳回原因...' : '请输入需要补充的内容...';
  const pendingItems = Array.isArray(items) ? items : [];

  function submitReason() {
    if (!reasonState) return;
    if (!reasonText.trim()) {
      showToast(reasonState.mode === 'reject' ? '请填写驳回原因。' : '请填写补充说明。');
      return;
    }
    setReasonState(null);
    setReasonText('');
    showToast(reasonState.mode === 'reject' ? '已填写驳回原因，仅作为前端本地演示。' : '已填写补充说明，仅作为前端本地演示。');
  }

  return (
    <div className={`h5-pending-sheet ${open ? 'h5-pending-sheet-open' : ''}`} aria-hidden={!open}>
      <button className="h5-pending-mask" onClick={onClose} aria-label="关闭待确认浮态" />
      <section
        className="h5-pending-panel"
        aria-label="待确认浮态"
        onTouchStart={(event) => { touchStartY.current = event.touches[0].clientY; }}
        onTouchEnd={(event) => { if (event.changedTouches[0].clientY - touchStartY.current > 56) onClose(); }}
      >
        <button className="h5-pending-handle" onClick={onClose} aria-label="关闭待确认浮态" />
        <header className="h5-pending-header">
          <div>
            <h2>待确认</h2>
            <p>请及时确认以下事项</p>
          </div>
          <button className="h5-pending-mini-card" onClick={() => showToast('待确认列表功能即将上线')}>
            <span>待确认</span>
            <strong>{pendingItems.length}</strong>
          </button>
        </header>
        <main className="h5-pending-list">
          {pendingItems.length === 0 ? (
            <div className="h5-message-empty">
              <h2>暂无待确认项</h2>
              <p>需要用户确认的事项会进入这里</p>
            </div>
          ) : null}
          {pendingItems.map((item, index) => (
            <article className={`h5-pending-card ${shakeId === item.pending_id ? 'h5-card-shake' : ''}`} key={item.pending_id}>
              <div className="h5-pending-card-head">
                <ConfirmTypeIcon index={index} />
                <button className="h5-confirm-voice" onClick={() => showToast('语音补充功能即将上线')} aria-label="语音补充">
                  <VoiceSupplementIcon />
                </button>
              </div>
              <div className="h5-confirm-card-body">
                <h2>待确认事项</h2>
                <p className="h5-confirm-copy">{item.display_text}</p>
                <div className="h5-confirm-meta">
                  <span>来源：S2 治理结果</span>
                  <span>创建时间：{item.created_at}</span>
                </div>
                <div className="h5-confirm-actions">
                  <button className="h5-confirm-primary" onClick={() => onConfirmItem(item)}>确认</button>
                  <button onClick={() => { setReasonState({ itemId: item.pending_id, mode: 'reject' }); setReasonText(''); setShakeId(item.pending_id); }}>驳回</button>
                  <button className="h5-confirm-add" onClick={() => onSupplementItem(item)}>补充</button>
                </div>
              </div>
            </article>
          ))}
        </main>
      </section>
      {reasonState ? (
        <div className="h5-reason-dialog-mask" role="presentation" onClick={() => setReasonState(null)}>
          <section className="h5-reason-dialog" role="dialog" aria-label={reasonTitle} onClick={(event) => event.stopPropagation()}>
            <h3>{reasonTitle}</h3>
            <textarea value={reasonText} placeholder={reasonPlaceholder} onChange={(event) => setReasonText(event.target.value)} autoFocus />
            <div className="h5-reason-actions">
              <button onClick={() => setReasonState(null)}>取消</button>
              <button className="h5-reason-submit" onClick={submitReason}>提交</button>
            </div>
          </section>
        </div>
      ) : null}
    </div>
  );
}
