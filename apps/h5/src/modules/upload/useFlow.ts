import { useCallback } from 'react';
import type { InteractionMessage } from '../input_flow/h5Interaction';
import { safeCreateObjectURL } from '../../utils/browserSafe';
import { uploadOriginalFile } from './api';

type AppendMessage = (message: Omit<InteractionMessage, 'id' | 'createdAt'>) => void;

type UseUploadFlowOptions = {
  appendMessage: AppendMessage;
  appendToCentralInput: (text: string) => void;
  showToast: (message: string) => void;
  closeUpload: () => void;
};

export function useUploadFlow({
  appendMessage,
  appendToCentralInput,
  showToast,
  closeUpload,
}: UseUploadFlowOptions) {
  const uploadSelectedFile = useCallback(async (file: File, kind: 'image' | 'file') => {
    showToast('正在上传文件...');
    try {
      const uploadedFile = await uploadOriginalFile(file);
      const action = kind === 'image' ? '图片' : '文件';
      const previewUrl = kind === 'image' ? safeCreateObjectURL(file) : undefined;
      appendMessage({
        type: kind,
        action,
        content: `已上传：${uploadedFile.filename}`,
        fileName: uploadedFile.filename,
        fileSize: uploadedFile.file_size,
        dataUrl: previewUrl,
      });
      appendToCentralInput(
        `已上传${kind === 'image' ? '图片' : '文件'}：${uploadedFile.filename}，文件编号：${uploadedFile.upload_id}。请补充业务说明。`,
      );
      showToast('上传成功，原件已保存。');
    } catch (error) {
      const message = error instanceof Error && error.message.trim() ? error.message.trim() : '上传失败。';
      appendMessage({
        type: 'status',
        action: kind === 'image' ? '图片' : '文件',
        content: `上传失败：${message}`,
      });
      showToast(message);
    }
  }, [appendMessage, appendToCentralInput, showToast]);

  const handleImageInput = useCallback(async (fileList: FileList | null) => {
    const file = fileList?.[0];
    closeUpload();
    if (file) await uploadSelectedFile(file, 'image');
  }, [closeUpload, uploadSelectedFile]);

  const handleFileInput = useCallback(async (fileList: FileList | null) => {
    const file = fileList?.[0];
    closeUpload();
    if (file) await uploadSelectedFile(file, 'file');
  }, [closeUpload, uploadSelectedFile]);

  return { handleImageInput, handleFileInput };
}
