import { useQuery } from '@tanstack/react-query';
import { eventsApi, type ListParams } from './events-api';

export const eventsKeys = {
  all: ['events'] as const,
  list: (params: ListParams) => [...eventsKeys.all, 'list', params] as const,
};

export const useEvents = (params: ListParams = {}) =>
  useQuery({
    queryKey: eventsKeys.list(params),
    queryFn: () => eventsApi.list(params),
    // Live feed: poll the backend so new detections appear automatically.
    refetchInterval: 5000,
  });
