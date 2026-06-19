import React from 'react';

export function ConfirmDialog({ open, onCancel, onConfirm }: { open: boolean; onCancel: () => void; onConfirm: () => void }) {
  if (!open) return null;
  return (
    <div className="h5-confirm-dialog-mask" role="presentation" onClick={onCancel}>
      <section className="h5-confirm-dialog" role="dialog" onClick={(event) => event.stopPropagation()}>
        <h3>确定退出登录吗？</h3>
        <p>当前为前端演示，将模拟清除本地登录态并返回登录页。</p>
        <div>
          <button onClick={onCancel}>取消</button>
          <button className="h5-dialog-danger" onClick={onConfirm}>退出登录</button>
        </div>
      </section>
    </div>
  );
}
