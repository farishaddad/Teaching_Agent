# Module 15 — Observability, Evaluation & Monitoring for AI
## [NEW 2026] Update: Latest Techniques, Tools & Approaches

---

## GAP ANALYSIS

Based on web research into the current (mid-2026) state of AI observability, here are the gaps in the original module:

1. **OpenTelemetry for AI is now production-ready** — The original module mentions OTel in passing. In 2026, OpenTelemetry GenAI semantic conventions, OpenInference, and the `traceAI` register pattern are the de facto standard. This deserves its own section.

2. **"Evals as Code" is the new paradigm** — The original covers offline evals and online A/B but doesn't name the "evals as code" discipline: evaluation suites that run in CI/CD, gate deployments, and convert production failures into regression tests.

3. **LLM-as-Judge has matured significantly** — The original mentions it briefly. In 2026, G-Eval, pairwise comparison, rubric-based scoring, Cohen's kappa calibration, and bias controls (length bias, family bias) are established practice.

4. **Agent-specific observability is a distinct discipline** — The original treats observability as if the target is a simple LLM API call. In 2026, multi-step agent traces with tool invocations, reasoning chains, subagent spawning, and per-agent cost attribution require different approaches.

5. **Vendor landscape has consolidated** — The original names Langfuse, Phoenix, and CloudWatch. In 2026, the landscape includes Braintrust, Galileo, Latitude, DeepEval, Arize AX, Langfuse v3 (OTel-native), Opik (Comet), and MLflow. Students will encounter vendor confusion.

6. **Langfuse v3 is fundamentally different** — It moved to an OTel-native architecture with observations (not traces) as the primary table. The old decorator-based SDK is legacy.

7. **Real-time / online evaluation** — Runtime guardrails that score responses in <200ms (Galileo Luna-2, Bedrock Guardrails with Automated Reasoning) are now production practice, not experimental.

8. **Cost attribution for multi-agent systems** — Per-user, per-task, per-agent, per-tenant cost breakdowns are table stakes. The original only covers basic token counting.

9. **Context rot and semantic drift as named failure modes** — These are now well-documented observability targets, not just abstract concerns.

10. **AWS Bedrock Guardrails + AgentCore + CloudWatch AI Observability** — Significant new capabilities since the original module was written (Automated Reasoning checks, AgentCore policy guardrails, CloudWatch GenAI observability).

---

## [NEW 2026] SLIDES

---

### [NEW 2026] Slide 1: The 2026 Observability Stack — Three Layers
**Insert after:** "Why AI observability is different from traditional APM" section
**Format:** Concept diagram

**Content:**

The 2026 AI observability stack has crystallised into three distinct layers:

```
┌─────────────────────────────────────────────────────┐
│  LAYER 3: EVALUATION & QUALITY SCORING              │
│  LLM-as-judge · Rubric scorers · Regression suites  │
│  Online guardrails · Drift detection · Evals as code│
├─────────────────────────────────────────────────────┤
│  LAYER 2: TRACING & TELEMETRY                       │
│  OpenTelemetry GenAI · OpenInference · Spans/traces  │
│  Token attribution · Latency · Cost per span        │
├─────────────────────────────────────────────────────┤
│  LAYER 1: INSTRUMENTATION & COLLECTION              │
│  traceAI register · SDK decorators · Auto-instr.    │
│  Span enrichment · Sampling · Export to backends    │
└─────────────────────────────────────────────────────┘
```

Key insight: In 2025, these layers were often conflated into a single tool. In 2026, the best teams use **composable layers** — one standard for telemetry (OTel), pluggable backends for storage, and eval logic that runs both offline and inline.

**Facilitator Notes:**
- Draw this on a whiteboard as three stacked boxes
- Ask students: "Which layer does your team have today? Which is missing?"
- Common student question: "Do I need all three?" — Yes, but you can adopt incrementally (Layer 1 first)
- Time: 5 minutes
- Emphasise that most teams skip Layer 3 (evaluation) and pay for it in silent quality degradation

---

### [NEW 2026] Slide 2: OpenTelemetry for AI — The New Standard
**Insert after:** Slide 1 (The 2026 Stack)
**Format:** Concept explanation + code example

**Content:**

**OpenTelemetry GenAI Semantic Conventions** (graduated to stable in 2025) define how LLM calls, tool invocations, and retrieval operations are represented as distributed traces.

Three complementary specs exist:
| Spec | Maintainer | Focus |
|------|-----------|-------|
| **OTel GenAI SemConv** | OpenTelemetry (CNCF) | Standard `gen_ai.*` attributes for model calls |
| **OpenInference** | Arize AI | Extended semantic conventions for agents, RAG, embeddings |
| **OpenLLMetry** | Traceloop | Auto-instrumentation libraries for popular SDKs |

The **canonical formula** for 2026:
```
OTel GenAI + OpenInference + eval-as-span-attribute = complete AI observability
```

Key attributes captured per span:
- `gen_ai.system` — provider (openai, anthropic, bedrock)
- `gen_ai.request.model` — model ID
- `gen_ai.usage.input_tokens` / `output_tokens`
- `gen_ai.response.finish_reason`
- OpenInference adds: `embedding.model_name`, `retrieval.documents`, `tool.name`, `tool.parameters`

**Facilitator Notes:**
- Show the OTel blog post (May 2026) live if internet is available
- Common student question: "Does this replace vendor-specific SDKs?" — Not entirely; vendor SDKs add convenience, but they now export via OTel under the hood (e.g., Langfuse v3)
- Time: 5 minutes
- ⚡ ADVANCED: Show the `traceAI` register pattern for auto-instrumentation

---

### [NEW 2026] Slide 3: The traceAI Register Pattern
**Insert after:** Slide 2
**Format:** Code walkthrough

**Content:**

The dominant instrumentation pattern in 2026 — two lines to instrument any LLM provider:

```python
from openinference.instrumentation import traceAI
import openai

# One line to instrument all OpenAI calls
traceAI('openai')

# Or with Anthropic
traceAI('anthropic')

# Or with Bedrock
traceAI('bedrock')

# All subsequent calls automatically emit OTel spans
# with gen_ai.* and OpenInference attributes
client = openai.Client()
response = client.chat.completions.create(...)
# ^ This now produces a full trace span automatically
```

**Span enrichment** (adding custom scores to existing spans):
```python
from opentelemetry import trace

span = trace.get_current_span()
span.set_attribute("eval.faithfulness", 0.92)
span.set_attribute("eval.relevance", 0.87)
span.set_attribute("cost.usd", 0.0034)
```

This pattern is used by: Arize Phoenix, Langfuse v3, MLflow, Dynatrace, Datadog.

**Facilitator Notes:**
- This is the "hello world" of AI observability in 2026 — make sure every student sees this
- Common question: "What about LangChain/LlamaIndex?" — Both have OpenInference auto-instrumentors
- Time: 4 minutes
- ⚡ ADVANCED: Discuss span sampling strategies for high-throughput production systems

---

### [NEW 2026] Slide 4: Langfuse v3 — What Changed
**Insert after:** Original Langfuse section
**Format:** Comparison table + concept

**Content:**

Langfuse v3 (GA June 2025, major updates through 2026) represents a fundamental architecture shift:

| Aspect | Langfuse v2 (legacy) | Langfuse v3 (current) |
|--------|---------------------|----------------------|
| **Core table** | Traces (hierarchical) | **Observations** — every LLM call, tool, agent step is a queryable row |
| **SDK foundation** | Custom decorators | **OpenTelemetry-native** — uses OTel exporters |
| **Evaluation** | Manual scores attached to traces | **Evals as code**: Python/TypeScript functions in UI, run on live data or datasets |
| **Monitoring** | Dashboard only | **Threshold-based monitors** with alerts (cost, quality, latency) |
| **Agent support** | Basic nesting | Deep agent tracing — single trace can contain thousands of operations |
| **Search** | Filters | **Natural language search** (powered by Bedrock, zero-retention) |

Key 2026 additions:
- **Monitors & Alerts** (June 2026): Define metric thresholds, get notified on drift
- **Custom evaluator functions**: Write Python/TS evals directly in Langfuse UI, attach to live observations
- **MCP integration**: Langfuse skill for AI coding assistants (Claude Code, etc.) — set up observability without leaving editor

**Why the shift to "observations" matters:**
> "As agentic applications grow more complex, a single trace can contain thousands of operations, and the interesting ones are rarely at the top level." — Langfuse team

**Facilitator Notes:**
- If students have used Langfuse before, emphasise that the v3 mental model is different
- Demo: Show the observations table view vs. the old trace tree view
- Common question: "Is Langfuse still free/open-source?" — Yes, self-hostable; cloud has generous free tier
- Time: 5 minutes

---

### [NEW 2026] Slide 5: Evals as Code — The New Discipline
**Insert after:** Original "Evaluation strategies" section
**Format:** Concept explanation + workflow diagram

**Content:**

**"Evals as code"** = Treating LLM evaluations like unit tests: version-controlled, automated, gating deployments.

```
Development                    CI/CD                         Production
┌──────────┐    ┌──────────────────────────┐    ┌──────────────────────┐
│ Write    │    │ PR triggers eval suite   │    │ Online scoring on    │
│ eval     │───▶│ 100+ test cases run      │───▶│ live traffic (sample)│
│ function │    │ Regression gate: PASS/FAIL│    │ Failures → new tests │
└──────────┘    └──────────────────────────┘    └──────────────────────┘
                         │                                │
                         ▼                                ▼
                    Block deploy if                Convert production
                    quality drops                  failures into new
                                                  regression test cases
```

The defining insight: **production failures should automatically become new test cases**, creating a flywheel that makes the system more robust with every deployment.

Tools supporting this pattern:
| Tool | Evals-as-code support |
|------|----------------------|
| **Braintrust** | Strongest — full CI/CD integration, auto-regression from production |
| **Langfuse v3** | Custom evaluator functions in UI + dataset experiments |
| **CircleCI Evals Orb** | Vendor-agnostic CI integration |
| **DeepEval** | Open-source pytest plugin for LLM evals |
| **Athina** | Evals in CI/CD with custom scorers |
| **Dagger** | "Evals as code" native — containerised eval pipelines |

Stat: **42% of companies abandoned the majority of their AI initiatives in 2025** (S&P Global) — most because the system shipped fine then *silently got worse* without anyone catching it.

**Facilitator Notes:**
- This is the single most impactful practice to teach — it prevents "silent AI degradation"
- Draw the flywheel on whiteboard: ship → monitor → fail → test case → block → fix → ship
- Common question: "How many test cases do I need?" — Start with 50-100 covering key personas/scenarios, grow from production failures
- Time: 6 minutes

---

### [NEW 2026] Slide 6: LLM-as-Judge in 2026 — Beyond Simple Scoring
**Insert after:** Slide 5 (Evals as Code)
**Format:** Concept + comparison table

**Content:**

LLM-as-Judge has moved from "use GPT-4 to score things" to a **rigorous evaluation discipline** with known failure modes and calibration methods.

**Three judging techniques:**
| Technique | How It Works | Best For |
|-----------|-------------|----------|
| **Pointwise (G-Eval)** | Judge scores a single output on a rubric (1-5 Likert) | General quality assessment |
| **Pairwise** | Judge picks the better of two outputs | Comparing model versions |
| **Listwise** | Judge ranks N outputs simultaneously | Choosing best among candidates |

**Known biases to calibrate against:**
- **Length bias**: Judges favour longer responses (~30% effect)
- **Family bias**: GPT-4 judges favour GPT-4 outputs over Claude outputs (and vice versa)
- **Position bias**: In pairwise, judges favour the first option presented
- **Self-enhancement bias**: Models rate their own outputs higher

**Calibration protocol (2026 best practice):**
1. Run judge on 50-100 human-annotated examples
2. Compute Cohen's κ (inter-annotator agreement) — target ≥ 0.7
3. If κ < 0.7: refine rubric, add few-shot examples, or switch judge model
4. Report κ alongside all judge scores in production

**Cost control:** A 100-case eval suite with GPT-4o as judge costs ~$2-5. Running on every PR is affordable.

**Facilitator Notes:**
- Show that LLM-as-judge is NOT just "ask GPT to rate this" — it's a measurement system that needs calibration
- Common question: "Which model should be the judge?" — Generally the strongest model you can afford; cross-family judging reduces bias
- Advanced: Discuss fine-tuned judge models (Galileo Luna-2, Patronus Lynx) for sub-200ms inline scoring
- Time: 6 minutes

---

### [NEW 2026] Slide 7: Agent-Specific Observability — Four Dimensions
**Insert after:** Original "What to instrument" section
**Format:** Framework/concept

**Content:**

Agent observability requires tracing across **four dimensions** that traditional APM doesn't cover:

| Dimension | What It Captures | Why It Matters |
|-----------|-----------------|---------------|
| **1. Execution traces** | Full reasoning chain: LLM calls → tool invocations → subagent handoffs → verification loops | Agents fail in mid-sequence, not at endpoint |
| **2. Output evaluations** | Per-step quality scoring (faithfulness, tool correctness, goal progress) | An agent can "succeed" (no error) while producing garbage |
| **3. Token cost attribution** | Per-agent, per-user, per-task, per-tenant cost breakdown | A single agent run can cost $0.01 or $5.00 depending on path taken |
| **4. Identity tracking** | Which agent, which version, which model, which harness config | Multi-agent systems need per-agent forensics |

**The key failure mode agents introduce:**
> "Traditional APM catches crashes. Agent observability catches *correct execution that produces wrong results*."

Example: An agent that successfully calls 12 tools, receives valid responses from all of them, and produces a confident final answer that is factually wrong — every span shows green, but the output is a hallucination. Only Layer 3 (evaluation) catches this.

**Facilitator Notes:**
- Use the "all green, all wrong" example to drive home why eval is non-optional for agents
- Ask: "If your agent runs 15 tool calls and the final answer is wrong, how do you find which step introduced the error?" — This is what per-step evaluation solves
- Time: 5 minutes

---

### [NEW 2026] Slide 8: Multi-Agent Cost Attribution Patterns
**Insert after:** Slide 7 (Agent-Specific Observability)
**Format:** Concept + code pattern

**Content:**

Cost attribution for multi-agent systems is **multi-dimensional** — you need breakdowns by:
- Per-user (who triggered it)
- Per-task (what was being accomplished)
- Per-agent (which specialist consumed the tokens)
- Per-workflow (which orchestration path was taken)
- Per-tenant (for multi-tenant SaaS)

**The reliable pattern** (tag at trace root, propagate through children):

```python
# At trace root — tag with all attribution dimensions
span = trace.get_current_span()
span.set_attribute("attribution.user_id", "user_123")
span.set_attribute("attribution.task_id", "research_task_456")
span.set_attribute("attribution.tenant", "acme_corp")
span.set_attribute("attribution.workflow", "multi_agent_research")

# Each child span (subagent, tool call) inherits via context propagation
# Observability platform aggregates cost by any dimension
```

**Common failure modes in agent cost:**
| Failure | What Happens | How to Catch |
|---------|-------------|-------------|
| **Runaway agent** | Agent loops or retries indefinitely, burning $50+ on a $0.10 task | Max-token budget per trace; alert at 5x expected cost |
| **Context stuffing** | Agent loads excessive context on every LLM call | Track input_tokens per span; alert on >50% of window used |
| **Subagent explosion** | Orchestrator spawns too many subagents | Count spans per trace; alert on >N total calls |
| **Model misrouting** | Complex tasks routed to expensive model when cheap model suffices | Compare model usage vs. task complexity |

**Production rule:** Instrument cost attribution on Day One. Retroactive tagging from logs always misses edge cases and under-reports long agentic traces.

**Facilitator Notes:**
- This is critical for any team running agents in production — "who pays for this?" is always the first enterprise question
- Common question: "How do we set budgets?" — Start with 10x the median cost as alert threshold, tighten over time
- Time: 5 minutes
- ⚡ ADVANCED: Discuss quality-bounded cost optimisation (routing to cheaper models only when quality remains above threshold)

---

### [NEW 2026] Slide 9: The 2026 Vendor Landscape — Who Does What
**Insert after:** Original "Observability tools" section
**Format:** Comparison table

**Content:**

The AI observability market consolidated significantly in early 2026. Here's the current landscape:

| Platform | Primary Strength | Open Source? | Best For |
|----------|-----------------|-------------|----------|
| **Braintrust** | Evals + CI/CD integration + production monitoring loop | No (generous free tier: 1M spans/month) | Teams wanting eval-gated deployments |
| **Langfuse v3** | OTel-native tracing + prompt management + custom evals | Yes (self-hostable) | Teams wanting full control + OSS |
| **Arize Phoenix** | Drift detection + clustering + production forensics | Yes (open source) | Teams needing production anomaly detection |
| **Galileo** | Sub-200ms runtime guardrails (Luna-2 evaluator models) | No | Teams needing inline quality blocking |
| **Latitude** | Issue lifecycle tracking (active→resolved→regressed) | Partial | Teams wanting Sentry-like error management for AI |
| **DeepEval** | Pytest plugin for LLM evals + 14 built-in metrics | Yes | Developers wanting test-first eval in CI |
| **LangSmith** | Deep LangChain/LangGraph integration + annotation workflows | No | LangChain-native teams |
| **Datadog LLM Obs** | Unified infra + LLM monitoring for existing Datadog users | No | Enterprise with existing Datadog investment |
| **AWS CloudWatch GenAI** | Native Bedrock integration + Guardrails monitoring | AWS service | AWS-native teams |
| **MLflow** | Model registry + eval + OSS standard for ML lifecycle | Yes | Teams already using MLflow for MLOps |

**Decision framework:**
1. Already on AWS Bedrock? → CloudWatch GenAI + Langfuse for evals
2. Need OSS self-hosted? → Langfuse v3 + Arize Phoenix
3. Want fastest CI/CD integration? → Braintrust or DeepEval
4. Need real-time blocking? → Galileo or Bedrock Guardrails
5. LangChain shop? → LangSmith + DeepEval for CI

**Facilitator Notes:**
- Emphasise: the tool doesn't matter as much as the *practice* — any tool with OTel support works
- Students will ask "which should I pick?" — Guide them through the decision framework above
- Note: This landscape shifts every 6 months; teach the principles, not the product names
- Time: 5 minutes

---

### [NEW 2026] Slide 10: Online vs. Offline Evaluation — The Full Taxonomy
**Insert after:** Slide 9 (Vendor Landscape)
**Format:** Framework/comparison

**Content:**

The 2026 consensus distinguishes **four evaluation modes** (not just "offline" and "online"):

| Mode | When It Runs | Latency Budget | Purpose |
|------|-------------|---------------|---------|
| **Experiments** (offline) | Before deployment; on datasets | Unlimited | Regression testing, model comparison |
| **CI gate** (pre-deploy) | On every PR/commit | Minutes | Block quality regressions before ship |
| **Online scoring** (post-deploy) | On sampled production traffic | Seconds | Detect drift, catch edge cases |
| **Runtime guardrails** (inline) | On every request in real-time | <200ms | Block harmful/wrong outputs before user sees them |

**The evaluation cascade** (how production teams wire these together):

```
[Every PR]           [Every deploy]        [Every request]       [Sampled]
    │                     │                      │                   │
    ▼                     ▼                      ▼                   ▼
 CI eval suite      Canary eval on         Runtime guardrails    Async LLM-as-judge
 (100+ cases)       10% traffic            (Bedrock/Galileo)     on 5% of traffic
 PASS/FAIL gate     Compare to baseline    Block bad outputs     Score for drift
```

**Key insight:** Runtime guardrails and LLM-as-judge are **not the same thing**:
- Guardrails = fast, deterministic or fine-tuned model, blocking action, <200ms
- LLM-as-judge = slow, general-purpose model, scoring/labelling, 1-10 seconds

You need both: guardrails for safety, judge for quality measurement.

**Facilitator Notes:**
- Draw the cascade on whiteboard — this is the "ideal end state" students should aim for
- Common question: "Can I start with just one?" — Yes. Start with CI gate (cheapest, highest ROI), add online scoring next, add guardrails last
- Time: 5 minutes

---

### [NEW 2026] Slide 11: AWS Bedrock Guardrails + Automated Reasoning (2026)
**Insert after:** Original AWS CloudWatch section
**Format:** Concept + architecture

**Content:**

AWS Bedrock's observability and guardrails stack has expanded significantly in 2025-2026:

**Bedrock Guardrails — What's New:**
- **Automated Reasoning checks** (April 2026): Formal verification using mathematical logic to validate AI outputs against defined rules and constraints. Not probabilistic — provably correct.
- **AgentCore policy guardrails** (June 2026): Guardrails evaluate *every* agent action (tool calls, model calls, inter-agent messages) in real-time
- **Content filters + PII detection + denied topics** — now with per-policy granularity

**Architecture:**
```
User Request → Bedrock Agent → [Tool Call]
                   │                │
                   ▼                ▼
           Input Guardrail    Tool Guardrail
           (prompt check)     (action check)
                                    │
                                    ▼
                              Tool Execution
                                    │
                                    ▼
                           Output Guardrail
                           (response check)
                           + Automated Reasoning
                                    │
                                    ▼
                              User Response
```

**CloudWatch GenAI Observability:**
- Native metrics for Bedrock model invocations (latency, tokens, errors)
- Guardrail-specific metrics: filter rate, violation counts, action types blocked
- Custom dashboards combining infra metrics + AI-specific metrics

**Key production patterns:**
1. Set up CloudWatch alarms on guardrail violation rate (alert if >5% of requests trigger)
2. Use Automated Reasoning for compliance-critical outputs (financial, medical, legal)
3. Track cost per model invocation via CloudWatch cost attribution tags

**Facilitator Notes:**
- Emphasise Automated Reasoning as a differentiator — no other provider offers formal verification for LLM outputs
- Demo: Show Bedrock console → Guardrails → Test interface
- Common question: "Does this add latency?" — Yes, ~50-150ms per guardrail check; design for it
- Time: 5 minutes

---

### [NEW 2026] Slide 12: Context Rot & Semantic Drift — Named Failure Modes
**Insert after:** Original "alerting and drift detection" section
**Format:** Concept explanation

**Content:**

Two failure modes that are now well-documented observability targets:

**Context Rot:**
Model performance degrades **30%+** when key content falls in mid-window positions — even with million-token context windows. (Stanford "Lost in the Middle" study, corroborated by Chroma research 2025)

Observable signals:
- Quality scores drop as context length increases
- Important-information-position vs. accuracy correlation
- Tool call success rate declining for long-running agents

**Semantic Drift:**
The AI system's outputs gradually shift in tone, accuracy, or behaviour over time — often undetectable without systematic measurement.

Causes:
- Model provider updates (silent model version changes)
- Shifting input distribution (user behaviour changes)
- RAG knowledge base staleness (retrieved context becomes outdated)
- Prompt entropy accumulation in long-running agents

**How to instrument for both:**
| Failure Mode | Observable Metric | Alert Threshold |
|---|---|---|
| Context rot | Quality score × context length correlation | r > -0.3 (negative correlation = rot) |
| Semantic drift | Week-over-week quality score delta | >5% decline sustained 3 days |
| Model version change | Response distribution shift (embedding distance) | >0.15 cosine shift from baseline |
| RAG staleness | Knowledge freshness score (days since source update) | >30 days average |

**Facilitator Notes:**
- "Context rot" is a powerful concept students remember — use it as a hook
- Show a hypothetical chart: quality score vs. context tokens filled — the "U-shape" where beginning and end of context are fine, middle degrades
- Time: 4 minutes

---

### [NEW 2026] Slide 13: Building an Eval Suite from Scratch
**Insert after:** Slide 5 (Evals as Code)
**Format:** Hands-on activity / code walkthrough

**Content:**

**Practical: Build a minimal eval suite in Python (using DeepEval)**

```python
# eval_suite.py — runs in CI on every PR
from deepeval import evaluate
from deepeval.metrics import (
    AnswerRelevancyMetric,
    FaithfulnessMetric,
    HallucinationMetric
)
from deepeval.test_case import LLMTestCase

# Define test cases from known-good examples
test_cases = [
    LLMTestCase(
        input="What is the capital of France?",
        actual_output=my_llm_app("What is the capital of France?"),
        expected_output="Paris",
        retrieval_context=["France is a country in Europe. Its capital is Paris."]
    ),
    # Add 50-100 cases covering key scenarios...
]

# Define metrics
metrics = [
    AnswerRelevancyMetric(threshold=0.7),
    FaithfulnessMetric(threshold=0.8),
    HallucinationMetric(threshold=0.5),  # lower = fewer hallucinations
]

# Run evaluation — this gates deployment
results = evaluate(test_cases, metrics)

# In CI: exit(1) if any metric below threshold
for result in results:
    if not result.success:
        print(f"FAILED: {result.metric_name} = {result.score}")
        exit(1)
```

**CI integration (GitHub Actions example):**
```yaml
- name: Run LLM Evals
  run: python eval_suite.py
  env:
    OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
```

**Facilitator Notes:**
- Walk through this code line by line
- Key insight: This is no harder than writing unit tests — the barrier is cultural, not technical
- Common question: "What if my LLM app is non-deterministic?" — That's why you use statistical thresholds (0.7, 0.8) not exact match
- Time: 8 minutes (extended activity)

---

### [NEW 2026] Slide 14: Streaming Evaluation — Metrics That Matter
**Insert after:** Slide 12 (Context Rot)
**Format:** Concept + metrics table

**Content:**

For streaming LLM applications (most production UIs), evaluation isn't a single "quality" number — it's **four distinct metrics**:

| Metric | What It Measures | Target (2026 benchmarks) |
|--------|-----------------|-------------------------|
| **TTFT** (Time to First Token) | How fast the first token appears | <500ms for chat, <200ms for autocomplete |
| **Inter-token P99** | 99th percentile time between consecutive tokens | <50ms (feels "smooth") |
| **Mid-stream consistency** | Does the response contradict itself mid-generation? | <2% contradiction rate |
| **Premature termination** | Response cuts off before completing the thought | <1% of responses |

**Why this matters:**
A response can score 5/5 on quality but feel terrible to users because TTFT is 3 seconds or tokens arrive in bursts.

Production observability should track both:
- **Quality metrics** (faithfulness, relevance, hallucination)
- **Experience metrics** (TTFT, throughput, completion rate)

**Facilitator Notes:**
- Quick demo: Open any streaming LLM UI and point out the "thinking..." delay (TTFT) vs. token flow
- Students from traditional web dev will recognize parallels to TTFB and CLS (web vitals)
- Time: 3 minutes
- SKIP FOR BEGINNERS — advanced students only

---

### [NEW 2026] Slide 15: The Arize AX Vision — Self-Improving Agents
**Insert after:** Slide 9 (Vendor Landscape)
**Format:** Case study / emerging concept

**Content:**

**Emerging concept: "AI Factory for Self-Improving Agents"** (Arize, Observe 2026 conference)

The vision: observability is not just for debugging — it's the **feedback loop that makes agents better automatically**.

```
[Agent runs in production]
         │
         ▼
[Observability captures trace + eval scores]
         │
         ▼
[Automated failure clustering — group similar failures]
         │
         ▼
[Root cause identification — which component failed?]
         │
         ▼
[Automated fix suggestion — new prompt / tool / routing]
         │
         ▼
[Eval validates fix — run against failure cluster]
         │
         ▼
[Deploy improved agent — self-healing loop]
```

**Where we are today (mid-2026):**
- Failure clustering: ✅ Available (Arize, Latitude, Braintrust)
- Root cause identification: ⚠️ Semi-automated (requires human confirmation)
- Automated fix: 🔬 Research stage (Arize AX early preview)
- Full loop: ❌ Not yet production-ready

**Why teach this now:** Students should understand this is the direction — build observability today with the data that will power automated improvement tomorrow.

**Facilitator Notes:**
- Frame as "the north star" — not what they'll build today, but what good observability enables
- Common question: "Is this real or hype?" — The clustering and failure identification parts are real and production-grade today. The automated fix loop is emerging.
- Time: 4 minutes

---

### [NEW 2026] Slide 16: Observability for RAG Systems — Specific Metrics
**Insert after:** Slide 7 (Agent-Specific Observability)
**Format:** Metrics table + concept

**Content:**

RAG systems need **retrieval-specific observability** beyond general LLM metrics:

| Metric | What It Measures | How to Compute | Alert Threshold |
|--------|-----------------|---------------|-----------------|
| **Retrieval recall@k** | Of relevant docs, how many were retrieved? | Compare against labelled golden set | <0.7 |
| **Retrieval precision@k** | Of retrieved docs, how many were relevant? | Judge (LLM or human) per query | <0.5 |
| **Context utilisation** | How much of retrieved context actually appeared in the answer? | Token overlap analysis | <30% (wasteful retrieval) |
| **Faithfulness** | Does the answer only contain claims supported by retrieved context? | RAGAS / NLI-based | <0.8 |
| **Answer relevance** | Does the answer actually address the question? | Cosine similarity or judge | <0.7 |
| **Knowledge freshness** | Average age of retrieved documents | Timestamp analysis | >30 days |
| **Chunk hit rate** | % of queries that find at least one relevant chunk | Binary per query | <90% |

**Production RAG monitoring dashboard should show:**
1. Daily average faithfulness and relevance scores
2. Retrieval latency P50/P95/P99
3. Zero-result query rate (queries that find no chunks)
4. Top-failing query clusters (grouped by topic)
5. Cost per query (embedding + LLM + retrieval)

**Facilitator Notes:**
- If you've covered Module 8 (RAG), connect back to the RAGAS metrics discussed there
- Demo: Show what a Langfuse trace looks like for a RAG query (retrieval span → LLM span → eval scores)
- Time: 5 minutes

---

### [NEW 2026] Slide 17: The 90-Day Observability Rollout Plan
**Insert after:** "Building a feedback loop" section
**Format:** Process / timeline

**Content:**

Practical phased plan from "no instrumentation" to "deterministic incident replay":

**Days 1–30: Foundation**
- [ ] Add traceAI instrumentation to all LLM calls
- [ ] Set up OTel exporter to chosen backend (Langfuse/Phoenix/Braintrust)
- [ ] Tag spans with user_id, task_type, model_version
- [ ] Build first dashboard: latency, token usage, cost, error rate
- [ ] Set basic alerts: error rate >5%, latency P99 >10s, daily cost >$X

**Days 31–60: Evaluation**
- [ ] Write 50-case eval suite covering key user scenarios
- [ ] Add CI gate: evals run on every PR, block on regression
- [ ] Deploy LLM-as-judge on 5% of production traffic (async)
- [ ] Set up weekly quality report: average scores + trends + top failures
- [ ] Create first "failure → test case" feedback loop

**Days 61–90: Advanced**
- [ ] Add runtime guardrails on critical paths (PII, safety, factuality)
- [ ] Implement per-agent cost attribution (if multi-agent)
- [ ] Deploy drift detection: alert on week-over-week quality decline
- [ ] Build incident replay capability: given a failed trace, recreate exact inputs
- [ ] Establish eval review cadence: weekly review of new failure clusters

**Facilitator Notes:**
- This is the "take-away action plan" — students should screenshot or save this
- Common question: "We're already at day 60+" — Celebrate! Then ask about guardrails and drift detection
- Time: 4 minutes

---

### [NEW 2026] Slide 18: Hands-On Lab — Build an Observability Dashboard
**Insert after:** Original hands-on activity section
**Format:** Hands-on activity (replacement/extension of original)

**Content:**

**Updated Lab: Wire Up a Complete Observability Stack (20 min)**

**Objective:** Set up instrumentation, capture a trace, attach an eval score, and trigger an alert.

**Prerequisites:** Python 3.10+, OpenAI API key (or Bedrock access)

**Steps:**

1. **Install** (2 min):
```bash
pip install openai openinference-instrumentation-openai langfuse
```

2. **Instrument** (3 min):
```python
from openinference.instrumentation import traceAI
from langfuse import Langfuse

# Connect to Langfuse (free cloud account)
langfuse = Langfuse()

# Auto-instrument OpenAI
traceAI('openai')
```

3. **Generate traces** (3 min):
```python
import openai
client = openai.Client()

# Run 10 queries — each generates a trace automatically
questions = ["What is RAG?", "Explain transformers", ...]
for q in questions:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": q}]
    )
```

4. **Attach eval scores** (5 min):
```python
# Score each trace for relevance (manual for demo; automate in production)
for trace in langfuse.get_traces(limit=10):
    langfuse.score(
        trace_id=trace.id,
        name="relevance",
        value=0.85,  # In production: compute this with LLM-as-judge
    )
```

5. **Set up a monitor** (3 min):
    - In Langfuse UI → Monitors → New Monitor
    - Metric: average relevance score
    - Threshold: alert if drops below 0.7
    - Window: last 1 hour

6. **Trigger the alert** (4 min):
    - Send 5 deliberately bad queries (nonsense input)
    - Observe the score drop in the dashboard
    - Verify alert fires

**Expected outcome:** Students have a working observability stack with traces, evals, and alerting — in 20 minutes.

**Facilitator Notes:**
- Have a pre-configured Langfuse cloud project as backup if students have setup issues
- Alternative for AWS-native: Use Bedrock + CloudWatch instead of OpenAI + Langfuse
- Time: 20 minutes (this replaces the original activity)

---

### [NEW 2026] Slide 19: Anti-Patterns — How Observability Goes Wrong
**Insert after:** Slide 17 (90-Day Plan)
**Format:** Common mistakes / discussion

**Content:**

**Five ways teams get AI observability wrong:**

| Anti-Pattern | What Happens | The Fix |
|---|---|---|
| **"Log everything, look at nothing"** | Terabytes of traces accumulate but no one reviews them. Alerts fire so often they're ignored. | Define 3-5 metrics that matter. Review weekly. Alert only on actionable thresholds. |
| **"Eval in staging only"** | System works perfectly in dev; degrades silently in production. | Online scoring on sampled production traffic is non-negotiable. |
| **"Judge without calibrating"** | LLM-as-judge produces scores nobody trusts. Scores fluctuate without explanation. | Calibrate against human labels (κ ≥ 0.7) before trusting automated scores. |
| **"Trace without attribution"** | You know something is expensive but can't tell which user, agent, or feature caused it. | Tag at the root span. Always. Day one. |
| **"Metrics without action"** | Beautiful dashboards, zero follow-through when metrics decline. | Every alert must have a documented response: who investigates, what they check, what they can change. |

**Discussion question:** "Which anti-pattern is your team most likely to fall into? What would you do differently based on what you've learned today?"

**Facilitator Notes:**
- Use this as a reflection slide near the end of the module
- Each anti-pattern resonates with different student backgrounds — let the room identify which they've seen
- Time: 4 minutes

---

### [NEW 2026] Slide 20: Knowledge Check Updates — 2026 Edition
**Insert after:** Original Knowledge Check section
**Format:** Quiz (supplementary questions)

**Content:**

**Additional quiz questions reflecting 2026 material:**

Q6. What is the "traceAI register pattern" used for in 2026 AI observability?
- A) Training a model to trace its own reasoning
- B) Auto-instrumenting LLM SDK calls to emit OpenTelemetry spans ✅
- C) Registering models with a central model registry
- D) Creating trace-based unit tests

Q7. In the "evals as code" discipline, what happens when a production failure is detected?
- A) The system is immediately rolled back
- B) An alert is sent and a human investigates
- C) The failure is automatically converted into a new regression test case ✅
- D) The model is retrained on the failure example

Q8. What is "context rot" in the context of AI observability?
- A) When the context window fills up and the model stops responding
- B) Performance degradation when key content falls in mid-window positions ✅
- C) When cached prompts expire and need refreshing
- D) Data corruption in the vector store over time

Q9. Which evaluation mode has a latency budget of <200ms and blocks harmful outputs in real-time?
- A) Offline experiments
- B) CI gate evaluation
- C) Online scoring (async)
- D) Runtime guardrails ✅

Q10. In multi-agent cost attribution, what is the "reliable pattern" for tracking costs?
- A) Count total tokens at the end and divide by number of agents
- B) Tag attribution dimensions at the trace root and propagate through children ✅
- C) Use the model provider's billing API to disaggregate after the fact
- D) Assign a fixed cost budget to each agent at deployment time

**Facilitator Notes:**
- Use Q6-Q10 as supplementary to the original Q1-Q5
- For advanced groups, use all 10; for beginners, stick with original 5 + Q6 and Q8

---

## FACILITATOR UPDATE BRIEF

---

### 🎤 Top 3 Most Important Additions

1. **Evals as Code + CI Gating (Slide 5 + 13)** — This is the single highest-ROI practice missing from the original. The stat that 42% of companies abandoned AI initiatives due to silent degradation makes the business case visceral. Every student should leave knowing how to write an eval suite that blocks bad deployments.

2. **OpenTelemetry for AI / traceAI pattern (Slides 2-3)** — The original mentioned OTel in passing. In 2026 it's the foundation. The `traceAI('openai')` one-liner is the new "hello world" of observability. Students who don't know this will look outdated in any job interview.

3. **Agent-Specific Observability + Cost Attribution (Slides 7-8)** — With multi-agent systems now shipping in production, the "four dimensions" framework and cost tagging patterns are immediately applicable for anyone building agents.

---

### 🔄 What's Now Outdated in the Original

| Original Content | Status | How to Handle |
|---|---|---|
| Langfuse described as "decorator-based tracing" | **Outdated** — v3 is OTel-native with observations table | Replace with Slide 4; note the migration path |
| Phoenix described as standalone open-source tool | **Partially outdated** — Now "Arize Phoenix" with expanded agent tracing + AX vision | Update in passing; add Slide 15 |
| "Hallucination rate" as the primary metric | **Incomplete** — Still important but now part of a broader eval taxonomy | Expand with Slides 6, 10, 14 |
| CloudWatch mentioned generically | **Outdated** — Bedrock Guardrails + Automated Reasoning + GenAI Observability are specific capabilities | Replace with Slide 11 |
| A/B testing as the primary online evaluation method | **Outdated** — Online scoring, runtime guardrails, and eval cascades have supplanted simple A/B | Replace with Slide 10 |

---

### ⏱️ Fitting New Content into 60 Minutes

**Recommended approach: 75-minute extended version**

This module genuinely has too much important new content for 60 minutes. Recommend:

- **60-min version:** Keep original structure but swap in updated content for Slides 1-5, 7, 9-11. Replace original lab with updated lab (Slide 18). Skip Slides 14, 15, 19 (mark as recommended self-study).

- **75-min version (recommended):** All slides. The additional 15 minutes covers agent observability, cost attribution, and the 90-day plan — content that is immediately actionable for any team deploying agents.

- **90-min deep-dive version:** Add the full eval suite build lab (Slide 13) as a 20-min hands-on exercise rather than a walkthrough.

**Suggested 75-min agenda:**
| Time | Content | Slides |
|------|---------|--------|
| 0-5 | The 2026 observability stack overview | Slide 1 |
| 5-15 | OTel for AI + traceAI pattern | Slides 2-3 |
| 15-20 | Langfuse v3 what changed | Slide 4 |
| 20-30 | Evals as code + LLM-as-judge | Slides 5-6 |
| 30-40 | Agent-specific observability + cost attribution | Slides 7-8 |
| 40-45 | Vendor landscape 2026 | Slide 9 |
| 45-50 | Online eval taxonomy + Bedrock Guardrails | Slides 10-11 |
| 50-55 | Context rot + drift + streaming metrics | Slides 12, 14 |
| 55-65 | Hands-on lab | Slide 18 |
| 65-70 | 90-day plan + anti-patterns | Slides 17, 19 |
| 70-75 | Knowledge check + close | Slide 20 |

---

### 🛠️ New Tools/Accounts/Demos to Set Up in Advance

1. **Langfuse Cloud account** (free) — for live demo and student lab
2. **OpenAI API key** (or Bedrock access) — for generating traces in the lab
3. **DeepEval installed** — `pip install deepeval` — for showing eval-as-code pattern
4. **Arize Phoenix local instance** (optional) — `pip install arize-phoenix` and run `phoenix serve` for a local demo of drift detection
5. **AWS console access** — for showing Bedrock Guardrails + CloudWatch GenAI dashboards (if AWS-native audience)
6. **Pre-built Langfuse project** with ~50 traces already captured — as backup if student instrumentation fails during lab

---

*Module 15 Update — AI & Agentic AI Training Programme — July 2026*
