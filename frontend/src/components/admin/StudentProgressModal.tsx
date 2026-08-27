/**
 * Student Progress Modal — detailed view of a student's engagement,
 * topic strengths, weaknesses, and interaction history.
 */

import { useQuery } from '@tanstack/react-query';
import { fetchStudentProgress, fetchStudentInteractions } from '../../api/admin';

interface TopicProgress {
  topic_slug: string;
  topic_name: string;
  questions_asked: number;
  unique_sessions: number;
  avg_follow_up_depth: number;
  confidence_score: number;
  last_accessed: string | null;
  weakness_flag: boolean;
}

interface StudentProgressModalProps {
  studentId: string;
  onClose: () => void;
}

export default function StudentProgressModal({ studentId, onClose }: StudentProgressModalProps) {
  const { data: progress, isLoading } = useQuery({
    queryKey: ['student-progress', studentId],
    queryFn: () => fetchStudentProgress(studentId),
  });

  const { data: interactions } = useQuery({
    queryKey: ['student-interactions', studentId],
    queryFn: () => fetchStudentInteractions(studentId),
  });

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-2xl shadow-2xl max-w-4xl w-full max-h-[90vh] overflow-hidden flex flex-col">
        {/* Header */}
        <div className="px-6 py-4 border-b border-gray-200 flex items-center justify-between">
          <div>
            <h2 className="text-xl font-bold text-gray-900">
              {progress?.student_name || 'Student'} — Progress Report
            </h2>
            <p className="text-sm text-gray-500">
              {progress?.cohort} · Enrolled: {progress?.enrollment_date}
            </p>
          </div>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 p-1"
          >
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-y-auto p-6 space-y-6">
          {isLoading ? (
            <div className="flex items-center justify-center h-32">
              <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-600"></div>
            </div>
          ) : progress ? (
            <>
              {/* Summary Stats */}
              <div className="grid grid-cols-4 gap-4">
                <StatCard label="Total Questions" value={progress.total_questions} />
                <StatCard label="Sessions" value={progress.total_sessions} />
                <StatCard label="Active Days" value={progress.active_days} />
                <StatCard label="Topics Covered" value={progress.topics.length} />
              </div>

              {/* Weaknesses */}
              {progress.weaknesses.length > 0 && (
                <div className="bg-red-50 border border-red-200 rounded-xl p-4">
                  <h3 className="text-sm font-semibold text-red-800 mb-3">
                    ⚠️ Areas Needing Attention ({progress.weaknesses.length})
                  </h3>
                  <div className="space-y-2">
                    {progress.weaknesses.map((w: TopicProgress) => (
                      <div key={w.topic_slug} className="flex items-center justify-between">
                        <div>
                          <span className="text-sm font-medium text-red-900">{w.topic_name}</span>
                          <span className="text-xs text-red-600 ml-2">
                            {w.questions_asked} questions across {w.unique_sessions} sessions
                          </span>
                        </div>
                        <ConfidenceBadge score={w.confidence_score} />
                      </div>
                    ))}
                  </div>
                  <p className="text-xs text-red-600 mt-3">
                    Student is repeatedly asking basic questions on these topics without progressing.
                    Consider targeted intervention or additional resources.
                  </p>
                </div>
              )}

              {/* Strengths */}
              {progress.strengths.length > 0 && (
                <div className="bg-green-50 border border-green-200 rounded-xl p-4">
                  <h3 className="text-sm font-semibold text-green-800 mb-3">
                    ✅ Strong Areas ({progress.strengths.length})
                  </h3>
                  <div className="space-y-2">
                    {progress.strengths.map((s: TopicProgress) => (
                      <div key={s.topic_slug} className="flex items-center justify-between">
                        <span className="text-sm text-green-900">{s.topic_name}</span>
                        <ConfidenceBadge score={s.confidence_score} />
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* All Topics */}
              <div>
                <h3 className="text-sm font-semibold text-gray-800 mb-3">
                  Topic Engagement ({progress.topics.length} topics)
                </h3>
                <div className="space-y-2">
                  {progress.topics
                    .sort((a: TopicProgress, b: TopicProgress) => b.questions_asked - a.questions_asked)
                    .map((topic: TopicProgress) => (
                      <div
                        key={topic.topic_slug}
                        className={`flex items-center gap-3 p-3 rounded-lg border ${
                          topic.weakness_flag
                            ? 'border-red-200 bg-red-50'
                            : 'border-gray-100 bg-gray-50'
                        }`}
                      >
                        <div className="flex-1">
                          <p className="text-sm font-medium text-gray-900">{topic.topic_name}</p>
                          <p className="text-xs text-gray-500">
                            {topic.questions_asked} questions · {topic.unique_sessions} sessions ·
                            Depth: {topic.avg_follow_up_depth}
                          </p>
                        </div>
                        <ConfidenceBadge score={topic.confidence_score} />
                        {topic.weakness_flag && (
                          <span className="text-xs px-2 py-0.5 rounded-full bg-red-100 text-red-700">
                            Struggling
                          </span>
                        )}
                      </div>
                    ))}
                </div>
              </div>

              {/* Recent Interactions */}
              {interactions?.interactions?.length > 0 && (
                <div>
                  <h3 className="text-sm font-semibold text-gray-800 mb-3">
                    Recent Questions
                  </h3>
                  <div className="space-y-2 max-h-60 overflow-y-auto">
                    {interactions.interactions.slice(0, 10).map((item: any) => (
                      <div key={item.interaction_id} className="border border-gray-100 rounded-lg p-3">
                        <div className="flex items-start justify-between">
                          <p className="text-sm text-gray-800">{item.query}</p>
                          {item.guardrail_triggered && (
                            <span className="text-xs px-2 py-0.5 rounded-full bg-amber-100 text-amber-700 ml-2 flex-shrink-0">
                              🛡️ Blocked
                            </span>
                          )}
                        </div>
                        <p className="text-xs text-gray-400 mt-1">
                          {item.timestamp} · {item.topic_detected || 'Unclassified'}
                        </p>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </>
          ) : (
            <p className="text-gray-400">No progress data available.</p>
          )}
        </div>

        {/* Footer */}
        <div className="px-6 py-3 border-t border-gray-200 flex justify-end">
          <button
            onClick={onClose}
            className="px-4 py-2 bg-gray-100 hover:bg-gray-200 rounded-lg text-sm font-medium text-gray-700"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
}

function StatCard({ label, value }: { label: string; value: number }) {
  return (
    <div className="bg-gray-50 rounded-lg p-3 text-center">
      <p className="text-2xl font-bold text-gray-900">{value}</p>
      <p className="text-xs text-gray-500">{label}</p>
    </div>
  );
}

function ConfidenceBadge({ score }: { score: number }) {
  const color =
    score >= 0.7 ? 'bg-green-100 text-green-800' :
    score >= 0.4 ? 'bg-yellow-100 text-yellow-800' :
    'bg-red-100 text-red-800';

  return (
    <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${color}`}>
      {Math.round(score * 100)}% confidence
    </span>
  );
}
