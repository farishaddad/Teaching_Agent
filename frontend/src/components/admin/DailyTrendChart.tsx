/**
 * Daily activity trend chart — questions asked, unique students, tokens
 * Uses a lightweight canvas chart (or recharts if installed)
 */

import { useMemo } from 'react';

interface DailyMetric {
  date: string;
  total_questions: number;
  unique_students: number;
  total_tokens: number;
  estimated_bedrock_cost_usd: number;
  guardrail_triggers: number;
}

interface DailyTrendChartProps {
  metrics: DailyMetric[];
}

export default function DailyTrendChart({ metrics }: DailyTrendChartProps) {
  const maxQuestions = useMemo(
    () => Math.max(...metrics.map((m) => m.total_questions), 1),
    [metrics]
  );

  if (!metrics.length) {
    return <p className="text-gray-400 text-sm">No data for this period.</p>;
  }

  return (
    <div className="space-y-4">
      {/* Mini legend */}
      <div className="flex gap-4 text-xs text-gray-500">
        <span className="flex items-center gap-1">
          <span className="w-3 h-3 rounded-sm bg-blue-500 inline-block"></span>
          Questions
        </span>
        <span className="flex items-center gap-1">
          <span className="w-3 h-3 rounded-sm bg-red-400 inline-block"></span>
          Guardrail Triggers
        </span>
      </div>

      {/* Bar chart */}
      <div className="flex items-end gap-[2px] h-48 overflow-x-auto">
        {metrics.map((m) => {
          const height = (m.total_questions / maxQuestions) * 100;
          const guardrailHeight = maxQuestions > 0
            ? (m.guardrail_triggers / maxQuestions) * 100
            : 0;

          return (
            <div
              key={m.date}
              className="flex flex-col items-center flex-shrink-0 group relative"
              style={{ width: `${100 / Math.min(metrics.length, 30)}%`, minWidth: '12px' }}
            >
              {/* Tooltip */}
              <div className="absolute bottom-full mb-2 hidden group-hover:block z-10 bg-gray-800 text-white text-xs rounded px-2 py-1 whitespace-nowrap">
                <p className="font-medium">{m.date}</p>
                <p>Questions: {m.total_questions}</p>
                <p>Students: {m.unique_students}</p>
                <p>Tokens: {m.total_tokens.toLocaleString()}</p>
                <p>Guardrails: {m.guardrail_triggers}</p>
                <p>Cost: ${m.estimated_bedrock_cost_usd.toFixed(4)}</p>
              </div>

              {/* Bars stacked */}
              <div className="w-full flex flex-col justify-end h-full">
                {/* Guardrail portion (red, on top) */}
                {guardrailHeight > 0 && (
                  <div
                    className="w-full bg-red-400 rounded-t-sm"
                    style={{ height: `${guardrailHeight}%` }}
                  ></div>
                )}
                {/* Questions portion (blue) */}
                <div
                  className="w-full bg-blue-500 rounded-t-sm hover:bg-blue-600 transition-colors cursor-pointer"
                  style={{ height: `${height}%`, minHeight: m.total_questions > 0 ? '2px' : '0' }}
                ></div>
              </div>
            </div>
          );
        })}
      </div>

      {/* X-axis labels (show every 5th) */}
      <div className="flex justify-between text-xs text-gray-400 mt-1">
        {metrics
          .filter((_, i) => i % Math.ceil(metrics.length / 6) === 0)
          .map((m) => (
            <span key={m.date}>{m.date.slice(5)}</span> // Show MM-DD
          ))}
      </div>

      {/* Summary stats */}
      <div className="grid grid-cols-3 gap-4 pt-4 border-t border-gray-100">
        <div>
          <p className="text-xs text-gray-500">Total Questions</p>
          <p className="text-lg font-semibold">
            {metrics.reduce((sum, m) => sum + m.total_questions, 0).toLocaleString()}
          </p>
        </div>
        <div>
          <p className="text-xs text-gray-500">Avg/Day</p>
          <p className="text-lg font-semibold">
            {Math.round(
              metrics.reduce((sum, m) => sum + m.total_questions, 0) / metrics.length
            )}
          </p>
        </div>
        <div>
          <p className="text-xs text-gray-500">Total Cost</p>
          <p className="text-lg font-semibold">
            ${metrics.reduce((sum, m) => sum + m.estimated_bedrock_cost_usd, 0).toFixed(2)}
          </p>
        </div>
      </div>
    </div>
  );
}
