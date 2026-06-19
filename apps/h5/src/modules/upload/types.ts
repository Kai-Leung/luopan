export type UploadFileStoredResponse = {
  upload_id: string;
  filename: string;
  content_type: string;
  file_size: number;
  storage_path: string;
  saved: true;
};
