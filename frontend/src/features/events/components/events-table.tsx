import { useEffect, useRef } from 'react';
import { ApiError } from '@/lib/api-client';
import { useDebouncedValue } from '@/lib/use-debounced-value';
import { useInfiniteEvents } from '../events-hooks';
import { type AccessEvent, type EventFilters } from '../events-types';

const timeFormatter = new Intl.DateTimeFormat('pl-PL', {
  dateStyle: 'short',
  timeStyle: 'medium',
});

const formatTime = (iso: string): string => timeFormatter.format(new Date(iso));

/** Drop duplicate ids that offset-pagination can produce when new rows arrive. */
const dedupeById = (events: AccessEvent[]): AccessEvent[] => {
  const seen = new Set<string>();
  return events.filter((event) => {
    if (seen.has(event.id)) return false;
    seen.add(event.id);
    return true;
  });
};

const EventRow = ({ event }: { event: AccessEvent }) => (
  <tr>
    <td className="mono">{event.code}</td>
    <td>
      {event.allowed ? (
        <span className="badge badge-allowed">Dozwolona</span>
      ) : (
        <span className="badge badge-denied">Odrzucona</span>
      )}
    </td>
    <td>{event.label ?? <span className="muted">—</span>}</td>
    <td className="muted">{formatTime(event.created_at)}</td>
  </tr>
);

export const EventsTable = ({ filters }: { filters: EventFilters }) => {
  const debouncedFilters = useDebouncedValue(filters, 300);
  const eventsQuery = useInfiniteEvents(debouncedFilters);
  const { fetchNextPage, hasNextPage, isFetchingNextPage } = eventsQuery;
  const sentinelRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    const node = sentinelRef.current;
    if (!node) return;
    const observer = new IntersectionObserver((entries) => {
      for (const entry of entries) {
        if (entry.isIntersecting && hasNextPage && !isFetchingNextPage) {
          fetchNextPage();
        }
      }
    });
    observer.observe(node);
    return () => {
      observer.disconnect();
    };
  }, [fetchNextPage, hasNextPage, isFetchingNextPage]);

  if (eventsQuery.isPending) return <p className="muted">Ładowanie historii…</p>;

  if (eventsQuery.isError) {
    const { error } = eventsQuery;
    const message =
      error instanceof ApiError ? error.message : 'Nie udało się pobrać historii.';
    return <p className="alert alert-error">{message}</p>;
  }

  const rows = dedupeById(eventsQuery.data.pages.flatMap((page) => page.data));
  const total = eventsQuery.data.pages[0].total;

  let footer = `To wszystkie wyniki (${String(total)})`;
  if (isFetchingNextPage) {
    footer = 'Ładowanie kolejnych…';
  } else if (hasNextPage) {
    footer = 'Przewiń, aby załadować więcej';
  }

  return (
    <div className="card">
      <div className="card-head">
        <h2>Historia wykryć</h2>
        <span className="badge">{total}</span>
        <span className="live-dot" title="Odświeża się na żywo co 5 s" />
      </div>
      {rows.length === 0 ? (
        <p className="muted">Brak wykryć dla podanych filtrów.</p>
      ) : (
        <>
          <table className="table">
            <thead>
              <tr>
                <th>Kod</th>
                <th>Status</th>
                <th>Etykieta</th>
                <th>Czas</th>
              </tr>
            </thead>
            <tbody>
              {rows.map((event) => (
                <EventRow key={event.id} event={event} />
              ))}
            </tbody>
          </table>
          <div ref={sentinelRef} className="scroll-sentinel">
            <span className="muted">{footer}</span>
          </div>
        </>
      )}
    </div>
  );
};
