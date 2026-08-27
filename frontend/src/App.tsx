/**
 * Teaching Agent Frontend — App Root
 * Routes between student chat, admin dashboard, and tutorial
 */

import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import AdminLayout from './components/admin/AdminLayout';
import Tutorial from './components/Tutorial';

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
          <Route path="/" element={<div className="p-8 text-center text-gray-500">Student Chat (coming next)</div>} />
          
          {/* Tutorial */}
          <Route path="/tutorial" element={<Tutorial />} />
          
          {/* Admin dashboard */}
          <Route path="/admin/*" element={<AdminLayout />} />
          
          {/* Auth (placeholder — built by Kiro in Module 1) */}
          <Route path="/login" element={<div>Login</div>} />
          <Route path="/auth/callback" element={<div>Auth Callback</div>} />
          
          {/* Fallback */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  );
}
