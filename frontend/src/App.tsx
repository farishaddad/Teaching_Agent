/**
 * Teaching Agent Frontend — App Root
 *
 * Route structure:
 *   /              → Student chat (protected)
 *   /login         → Login page (public)
 *   /auth/callback → Cognito redirect handler (public)
 *   /admin/*       → Instructor dashboard (protected, instructor-only)
 *   /tutorial      → Tutorial module (protected)
 */

import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import AdminLayout from './components/admin/AdminLayout';
import AuthCallback from './components/AuthCallback';
import Login from './components/Login';
import { useAuth } from './hooks/useAuth';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 30_000, // 30 s cache
      retry: 1,
    },
  },
});

// ── Route guards ──────────────────────────────────────────────────────────────

/** Redirect unauthenticated users to /login. */
function RequireAuth({ children }: { children: React.ReactNode }) {
  const { isAuthenticated, isLoading } = useAuth();

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <svg
          className="animate-spin h-8 w-8 text-indigo-600"
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          aria-label="Loading"
        >
          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4l3-3-3-3v4a8 8 0 00-8 8h4z" />
        </svg>
      </div>
    );
  }

  return isAuthenticated ? <>{children}</> : <Navigate to="/login" replace />;
}

/** Redirect authenticated users away from /login. */
function RedirectIfAuthenticated({ children }: { children: React.ReactNode }) {
  const { isAuthenticated, isLoading } = useAuth();

  if (isLoading) return null;

  return isAuthenticated ? <Navigate to="/" replace /> : <>{children}</>;
}

// ── App ───────────────────────────────────────────────────────────────────────

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Routes>
          {/* Public routes */}
          <Route
            path="/login"
            element={
              <RedirectIfAuthenticated>
                <Login />
              </RedirectIfAuthenticated>
            }
          />
          <Route path="/auth/callback" element={<AuthCallback />} />

          {/* Protected: student chat */}
          <Route
            path="/"
            element={
              <RequireAuth>
                <div className="min-h-screen bg-gray-50 flex items-center justify-center">
                  <p className="text-gray-500">Student Chat — coming soon</p>
                </div>
              </RequireAuth>
            }
          />

          {/* Protected: admin */}
          <Route
            path="/admin/*"
            element={
              <RequireAuth>
                <AdminLayout />
              </RequireAuth>
            }
          />

          {/* Protected: tutorial */}
          <Route
            path="/tutorial"
            element={
              <RequireAuth>
                <div className="min-h-screen bg-gray-50 flex items-center justify-center">
                  <p className="text-gray-500">Tutorial — coming soon</p>
                </div>
              </RequireAuth>
            }
          />

          {/* Fallback */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  );
}
