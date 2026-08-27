# Module 06 — AI Development Lifecycle (AI-DLC)
## 🔄 2026 Update: Gap Analysis, New Slides & Facilitator Notes

---

## GAP ANALYSIS

The original module was built around a traditional "AI-DLC vs SDLC" framing with 6 stages (Discover → Design → Develop → Evaluate → Deploy → Monitor). Since early 2025, the landscape has shifted substantially:

### What's Now Outdated or Incomplete

1. **The SDLC itself has been rewritten by AI agents.** The framing of "AI-DLC as a variant of SDLC" is now incomplete — the SDLC is being rebuilt around AI agents. 41% of all code is AI-generated (2026 data). The original module treats AI as the *product* being built through a lifecycle, but doesn't address AI as a *participant* in the lifecycle itself.

2. **"Prompt engineering as a development discipline" is now too narrow.** The field has evolved to **context engineering** (managing what the model sees and when) and **spec-driven development** (specs as the unit of work that coordinate agents). The original framing stops at prompt versioning.

3. **MLOps/LLMOps distinction needs updating.** MLflow 3.10 (March 2026) now covers GenAI agent observability, LLM tracing, multi-turn conversation evaluation, and cost tracking. The tool landscape has matured significantly — LLMOps is no longer "MLOps plus a few extras."

4. **Evaluation coverage lacks CI/CD integration.** The original mentions RAGAS and benchmarks but doesn't cover **evals-as-code** — the practice of running automated LLM evaluations as CI/CD gates. This is now table stakes for any production AI team.

5. **Vibe coding is absent.** Coined by Andrej Karpathy in Feb 2025 and named Collins Dictionary Word of the Year, 92% of US developers use AI tools daily, with 41% of code being AI-generated. The module doesn't address the productivity gains, quality risks, or governance implications.

6. **Prompt management tools are not covered.** A $4.7B market has emerged: PromptLayer, Braintrust, Langfuse, LangSmith, etc. — treating prompts as versioned, deployable artifacts with environment promotion (staging → production).

7. **Responsible AI gates are under-specified.** The original mentions "checkpoints" but doesn't detail what automated gates look like: red-teaming in CI, bias detection, EU AI Act compliance checks, or tripwire mechanisms.

8. **Spec-Driven Development (SDD) is completely absent.** Microsoft, Amazon (Kiro), and GitHub have all released spec-driven tooling in 2026. Specs are becoming the shared source of truth for both humans and AI agents throughout the lifecycle.

9. **The Agentic SDLC concept is missing.** The notion that agents participate across all 7 SDLC stages (requirements → architecture → code → review → test → deploy → operate) with 21–55% productivity lifts per developer is a major addition.

10. **Cost and FinOps for AI development are absent.** Token costs, GPU costs during development, and the cost-of-eval are now first-order concerns in AI-DLC planning.

---

## NEW SLIDES

---

### [NEW 2026] Slide: The Agentic SDLC — AI as Participant, Not Just Product
**Insert after:** Section 1 (How AI-DLC differs from traditional SDLC)
**Format:** Concept explanation with diagram

**Content:**

The SDLC is no longer just the lifecycle for *building* AI — AI agents are now active participants *across the entire lifecycle*. This is the single biggest shift in software development methodology since Agile.

```
TRADITIONAL:  Human → Code → Test → Deploy
AI-AUGMENTED: Human → AI assists → Human reviews → Deploy
AGENTIC:      Human specs → Agents execute → Agents test → Human validates → Deploy
```

**The 2026 reality:**
- 41% of all new code is AI-generated (Stack Overflow 2026 survey)
- 92% of US developers use AI coding tools daily
- Productivity lifts of 21–55% per developer when AI is integrated across all stages
- But: 45% of AI-generated code fails security benchmarks (OWASP categories)
- Developer trust in AI code accuracy dropped to 29% (from 43% in 2024)

**The implication for AI-DLC:** You must now design your lifecycle to handle two parallel concerns:
1. Building AI products (the original AI-DLC focus)
2. Governing AI participation in the development process itself

**Facilitator Notes:**
- Open with: "When we talked about AI-DLC in the first half of this module, we focused on building AI products. But there's a parallel revolution — AI is now a participant in how ALL software gets built."
- Common question: "Does this replace developers?" Answer: No, but it shifts the developer role from writing code to writing specs, reviewing agent output, and governing the process.
- For beginners: Focus on the statistics and the high-level shift. For advanced: Dive into the governance implications.
- Time: 5 minutes
- Draw on the board: the three arrows showing Traditional → AI-Augmented → Agentic

---

### [NEW 2026] Slide: Vibe Coding — The Spectrum from Exploration to Discipline
**Insert after:** [NEW 2026] The Agentic SDLC
**Format:** Concept explanation with spectrum diagram

**Content:**

**Vibe coding** (coined by Andrej Karpathy, Feb 2025; Collins Word of the Year 2025): Prompt-driven development where developers describe goals in natural language and AI generates most of the code.

The spectrum (Karpathy's own evolution by 2026):

```
VIBE CODING ←────────────────────────────→ AGENTIC ENGINEERING
"Describe it,              "Specs coordinate agents,
 ship it, YOLO"             humans validate & govern"
```

| Dimension | Vibe Coding | Agentic Engineering |
|---|---|---|
| Planning | Minimal | Spec-driven |
| Review | Optional | Mandatory |
| Testing | Manual/ad-hoc | Automated evals in CI |
| Governance | None | Full lifecycle |
| Best for | Prototypes, MVPs, exploration | Production, enterprise, regulated |

**Key statistics (2026):**
- $4.7B market, projected $12.3B by 2027
- 63% of vibe coding users are non-developers
- MIT Technology Review named generative coding a "10 Breakthrough Technologies of 2026"
- 84% of developers in Stack Overflow survey use or plan to use AI coding tools

**The message for AI-DLC:** Vibe coding is valid for exploration and prototyping phases. But production AI systems require the disciplined end of the spectrum — specs, eval gates, and governance.

**Facilitator Notes:**
- This is a topic that will get strong reactions. Some students will be enthusiastic vibe coders; others will be sceptical. Frame it as a spectrum, not a binary.
- Common question: "Is vibe coding dangerous?" Answer: Not inherently — it depends on the governance context. Prototyping with vibe coding is fine. Shipping to production without review is dangerous.
- For beginners: Focus on what it is and where it fits. For advanced: Discuss the 45% security failure rate and implications for code review.
- Time: 5 minutes

---

### [NEW 2026] Slide: Spec-Driven Development (SDD) — The Spec is the New Code
**Insert after:** [NEW 2026] Vibe Coding
**Format:** Concept explanation with workflow diagram

**Content:**

**Spec-Driven Development (SDD):** A methodology where structured specifications are the shared source of truth for both humans and AI agents. Instead of prompting first and aligning later, teams align first and let AI accelerate execution from a clear spec.

**The core insight:** In an agentic world, the spec replaces the prompt as the unit of engineering intent.

```
Traditional:    Requirements → Code → Test → Repeat
SDD:            Spec → Agent generates → Agent tests against spec → Human validates → Ship
```

**Key tools (2026):**
| Tool | Approach | Who Uses It |
|---|---|---|
| Amazon Kiro | Story-driven specs with acceptance criteria | AWS-native teams |
| GitHub Spec Kit | Issue-to-spec pipeline with agent execution | GitHub ecosystem |
| Augment Cosmos | Spec-coordinated multi-agent pipelines | Enterprise engineering |
| OpenSpec | Open-source spec format standard | OSS community |
| BMAD-METHOD | Behaviour-driven specs for AI agents | BDD practitioners |

**What makes a good spec for agents:**
1. Unambiguous success criteria (machine-verifiable)
2. Edge cases explicitly enumerated
3. Constraints stated (not implied)
4. Test expectations embedded
5. Context boundaries defined

**Microsoft's framing:** "Spec-Driven Development is a structural component of the AI-native Development Lifecycle (AIDLC), where specifications coordinate every stage from authoring through deployment."

**Facilitator Notes:**
- Connect to Module 2 (use case identification): specs are the bridge between a use case and agent execution.
- Common question: "How detailed does a spec need to be?" Answer: Detailed enough that an agent can generate code AND tests from it. Rule of thumb: if a human reviewer can't verify correctness from the spec alone, it's too vague.
- For beginners: Focus on the "spec as shared truth" concept. For advanced: Discuss spec authoring as a new engineering discipline.
- Time: 5 minutes

---

### [NEW 2026] Slide: The Updated AI-DLC — 7 Stages with Agent Participation
**Insert after:** Section 2 (Stages: Discover → Design → Develop → Evaluate → Deploy → Monitor)
**Format:** Updated framework diagram

**Content:**

[UPDATE 2026] The AI-DLC stages need expansion from 6 to 7, with explicit agent participation at each:

```
┌─────────────┐   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐
│  1. DISCOVER │──▶│  2. SPECIFY  │──▶│  3. DESIGN   │──▶│  4. DEVELOP  │
│              │   │   [NEW]      │   │              │   │              │
│ Human: Leads │   │ Human: Leads │   │ Human: Leads │   │ Agent: Leads │
│ Agent: Research │ │ Agent: Draft │   │ Agent: Suggest│  │ Human: Review│
└──────────────┘   └──────────────┘   └──────────────┘   └──────────────┘
        │                                                         │
        ▼                                                         ▼
┌─────────────┐   ┌─────────────┐   ┌─────────────┐
│  7. GOVERN   │◀──│  6. MONITOR  │◀──│  5. EVALUATE │
│  [NEW]       │   │              │   │  & DEPLOY    │
│ Human: Leads │   │ Agent: Leads │   │ Agent: Eval  │
│ Agent: Audit │   │ Human: Alert │   │ Human: Gate  │
└──────────────┘   └──────────────┘   └──────────────┘
```

**Key changes from the original 6-stage model:**
- **Stage 2 (SPECIFY)** is new — reflects the rise of spec-driven development
- **Stage 7 (GOVERN)** is separated from Monitor — reflects regulatory requirements (EU AI Act)
- Each stage now has explicit **human vs. agent** role assignments
- Evaluate and Deploy are merged — reflecting CI/CD with eval gates (you don't deploy without passing evals)

**Facilitator Notes:**
- Draw this on the board. Ask: "In the original AI-DLC, who did the work at each stage?" Then overlay: "Now who does it?"
- Common question: "If agents lead development, what do developers do?" Answer: They specify, review, validate, and govern. The shift is from author to architect/reviewer.
- Time: 5 minutes

---

### [NEW 2026] Slide: Prompt Management as Infrastructure
**Insert after:** Section on prompt engineering as development discipline
**Format:** Tool comparison table

**Content:**

Prompts are no longer strings in your codebase. In 2026, they are **versioned, deployable artifacts** managed by dedicated infrastructure.

**Why this matters:**
- A small prompt edit can affect accuracy, tone, compliance, or conversion rates
- Production systems may run 50–200 different prompts across features
- Teams need to A/B test, roll back, and audit prompt changes independently of code releases

**The 2026 Prompt Management Stack:**

| Tool | Strength | Pricing Model |
|---|---|---|
| PromptLayer | Dedicated prompt registry with version history | Free tier + paid |
| Braintrust | Versioning + eval gates + runtime routing | $249/mo ($800M valuation) |
| Langfuse | Self-hosted versioning + observability (OSS) | Open source + cloud |
| LangSmith | Full lifecycle (versioning → eval → monitoring) | $39/seat |
| PromptHub | Prompt collaboration for non-engineers | Per-seat |
| Helicone | Prompt + cost observability | Usage-based |
| Vellum | Enterprise prompt orchestration | Enterprise |

**Key capabilities to look for:**
1. **Version control** — git-like history for every prompt
2. **Environment promotion** — staging → production pipeline
3. **A/B testing** — run multiple prompt versions simultaneously
4. **Eval integration** — automated scoring before promotion
5. **Rollback** — instant revert when metrics drop
6. **Audit trail** — who changed what, when, and why
7. **Collaboration** — PMs and domain experts can contribute without code deploys

**The pattern:** Prompts should be managed like feature flags — changed at runtime, tested independently, and governed by eval gates.

**Facilitator Notes:**
- This surprises many students: "Wait, prompts aren't just strings in my code?" Emphasise the scale problem — 50+ prompts across a product, each affecting behaviour.
- Common question: "Can't I just use git?" Answer: You can for storage, but you lose runtime A/B testing, eval integration, and non-engineer collaboration.
- For beginners: Focus on the "why" — a small change breaks things. For advanced: Discuss the architecture of prompt-as-config vs. prompt-in-code.
- Time: 5 minutes

---

### [NEW 2026] Slide: Evals-as-Code — Automated LLM Testing in CI/CD
**Insert after:** Section on model evaluation frameworks
**Format:** Technical concept with code example

**Content:**

**Evals-as-code:** The practice of writing LLM evaluations as programmatic tests that run automatically in your CI/CD pipeline — just like unit tests, but for AI behaviour.

**The core pattern:**
```
PR opened → CI triggered → Eval suite runs → Score computed → Gate decision (pass/fail) → Deploy or block
```

**What an eval gate looks like (pseudocode):**
```python
# eval_suite.py — runs in GitHub Actions on every PR
eval_results = run_evals(
    prompt_version="v2.3.1",
    dataset="golden_set_v4.json",  # 200 curated test cases
    metrics=["faithfulness", "relevance", "toxicity"],
    judge_model="claude-3.5-sonnet"  # LLM-as-judge
)

# Gate decision
if eval_results.faithfulness < 0.85:
    sys.exit(1)  # Block the deploy
if eval_results.toxicity > 0.02:
    sys.exit(1)  # Block the deploy
```

**The 4-layer eval pyramid (2026 best practice):**

```
         ┌─────────────────┐
         │  Human Review    │  ← Expensive, infrequent, high-signal
         ├─────────────────┤
         │  LLM-as-Judge   │  ← Scalable, nuanced, needs calibration
         ├─────────────────┤
         │  Heuristic/Rule │  ← Fast, cheap, catches obvious failures
         ├─────────────────┤
         │  Deterministic   │  ← Regex, format checks, length limits
         └─────────────────┘
```

**Production tools for eval gates:**
- **Braintrust** — native CI/CD integration, dataset management
- **LangSmith** — regression testing with automatic comparisons
- **Confident AI (DeepEval)** — red teaming + evals + regression in one
- **FutureAGI** — classifier cascade for cheap/fast gating
- **BuildPulse** — LLM CI focused on prompt regression testing

**Key principle:** "CI/CD quality gates beat post-hoc dashboards. Regression test on every deploy; block the deploy when eval scores drop." (Braintrust, 2026)

**Facilitator Notes:**
- This is the slide that makes engineers excited. Frame it as: "You already have unit tests and integration tests in CI. Evals are your AI equivalent."
- Common question: "How do I build a golden dataset?" Answer: Start with 50 hand-curated examples. Grow to 200+ over time. Include edge cases, adversarial inputs, and regression examples from production failures.
- ⚡ ADVANCED: Discuss Welch's t-test for statistical significance of eval score changes, and classifier cascades for cost-efficient gating.
- Time: 7 minutes

---

### [NEW 2026] Slide: LLMOps in 2026 — The Six-Layer Stack
**Insert after:** Section on MLOps and LLMOps
**Format:** Framework/architecture diagram

**Content:**

[UPDATE 2026] LLMOps has matured from "MLOps with a few extras" to a distinct discipline with six defined layers:

```
┌──────────────────────────────────────────────────┐
│ Layer 6: GOVERNANCE                              │
│ Responsible AI gates, audit trails, compliance   │
├──────────────────────────────────────────────────┤
│ Layer 5: COST CONTROL (FinOps for AI)            │
│ Token budgets, model routing, cost attribution   │
├──────────────────────────────────────────────────┤
│ Layer 4: OBSERVABILITY                           │
│ Traces, spans, latency, hallucination rate       │
├──────────────────────────────────────────────────┤
│ Layer 3: EVALUATION (Continuous)                 │
│ Evals-as-code, golden datasets, LLM-as-judge    │
├──────────────────────────────────────────────────┤
│ Layer 2: CI/CD FOR AI ARTIFACTS                  │
│ Prompt versioning, model registry, env promotion │
├──────────────────────────────────────────────────┤
│ Layer 1: MODEL SERVING                           │
│ Inference, routing, caching, scaling             │
└──────────────────────────────────────────────────┘
```

**Key differences from traditional MLOps:**

| Dimension | MLOps (Traditional ML) | LLMOps (2026) |
|---|---|---|
| Primary artifact | Trained model | Prompt + retrieval config + model version |
| Evaluation | Accuracy/F1 on held-out set | Multi-dimensional (faithfulness, relevance, toxicity, cost) |
| Deployment unit | Model binary | Prompt version + model endpoint + RAG config |
| Monitoring | Data/concept drift | Output quality drift, hallucination rate, cost per query |
| CI/CD | Retrain → validate → deploy | Eval gates → canary → promote |
| Cost model | GPU hours for training | Token costs at inference (ongoing) |

**MLflow 3.10 (March 2026) now covers:** GenAI agent observability, LLM tracing, multi-turn conversation evaluation, and cost tracking — making it the most comprehensive OSS lifecycle platform.

**Gartner data:** 85% of AI projects fail. Organisations with structured LLMOps frameworks are significantly more likely to reach production successfully.

**Facilitator Notes:**
- Draw the 6-layer stack on the board. Ask students: "Which layers does your organisation have today?" Most will have Layer 1 (serving) and maybe Layer 4 (basic observability). The gap is typically Layers 2, 3, and 5.
- Common question: "Do I need all 6 layers from day one?" Answer: No. Start with Layer 1 + 3 (serving + basic eval). Add layers as you scale.
- Time: 7 minutes

---

### [NEW 2026] Slide: The AI Artifact Registry — Beyond Model Versioning
**Insert after:** [NEW 2026] LLMOps Six-Layer Stack
**Format:** Concept with architecture diagram

**Content:**

In 2026, a production AI system's "deployable artifact" is no longer just a model. It's a **composite bundle:**

```
AI DEPLOYMENT ARTIFACT (2026)
├── Model version (pointer to hosted model endpoint)
├── Prompt versions (system prompt, user prompt templates)
├── RAG configuration (chunk size, embedding model, retrieval params)
├── Guardrail rules (input/output filters, safety policies)
├── Eval dataset (golden set for regression testing)
├── Tool schemas (function definitions, MCP server configs)
├── Agent instructions (orchestration logic, persona)
└── Environment config (temperature, max tokens, routing rules)
```

**What this means for your registry:**

| Registry Layer | What It Tracks | Tools |
|---|---|---|
| Model Registry | Model versions, lineage, stage | MLflow, SageMaker Registry, Bedrock |
| Prompt Registry | Prompt versions, A/B tests, env promotion | PromptLayer, Braintrust, Langfuse |
| RAG Config Store | Retrieval params, embedding versions, chunk configs | Custom (often in-house) |
| Agent Blueprint Store | Agent instructions, tool configs, guardrails | Bedrock Agent versioning |
| Eval Asset Store | Golden datasets, eval rubrics, baselines | Braintrust, LangSmith |

**The deployment question has changed:** It's no longer "which model version do I deploy?" It's "which *combination* of model + prompt + RAG + guardrails + tools passes all my eval gates?"

**Facilitator Notes:**
- This extends the original module's treatment of model registries. Frame as: "The model is just one piece of the puzzle. You need to version and coordinate all of these together."
- Common question: "How do I manage this complexity?" Answer: Start with prompt + model versioning. Add RAG config next. Most teams don't need the full stack on day one.
- ⚡ ADVANCED: Discuss composite artifact versioning strategies — GitOps with a manifest file vs. dedicated platforms.
- Time: 4 minutes

---

### [NEW 2026] Slide: AI-Assisted Development Across the Lifecycle
**Insert after:** [NEW 2026] Spec-Driven Development
**Format:** Table with 7 stages

**Content:**

AI agents now participate across all 7 stages of the SDLC with measurable productivity gains:

| Stage | AI Participation | Human Role | Lift |
|---|---|---|---|
| **Requirements** | Agents draft specs from conversations, research prior art | Validate, refine, add edge cases | 25% faster |
| **Architecture** | Agents suggest patterns, evaluate trade-offs, generate diagrams | Decide, constrain, review | 20% faster |
| **Code** | Agents write implementation from specs | Review, integration, security check | 55% faster |
| **Review** | Agents flag issues, suggest fixes, check style | Final approval, nuance, context | 30% faster |
| **Test** | Agents generate tests from specs and code | Review coverage, add edge cases | 40% faster |
| **Deploy** | Agents run eval gates, canary deploys, rollback | Set thresholds, approve production | 21% faster |
| **Operate** | Agents monitor, alert, triage, propose fixes | Decide on fixes, approve changes | 25% faster |

*Source: Forasoft 2026 SDLC study, multiple enterprise case studies*

**Key risk:** Adoption is uneven. Most teams have AI in the Code stage but lack it in Requirements, Review, and Operate. This creates "governance gaps" — code generated fast without adequate spec or review.

**Optiver's insight:** "An agentic SDLC starts from a different assumption: agents do most of the work, and humans guide and refine. That changes requirements across the workflow. We found ourselves tightening specifications, exposing more of our tooling programmatically, and pushing failures into places where they could be detected automatically."

**Facilitator Notes:**
- Walk through each stage briefly. Ask: "Which stages does your team currently have AI assistance in?" Most will say Code only.
- The security data point (62% of AI-generated code contains vulnerabilities — CSA 2025) is a great counterpoint to the productivity gains. Both are true simultaneously.
- Time: 5 minutes

---

### [NEW 2026] Slide: GitHub Agentic Workflows — AI Agents in Your CI/CD
**Insert after:** [NEW 2026] AI-Assisted Development Across the Lifecycle
**Format:** Case study / demo walkthrough

**Content:**

On February 13, 2026, GitHub shipped **Agentic Workflows** (technical preview): AI agents triggered by issues and pull requests that can:
- Triage bugs automatically
- Generate fixes and open PRs
- Write tests for new code
- Run security scans and suggest remediations
- All without human intervention (until approval gate)

**How it works:**
```yaml
# .github/workflows/ai-triage.yml
on:
  issues:
    types: [opened]
jobs:
  triage:
    runs-on: ubuntu-latest
    steps:
      - uses: github/agentic-triage@v1
        with:
          model: "gpt-4o"
          labels: ["bug", "feature", "docs"]
          auto_assign: true
          generate_fix: true  # Opens a PR with suggested fix
```

**The pattern:** Issues → Agent triages → Agent generates fix → Eval gate runs → Human reviews PR → Merge

**What this means for AI-DLC:** The lifecycle is no longer a waterfall or even sprints — it's an event-driven loop where agents respond to signals (issues, alerts, PRs) and humans validate outcomes.

**Facilitator Notes:**
- This is a great "wow" moment in the module. Show a real example if possible.
- Common question: "Is this production-ready?" Answer: Technical preview as of Feb 2026. The pattern is mature; the specific GitHub implementation is new.
- ⚡ ADVANCED: Discuss how this connects to Module 12 (multi-agent orchestration) — each workflow step could be a different specialised agent.
- Time: 4 minutes
- SKIP FOR BEGINNERS if running short on time.

---

### [NEW 2026] Slide: The Security Gap in AI-Generated Code
**Insert after:** [NEW 2026] Vibe Coding
**Format:** Data-driven concern with mitigation strategies

**Content:**

**The problem:** Speed gains from AI coding come with a security tax that most organisations aren't accounting for.

**The data (2025-2026):**
- 45% of AI-generated code samples fail security benchmarks across OWASP Top-10 categories (Hostinger 2026)
- 62% of AI-generated code contains design flaws or known vulnerabilities due to missing threat models (Cloud Security Alliance 2025)
- Developer trust in AI code accuracy dropped from 43% (2024) to 29% (2025)
- Only 33% trust AI code accuracy in 2026

**Why this happens:**
1. Models trained on public code (which includes vulnerable code)
2. Models lack context about your specific threat model
3. Models optimise for functionality, not security by default
4. No automatic SAST/DAST in the generation loop

**Mitigation strategies for AI-DLC:**
| Strategy | When | Tool Examples |
|---|---|---|
| Security-aware prompting | At generation time | "Follow OWASP secure coding guidelines" in system prompt |
| Automated SAST in CI | Before merge | Snyk, SonarQube, Semgrep with AI rules |
| AI-specific code review | At PR review | GitHub Copilot code review, CodeRabbit |
| Threat model injection | At spec time | Include threat model in spec so agent generates secure code |
| Sandbox execution testing | At eval time | Run generated code in sandboxed environments before deploy |

**The AI-DLC principle:** Every AI code generation step must have a corresponding AI security validation step. Speed without security is technical debt at machine scale.

**Facilitator Notes:**
- This is the "sobering" slide after the exciting vibe coding content. Frame as: "The productivity gains are real. So are the risks. Your AI-DLC must account for both."
- Common question: "Does this mean we shouldn't use AI coding tools?" Answer: Absolutely not. It means your CI pipeline needs security gates that account for AI-specific vulnerability patterns.
- Time: 4 minutes

---

### [NEW 2026] Slide: Responsible AI Gates — Automated Checkpoints in Production
**Insert after:** Section on Responsible AI checkpoints at each stage
**Format:** Framework with concrete examples

**Content:**

[UPDATE 2026] "Responsible AI checkpoints" should be concrete, automated gates — not just discussion points in a meeting.

**The 2026 Responsible AI Gate Framework:**

```
┌─────────────────────────────────────────────────────────────┐
│ GATE 1: PRE-DEVELOPMENT (Before building)                    │
│ • Bias risk assessment based on use case and data            │
│ • Regulatory classification (EU AI Act risk tier)            │
│ • Privacy impact assessment for data in scope                │
│ • Proportionality check: is AI the right approach?           │
├─────────────────────────────────────────────────────────────┤
│ GATE 2: PRE-DEPLOYMENT (Before shipping)                     │
│ • Red-team testing (adversarial inputs, jailbreak attempts)  │
│ • Bias/fairness evaluation on representative test data       │
│ • Toxicity/harmful content evaluation                        │
│ • Hallucination rate below threshold                         │
│ • Explainability documentation (model card)                  │
├─────────────────────────────────────────────────────────────┤
│ GATE 3: POST-DEPLOYMENT (Ongoing)                            │
│ • Continuous bias monitoring on live traffic                  │
│ • Output quality drift detection                             │
│ • User feedback loop analysis                                │
│ • Incident response and rollback readiness                   │
│ • Periodic re-certification for high-risk systems            │
└─────────────────────────────────────────────────────────────┘
```

**Tooling for automated gates (2026):**
- **Confident AI** — red teaming + evals + regression in one platform
- **Amazon Bedrock Guardrails** — content filtering, denied topics, PII detection
- **Azure AI Content Safety** — real-time content moderation
- **FairML / AIF360** — bias detection and mitigation
- **ai-sdlc framework** (GitHub OSS) — declarative governance for AI SDLC

**EU AI Act Phase 3 (August 2026):** Enforcement for high-risk systems begins. Responsible AI gates are no longer optional for regulated industries.

**Facilitator Notes:**
- Connect to Module 16 (Governance). Here we focus on the *technical implementation* of gates; Module 16 covers the *policy framework*.
- Common question: "What threshold do I set for hallucination rate?" Answer: It depends on the use case. Medical/legal: <1%. Customer support: <5%. Creative writing: thresholds may not apply.
- Time: 5 minutes

---

### [NEW 2026] Slide: LLM-as-Judge — Scalable Automated Evaluation
**Insert after:** [NEW 2026] Evals-as-Code
**Format:** Technical concept with examples

**Content:**

**LLM-as-Judge:** Using a separate LLM to evaluate the outputs of your production LLM. The most scalable evaluation method for nuanced quality assessment.

**How it works:**
```python
# Simplified LLM-as-judge pattern
judge_prompt = """
Evaluate the following AI response for faithfulness to the source document.

Source: {source_document}
Response: {ai_response}

Score from 1-5 where:
5 = Completely faithful, no hallucinations
4 = Mostly faithful, minor unsupported claims
3 = Partially faithful, some hallucinated content
2 = Mostly unfaithful
1 = Completely hallucinated

Provide your score and a one-sentence justification.
"""

judge_response = call_llm(model="claude-3.5-sonnet", prompt=judge_prompt)
```

**Best practices (2026 consensus):**
| Practice | Why |
|---|---|
| Use a stronger model as judge than the model being evaluated | Avoids "blind leading the blind" |
| Use rubrics, not binary pass/fail | More nuanced and actionable feedback |
| Calibrate against human evaluators | Measure judge-human agreement regularly |
| Use multiple judges for high-stakes decisions | Reduces single-model bias |
| Log judge reasoning, not just scores | Enables debugging and improvement |

**When NOT to use LLM-as-Judge:**
- Factual accuracy against a ground truth (use deterministic checks)
- Format compliance (use regex/schema validation)
- Latency-critical real-time gates (too slow)

**Tools with built-in judge support:**
- RAGAS v2, DeepEval, LangSmith, Braintrust, Phoenix

**Facilitator Notes:**
- This extends the original module's coverage of "model evaluation frameworks." The key insight: LLM-as-judge is how you scale evaluation beyond the 200 examples in your golden dataset.
- Common question: "Isn't it circular to use an AI to judge an AI?" Answer: Not if the judge is stronger than the subject, and you calibrate against humans.
- ⚡ ADVANCED: Discuss judge calibration, inter-rater reliability metrics, and the cost of running judges at scale.
- Time: 5 minutes

---

### [NEW 2026] Slide: The AI Development FinOps Reality
**Insert after:** [NEW 2026] LLMOps Six-Layer Stack
**Format:** Data and framework

**Content:**

Cost is a first-order engineering concern in AI development — not just a finance problem.

**The 2026 cost landscape:**
| Cost Category | Where It Hits | Typical Range |
|---|---|---|
| Inference (production) | Every user query | $0.001–$0.15 per request |
| Evaluation (CI/CD) | Every PR, every prompt change | $5–$50 per eval run |
| Development (iteration) | Every developer prompt while building | $50–$500/dev/month |
| Fine-tuning (periodic) | Model customisation | $100–$10,000 per run |
| RAG indexing (periodic) | Embedding generation | $0.01–$1 per 1000 chunks |

**AI-DLC cost decisions:**
1. **Model routing:** Use cheap/fast models for simple tasks, expensive models for hard tasks. Pattern: classifier → router → specialist model.
2. **Caching:** Cache common responses. 40–70% of production queries are near-duplicates.
3. **Eval budget allocation:** Not every PR needs the full eval suite. Use tiered evaluation — cheap heuristics first, expensive judges only when needed.
4. **Prompt optimisation for token efficiency:** Shorter prompts = lower cost at scale. DSPy can auto-optimise prompts for token efficiency.

**The FinOps question for every AI-DLC stage:**
- Discover: "What's the cost ceiling for this use case?"
- Design: "Which model tier meets quality at acceptable cost?"
- Develop: "Are we burning tokens on iteration we could reduce with better specs?"
- Evaluate: "What's our eval budget per deploy?"
- Deploy: "What's our cost-per-request target?"
- Monitor: "Are we trending over budget? Where?"

**Facilitator Notes:**
- This is new territory for many engineering teams used to fixed infrastructure costs. Frame as: "Unlike a server that costs the same whether idle or busy, AI costs scale with every request."
- Common question: "How do I budget for this?" Answer: Start with cost-per-request targets for each use case. Work backwards from business value.
- Time: 4 minutes

---

### [NEW 2026] Slide: Canary Deployments for AI Systems
**Insert after:** [NEW 2026] Evals-as-Code
**Format:** Technical pattern

**Content:**

AI deployments need canary strategies that account for non-deterministic outputs:

```
┌─────────────────────────────────────────────────────────────┐
│ CANARY DEPLOYMENT FOR AI (2026 Best Practice)                │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. Deploy new prompt/model to 5% of traffic                 │
│  2. Run online evals on canary cohort for 4-24 hours         │
│  3. Compare metrics: canary vs. baseline                     │
│     - Quality: faithfulness, relevance (LLM-as-judge)        │
│     - Safety: toxicity, hallucination rate                   │
│     - Performance: latency P50/P99, token usage              │
│     - Cost: cost-per-request delta                           │
│     - User: satisfaction signals, thumbs up/down ratio       │
│  4. Statistical significance test (Welch's t-test)           │
│  5. If pass: promote to 25% → 50% → 100%                    │
│     If fail: auto-rollback + alert + incident                │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Why traditional canary doesn't work for AI:**
- Outputs are non-deterministic — you can't diff outputs like you diff API responses
- Quality degradation may be subtle (slightly worse, not broken)
- Need probabilistic comparison, not binary pass/fail

**Tools:** Braintrust (native canary support), LaunchDarkly (AI feature flags), custom with eval frameworks

**Facilitator Notes:**
- For engineers who've done canary for traditional services: "Same concept, but your comparison metric isn't error rate — it's eval score distributions."
- ⚡ ADVANCED: Discuss statistical testing requirements. How many samples do you need for significance?
- Time: 3 minutes
- SKIP FOR BEGINNERS

---

### [NEW 2026] Slide: The Role Shift — From Developer to AI Systems Engineer
**Insert after:** Module closing / outcomes section
**Format:** Discussion / reflection

**Content:**

The AI-DLC creates a new role archetype: the **AI Systems Engineer** — someone who builds, evaluates, and governs AI systems rather than just writing code.

**The skill shift:**

| Traditional Developer | AI Systems Engineer |
|---|---|
| Writes code | Writes specs + reviews agent-generated code |
| Runs unit tests | Designs eval suites + calibrates judges |
| Manages git branches | Manages prompt versions + model versions + RAG configs |
| Reviews PRs | Reviews AI-generated PRs + governs agent behaviour |
| Monitors dashboards | Builds AI-specific observability (traces, hallucination rate) |
| Ships features | Ships composite AI artifacts (prompt + model + RAG + guardrails) |
| Optimises performance | Optimises quality, cost, and latency simultaneously |

**What this means for career development:**
- AI-DLC fluency is the differentiator between "uses AI tools" and "engineers AI systems"
- The engineers who understand the full lifecycle (not just the coding stage) are the ones leading AI projects
- This is Module 6's core value proposition: you now understand the *system*, not just the *technique*

**Discussion Questions:**
1. Which parts of the AI-DLC does your current team handle well? Where are the gaps?
2. How would you introduce eval gates into your existing CI/CD pipeline tomorrow?
3. If 41% of code is AI-generated, what does "code review" look like in 2027?

**Facilitator Notes:**
- This is the "so what" slide — connecting the technical content to career and organisational implications.
- Use as a module closer. Give 5 minutes for pair discussion on the questions.
- Time: 5 minutes

---

### [NEW 2026] Slide: Lab Extension — Design Your AI-DLC Pipeline
**Insert after:** Hands-on activity section
**Format:** Hands-on activity

**Content:**

**Extended Lab: Design a Complete AI-DLC Pipeline (20 min)**

**Scenario:** Your team is building a customer support AI agent. It uses RAG to retrieve product docs, an LLM to generate responses, and guardrails to filter harmful content. You need to ship updates weekly.

**Design your pipeline by specifying:**

1. **Artifact inventory:** What gets versioned and deployed together?
   - [ ] Prompt version
   - [ ] Model endpoint selection
   - [ ] RAG retrieval config
   - [ ] Guardrail rules
   - [ ] Eval golden dataset
   - [ ] Other: _______

2. **Eval gate design:** What do you evaluate before deploying?
   - Metric 1: _______ (threshold: ___)
   - Metric 2: _______ (threshold: ___)
   - Metric 3: _______ (threshold: ___)
   - Judge model: _______

3. **Canary strategy:** How do you roll out safely?
   - % traffic to canary: ___
   - Duration before promotion: ___
   - Auto-rollback trigger: ___

4. **Responsible AI gate:** What checks run before shipping?
   - Gate 1: _______
   - Gate 2: _______
   - Gate 3: _______

5. **Cost controls:** What's your budget and routing strategy?
   - Cost-per-request target: $___
   - Model routing rule: _______
   - Caching strategy: _______

**Deliverable:** A one-page pipeline diagram with all decisions documented.

**Facilitator Notes:**
- This lab synthesises all the new content. Works best in pairs or small groups.
- Give 15 min for design, 5 min for 2-3 groups to share.
- Have a "reference answer" ready showing a mature pipeline for comparison.
- Time: 20 minutes (can be shortened to 10 if running long)

---

### [NEW 2026] Slide: The AI-Native Development Lifecycle (AIDLC) vs. Traditional AI-DLC
**Insert after:** [NEW 2026] The Updated AI-DLC — 7 Stages
**Format:** Comparison table

**Content:**

Two frameworks are emerging in 2026. Understanding the distinction matters:

| Dimension | AI-DLC (Building AI Products) | AIDLC (Building Software with AI Agents) |
|---|---|---|
| Focus | Lifecycle for AI/ML systems | Lifecycle for any software, AI-assisted |
| Primary artifact | AI system (model + prompt + RAG + agent) | Software product (may include AI) |
| Who does the work | Humans build AI, deploy it | AI agents build software, humans validate |
| Key challenge | Eval, monitoring, non-determinism | Governance, security, spec quality |
| Lifecycle stages | Discover → Specify → Design → Develop → Evaluate → Monitor → Govern | Spec → Generate → Review → Test → Deploy → Operate |
| Key role | AI/ML Engineer, AI PM | Any developer using AI tools |
| Methodologies | AI-DLC, LLMOps | SDD, Agentic Engineering |

**Why both matter:** Most teams in 2026 are doing BOTH simultaneously:
- Building AI products (AI-DLC) — e.g., building a RAG chatbot
- Building those products using AI-assisted development (AIDLC) — e.g., using Copilot/Cursor to write the RAG pipeline code

**The meta-insight:** AI is both the product AND the tool. Your lifecycle framework needs to account for both.

**Facilitator Notes:**
- This distinction often confuses students initially. Use a concrete example: "You're using Cursor (AIDLC) to write a RAG pipeline (AI-DLC). Both lifecycles apply simultaneously."
- Common question: "Which one should I focus on?" Answer: AI-DLC if you're building AI products. AIDLC if you're a software team adopting AI tools. Most teams need both.
- Time: 4 minutes

---

### [NEW 2026] Slide: MLflow 3.10 — The Unified AI Lifecycle Platform
**Insert after:** [NEW 2026] The AI Artifact Registry
**Format:** Tool deep-dive

**Content:**

MLflow 3.10 (March 2026) has evolved from an experiment tracker to a unified AI lifecycle platform:

**What's new (2025-2026 additions):**
| Capability | What It Does | AI-DLC Stage |
|---|---|---|
| GenAI Agent Observability | Trace multi-turn agent conversations | Monitor |
| LLM Tracing | OpenTelemetry-compatible spans for LLM calls | Monitor |
| Multi-turn Eval | Evaluate conversational AI over multiple turns | Evaluate |
| Cost Tracking | Token usage and cost attribution per experiment | All |
| Prompt Engineering UI | Collaborative prompt iteration and versioning | Develop |
| Model Registry (expanded) | Now supports prompt artifacts alongside models | Deploy |

**The MLflow lifecycle (2026):**
```
Experiment → Log runs → Register (model + prompt + config) → Stage promotion → Deploy → Trace → Evaluate → Iterate
```

**Why it matters:** MLflow is used by millions (thousands of contributors). If you're in the MLOps/LLMOps world, it's likely already in your stack — and it now covers most of the AI-DLC.

**Facilitator Notes:**
- Many students will already know MLflow for traditional ML. Frame as: "The tool you know has grown up. It now covers the LLM lifecycle too."
- ⚡ ADVANCED: Discuss how MLflow compares to Langfuse/LangSmith for the LLM-specific parts. MLflow is broader but less deep; Langfuse/LangSmith are deeper on LLM-specific observability.
- Time: 3 minutes
- SKIP FOR BEGINNERS if running short

---

### [NEW 2026] Slide: Key Terminology Update (2025-2026)
**Insert after:** Key Concepts & Definitions section
**Format:** Definitions table

**Content:**

[UPDATE 2026] Add these terms to the module's key concepts table:

| Term | Definition |
|---|---|
| **Context Engineering** | The discipline of managing what information a model sees, when, where in the window, and in what format — broader than prompt engineering |
| **Vibe Coding** | Prompt-driven development where developers describe goals in natural language and AI generates code (coined Karpathy, 2025) |
| **Agentic Engineering** | The disciplined end of AI-assisted development — specs, eval gates, governance (Karpathy, 2026 evolution) |
| **Spec-Driven Development (SDD)** | Methodology using structured specifications as shared source of truth for both humans and AI agents |
| **Evals-as-Code** | LLM evaluations written as programmatic tests that run automatically in CI/CD pipelines |
| **LLM-as-Judge** | Using a separate LLM to evaluate the outputs of your production LLM |
| **Prompt Registry** | Infrastructure for versioning, promoting, and managing prompts as deployable artifacts |
| **AI Artifact** | The composite deployable unit: model version + prompt + RAG config + guardrails + eval dataset |
| **Canary for AI** | Traffic-splitting deployment with probabilistic quality comparison (not deterministic diff) |
| **Eval Gate** | Automated quality threshold that blocks deployment if eval scores drop below acceptable levels |
| **Golden Dataset** | Curated test set (50-500 examples) used for regression testing AI systems in CI |
| **AIDLC** | AI-native Development Lifecycle — building any software using AI agents as active participants |

**Facilitator Notes:**
- These terms come up constantly in 2026 practitioner conversations. Students should leave this module using them confidently.
- Consider a quick quiz: "Which of these terms were you already familiar with? Which are new?"
- Time: 3 minutes (just reference the table; don't read every definition aloud)

---

## FACILITATOR UPDATE BRIEF

### 🎤 Top 3 Most Important Additions

1. **Evals-as-Code / CI/CD Gates** — This is the single most impactful new practice. The shift from "evaluate after deployment" to "gate deployment with automated evals" is what separates hobby projects from production AI. Every student should leave understanding this pattern.

2. **The Agentic SDLC / Spec-Driven Development** — The fundamental reframing that AI is now a *participant* in the lifecycle, not just the *product* being built. This changes how students think about their own roles and workflows.

3. **Vibe Coding → Agentic Engineering Spectrum** — This gives students a vocabulary to describe the range of AI-assisted development approaches and understand where governance is needed vs. where speed is acceptable.

### 🔄 What's Now Outdated

| Original Content | Issue | How to Address |
|---|---|---|
| "Prompt engineering as a development discipline" | Now too narrow — should be "context engineering" | Update the framing; explain the hierarchy (prompt eng → context eng → harness eng) |
| "MLOps and LLMOps" as separate concepts needing introduction | LLMOps is now mature and distinct — no longer needs framing as "MLOps extension" | Present the 6-layer LLMOps stack directly |
| 6-stage AI-DLC (Discover → Monitor) | Needs SPECIFY and GOVERN stages added | Use the updated 7-stage model |
| RAGAS and benchmarks as the primary eval approach | Now one layer in a multi-layer eval pyramid | Present the 4-layer eval pyramid with evals-as-code |

### ⏱️ Timing Guidance

The original 60-minute module remains viable if you:
- Compress the "AI-DLC vs SDLC" section (students already get this)
- Add 15 min of new content (Agentic SDLC, Vibe Coding, Evals-as-Code)
- Use the extended lab as the activity (replaces the original activity)

**For a 90-minute extended version:** Add the full spec-driven development section, the FinOps slide, the LLMOps 6-layer deep-dive, and give the full 20-minute lab. This is the recommended format for technical audiences.

### 🛠️ New Tools/Accounts/Demos to Set Up

1. **Braintrust account** (free tier) — for demonstrating eval gates and prompt versioning
2. **Langfuse self-hosted or cloud** (OSS) — for showing traces and prompt management
3. **GitHub Actions workflow** — prepare a sample repo with an eval gate in CI (can be a simple LLM-as-judge script)
4. **MLflow 3.10** — if doing a live demo of the unified lifecycle
5. **Sample golden dataset** (50 Q&A pairs with expected outputs) — for the lab exercise

### 📋 Pre-Reading Recommendation

Assign students one of:
- "Spec-Driven Development: A Spec-First Approach to AI-Native Engineering" (Microsoft Developer Blog, June 2026)
- "Engineering the Agentic SDLC" (Optiver Tech Blog, June 2026)

Both are accessible to non-engineers and set up the key concepts before class.

---

*Module 06 Update — AI & Agentic AI Training Programme — July 2026*
