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

// ─── Course Materials (RAG S3 bucket) ─────────────────────────────────

export interface MaterialItem {
  key: string;
  size: number;
  last_modified: string;
}

export interface MaterialList {
  bucket: string;
  items: MaterialItem[];
  count: number;
}

export function listMaterials(prefix = ''): Promise<MaterialList> {
  const params = prefix ? `?prefix=${encodeURIComponent(prefix)}` : '';
  return adminFetch(`/materials${params}`);
}

export function deleteMaterial(key: string) {
  // Key may contain slashes; encode each segment but keep the path separators
  // so it matches the backend's {key:path} route.
  const encoded = key.split('/').map(encodeURIComponent).join('/');
  return adminFetch(`/materials/${encoded}`, { method: 'DELETE' });
}

export function syncKnowledgeBase() {
  return adminFetch('/materials/sync', { method: 'POST' });
}

interface PresignResponse {
  url: string;
  key: string;
  method: string;
  headers: Record<string, string>;
  expires_in: number;
  max_bytes: number;
}

/**
 * Upload a course-material file: ask the backend for a presigned URL, then
 * PUT the file directly to S3 (bypasses the API Gateway 10 MB limit). The
 * direct-to-S3 request must NOT send credentials and MUST send the same
 * Content-Type the URL was signed for.
 */
export async function uploadMaterial(file: File, prefix = ''): Promise<{ key: string }> {
  const contentType = file.type || 'application/octet-stream';
  const presign: PresignResponse = await adminFetch('/materials/presign', {
    method: 'POST',
    body: JSON.stringify({
      filename: file.name,
      content_type: contentType,
      prefix,
    }),
  });

  if (file.size > presign.max_bytes) {
    throw new Error(
      `File too large (${Math.round(file.size / 1024 / 1024)}MB). ` +
      `Max is ${Math.round(presign.max_bytes / 1024 / 1024)}MB.`
    );
  }

  const putRes = await fetch(presign.url, {
    method: 'PUT',
    headers: presign.headers,
    body: file,
    // Direct to S3 — no cookies/credentials.
  });
  if (!putRes.ok) {
    throw new Error(`Upload to storage failed (HTTP ${putRes.status}).`);
  }
  return { key: presign.key };
}
