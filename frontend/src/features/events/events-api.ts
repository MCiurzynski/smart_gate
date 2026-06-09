import { apiClient } from '@/lib/api-client';
import { type EventList } from './events-types';

/** Server-side query params for GET /events/ (snake_case maps to backend). */
export interface EventQuery {
  offset?: number;
  limit?: number;
  code?: string;
  label?: string;
  allowed?: boolean;
  dateFrom?: string;
  dateTo?: string;
}

export const eventsApi = {
  list: (query: EventQuery = {}): Promise<EventList> => {
    const params = new URLSearchParams();
    params.set('offset', String(query.offset ?? 0));
    params.set('limit', String(query.limit ?? 50));
    if (query.code) params.set('code', query.code);
    if (query.label) params.set('label', query.label);
    if (query.allowed !== undefined) params.set('allowed', String(query.allowed));
    if (query.dateFrom) params.set('date_from', query.dateFrom);
    if (query.dateTo) params.set('date_to', query.dateTo);
    return apiClient.get<EventList>(`/events/?${params.toString()}`);
  },
};
