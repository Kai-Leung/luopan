import React, { useRef } from 'react';
import { CameraIcon, FileIcon } from '../icons/H5Icons';

export type PendingUploadPreview = {
  fileName: string;
  fileSizeText: string;
  kind: 'image' | 'file';
  previewUrl?: string;
};

export function UploadChoiceSheet({
  open,
  onClose,
  onOpenCamera,
  onOpenAlbum,
  onOpenFile,
  pendingUpload,
  onClearPendingUpload,
  onConfirmUpload,
}: {
  open: boolean;
  onClose: () => void;
  onOpenCamera: () => void;
  onOpenAlbum: () => void;
  onOpenFile: () => void;
  pendingUpload: PendingUploadPreview | null;
  onClearPendingUpload: () => void;
  onConfirmUpload: () => void;
}) {
  const touchStartY = useRef(0);
  return (
    <div className={`h5-upload-sheet ${open ? 'h5-upload-sheet-open' : ''}`} aria-hidden={!open}>
      <button className="h5-upload-mask" onClick={onClose} aria-label="关闭上传选择" />
      <section
        className="h5-upload-panel"
        aria-label="上传选择"
        onTouchStart={(event) => { touchStartY.current = event.touches[0].clientY; }}
        onTouchEnd={(event) => { if (event.changedTouches[0].clientY - touchStartY.current > 56) onClose(); }}
      >
        <button className="h5-upload-handle" onClick={onClose} aria-label="关闭上传选择" />
        <div className="h5-upload-head">
          <h2>上传选择</h2>
        </div>
        <div className="h5-upload-recents">
          <button className="h5-upload-camera" onClick={onOpenCamera}>
            <CameraIcon />
            <span>相机</span>
          </button>
          <button className="h5-upload-thumb" onClick={onOpenAlbum}>
            <span className="h5-upload-album-label">全部照片</span>
          </button>
          <button className="h5-upload-thumb" onClick={onOpenFile}>
            <span className="h5-upload-album-label">选择文件</span>
          </button>
        </div>
        {pendingUpload ? (
          <div className="h5-upload-selected">
            {pendingUpload.previewUrl ? (
              <img src={pendingUpload.previewUrl} alt={pendingUpload.fileName} />
            ) : (
              <span className="h5-upload-selected-icon"><FileIcon /></span>
            )}
            <div className="h5-upload-selected-copy">
              <strong>{pendingUpload.fileName}</strong>
              <span>{pendingUpload.fileSizeText}</span>
            </div>
            <div className="h5-upload-selected-actions">
              <button type="button" onClick={onClearPendingUpload}>取消</button>
              <button type="button" onClick={onConfirmUpload}>上传</button>
            </div>
          </div>
        ) : null}
      </section>
    </div>
  );
}
