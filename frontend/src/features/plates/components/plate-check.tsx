import { type SyntheticEvent, useState } from 'react';
import { ApiError } from '@/lib/api-client';
import { platesApi } from '../plates-api';
import { type CheckResult } from '../plates-types';

type Status =
  | { kind: 'idle' }
  | { kind: 'loading' }
  | { kind: 'allowed'; result: CheckResult }
  | { kind: 'denied'; message: string };

export const PlateCheck = () => {
  const [code, setCode] = useState('');
  const [status, setStatus] = useState<Status>({ kind: 'idle' });

  const handleSubmit = (event: SyntheticEvent): void => {
    event.preventDefault();
    setStatus({ kind: 'loading' });
    platesApi
      .check(code.trim())
      .then((result) => {
        setStatus({ kind: 'allowed', result });
      })
      .catch((error: unknown) => {
        const message = error instanceof ApiError ? error.message : 'Błąd sprawdzania tablicy.';
        setStatus({ kind: 'denied', message });
      });
  };

  return (
    <div className="card form-card">
      <h2>Sprawdź tablicę</h2>
      <p className="muted">Zweryfikuj, czy dany kod znajduje się na whiteliście bramy.</p>

      <form className="inline-form" onSubmit={handleSubmit}>
        <input
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
        <button type="submit" className="btn btn-primary" disabled={status.kind === 'loading'}>
          {status.kind === 'loading' ? 'Sprawdzanie…' : 'Sprawdź'}
        </button>
      </form>

      {status.kind === 'allowed' ? (
        <div className="alert alert-success">
          ✅ <strong className="mono">{status.result.data.code}</strong> jest na whiteliście
          {status.result.data.label ? ` (${status.result.data.label})` : ''}.
        </div>
      ) : null}

      {status.kind === 'denied' ? <div className="alert alert-error">⛔ {status.message}</div> : null}
    </div>
  );
};
