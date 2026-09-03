/**
 * Teaching Agent Frontend — App Root
 */

import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import AdminLayout from './components/admin/AdminLayout';
import Home from './components/Home';
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
          {/* Student chat view (auth-aware home) */}
          <Route path="/" element={<Home />} />
          
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
