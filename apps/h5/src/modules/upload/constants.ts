export const UPLOAD_MAX_FILE_SIZE = 10 * 1024 * 1024;

export const UPLOAD_ALLOWED_EXTENSIONS = ['jpg', 'jpeg', 'png', 'heic', 'heif', 'pdf'] as const;

export const UPLOAD_ALLOWED_MIME_TYPES = [
  'image/jpeg',
  'image/jpg',
  'image/pjpeg',
  'image/png',
  'image/x-png',
  'image/heic',
  'image/heif',
  'image/heic-sequence',
  'image/heif-sequence',
  'application/pdf',
] as const;

export const UPLOAD_ALLOWED_DESCRIPTION = '仅支持 jpg、jpeg、png、heic、heif、pdf，单个文件不超过 10MB。';
