import React from 'react';
import type { RefObject } from 'react';
import type { InteractionMessage } from '../../../modules/input_flow/h5Interaction';
import { formatFileSize } from '../../../modules/input_flow/h5Interaction';
import { FileIcon, ImageIcon } from '../icons/H5Icons';
import { FactCard } from '../FactCard/FactCard';

export function MessageStream({
  messages,
  messageEndRef,
}: {
  messages: InteractionMessage[];
  messageEndRef: RefObject<HTMLDivElement | null>;
}) {
  const visibleMessages = Array.isArray(messages) ? messages : [];
  return (
    <div className="h5-message-stream">
      {visibleMessages.length > 0 ? (
        <div className="h5-message-list" aria-label="本地输入记录">
          {visibleMessages.map((message) => (
            <article className={`h5-message-bubble h5-message-${message.type}`} key={message.id}>
              {message.type === 'image' ? (
                <div className="h5-message-image-body">
                  {message.dataUrl ? (
                    <img className="h5-message-image-preview" src={message.dataUrl} alt={message.fileName || '本地图片记录'} />
                  ) : (
                    <div className="h5-message-image-fallback">
                      <ImageIcon />
                      <span>本地图片记录</span>
                    </div>
                  )}
                  <p>{message.fileName || message.content}</p>
                </div>
              ) : message.type === 'file' ? (
                <div className="h5-message-file-card">
                  <span className="h5-message-file-icon"><FileIcon /></span>
                  <span className="h5-message-file-copy">
                    <strong>{message.fileName || message.content}</strong>
                    <small>{formatFileSize(message.fileSize)}</small>
                  </span>
                </div>
              ) : (
                <FactCard content={message.content} />
              )}
            </article>
          ))}
          <div ref={messageEndRef} />
        </div>
      ) : (
        <div className="h5-message-empty">
          <h2>今天从哪里开始？</h2>
          <p>输入内容会显示在这里</p>
          <div className="h5-message-empty-phrases">
            <span>记录了什么</span>
            <span>查一下费用</span>
            <span>有没有风险</span>
          </div>
        </div>
      )}
    </div>
  );
}
