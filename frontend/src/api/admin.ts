/**
 * Admin API client — communicates with /api/admin/* endpoints
 */

// When VITE_API_URL is set, call it directly (e.g. production build against
// the deployed API). When empty (local dev), use a relative path so requests
// flow through the Vite dev proxy (see vite.config.ts) to the live API — this
// keeps the admin client consistent with the rest of the app and avoids
// hardcoding a backend URL.
const API_BASE = import.meta.env.VITE_API_URL || '';

async function adminFetch(path: string, options?: RequestInit) {
  const response = await fetch(`${API_BASE}/api/admin${path}`, {
    credentials: 'include', // Send httpOnly cookies
    headers: {
      'Content-Type': 'application/json',
      ...options?.headers,
    },
    ...options,
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
    throw new Error(error.detail || `HTTP ${response.status}`);
  }

  return response.json();
}

// ─── Dashboard ────────────────────────────────────────────────────────

export function fetchDashboard(days: number = 30) {
  return adminFetch(`/dashboard?days=${days}`);
}

export function fetchCosts(days: number = 30) {
  return adminFetch(`/costs?days=${days}`);
}

export function fetchTokenUsage(days: number = 30, groupBy: string = 'day') {
  return adminFetch(`/metrics/tokens?days=${days}&group_by=${groupBy}`);
}

// ─── Student Management ───────────────────────────────────────────────

export function listStudents(cohort?: string) {
  const params = cohort ? `?cohort=${cohort}` : '';
  return adminFetch(`/students${params}`);
}

export function createStudent(data: {
  email: string;
  first_name: string;
  last_name: string;
  cohort: string;
}) {
  return adminFetch('/students', {
    method: 'POST',
    body: JSON.stringify(data),
  });
}

export function bulkCreateStudents(data: { students: any[] }) {
  return adminFetch('/students/bulk', {
    method: 'POST',
    body: JSON.stringify(data),
  });
}

export function updateStudent(studentId: string, data: any) {
  return adminFetch(`/students/${studentId}`, {
    method: 'PATCH',
    body: JSON.stringify(data),
  });
}

export function disableStudent(studentId: string) {
  return adminFetch(`/students/${studentId}/disable`, { method: 'POST' });
}

export function resetPassword(studentId: string) {
  return adminFetch(`/students/${studentId}/reset-password`, { method: 'POST' });
}

// ─── Student Progress ─────────────────────────────────────────────────

export function fetchStudentProgress(studentId: string) {
  return adminFetch(`/students/${studentId}/progress`);
}

export function fetchStudentInteractions(studentId: string, page: number = 1) {
  return adminFetch(`/students/${studentId}/interactions?page=${page}`);
}
