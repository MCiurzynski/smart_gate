import { apiClient } from '@/lib/api-client';
import {
  type CheckResult,
  type PlateInput,
  type PlateList,
  type PlateWithId,
} from './plates-types';

export interface ListParams {
  offset?: number;
  limit?: number;
}

/**
 * Thin, typed wrapper over the backend /api/plates endpoints. Note the trailing
 * slash on the collection routes — FastAPI's router defines them that way.
 */
export const platesApi = {
  list: ({ offset = 0, limit = 100 }: ListParams = {}): Promise<PlateList> => {
    const query = new URLSearchParams({ offset: String(offset), limit: String(limit) });
    return apiClient.get<PlateList>(`/plates/?${query.toString()}`);
  },

  create: (input: PlateInput): Promise<PlateWithId> =>
    apiClient.post<PlateWithId>('/plates/', input),

  update: (code: string, input: PlateInput): Promise<PlateWithId> =>
    apiClient.patch<PlateWithId>(`/plates/${encodeURIComponent(code)}`, input),

  remove: (code: string): Promise<{ message: string }> =>
    apiClient.delete<{ message: string }>(`/plates/${encodeURIComponent(code)}`),

  check: (code: string): Promise<CheckResult> =>
    apiClient.get<CheckResult>(`/plates/${encodeURIComponent(code)}`),
};
