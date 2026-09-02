/**
 * Auth Callback — exchanges the Cognito authorization code for tokens.
 *
 * Delegates the exchange to `useAuth().handleCallback`, which reads the PKCE
 * verifier stored at login (`sessionStorage['pkce_verifier']`), sends it to
 * the backend `/api/auth/callback` (as `code_verifier`), and uses the same
 * `VITE_COGNITO_REDIRECT_URI` the login redirect used. Doing the exchange here
 * inline (without the verifier) breaks the PKCE flow, so this component is a
 * thin UI wrapper over the hook.
 */

import { useEffect, useRef } from 'react';
import { useAuth } from '../hooks/useAuth';

export default function AuthCallback() {
  const { handleCallback, isLoading, error } = useAuth();
  // Guard against double-invocation (React 18 StrictMode mounts effects twice);
  // the PKCE verifier is single-use, so the exchange must run exactly once.
  const startedRef = useRef(false);

  useEffect(() => {
    if (startedRef.current) return;
    startedRef.current = true;

    const params = new URLSearchParams(window.location.search);
    const code = params.get('code');
    const oauthError = params.get('error');

    if (oauthError || !code) {
      // No code / explicit error — let the hook surface it via `error`, and
      // fall back to the login route.
      void handleCallback('');
      return;
    }

    void handleCallback(code);
  }, [handleCallback]);

  const status: 'loading' | 'error' = error ? 'error' : 'loading';

  return (
    <div className="flex items-center justify-center h-screen bg-gray-50">
      <div className="bg-white rounded-xl shadow-lg p-8 max-w-md w-full text-center">
        {status === 'loading' && (
          <>
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto mb-4"></div>
            <p className="text-gray-600">
              {isLoading ? 'Completing sign-in…' : 'Redirecting…'}
            </p>
          </>
        )}
        {status === 'error' && (
          <>
            <p className="text-2xl mb-2">❌</p>
            <p className="text-red-600 text-sm">{error}</p>
            <a href="/login" className="text-blue-600 text-sm mt-4 block hover:underline">
              ← Try logging in again
            </a>
          </>
        )}
      </div>
    </div>
  );
}
