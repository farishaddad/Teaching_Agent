/**
 * Weakness Alerts — highlights topics where multiple students are struggling
 */

interface Weakness {
  topic: string;
  student_count: number;
  avg_confidence: number;
}

interface WeaknessAlertsProps {
  weaknesses: Weakness[];
}

export default function WeaknessAlerts({ weaknesses }: WeaknessAlertsProps) {
  if (!weaknesses.length) {
    return (
      <div className="text-center py-8">
        <p className="text-3xl mb-2">✅</p>
        <p className="text-sm text-gray-500">No widespread weaknesses detected.</p>
        <p className="text-xs text-gray-400 mt-1">
          Students are engaging well across all topics.
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-3">
      <p className="text-xs text-gray-500">
        Topics where multiple students show low confidence (repeated basic questions, low follow-up depth).
      </p>
      {weaknesses.map((w) => (
        <div
          key={w.topic}
          className="flex items-center justify-between p-3 bg-red-50 border border-red-100 rounded-lg"
        >
          <div>
            <p className="text-sm font-medium text-red-900">{w.topic}</p>
            <p className="text-xs text-red-600">
              {w.student_count} students struggling · {Math.round(w.avg_confidence * 100)}% avg confidence
            </p>
          </div>
          <button className="text-xs text-red-700 hover:text-red-900 font-medium px-2 py-1 rounded hover:bg-red-100">
            View Details
          </button>
        </div>
      ))}
      <p className="text-xs text-gray-400 mt-2">
        💡 Consider adding supplementary materials or scheduling a live session on these topics.
      </p>
    </div>
  );
}
