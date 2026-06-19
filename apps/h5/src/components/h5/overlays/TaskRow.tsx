import React from 'react';

export function TaskRow({ title, urgent, onClick }: { title: string; urgent?: string; onClick: () => void }) {
  return (
    <li className="h5-task-item">
      <span className="h5-task-dot h5-task-dot-blue" />
      <button className="h5-task-link" onClick={onClick}>{title}</button>
      {urgent ? <span className="h5-task-urgent">{urgent}</span> : null}
    </li>
  );
}
