import { SearchPage } from './pages/SearchPage';
import { ErrorBoundary } from './components/ErrorBoundary';

function App() {
  return (
    <ErrorBoundary>
      <SearchPage />
    </ErrorBoundary>
  );
}

export default App;
