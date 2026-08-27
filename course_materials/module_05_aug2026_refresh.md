# Module 05: Building Your AI Roadmap — August 2026 Content Refresh

**Module:** 05 — Building Your AI Roadmap  
**Track:** Strategy  
**Refresh Date:** 12 August 2026  
**Previous Update:** July 2026  

---

## A) EXECUTIVE SUMMARY — What Changed Since July 2026

1. **Gartner's Agent Sprawl is now quantified**: By 2028, the average Fortune 500 will run 150,000+ AI agents (up from <15 in 2025). Only 13% of organisations believe they have adequate governance. This is the single biggest roadmap risk for H2 2026.

2. **OWASP released a dedicated Agentic AI Security Maturity Framework** (published 3 June, presented at Infosecurity Europe 4 June 2026): A two-axis model mapping deployment type (AT0–AT5) against governance maturity (Level 0–3). Immediately actionable for roadmap governance sections.

3. **ActivTrak's 120,000-worker study reveals the "2% problem"**: Only 2% of the workforce has reached the AI maturity stage where AI transforms workflows. 82% maintain their level quarter-over-quarter — once trained, benefits compound. This has major implications for the 70% (people/process) investment in roadmaps.

4. **OpenAI declares "past the experimentation phase"** (6 August 2026): Enterprise now >40% of OpenAI revenue; APIs process 15B tokens/minute; shift from individual copilots to "managing teams of agents." Introduced Workspace Agents and OpenAI Frontier as unified enterprise layer.

5. **Anthropic's 2026 State of AI Agents Report** (based on 500+ technical leaders): 57% of organisations deploy agents for multi-stage workflows; 81% plan more complex use cases in 2026; 39% developing multi-step agents. Claude Managed Agents launched (10 July 2026) for production-grade deployment.

6. **Gartner predicts enterprises will abandon assistive AI for outcome-focused workflows by 2028** (2 April 2026): Over half will stop paying for copilots/smart advisors in favour of platforms that commit to workflow results — validates the Defend/Extend/Upend model from July update.

7. **AWS published "Operationalizing Agentic AI on AWS"** — prescriptive guidance treating agentic AI as "a new operational paradigm, not a feature." Covers lifecycle management, trust enforcement, interoperability, and alignment to business models.

8. **HBR's "Manage Your AI Investments Like a Portfolio"** (Jan 2026) now widely cited: Dual-lens approach (advancement pipeline with gates + whole-portfolio dashboard across risk/return, time horizon, capabilities). Reinforces the Three-Horizon model from July update.

9. **Gartner's proportional governance**: 40% of enterprises will demote/decommission autonomous AI agents by 2027 due to governance gaps discovered only after production incidents. Binary governance (locked down OR fully trusted) is the root cause of failure.

10. **The Atlassian AI Efficiency Paradox** (June 2026): AI helps individuals work faster, but output backs up at reviews, approvals, and human-judgment gates — wiping out speed gains. Roadmaps must include bottleneck redesign, not just AI deployment.

---

## B) NEW SLIDES [NEW AUG-2026]

---

### [NEW AUG-2026] Slide 1: Agent Sprawl — The 150,000 Agent Problem

**Insert after:** Slide 9 (Agent Washing & Workslop)  
**Source:** Gartner Press Release, 28 April 2026; IBM Think, May 2026

**Content:**

**The headline statistic:**
> "By 2028, an average global Fortune 500 enterprise will have over 150,000 agents in use, up from less than 15 in 2025." — Gartner, April 2026

**Why this matters for your roadmap:**
- Only 13% of organisations believe they have the right AI agent governance in place (Gartner)
- By 2027, 40% of enterprises will demote or decommission autonomous AI agents due to governance gaps discovered only after production incidents
- "If employees are unable to work in sanctioned tools, they will go around controls and start using shadow AI — which presents far greater risks." — Max Goss, Gartner

**Gartner's 6-Step Agent Governance Framework:**

| Step | Action |
|------|--------|
| 1 | Establish agent governance and policies (who can build, share, connect) |
| 2 | Build centralised agent inventory (use AI TRiSM tools to discover & categorise) |
| 3 | Define agent identity, permissions & lifecycle model |
| 4 | Develop AI information governance (what data agents can access) |
| 5 | Monitor & remediate agent behaviour (ongoing compliance, anomaly detection) |
| 6 | Foster a culture of responsible AI usage (training, community of practice) |

**Roadmap implication:**
- Every agentic roadmap now needs an "Agent Governance" workstream running in parallel
- Sprint 0 should include an agent inventory audit — most organisations don't know what agents they already have
- Budget for AI TRiSM tooling in your platform layer

**Facilitator Notes:**
- The jump from <15 to 150,000 agents in 3 years is the "Holy sh*t" moment — let it land
- Ask: "How many agents does your organisation have RIGHT NOW? Does anyone know?" (Usually nobody does)
- This slide pairs with Slide 9 (Agent Washing) — sprawl + washing = chaos
- Time: 5 minutes

---

### [NEW AUG-2026] Slide 2: The OWASP Agentic AI Security Maturity Framework

**Insert after:** Slide 1 (Agent Sprawl) or Governance section  
**Source:** OWASP GenAI Security Project, "State of Agentic AI Security and Governance," 3 June 2026; Infosecurity Europe presentation, 4 June 2026

**Content:**

**The problem OWASP is solving:**
> "Most organizations are deploying agents faster than they can govern them. Governance is still operating at maturity levels designed for AI copilots while teams are shipping multi-agent systems." — Ariel Fogel, Pillar Security / OWASP

**Two-axis maturity model:**

**Axis 1 — What are you deploying? (Adoption Tiers AT0–AT5)**

| Tier | Type | Risk Level |
|------|------|-----------|
| AT0 | Shadow AI (no org awareness) | Uncontrolled |
| AT1 | Vendor embedded assistant | Low (vendor-managed) |
| AT2 | Platform integrated (your data, no code execution) | Moderate |
| AT3 | Citizen developer agent (low-code, org data) | Elevated |
| AT4 | Code-executing agent (generates & runs code) | High |
| AT5 | Custom in-house agent (you built it; you own it) | Highest |

**Axis 2 — How mature is your governance? (Levels 0–3)**

| Level | Description |
|-------|-------------|
| 0 | Unaware / ad hoc — no policies, minimal logging |
| 1 | Experimentation without guardrails — pilots lack autonomy limits |
| 2 | Policy-defined, human-in-the-loop — formal policies, CAIO owner, periodic monitoring |
| 3 | Integrated, continuous oversight — real-time dashboards, kill switches, governance-as-code |

**The decision rule:**
- Map each agent to its deployment tier
- Check governance maturity
- If governance < deployment tier requirements → **either invest in controls OR reduce agent autonomy**
- "Don't operate in the red cells" — Fogel

**Facilitator Notes:**
- This is immediately useful for any student running agentic pilots — they can classify their agents TODAY
- The OWASP framework complements the 6 readiness dimensions from July's update
- For advanced: discuss how governance-as-code (Level 3) relates to DevOps/GitOps practices
- Time: 6 minutes

---

### [NEW AUG-2026] Slide 3: The 2% Problem — Why Most Workers Stall at AI Experimentation

**Insert after:** BCG 10-20-70 Rule (Slide 2 from July update)  
**Source:** ActivTrak Productivity Lab, "AI Adoption Maturity 1H 2026" (analysis of 120,620 workers, published July 2026)

**Content:**

**The breakthrough finding:**
> "Only 2% of workers have reached the stage of AI adoption maturity where AI transforms workflows." — ActivTrak, July 2026

**What the data shows:**
- 95% of companies have adopted AI to some degree (by early 2025)
- Average organisation now uses 7 AI tools (up from 2 in 2023)
- AI users average 6h 34min productive daily (vs 6h 17min for non-users) — a persistent 17-min gap
- 82% of AI users maintain their maturity level quarter-over-quarter
- Few progress beyond experimentation or task-level assistance

**The 4-stage behavioural maturity model (ActivTrak):**

| Stage | Behaviour | % of Workforce |
|-------|-----------|---------------|
| 1 — Aware | Occasional use, no workflow change | ~60% |
| 2 — Experimenting | Regular use for tasks, not workflows | ~30% |
| 3 — Integrating | AI embedded in daily workflows | ~8% |
| 4 — Transforming | AI fundamentally reshapes how work is done | **~2%** |

**The compounding insight:**
- 80% of Stage 2 users and 70% of Stage 3 users maintain their levels Q-over-Q
- Once a worker crosses into advanced adoption, it forms a **permanent habit**
- Every investment in training and enablement compounds over time

**Roadmap implication:**
- The 70% (people & process) investment isn't optional — it's what moves workers from Stage 1 to Stage 3+
- ROI doesn't come from tool deployment — it comes from behavioural change
- Budget for enablement programmes, not just licenses

**Facilitator Notes:**
- The "2% vs 95%" paradox is a powerful frame: almost everyone has AI, almost nobody transforms with it
- Ask: "What stage are YOU at? What about your team?"
- The compounding insight is key for ROI conversations: invest in training → permanent productivity gain
- Time: 5 minutes

---

### [NEW AUG-2026] Slide 4: The AI Efficiency Paradox — When Speed Creates Bottlenecks

**Insert after:** Process Redesign Before Automation (Slide 10 from July update)  
**Source:** Atlassian, "The AI Efficiency Paradox," June 2026; HBR, "AI Doesn't Reduce Work — It Intensifies It," Feb 2026

**Content:**

**The paradox:**
> "As AI helps individuals work faster, the surge of output backs up at reviews, approvals, and other human-judgment gates, slowing down the flow and wiping out the speed gains." — Atlassian, June 2026

**How this manifests:**
```
Individual AI user: Produces 3× more output per day
→ Manager/reviewer: Now has 3× more to review (same hours)
→ Approval queue: Backs up
→ Total cycle time: UNCHANGED or WORSE
```

**HBR reinforces (Feb 2026):**
> "AI doesn't reduce work — it intensifies it. Companies worried about getting more employees to use AI should first ask whether the organisation can absorb the output."

**The roadmap fix — redesign the FLOW, not just the TASK:**
1. Identify human-judgment gates downstream of AI-accelerated tasks
2. Ask: Can any gates be automated, eliminated, or parallelised?
3. Redesign approval workflows before deploying AI upstream
4. Measure cycle time (end-to-end), not just task time (individual)

**Implications for the Three-Horizon Portfolio:**
- H1 Quick Wins must include gate redesign alongside tool deployment
- Any initiative that only accelerates individual tasks without addressing flow = workslop risk
- Add "bottleneck analysis" as a mandatory step in initiative scoping

**Facilitator Notes:**
- Engineers LOVE this slide because it's a systems thinking problem — it's not "soft stuff"
- Draw the queuing diagram: fast input → slow gate → backed up queue
- Connects to Deloitte's "process redesign before automation" — this is the specific mechanism that explains WHY
- Time: 5 minutes

---

### [NEW AUG-2026] Slide 5: Gartner's Assistive → Outcome-Focused Shift

**Insert after:** Defend/Extend/Upend (Slide 14 from July update)  
**Source:** Gartner Press Release, 2 April 2026

**Content:**

**The prediction:**
> "By 2028, over half of all enterprises will stop paying for assistive intelligence (copilots, smart advisors) and instead favour platforms that commit to workflow RESULTS." — Gartner, April 2026

**What this means for roadmaps:**

| Era | Focus | Metric | Example |
|-----|-------|--------|---------|
| 2023–2025 | Assistive AI | "Did the user engage?" | Writing assistants, summarisation |
| 2026–2028 | Outcome AI | "Did the business result improve?" | Agent completes the task end-to-end |

**The implication for your portfolio:**
- "Defend" projects (copilots, assistants) → being commoditised; enterprise willingness to pay declining
- "Extend" projects (outcome-focused agents) → where budget is shifting
- Roadmaps heavy on assistive tools face obsolescence risk by 2028

**Gartner's additional predictions (2026 Hype Cycle for Agentic AI):**
- Only 17% of organisations have deployed AI agents to date
- More than 60% expect to within two years — most aggressive adoption curve ever measured
- 40% of enterprise applications will embed task-specific agents by end of 2026 (up from <5% in 2025)
- By 2028, 45% of CIOs will lead AI agent systems outside IT

**Facilitator Notes:**
- This validates the Defend/Extend/Upend from last month — now with a timeline (2028 deadline for the shift)
- For students with large copilot deployments: "You're not wrong, you're just early-stage. The question is: what's your path from assistive to outcome?"
- The 17% deployed / 60% intending gap = massive opportunity window for organisations that move now
- Time: 5 minutes

---

### [NEW AUG-2026] Slide 6: AI Portfolio Governance — When Informal Fails

**Insert after:** Three-Horizon Portfolio (Slide 6 from July update)  
**Source:** Bizzdesign, "AI Portfolio Management," July 2026; DataGalaxy, "Regain Control," June 2026; HBR, Jan 2026

**Content:**

**The portfolio governance problem:**
> "The biggest blocker for CDAOs and Heads of Data/AI is the lack of organising their AI investments like an AI portfolio. Fundamentals of portfolio management — visibility, accountability, cost governance, lifecycle management — are missing." — DataGalaxy, June 2026

**Six signs your AI portfolio has outgrown informal governance** (Bizzdesign, July 2026):
1. You can't reliably answer "where is AI being used?"
2. Nobody can say "who owns this model/agent?"
3. No one tracks what risks each AI initiative carries
4. You can't measure whether it's delivering value
5. Duplicate initiatives exist across teams without awareness
6. Isolated approvals aren't preventing sprawl

**HBR's dual-lens portfolio model:**
- **Lens 1 — Advancement Pipeline:** Clear gates projects must pass (ideation → pilot → production → scale)
- **Lens 2 — Whole-Portfolio Dashboard:** Balances across risk/return, time horizon, capability areas, and mission alignment

**The Bizzdesign framework for AI Portfolio Management:**
- Coordinated oversight of AI use cases, features, applications, models, and technologies
- Consistent way to understand: what AI you have, who owns it, where it may be used, whether it's aligned to strategy
- Bridges Enterprise Architecture and Strategic Portfolio Management

**Facilitator Notes:**
- This adds operational teeth to the Three-Horizon portfolio from last month's update
- If students' organisations have >10 AI initiatives running, they NEED portfolio governance
- Common question: "Who owns this?" → Usually nobody, which is the problem
- Time: 4 minutes

---

### [NEW AUG-2026] Slide 7: OpenAI's Enterprise Vision — The "Unified AI Operating Layer"

**Insert after:** Enterprise AI Transformation Data (Slide 13 from July update)  
**Source:** OpenAI, "The Next Phase of Enterprise AI," 6 August 2026; OpenAI, "Introducing Workspace Agents," 11 August 2026

**Content:**

**OpenAI's current enterprise position (August 2026):**
- Enterprise = >40% of OpenAI revenue (on track for parity with consumer by EOY 2026)
- APIs process 15 billion tokens per minute
- Codex: 3 million weekly active users (5× growth since Jan 2026)
- Revenue: $2B/month (4× faster growth than Alphabet/Meta at equivalent stage)

**The shift OpenAI observes in mature customers:**
> "People who are furthest ahead have gone from using AI for help on tasks, to managing teams of agents to do tasks for them." — Denise Dresser, OpenAI CRO, August 2026

**Key enterprise product releases (Aug 2026):**
- **OpenAI Frontier:** Unified platform for building, deploying, governing agents company-wide
- **Workspace Agents:** Agents that gather context from systems, follow team processes, ask for approval, keep work moving across tools
- **Stateful Runtime Environment** (with AWS): Agents keep context, remember prior work, operate across tools

**Case studies cited:**
- Global investment company: Agents across sales process → 90% more time for salespeople with customers
- Large energy producer: Agents increased output by 5% → >$1B additional revenue
- OpenAI internal: Codex usage = 85% of output tokens for average OpenAI worker; Legal, Finance, Recruiting all adopted by April 2026

**Roadmap implication:**
- The "unified operating layer" concept validates Gartner's "AI Agent Layer" thesis
- Organisations still running point solutions are falling behind
- Roadmaps should plan for platform consolidation by H2 2026/H1 2027

**Facilitator Notes:**
- Don't position this as an OpenAI sales pitch — use it as evidence of WHERE the market is heading
- The $1B revenue case study from the energy company is the kind of ROI data executives need
- The "managing teams of agents" framing is the best 1-line summary of the assistive→outcome shift
- Time: 5 minutes

---

### [NEW AUG-2026] Slide 8: Anthropic's Enterprise Agent Reality Check (June 2026)

**Insert after:** Slide 7 (OpenAI's Vision)  
**Source:** Anthropic, "The 2026 State of AI Agents Report" (500+ technical leaders); claude.com/blog, "How Enterprises Are Building AI Agents in 2026," 21 June 2026

**Content:**

**Where enterprises actually ARE (not where vendors say they should be):**

| Metric | Data |
|--------|------|
| Orgs deploying agents for multi-stage workflows | 57% |
| Running cross-functional processes across teams | 16% |
| Plan more complex use cases in 2026 | 81% |
| Developing multi-step process agents | 39% |
| Deploying cross-functional agents | 29% |
| Employees using AI at work (US) | 40% (up from 20% in 2023) |
| Orgs using AI for coding | ~90% |

**Featured implementation patterns (from Novo Nordisk, Doctolib, L'Oréal, Shopify):**
- Moving beyond single-step automation toward multi-stage workflows that span teams
- Achieving 80–90% resolution rates where agents handle complex workloads with limited human intervention
- Enabling employees to refocus on relationship building and strategic work

**Claude Managed Agents (launched 10 July 2026):**
- Suite of composable APIs for building and deploying cloud-hosted agents at scale
- Anthropic-managed harness + production infrastructure for state, memory, permissions, scheduled execution
- Promise: prototype to production in days, not months

**Key Anthropic insight for roadmapping:**
> "Will AI produce lasting advantages or incremental gains that plateau within a quarter?"
- The answer depends on whether organisations redesign work or merely accelerate existing tasks

**Facilitator Notes:**
- Use this as a counterpoint to OpenAI's vision — more grounded in current reality
- The 57% multi-stage / 16% cross-functional split shows where most enterprises ACTUALLY are
- The "lasting advantages vs plateau" question is a great discussion prompt
- Time: 4 minutes

---

### [NEW AUG-2026] Slide 9: AWS's Agentic AI Operating Model

**Insert after:** Agentic Roadmap (Slide 8 from July update)  
**Source:** AWS Prescriptive Guidance, "Operationalizing Agentic AI on AWS," 2026; AWS Blog, "From Lagging to Leading," 15 July 2026

**Content:**

**AWS's core thesis:**
> "Agentic AI is not a feature — it's a new operational paradigm. Organisations that invest in disciplined architecture, trust frameworks, and business-aligned deployment models will lead the next generation of adaptive, intelligent enterprises." — AWS Prescriptive Guidance, 2026

**What "operationalising" requires (per AWS):**
- Lifecycle management for agents (not just models)
- Trust enforcement at machine speed
- Interoperability across agent systems
- Alignment to business models (not just technology decisions)

**The business preparation layer (often skipped):**
> "Operationalizing agentic AI requires more than deploying intelligent agents. It demands a fundamental transformation in how the business organizes teams, designs processes, and governs technology." — AWS

**Key AWS services for the agentic stack (2026):**
- **Amazon Bedrock Guardrails** — new API targeting agentic AI workflows (June 2026)
- **Amazon Bedrock AgentCore** — serverless AI agent infrastructure
- **OpenAI models on Bedrock** — GA since June 2026 (model choice flexibility)
- **Stateful Runtime Environment** — (with OpenAI) for context-persistent agents
- **AWS CAF for AI/ML/GenAI** — updated cloud adoption framework

**Relevance to this module:**
- AWS positions operationalisation as architecture + culture + governance — mirrors BCG 10-20-70
- Their prescriptive guidance provides implementation patterns for each phase of the agentic roadmap
- Free, publicly available documentation students can reference

**Facilitator Notes:**
- Position as "implementation guidance" not "product pitch" — the principles are cloud-agnostic
- The AWS CAF for AI is a free download that gives students a structured assessment tool
- For students on AWS: the Bedrock Guardrails + AgentCore combination addresses governance gaps directly
- Time: 4 minutes

---

### [NEW AUG-2026] Slide 10: Proportional Governance — Why Binary Controls Fail

**Insert after:** OWASP Framework (Slide 2 in this addendum)  
**Source:** Gartner, "Applying Uniform Governance Across AI Agents Will Lead to Enterprise AI Agent Failure," 26 May 2026

**Content:**

**The Gartner warning:**
> "Enterprises are treating AI agent governance as binary — either locked down or fully trusted — and that is the root cause of failure." — Shiva Varma, Gartner, May 2026

**The prediction:**
- By 2027, 40% of enterprises will demote or decommission autonomous AI agents due to governance gaps identified only AFTER production incidents

**The two failure modes of binary governance:**

| Mode | Problem | Result |
|------|---------|--------|
| Over-restriction | Same controls on simple agents as complex ones | Slows delivery → drives shadow development |
| Under-restriction | High-autonomy agents with insufficient oversight | Operational, security, and compliance risk |

**Gartner's proportional governance model:**
- Classify AI agents across distinct autonomy levels
- Each level = different trust boundary + corresponding governance requirements
- Low-autonomy agents (e.g., summarisation assistants) → lighter controls
- High-autonomy agents (e.g., code-executing, multi-system) → full governance stack

**How to integrate into your roadmap:**
1. Add "governance tier assessment" to every agent initiative
2. Define 3–4 autonomy tiers with escalating requirements
3. Build a governance registry that tracks tier + controls per agent
4. Review and adjust tiers quarterly as agents evolve

**Facilitator Notes:**
- This resolves the tension students feel: "If we govern everything, nothing moves. If we govern nothing, it's chaos."
- The proportional model says: "Govern PROPORTIONALLY to autonomy"
- Connects directly to OWASP's AT0–AT5 deployment tiers
- Time: 4 minutes

---

### [NEW AUG-2026] Slide 11: Digital Applied's H1 2026 Deployment Retrospective

**Insert after:** Enterprise AI Transformation Data (Slide 13 from July update)  
**Source:** Digital Applied, "Agentic AI H1 2026 Retrospective: 100 Deployments Analyzed," May 2026

**Content:**

**What 100 real-world agentic deployments reveal (Jan–April 2026):**

**Patterns that emerged:**
- **Orchestrators are dominant** — multi-agent coordination is the norm, not the exception
- **Eval-first is rising** — teams that build evaluation frameworks before deploying outperform
- **Governance is maturing** — no longer optional; now a deployment prerequisite
- **Observability is table stakes** — if you can't see what agents are doing, you can't run them in production

**Key statistics (Digital Applied, April 2026):**
- Only 41% of agent rollouts achieve positive ROI within 12 months
- 19% never reach payback
- Primary causes of failure: evaluation drift, governance gaps, unmeasured rework (NOT agent capability)

**What this means for roadmaps:**
- Build evaluation infrastructure BEFORE deploying agents (not after)
- Include observability in your platform layer budget
- Expect 12-month payback cycles (not 30-day magic)
- The 41% success rate means portfolio thinking is essential — not every bet will pay off

**Facilitator Notes:**
- The 41% ROI figure is sobering — balances the optimistic vendor narratives
- "Eval-first" is a concrete practice students can implement immediately
- The failure causes (drift, governance, rework) are all PROCESS issues, not technology issues — reinforces 10-20-70
- Time: 4 minutes

---

### [NEW AUG-2026] Slide 12: The Stanford Enterprise AI Playbook — "It's Never the Model"

**Insert after:** Pilot Purgatory (Slide 1 from July update)  
**Source:** Stanford Digital Economy Lab, "The Enterprise AI Playbook: Lessons from 51 Successful Developments," April 2026

**Content:**

**The headline finding:**
> "Across 51 enterprise cases over 5 months, we found stories of transformation measured in weeks and others measured in years. Same technology, same use cases, vastly different outcomes. The difference was NEVER the AI model. It was always the organisation." — Stanford Digital Economy Lab, 2026

**What separated fast transformers from slow ones:**
- Not model choice (GPT vs Claude vs Gemini)
- Not budget size
- Not industry sector
- **It was:** Organisational readiness, process design, executive sponsorship, and change management

**Implications for roadmapping:**
- Stop debating which model to use — start debating how to change the organisation
- The model selection decision (often the first thing teams fixate on) is the LEAST important variable
- Your roadmap's success depends on the 70% (people & process), full stop

**How this connects to our framework:**
- Stanford validates BCG 10-20-70
- Stanford validates ActivTrak's 2% problem (tools ≠ transformation)
- Stanford validates Gartner's Extend focus (organisation change, not individual productivity)

**Facilitator Notes:**
- Quote "It was never the model. It was always the organisation" — write it on the whiteboard
- This is liberating for students who feel behind on model selection: "You haven't missed anything important"
- Challenge: "If the model doesn't matter, what does your roadmap need to focus on?"
- Time: 4 minutes

---

### [NEW AUG-2026] Slide 13: The Kognitos 5% — What Scaled Enterprises Do Differently

**Insert after:** Stanford Playbook (Slide 12 in this addendum)  
**Source:** Kognitos, "Enterprise AI Adoption Strategy for Scale," June 2026

**Content:**

**The gap:**
- 85% of enterprises have deployed AI in at least one business function
- Only 23% have scaled it across the enterprise
- Only 5% have achieved full AI-native operations

**The six-pillar strategy architecture (Kognitos, 2026):**
The 5% who succeed don't just have AI tools — they have:
1. **Strategic architecture** — AI embedded in corporate strategy, not siloed
2. **Platform thinking** — Shared capabilities, not replicated per-team
3. **Governance fabric** — Proportional, continuous, not binary
4. **Enablement engine** — Ongoing training + champions + measurement
5. **Portfolio discipline** — Three-horizon allocation + gates + rebalancing
6. **Transformation mindset** — Redesign work, don't just layer AI on it

**Notice:** Every pillar maps to content already in this module:
- Pillar 1 → Agentic Roadmap (July Slide 8)
- Pillar 2 → AI CoE (July Slide 15)
- Pillar 3 → OWASP + Proportional Governance (this update)
- Pillar 4 → ActivTrak 2% insight (this update)
- Pillar 5 → Three-Horizon + Gartner Funnel (July Slides 6–7)
- Pillar 6 → Process Redesign (July Slide 10)

**Facilitator Notes:**
- This slide is a synthesis/capstone — use it to show how ALL the module content connects
- The 85% → 23% → 5% funnel creates urgency: "Which group do you want to be in?"
- Can be used as a wrap-up or preview slide at module start
- Time: 3 minutes

---

### [NEW AUG-2026] Slide 14: Atlassian's Four-Stage AI ROI Framework

**Insert after:** AI ROI Measurement (Slide 11 from July update)  
**Source:** Atlassian, "Stop Guessing at AI ROI: A Four-Stage Framework for Real Results," June 2026

**Content:**

**The problem:**
> "When asked for hard ROI figures, leaders scramble to gather time-saved estimates and productivity anecdotes — which only capture a narrow slice of the story." — Atlassian, June 2026

**Atlassian's Four-Stage ROI Framework:**

| Stage | Focus | Metric Type | Example |
|-------|-------|-------------|---------|
| 1 — Exploring | Adoption | Activity metrics | # users activated, frequency of use |
| 2 — Expanding | Efficiency | Time/cost savings | Hours saved, throughput increase |
| 3 — Embedding | Effectiveness | Quality/outcome improvement | Error rates, decision quality, NPS |
| 4 — Transforming | Value creation | Strategic impact | New revenue streams, market position, capabilities |

**Key additions vs. our existing Tier 1/2/3 model:**
- Adds a 4th stage (Transforming) that captures STRATEGIC value — not just financial
- Includes quality/effectiveness metrics at Stage 3 (not just time saved)
- Explicitly maps to organisational maturity, not just project lifecycle

**The "hidden labour" of AI (HBR, August 2026):**
- AI can automate hours of work per week BUT requires substantial human oversight
- Leaders need to account for "botsitting" labour in ROI calculations
- True ROI = (gains from AI) - (investment) - (oversight labour)

**Facilitator Notes:**
- This extends the Tier 1/2/3 model from last month with a maturity lens
- The "botsitting" concept from HBR is a crowd-favourite — AI creates new work while saving old work
- Ask: "Are you measuring Stage 1 or Stage 3 metrics? Most organisations never get past Stage 2."
- Time: 4 minutes

---

### [NEW AUG-2026] Slide 15: Updated 2026 Predictions Dashboard

**Insert after:** Microsoft's AI Multiplier Effect (Slide 18 from July update)  
**Source:** Multiple (compiled August 2026)

**Content:**

**Key predictions consolidated for roadmap planning (as of August 2026):**

| Prediction | Source | Timeline |
|-----------|--------|----------|
| 150,000+ agents per Fortune 500 enterprise | Gartner | By 2028 |
| 40% of enterprise apps embed task-specific agents | Gartner | End of 2026 |
| 45% of CIOs lead AI agent systems outside IT | Gartner | By 2028 |
| >50% of enterprises abandon assistive AI for outcome platforms | Gartner | By 2028 |
| 40% of enterprises demote/decommission agents (governance gaps) | Gartner | By 2027 |
| AI agents outnumber sellers 10:1 | Gartner | By 2028 |
| Only 2% of workers at "transforming" stage | ActivTrak | H1 2026 (actual) |
| 57% deploy agents for multi-stage workflows | Anthropic | H1 2026 (actual) |
| 81% plan more complex agent use cases | Anthropic | 2026 planned |
| Enterprise AI market: $347 billion | Industry estimate | 2026 |
| OpenAI enterprise revenue: parity with consumer | OpenAI | End of 2026 |

**Use these predictions to:**
- Build urgency in business cases (the market is moving FAST)
- Set realistic expectations (2% transforming, 41% ROI in year one)
- Plan governance investment (most enterprises underprepared)
- Sequence your roadmap (assistive → outcome → autonomous)

**Facilitator Notes:**
- This is a reference slide — don't teach it; use it to support arguments throughout the module
- Update these numbers quarterly (they WILL change)
- The mix of optimistic vendor predictions + sobering reality data (2%, 41%) keeps credibility
- Time: 2 minutes (reference only)

---

## C) UPDATED CASE STUDIES

### Case Study 1: ActivTrak's 120,000-Worker AI Adoption Study (July 2026)
**Source:** ActivTrak Productivity Lab, multiple publications July 2026

**What happened:** ActivTrak analysed 443 million hours of work data across 120,620 workers to measure actual AI adoption behaviour (not self-reported surveys).

**Key findings:**
- 95% of companies adopted AI; average org uses 7 AI tools
- Only 2% reached "transforming" stage
- AI users gained a persistent 17-minute/day productivity advantage
- 82% maintained their maturity level quarter-over-quarter (sticky habits)
- In one case study: 95% had AI activated, but 30% barely used it

**Module relevance:** Validates the 70% investment in people/process. Demonstrates that tool deployment ≠ organisational transformation. Provides hard evidence for enablement budgets.

---

### Case Study 2: OpenAI Internal Adoption (August 2026)
**Source:** OpenAI, "How Agents Are Transforming Work," 11 August 2026

**What happened:** OpenAI ate its own dogfood — Engineering adopted Codex first, then Legal, Finance, and Recruiting crossed the threshold by April 2026.

**Key findings:**
- Codex now accounts for >85% of output tokens for the average OpenAI employee
- Shifted from "AI helps with tasks" to "managing teams of agents doing tasks"
- Non-engineering departments (Legal, Finance, HR) adopted in Q1–Q2 2026

**Module relevance:** Demonstrates the "assistive → outcome" shift in practice. Shows that non-technical functions can adopt AI agents. Provides a timeline for cross-functional adoption (6–12 months from engineering to company-wide).

---

### Case Study 3: OpenAI Frontier — Enterprise Results (August 2026)
**Source:** OpenAI, "Introducing OpenAI Frontier," 11 August 2026

**Key findings:**
- Global investment company: Agents across sales → 90%+ more time for customer-facing work
- Large energy producer: Agents → 5% output increase → >$1B additional revenue
- Oracle, State Farm, Uber deploying agents company-wide via Frontier platform

**Module relevance:** Provides specific, large-scale ROI examples for business case development. Demonstrates the "unified operating layer" concept in practice.

---

### Case Study 4: Pixieset — 35% AI Feature Adoption with Amazon Bedrock (August 2026)
**Source:** AWS Machine Learning Blog, 11 August 2026

**What happened:** Photography platform Pixieset achieved 35% AI feature adoption by focusing on solving the right problem (not just deploying AI broadly).

**Module relevance:** Demonstrates that adoption success comes from problem-market fit, not technology sophistication. Supports the "simpler alternative test" principle.

---

## D) UPDATED TOOLS & RESOURCES

### New Frameworks & Guidance (June–August 2026)

| Resource | Source | Type | URL |
|----------|--------|------|-----|
| OWASP Agentic AI Security Maturity Framework | OWASP GenAI Security Project | Governance framework | owasp.org/www-project-ai-maturity-assessment/ |
| Operationalizing Agentic AI on AWS | AWS Prescriptive Guidance | Architecture guide | docs.aws.amazon.com/prescriptive-guidance/latest/strategy-operationalizing-agentic-ai/ |
| Foundations of Agentic AI on AWS | AWS Prescriptive Guidance | Architecture patterns | docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-foundations/ |
| Agentic AI Patterns & Workflows on AWS | AWS Prescriptive Guidance | Implementation patterns | docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-patterns/ |
| AWS CAF for AI/ML/GenAI (updated 2026) | AWS Whitepapers | Adoption framework | docs.aws.amazon.com/whitepapers/latest/aws-caf-for-ai/ |
| AI Portfolio Management Guide | Bizzdesign | EA/SPM framework | bizzdesign.com/guides/ai-portfolio-management |
| ActivTrak AI Adoption Maturity Data H1 2026 | ActivTrak | Behavioural research | activtrak.com/blog/ai-adoption-maturity-data/ |
| Atlassian 4-Stage AI ROI Framework | Atlassian | Measurement guide | atlassian.com/blog/strategy/enterprise-ai-roi-framework |
| Gartner 6-Step Agent Governance | Gartner | Governance checklist | gartner.com/en/newsroom (28 April 2026) |

### New Reports

| Report | Source | Date |
|--------|--------|------|
| The 2026 State of AI Agents Report | Anthropic | June 2026 |
| The Enterprise AI Playbook: 51 Successful Developments | Stanford Digital Economy Lab | April 2026 |
| Agentic AI H1 2026 Retrospective: 100 Deployments | Digital Applied | May 2026 |
| Hype Cycle for Agentic AI 2026 | Gartner | April 2026 |
| Hype Cycle for Agentic Automation 2026 | Gartner | July 2026 |
| Hype Cycle for Employee Adoption of AI Agents 2026 | Gartner | July 2026 |
| State of Agentic AI Security & Governance | OWASP | June 2026 |
| The Next Phase of Enterprise AI | OpenAI | August 2026 |
| AI Doesn't Reduce Work — It Intensifies It | HBR | February 2026 |
| The "Last Mile" Problem Slowing AI Transformation | HBR | March 2026 |
| Manage Your AI Investments Like a Portfolio | HBR | January 2026 |

### Product Launches Relevant to Module 05

| Product | Vendor | Date | Relevance |
|---------|--------|------|-----------|
| Claude Managed Agents | Anthropic | 10 July 2026 | Production agent deployment platform |
| OpenAI Workspace Agents | OpenAI | 11 August 2026 | Team-level agent orchestration |
| OpenAI Frontier | OpenAI | 11 August 2026 | Enterprise agent governance platform |
| Amazon Bedrock Guardrails (Agentic API) | AWS | June 2026 | Agent workflow governance |
| Amazon Bedrock AgentCore | AWS | 2026 | Serverless agent infrastructure |
| OpenAI models on Bedrock (GA) | AWS + OpenAI | 1 June 2026 | Model flexibility for enterprise |
| GPT-5.6 (80% price reduction) | OpenAI | 30 July 2026 | Cost barrier reduction for agents |
| Bizzdesign Unify | Bizzdesign | April 2026 | AI-native portfolio management |

---

## E) FARIS HADDAD CONTENT INTEGRATION

**Search results:** Direct searches for published content by Faris Haddad (LinkedIn articles, Medium posts, blog posts) related to AI/agentic topics did not return specific published articles in the June–August 2026 timeframe.

**Note:** One result from ELVTR (uk.elvtr.com) confirms Faris Haddad's role as instructor for an "AI Solutions Architecture Course" — this is likely the course itself.

**Recommendation for in-class references:**
- If Faris has published LinkedIn posts or internal Amazon content on AI roadmapping, agentic transformation, or enterprise AI strategy during this period, reference them as:
  - "As I've been writing about recently..."
  - "In my LinkedIn post on [topic], I shared..."
  - "From my work with enterprise clients on this exact challenge..."
- The facilitator should check their own LinkedIn activity from July–August 2026 for relevant posts to integrate
- Consider publishing a short LinkedIn piece on the "2% problem" or "Agent Sprawl" as class prep — it creates a citable reference

**Potential integration points:**
- If there's content on the agentic roadmap challenges → reference in Slide 8 (Agentic Roadmap)
- If there's content on enterprise AI maturity → reference in the Maturity Models section
- If there's content on AI Centre of Excellence → reference in Slide 15 (CoE)
- Any ELVTR course-adjacent LinkedIn content can be referenced as "As we explore in the broader curriculum..."

---

## F) FACILITATOR REFRESH BRIEF

### Top 3 Things That Changed Since July 2026

1. **Agent Sprawl is now THE governance conversation** (Gartner 150K prediction + OWASP framework + proportional governance). July's update introduced agent governance conceptually; August has concrete frameworks (OWASP's 2-axis model, Gartner's 6-step framework, proportional governance). Add these to the governance section immediately.

2. **Hard evidence that AI deployment ≠ transformation** (ActivTrak 2% study + Atlassian efficiency paradox + Stanford "It was never the model"). July's update made the 70% people/process argument; August now has data from 120,000 workers proving it. This is the proof students need to get budget for enablement programmes.

3. **The assistive→outcome shift is accelerating** (Gartner abandoning copilots prediction + OpenAI Workspace Agents + Anthropic Managed Agents). The Defend/Extend/Upend model from July is now validated by market moves. Enterprises are shifting spending from individual productivity to workflow outcomes.

### What to Emphasise as "Breaking News"

- **OWASP Agentic AI Security Maturity Framework** (released today's date context, June 2026) — "Hot off the press" — students can use it in their next governance conversation
- **ActivTrak 2% finding** — "The most sobering statistic in AI adoption right now"
- **Gartner: 40% will decommission agents by 2027** — "Your governance investment isn't nice-to-have; it's a decommission avoidance strategy"
- **OpenAI × AWS partnership** (Stateful Runtime, OpenAI on Bedrock GA) — "The platform wars are consolidating around interoperability, not lock-in"

### Demos & Tools to Set Up Fresh

1. **OWASP AI Maturity Assessment page** — Have open in browser for live classification exercise
   - URL: owasp.org/www-project-ai-maturity-assessment/
   - Activity: Have students classify their top 3 agents on the AT0–AT5 axis

2. **AWS "Operationalizing Agentic AI" guide** — Keep PDF loaded for architecture reference
   - URL: docs.aws.amazon.com/prescriptive-guidance/latest/strategy-operationalizing-agentic-ai/

3. **ActivTrak 4-stage model diagram** — Screenshot for projection
   - URL: activtrak.com/blog/ai-adoption-maturity-model/

4. **Gartner 6-step agent governance summary** — Print as handout
   - Source: Gartner press release, 28 April 2026

5. **Updated Agentic Readiness Self-Assessment** — Add a "governance tier" row to the existing assessment from July Slide 17, incorporating the proportional governance concept

6. **Live exercise (NEW):** "Agent Inventory Audit"
   - Have students list every AI tool/agent they or their team use
   - Classify each on OWASP's AT0–AT5 scale
   - Check governance maturity level for each
   - Identify "red cells" (deployment > governance)
   - Time: 8 minutes (replace or supplement existing activity)

### Suggested Slide Integration Order (for 60-min version)

From this August addendum, add to the Standard 60-minute version:
1. **Slide 3** (2% Problem) → After BCG 10-20-70 opening section (~5 min)
2. **Slide 12** (Stanford "Never the Model") → After Pilot Purgatory (~4 min)
3. **Slide 1** (Agent Sprawl) + **Slide 10** (Proportional Governance) → In governance section (~9 min)
4. **Slide 5** (Assistive → Outcome) → After Defend/Extend/Upend (~5 min)

Total additional time: ~23 min → Requires trimming or extending to 75-minute version

For 75-minute version, add all the above plus:
5. **Slide 4** (Efficiency Paradox) → After Process Redesign
6. **Slide 7 or 8** (OpenAI or Anthropic data) → In Case Studies
7. **Slide 14** (Atlassian ROI Framework) → After ROI section

---

*Module 05 August 2026 Refresh completed — 12 August 2026*
