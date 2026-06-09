import { EMPTY_FILTERS, type EventFilters } from '../events-types';

interface Props {
  filters: EventFilters;
  onChange: (filters: EventFilters) => void;
}

export const EventsFilters = ({ filters, onChange }: Props) => {
  const update = (patch: Partial<EventFilters>): void => {
    onChange({ ...filters, ...patch });
  };

  const handleReset = (): void => {
    onChange(EMPTY_FILTERS);
  };

  return (
    <div className="card filters">
      <div className="field">
        <label htmlFor="filter-code">Nr rejestracyjny</label>
        <input
          id="filter-code"
          className="input"
          value={filters.code}
          onChange={(event) => {
            update({ code: event.target.value.toUpperCase() });
          }}
          placeholder="np. WA123"
          autoComplete="off"
        />
      </div>

      <div className="field">
        <label htmlFor="filter-label">Etykieta</label>
        <input
          id="filter-label"
          className="input"
          value={filters.label}
          onChange={(event) => {
            update({ label: event.target.value });
          }}
          placeholder="np. firmowe"
          autoComplete="off"
        />
      </div>

      <div className="field">
        <label htmlFor="filter-status">Status</label>
        <select
          id="filter-status"
          className="input"
          value={filters.status}
          onChange={(event) => {
            update({ status: event.target.value as EventFilters['status'] });
          }}
        >
          <option value="all">Wszystkie</option>
          <option value="allowed">Dozwolone</option>
          <option value="denied">Odrzucone</option>
        </select>
      </div>

      <div className="field">
        <label htmlFor="filter-from">Od</label>
        <input
          id="filter-from"
          type="date"
          className="input"
          value={filters.dateFrom}
          onChange={(event) => {
            update({ dateFrom: event.target.value });
          }}
        />
      </div>

      <div className="field">
        <label htmlFor="filter-to">Do</label>
        <input
          id="filter-to"
          type="date"
          className="input"
          value={filters.dateTo}
          onChange={(event) => {
            update({ dateTo: event.target.value });
          }}
        />
      </div>

      <button type="button" className="btn btn-ghost" onClick={handleReset}>
        Wyczyść
      </button>
    </div>
  );
};
