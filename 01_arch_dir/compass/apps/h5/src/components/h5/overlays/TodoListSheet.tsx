import React from 'react';

type TodoListItem = {
  id: string;
  title: string;
  tag?: string;
};

const TODO_LIST_ITEMS: TodoListItem[] = [];

export function TodoListSheet({ open, onClose, onMockAction }: { open: boolean; onClose: () => void; onMockAction: (message: string) => void }) {
  return (
    <div className={`h5-upload-sheet ${open ? 'h5-upload-sheet-open' : ''}`} aria-hidden={!open}>
      <button className="h5-upload-mask" onClick={onClose} aria-label="关闭全部事项" />
      <section className="h5-upload-panel h5-todo-panel" aria-label="全部事项">
        <button className="h5-upload-handle" onClick={onClose} aria-label="关闭全部事项" />
        <div className="h5-upload-head">
          <h2>全部事项</h2>
          <button>查看列表（开发中）</button>
        </div>
        <div className="h5-todo-list">
          {TODO_LIST_ITEMS.map((item) => (
            <button className="h5-todo-card" key={item.id} onClick={() => onMockAction(`事项详情：${item.title}`)}>
              <span className="h5-task-dot h5-task-dot-blue" />
              <span className="h5-todo-title">{item.title}</span>
              {item.tag ? <span className="h5-task-urgent h5-todo-tag">{item.tag}</span> : null}
            </button>
          ))}
        </div>
      </section>
    </div>
  );
}
