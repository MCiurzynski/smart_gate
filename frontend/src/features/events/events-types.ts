/** Mirrors backend `AccessEventRead` (src/events/schemas.py). */
export interface AccessEvent {
  id: string;
  code: string;
  allowed: boolean;
  label: string | null;
  created_at: string;
}

/** Paginated history payload (backend `AccessEventPublic`). */
export interface EventList {
  data: AccessEvent[];
  total: number;
  offset: number;
  limit: number;
}

/** UI filter state (form values), distinct from the server query shape. */
export interface EventFilters {
  code: string;
  label: string;
  status: 'all' | 'allowed' | 'denied';
  dateFrom: string;
  dateTo: string;
}

export const EMPTY_FILTERS: EventFilters = {
  code: '',
  label: '',
  status: 'all',
  dateFrom: '',
  dateTo: '',
};
