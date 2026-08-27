/**
 * Top Topics widget — shows most-asked-about topics
 */

interface TopTopicsProps {
  topics: { topic: string; question_count: number }[];
}

export default function TopTopics({ topics }: TopTopicsProps) {
  if (!topics.length) {
    return <p className="text-sm text-gray-400">No topic data yet.</p>;
  }

  const maxCount = Math.max(...topics.map((t) => t.question_count), 1);

  return (
    <div className="space-y-3">
      {topics.map((topic, i) => (
        <div key={topic.topic} className="space-y-1">
          <div className="flex items-center justify-between">
            <span className="text-sm text-gray-700 truncate">{topic.topic}</span>
            <span className="text-xs font-medium text-gray-500 ml-2">
              {topic.question_count}
            </span>
          </div>
          <div className="w-full bg-gray-100 rounded-full h-2">
            <div
              className="bg-blue-500 rounded-full h-2 transition-all"
              style={{ width: `${(topic.question_count / maxCount) * 100}%` }}
            ></div>
          </div>
        </div>
      ))}
    </div>
  );
}
