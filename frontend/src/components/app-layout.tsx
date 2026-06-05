import { Suspense } from 'react';
import { NavLink, Outlet } from 'react-router-dom';
import { ErrorBoundary } from './error-boundary';

const navClass = ({ isActive }: { isActive: boolean }): string =>
  isActive ? 'nav-link active' : 'nav-link';

export const AppLayout = () => (
  <div className="app">
    <header className="app-header">
      <span className="brand">𓈈 Smart Gate</span>
      <nav className="nav">
        <NavLink to="/plates" className={navClass}>
          Whitelist
        </NavLink>
        <NavLink to="/check" className={navClass}>
          Sprawdź tablicę
        </NavLink>
      </nav>
    </header>

    <main className="app-main">
      <ErrorBoundary>
        <Suspense fallback={<p className="muted">Ładowanie…</p>}>
          <Outlet />
        </Suspense>
      </ErrorBoundary>
    </main>
  </div>
);
