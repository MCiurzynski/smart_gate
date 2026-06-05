import { keepPreviousData, useInfiniteQuery } from '@tanstack/react-query';
import { eventsApi, type EventQuery } from './events-api';
import { type EventFilters } from './events-types';

const PAGE_SIZE = 50;

/** Map UI filter state to the backend query shape (drops empty values). */
const toQuery = (filters: EventFilters): EventQuery => {
  const code = filters.code.trim();
  const label = filters.label.trim();
  return {
    code: code === '' ? undefined : code,
    label: label === '' ? undefined : label,
    allowed: filters.status === 'all' ? undefined : filters.status === 'allowed',
    dateFrom: filters.dateFrom
      ? new Date(`${filters.dateFrom}T00:00:00`).toISOString()
      : undefined,
    dateTo: filters.dateTo
      ? new Date(`${filters.dateTo}T23:59:59.999`).toISOString()
      : undefined,
  };
};

export const eventsKeys = {
  all: ['events'] as const,
  list: (query: EventQuery) => [...eventsKeys.all, 'list', query] as const,
};

export const useInfiniteEvents = (filters: EventFilters) => {
  const query = toQuery(filters);
  return useInfiniteQuery({
    queryKey: eventsKeys.list(query),
    queryFn: ({ pageParam }) =>
      eventsApi.list({ ...query, offset: pageParam, limit: PAGE_SIZE }),
    initialPageParam: 0,
    getNextPageParam: (lastPage) => {
      const loaded = lastPage.offset + lastPage.data.length;
      return loaded < lastPage.total ? loaded : undefined;
    },
    // Keep the previous results visible while a new filter query loads.
    placeholderData: keepPreviousData,
    // Live feed: poll so new detections appear automatically.
    refetchInterval: 5000,
  });
};
