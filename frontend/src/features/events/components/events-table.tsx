import { ApiError } from '@/lib/api-client';
import { useEvents } from '../events-hooks';
import { type AccessEvent } from '../events-types';

const timeFormatter = new Intl.DateTimeFormat('pl-PL', {
  dateStyle: 'short',
  timeStyle: 'medium',
});

const formatTime = (iso: string): string => timeFormatter.format(new Date(iso));

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

export const EventsTable = () => {
  const eventsQuery = useEvents();

  if (eventsQuery.isPending) return <p className="muted">Ładowanie historii…</p>;

  if (eventsQuery.isError) {
    const { error } = eventsQuery;
    const message = error instanceof ApiError ? error.message : 'Nie udało się pobrać historii.';
    return <p className="alert alert-error">{message}</p>;
  }

  const { data, total } = eventsQuery.data;

  return (
    <div className="card">
      <div className="card-head">
        <h2>Historia wykryć</h2>
        <span className="badge">{total}</span>
        <span className="live-dot" title="Odświeża się na żywo co 5 s" />
      </div>
      {data.length === 0 ? (
        <p className="muted">Brak wykryć. Detector jeszcze nic nie zgłosił.</p>
      ) : (
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
            {data.map((event) => (
              <EventRow key={event.id} event={event} />
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};
