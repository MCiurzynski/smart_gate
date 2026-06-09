import { Component, type ErrorInfo, type ReactNode } from 'react';

interface Props {
  children: ReactNode;
}

interface State {
  error: Error | null;
}

/** Catches render-time errors in the routed page tree. */
export class ErrorBoundary extends Component<Props, State> {
  state: State = { error: null };

  static getDerivedStateFromError(error: Error): State {
    return { error };
  }

  componentDidCatch(error: Error, info: ErrorInfo): void {
    console.error('Nieobsłużony błąd UI:', error, info.componentStack);
  }

  handleReset = (): void => {
    this.setState({ error: null });
  };

  render(): ReactNode {
    const { error } = this.state;
    if (error) {
      return (
        <div className="alert alert-error">
          <strong>Coś poszło nie tak.</strong>
          <p>{error.message}</p>
          <button type="button" className="btn btn-sm" onClick={this.handleReset}>
            Spróbuj ponownie
          </button>
        </div>
      );
    }
    return this.props.children;
  }
}
