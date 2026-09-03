/**
 * Tutorial Chapter — fetches markdown from static files (no auth required)
 */

import { useEffect, useState, useRef } from 'react';

interface Chapter {
  slug: string;
  title: string;
  estimated_minutes: number;
}

const CHAPTERS: Chapter[] = [
  { slug: '01-architecture', title: 'Architecture Overview', estimated_minutes: 15 },
  { slug: '02-authentication', title: 'Setting Up Authentication', estimated_minutes: 20 },
  { slug: '03-rag-pipeline', title: 'Building the RAG Pipeline', estimated_minutes: 25 },
  { slug: '04-guardrails', title: 'Implementing Guardrails', estimated_minutes: 25 },
  { slug: '05-tracking', title: 'Tracking & Analytics', estimated_minutes: 20 },
  { slug: '06-deployment', title: 'Deployment', estimated_minutes: 20 },
  { slug: '07-extending', title: 'Extending the Agent', estimated_minutes: 25 },
  { slug: '08-course-materials', title: 'Managing Course Materials', estimated_minutes: 15 },
];

interface TutorialChapterProps {
  slug: string;
  isCompleted: boolean;
  onToggleComplete: () => void;
  onNavigate: (slug: string) => void;
}

export default function TutorialChapter({ slug, isCompleted, onToggleComplete, onNavigate }: TutorialChapterProps) {
  const [content, setContent] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const contentRef = useRef<HTMLDivElement>(null);

  const chapterIndex = CHAPTERS.findIndex(c => c.slug === slug);
  const chapter = CHAPTERS[chapterIndex];

  useEffect(() => {
    setLoading(true);
    setError('');
    // Fetch directly from Vite static assets — no auth needed
    fetch(`/tutorial/${slug}.md`)
      .then(res => {
        if (!res.ok) throw new Error(`${res.status}: ${res.statusText}`);
        return res.text();
      })
      .then(md => {
        setContent(md);
        setLoading(false);
      })
      .catch(err => {
        setError(err.message);
        setLoading(false);
      });
    contentRef.current?.scrollTo(0, 0);
  }, [slug]);

  // Intercept internal chapter links so they navigate within the SPA instead
  // of triggering a full-page (SPA-fallback) navigation to a .md path.
  useEffect(() => {
    const root = contentRef.current;
    if (!root || loading) return;

    const handler = (e: MouseEvent) => {
      const anchor = (e.target as HTMLElement).closest('a[data-chapter]');
      if (!anchor) return;
      const targetSlug = anchor.getAttribute('data-chapter');
      if (targetSlug && CHAPTERS.some(c => c.slug === targetSlug)) {
        e.preventDefault();
        onNavigate(targetSlug);
      }
    };

    root.addEventListener('click', handler);
    return () => root.removeEventListener('click', handler);
  }, [content, loading, onNavigate]);

  // Add copy buttons to code blocks
  useEffect(() => {
    if (!contentRef.current || loading) return;
    const blocks = contentRef.current.querySelectorAll('pre');
    blocks.forEach(block => {
      if (block.querySelector('.copy-btn')) return;
      const btn = document.createElement('button');
      btn.className = 'copy-btn';
      btn.textContent = '📋 Copy';
      btn.style.cssText = 'position:absolute;top:6px;right:6px;font-size:11px;padding:3px 8px;background:#374151;color:#d1d5db;border:none;border-radius:4px;cursor:pointer';
      btn.onclick = () => {
        navigator.clipboard.writeText(block.querySelector('code')?.textContent || block.textContent || '');
        btn.textContent = '✓ Copied!';
        setTimeout(() => (btn.textContent = '📋 Copy'), 2000);
      };
      block.style.position = 'relative';
      block.appendChild(btn);
    });
  }, [content, loading]);

  if (loading) return (
    <div className="flex items-center justify-center h-64">
      <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-600 mr-3"></div>
      <span className="text-gray-500">Loading chapter...</span>
    </div>
  );

  if (error) return (
    <div className="p-8">
      <div className="bg-red-50 border border-red-200 rounded-lg p-4">
        <p className="text-red-700 font-medium">Could not load chapter</p>
        <p className="text-red-500 text-sm mt-1">{error}</p>
        <p className="text-xs text-gray-400 mt-2">Make sure you ran: <code>cp tutorial/*.md frontend/public/tutorial/</code></p>
      </div>
    </div>
  );

  const html = markdownToHtml(content);

  return (
    <div ref={contentRef} className="max-w-4xl mx-auto px-8 py-6 overflow-y-auto">
      <div className="flex items-center justify-between mb-6 pb-4 border-b border-gray-200">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">{chapter?.title || slug}</h1>
          <p className="text-sm text-gray-500 mt-1">⏱️ {chapter?.estimated_minutes || 0} min read</p>
        </div>
        <button
          onClick={onToggleComplete}
          className={`px-4 py-2 rounded-lg text-sm font-medium ${isCompleted ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-600 hover:bg-gray-200'}`}
        >
          {isCompleted ? '✅ Completed' : '☐ Mark Complete'}
        </button>
      </div>

      <article
        className="prose prose-gray max-w-none"
        style={{ lineHeight: '1.7' }}
        dangerouslySetInnerHTML={{ __html: html }}
      />

      <div className="flex items-center justify-between mt-12 pt-6 border-t border-gray-200">
        {chapterIndex > 0 ? (
          <button onClick={() => onNavigate(CHAPTERS[chapterIndex - 1].slug)} className="text-sm text-blue-600 hover:text-blue-800 font-medium">
            ← Previous
          </button>
        ) : <div />}
        {chapterIndex < CHAPTERS.length - 1 ? (
          <button onClick={() => onNavigate(CHAPTERS[chapterIndex + 1].slug)} className="text-sm text-blue-600 hover:text-blue-800 font-medium">
            Next →
          </button>
        ) : (
          <span className="text-sm text-green-600 font-medium">🎉 Tutorial Complete!</span>
        )}
      </div>
    </div>
  );
}

function markdownToHtml(md: string): string {
  return md
    .replace(/```(\w*)\n([\s\S]*?)```/g, (_m, lang, code) =>
      `<pre style="background:#1e293b;color:#e2e8f0;padding:16px;border-radius:8px;overflow-x:auto;font-size:13px"><code class="language-${lang}">${escHtml(code)}</code></pre>`)
    .replace(/`([^`]+)`/g, '<code style="background:#f1f5f9;padding:2px 5px;border-radius:3px;font-size:0.9em">$1</code>')
    .replace(/^#{4} (.+)$/gm, '<h4 style="font-size:1rem;font-weight:600;margin:1.5rem 0 0.5rem">$1</h4>')
    .replace(/^#{3} (.+)$/gm, '<h3 style="font-size:1.15rem;font-weight:700;margin:2rem 0 0.5rem">$1</h3>')
    .replace(/^#{2} (.+)$/gm, '<h2 style="font-size:1.4rem;font-weight:700;margin:2.5rem 0 0.75rem;padding-bottom:0.5rem;border-bottom:2px solid #e2e8f0">$1</h2>')
    .replace(/^# (.+)$/gm, '<h1 style="font-size:1.8rem;font-weight:800;margin:0 0 1rem">$1</h1>')
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.+?)\*/g, '<em>$1</em>')
    .replace(/\[([^\]]+)\]\(([^)]+)\)/g, (_m, text, href) => {
      // Internal chapter links look like ./02-authentication.md or
      // 02-authentication.md (optionally with a #anchor). Render these as
      // in-app navigation triggers instead of real anchors — otherwise the
      // browser navigates to a non-routed path and the SPA fallback shows the
      // landing page. External links (http/https) open in a new tab as usual.
      const chapterMatch = /^\.?\/?((?:\d{2})-[a-z0-9-]+)\.md(?:#.*)?$/i.exec(href);
      if (chapterMatch) {
        const targetSlug = chapterMatch[1];
        return `<a href="#${targetSlug}" data-chapter="${targetSlug}" style="color:#3b82f6;text-decoration:underline;cursor:pointer">${text}</a>`;
      }
      // README.md (tutorial index) → go to the first chapter.
      if (/^\.?\/?README\.md(?:#.*)?$/i.test(href)) {
        return `<a href="#01-architecture" data-chapter="01-architecture" style="color:#3b82f6;text-decoration:underline;cursor:pointer">${text}</a>`;
      }
      return `<a href="${href}" target="_blank" rel="noopener" style="color:#3b82f6;text-decoration:underline">${text}</a>`;
    })
    .replace(/^> (.+)$/gm, '<blockquote style="border-left:4px solid #e2e8f0;margin:1rem 0;padding:0.5rem 1rem;color:#64748b">$1</blockquote>')
    .replace(/^\|(.+)\|$/gm, (row) => {
      const cells = row.split('|').filter(Boolean).map(c => c.trim());
      if (cells.every(c => /^[-:]+$/.test(c))) return '';
      return `<tr>${cells.map(c => `<td style="border:1px solid #e2e8f0;padding:8px 12px">${c}</td>`).join('')}</tr>`;
    })
    .replace(/(<tr>.*<\/tr>)+/gs, m => `<table style="border-collapse:collapse;width:100%;margin:1rem 0">${m}</table>`)
    .replace(/^- (.+)$/gm, '<li style="margin:0.25rem 0">$1</li>')
    .replace(/^\d+\. (.+)$/gm, '<li style="margin:0.25rem 0">$1</li>')
    .replace(/(<li.*<\/li>(\n)?)+/g, m => `<ul style="margin:0.75rem 0;padding-left:1.5rem">${m}</ul>`)
    .replace(/^---$/gm, '<hr style="margin:2rem 0;border:none;border-top:1px solid #e2e8f0">')
    .replace(/\n\n/g, '</p><p style="margin:0.75rem 0">')
    .replace(/^(.)/m, '<p style="margin:0.75rem 0">$1')
    + '</p>';
}

function escHtml(s: string) {
  return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}
