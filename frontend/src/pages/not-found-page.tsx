import { Link } from 'react-router-dom';

const NotFoundPage = () => (
  <div className="page page-narrow center">
    <h2>404 — nie znaleziono</h2>
    <p className="muted">Ta strona nie istnieje.</p>
    <Link className="btn btn-primary" to="/plates">
      Wróć do whitelisty
    </Link>
  </div>
);

export default NotFoundPage;
