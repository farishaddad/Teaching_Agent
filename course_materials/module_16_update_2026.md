# Module 16 Update — AI Governance, Responsible AI & The Road Ahead
## [NEW 2026] Content Additions & Facilitator Delivery Notes

---

## STEP 2: GAP ANALYSIS

The original module (early 2025 vintage) has the following gaps against mid-2026 reality:

1. **EU AI Act timeline is outdated** — The Digital Omnibus (May 2026) pushed high-risk system deadlines from Aug 2026 to Dec 2027 (Annex III) and Aug 2028 (Annex I). The original module teaches Aug 2026 as the main deadline. This is now wrong.

2. **US regulation landscape missing entirely** — Colorado repealed and replaced its original AI Act (SB 26-189, signed May 14 2026). Multiple US states now have AI-specific legislation. No US regulatory content exists in the original module.

3. **Agentic AI governance not covered** — The original module treats AI governance as a model/output problem. In 2026, the governance challenge is agent autonomy: who is accountable when an agent takes an action? Only 21% of enterprises have mature governance for autonomous agents (arXiv survey).

4. **NIST AI RMF revision in progress but no 1.1 yet** — The White House AI Action Plan (July 2025) tasked NIST with revising the AI RMF to remove references to misinformation, DEI, and climate change. The Generative AI Profile (AI 600-1) is the key companion document. Original module mentions NIST RMF but not the GenAI Profile.

5. **ISO 42001 adoption has exploded** — IBM, Anthropic, Microsoft, KPMG, Changi Airport all certified by April 2026. Original module mentions it as emerging; it is now the gold standard.

6. **AI FinOps has become its own discipline** — Agentic workflows consume 5–30× more tokens per task. The FinOps Foundation published dedicated AI guidance. "Return on AI" replaces simple cost tracking. Original module is too surface-level.

7. **Frontier model governance is now real** — Anthropic's System Card for Claude Fable 5 (319 pages) introduced 8 governance mechanisms including visible safety fallbacks. Reasoning models have unique safety risks (the thinking process is more dangerous than the answer). Not covered.

8. **AI compliance tooling market has matured** — Platforms like Modulos, OneTrust, Vanta, Holistic AI now offer automated EU AI Act conformity assessment. None mentioned in original.

9. **AI auditing has formalised** — MLflow/ISO 42001/NIST all now converge on "proof bundles" linking decisions to data inputs + model configs at decision time. Original module doesn't cover operational auditing.

10. **Agentic FinOps is a new sub-discipline** — Unbounded inference, retry loops, multi-agent token explosion. Traditional cloud FinOps tools don't work. Dedicated "agentic cost architecture" patterns emerging.

---

## STEP 3: NEW SLIDES

---

### [NEW 2026] Slide 1: The Governance Landscape Has Shifted — 2026 Reality Check

**Insert after:** Module Overview / opening section  
**Format:** Concept explanation with data points

**Content:**

The AI governance landscape in mid-2026 is fundamentally different from early 2025:

| Dimension | Early 2025 | Mid-2026 |
|---|---|---|
| EU AI Act | Entered force Aug 2024; theoretical | Enforcement active; Omnibus reshuffled timelines |
| US Regulation | Colorado AI Act passed 2024 | Colorado repealed & replaced; multi-state patchwork |
| ISO 42001 | Newly published; few adopters | IBM, Anthropic, Microsoft, KPMG certified |
| Agentic AI | Experimental | Production deployments; 35% of orgs deploying agents |
| FinOps for AI | Token cost awareness | Full discipline; dedicated frameworks |
| Frontier safety | GPT-4 class discussion | Mythos/Fable 5 — models that outperform humans at hacking |

> Key stat: Only 21% of enterprises have mature governance models for autonomous agents, while 40% of agentic AI projects are projected to fail by 2027 due to inadequate governance. (arXiv, 2026)

**Facilitator Notes:**
- Open with this slide to set context and create urgency
- Ask: "How many of you have a governance framework that covers AI agents specifically — not just models?"
- Common question: "Is governance just a compliance exercise?" Answer: No — it's an operational necessity. Ungoverned agents cause real financial and reputational damage.
- Time: 3 minutes
- Suitable for all levels

---

### [NEW 2026] Slide 2: EU AI Act — The Real Timeline (Post-Digital Omnibus)

**Insert after:** EU AI Act section  
**Format:** Concept explanation / timeline

**Content:**

**CRITICAL UPDATE:** The EU Digital Omnibus (political agreement May 7, 2026) reshaped the AI Act timeline significantly:

```
ALREADY ACTIVE:
  ✅ Feb 2, 2025 — Prohibited AI practices + AI literacy obligations
  ✅ Aug 2, 2025 — GPAI model rules + governance + penalties framework

COMING (still live dates):
  ⚠️ Aug 2, 2026 — Article 50 transparency obligations activate
                  — GPAI penalty enforcement powers go live
                  — Market surveillance authorities can investigate
                  — Watermarking obligations (moved to Dec 2, 2026)

PUSHED BACK (was Aug 2026, now later):
  📅 Dec 2, 2027 — High-risk AI systems (Annex III) — MAIN compliance wave
  📅 Aug 2, 2028 — High-risk AI in regulated products (Annex I)
  📅 Aug 2, 2027 — AI regulatory sandboxes at national level
```

**What the Omnibus ALSO did:**
- Expanded ability to process special categories of personal data (e.g. biometric, health) specifically for bias detection and mitigation
- Introduced new rules on AI-generated intimate content ("nudifier" ban)
- Reduced watermarking grace period from 6 months to 3 months

**Fines remain unchanged:** Up to €35M or 7% of global turnover — higher than GDPR.

**Facilitator Notes:**
- IMPORTANT: If you taught this module before June 2026, the timeline you taught is wrong. Explicitly acknowledge this.
- Student question: "So we have more time?" Answer: "For high-risk conformity assessment, yes — 16 months more. But transparency obligations and GPAI enforcement still hit Aug 2026. And the extra time means MORE scrutiny, not less."
- Time: 5 minutes
- Relevant for all levels — everyone needs to know the real dates

---

### [NEW 2026] Slide 3: The US Regulatory Patchwork — Colorado, State Laws & Federal Signals

**Insert after:** EU AI Act timeline slide  
**Format:** Comparison table

**Content:**

The US is NOT waiting for federal AI legislation. A state-by-state patchwork is forming:

**Colorado — the bellwether:**
- Original Colorado AI Act (SB 24-205, passed May 2024) — first "comprehensive" US AI law
- Enforcement stayed (April 2026) after DOJ + xAI lawsuit
- **Repealed and replaced** by SB 26-189 (signed May 14, 2026)
- New law: "Automated Decision-Making Technology in Consequential Decisions"
- Lighter touch: eliminates several developer obligations, focuses on deployer outcomes
- Effective: January 1, 2027

**Key differences in the new Colorado approach:**
| Original (SB 24-205) | Replacement (SB 26-189) |
|---|---|
| Regulated "high-risk AI systems" | Regulates "ADMT in consequential decisions" |
| Developer + deployer duties | Lighter developer obligations |
| Focus on process compliance | Focus on outcome accountability |
| Pre-deployment documentation heavy | Post-deployment monitoring emphasis |

**Other US states with AI legislation in flight (2026):**
Multiple states queuing legislation behind Colorado. No federal law yet, but sector-specific guidance (healthcare, finance, employment) is accumulating.

**Facilitator Notes:**
- This is genuinely new content — the original module only covered EU
- Key insight for students: "If you sell AI into the US, you need to track state-by-state requirements"
- Common question: "Will there be a federal AI law?" Answer: "Not imminent, but the NIST AI RMF serves as de facto federal guidance"
- Time: 4 minutes
- ⚡ ADVANCED: deep-dive the SB 26-189 specifics for legal/compliance-focused students

---

### [NEW 2026] Slide 4: NIST AI RMF — The GenAI Profile & What's Coming

**Insert after:** NIST AI RMF section  
**Format:** Concept explanation

**Content:**

**NIST AI RMF 1.0 Status:**
- Still the current edition (no 2.0 as of mid-2026)
- Revision in progress: White House AI Action Plan (July 23, 2025) tasked NIST with revising to "eliminate references to misinformation, DEI, and climate change"
- Core 4-function structure unchanged: GOVERN → MAP → MEASURE → MANAGE

**The Generative AI Profile (AI 600-1) — Released July 2024:**
- Maps the AI RMF specifically to generative AI systems
- Covers **12 risk categories** with **200+ suggested actions**
- Now the most referenced companion document for enterprise AI risk management
- Explicitly addresses: hallucination, data privacy in training, IP/copyright, CBRN misuse, environmental costs

**New in 2025-2026: Cybersecurity × AI Integration:**
- NIST hosted Cybersecurity and AI Profile Workshop (April 2025)
- Creating profiles that bridge the Cybersecurity Framework (CSF) AND the AI RMF
- This is critical for agentic systems where AI + security intersect

**Third-Party Risk elevated to primary concern:**
- Supply chain vulnerabilities for AI models now explicitly addressed
- Third-party model assessment is a primary (not secondary) consideration
- Relevant for: fine-tuned models, MCP tool providers, RAG data sources

**Facilitator Notes:**
- The political context (White House revision) is sensitive — present factually, don't editorialise
- Student question: "Should we wait for 1.1?" Answer: "No. 1.0 + GenAI Profile is actionable now. Structure your risk management around the 4 functions regardless of wording changes."
- Time: 4 minutes

---

### [NEW 2026] Slide 5: ISO 42001 — From Emerging to Enterprise Standard

**Insert after:** ISO 42001 section  
**Format:** Case study / evidence

**Content:**

**ISO/IEC 42001:2023 has arrived.** Published December 2023, by April 2026 it is certified across:

| Organisation | Certified For | Significance |
|---|---|---|
| IBM | Granite models | First major model provider certified |
| Anthropic | Claude | Frontier AI model provider |
| Microsoft | 365 Copilot | Largest enterprise AI deployment |
| KPMG Australia | Advisory practice | Big Four accounting/consulting |
| Changi Airport (Singapore) | Operational AI systems | Critical infrastructure |
| Cornerstone OnDemand | Workforce AI platform | HR/enterprise SaaS |

**What ISO 42001 actually requires (AIMS — AI Management System):**
1. AI policy, objectives, and leadership commitment
2. Risk assessment specifically for AI systems
3. AI lifecycle management (development, deployment, retirement)
4. Data management and quality controls
5. Third-party and supply chain governance
6. Monitoring, measurement, and continual improvement
7. Transparency and explainability processes

**How it connects to other frameworks:**
- ISO 42001 provides the MANAGEMENT SYSTEM
- NIST AI RMF provides the RISK FUNCTIONS
- EU AI Act provides the LEGAL REQUIREMENTS
- Together they form a complete governance stack

**Facilitator Notes:**
- The certification list is powerful — name-drop these in class to show this isn't theoretical
- Student question: "Do we need to certify?" Answer: "Not legally required, but it's becoming a procurement prerequisite — especially for EU-facing business"
- Time: 4 minutes
- Relevant for all levels

---

### [NEW 2026] Slide 6: Governing Agentic AI — The New Challenge

**Insert after:** Responsible AI pillars section  
**Format:** Concept explanation — this is a major new topic

**Content:**

**The governance problem has changed.**

Traditional AI governance governs **outputs** (is this prediction fair? Is this classification explainable?).

Agentic AI governance must govern **actions** (did this agent have authority to send that email? Who is liable for this purchase order? What happens when agents coordinate without human oversight?).

**The Agentic Governance Gap:**
- Only 21% of enterprises have mature governance for autonomous agents
- 40% of agentic AI projects projected to fail by 2027 due to inadequate governance
- Starting Aug 2, 2026: any AI agent classified as high-risk must meet EU AI Act requirements for human oversight mechanisms and control systems

**The Four-Layer Agentic Operating Model** (Berkeley CMR, 2026):

```
Layer 4: ORGANIZATIONAL GOVERNANCE
  Accountability, culture, skills, policy

Layer 3: REAL-TIME CONTROL  
  Runtime enforcement, circuit breakers, kill switches

Layer 2: COORDINATION ARCHITECTURE
  Agent-to-agent protocols, handoff rules, scope boundaries

Layer 1: COGNITIVE SPECIALIZATION
  What each agent knows, can do, and is allowed to attempt
```

**The fundamental principle:** Governance must shift from documentation to enforcement — every AI action validated, monitored, and logged BEFORE execution.

**Facilitator Notes:**
- This is the MOST important new topic in the module — spend time here
- Open with: "Raise your hand if your org has a governance framework that covers what happens when one AI agent calls another AI agent to take an action on behalf of your company"
- Expected answer: near-zero hands. This creates the learning moment.
- Time: 5 minutes

---

### [NEW 2026] Slide 7: Five Pillars of Agentic Governance

**Insert after:** Agentic governance intro slide  
**Format:** Framework / concept

**Content:**

**The Five-Pillar Framework** (synthesised from RTSLabs, Berkeley CMR, and Galileo research):

| Pillar | What It Means | Implementation Pattern |
|---|---|---|
| **1. Decision Boundaries** | Define what agents can and cannot decide autonomously | Capability matrices; risk-tiered authority levels |
| **2. Runtime Enforcement** | Validate every action before execution (not after) | Guardrail APIs; permission checks at tool-call time |
| **3. Observability** | Full trace of reasoning chain + actions + outcomes | Structured logs; LLM traces; decision audit trails |
| **4. Human Oversight** | Structured intervention points at risk thresholds | HITL gates; escalation rules; approval workflows |
| **5. Accountability** | Clear ownership of agent behaviour and outcomes | Agent identity; responsible owner per agent class |

**Key design principle:** Not all decisions require the same level of control. Governance depends on correctly mapping risk levels to oversight models:

| Risk Level | Example | Oversight Model |
|---|---|---|
| Low | Summarise an email | Fully autonomous; log only |
| Medium | Draft a customer response | Autonomy + post-hoc review |
| High | Approve a £10K purchase order | Human approval required pre-execution |
| Critical | Modify production infrastructure | Human-in-the-loop with dual approval |

**Facilitator Notes:**
- Walk through each pillar with a concrete example from an agent system students might build
- Common question: "Doesn't this kill the value of autonomy?" Answer: Use the TacticalEdge framing — "compliance without killing autonomy"
- Time: 5 minutes

---

### [NEW 2026] Slide 8: Human-in-the-Loop for Agents — Architectural Patterns

**Insert after:** Five Pillars slide  
**Format:** Technical patterns (diagrams)

**Content:**

**HITL is not a checkbox — it's an architecture decision.**

Three production patterns for human oversight in agentic systems (from Galileo, 2026):

**Pattern 1: Gate-Based HITL**
```
Agent reasons → proposes action → GATE → human approves/rejects → execute/abort
```
- Best for: high-stakes actions (financial, legal, customer-facing)
- Latency cost: seconds to hours (depends on human availability)
- Risk: human fatigue if too many gates

**Pattern 2: Confidence-Threshold HITL**
```
Agent reasons → confidence score → if < threshold → escalate to human
                                  → if ≥ threshold → auto-execute + log
```
- Best for: medium-risk actions with variable certainty
- Requires: calibrated confidence scoring (not trivial)
- Risk: model overconfidence passes unsafe actions

**Pattern 3: Audit-Trail HITL (post-hoc)**
```
Agent reasons → executes → logs full chain → human reviews batch async
```
- Best for: low-risk, high-volume actions
- Enables: statistical sampling, anomaly detection
- Risk: damage done before review catches it

**Which pattern when?**
- Use Pattern 1 for irreversible, high-value actions
- Use Pattern 2 for reversible but customer-visible actions
- Use Pattern 3 for internal, reversible, low-impact actions
- Most production systems use ALL THREE at different points in the workflow

**Facilitator Notes:**
- Draw the three patterns on whiteboard while explaining
- Student question: "What if the human doesn't respond?" — Design for this: timeout → safe default (reject/queue)
- Time: 4 minutes
- ⚡ ADVANCED: discuss confidence calibration challenges

---

### [NEW 2026] Slide 9: AI FinOps — Why Token Prices Fall But Bills Rise

**Insert after:** FinOps for AI section  
**Format:** Data-driven concept explanation

**Content:**

**The AI FinOps Paradox (2026):**
- Per-token costs have fallen 90%+ since GPT-4 launch
- Yet total enterprise AI spend is rising FASTER than total cloud spend
- Reason: volume explosion — especially from agentic workflows

**Key data points:**
- Agentic workflows consume **5–30× more tokens** per business task than single-shot chatbot calls (UD.hk/2026 FinOps Report)
- Cloud waste rose to **29% for first time in 5 years** — driven by AI workloads (Flexera 2026)
- Among enterprises spending >$100M/yr on cloud: unit cost of AI fell, but total AI spend rose faster

**Why traditional FinOps doesn't work for AI:**

| Traditional Cloud FinOps | AI FinOps |
|---|---|
| Predictable request volume | Unpredictable token consumption |
| Stable compute units (vCPU, RAM) | Variable units (tokens, GPU-seconds, model calls) |
| Easy cost attribution (service → team) | Hard attribution (agent call → sub-agent → tool → model) |
| Bill correlates with usage | Bill correlates with reasoning complexity |

**BCG's "Return on AI" metric:**
> Traditional cost-per-token is insufficient. "Return on AI" captures the full cost of the AI being applied — including retries, failures, manual correction, latency costs, and support effort.

**Facilitator Notes:**
- The "paradox" framing hooks students immediately
- Ask: "Has anyone here been surprised by an AI bill?" — gets engagement
- Key insight: "A cheaper model that fails more often can INCREASE total cost"
- Time: 4 minutes

---

### [NEW 2026] Slide 10: Agentic FinOps — Governing Unbounded Inference

**Insert after:** AI FinOps paradox slide  
**Format:** Technical patterns

**Content:**

**The New Problem: Unbounded Inference**

Unlike traditional APIs where request volume is predictable, AI agents make **runtime decisions** about:
- How many tokens to consume per step
- Which models to invoke (routing decisions)
- How many reasoning loops to execute
- Whether to spawn sub-agents (multiplicative cost)

**The Agentic Cost Architecture (6 Controls):**

1. **Token budgets per task** — Hard caps on total tokens an agent can consume for a single business task. Kill the loop if exceeded.

2. **Model routing** — Route each call to the cheapest model capable of meeting the quality bar. Not every sub-task needs GPT-4/Claude Opus.

3. **Cost attribution to business outcomes** — Every inference call tagged to a feature, team, AND business outcome. "What did each token achieve?"

4. **Retry circuit breakers** — Cap retry attempts (e.g., max 2 retries per tool call). A misconfigured retry loop can burn thousands.

5. **Agent-level cost dashboards** — Real-time per-agent spend visibility. Alert thresholds per agent class.

6. **Inference budget governance** — Quarterly/monthly token budgets per team, with approval workflows for overages.

**Tool landscape (2026):**
- Finout (AI-specific FinOps)
- CloudZero (AI cost intelligence)
- Amnic (multi-provider token tracking)
- AWS Cost Explorer (Bedrock usage reports)
- Usage.ai (AI KPI playbook)

**Facilitator Notes:**
- Practical: walk through a real scenario of an agentic workflow's cost explosion
- Example: "A multi-agent research pipeline that was budgeted at $2/query but averaged $47/query because sub-agents spawned recursively"
- Time: 5 minutes
- ⚡ ADVANCED: discuss model routing architectures in depth

---

### [NEW 2026] Slide 11: Frontier Model Governance — When Models Outperform Humans at Hacking

**Insert after:** Emerging frontier section  
**Format:** Case study / concept

**Content:**

**The Mythos Moment (2026):**
- Anthropic's Claude Mythos (higher-capability model) **outperforms humans at some hacking and cybersecurity tasks**
- This wasn't designed — it emerged as a byproduct of improved reasoning and code generation
- Forbes: "Frontier models turn AI safety into a fiduciary responsibility"

**Anthropic's Response — The 8 Governance Mechanisms (Claude Fable 5 System Card, June 2026):**

1. **Visible Safety Fallback** — High-risk queries (bio, chem, cyber) trigger automatic downgrade to safer model + user notice
2. **Tiered Access** — Mythos restricted to "trusted partners"; Fable (public) ships with surgical safety classifiers
3. **319-page System Card** — Most detailed governance documentation ever published for a frontier model
4. **Capability-based restriction** — Not all users get all capabilities
5. **Post-deployment monitoring** — Continuous safety evaluation
6. **Red-teaming at scale** — Pre-release adversarial testing
7. **Model-to-model safety cascades** — Safer model validates outputs of more capable model
8. **Responsible disclosure timeline** — Vulnerability reporting process

**The Reasoning Model Safety Problem:**
- Research finding: "The thinking process in reasoning models poses GREATER safety concerns than their final answers" (arXiv 2502.12659)
- The stronger the reasoning ability, the greater the potential harm when answering unsafe questions
- Distilled reasoning models show POORER safety than their safety-aligned base models

**Facilitator Notes:**
- This is a powerful class discussion moment: "At what point does a model become too capable to deploy widely?"
- Student question: "Should reasoning models be regulated differently?" — Use OpenAI o3-mini System Card as reference: scored Medium for Persuasion, CBRN, and Model Autonomy
- Time: 5 minutes
- Suitable for all levels — make it concrete, not abstract

---

### [NEW 2026] Slide 12: AI Compliance Tooling — The 2026 Market

**Insert after:** Governance frameworks section  
**Format:** Comparison table / tools overview

**Content:**

**The compliance tooling market has matured rapidly.** The days of "governance by spreadsheet" are over.

**Top AI Compliance Platforms (2026):**

| Platform | Strength | EU AI Act | ISO 42001 | NIST RMF |
|---|---|---|---|---|
| **OneTrust** | Full GRC + AI governance module | ✅ | ✅ | ✅ |
| **Vanta** | Security compliance + AI agent for evidence | ✅ | Partial | ✅ |
| **Modulos** | AI-specific governance; EU AI Act focus | ✅ | ✅ | ✅ |
| **Holistic AI** | Auditing + bias detection + compliance | ✅ | ✅ | ✅ |
| **Centraleyes** | Risk management + regulatory mapping | ✅ | ✅ | ✅ |
| **LogicGate** | Workflow-based GRC | ✅ | Partial | ✅ |
| **Drata** | Automation-first compliance | ✅ | Partial | ✅ |

**Two distinct jobs these tools solve:**
1. **Governing and documenting an AI programme** — Inventories, risk assessments, audit evidence, framework mapping
2. **Technical compliance testing** — Bias detection, fairness metrics, explainability scoring, model monitoring

**Key insight from Legiscope (2026):**
> "The market is still catching up. Most tools solve workflow problems but store audit logs in vendor-managed environments — outside your defined perimeter."

**What to look for:**
- Automated evidence collection (not manual uploads)
- Real-time regulatory change monitoring
- Multi-framework mapping (EU AI Act + ISO 42001 + NIST simultaneously)
- API integration with your ML pipeline (not a separate system)

**Facilitator Notes:**
- Don't endorse a specific vendor — present as a landscape
- Demo tip: if possible, show a 2-minute walkthrough of Modulos or Holistic AI's free tier
- Student question: "Which one should we buy?" — Answer depends on their existing GRC stack
- Time: 4 minutes

---

### [NEW 2026] Slide 13: AI Auditing — From Model Cards to Proof Bundles

**Insert after:** Compliance tooling slide  
**Format:** Concept explanation

**Content:**

**The evolution of AI documentation:**

```
2020: Model Cards (Google)
  → What the model is, how it was trained, performance metrics

2022: System Cards (OpenAI)
  → Model + deployment context + safety evaluations

2024: Risk Cards / Impact Assessments
  → Model + system + societal impact + mitigations

2026: PROOF BUNDLES
  → Traceability linking EVERY decision to exact data inputs 
     + model configuration + timestamp AT DECISION TIME
```

**What a proof bundle contains:**
- The specific model version (commit hash / model ID)
- The exact input data that produced the decision
- The configuration parameters active at decision time
- The decision output and confidence score
- Any human overrides or approvals in the chain
- Timestamp and audit trail

**Why this matters now:**
- EU AI Act requires "traceability" for high-risk systems
- ISO 42001 requires "monitoring, measurement, and continual improvement"
- MLflow (2026): "Regulators treat AI outputs as extensions of human decision-making authority"
- Every automated decision now carries legal and reputational weight

**The three types of AI audit:**

| Audit Type | What It Checks | When |
|---|---|---|
| **Pre-deployment** | Conformity assessment, risk classification, bias testing | Before go-live |
| **Continuous** | Runtime monitoring, drift detection, fairness metrics over time | Ongoing |
| **Incident-driven** | Root cause analysis, decision reconstruction, liability determination | After an event |

**Facilitator Notes:**
- Connect to Module 15 (Observability) — the traces you build there are the raw material for audits here
- Key message: "If you can't reconstruct WHY a decision was made at a specific point in time, you fail the audit"
- Time: 4 minutes

---

### [NEW 2026] Slide 14: Building an AI Centre of Excellence (CoE) — 2026 Patterns

**Insert after:** AI CoE section  
**Format:** Framework / organisational design

**Content:**

**The AI CoE has evolved from a "nice to have" to an operational necessity.**

**Three CoE Models in Production (2026):**

| Model | Structure | Best For |
|---|---|---|
| **Centralised** | Single team owns all AI governance + standards + tooling | Organisations early in AI maturity; need consistency |
| **Federated** | Central team sets policy; embedded AI leads in each BU execute | Large enterprises with multiple AI teams |
| **Hybrid/Hub-and-Spoke** | Central platform team + distributed domain specialists | Most common in practice; balances speed and control |

**What a mature AI CoE actually owns (2026):**
1. AI policy and responsible AI principles
2. Framework compliance (EU AI Act, NIST, ISO 42001)
3. Model and agent registry
4. Evaluation standards and benchmark suites
5. FinOps governance (token budgets, model routing policies)
6. Incident response for AI failures
7. Training and upskilling programmes (like this course!)
8. Vendor evaluation and procurement standards

**Anti-patterns to avoid:**
- ❌ CoE as "AI police" — creates adversarial relationship with builders
- ❌ CoE without engineering representation — produces unimplementable policy
- ❌ CoE without executive sponsor — gets ignored
- ❌ CoE that only reviews, never enables — slows everyone down

**Facilitator Notes:**
- Ask students: "Does your org have an AI CoE? What model is it?" — generates good discussion
- Key insight: the best CoEs are 60% enablement, 40% governance
- Time: 4 minutes

---

### [NEW 2026] Slide 15: The Agent Identity Problem — Who Did What?

**Insert after:** Agentic governance section  
**Format:** Discussion / emerging challenge

**Content:**

**When agents act autonomously, traditional identity and access management breaks down.**

**The problem:**
- Traditional IAM: Human → credentials → action → audit log
- Agentic IAM: Human → agent → sub-agent → tool → external system → action → ???

**Questions that governance must answer:**
1. Does each agent have a distinct identity?
2. Can you trace any action back to a specific agent instance?
3. Can you trace that agent back to the human who authorised it?
4. If an agent calls another agent, who owns the outcome?
5. If an agent's tool call triggers a real-world action (purchase, email, deployment), who is liable?
6. Can you revoke an agent's permissions without affecting others?

**Emerging patterns:**
- **Agent-as-service-account** — Each agent class gets a dedicated service identity with scoped permissions
- **Delegation chains** — Formal record of authority delegation from human → primary agent → sub-agents
- **Action provenance** — Every action carries a full provenance chain (who authorised → who delegated → who executed)
- **Capability-based security** — Agents get fine-grained capabilities (not broad role-based access)

**Facilitator Notes:**
- This is a genuinely unsolved problem in most enterprises — acknowledge that
- Discussion prompt: "Your company's AI agent sends a legally binding email to a customer. Who is responsible?"
- Time: 4 minutes
- ⚡ ADVANCED: discuss MCP security implications (agent ↔ tool trust boundaries)

---

### [NEW 2026] Slide 16: Responsible AI in Practice — Beyond Principles to Measurement

**Insert after:** Responsible AI pillars section  
**Format:** Practical framework

**Content:**

**The era of "principles without measurement" is over.**

In 2026, responsible AI requires operational metrics — not just ethical statements.

**Measurable Responsible AI KPIs:**

| Pillar | Metric | Target Example |
|---|---|---|
| **Fairness** | Demographic parity ratio across protected groups | Within 0.8–1.2 range |
| **Explainability** | % of decisions with human-readable explanation available | >95% for high-risk |
| **Accountability** | % of AI systems with documented responsible owner | 100% |
| **Privacy** | PII exposure rate in model outputs (measured via red-teaming) | <0.01% |
| **Transparency** | % of AI-generated content properly labelled (Art 50 req) | 100% post-Aug 2026 |
| **Safety** | Harmful output rate post-guardrails | <0.1% on safety benchmarks |
| **Robustness** | Performance degradation under adversarial input | <5% accuracy drop |

**The measurement stack:**
- Define metrics per pillar at design time (Module 6 — AI-DLC)
- Implement measurement at deploy time (Module 15 — Observability)
- Report and act at governance time (this module)

**Facilitator Notes:**
- Key message: "If you can't measure it, you can't govern it"
- Connect back: "Remember the observability module? This is WHY you need those traces"
- Time: 3 minutes

---

### [NEW 2026] Slide 17: AI Risk Tiering — Operationalising Risk Classification

**Insert after:** Responsible AI measurement slide  
**Format:** Practical decision framework

**Content:**

**Every organisation needs an internal AI risk classification that maps to their governance controls.**

**The Four-Tier Model (aligned to EU AI Act concepts):**

| Tier | Risk Level | Governance Requirements | Example |
|---|---|---|---|
| **Tier 0** | Minimal | Register in AI inventory; standard dev practices | Internal summarisation tool |
| **Tier 1** | Limited | + Transparency labelling; + basic monitoring | Customer-facing chatbot |
| **Tier 2** | High | + Conformity assessment; + HITL gates; + bias testing; + incident response plan | Hiring screening; credit scoring |
| **Tier 3** | Unacceptable | PROHIBITED — do not build | Social scoring; real-time biometric mass surveillance |

**For agentic systems, add:**

| Agent Autonomy Level | Additional Requirements |
|---|---|
| Copilot (human confirms every action) | Standard Tier 1 governance |
| Semi-autonomous (acts within defined bounds) | Tier 2 + action logging + rollback capability |
| Fully autonomous (acts independently) | Tier 2 or 3 + real-time monitoring + kill switch + delegation audit |

**How to classify:**
1. What decisions does the system make/influence?
2. Who is affected and how severely?
3. Is the action reversible?
4. What is the autonomy level?
5. Is it covered by sector-specific regulation (healthcare, finance, employment)?

**Facilitator Notes:**
- Hands-on: have students classify 3-4 example AI systems using this framework
- Student question: "Who decides the tier?" — Answer: AI CoE or Risk function, with input from the product/engineering team
- Time: 4 minutes

---

### [NEW 2026] Slide 18: Governance for Multi-Agent Systems — Chain of Responsibility

**Insert after:** Agent identity slide  
**Format:** Architecture pattern

**Content:**

**When agents call agents, governance must follow the chain.**

**The Chain of Responsibility Pattern:**

```
BUSINESS OWNER (human)
    │
    ▼
ORCHESTRATOR AGENT (high privilege, heavily monitored)
    │
    ├── SUB-AGENT A (scoped: read-only data access)
    │       └── TOOL CALL → external API
    │
    ├── SUB-AGENT B (scoped: draft content only)
    │       └── TOOL CALL → internal system
    │
    └── SUB-AGENT C (scoped: execute within budget)
            └── TOOL CALL → payment system → REQUIRES HUMAN GATE
```

**Governance rules for multi-agent chains:**
1. **Principle of least privilege** — each agent gets minimum permissions needed
2. **No privilege escalation** — sub-agent cannot gain permissions its parent doesn't have
3. **Visibility obligation** — orchestrator must log all delegations
4. **Budget propagation** — token/action budgets flow down and cannot be exceeded in aggregate
5. **Termination authority** — any agent in the chain can be killed independently
6. **Accountability roll-up** — all sub-agent actions attribute to the orchestrator owner

**Facilitator Notes:**
- Draw this chain live on whiteboard
- Connect to Module 12 (Multi-Agent Systems) — the architecture decisions there have governance implications here
- Key principle: "The orchestrator is accountable for everything its sub-agents do"
- Time: 4 minutes
- ⚡ ADVANCED: discuss MCP tool-calling trust boundaries

---

### [NEW 2026] Slide 19: The Road Ahead — What's Coming 2027–2028

**Insert after:** Emerging frontier section  
**Format:** Forward-looking discussion

**Content:**

**The next 18 months will bring:**

1. **EU AI Act Annex III enforcement (Dec 2027)** — The "main wave" of high-risk system compliance. Every enterprise with AI in hiring, credit, healthcare, law enforcement, or critical infrastructure must be conformity-assessed.

2. **Reasoning model regulation** — Models that "think" pose unique risks (the thinking is more dangerous than the output). Expect regulatory attention to chain-of-thought transparency.

3. **Agent-to-agent liability frameworks** — When Agent A hires Agent B (via MCP or A2A protocol), who is liable for Agent B's actions? Legal frameworks will emerge.

4. **AI-generated content at scale** — Watermarking obligations activate Dec 2026. Detection arms race between generators and detectors.

5. **Sovereign AI** — More nations demanding AI models trained on local data, deployed on local infrastructure, governed by local law.

6. **AI auditor profession** — Formalisation of the "AI auditor" role. Certification programmes emerging (ISO 42001 Lead Auditor already exists).

7. **FinOps for agents as standard practice** — Token budgets and model routing will be as standard as cloud resource tagging.

8. **"AI Supply Chain" as a governance domain** — Model provenance, training data lineage, and tool-provider trust will need formal governance.

**Facilitator Notes:**
- End the module on a forward-looking note — students should leave knowing what to watch
- Discussion: "Which of these 8 trends will affect YOUR work first?"
- Time: 4 minutes

---

### [NEW 2026] Slide 20: Action Plan — What to Do Monday Morning

**Insert after:** Road Ahead slide (final content slide)  
**Format:** Practical checklist / call to action

**Content:**

**Your governance action plan — start here:**

**Week 1: Assess**
- [ ] Do you have an AI inventory? (List every AI system deployed or in development)
- [ ] Are your AI systems risk-classified? (Use the 4-tier model)
- [ ] Do you know which of your systems are "high-risk" under the AI Act?

**Week 2: Framework**
- [ ] Adopt a primary framework (ISO 42001 for management system; NIST AI RMF for risk functions)
- [ ] Define responsible AI metrics for each pillar
- [ ] Establish a governance forum (even if informal)

**Week 3: Agentic Readiness**
- [ ] Do your agents have distinct identities and scoped permissions?
- [ ] Is there a human-in-the-loop gate for high-risk actions?
- [ ] Can you reconstruct the reasoning chain for any agent action?

**Week 4: Operational**
- [ ] Set up AI FinOps: token budgets, cost attribution, model routing
- [ ] Implement basic observability (Module 15) for audit trail
- [ ] Document your first "proof bundle" for one production AI system

**Ongoing:**
- [ ] Monitor regulatory changes (EU Omnibus finalisation, US state laws)
- [ ] Build toward ISO 42001 certification (even if not certifying yet, the structure helps)
- [ ] Train your team (start with this course!)

**Facilitator Notes:**
- Print this as a handout — students take it away
- Frame as: "You don't need to do all of this. But you need to START."
- End on an empowering note: "You now have the knowledge. The gap between you and your peers just closed."
- Time: 3 minutes (close the module)

---

## STEP 4: FACILITATOR UPDATE BRIEF

---

### 🎤 Top 3 Most Important Additions

1. **Agentic AI Governance (Slides 6–8, 15, 18)** — This is the biggest gap in the original module. Enterprises are deploying agents NOW and have no governance for them. The four-layer model, five-pillar framework, and HITL patterns are immediately actionable.

2. **EU AI Act Post-Omnibus Timeline (Slide 2)** — The original timeline is WRONG. The Digital Omnibus changed everything. Every student who previously learned "Aug 2026 for high-risk" needs correcting to "Dec 2027."

3. **AI FinOps as a governance discipline (Slides 9–10)** — The paradox of falling token prices + rising bills is universally relatable and connects governance to real business outcomes. The "unbounded inference" problem from agentic systems is genuinely new.

---

### 🔄 What in the Original is Now Outdated

| Original Content | Issue | How to Address |
|---|---|---|
| "Aug 2026 is the main high-risk deadline" | Pushed to Dec 2027 by Omnibus | Replace with Slide 2; acknowledge the change explicitly |
| ISO 42001 presented as "emerging" | Now widely adopted by major companies | Update with Slide 5 certification examples |
| FinOps as simple token cost awareness | Now a full discipline with dedicated tools | Replace with Slides 9–10 |
| No US regulatory content | Colorado AI Act replaced; multi-state landscape | Add Slide 3 |
| Frontier trends as speculative | Mythos/Fable 5 made them concrete | Add Slide 11 with real system card data |

---

### ⏱️ How to Fit in 60 Minutes

The original 60-minute module can accommodate 5–7 of these new slides by:
- Compressing the EU AI Act section to the updated timeline (Slide 2 replaces the old one, doesn't add to it)
- Compressing ISO 42001 (Slide 5 replaces old mention)
- Adding agentic governance (Slides 6–7) as the new "core" section (~10 min)
- Adding FinOps update (Slides 9–10) (~8 min)
- Closing with Road Ahead + Action Plan (Slides 19–20) (~7 min)

**Recommended 60-minute agenda with updates:**

| Time | Content | Slides |
|---|---|---|
| 0–5 | Opening + 2026 Reality Check | Slide 1 |
| 5–15 | Regulatory landscape (EU Omnibus + US + NIST + ISO 42001) | Slides 2–5 |
| 15–30 | Agentic AI Governance (core new content) | Slides 6–8, 15 |
| 30–40 | AI FinOps + Unbounded Inference | Slides 9–10 |
| 40–48 | Compliance tooling + Auditing + Measurement | Slides 12–13, 16 |
| 48–55 | Road Ahead + Discussion | Slide 19 |
| 55–60 | Action Plan + Close | Slide 20 |

**If extended to 90 minutes:** Add frontier model governance (Slide 11), multi-agent governance chain (Slide 18), risk tiering hands-on exercise (Slide 17), and the full AI CoE discussion (Slide 14). The 90-minute version is recommended for senior/governance-focused audiences.

---

### 🛠️ New Tools/Accounts/Demos to Set Up

1. **Modulos.ai** — Free tier available; can demo EU AI Act compliance workflow
2. **Holistic AI** — Has a risk assessment demo that takes 5 minutes
3. **FinOps.org AI overview page** — Good handout/reference (finops.org/wg/finops-for-ai-overview/)
4. **Anthropic Claude Fable 5 System Card** — 319 pages; excerpt key governance mechanisms for class reference
5. **EU AI Act timeline visual** — Print the Omnibus-updated timeline from Slide 2 as a large poster/handout
6. **ISO 42001 certification list** — Show the IBM/Anthropic/Microsoft examples on screen (from enz.ai)

---

*Module 16 Update — Generated July 2026 | Based on web research conducted July 5, 2026*
