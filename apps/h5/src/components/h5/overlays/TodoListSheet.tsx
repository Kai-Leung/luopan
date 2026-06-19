import React from 'react';

type TodoListItem = {
  id: string;
  title: string;
  tag?: string;
};

export function TodoListSheet({
  open,
  onClose,
  items,
  onSelect,
}: {
  open: boolean;
  onClose: () => void;
  items: TodoListItem[];
  onSelect: (item: TodoListItem) => void;
}) {
  return (
    <div className={`h5-upload-sheet ${open ? 'h5-upload-sheet-open' : ''}`} aria-hidden={!open}>
      <button className="h5-upload-mask" onClick={onClose} aria-label="关闭全部事项" />
      <section className="h5-upload-panel h5-todo-panel" aria-label="全部事项">
        <button className="h5-upload-handle" onClick={onClose} aria-label="关闭全部事项" />
        <div className="h5-upload-head">
          <h2>全部事项</h2>
          <span>{items.length} 项</span>
        </div>
        <div className="h5-todo-list">
          {items.map((item) => (
            <button className="h5-todo-card" key={item.id} onClick={() => onSelect(item)}>
              <span className="h5-task-dot h5-task-dot-blue" />
              <span className="h5-todo-title">{item.title}</span>
              {item.tag ? <span className="h5-task-urgent h5-todo-tag">{item.tag}</span> : null}
            </button>
          ))}
          {items.length === 0 ? <div className="h5-todo-empty">当前没有待处理事项。</div> : null}
        </div>
      </section>
    </div>
  );
}
