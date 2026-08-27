/**
 * Tutorial Viewer — in-app chapter navigation with progress tracking
 */

import { useState, useEffect } from 'react';
import { useQuery } from '@tanstack/react-query';
import TutorialChapter from './TutorialChapter';

const API_BASE = import.meta.env.VITE_API_URL || '';

interface Chapter {
  slug: string;
  title: string;
  estimated_minutes: number;
}

export default function Tutorial() {
  const [activeSlug, setActiveSlug] = useState<string>('01-architecture');
  const [completed, setCompleted] = useState<Set<string>>(() => {
    const stored = localStorage.getItem('tutorial_completed');
    return stored ? new Set(JSON.parse(stored)) : new Set();
  });

  const { data: chaptersData } = useQuery({
    queryKey: ['tutorial-chapters'],
    queryFn: async () => {
      const res = await fetch(`${API_BASE}/api/tutorial`, { credentials: 'include' });
      return res.json();
    },
  });

  const chapters: Chapter[] = chaptersData?.chapters || [];

  // Persist completion state
  useEffect(() => {
    localStorage.setItem('tutorial_completed', JSON.stringify([...completed]));
  }, [completed]);

  const toggleComplete = (slug: string) => {
    setCompleted((prev) => {
      const next = new Set(prev);
      if (next.has(slug)) next.delete(slug);
      else next.add(slug);
      return next;
    });
  };

  const progressPercent = chapters.length > 0
    ? Math.round((completed.size / chapters.length) * 100)
    : 0;

  return (
    <div className="flex h-screen bg-gray-50">
      {/* Sidebar */}
      <aside className="w-72 bg-white border-r border-gray-200 flex flex-col overflow-y-auto">
        <div className="px-4 py-5 border-b border-gray-100">
          <h1 className="text-sm font-bold text-gray-900">📚 Tutorial</h1>
          <p className="text-xs text-gray-500 mt-1">Build Your Own AI Teaching Agent</p>
          {/* Progress bar */}
          <div className="mt-3">
            <div className="flex items-center justify-between text-xs text-gray-500 mb-1">
              <span>{completed.size}/{chapters.length} chapters</span>
              <span>{progressPercent}%</span>
            </div>
            <div className="w-full bg-gray-100 rounded-full h-2">
              <div
                className="bg-green-500 h-2 rounded-full transition-all duration-300"
                style={{ width: `${progressPercent}%` }}
              ></div>
            </div>
          </div>
        </div>

        <nav className="flex-1 px-2 py-3 space-y-1">
          {chapters.map((chapter, i) => (
            <button
              key={chapter.slug}
              onClick={() => setActiveSlug(chapter.slug)}
              className={`w-full flex items-center gap-2 px-3 py-2.5 rounded-lg text-left text-sm transition-colors ${
                activeSlug === chapter.slug
                  ? 'bg-blue-50 text-blue-700 font-medium'
                  : 'text-gray-600 hover:bg-gray-50'
              }`}
            >
              {/* Completion indicator */}
              <span className={`flex-shrink-0 w-5 h-5 rounded-full border-2 flex items-center justify-center text-xs ${
                completed.has(chapter.slug)
                  ? 'bg-green-500 border-green-500 text-white'
                  : 'border-gray-300'
              }`}>
                {completed.has(chapter.slug) ? '✓' : i + 1}
              </span>
              <div className="flex-1 min-w-0">
                <p className="truncate">{chapter.title}</p>
                <p className="text-xs text-gray-400">{chapter.estimated_minutes} min</p>
              </div>
            </button>
          ))}
        </nav>
      </aside>

      {/* Main Content */}
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
