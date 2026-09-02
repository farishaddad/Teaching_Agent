/**
 * RequireInstructor — route guard for instructor-only areas (e.g. /admin).
 *
 * Uses the cookie-based session (`useAuth`) to gate access:
 *  - while the session is loading → shows a spinner
 *  - not authenticated → redirects to /login
 *  - authenticated but not an instructor → shows an "access denied" notice
 *  - instructor → renders the protected content
 *
 * This prevents unauthenticated users from hitting the admin API and seeing a
 * raw 401, and gives non-instructors a clear message instead of a broken page.
 */

import type { ReactNode } from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';

export default function RequireInstructor({ children }: { children: ReactNode }) {
  const { isLoading, isAuthenticated, isInstructor } = useAuth();

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-screen bg-gray-50">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600" />
        <span className="ml-3 text-gray-500">Checking access…</span>
      </div>
    );
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  if (!isInstructor) {
    return (
      <div className="flex items-center justify-center h-screen bg-gray-50 px-4">
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-8 max-w-md text-center">
          <p className="text-3xl mb-3">🔒</p>
          <h1 className="text-lg font-semibold text-gray-900 mb-1">
            Instructor access required
          </h1>
          <p className="text-sm text-gray-500">
            Your account isn’t authorized to view the admin dashboard. Contact
            your instructor if you believe this is a mistake.
          </p>
          <a href="/" className="text-blue-600 text-sm mt-4 inline-block hover:underline">
            ← Back to home
          </a>
        </div>
      </div>
    );
  }

  return <>{children}</>;
}
