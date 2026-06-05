import { useState } from 'react';
import { EventsFilters } from '@/features/events/components/events-filters';
import { EventsTable } from '@/features/events/components/events-table';
import { EMPTY_FILTERS, type EventFilters } from '@/features/events/events-types';

const EventsPage = () => {
  const [filters, setFilters] = useState<EventFilters>(EMPTY_FILTERS);

  return (
    <div className="page">
      <EventsFilters filters={filters} onChange={setFilters} />
      <EventsTable filters={filters} />
    </div>
  );
};

export default EventsPage;
