/**
 * Tutorial Viewer — sidebar + chapter content, all served from static files
 */

import { useState, useEffect } from 'react';
import TutorialChapter from './TutorialChapter';

const CHAPTERS = [
  { slug: '01-architecture', title: 'Architecture Overview', estimated_minutes: 15 },
  { slug: '02-authentication', title: 'Setting Up Authentication', estimated_minutes: 20 },
  { slug: '03-rag-pipeline', title: 'Building the RAG Pipeline', estimated_minutes: 25 },
  { slug: '04-guardrails', title: 'Implementing Guardrails', estimated_minutes: 25 },
  { slug: '05-tracking', title: 'Tracking & Analytics', estimated_minutes: 20 },
  { slug: '06-deployment', title: 'Deployment', estimated_minutes: 20 },
  { slug: '07-extending', title: 'Extending the Agent', estimated_minutes: 25 },
];

export default function Tutorial() {
  const [activeSlug, setActiveSlug] = useState('01-architecture');
  const [completed, setCompleted] = useState<Set<string>>(() => {
    const stored = localStorage.getItem('tutorial_completed');
    return stored ? new Set(JSON.parse(stored)) : new Set();
  });

  useEffect(() => {
    localStorage.setItem('tutorial_completed', JSON.stringify([...completed]));
  }, [completed]);

  const toggleComplete = (slug: string) => {
    setCompleted(prev => {
      const next = new Set(prev);
      if (next.has(slug)) next.delete(slug); else next.add(slug);
      return next;
    });
  };

  const progress = Math.round((completed.size / CHAPTERS.length) * 100);

  return (
    <div className="flex h-screen bg-gray-50">
      {/* Sidebar */}
      <aside className="w-72 bg-white border-r border-gray-200 flex flex-col overflow-y-auto flex-shrink-0">
        <div className="px-4 py-5 border-b border-gray-100">
          <div className="flex items-center gap-2 mb-1">
            <span>📚</span>
            <h1 className="text-sm font-bold text-gray-900">Tutorial</h1>
          </div>
          <p className="text-xs text-gray-500">Build Your Own AI Teaching Agent</p>
          <div className="mt-3">
            <div className="flex justify-between text-xs text-gray-400 mb-1">
              <span>{completed.size}/{CHAPTERS.length} chapters</span>
              <span>{progress}%</span>
            </div>
            <div className="w-full bg-gray-100 rounded-full h-1.5">
              <div className="bg-green-500 h-1.5 rounded-full transition-all" style={{ width: `${progress}%` }}></div>
            </div>
          </div>
        </div>
        <nav className="flex-1 px-2 py-3 space-y-1">
          {CHAPTERS.map((ch, i) => (
            <button
              key={ch.slug}
              onClick={() => setActiveSlug(ch.slug)}
              className={`w-full flex items-center gap-2 px-3 py-2.5 rounded-lg text-left text-sm transition-colors ${
                activeSlug === ch.slug ? 'bg-blue-50 text-blue-700 font-medium' : 'text-gray-600 hover:bg-gray-50'
              }`}
            >
              <span className={`flex-shrink-0 w-5 h-5 rounded-full border-2 flex items-center justify-center text-xs font-medium ${
                completed.has(ch.slug) ? 'bg-green-500 border-green-500 text-white' : 'border-gray-300 text-gray-400'
              }`}>
                {completed.has(ch.slug) ? '✓' : i + 1}
              </span>
              <div className="flex-1 min-w-0">
                <p className="truncate leading-snug">{ch.title}</p>
                <p className="text-xs text-gray-400">{ch.estimated_minutes} min</p>
              </div>
            </button>
          ))}
        </nav>
      </aside>

      {/* Content */}
      <main className="flex-1 overflow-y-auto">
        <TutorialChapter
          slug={activeSlug}
          isCompleted={completed.has(activeSlug)}
          onToggleComplete={() => toggleComplete(activeSlug)}
          onNavigate={setActiveSlug}
        />
      </main>
    </div>
  );
}
