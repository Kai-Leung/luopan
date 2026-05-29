import React from 'react';

export function FactCard({ content }: { content: string }) {
  const safeContent = typeof content === 'string' ? content : '';
  return (
    <p>
      {safeContent.split('\n').map((line, index) => (
        <React.Fragment key={`${line}-${index}`}>
          {index > 0 ? <br /> : null}
          {line}
        </React.Fragment>
      ))}
    </p>
  );
}
