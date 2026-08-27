/**
 * AuthCallback — handles the Cognito Hosted UI redirect.
 *
 * Cognito redirects here after successful authentication with:
 *   /auth/callback?code=<authorization_code>&state=<state>
 *
 * This component extracts the code and delegates to useAuth.handleCallback,
 * which POSTs to the backend to exchange the code for tokens (httpOnly cookies).
 */

import { useEffect, useRef } from 'react';
import { useSearchParams } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';

export default function AuthCallback() {
  const [searchParams] = useSearchParams();
  const { handleCallback } = useAuth();
  const handled = useRef(false);

  useEffect(() => {
    // Guard against double-invocation in React Strict Mode
    if (handled.current) return;
    handled.current = true;

    const code = searchParams.get('code');
    const error = searchParams.get('error');
    const errorDescription = searchParams.get('error_description');

    if (error) {
      // Cognito returned an explicit error (e.g., access_denied)
      console.error('Cognito auth error:', error, errorDescription);
      window.location.replace(`/login?error=${encodeURIComponent(errorDescription ?? error)}`);
      return;
    }

    if (!code) {
      window.location.replace('/login');
      return;
    }

    void handleCallback(code);
  }, [handleCallback, searchParams]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
      <div className="text-center">
        <svg
          className="animate-spin mx-auto h-10 w-10 text-indigo-600 mb-4"
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          aria-hidden="true"
        >
          <circle
            className="opacity-25"
            cx="12"
            cy="12"
            r="10"
            stroke="currentColor"
            strokeWidth="4"
          />
          <path
            className="opacity-75"
            fill="currentColor"
            d="M4 12a8 8 0 018-8v4l3-3-3-3v4a8 8 0 00-8 8h4z"
          />
        </svg>
        <p className="text-gray-600 text-sm font-medium">Completing sign-in…</p>
      </div>
    </div>
  );
}
