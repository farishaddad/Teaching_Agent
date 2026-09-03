/**
 * Chat API client — student Q&A against the course materials.
 *
 * Talks to the backend chat endpoint (POST /api/chat/), which retrieves from
 * the Bedrock Knowledge Base, applies guardrails, and returns a grounded
 * answer with citations. Auth is cookie-based (httpOnly), so requests send
 * credentials just like the admin client.
 */

const API_BASE = import.meta.env.VITE_API_URL || '';

export interface SourceCitation {
  source: string;
  excerpt: string;
}

export interface TokenUsage {
  input: number;
  output: number;
  total: number;
}

export interface ChatResponse {
  answer: string;
  sources: SourceCitation[];
  session_id: string;
  tokens_used: TokenUsage;
  guardrail_triggered: boolean;
}

/**
 * Send a student message and get a grounded answer.
 *
 * @param message   The student's question (1–2000 chars).
 * @param sessionId Optional session id to continue a conversation. Omit on the
 *                  first turn; pass the value returned by the previous response
 *                  on subsequent turns.
 */
export async function sendChat(
  message: string,
  sessionId?: string,
): Promise<ChatResponse> {
  // Note the trailing slash: the chat router mounts the handler at "/" under
  // the /api/chat prefix, so the endpoint is /api/chat/.
  const response = await fetch(`${API_BASE}/api/chat/`, {
    method: 'POST',
    credentials: 'include',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      message,
      ...(sessionId ? { session_id: sessionId } : {}),
    }),
  });

  if (!response.ok) {
    if (response.status === 401) {
      throw new Error('Your session has expired. Please log in again.');
    }
    const err = await response.json().catch(() => ({ detail: 'Unknown error' }));
    // FastAPI validation errors put an array in `detail`; keep the message readable.
    const detail = typeof err.detail === 'string' ? err.detail : `HTTP ${response.status}`;
    throw new Error(detail);
  }

  return response.json();
}
