# Module 05: Building Your AI Roadmap — 2026 Update

## Gap Analysis

Based on web research into AI roadmapping, maturity models, portfolio frameworks, and enterprise transformation patterns in 2025–2026, the following gaps exist in the original module:

1. **Agentic AI roadmapping is now a distinct discipline** — The original module treats AI roadmapping generically. In 2026, organisations need a dedicated "agentic roadmap" layer that accounts for agent-compatible architectures, orchestration frameworks, and the silicon-based workforce concept (Deloitte Tech Trends 2026).

2. **The "pilot purgatory" problem is now quantified** — IDC reports 88% of AI POCs fail to reach production; 42% of enterprises abandoned GenAI initiatives in 2025 (up from 17% the year prior). The module should address root causes and escape patterns.

3. **New maturity models have emerged** — CMU SEI + Accenture released the AI Adoption Maturity Model (June 2026); n8n published a 5-level framework assessed across 4 dimensions; Sphere Inc. released an Agentic AI Maturity Map with 5 levels. The original module's maturity discussion needs updating.

4. **Portfolio thinking has replaced single-project planning** — The 60/30/10 Three-Horizon AI Portfolio framework (Iternal Technologies) and Gartner's 7-step AI Project Prioritisation Funnel are now industry standard. The original module's "quick wins vs transformational bets" framing is insufficient.

5. **The BCG 10-20-70 rule is now widely cited** — 10% algorithms, 20% technology, 70% people and process. First agentic clients see 3× productivity improvement, 80% reduction in cycle time. The module doesn't emphasise organisational change sufficiently.

6. **AI ROI measurement has matured** — Multi-dimensional frameworks (financial, operational, capability) with tiered KPIs are now standard. The original "metrics that matter" section needs concrete frameworks.

7. **"Agent washing" is a new risk** — Deloitte warns of vendors rebranding existing automation as "agentic" and of "workslop" where poorly-designed agents add work to a process. Roadmaps must include evaluation criteria to avoid this.

8. **The Gartner Defend/Extend/Upend categorisation** — A new strategic-intent taxonomy for AI projects that determines which deliver near-term financial ROI (only "Extend" projects).

9. **Six readiness dimensions for agentic AI** — Strategic alignment, technical infrastructure, data readiness, process maturity, governance/risk management, workforce readiness. More specific than the original value/feasibility/readiness axes.

10. **Process redesign before automation** — Deloitte's key finding: true value comes from redesigning operations, not layering agents onto old workflows. Henry Ford analogy: "finding better ways of doing things that should not have to be done at all."

---

## New Slides — [NEW 2026]

---

### [NEW 2026] Slide 1: The Pilot Purgatory Problem — Why AI Roadmaps Fail

**Insert after:** Module Overview / Course Philosophy slide  
**Format:** Concept explanation with data points

**Content:**

**The brutal statistics (2025–2026):**
- 88% of AI proofs-of-concept fail to reach production (IDC)
- 42% of companies abandoned GenAI initiatives in 2025 — up from 17% the year prior
- Only 14% of agentic AI solutions are deployment-ready; just 11% are in production (Deloitte 2025)
- 95% of generative AI pilots fail to deliver immediate financial returns (MIT 2025)

**Root causes:**
- Treating AI as a technology project rather than an organisational change programme
- No portfolio logic — evaluating each pilot in isolation
- Missing infrastructure between experiment and production (orchestration, governance, integration)
- Selecting projects based on excitement rather than feasibility

**The escape pattern:**
> "Organisations that treat AI as a technology project consistently underperform. The BCG 10-20-70 rule: 10% technology, 20% data and analytics, 70% people and process. Organisations that follow this outperform those that don't by 3×." — ssntpl.com

**Facilitator Notes:**
- Open with: "Before we build a roadmap, let's understand why most roadmaps fail. This is the problem we're solving today."
- Common student question: "Is our company one of the 88%?" — Ask them to reflect honestly.
- Emphasise that the 10-20-70 split is counter-intuitive for technical audiences: most investment goes to people and process, not algorithms.
- Time: 5 minutes
- Suitable for all levels

---

### [NEW 2026] Slide 2: The BCG 10-20-70 Rule — AI is an Organisational Problem

**Insert after:** Slide 1 (Pilot Purgatory)  
**Format:** Concept with visual breakdown

**Content:**

```
┌──────────────────────────────────────────────┐
│            BCG 10-20-70 Rule                 │
├──────────────────────────────────────────────┤
│  10%  │  Algorithms & Models                 │
│       │  (picking the right model/technique) │
├───────┼──────────────────────────────────────┤
│  20%  │  Technology & Data Infrastructure    │
│       │  (pipelines, compute, integration)   │
├───────┼──────────────────────────────────────┤
│  70%  │  People, Process & Change Mgmt       │
│       │  (workflows, training, governance,   │
│       │   organisational design, culture)    │
└───────┴──────────────────────────────────────┘
```

**Why this matters for roadmapping:**
- A roadmap that only covers technology choices will address 30% of the success factors
- The 70% requires: executive sponsorship, change champions, workflow redesign, governance bodies, success metrics, communication plans
- BCG's agentic clients see 3× productivity improvement — but only when teams redesign how work is done, not just layer AI onto existing processes

**Key quote (Deloitte Tech Trends 2026):**
> "True value comes from redesigning operations, not just layering agents onto old workflows."

**Facilitator Notes:**
- This is the single most important slide in the module for senior leaders. Pause and let it sink in.
- Ask: "What percentage of your current AI budget is going to the 70%?"
- For engineers: this may feel soft — acknowledge it, then show them how many technical projects die because of the 70%, not the 30%.
- Time: 5 minutes

---

### [NEW 2026] Slide 3: Updated AI Maturity Models — 2026 Landscape

**Insert after:** AI Maturity Models section  
**Format:** Comparison table

**Content:**

| Model | Source | Levels | Key Innovation |
|-------|--------|--------|----------------|
| **AI Adoption Maturity Model** | CMU SEI + Accenture (June 2026) | Structured assessment | Field-tested; assessment-based roadmap creation; applies to both commercial and government |
| **5-Level AI Maturity Framework** | n8n (June 2026) | 0–4: Awareness → Autonomous | Assessed across 4 dimensions: Usage, Sophistication, Governance, Infrastructure |
| **Agentic AI Maturity Map** | Sphere Inc. (2026) | 5 levels | Chatbots → Tool-Enabled → Workflow → Orchestrated → Autonomous Operations |
| **Gyde Enterprise Model** | Gyde.ai (2026) | Exploratory → Functional → Strategic → Transformational | Highlights the "jump from pilots to production" as the stall point |
| **Digital Applied Model** | DigitalApplied (2026) | Exploration → Experimentation → Integration → Orchestration → Autonomous | Explicit "Orchestration" stage before autonomy |

**Which model to use:**
- **CMU SEI + Accenture**: Best for formal enterprise assessments, especially regulated industries
- **n8n 5-Level**: Best for practical self-assessment and benchmarking
- **Agentic AI Maturity Map**: Best when your roadmap focuses specifically on agentic capabilities

**Facilitator Notes:**
- Show the progression: every model now includes an "agentic" or "orchestration" stage — this wasn't present in 2024 models
- Student question: "Which one should we use?" → It depends on your organisation's context. CMU SEI for formal assessments, n8n for quick internal alignment.
- ADVANCED: Discuss how the n8n model identifies two "chasms" — Level 0→1 (policy challenge) and Level 2→3 (organisational challenge)
- Time: 7 minutes

---

### [NEW 2026] Slide 4: The n8n 5-Level Framework Deep Dive

**Insert after:** Slide 3 (Maturity Models Landscape)  
**Format:** Concept with progressive detail

**Content:**

**Level 0: Awareness ("Shadow AI")**
- Employees using personal AI accounts with no organisational visibility
- "Most dangerous stage" — organisation bears all risks, captures no strategic benefits
- Key action: Audit what tools employees are already using

**Level 1: Experimental (Sanctioned Pilots)**
- Isolated teams experimenting with AI
- The "pilot purgatory" danger zone
- 88% of POCs stall here (IDC)
- Key action: Enterprise-tier tooling + baseline governance

**Level 2: Operational (Integration)**
- AI deployed across multiple business functions with measurable ROI
- Agentic workflows first appear here (human-in-the-loop)
- Key challenge: Legacy system integration, orchestration layer needed
- Data point: JPMorgan Chase deployed LLM Suite across 200,000 daily users, 450+ use cases

**Level 3: Enterprise-Wide (The Hardest Transition)**
- AI operates across departmental boundaries
- Only 5% of companies reach this (BCG: "future-built")
- Requires: organisation-wide governance, scalable platforms, leadership-driven strategy

**Level 4: Autonomous Operations**
- AI systems self-monitor, self-improve, self-coordinate
- Human oversight shifts from operational to strategic
- The frontier — almost no enterprise is here yet

**The Two Critical Transitions:**
1. L0→L1: **Leadership & policy challenge** (change management, not technology)
2. L2→L3: **Organisational design challenge** (cross-departmental coordination)

**Facilitator Notes:**
- Ask students: "Where is your organisation on this ladder?" — This creates instant engagement
- Key insight for students: the transitions between levels are harder than operating at a level
- For beginners: focus on L0–L2; for advanced: discuss L3–L4 in depth
- Time: 7 minutes

---

### [NEW 2026] Slide 5: The SEI-Accenture AI Adoption Maturity Model

**Insert after:** Slide 4 (n8n Framework)  
**Format:** Case study / framework reference  
**⚡ ADVANCED**

**Content:**

**Released:** June 2026 by Carnegie Mellon University's Software Engineering Institute in partnership with Accenture

**What it is:**
- A field-tested, structured assessment instrument for measuring an organisation's AI adoption capability
- Modelled after CMM/CMMI — assessing the degree to which key practices are implemented and governed
- Applies to both commercial enterprises and government organisations

**Key differentiator from other models:**
- Assessment-based: produces a scored result, not just a self-identified level
- Practice-focused: measures "ability to perform and sustain specific technical practices"
- Roadmap-generating: the assessment output is a gap analysis that directly produces an actionable roadmap
- Tested in complex environments (defence, healthcare, financial services)

**How to use it in roadmapping:**
1. Run the assessment across your AI programme
2. Identify gaps between current capability and target state
3. Use the gap analysis to sequence your roadmap priorities
4. Reassess quarterly to track progress

**Facilitator Notes:**
- This is the most rigorous model available — position it as the "gold standard" for enterprises that need formal justification (board-level reporting, regulatory requirements)
- Common student question: "Is it free?" → Yes, downloadable from SEI Digital Library
- Skip for beginners unless they work in defence/regulated sectors
- Time: 4 minutes

---

### [NEW 2026] Slide 6: The Three-Horizon AI Portfolio (60/30/10)

**Insert after:** Quick Wins vs Transformational Bets section  
**Format:** Framework with allocation logic

**Content:**

**Single-project AI thinking creates pilot purgatory. Portfolio thinking is the antidote.**

| Horizon | Allocation | What it includes | Timeline | Example |
|---------|-----------|------------------|----------|---------|
| **H1: Quick Wins** | 60–70% | Proven tech, immediate productivity | 30–60 days to ROI | Chat assistants, summarisation, meeting intelligence |
| **H2: Advanced** | 20–30% | Established AI + customisation | 3–6 months | RAG systems, workflow automation, bounded agentic AI |
| **H3: Experimental** | 10–20% | Emerging tech, high optionality | 6–18 months | Full agentic workflows, multimodal, domain-specific models |

**Portfolio mechanics:**
- H1 success builds AI literacy, credibility, and funding for H2/H3
- Items migrate from H3 → H2 → H1 as technologies mature
- Rebalance quarterly — not weekly, not annually
- Gartner projects 33% of enterprise software will include agentic AI by 2028 — today's H3 becomes tomorrow's H1

**Two failure modes the portfolio prevents:**
1. **All H1, no H3:** Delivers quick wins but falls permanently behind as technology evolves
2. **All H3, no H1:** Innovation theatre with no ROI — eventually loses budget and executive confidence

**Facilitator Notes:**
- This replaces the simpler "quick wins vs transformational bets" framing from the original module
- Draw the three horizons on a whiteboard — the visual sticks
- Ask: "Where is your organisation over-indexing? All H1 or all H3?"
- Key insight: H1 *funds* H2 and H3 — you can't skip it
- Time: 7 minutes

---

### [NEW 2026] Slide 7: Gartner's 7-Step AI Project Prioritisation Funnel

**Insert after:** Slide 6 (Three-Horizon Portfolio)  
**Format:** Process framework

**Content:**

**Problem:** "If you're staring down a spreadsheet of 150+ AI ideas…" — Gartner

**The funnel progressively narrows to 3–5 high-impact projects:**

```
Step 1: Categorise by strategic intent (Defend / Extend / Upend)
  → Keep only "Extend" — sole reliable path to near-term financial ROI
  ↓
Step 2: Anchor each to a preexisting business outcome/metric
  → No clear link to financial impact? Strike it.
  ↓
Step 3: Establish a baseline (historical data must exist)
  → No baseline = no way to demonstrate ROI. Strike it.
  ↓
Step 4: Assess deployment ease & data readiness
  → High execution burden? Not near-term. Strike it.
  ↓
Step 5: Align to primary financial goal (cost reduction OR revenue growth)
  → Doesn't align? Strike it.
  ↓
Step 6: Identify teams with highest productivity impact
  → Finance, anti-fraud, HR, software engineering, data & analytics
  ↓
Step 7: Zero in on easiest benefit to harvest
  → Fewest organisational changes needed to convert AI output to $ value
```

**Key Gartner insight — the Defend/Extend/Upend taxonomy:**
- **Defend**: Boosts individual productivity — rarely yields positive financial ROI
- **Extend**: Transforms existing divisions for competitive differentiation — best near-term bet
- **Upend**: Disrupts markets — low odds of success, long timelines

**Facilitator Notes:**
- This is immediately actionable — students can apply it to their backlog the next day
- Common pushback: "But our CEO wants us to Upend!" → Acknowledge, but show that Extend funds Upend
- Practical exercise: have students apply Steps 1–3 to their top 5 candidate use cases right now
- Time: 6 minutes

---

### [NEW 2026] Slide 8: The Agentic Roadmap — A New Layer

**Insert after:** Slide 7 (Gartner Funnel)  
**Format:** Concept with phased approach

**Content:**

**Why agentic roadmaps are different from generic AI roadmaps:**
- Agents require agent-compatible architectures (microservices, APIs, event-driven)
- Agents require new governance frameworks (managing a "silicon-based workforce")
- Agents create new risk categories (autonomous decisions, cascading failures)
- Legacy systems weren't designed for real-time agent interaction

**Deloitte findings (2025):**
- 30% of organisations exploring agentic options
- 38% piloting solutions
- Only 14% deployment-ready
- 42% still developing their agentic strategy; 35% have no formal strategy at all

**The phased agentic roadmap (synthesised from Deloitte, Sutherland, Arion Research):**

| Phase | Focus | Duration | Outcome |
|-------|-------|----------|---------|
| **1. Foundation** | Infrastructure modernisation, API readiness, data architecture | Months 1–3 | Agent-compatible systems |
| **2. Bounded Agents** | Single-task agents with HITL, narrow scope, measured outcomes | Months 3–6 | Validated agent patterns |
| **3. Workflow Agents** | Multi-step agents spanning tools/data sources | Months 6–12 | Production agentic workflows |
| **4. Orchestrated** | Multi-agent coordination, cross-department automation | Months 12–18 | Enterprise-scale orchestration |
| **5. Autonomous** | Self-monitoring, self-improving agent ecosystems | Month 18+ | Strategic human oversight only |

**Six readiness dimensions to assess at each phase:**
1. Strategic alignment
2. Technical infrastructure
3. Data readiness
4. Process maturity
5. Governance & risk management
6. Workforce readiness

**Facilitator Notes:**
- This is the single most timely slide for 2026 — every student's organisation is asking "what's our agent strategy?"
- Emphasise that Phase 1 (infrastructure) is boring but essential — most failures happen because organisations jump to Phase 3
- The 6 readiness dimensions can become a self-assessment exercise (see Activity slide below)
- Time: 7 minutes

---

### [NEW 2026] Slide 9: "Agent Washing" and "Workslop" — New Risks to Navigate

**Insert after:** Slide 8 (Agentic Roadmap)  
**Format:** Concept with warning signs

**Content:**

**Agent Washing (Deloitte Tech Trends 2026):**
> "Many so-called agentic initiatives are actually automation use cases in disguise. Enterprises often apply agents where simpler tools would suffice, resulting in poor ROI."

**How to detect agent washing:**
- Does it require an LLM to reason about the next step? → Agent
- Does it follow a fixed, deterministic sequence? → Automation (not an agent)
- Is the vendor just rebranding their RPA/workflow tool? → Probably agent washing

**Workslop (also Deloitte):**
> "Poorly-designed agentic applications can actually add work to a process."

**Signs of workslop:**
- The human spends more time reviewing agent output than doing the task themselves
- The agent introduces errors that downstream humans must catch
- Total cycle time increases after agent deployment
- The agent creates "coordination overhead" — more meetings about the agent than the agent saves

**Roadmap implication:**
- Every agentic initiative needs a **"simpler alternative test"**: Could a rule-based workflow, an API integration, or a single prompt achieve 80% of this outcome without the complexity of an agent?
- Include "agent vs automation decision criteria" in your governance framework

**Henry Ford quote (cited by Deloitte):**
> "Many people are busy trying to find better ways of doing things that should not have to be done at all."

**Facilitator Notes:**
- This is a crowd-favourite slide — it gives students permission to push back on hype
- Common reaction: "Oh, that's what we're doing!" — Let the realisation land.
- For advanced audiences: discuss how to run a "simpler alternative audit" across their backlog
- Time: 5 minutes

---

### [NEW 2026] Slide 10: Process Redesign Before Automation

**Insert after:** Slide 9 (Agent Washing)  
**Format:** Concept with before/after

**Content:**

**The Deloitte insight that changes everything:**
> "Leading organizations are discovering something different: True value comes from redesigning operations, not just layering agents onto old workflows."

**Wrong approach:**
```
Human process (10 steps, 4 handoffs) → Add AI to each step → Same complexity, now with an AI layer
```

**Right approach:**
```
Human process (10 steps, 4 handoffs) → Ask: "What work needs to happen at all?" → Redesign to 4 steps → Automate the 4
```

**The implications for roadmapping:**
- Every AI initiative on your roadmap should include a "process redesign" phase BEFORE the "AI implementation" phase
- Budget 30–40% of initiative timeline for workflow redesign
- Involve operations people, not just engineers, in roadmap design

**Gartner prediction (2026):**
- 15% of day-to-day work decisions will be made autonomously by agentic AI by 2028
- 33% of enterprise software will include agentic AI by 2028
- But: >40% of agentic AI projects will fail by 2027 because legacy systems can't support modern AI execution demands

**Facilitator Notes:**
- Engineers may resist this: "We're not process consultants" — Acknowledge, then show that without process redesign, their technical work will be built on a broken foundation
- Pair this with an exercise: pick one process in your organisation and sketch what it would look like if you redesigned it from scratch for an AI-native world
- Time: 5 minutes

---

### [NEW 2026] Slide 11: AI ROI Measurement — The Modern Framework

**Insert after:** Metrics That Matter section  
**Format:** Framework / table

**Content:**

**Measuring AI ROI is not a single number. It's a multi-dimensional framework.**

**Three tiers of AI adoption KPIs (Worklytics 2025):**

| Tier | What it measures | Example KPIs | When to use |
|------|-----------------|--------------|-------------|
| **Tier 1: Action Counts** | Activity and adoption | # users, # AI interactions, feature usage rate | Weeks 1–4 (pilot validation) |
| **Tier 2: Workflow Time Saved** | Operational efficiency | Hours recovered, cycle time reduction, throughput increase | Months 1–3 (value demonstration) |
| **Tier 3: Revenue/Cost Impact** | Financial outcomes | Revenue attributable to AI, cost reduction $, headcount redeployed | Months 3–12 (ROI proof) |

**Key data points for calibration:**
- Average companies using GenAI see **3.7× ROI**; top leaders see **10.3×** (Lazarev 2026)
- Companies with structured measurement frameworks achieve **40–60% higher returns** than those with intuitive assessment
- 74% of orgs that deployed AI in 2025 achieved positive ROI within first year (Deloitte)
- BUT: 86–89% of AI pilots never reached production at scale

**The simple formula:**
> AI ROI = (Total AI-Driven Value − Total AI Investment) / Total AI Investment × 100

**What "Total AI-Driven Value" includes:**
- Direct cost reduction (labour, materials, vendor fees)
- Revenue uplift (conversion, speed-to-market, new capabilities)
- Risk reduction (compliance, error rates, security incidents avoided)
- Capability value (skills built, knowledge retained, time-to-insight improved)

**Facilitator Notes:**
- Students often want a single ROI number — help them understand that a single number is misleading for AI
- The 3-tier model is powerful because it maps to a timeline: you should expect Tier 1 metrics first, Tier 3 last
- Challenge: "What if we can't measure Tier 3 yet?" → That's fine — Tier 2 is sufficient to justify continued investment for the first 3 months
- Time: 6 minutes

---

### [NEW 2026] Slide 12: AI Agent Performance KPIs (Fin.ai Framework)

**Insert after:** Slide 11 (ROI Framework)  
**Format:** Table / reference
**⚡ ADVANCED**

**Content:**

**When your roadmap includes agentic deployments, standard AI KPIs aren't enough. Add these:**

| KPI | What It Measures | Target Range |
|-----|-----------------|--------------|
| **Resolution Rate** | % of tasks the agent completes without human escalation | 70–90% |
| **CX Score** | Customer/user satisfaction with agent interactions | ≥4.2/5.0 |
| **Cost per Resolution** | Total cost of agent operation per completed task | 30–70% reduction vs manual |
| **Automation Rate** | % of total volume handled autonomously | Increases over time |
| **Error Escalation Rate** | % of agent actions that require human correction | <5% for production-ready |
| **Time to Resolution** | How long the agent takes vs a human for equivalent task | Should be 3–10× faster |
| **Human-in-Loop Ratio** | Proportion of decisions requiring human approval | Decreases as trust builds |

**How to include in your roadmap:**
- Set baseline KPIs BEFORE deploying agents (human-only performance)
- Set target KPIs at each phase of the agentic roadmap
- Report monthly; trigger governance review if Error Escalation exceeds threshold

**Facilitator Notes:**
- ADVANCED: Best for students who are actively planning agent deployments
- For beginners: mention briefly and point to the Tier 1/2/3 framework instead
- Common question: "What automation rate should we target?" → Start with 50% and improve iteratively. 90%+ on day one is a red flag for agent washing.
- Time: 4 minutes

---

### [NEW 2026] Slide 13: Enterprise AI Transformation Data — BCG 2026 Findings

**Insert after:** Slide 12 (Agent KPIs) or Case Studies section  
**Format:** Data-driven case study

**Content:**

**BCG's latest findings on enterprise AI (June 2026):**

| Metric | BCG Data |
|--------|----------|
| First agentic clients: productivity improvement | **3×** (vs 10–20% from early GenAI waves) |
| Cycle time reduction with agentic AI | **80%** |
| Long-term cost reduction potential | **60%+** |
| AI-first banks: AI handles % of repetitive tasks | **70–80%** |
| AI-first banks: AI handles % of reasoning tasks | **30–50%** |
| BCG "Future-built" organisations | Only **5%** |
| "Scalers" (pockets of success) | **35%** |
| "Laggards" (no material AI value) | **60%** |

**The BCG "operating system of work" concept:**
> "In early waves, we saw organisations delivering productivity improvements of just 10% to 20%. In contrast, our first agentic clients are demonstrating a three-fold increase in productivity."

**What separates the 5% from the 60%:**
- Not technology choices — it's whether they redesign work around AI vs layer AI onto existing processes
- "The organisations getting value from agentic AI are not the ones with the best technology, but the ones working closely with their teams to redesign how they work" (BCG June 2026)

**New risk — AI deskilling (BCG June 2026):**
> "The skills that leaders consider most critical — judgment, problem framing, creative thinking — are most at risk due to AI deskilling."
- Roadmaps must include skill preservation strategies alongside automation

**Facilitator Notes:**
- The 3× productivity figure vs 10–20% for basic GenAI is the headline that captures executive attention
- The 5%/35%/60% split creates urgency: "Where do you want to be?"
- The deskilling warning is important — it's a new risk category that students may not have considered
- Time: 5 minutes

---

### [NEW 2026] Slide 14: The "Defend / Extend / Upend" Strategic Intent Model

**Insert after:** Stakeholder Alignment section  
**Format:** Framework with decision logic

**Content:**

**Gartner's AI strategic intent taxonomy (2026):**

| Category | What It Does | Near-Term Financial ROI? | Example |
|----------|-------------|--------------------------|---------|
| **Defend** | Boosts individual productivity | ❌ Rarely yields positive financial ROI | Individual copilots, writing assistants |
| **Extend** | Transforms existing divisions/teams for competitive differentiation | ✅ Best bet for near-term impact | Customer service agents, automated underwriting, supply chain optimisation |
| **Upend** | Changes competitive strategy, disrupts markets | ❌ Low odds, long timelines | New AI-native business models, platform plays |

**The Gartner guidance:**
> "Keep only the 'Extend' initiatives. They are the sole reliable path to near-term ROI."

**Why "Defend" projects fail the ROI test:**
- They make individuals faster, but unless the organisation changes how it allocates labour, no financial value is harvested
- Time saved must be converted to: reduced headcount, redeployed capacity, or increased output — most orgs don't do this

**How to sequence:**
1. **Near-term (0–6 months):** Fund "Extend" projects that generate measurable financial impact
2. **Medium-term (6–18 months):** Use Extend ROI to fund selected "Upend" bets
3. **Always running:** "Defend" projects as table-stakes (but don't expect them to prove AI ROI)

**Facilitator Notes:**
- This is controversial — many organisations are heavily invested in "Defend" (copilots). Don't dismiss those investments, but show why they aren't the path to proving AI ROI.
- Key question: "Is it Defend, Extend, or Upend?" should become a reflex when evaluating any new AI proposal
- Time: 5 minutes

---

### [NEW 2026] Slide 15: Building an AI Centre of Excellence (CoE) — 2026 Model

**Insert after:** Stakeholder Alignment section  
**Format:** Organisational design with roles

**Content:**

**What an AI CoE IS (2026 consensus):**
- Cross-functional coordination body that sets standards, enables delivery, and governs AI
- "Connective tissue" that gathers proven practices, smooths out rough edges, and helps every team move forward in sync (EPAM)
- Blends platform thinking (shared capabilities) with product thinking (outcomes, adoption, measurable impact) (Stack AI)

**What an AI CoE is NOT:**
- ❌ Not a delivery team (it doesn't build every model)
- ❌ Not a gatekeeper or bottleneck
- ❌ Not a committee that meets quarterly and produces reports
- ❌ Not a single team of data scientists
- Its role: "ensure every project meets the same quality, security, and governance bar, and that lessons learned in one team become available to the others" (ud.hk)

**Core functions (2026 CoE architecture):**

| Function | What It Does |
|----------|-------------|
| **AI Strategy & Portfolio** | Maintains the three-horizon portfolio; prioritises use cases |
| **Governance & Standards** | Sets responsible AI policies; runs model risk reviews |
| **Platform & Infrastructure** | Provides shared AI platform, tools, and compute |
| **Enablement & Literacy** | Runs training (like THIS course); builds internal AI champions |
| **Delivery Support** | Embeds specialists in project teams; runs design reviews |
| **Measurement & Learning** | Tracks ROI across portfolio; feeds learnings back |

**Key decisions (from Trantor 2026 guide):**
- Centralised vs. federated vs. hub-and-spoke model?
- Funding: central budget vs. business-unit funded vs. chargeback?
- Where does the CoE report? (CTO, CDO, CEO, or independent?)

**Facilitator Notes:**
- CIO.com: "Most companies are stuck in pilot purgatory. Building a CoE helps you stop reinventing the wheel and start actually making money from AI."
- Students often ask "Do we need a CoE?" → If >3 teams are building AI independently, yes.
- ADVANCED: Discuss the hub-and-spoke model (central standards + embedded specialists)
- Time: 6 minutes

---

### [NEW 2026] Slide 16: The "Simpler Alternative Test" — Governance for Roadmap Quality

**Insert after:** Slide 9 (Agent Washing) or Governance section  
**Format:** Decision framework / checklist

**Content:**

**Before adding ANY initiative to your AI roadmap, apply this 5-question filter:**

1. **Does this require an LLM to reason dynamically?**  
   If no → Use rules-based automation, not an agent

2. **Is there a commercial off-the-shelf tool that already does this?**  
   If yes → Buy before build (unless strategic differentiation is the goal)

3. **Can a single well-crafted prompt achieve 80% of the outcome?**  
   If yes → Start with prompt + API, not an agent framework

4. **Does the process need to be redesigned before automating?**  
   If yes → Redesign first, then decide whether AI is even needed

5. **Is the expected ROI greater than the cost of maintaining the AI system?**  
   If unclear → Run a 2-week spike before committing roadmap space

**The "enthusiasm bias" trap:**
> "The most common pattern: use cases are chosen based on what is exciting rather than what is feasible. Generative AI applications generate more enthusiasm than process automation. But enthusiasm and ROI are poorly correlated in AI." — DOsystems

**Facilitator Notes:**
- This is a popular exercise: have students apply the 5 questions to their top 3 candidate projects
- It often kills 30–50% of a team's AI backlog — that's the point
- Common resistance: "But we WANT to use agents!" → Redirect: "You want the outcome, not the technology. Agents are a means, not a goal."
- Time: 4 minutes

---

### [NEW 2026] Slide 17: Agentic Readiness Self-Assessment (Activity)

**Insert after:** Hands-On Activity section  
**Format:** Interactive workshop activity

**Content:**

**Activity: Agentic Readiness Assessment (10 min)**

Rate your organisation 1–5 on each dimension:

| Dimension | 1 (Not Ready) | 3 (Partially Ready) | 5 (Fully Ready) |
|-----------|---------------|---------------------|-----------------|
| **Strategic Alignment** | No AI strategy exists | AI strategy exists but not adopted | AI embedded in corporate strategy |
| **Technical Infrastructure** | Legacy-only; no APIs | Some modern services; partial API coverage | Microservices architecture; event-driven; API-first |
| **Data Readiness** | Siloed; no cataloging | Catalogued; some pipelines | Real-time, searchable, agent-accessible |
| **Process Maturity** | Undocumented; ad-hoc | Documented; some standardisation | Designed for automation; modular processes |
| **Governance & Risk** | No AI policy | Draft policies; no enforcement | Active governance; automated compliance |
| **Workforce Readiness** | No AI literacy | Pockets of AI users | Organisation-wide AI fluency + CoE |

**Scoring:**
- 6–12: **Foundation phase** — focus on literacy, policy, and infrastructure basics
- 13–20: **Ready for bounded agents** — start with single-task, human-in-the-loop agents
- 21–26: **Ready for workflow agents** — multi-step agents across tools
- 27–30: **Ready for orchestration** — multi-agent systems, cross-department automation

**Debrief questions:**
- Which dimension is your biggest gap?
- What one action would move your weakest dimension by +1?
- Where is your organisation on the n8n maturity staircase based on your total score?

**Facilitator Notes:**
- This is the module's signature hands-on activity — it replaces or supplements the original roadmap exercise
- Give students 5 min to score individually, then 3 min to discuss in pairs
- Collect aggregate scores (show of hands by range) to create a real-time class benchmark
- Works for all levels — beginners learn from the assessment framing; advanced students debate edge cases
- Time: 10 minutes

---

### [NEW 2026] Slide 18: Microsoft's AI Multiplier Effect — Economic Data

**Insert after:** Case Studies section  
**Format:** Data / evidence

**Content:**

**Microsoft's AI Transformation Report (2025–2026):**
> "Every new dollar spent on AI solutions and services by adopters is expected to generate an additional $4.9 in the global economy."

**Additional data points for roadmap business cases:**

| Source | Finding |
|--------|---------|
| Microsoft (1000+ customer stories) | $4.9 GDP multiplier per $1 AI investment |
| Lazarev Agency (2026) | Average GenAI ROI: 3.7×; top performers: 10.3× |
| Deloitte (2025) | 74% achieved positive ROI within first year |
| BCG (2026) | Agentic AI: 3× productivity, 80% cycle time reduction |
| PwC (2026) | 84% of C-suite view AI as critical for competitiveness |
| Gartner (2026) | 55% of enterprises increased AI investment despite budget cuts elsewhere |

**How to use these in your roadmap pitch:**
- For CFO conversations: lead with 3.7× average ROI and $4.9 multiplier
- For board conversations: lead with 84% of peers consider AI critical
- For engineering leadership: lead with BCG's 3× productivity and 80% cycle time data
- For risk conversations: 42% abandonment rate means poor execution IS the risk, not AI itself

**Facilitator Notes:**
- These numbers change quarterly — encourage students to refresh before their actual roadmap presentations
- Caution: all ROI figures are averages with wide variance. The 86–89% pilot-to-production failure rate balances the optimism.
- Time: 3 minutes

---

### [NEW 2026] Slide 19: From Roadmap to Execution — The 90-Day Sprint Model

**Insert after:** 30/60/90 Sequencing section  
**Format:** Process / execution framework

**Content:**

**Updated sequencing model (synthesised from moweb.com, Arion Research, Sutherland 2026):**

**Sprint 0 (Weeks 1–2): Foundation**
- Audit current Shadow AI usage
- Run agentic readiness self-assessment
- Identify executive sponsor
- Establish CoE or working group

**Sprint 1 (Weeks 3–6): Portfolio & Strategy**
- Apply Gartner 7-step funnel to backlog → reduce to 3–5 projects
- Classify using 60/30/10 three-horizon framework
- Run "simpler alternative test" on each
- Set baseline metrics for top 3 projects

**Sprint 2 (Weeks 7–10): First Deployment**
- Deploy Horizon 1 quick win to widest possible audience
- Measure Tier 1 KPIs (adoption, usage, satisfaction)
- Begin process redesign for top Horizon 2 initiative
- Establish governance baseline (policies, risk review cadence)

**Sprint 3 (Weeks 11–13): Scale & Report**
- Publish first ROI report (Tier 2 metrics: time saved, throughput)
- Present to leadership: results, learnings, next quarter roadmap
- Lock in funding for Horizon 2 initiatives
- Begin Sprint 0 for agentic roadmap (if readiness score ≥13)

**Facilitator Notes:**
- This gives students a concrete "Monday morning" action plan — they can literally start Week 1 after this module
- The original 30/60/90 framing is still valid but less specific. Use this as an updated, more actionable version.
- Common question: "What if we don't have executive sponsorship yet?" → Sprint 0's Shadow AI audit is the tool to GET sponsorship (show the risk).
- Time: 5 minutes

---

### [NEW 2026] Slide 20: Key Terminology Shifts — Vocabulary Update

**Insert after:** Key Concepts & Definitions section  
**Format:** Table

**Content:**

| Old Term (2023–2024) | New/Updated Term (2025–2026) | Why the Shift |
|---------------------|-------------------------------|---------------|
| AI strategy | AI operating model | Strategy alone isn't enough — need ops model |
| AI maturity model | AI adoption maturity model | Shift from "how mature" to "how ready to adopt" |
| Pilot | Proof of value (PoV) | Removes the "experiment with no end date" connotation |
| Quick wins vs moonshots | Three-horizon portfolio (60/30/10) | More nuanced than binary |
| ROI | Multi-dimensional value framework | Single-number ROI is misleading for AI |
| AI team | AI Centre of Excellence | Coordination body, not just a team |
| Chatbot | Bounded agent (Level 2) | Recognises that modern chatbots use tools, memory, reasoning |
| Automation vs AI | Agent vs automation decision criteria | New distinction: does it require reasoning? |
| AI adoption | AI transformation | Adoption = layering; transformation = redesigning |
| Metrics | Three-tier KPI framework | Action counts → Time saved → Financial impact |
| AI governance | Silicon-based workforce management | Deloitte's "agents as workers" framing |
| Shadow IT | Shadow AI | Same concept, AI-specific |

**Facilitator Notes:**
- Quick reference slide — flip to it whenever students use outdated terminology in discussion
- The "adoption vs transformation" distinction is the single most important vocabulary shift
- Don't be dogmatic about terminology — but explain why the shift happened
- Time: 3 minutes

---

## Facilitator Update Brief

### Top 3 Most Important Additions

1. **The Three-Horizon Portfolio (60/30/10) + Gartner Funnel** — Replaces the simplistic "quick wins vs transformational bets" with an actual allocation framework and a step-by-step prioritisation process. Students leave with a concrete decision tool.

2. **The Agentic Roadmap as a distinct layer** — Every organisation is now asking "what's our agent strategy?" The 5-phase agentic roadmap, Deloitte's reality check data, and the process-redesign-first principle are essential for 2026 relevance.

3. **Pilot Purgatory + BCG 10-20-70 + Process Redesign Before Automation** — These three slides together address the #1 reason AI roadmaps fail: treating it as a technology project. The data (88% PoC failure, 42% abandonment, 60% laggards) creates urgency for a better approach.

### What's Now Outdated in the Original Module

| Original Content | What to Do in Class |
|---|---|
| "Quick wins vs transformational bets" (binary framing) | Acknowledge as a starting point, then introduce the 60/30/10 portfolio as the evolved version |
| Generic AI maturity discussion | Update with specific 2026 models (n8n, SEI-Accenture, Sphere). Keep original as "the concept," show new ones as "the latest instruments" |
| "30/60/90 sequencing" without specifics | Replace with the Sprint 0/1/2/3 model which is more actionable |
| "Metrics that matter" without a framework | Overlay the three-tier KPI model (Action → Time → Financial) |
| No mention of agentic roadmapping | Add Slides 8–9 as a dedicated section — this is the #1 topic in enterprise AI strategy right now |

### Timing Guidance

The original module is 60 minutes. With 20 new slides, the content now supports:

- **60-minute version (standard):** Use original structure + add Slides 1, 2, 6, 7, 8, 13, 17, 19 (the highest-impact 8 additions). Skip ADVANCED slides.
- **75-minute extended version:** Add Slides 3, 4, 9, 10, 11, 14, 15 on top of the standard set
- **90-minute deep-dive:** All 20 new slides + original content. Best for leadership audiences who need full strategic depth.

**Suggested 60-minute integration:**
- Replace "quick wins vs transformational bets" with Slides 6+7 (~13 min)
- Replace generic maturity section with Slide 4 (~7 min)
- Add Slides 1+2 to opening (~10 min)
- Add Slide 8 (Agentic Roadmap) to main content (~7 min)
- Use Slide 17 (Readiness Assessment) as the activity (~10 min)
- Use Slide 19 (90-Day Sprint) as closing actionable takeaway (~5 min)
- Remaining ~8 min for Q&A and transitions

### New Tools/Accounts/Demos to Set Up in Advance

1. **CMU SEI AI Adoption Maturity Model** — Download from SEI Digital Library (free). Have the assessment instrument available as a handout or screen-share.
2. **n8n AI Maturity Framework blog post** — Keep URL ready for students who want the 4-dimension scoring detail
3. **Gartner AI Prioritisation Funnel** — Print or screen-grab the 7-step diagram
4. **Agentic Readiness Self-Assessment** (Slide 17) — Prepare as a handout or Miro/Mural board
5. **BCG 10-20-70 graphic** — Create a simple visual for the split (can be hand-drawn on whiteboard)
6. **Live demo (optional):** Show 2–3 real AI project proposals and walk through the Gartner Funnel live, striking projects at each step

---

*Module 05 Update completed — July 2026*
