type RequestOptions = {
  method?: 'GET' | 'POST';
  body?: unknown;
  errorMessage?: string;
};

export function buildRequestUrl(endpoint: string): string {
  const apiBase = (import.meta.env.VITE_API_BASE || '').trim().replace(/\/+$/, '');
  if (!apiBase) {
    return endpoint;
  }

  const normalizedEndpoint = endpoint.startsWith('/') ? endpoint : `/${endpoint}`;
  return `${apiBase}${normalizedEndpoint}`;
}

export async function requestJSON<T>(
  url: string,
  options: RequestOptions = {}
): Promise<T> {
  const headers: Record<string, string> = {};
  if (options.body) {
    headers['Content-Type'] = 'application/json';
  }

  const response = await fetch(buildRequestUrl(url), {
    method: options.method || 'POST',
    headers,
    ...(options.body ? { body: JSON.stringify(options.body) } : {}),
  });

  if (!response.ok) {
    const message = await readSafeErrorMessage(response, options.errorMessage || '请求处理失败');
    throw new Error(message);
  }

  return response.json();
}

async function readSafeErrorMessage(response: Response, fallbackMessage: string): Promise<string> {
  try {
    const body = await response.json() as { detail?: unknown };
    if (typeof body.detail === 'string' && body.detail.trim()) {
      return `${fallbackMessage}：${body.detail.trim()}`;
    }
  } catch {
    // ignore non-JSON response bodies
  }
  return `${fallbackMessage}（HTTP ${response.status}）`;
}
