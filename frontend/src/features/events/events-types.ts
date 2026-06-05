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
