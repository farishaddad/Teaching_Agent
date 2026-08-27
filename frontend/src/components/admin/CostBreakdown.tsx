/**
 * AWS Cost Breakdown — shows per-service costs as a visual bar + table
 */

interface CostData {
  period_start: string;
  period_end: string;
  bedrock_converse_cost: number;
  bedrock_kb_cost: number;
  bedrock_guardrails_cost: number;
  dynamodb_cost: number;
  lambda_cost: number;
  api_gateway_cost: number;
  s3_cost: number;
  cognito_cost: number;
  total_cost: number;
  cost_per_student: number;
  cost_per_interaction: number;
}

interface CostBreakdownProps {
  data: CostData;
}

export default function CostBreakdown({ data }: CostBreakdownProps) {
  const services = [
    { name: 'Bedrock (LLM)', cost: data.bedrock_converse_cost, color: 'bg-blue-500' },
    { name: 'Bedrock (KB)', cost: data.bedrock_kb_cost, color: 'bg-blue-300' },
    { name: 'Bedrock (Guardrails)', cost: data.bedrock_guardrails_cost, color: 'bg-indigo-400' },
    { name: 'DynamoDB', cost: data.dynamodb_cost, color: 'bg-orange-400' },
    { name: 'Lambda', cost: data.lambda_cost, color: 'bg-yellow-500' },
    { name: 'API Gateway', cost: data.api_gateway_cost, color: 'bg-green-400' },
    { name: 'S3', cost: data.s3_cost, color: 'bg-red-400' },
    { name: 'Cognito', cost: data.cognito_cost, color: 'bg-purple-400' },
  ].sort((a, b) => b.cost - a.cost);

  const maxCost = Math.max(...services.map((s) => s.cost), 0.01);

  return (
    <div className="space-y-4">
      {/* Total + per-unit costs */}
      <div className="flex items-baseline gap-4 pb-3 border-b border-gray-100">
        <div>
          <span className="text-3xl font-bold text-gray-900">
            ${data.total_cost.toFixed(2)}
          </span>
          <span className="text-sm text-gray-500 ml-2">total ({data.period_start} → {data.period_end})</span>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-3 text-sm">
        <div className="bg-gray-50 rounded-lg p-2">
          <p className="text-gray-500 text-xs">Per Student</p>
          <p className="font-semibold">${data.cost_per_student.toFixed(4)}</p>
        </div>
        <div className="bg-gray-50 rounded-lg p-2">
          <p className="text-gray-500 text-xs">Per Interaction</p>
          <p className="font-semibold">${data.cost_per_interaction.toFixed(6)}</p>
        </div>
      </div>

      {/* Horizontal bar chart by service */}
      <div className="space-y-2">
        {services.map((s) => (
          <div key={s.name} className="flex items-center gap-2">
            <span className="text-xs text-gray-600 w-32 text-right truncate">{s.name}</span>
            <div className="flex-1 bg-gray-100 rounded-full h-4 overflow-hidden">
              <div
                className={`h-full rounded-full ${s.color} transition-all`}
                style={{ width: `${(s.cost / maxCost) * 100}%`, minWidth: s.cost > 0 ? '4px' : '0' }}
              ></div>
            </div>
            <span className="text-xs font-mono text-gray-700 w-16 text-right">
              ${s.cost.toFixed(4)}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}
