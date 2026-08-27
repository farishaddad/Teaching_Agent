/**
 * KPI metric cards for the dashboard header
 */

interface MetricsCardsProps {
  data: {
    total_students: number;
    active_students_7d: number;
    total_interactions: number;
    total_tokens_used: number;
    estimated_monthly_cost_usd: number;
    guardrail_trigger_rate: number;
    avg_questions_per_student: number;
  };
}

export default function MetricsCards({ data }: MetricsCardsProps) {
  const cards = [
    {
      label: 'Total Students',
      value: data.total_students,
      icon: '👥',
      detail: `${data.active_students_7d} active (7d)`,
      color: 'blue',
    },
    {
      label: 'Total Interactions',
      value: data.total_interactions.toLocaleString(),
      icon: '💬',
      detail: `${data.avg_questions_per_student.toFixed(1)} avg/student`,
      color: 'green',
    },
    {
      label: 'Tokens Used',
      value: formatTokens(data.total_tokens_used),
      icon: '⚡',
      detail: 'Input + Output',
      color: 'purple',
    },
    {
      label: 'Est. Monthly Cost',
      value: `$${data.estimated_monthly_cost_usd.toFixed(2)}`,
      icon: '💰',
      detail: 'Projected from usage',
      color: 'amber',
    },
    {
      label: 'Guardrail Rate',
      value: `${data.guardrail_trigger_rate}%`,
      icon: '🛡️',
      detail: 'Interactions blocked',
      color: data.guardrail_trigger_rate > 10 ? 'red' : 'green',
    },
  ];

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">
      {cards.map((card) => (
        <div
          key={card.label}
          className="bg-white rounded-xl shadow-sm border border-gray-200 p-4 hover:shadow-md transition-shadow"
        >
          <div className="flex items-center justify-between">
            <span className="text-2xl">{card.icon}</span>
            <span className={`text-xs px-2 py-0.5 rounded-full bg-${card.color}-100 text-${card.color}-700`}>
              {card.detail}
            </span>
          </div>
          <p className="mt-3 text-2xl font-bold text-gray-900">{card.value}</p>
          <p className="text-sm text-gray-500">{card.label}</p>
        </div>
      ))}
    </div>
  );
}

function formatTokens(tokens: number): string {
  if (tokens >= 1_000_000) return `${(tokens / 1_000_000).toFixed(1)}M`;
  if (tokens >= 1_000) return `${(tokens / 1_000).toFixed(1)}K`;
  return tokens.toString();
}
