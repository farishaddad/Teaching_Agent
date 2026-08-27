/**
 * Tutorial Chapter — renders a single chapter's markdown content
 * with code block copy buttons and navigation
 */

import { useQuery } from '@tanstack/react-query';
import { useState, useEffect, useRef } from 'react';

const API_BASE = import.meta.env.VITE_API_URL || '';

interface TutorialChapterProps {
  slug: string;
  isCompleted: boolean;
  onToggleComplete: () => void;
  onNavigate: (slug: string) => void;
}

export default function TutorialChapter({
  slug,
  isCompleted,
  onToggleComplete,
  onNavigate,
}: TutorialChapterProps) {
  const contentRef = useRef<HTMLDivElement>(null);

  const { data, isLoading, error } = useQuery({
    queryKey: ['tutorial-chapter', slug],
    queryFn: async () => {
      const res = await fetch(`${API_BASE}/api/tutorial/${slug}`, { credentials: 'include' });
      if (!res.ok) throw new Error('Chapter not found');
      return res.json();
    },
    enabled: !!slug,
  });

  // Scroll to top on chapter change
  useEffect(() => {
    contentRef.current?.scrollTo(0, 0);
  }, [slug]);

  // Add copy buttons to code blocks after render
  useEffect(() => {
    if (!contentRef.current) return;
    const codeBlocks = contentRef.current.querySelectorAll('pre');
    codeBlocks.forEach((block) => {
      if (block.querySelector('.copy-btn')) return; // Already has button
      const btn = document.createElement('button');
      btn.className = 'copy-btn';
      btn.textContent = '📋 Copy';
      btn.style.cssText = 'position:absolute;top:4px;right:4px;font-size:11px;padding:2px 8px;background:#374151;color:#d1d5db;border:none;border-radius:4px;cursor:pointer;opacity:0.7;';
      btn.onclick = () => {
        const code = block.querySelector('code')?.textContent || block.textContent || '';
        navigator.clipboard.writeText(code);
        btn.textContent = '✓ Copied!';
        setTimeout(() => (btn.textContent = '📋 Copy'), 2000);
      };
      block.style.position = 'relative';
      block.appendChild(btn);
    });
  }, [data?.content]);

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-8">
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <p className="text-red-700">Chapter not found. Please select a chapter from the sidebar.</p>
        </div>
      </div>
    );
  }

  const html = markdownToHtml(data?.content || '');

  return (
    <div ref={contentRef} className="max-w-4xl mx-auto px-8 py-6">
      {/* Chapter header */}
      <div className="flex items-center justify-between mb-6 pb-4 border-b border-gray-200">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">{data?.title}</h1>
          <p className="text-sm text-gray-500 mt-1">
            ⏱️ {data?.estimated_minutes} min read
          </p>
        </div>
        <button
          onClick={onToggleComplete}
          className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
            isCompleted
              ? 'bg-green-100 text-green-700 hover:bg-green-200'
              : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
          }`}
        >
          {isCompleted ? '✅ Completed' : '☐ Mark Complete'}
        </button>
      </div>

      {/* Markdown content */}
      <article
        className="prose prose-gray max-w-none prose-headings:scroll-mt-4 prose-code:bg-gray-100 prose-code:px-1 prose-code:py-0.5 prose-code:rounded prose-pre:bg-gray-900 prose-pre:text-gray-100"
        dangerouslySetInnerHTML={{ __html: html }}
      />

      {/* Navigation */}
      <div className="flex items-center justify-between mt-12 pt-6 border-t border-gray-200">
        {data?.prev_chapter ? (
          <button
            onClick={() => onNavigate(data.prev_chapter)}
            className="flex items-center gap-2 text-sm text-blue-600 hover:text-blue-800 font-medium"
          >
            ← Previous Chapter
          </button>
        ) : <div />}
        {data?.next_chapter ? (
          <button
            onClick={() => onNavigate(data.next_chapter)}
            className="flex items-center gap-2 text-sm text-blue-600 hover:text-blue-800 font-medium"
          >
            Next Chapter →
          </button>
        ) : (
          <span className="text-sm text-green-600 font-medium">🎉 Tutorial Complete!</span>
        )}
      </div>
    </div>
  );
}

/**
 * Simple markdown → HTML converter (covers headings, code, tables, lists, bold, italic, links)
 * For production, use a library like marked or remark.
 */
function markdownToHtml(md: string): string {
  let html = md
    // Code blocks (```lang\n...\n```)
    .replace(/```(\w*)\n([\s\S]*?)```/g, '<pre><code class="language-$1">$2</code></pre>')
    // Inline code
    .replace(/`([^`]+)`/g, '<code>$1</code>')
    // Headings
    .replace(/^#### (.+)$/gm, '<h4>$1</h4>')
    .replace(/^### (.+)$/gm, '<h3>$1</h3>')
    .replace(/^## (.+)$/gm, '<h2>$1</h2>')
    .replace(/^# (.+)$/gm, '<h1>$1</h1>')
    // Bold + italic
    .replace(/\*\*\*(.+?)\*\*\*/g, '<strong><em>$1</em></strong>')
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.+?)\*/g, '<em>$1</em>')
    // Links
    .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank" rel="noopener">$1</a>')
    // Horizontal rule
    .replace(/^---$/gm, '<hr>')
    // Tables (basic)
    .replace(/^\|(.+)\|$/gm, (match) => {
      const cells = match.split('|').filter(Boolean).map(c => c.trim());
      if (cells.every(c => /^[-:]+$/.test(c))) return ''; // separator row
      const tag = 'td';
      return `<tr>${cells.map(c => `<${tag}>${c}</${tag}>`).join('')}</tr>`;
    })
    // Unordered lists
    .replace(/^- (.+)$/gm, '<li>$1</li>')
    // Ordered lists
    .replace(/^\d+\. (.+)$/gm, '<li>$1</li>')
    // Paragraphs (double newline)
    .replace(/\n\n/g, '</p><p>')
    // Single newlines in flow
    .replace(/\n/g, '<br>');

  // Wrap in paragraph
  html = `<p>${html}</p>`;

  // Wrap consecutive <li> in <ul>
  html = html.replace(/(<li>.*?<\/li>)+/gs, '<ul>$&</ul>');

  // Wrap consecutive <tr> in <table>
  html = html.replace(/(<tr>.*?<\/tr>)+/gs, '<table class="border-collapse w-full">$&</table>');

  return html;
}
