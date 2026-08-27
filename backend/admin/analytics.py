"""Analytics engine — aggregates student data for the admin dashboard.

Computes:
- Overall platform metrics (total students, interactions, tokens, costs)
- Per-student progress and weakness analysis
- Daily/weekly trends
- Cost tracking and projections
"""

import os
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from typing import Optional

import boto3
import structlog

from backend.admin.models import (
    CostBreakdown,
    DailyMetrics,
    OverallDashboard,
    StudentProgressReport,
    TopicProgress,
)

logger = structlog.get_logger()

TABLE_NAME = os.environ.get("TRACKING_TABLE_NAME", "teaching-agent-tracking-dev")
dynamodb = boto3.resource("dynamodb", region_name="eu-west-2")
table = dynamodb.Table(TABLE_NAME)

# Cost constants (eu-west-2 pricing as of 2026)
BEDROCK_INPUT_TOKEN_COST = 0.003 / 1000  # $3/MTok input
BEDROCK_OUTPUT_TOKEN_COST = 0.015 / 1000  # $15/MTok output
BEDROCK_KB_RETRIEVAL_COST = 0.001  # Per retrieval call (approximate)
BEDROCK_GUARDRAIL_COST = 0.00075  # Per assessment (approximate)


# ─── Course Topic Taxonomy ────────────────────────────────────────────

COURSE_TOPICS = {
    "agent-fundamentals": "Agent Fundamentals & Architecture",
    "llm-foundations": "LLM Foundations",
    "prompt-engineering": "Prompt Engineering",
    "rag": "Retrieval-Augmented Generation (RAG)",
    "tool-use": "Tool Use & Function Calling",
    "multi-agent": "Multi-Agent Systems",
    "planning-reasoning": "Planning & Reasoning",
    "memory-state": "Memory & State Management",
    "guardrails-safety": "Guardrails & AI Safety",
    "evaluation": "Agent Evaluation & Testing",
    "deployment": "Deployment & Operations",
    "ethics-governance": "Ethics & Governance",
    "bedrock-services": "Amazon Bedrock Services",
    "use-cases": "Real-World Use Cases",
    "agent-frameworks": "Agent Frameworks (LangGraph, CrewAI, etc.)",
    "human-in-loop": "Human-in-the-Loop Patterns",
}

# Keywords for topic detection (used in weakness analysis)
TOPIC_KEYWORDS = {
    "agent-fundamentals": ["agent", "autonomous", "architecture", "components", "agent loop"],
    "llm-foundations": ["llm", "language model", "transformer", "tokens", "context window", "foundation model"],
    "prompt-engineering": ["prompt", "system prompt", "few-shot", "chain of thought", "cot", "instruction"],
    "rag": ["rag", "retrieval", "knowledge base", "embeddings", "vector", "chunks", "grounding"],
    "tool-use": ["tool", "function calling", "api", "action", "tool use"],
    "multi-agent": ["multi-agent", "orchestration", "crew", "swarm", "collaboration"],
    "planning-reasoning": ["planning", "reasoning", "step by step", "decomposition", "react"],
    "memory-state": ["memory", "state", "context", "conversation history", "persistence"],
    "guardrails-safety": ["guardrail", "safety", "filter", "content policy", "pii", "hallucination"],
    "evaluation": ["evaluation", "testing", "benchmark", "metrics", "accuracy"],
    "deployment": ["deploy", "production", "scaling", "lambda", "infrastructure", "cdk"],
    "ethics-governance": ["ethics", "bias", "responsible", "governance", "fairness"],
    "bedrock-services": ["bedrock", "converse api", "knowledge base", "aws", "claude"],
    "use-cases": ["use case", "example", "application", "industry", "real world"],
    "agent-frameworks": ["langgraph", "crewai", "autogen", "framework", "langchain"],
    "human-in-loop": ["human", "approval", "review", "oversight", "escalation"],
}


async def get_overall_dashboard(days: int = 30) -> OverallDashboard:
    """Generate the top-level admin dashboard metrics."""
    end_date = datetime.now(timezone.utc)
    start_date = end_date - timedelta(days=days)

    # Query daily aggregates from GSI
    daily_data = await _query_daily_metrics(start_date, end_date)

    # Compute aggregates
    total_interactions = sum(d.total_questions for d in daily_data)
    total_tokens = sum(d.total_tokens for d in daily_data)
    unique_students_all = set()

    for d in daily_data:
        unique_students_all.add(d.date)  # Simplified — real impl queries distinct students

    # Estimate monthly cost
    estimated_cost = _estimate_monthly_cost(total_tokens, total_interactions, days)

    # Get student count from Cognito (cached)
    total_students = await _count_students()

    # Topic analysis
    top_topics = await _get_top_topics(start_date, end_date)
    common_weaknesses = await _get_common_weaknesses()

    return OverallDashboard(
        total_students=total_students,
        active_students_7d=len(unique_students_all),
        total_interactions=total_interactions,
        total_tokens_used=total_tokens,
        estimated_monthly_cost_usd=estimated_cost,
        guardrail_trigger_rate=_calc_guardrail_rate(daily_data),
        avg_questions_per_student=total_interactions / max(total_students, 1),
        daily_metrics=daily_data,
        top_topics=top_topics,
        common_weaknesses=common_weaknesses,
    )


async def get_student_progress(student_id: str) -> StudentProgressReport:
    """Generate a detailed progress report for a single student.

    Analyses:
    - Topics they've engaged with
    - Depth of engagement per topic
    - Identified weaknesses (repeated basic questions, low follow-up depth)
    - Strengths (advanced questions, high confidence indicators)
    """
    # Fetch all interactions for the student
    response = table.query(
        KeyConditionExpression="PK = :pk AND begins_with(SK, :prefix)",
        ExpressionAttributeValues={
            ":pk": f"STU#{student_id}",
            ":prefix": "INT#",
        },
        ScanIndexForward=True,
    )
    interactions = response.get("Items", [])

    if not interactions:
        return StudentProgressReport(
            student_id=student_id,
            student_name="",
            cohort="",
            enrollment_date="",
            total_questions=0,
            total_sessions=0,
            active_days=0,
            topics=[],
            weaknesses=[],
            strengths=[],
            engagement_trend=[],
        )

    # Analyse topics
    topic_data = _analyse_topic_engagement(interactions)
    topics = list(topic_data.values())
    weaknesses = [t for t in topics if t.weakness_flag]
    strengths = [t for t in topics if t.confidence_score >= 0.7 and not t.weakness_flag]

    # Engagement trend (daily)
    engagement_trend = _compute_engagement_trend(interactions)

    # Active days
    active_dates = set()
    for item in interactions:
        sk = item.get("SK", "")
        if "INT#" in sk:
            date_part = sk.split("#")[1][:10]
            active_dates.add(date_part)

    return StudentProgressReport(
        student_id=student_id,
        student_name="",  # Filled by route handler from Cognito
        cohort="",
        enrollment_date="",
        total_questions=len(interactions),
        total_sessions=_estimate_sessions(interactions),
        active_days=len(active_dates),
        topics=topics,
        weaknesses=weaknesses,
        strengths=strengths,
        engagement_trend=engagement_trend,
    )


async def get_cost_breakdown(period_days: int = 30) -> CostBreakdown:
    """Calculate AWS cost breakdown for the platform."""
    end_date = datetime.now(timezone.utc)
    start_date = end_date - timedelta(days=period_days)

    daily_data = await _query_daily_metrics(start_date, end_date)
    total_interactions = sum(d.total_questions for d in daily_data)
    total_tokens_in = sum(d.total_tokens_input for d in daily_data)
    total_tokens_out = sum(d.total_tokens_output for d in daily_data)
    total_students = await _count_students()

    # Calculate costs per service
    bedrock_converse = (total_tokens_in * BEDROCK_INPUT_TOKEN_COST) + (total_tokens_out * BEDROCK_OUTPUT_TOKEN_COST)
    bedrock_kb = total_interactions * BEDROCK_KB_RETRIEVAL_COST
    bedrock_guardrails = total_interactions * BEDROCK_GUARDRAIL_COST
    dynamodb_cost = total_interactions * 0.000001  # Approximate per-write cost
    lambda_cost = total_interactions * 0.0000002 * 512 * 5  # 512MB, 5s avg duration
    api_gw_cost = total_interactions * 0.0000035  # API Gateway per-request
    s3_cost = 0.023 * 0.5  # ~500MB course materials, $0.023/GB
    cognito_cost = total_students * 0.0055  # First 50k MAUs at $0.0055/MAU

    total = (
        bedrock_converse + bedrock_kb + bedrock_guardrails +
        dynamodb_cost + lambda_cost + api_gw_cost + s3_cost + cognito_cost
    )

    return CostBreakdown(
        period_start=start_date.strftime("%Y-%m-%d"),
        period_end=end_date.strftime("%Y-%m-%d"),
        bedrock_converse_cost=round(bedrock_converse, 4),
        bedrock_kb_cost=round(bedrock_kb, 4),
        bedrock_guardrails_cost=round(bedrock_guardrails, 4),
        dynamodb_cost=round(dynamodb_cost, 4),
        lambda_cost=round(lambda_cost, 4),
        api_gateway_cost=round(api_gw_cost, 4),
        s3_cost=round(s3_cost, 4),
        cognito_cost=round(cognito_cost, 4),
        total_cost=round(total, 2),
        cost_per_student=round(total / max(total_students, 1), 4),
        cost_per_interaction=round(total / max(total_interactions, 1), 6),
    )


# ─── Weakness Analysis ────────────────────────────────────────────────

def _analyse_topic_engagement(interactions: list[dict]) -> dict[str, TopicProgress]:
    """Detect which topics a student has engaged with and identify weaknesses.

    Weakness indicators:
    - Repeated basic questions on the same topic (not progressing)
    - Very short follow-up chains (asking but not going deeper)
    - Re-visiting topics after long gaps without improvement
    """
    topic_counts = Counter()
    topic_sessions = defaultdict(set)
    topic_last_seen = {}

    for item in interactions:
        query = item.get("query", "").lower()
        detected_topic = _detect_topic(query)
        if detected_topic:
            topic_counts[detected_topic] += 1
            # Use date as session proxy
            sk = item.get("SK", "")
            date_part = sk.split("#")[1][:10] if "#" in sk else ""
            topic_sessions[detected_topic].add(date_part)
            topic_last_seen[detected_topic] = sk.split("#")[1][:19] if "#" in sk else ""

    results = {}
    for topic_slug, count in topic_counts.items():
        sessions = len(topic_sessions[topic_slug])
        # Weakness: many questions across many sessions but shallow (high count, low depth ratio)
        avg_depth = count / max(sessions, 1)
        confidence = min(1.0, (avg_depth * 0.3) + (sessions * 0.1))

        # Flag as weakness if: >5 questions but confidence < 0.4 (lots of basic revisits)
        weakness = count > 5 and confidence < 0.4

        results[topic_slug] = TopicProgress(
            topic_slug=topic_slug,
            topic_name=COURSE_TOPICS.get(topic_slug, topic_slug),
            questions_asked=count,
            unique_sessions=sessions,
            avg_follow_up_depth=round(avg_depth, 2),
            confidence_score=round(confidence, 2),
            last_accessed=topic_last_seen.get(topic_slug),
            weakness_flag=weakness,
        )

    return results


def _detect_topic(query: str) -> Optional[str]:
    """Simple keyword-based topic detection from a student query."""
    query_lower = query.lower()
    best_match = None
    best_score = 0

    for topic_slug, keywords in TOPIC_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in query_lower)
        if score > best_score:
            best_score = score
            best_match = topic_slug

    return best_match if best_score > 0 else None


# ─── Helper Functions ─────────────────────────────────────────────────

async def _query_daily_metrics(start_date, end_date) -> list[DailyMetrics]:
    """Query aggregate daily metrics from DynamoDB GSI."""
    # In production, this queries the GSI1 (DATE#YYYY-MM-DD) partition
    # For now, return structure placeholder
    metrics = []
    current = start_date
    while current <= end_date:
        date_str = current.strftime("%Y-%m-%d")
        try:
            response = table.query(
                IndexName="GSI1",
                KeyConditionExpression="GSI1PK = :date_pk",
                ExpressionAttributeValues={":date_pk": f"DATE#{date_str}"},
                Select="COUNT",
            )
            count = response.get("Count", 0)
        except Exception:
            count = 0

        metrics.append(DailyMetrics(
            date=date_str,
            total_questions=count,
            unique_students=0,  # Would need distinct count from GSI1SK
            total_tokens_input=count * 500,  # Estimate: 500 input tokens avg
            total_tokens_output=count * 1500,  # Estimate: 1500 output tokens avg
            total_tokens=count * 2000,
            estimated_bedrock_cost_usd=round(count * 2000 * (BEDROCK_INPUT_TOKEN_COST + BEDROCK_OUTPUT_TOKEN_COST) / 2, 4),
            guardrail_triggers=0,
            avg_response_time_ms=2500,  # Estimate
        ))
        current += timedelta(days=1)

    return metrics


async def _count_students() -> int:
    """Count total students in Cognito user pool."""
    try:
        cognito = boto3.client("cognito-idp", region_name="eu-west-2")
        response = cognito.describe_user_pool(
            UserPoolId=os.environ.get("COGNITO_USER_POOL_ID", "")
        )
        return response.get("UserPool", {}).get("EstimatedNumberOfUsers", 0)
    except Exception:
        return 0


async def _get_top_topics(start_date, end_date) -> list[dict]:
    """Get most-asked-about topics across all students."""
    # Simplified — full implementation would scan interactions
    return [
        {"topic": "RAG", "question_count": 0},
        {"topic": "Prompt Engineering", "question_count": 0},
        {"topic": "Multi-Agent Systems", "question_count": 0},
    ]


async def _get_common_weaknesses() -> list[dict]:
    """Identify topics that multiple students struggle with."""
    return []


def _calc_guardrail_rate(daily_data: list[DailyMetrics]) -> float:
    """Calculate percentage of interactions that triggered guardrails."""
    total_q = sum(d.total_questions for d in daily_data)
    total_g = sum(d.guardrail_triggers for d in daily_data)
    return round(total_g / max(total_q, 1) * 100, 2)


def _estimate_sessions(interactions: list[dict]) -> int:
    """Estimate number of sessions from interaction timestamps (30-min gap = new session)."""
    if not interactions:
        return 0
    sessions = 1
    # Simplified — real implementation parses timestamps
    return max(1, len(interactions) // 5)


def _compute_engagement_trend(interactions: list[dict]) -> list[dict]:
    """Compute daily engagement counts for trend charts."""
    daily = Counter()
    for item in interactions:
        sk = item.get("SK", "")
        if "#" in sk:
            date_part = sk.split("#")[1][:10]
            daily[date_part] += 1

    return [{"date": d, "questions_asked": c} for d, c in sorted(daily.items())]


def _estimate_monthly_cost(total_tokens: int, total_interactions: int, days: int) -> float:
    """Project monthly cost from observed usage."""
    daily_avg_tokens = total_tokens / max(days, 1)
    daily_avg_interactions = total_interactions / max(days, 1)

    monthly_tokens = daily_avg_tokens * 30
    monthly_interactions = daily_avg_interactions * 30

    token_cost = monthly_tokens * (BEDROCK_INPUT_TOKEN_COST + BEDROCK_OUTPUT_TOKEN_COST) / 2
    interaction_cost = monthly_interactions * (BEDROCK_KB_RETRIEVAL_COST + BEDROCK_GUARDRAIL_COST)

    return round(token_cost + interaction_cost, 2)
