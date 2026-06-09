import { type SyntheticEvent, useState } from 'react';
import { ApiError } from '@/lib/api-client';
import { useCreatePlate } from '../plates-hooks';

export const AddPlateForm = () => {
  const [code, setCode] = useState('');
  const [label, setLabel] = useState('');
  const createPlate = useCreatePlate();

  const handleSubmit = (event: SyntheticEvent): void => {
    event.preventDefault();
    const trimmedLabel = label.trim();
    createPlate.mutate(
      { code: code.trim(), label: trimmedLabel === '' ? null : trimmedLabel },
      {
        onSuccess: () => {
          setCode('');
          setLabel('');
        },
      },
    );
  };

  const { error } = createPlate;
  let errorMessage: string | null = null;
  if (error instanceof ApiError) {
    errorMessage = error.message;
  } else if (error) {
    errorMessage = 'Nie udało się dodać tablicy.';
  }

  return (
    <form className="card form" onSubmit={handleSubmit}>
      <h2>Dodaj tablicę</h2>

      <div className="field">
        <label htmlFor="plate-code">Kod tablicy</label>
        <input
          id="plate-code"
          className="input"
          value={code}
          onChange={(event) => {
            setCode(event.target.value.toUpperCase());
          }}
          placeholder="np. WA12345"
          minLength={3}
          maxLength={10}
          autoComplete="off"
          required
        />
      </div>

      <div className="field">
        <label htmlFor="plate-label">Etykieta (opcjonalnie)</label>
        <input
          id="plate-label"
          className="input"
          value={label}
          onChange={(event) => {
            setLabel(event.target.value);
          }}
          placeholder="np. Auto firmowe"
          autoComplete="off"
        />
      </div>

      {errorMessage ? <p className="alert alert-error">{errorMessage}</p> : null}

      <button type="submit" className="btn btn-primary" disabled={createPlate.isPending}>
        {createPlate.isPending ? 'Dodawanie…' : 'Dodaj do whitelisty'}
      </button>
    </form>
  );
};
