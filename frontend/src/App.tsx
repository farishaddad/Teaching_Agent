/**
 * Teaching Agent Frontend — App Root
 */

import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import AdminLayout from './components/admin/AdminLayout';
import Tutorial from './components/Tutorial';
import Login from './components/Login';
import AuthCallback from './components/AuthCallback';
import RequireInstructor from './components/RequireInstructor';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 30000,
      retry: 1,
    },
  },
});

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Routes>
          {/* Student chat view */}
          <Route path="/" element={
            <div className="flex items-center justify-center h-screen bg-gray-50">
              <div className="text-center">
                <h1 className="text-3xl font-bold text-gray-900 mb-2">🤖 Teaching Agent</h1>
                <p className="text-gray-500 mb-6">Agentic AI Course Companion</p>
                <div className="space-x-4">
                  <a href="/tutorial" className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">Tutorial</a>
                  <a href="/admin" className="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300">Admin</a>
                  <a href="/login" className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700">Login</a>
                </div>
              </div>
            </div>
          } />
          
          {/* Auth */}
          <Route path="/login" element={<Login />} />
          <Route path="/auth/callback" element={<AuthCallback />} />
          
          {/* Tutorial */}
          <Route path="/tutorial" element={<Tutorial />} />
          
          {/* Admin dashboard — instructors only */}
          <Route
            path="/admin/*"
            element={
              <RequireInstructor>
                <AdminLayout />
              </RequireInstructor>
            }
          />
          
          {/* Fallback */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  );
}
