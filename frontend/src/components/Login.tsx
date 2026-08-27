/**
 * Login — entry page for the Teaching Agent.
 *
 * Clicking "Sign in" initiates the PKCE authorization code flow by:
 *  1. Generating a code verifier + challenge (in useAuth.login).
 *  2. Redirecting to the Cognito Hosted UI.
 *
 * Tokens are never handled here — all token management is in useAuth
 * and processed server-side at /api/auth/callback.
 */

import { useAuth } from '../hooks/useAuth';

export default function Login() {
  const { login, isLoading, error } = useAuth();

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center px-4">
      <div className="w-full max-w-md">
        {/* Card */}
        <div className="bg-white rounded-2xl shadow-lg px-8 py-10">
          {/* Logo / branding */}
          <div className="text-center mb-8">
            <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-indigo-600 mb-4">
              <span className="text-3xl" role="img" aria-label="robot">🤖</span>
            </div>
            <h1 className="text-2xl font-bold text-gray-900">Teaching Agent</h1>
            <p className="text-sm text-gray-500 mt-1">Agentic AI Course Companion</p>
          </div>

          {/* Sign-in description */}
          <p className="text-center text-gray-600 text-sm mb-8 leading-relaxed">
            Sign in with your course email to access the AI teaching assistant,
            ask questions, and track your progress.
          </p>

          {/* Error message */}
          {error && (
            <div
              role="alert"
              className="mb-6 rounded-lg bg-red-50 border border-red-200 px-4 py-3 text-sm text-red-700"
            >
              <span className="font-medium">Sign-in error: </span>
              {error}
            </div>
          )}

          {/* Sign-in button */}
          <button
            type="button"
            onClick={() => void login()}
            disabled={isLoading}
            className="w-full flex items-center justify-center gap-2 rounded-xl bg-indigo-600 px-4 py-3 text-sm font-semibold text-white shadow-sm hover:bg-indigo-700 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600 disabled:opacity-60 disabled:cursor-not-allowed transition-colors"
            aria-busy={isLoading}
          >
            {isLoading ? (
              <>
                <svg
                  className="animate-spin h-4 w-4 text-white"
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
                Redirecting…
              </>
            ) : (
              <>
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  className="h-4 w-4"
                  viewBox="0 0 20 20"
                  fill="currentColor"
                  aria-hidden="true"
                >
                  <path
                    fillRule="evenodd"
                    d="M10 1a9 9 0 100 18A9 9 0 0010 1zM6.5 9.5a3.5 3.5 0 117 0 3.5 3.5 0 01-7 0zm3.5 5a6.97 6.97 0 00-4.33 1.5A7.96 7.96 0 0010 18a7.96 7.96 0 004.33-1.5A6.97 6.97 0 0010 14.5z"
                    clipRule="evenodd"
                  />
                </svg>
                Sign in with course account
              </>
            )}
          </button>

          {/* Info note */}
          <p className="mt-6 text-center text-xs text-gray-400">
            Access is restricted to enrolled students.{' '}
            <span className="block mt-1">
              Contact your instructor if you need an account.
            </span>
          </p>
        </div>

        {/* Footer */}
        <p className="text-center text-xs text-gray-400 mt-6">
          Powered by Amazon Bedrock &amp; AWS Cognito
        </p>
      </div>
    </div>
  );
}
