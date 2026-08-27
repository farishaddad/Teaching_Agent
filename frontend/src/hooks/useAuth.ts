/**
 * useAuth — authentication state management hook.
 *
 * Responsibilities:
 * - Read the current user from the /api/auth/me endpoint (cookie-based session).
 * - Initiate the Cognito Hosted UI login redirect (PKCE auth code flow).
 * - Handle the /auth/callback redirect — exchange the auth code for tokens.
 * - Provide a logout function that clears cookies and redirects to Cognito logout.
 *
 * Token storage: all tokens live in httpOnly cookies set by the backend.
 * This hook never touches localStorage and never reads raw JWTs.
 */

import { useCallback, useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

// ── Types ─────────────────────────────────────────────────────────────────────

export interface AuthUser {
  id: string;
  email: string;
  givenName?: string;
  familyName?: string;
  cohort?: string;
  enrollmentDate?: string;
  groups: string[];
}

export interface AuthState {
  user: AuthUser | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  isInstructor: boolean;
  error: string | null;
}

// ── Constants (injected from environment) ─────────────────────────────────────

const API_BASE = import.meta.env.VITE_API_URL ?? 'http://localhost:8000';
const COGNITO_DOMAIN = import.meta.env.VITE_COGNITO_DOMAIN ?? '';
const COGNITO_CLIENT_ID = import.meta.env.VITE_COGNITO_CLIENT_ID ?? '';
const COGNITO_REDIRECT_URI = import.meta.env.VITE_COGNITO_REDIRECT_URI ?? `${window.location.origin}/auth/callback`;

// ── PKCE helpers ──────────────────────────────────────────────────────────────

/** Generate a cryptographically random code verifier for PKCE. */
function generateCodeVerifier(): string {
  const array = new Uint8Array(96);
  window.crypto.getRandomValues(array);
  return btoa(String.fromCharCode(...array))
    .replace(/\+/g, '-')
    .replace(/\//g, '_')
    .replace(/=+$/, '');
}

/** Derive the code challenge (S256) from the verifier. */
async function generateCodeChallenge(verifier: string): Promise<string> {
  const encoder = new TextEncoder();
  const data = encoder.encode(verifier);
  const digest = await window.crypto.subtle.digest('SHA-256', data);
  return btoa(String.fromCharCode(...new Uint8Array(digest)))
    .replace(/\+/g, '-')
    .replace(/\//g, '_')
    .replace(/=+$/, '');
}

// ── Core API calls ────────────────────────────────────────────────────────────

/** Fetch the currently authenticated user from the backend (cookie session). */
async function fetchCurrentUser(): Promise<AuthUser | null> {
  const response = await fetch(`${API_BASE}/api/auth/me`, {
    credentials: 'include',
  });
  if (response.status === 401) return null;
  if (!response.ok) throw new Error(`Failed to fetch user: ${response.status}`);
  return response.json();
}

/**
 * Exchange an authorization code for tokens via the backend callback endpoint.
 * The backend sets httpOnly cookies and returns the user profile.
 */
async function exchangeCodeForTokens(
  code: string,
  codeVerifier: string,
): Promise<AuthUser> {
  const response = await fetch(`${API_BASE}/api/auth/callback`, {
    method: 'POST',
    credentials: 'include',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ code, code_verifier: codeVerifier, redirect_uri: COGNITO_REDIRECT_URI }),
  });
  if (!response.ok) {
    const body = await response.json().catch(() => ({}));
    throw new Error(body.detail ?? `Auth callback failed (${response.status})`);
  }
  return response.json();
}

/** Call the backend logout endpoint to clear cookies and revoke refresh token. */
async function callLogoutEndpoint(): Promise<void> {
  await fetch(`${API_BASE}/api/auth/logout`, {
    method: 'POST',
    credentials: 'include',
  });
}

// ── Hook ──────────────────────────────────────────────────────────────────────

export function useAuth(): AuthState & {
  login: () => Promise<void>;
  logout: () => Promise<void>;
  handleCallback: (code: string) => Promise<void>;
} {
  const navigate = useNavigate();

  const [state, setState] = useState<AuthState>({
    user: null,
    isLoading: true,
    isAuthenticated: false,
    isInstructor: false,
    error: null,
  });

  // ── Load session on mount ────────────────────────────────────────────────

  useEffect(() => {
    let cancelled = false;

    async function loadUser() {
      try {
        const user = await fetchCurrentUser();
        if (!cancelled) {
          setState({
            user,
            isLoading: false,
            isAuthenticated: user !== null,
            isInstructor: user?.groups.includes('instructors') ?? false,
            error: null,
          });
        }
      } catch (err) {
        if (!cancelled) {
          setState({
            user: null,
            isLoading: false,
            isAuthenticated: false,
            isInstructor: false,
            error: err instanceof Error ? err.message : 'Failed to load session',
          });
        }
      }
    }

    void loadUser();
    return () => {
      cancelled = true;
    };
  }, []);

  // ── Login — redirect to Cognito Hosted UI with PKCE ──────────────────────

  const login = useCallback(async () => {
    const verifier = generateCodeVerifier();
    const challenge = await generateCodeChallenge(verifier);

    // Persist verifier in sessionStorage for use in handleCallback
    sessionStorage.setItem('pkce_verifier', verifier);

    const params = new URLSearchParams({
      response_type: 'code',
      client_id: COGNITO_CLIENT_ID,
      redirect_uri: COGNITO_REDIRECT_URI,
      scope: 'openid email profile',
      code_challenge_method: 'S256',
      code_challenge: challenge,
    });

    window.location.href = `${COGNITO_DOMAIN}/oauth2/authorize?${params.toString()}`;
  }, []);

  // ── Callback — exchange code for tokens ──────────────────────────────────

  const handleCallback = useCallback(
    async (code: string) => {
      setState((prev) => ({ ...prev, isLoading: true, error: null }));

      const verifier = sessionStorage.getItem('pkce_verifier');
      if (!verifier) {
        setState((prev) => ({
          ...prev,
          isLoading: false,
          error: 'PKCE verifier missing — please try logging in again.',
        }));
        return;
      }

      sessionStorage.removeItem('pkce_verifier');

      try {
        const user = await exchangeCodeForTokens(code, verifier);
        setState({
          user,
          isLoading: false,
          isAuthenticated: true,
          isInstructor: user.groups.includes('instructors'),
          error: null,
        });
        navigate('/', { replace: true });
      } catch (err) {
        setState({
          user: null,
          isLoading: false,
          isAuthenticated: false,
          isInstructor: false,
          error: err instanceof Error ? err.message : 'Login failed',
        });
        navigate('/login', { replace: true });
      }
    },
    [navigate],
  );

  // ── Logout ────────────────────────────────────────────────────────────────

  const logout = useCallback(async () => {
    try {
      await callLogoutEndpoint();
    } finally {
      setState({
        user: null,
        isLoading: false,
        isAuthenticated: false,
        isInstructor: false,
        error: null,
      });

      // Also redirect to Cognito to clear the Hosted UI session
      const params = new URLSearchParams({
        client_id: COGNITO_CLIENT_ID,
        logout_uri: window.location.origin,
      });
      window.location.href = `${COGNITO_DOMAIN}/logout?${params.toString()}`;
    }
  }, []);

  return { ...state, login, logout, handleCallback };
}
