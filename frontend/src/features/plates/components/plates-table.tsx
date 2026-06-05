import { useState } from 'react';
import { ApiError } from '@/lib/api-client';
import { useDeletePlate, usePlates, useUpdatePlate } from '../plates-hooks';
import { type Plate } from '../plates-types';

const PlateRow = ({ plate }: { plate: Plate }) => {
  const [editing, setEditing] = useState(false);
  const [label, setLabel] = useState(plate.label ?? '');
  const updatePlate = useUpdatePlate();
  const deletePlate = useDeletePlate();

  const handleSave = (): void => {
    const trimmed = label.trim();
    updatePlate.mutate(
      { code: plate.code, input: { code: plate.code, label: trimmed === '' ? null : trimmed } },
      {
        onSuccess: () => {
          setEditing(false);
        },
      },
    );
  };

  const handleCancel = (): void => {
    setLabel(plate.label ?? '');
    setEditing(false);
  };

  return (
    <tr>
      <td className="mono">{plate.code}</td>
      <td>
        {editing ? (
          <input
            className="input"
            value={label}
            onChange={(event) => {
              setLabel(event.target.value);
            }}
            placeholder="Etykieta"
          />
        ) : (
          plate.label ?? <span className="muted">—</span>
        )}
      </td>
      <td className="actions">
        {editing ? (
          <>
            <button type="button" className="btn btn-sm" onClick={handleSave} disabled={updatePlate.isPending}>
              {updatePlate.isPending ? 'Zapisywanie…' : 'Zapisz'}
            </button>
            <button type="button" className="btn btn-sm btn-ghost" onClick={handleCancel}>
              Anuluj
            </button>
          </>
        ) : (
          <>
            <button
              type="button"
              className="btn btn-sm btn-ghost"
              onClick={() => {
                setEditing(true);
              }}
            >
              Edytuj
            </button>
            <button
              type="button"
              className="btn btn-sm btn-danger"
              onClick={() => {
                deletePlate.mutate(plate.code);
              }}
              disabled={deletePlate.isPending}
            >
              Usuń
            </button>
          </>
        )}
      </td>
    </tr>
  );
};

export const PlatesTable = () => {
  const platesQuery = usePlates();

  if (platesQuery.isPending) return <p className="muted">Ładowanie listy…</p>;

  if (platesQuery.isError) {
    const { error } = platesQuery;
    const message = error instanceof ApiError ? error.message : 'Nie udało się pobrać listy tablic.';
    return <p className="alert alert-error">{message}</p>;
  }

  const { data, total } = platesQuery.data;

  return (
    <div className="card">
      <div className="card-head">
        <h2>Whitelist tablic</h2>
        <span className="badge">{total}</span>
      </div>
      {data.length === 0 ? (
        <p className="muted">Brak tablic na whiteliście. Dodaj pierwszą po prawej.</p>
      ) : (
        <table className="table">
          <thead>
            <tr>
              <th>Kod</th>
              <th>Etykieta</th>
              <th className="actions-head">Akcje</th>
            </tr>
          </thead>
          <tbody>
            {data.map((plate) => (
              <PlateRow key={plate.code} plate={plate} />
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};
