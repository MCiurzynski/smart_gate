import { apiClient } from '@/lib/api-client';
import { type EventList } from './events-types';

export interface ListParams {
  offset?: number;
  limit?: number;
}

export const eventsApi = {
  list: ({ offset = 0, limit = 50 }: ListParams = {}): Promise<EventList> => {
    const query = new URLSearchParams({ offset: String(offset), limit: String(limit) });
    return apiClient.get<EventList>(`/events/?${query.toString()}`);
  },
};
