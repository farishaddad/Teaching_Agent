/**
 * Auth Callback — exchanges the Cognito authorization code for tokens
 * Simple version that displays the auth code for API testing
 */

import { useEffect, useState } from 'react';

const API_BASE = import.meta.env.VITE_API_URL || '';

export default function AuthCallback() {
  const [status, setStatus] = useState<'loading' | 'success' | 'error'>('loading');
  const [message, setMessage] = useState('Completing sign-in…');
  const [token, setToken] = useState('');

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const code = params.get('code');
    const error = params.get('error');

    if (error) {
      setStatus('error');
      setMessage(`Login failed: ${error}`);
      return;
    }

    if (!code) {
      setStatus('error');
      setMessage('No authorization code received.');
      return;
    }

    // Exchange code for tokens via backend
    fetch(`${API_BASE}/api/auth/callback`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({
        code,
        redirect_uri: import.meta.env.VITE_REDIRECT_URI || 'http://localhost:5173/auth/callback',
      }),
    })
      .then(async (res) => {
        if (res.ok) {
          const data = await res.json();
          setStatus('success');
          setToken(data.access_token || '');
          setMessage('✅ Logged in successfully!');
          // Redirect to home after 2s
          setTimeout(() => { window.location.href = '/'; }, 2000);
        } else {
          const err = await res.text();
          setStatus('error');
          setMessage(`Auth failed: ${res.status} — ${err}`);
        }
      })
      .catch((err) => {
        setStatus('error');
        setMessage(`Network error: ${err.message}. API_BASE=${API_BASE}`);
      });
  }, []);

  return (
    <div className="flex items-center justify-center h-screen bg-gray-50">
      <div className="bg-white rounded-xl shadow-lg p-8 max-w-md w-full text-center">
        {status === 'loading' && (
          <>
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto mb-4"></div>
            <p className="text-gray-600">{message}</p>
          </>
        )}
        {status === 'success' && (
          <>
            <p className="text-2xl mb-2">✅</p>
            <p className="text-gray-900 font-medium">{message}</p>
            <p className="text-xs text-gray-400 mt-2">Redirecting...</p>
          </>
        )}
        {status === 'error' && (
          <>
            <p className="text-2xl mb-2">❌</p>
            <p className="text-red-600 text-sm">{message}</p>
            <a href="/" className="text-blue-600 text-sm mt-4 block hover:underline">← Go home</a>
          </>
        )}
      </div>
    </div>
  );
}
