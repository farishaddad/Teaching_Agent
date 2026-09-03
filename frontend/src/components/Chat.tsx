/**
 * Chat — student Q&A with the course materials.
 *
 * Sends questions to the backend RAG endpoint and renders grounded answers
 * with source citations. Maintains a session id across turns so the backend
 * can keep conversation context.
 */

import { useRef, useState, useEffect, FormEvent } from 'react';
import { useMutation } from '@tanstack/react-query';
import { sendChat, SourceCitation } from '../api/chat';

interface ChatTurn {
  role: 'user' | 'assistant';
  text: string;
  sources?: SourceCitation[];
  guardrail?: boolean;
}

export default function Chat() {
  const [input, setInput] = useState('');
  const [turns, setTurns] = useState<ChatTurn[]>([]);
  const [sessionId, setSessionId] = useState<string | undefined>(undefined);
  const [includeWeb, setIncludeWeb] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);

  const mutation = useMutation({
    mutationFn: (message: string) => sendChat(message, sessionId, includeWeb),
    onSuccess: (res) => {
      setSessionId(res.session_id);
      setTurns((prev) => [
        ...prev,
        {
          role: 'assistant',
          text: res.answer,
          sources: res.sources,
          guardrail: res.guardrail_triggered,
        },
      ]);
    },
    onError: (err: Error) => {
      setTurns((prev) => [
        ...prev,
        { role: 'assistant', text: `⚠️ ${err.message}` },
      ]);
    },
  });

  // Auto-scroll to the newest message.
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [turns, mutation.isPending]);

  function handleSubmit(e: FormEvent) {
    e.preventDefault();
    const message = input.trim();
    if (!message || mutation.isPending) return;
    setTurns((prev) => [...prev, { role: 'user', text: message }]);
    setInput('');
    mutation.mutate(message);
  }

  return (
    <div className="flex flex-col h-full max-w-3xl mx-auto w-full">
      {/* Messages */}
      <div className="flex-1 overflow-y-auto px-4 py-6 space-y-4">
        {turns.length === 0 && !mutation.isPending && (
          <div className="text-center text-gray-400 mt-16">
            <p className="text-4xl mb-3">💬</p>
            <p className="text-sm">
              Ask a question about the course materials to get started.
            </p>
            <p className="text-xs mt-2 text-gray-300">
              e.g. “What is the difference between a ReAct agent and a
              plan-and-execute agent?”
            </p>
          </div>
        )}

        {turns.map((turn, i) => (
          <div
            key={i}
            className={`flex ${turn.role === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-[85%] rounded-2xl px-4 py-2.5 text-sm whitespace-pre-wrap ${
                turn.role === 'user'
                  ? 'bg-blue-600 text-white'
                  : 'bg-white border border-gray-200 text-gray-800'
              }`}
            >
              {turn.guardrail && (
                <p className="text-xs font-medium text-amber-600 mb-1">
                  ⚠️ This response was adjusted by content guardrails.
                </p>
              )}
              <p>{turn.text}</p>

              {turn.sources && turn.sources.length > 0 && (
                <div className="mt-3 border-t border-gray-100 pt-2">
                  <p className="text-xs font-semibold text-gray-500 mb-1">Sources</p>
                  <ul className="space-y-1">
                    {turn.sources.map((s, si) => (
                      <li key={si} className="text-xs text-gray-500">
                        {s.url ? (
                          <a
                            href={s.url}
                            target="_blank"
                            rel="noreferrer"
                            className="font-medium text-blue-600 hover:underline"
                          >
                            🌐 {s.source}
                          </a>
                        ) : (
                          <span className="font-medium text-gray-700">{s.source}</span>
                        )}
                        {s.excerpt && <span className="text-gray-400"> — {s.excerpt}</span>}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </div>
        ))}

        {mutation.isPending && (
          <div className="flex justify-start">
            <div className="bg-white border border-gray-200 rounded-2xl px-4 py-3">
              <span className="inline-flex gap-1">
                <span className="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce [animation-delay:-0.3s]" />
                <span className="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce [animation-delay:-0.15s]" />
                <span className="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce" />
              </span>
            </div>
          </div>
        )}

        <div ref={bottomRef} />
      </div>

      {/* Composer */}
      <form
        onSubmit={handleSubmit}
        className="border-t border-gray-200 bg-white px-4 py-3"
      >
        <div className="flex items-end gap-2">
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                handleSubmit(e);
              }
            }}
            rows={1}
            placeholder="Ask about the course materials…"
            className="flex-1 resize-none border border-gray-300 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500 max-h-40"
          />
          <button
            type="submit"
            disabled={!input.trim() || mutation.isPending}
            className="bg-blue-600 hover:bg-blue-700 disabled:opacity-40 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors"
          >
            Send
          </button>
        </div>

        {/* Source mode toggle */}
        <div className="flex items-center justify-between mt-2">
          <div className="inline-flex rounded-lg border border-gray-200 p-0.5 text-xs">
            <button
              type="button"
              onClick={() => setIncludeWeb(false)}
              className={`px-2.5 py-1 rounded-md font-medium transition-colors ${
                !includeWeb ? 'bg-blue-600 text-white' : 'text-gray-600 hover:bg-gray-100'
              }`}
            >
              📄 Course materials
            </button>
            <button
              type="button"
              onClick={() => setIncludeWeb(true)}
              className={`px-2.5 py-1 rounded-md font-medium transition-colors ${
                includeWeb ? 'bg-blue-600 text-white' : 'text-gray-600 hover:bg-gray-100'
              }`}
            >
              🌐 Course materials + Web
            </button>
          </div>
        </div>

        <p className="text-[11px] text-gray-400 mt-1.5">
          {includeWeb
            ? 'Answers use the course materials first, then supplement with web results (cited with links).'
            : 'Answers are grounded in the course materials only.'}{' '}
          Press Enter to send, Shift+Enter for a new line.
        </p>
      </form>
    </div>
  );
}
