import { env } from '@/config/env';

/** Error thrown for any non-2xx response, carrying the backend's detail. */
export class ApiError extends Error {
  readonly status: number;
  readonly detail: unknown;

  constructor(status: number, message: string, detail?: unknown) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
    this.detail = detail;
  }
}

interface RequestOptions extends Omit<RequestInit, 'body'> {
  body?: unknown;
}

interface ValidationItem {
  msg?: string;
}

/** Turn FastAPI's varied error shapes (string detail, 422 array) into a string. */
const extractMessage = (status: number, detail: unknown): string => {
  if (typeof detail === 'string') return detail;
  if (Array.isArray(detail)) {
    const first = detail[0] as ValidationItem | undefined;
    if (first?.msg) return first.msg;
  }
  return `Żądanie nie powiodło się (status ${String(status)})`;
};

const request = async <T>(path: string, options: RequestOptions = {}): Promise<T> => {
  const { body, headers, ...rest } = options;

  const requestHeaders = new Headers(headers);
  if (body !== undefined && !requestHeaders.has('Content-Type')) {
    requestHeaders.set('Content-Type', 'application/json');
  }

  const response = await fetch(`${env.apiBaseUrl}${path}`, {
    ...rest,
    headers: requestHeaders,
    body: body === undefined ? undefined : JSON.stringify(body),
  });

  const isJson = response.headers.get('content-type')?.includes('application/json') ?? false;
  const payload: unknown = isJson ? await response.json() : await response.text();

  if (!response.ok) {
    const detail =
      isJson && payload !== null && typeof payload === 'object'
        ? (payload as { detail?: unknown }).detail
        : payload;
    throw new ApiError(response.status, extractMessage(response.status, detail), detail);
  }

  return payload as T;
};

export const apiClient = {
  get: <T>(path: string, options?: RequestOptions): Promise<T> =>
    request<T>(path, { ...options, method: 'GET' }),
  post: <T>(path: string, body?: unknown): Promise<T> =>
    request<T>(path, { method: 'POST', body }),
  patch: <T>(path: string, body?: unknown): Promise<T> =>
    request<T>(path, { method: 'PATCH', body }),
  delete: <T>(path: string): Promise<T> =>
    request<T>(path, { method: 'DELETE' }),
};
