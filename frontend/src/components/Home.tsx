/**
 * Home — the app's root view.
 *
 * Auth-aware:
 * - While the session is loading, shows a spinner.
 * - Authenticated users get the chat interface with a top nav (Tutorial,
 *   Admin for instructors only, and Logout).
 * - Guests get the splash screen with Tutorial and Login (no Admin — that's
 *   instructor-only and gated server-side anyway).
 */

import { useAuth } from '../hooks/useAuth';
import Chat from './Chat';

export default function Home() {
  const { isLoading, isAuthenticated, isInstructor, user, login, logout } = useAuth();

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-screen bg-gray-50">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600" />
        <span className="ml-3 text-gray-500">Loading…</span>
      </div>
    );
  }

  // ── Guest: splash screen ────────────────────────────────────────────────
  if (!isAuthenticated) {
    return (
      <div className="flex items-center justify-center h-screen bg-gray-50">
        <div className="text-center">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">🤖 Teaching Agent</h1>
          <p className="text-gray-500 mb-6">Agentic AI Course Companion</p>
          <div className="space-x-4">
            <a
              href="/tutorial"
              className="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300"
            >
              Tutorial
            </a>
            <button
              onClick={() => void login()}
              className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700"
            >
              Login
            </button>
          </div>
        </div>
      </div>
    );
  }

  // ── Authenticated: chat interface with top nav ───────────────────────────
  return (
    <div className="flex flex-col h-screen bg-gray-50">
      <header className="flex items-center justify-between px-4 py-3 bg-white border-b border-gray-200">
        <div className="flex items-center gap-2">
          <span className="text-lg font-bold text-gray-900">🤖 Teaching Agent</span>
          <span className="hidden sm:inline text-xs text-gray-400">
            Course Companion
          </span>
        </div>
        <nav className="flex items-center gap-2 text-sm">
          <a
            href="/tutorial"
            className="px-3 py-1.5 text-gray-600 hover:bg-gray-100 rounded-lg font-medium"
          >
            Tutorial
          </a>
          {isInstructor && (
            <a
              href="/admin"
              className="px-3 py-1.5 text-gray-600 hover:bg-gray-100 rounded-lg font-medium"
            >
              Admin
            </a>
          )}
          <span className="hidden sm:inline text-xs text-gray-400 px-2">
            {user?.email}
          </span>
          <button
            onClick={() => void logout()}
            className="px-3 py-1.5 text-red-600 hover:bg-red-50 rounded-lg font-medium"
          >
            Logout
          </button>
        </nav>
      </header>

      <main className="flex-1 overflow-hidden">
        <Chat />
      </main>
    </div>
  );
}
