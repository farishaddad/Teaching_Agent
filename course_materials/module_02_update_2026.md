# Module 02 — Generative AI for Everyone: Steps to Success
## [2026 UPDATE] — New Slides & Facilitator Delivery Notes

---

## GAP ANALYSIS

Based on research into the current (mid-2026) state of enterprise GenAI adoption, the following gaps exist in the original module:

1. **"Pilot purgatory" is now the dominant enterprise failure pattern** — 88-95% of AI pilots never reach production. The original module's "experiment → pilot → scale" framing needs updating with the reality that most enterprises are stuck between pilot and scale, not between experiment and pilot.

2. **AI ROI measurement has matured significantly** — McKinsey's five-layer measurement framework, the CFO-friendly payback models, and the distinction between "activity metrics" (adoption rate) vs. "value metrics" (P&L impact) are now table stakes in enterprise conversations. The original module lacks this vocabulary.

3. **The "AI Operating Model" concept is now mainstream** — CoE structures (centralised, federated, hub-and-spoke, centre-of-enablement) are now standard vocabulary. The original module covers "organisational readiness" generically but misses these specific patterns.

4. **Agentic AI has shifted the adoption conversation** — The question is no longer just "which use cases for GenAI?" but "which workflows benefit from autonomous agents vs. copilots vs. automations?" BCG and McKinsey now frame this as a spectrum of human-AI collaboration.

5. **The "AI Champions" / internal influencer model is now proven** — CIOs are running structured AI advocacy programmes. The original module doesn't cover how to build internal adoption movements.

6. **New failure mode taxonomy** — Microsoft's 2026 red-teaming paper identified novel agentic failure modes (agent compromise, flow manipulation, human-in-the-loop bypass). EPAM catalogued 21+ enterprise agent failure modes. The original "common failure modes" section is too generic for 2026.

7. **Change management for AI agents specifically** — CIO.com and BCG both published 2026 frameworks for workforce preparation for agentic AI. The workforce fear/resistance dimension is sharper now.

8. **The "6% problem"** — McKinsey's 2025 State of AI report shows only 6% of enterprises qualify as genuine AI high performers with measurable EBIT impact. The 82-point gap between adoption (88%) and value capture (6%) is the defining statistic of 2026.

9. **Time-to-value expectations have compressed** — PwC's 2026 predictions note executives have "little patience for exploratory AI investments." Median ROI is expected within 6-12 months, not 18-24.

10. **"Portfolio discipline" replaces "pilot mania"** — Fortune (March 2026) articulated the shift from running many pilots to running a disciplined portfolio of AI bets with kill criteria.

---

## NEW SLIDES

---

### [NEW 2026] Slide: The 2026 AI Adoption Paradox
**Insert after:** Section on "The GenAI Adoption Journey"
**Format:** Concept explanation with key statistics

**The Paradox in Numbers:**
- 88% of enterprises have deployed AI in at least one function (McKinsey 2025)
- Only 6% qualify as genuine AI high performers with EBIT impact (McKinsey)
- 95% of GenAI pilots produce no measurable P&L impact (MIT NANDA 2025)
- 42% of U.S. companies abandoned most AI initiatives in 2025 (up from 17% prior year)
- Enterprise GenAI spending reached $37B in 2025 (3.2× YoY growth)

**The 82-Point Gap:** Between adoption (88%) and value capture (6%) lies the defining challenge of enterprise AI in 2026. The gap is not technological — it is operational, organisational, and measurement-driven.

**What changed:** In 2024, the bottleneck was "getting started." In 2026, the bottleneck is "getting to production and proving value."

**Facilitator Notes:**
- Open with: "Hands up if your organisation has at least one AI project running. Now keep your hand up if that project has proven P&L impact." The gap is the point.
- Common student question: "If 95% fail, why are companies still investing?" Answer: because the 5% that succeed see 2-8× ROI. The problem is method, not category.
- Emphasise: This is not an argument against AI — it's an argument for rigour.
- Time: 5 minutes
- Use as a motivational frame: this course exists to put you in the 6%.

---

### [NEW 2026] Slide: Pilot Purgatory — The Enterprise Trap
**Insert after:** The 2026 AI Adoption Paradox slide
**Format:** Concept explanation with diagnostic framework

**Definition:** Pilot Purgatory is the state where an enterprise runs multiple AI proofs of concept indefinitely — consuming budget and credibility — without moving a single project to production.

**The Diagnostic Signs:**
| Symptom | Root Cause |
|---------|-----------|
| More than 3 AI pilots running with no production timeline | No kill criteria or graduation gates |
| Each pilot has a different sponsor and no shared infrastructure | Missing AI Operating Model |
| "Success" is measured by demo quality, not business outcome | Wrong metrics (activity vs. value) |
| IT and business disagree on whether the pilot "worked" | No shared success definition pre-launch |
| The same AI consultancy keeps getting renewed for new PoCs | Build capability, not dependency |

**Escape Routes (from Fortune 500 survivors):**
1. **Kill or graduate** — Every pilot gets a 90-day production-or-kill decision gate
2. **Production-first design** — Start with production constraints (data, security, monitoring) from day 1
3. **One bet deep** — Reduce from 12 pilots to 3 well-resourced bets with clear ownership
4. **Measure outcomes, not outputs** — Define the P&L line item before writing the prompt

**Facilitator Notes:**
- This is often the most resonant slide in the module. Ask: "How many pilots is your org running right now? How many have shipped?"
- Common question: "But we need to experiment before committing!" — Answer: Yes, but experiments need hypotheses, timelines, and kill criteria. Pilot purgatory is experimentation without discipline.
- For advanced students: introduce the concept of "governance debt" — building AI systems without production-grade controls from the start creates compounding rework.
- Time: 7 minutes

---

### [NEW 2026] Slide: The AI Adoption Spectrum (2026 Update)
**Insert after:** Pilot Purgatory slide
**Format:** Comparison table / visual spectrum

**The New Adoption Spectrum:**

The 2024 framing was: Chatbot → Copilot → Automation. The 2026 framing adds the agentic dimension:

```
Human Effort ←──────────────────────────────────────────────→ AI Autonomy

[AI-Assisted]     [Copilot]        [Automation]       [Agentic]
 Human does the    Human leads,     AI executes,       AI plans, acts,
 work; AI helps    AI suggests      human monitors     self-corrects
 Draft editing     Code completion  Invoice processing Multi-step research
 Research support  Meeting summaries Email triage       Customer onboarding
```

**Key 2026 Insight (BCG):** "With agentic AI, every team becomes its own transformation engine." The adoption question is no longer "should we use AI?" but "where on this spectrum should each workflow sit?"

**Decision Framework:**
| Place on Spectrum | When to Choose |
|-------------------|---------------|
| AI-Assisted | High-stakes, novel, creative, or regulated work |
| Copilot | Repetitive knowledge work where human judgment still needed |
| Automation | High-volume, well-defined processes with clear rules |
| Agentic | Multi-step workflows where speed matters and error cost is manageable |

**Facilitator Notes:**
- Draw the spectrum on a whiteboard. Ask students to place 3 of their current work tasks on it.
- Common misconception: "Everything should be agentic." Correct: agents add complexity and cost. Match the level of autonomy to the task's error tolerance and value.
- Time: 5 minutes
- Connect forward to Modules 11-13 (Agentic Track) for those who want to go deeper.

---

### [NEW 2026] Slide: The AI ROI Crisis — Why Measurement Matters
**Insert after:** Section on "Common Failure Modes"
**Format:** Data-driven concept slide

**The Measurement Vacuum:**
- 88% of leaders believe measuring AI ROI will determine future market leaders
- Only 27% have standardised metrics in place (Promethium 2026)
- Programs without a named outcome show **negative ROI 60% of the time**
- Programs with a single named outcome show **2-4× ROI within 12 months**

**Why Most AI ROI Fails:**
> *"95% of generative AI pilots produce no measurable P&L impact — not because the technology doesn't work, but because organisations deploy before defining the metric the AI must move."* — MIT NANDA, 2025

**The Three ROI Patterns (validated in production):**
| Pattern | Typical ROI | Timeline |
|---------|------------|----------|
| Cost reduction (hours saved, headcount avoidance) | 3–8× | 6–9 months |
| Velocity lift (faster cycle time, throughput increase) | 5–15× | 3–6 months |
| Revenue uplift (conversion, upsell, new products) | 1.5–3× | 12–18 months |

**The Rule:** Define your target metric BEFORE building your AI solution. The metric determines the architecture.

**Facilitator Notes:**
- This slide reframes AI as a business investment, not a technology experiment. It speaks the language of CFOs and P&L owners.
- Common student question: "What if the value is hard to quantify (e.g., employee satisfaction, brand)?" Answer: Start with what's measurable. Soft benefits are real but don't fund budgets. Lead with hard ROI, follow with qualitative value.
- Time: 5 minutes
- ⚡ ADVANCED: Reference McKinsey's five-layer measurement framework (activity → adoption → productivity → business outcome → financial impact)

---

### [NEW 2026] Slide: McKinsey's Five-Layer AI Measurement Framework
**Insert after:** The AI ROI Crisis slide
**Format:** Framework / layered diagram

**The Five Layers (from McKinsey, April 2026):**

```
Layer 5: Financial Impact
  "Did EBIT / revenue / margin actually change?"
  ────────────────────────────────────────────────
Layer 4: Business Outcome
  "Did the business process get faster/cheaper/better?"
  ────────────────────────────────────────────────
Layer 3: Productivity
  "Are people / systems producing more per unit of input?"
  ────────────────────────────────────────────────
Layer 2: Adoption
  "Are people actually using the AI tool consistently?"
  ────────────────────────────────────────────────
Layer 1: Activity
  "Is the model responding? Are calls being made?"
```

**The Failure Pattern:** Most enterprises measure Layer 1-2 (activity, adoption) and declare success. High performers measure Layer 4-5 (business outcome, financial impact) and hold teams accountable to them.

**Gartner's Reinforcement (May 2026):** "Organisations measure AI success through activity-based metrics like 'productivity' or 'adoption rates' rather than tangible financial outcomes." This is why boards lose confidence in AI programmes.

**Application:**
- Before launching any AI initiative, define which layer you're targeting
- Layer 1-2 metrics are leading indicators, not success criteria
- Layer 4-5 metrics require pre-AI baselines — capture them BEFORE deployment

**Facilitator Notes:**
- Draw the pyramid on the board. Ask: "Which layer does your current AI dashboard measure?" Most will answer Layer 1-2.
- For beginners: focus on the principle (measure outcomes, not activity).
- ⚡ ADVANCED: Walk through how to construct a pre/post measurement design for a specific use case.
- Common question: "Layer 5 takes too long to prove." Answer: Yes — that's why you need leading indicators (Layer 3-4) with a validated causal chain to Layer 5.
- Time: 5 minutes

---

### [NEW 2026] Slide: The AI Operating Model — Three CoE Architectures
**Insert after:** Section on "Organisational Readiness"
**Format:** Comparison table with decision criteria

**By 2026, the AI Center of Excellence (CoE) has become the dominant operating model** for any organisation running more than two production AI use cases. (Deloitte Applied AI Research 2026)

**Three Proven Models:**

| Model | Structure | Best For | Risk |
|-------|-----------|----------|------|
| **Centralised CoE** | Single team owns all AI delivery | Early-stage orgs with <5 use cases | Bottleneck as demand grows |
| **Federated (Hub & Spoke)** | Central standards + embedded AI teams in BUs | Mid-maturity orgs scaling across functions | Consistency drift if governance is weak |
| **Centre-of-Enablement** | Advisory body; BUs own delivery; CoE provides standards, tools, training | AI-mature orgs with strong internal capability | Fragmentation without clear guardrails |

**The CoE's Five Jobs:**
1. **Strategy** — Prioritise AI investments, maintain the roadmap
2. **Governance** — Set policies, manage risk, ensure compliance
3. **Platform** — Provide shared infrastructure (model access, evaluation tools, observability)
4. **Enablement** — Train, coach, and support builders across the org
5. **Value Tracking** — Measure and report AI ROI back to leadership

**Facilitator Notes:**
- Ask: "Does your organisation have a formal AI operating model? Who owns the AI strategy?" Most will say "it's unclear" — that's the point.
- Common question: "We're too small for a CoE." Answer: Even a 2-person team can serve as a lightweight CoE. The function matters more than the headcount.
- Connect to Module 16 (AI Governance) for the governance depth.
- Time: 5 minutes

---

### [NEW 2026] Slide: AI Champions — Building Internal Adoption Movements
**Insert after:** AI Operating Model slide
**Format:** Playbook / how-to

**The AI Champions Model (CIO.com, 2026):**

CIOs running the most successful AI programmes don't rely on top-down mandates or training alone. They build **networks of internal advocates** — AI Champions embedded in business units who:

- Demonstrate AI tools in context (not in abstract demos)
- Translate business problems into AI-solvable frames
- Provide peer support and troubleshooting
- Feed use case ideas back to the CoE
- Model safe, productive AI behaviour for their teams

**How to Build an AI Champions Network:**

| Step | Action | Timeline |
|------|--------|----------|
| 1 | Identify 2-3 enthusiastic early adopters per business unit | Week 1-2 |
| 2 | Give them early access to tools + 4 hours of hands-on training | Week 2-3 |
| 3 | Define their role: "first responder for AI questions in your team" | Week 3 |
| 4 | Create a Champions Slack channel for peer learning | Week 3 |
| 5 | Run monthly "what's working" sessions where Champions share wins | Ongoing |
| 6 | Recognise and celebrate Champions publicly (newsletter, all-hands) | Monthly |

**Key Insight:** Champions are NOT the technical experts. They are the *translators* — people who understand both the business context and the AI possibility space well enough to connect the two.

**Facilitator Notes:**
- Ask: "Who in your organisation is already informally playing this role?" Most will identify 1-2 people. The programme simply formalises and scales what's already happening organically.
- Common question: "How do you motivate Champions without extra pay?" Answer: Access (early tools, leadership visibility), recognition, and professional development. Most Champions self-select because they're already enthusiastic.
- Time: 4 minutes

---

### [NEW 2026] Slide: The New Failure Taxonomy (2026 Update)
**Insert after:** Original "Common Failure Modes" section
**Format:** Updated classification table

**The Original Failure Modes (still valid but incomplete):**
- Hallucination / accuracy issues
- Data quality problems
- Lack of executive sponsorship
- No clear success metrics

**[UPDATE 2026] The Extended Failure Taxonomy:**

| Category | Failure Mode | Impact | Source |
|----------|-------------|--------|--------|
| **Scope** | Scope creep (agent tasked beyond its infrastructure) | 35% of all failures | EPAM 2026 |
| **Data** | Incomplete or inconsistent data for AI to act on | 26% of all failures | EPAM 2026 |
| **Governance** | No production-grade controls from start ("governance debt") | Compounding rework | InsightSoftware |
| **Measurement** | Measuring activity (adoption rate) instead of value (P&L impact) | False confidence | MIT/Gartner |
| **Integration** | AI works in demo but fails when hitting real systems (APIs, latency, auth) | 73% of pilots fail here | Fortune 500 analysis |
| **Trust** | Users don't trust AI output; workaround behaviours emerge | Silent adoption failure | TechTarget |
| **Cost** | Token/compute costs at production scale 10-50× higher than pilot | Budget surprise | CloudZero |
| **Agentic-specific** | Agent compromise, flow manipulation, HITL bypass | Novel 2026 risk class | Microsoft Security |

**The "Demo-to-Production Gap":** A system that works perfectly in demo may fail in production because demos don't test: real data quality, concurrent users, edge cases, error recovery, security constraints, and cost at scale.

**Facilitator Notes:**
- Walk through each row with a brief real-world anecdote where possible.
- The "scope creep" failure is particularly resonant — ask students if they've seen an AI project expand from "draft emails" to "manage my entire inbox" without architecture changes.
- Microsoft's agentic failure modes are new in 2026 — connect to Module 14 (AI Security) for depth.
- Common question: "How do we prevent these?" Answer: That's what Modules 5, 6, 14, 15, and 16 are for — this module names the risks; later modules provide the mitigations.
- Time: 7 minutes

---

### [NEW 2026] Slide: The Seven Product Management Mistakes That Kill AI
**Insert after:** New Failure Taxonomy slide
**Format:** Checklist / anti-patterns

**From analysis of failed AI products (IdeaPlan 2026):**

Most AI products fail because of product management mistakes, not model limitations:

1. **Solving problems nobody has** — Building AI for a process pain that doesn't actually exist or isn't painful enough to change behaviour
2. **The demo-to-production gap** — Building for the demo, not for the production constraints
3. **Data quality as afterthought** — "We'll clean the data later" (you won't)
4. **Wrong metrics** — Measuring model accuracy instead of user outcome
5. **Trust failures** — No explainability, no uncertainty signals, no graceful degradation
6. **Cost-value mismatch** — Solution costs more per transaction than the problem it solves
7. **Ignoring existing workflows** — AI that requires users to change how they work fails faster than AI that fits existing patterns

**The Antidote:** Before building, answer three questions:
- "If this AI didn't exist, would someone pay for this job to be done manually?" (validates demand)
- "What's the worst thing that happens when it's wrong?" (defines error tolerance)
- "Can we measure success in a number that a CFO cares about?" (defines the metric)

**Facilitator Notes:**
- This is highly actionable. Ask students to evaluate their own AI initiatives against all 7.
- Common question: "But leadership asked for this AI project!" Answer: Leadership asked for the outcome the AI is supposed to deliver. If the project can't prove it delivers that outcome, it's still failing.
- Time: 5 minutes
- SKIP FOR BEGINNERS if time is tight — the failure taxonomy slide covers enough.

---

### [NEW 2026] Slide: Change Management for AI Agents — The Workforce Dimension
**Insert after:** AI Champions slide
**Format:** Framework / people-focused

**The Agentic Shift Changes the Change Management Challenge (BCG June 2026):**

Traditional AI change management: "Here's a tool — please use it."
Agentic AI change management: "Here's a colleague — please trust it."

**Three Employee Segments Requiring Different Approaches:**

| Segment | Behaviour | Risk | Strategy |
|---------|-----------|------|----------|
| **Enthusiasts** (20-30%) | Already using AI tools, may adopt rogue agents | Shadow AI, security exposure | Channel into Champions role; give sanctioned tools |
| **Pragmatists** (40-50%) | Willing to try but need proof of value and safety | Will revert to old workflows if early experience is poor | Start with quick wins; pair with Champions; demonstrate time savings |
| **Resisters** (20-30%) | Fear job displacement; may actively undermine | Detraction, morale damage, sabotage by workaround | Address fears directly; reframe as augmentation; show concrete "new role" examples |

**Key Principle:** "AI agents double the importance of change leadership" (CIO.com, June 2025). The risk of getting this wrong is not just low adoption — it's active workforce harm.

**The Reframe That Works:**
- ❌ "AI will do your job faster" (threatening)
- ✅ "AI will handle the parts of your job you'd happily never do again" (liberating)

**Facilitator Notes:**
- This slide often triggers emotional responses. Acknowledge that fear of AI-driven job loss is legitimate — don't dismiss it.
- Ask: "Which of these three segments are you?" Most will self-identify as pragmatist. Then ask: "Which segment are the people you manage?"
- Common question: "What do we do with people whose entire job IS the repetitive task?" Answer: That's a leadership responsibility to address honestly with reskilling paths — not something to paper over with "augmentation" language.
- Time: 5 minutes

---

### [NEW 2026] Slide: From "Pilot Mania" to "Portfolio Discipline"
**Insert after:** Change Management slide
**Format:** Strategic framework

**The 2026 Strategic Shift (Fortune, March 2026):**

2024-2025: "Launch as many pilots as possible — see what sticks."
2026: "Run a disciplined portfolio of AI bets with clear kill criteria."

**The Portfolio Discipline Framework:**

| Dimension | Pilot Mania (old) | Portfolio Discipline (new) |
|-----------|-------------------|---------------------------|
| **Number of initiatives** | 10-20 concurrent pilots | 3-5 well-resourced bets |
| **Success definition** | "It works in demo" | "It moves a named P&L metric" |
| **Kill criteria** | None — pilots run indefinitely | 90-day production-or-kill gate |
| **Ownership** | Diffuse — "innovation team" | Named P&L owner per initiative |
| **Infrastructure** | Each pilot builds its own | Shared platform (AI CoE-provided) |
| **Measurement** | Adoption rate | Value realised vs. investment |

**McKinsey's Rewired Framework (May 2026):**
"Any given company is aligned on the 'what' of AI — where the value is, what domains can be transformed. But companies will only perform at the level of their capabilities."

Translation: Strategy is no longer the bottleneck. Execution capability is.

**Facilitator Notes:**
- Ask: "Which column does your organisation live in?" Most will say left. Then ask: "What would it take to move to the right column?"
- Key insight: Portfolio discipline is not about doing less AI — it's about doing fewer things better with clear accountability.
- Connect forward to Module 5 (Building Your AI Roadmap) for the detailed sequencing framework.
- Time: 5 minutes

---

### [NEW 2026] Slide: The "Time to Value" Compression
**Insert after:** Portfolio Discipline slide
**Format:** Data + implications

**Executive Patience Has Collapsed (PwC 2026):**

> *"Executives have little patience for exploratory AI investments. Every dollar must fuel measurable outcomes."*

**The New Timeline Expectations:**

| Era | Expected Time to Value | Leadership Tolerance |
|-----|----------------------|---------------------|
| 2023 | 18-24 months ("this is new, give it time") | High — exploratory budgets |
| 2024 | 12-18 months ("show me progress") | Medium — board reporting required |
| 2025 | 6-12 months ("show me ROI") | Low — P&L accountability |
| 2026 | 3-6 months ("prove it or kill it") | Very low — competing for capital |

**What This Means for How You Design AI Initiatives:**
1. **Start with the smallest scope that can prove value** — don't boil the ocean
2. **Define the metric on day 1** — not day 90
3. **Build measurement into the architecture** — not as a post-hoc exercise
4. **Plan for the "prove it" conversation** at the 90-day gate

**The Median ROI Data Point:** Programs with a single named outcome achieve 2-4× ROI within 12 months. Programs without a named outcome show negative ROI 60% of the time. (GroovyWeb 2026)

**Facilitator Notes:**
- This slide should create urgency. The message: "The window for 'exploratory' AI is closing. Everything from now on needs to be tied to a number."
- Common pushback: "Some AI value is long-term (e.g., building a knowledge graph)." Answer: True — but even long-term plays need intermediate milestones that prove progress in business terms.
- Time: 4 minutes

---

### [NEW 2026] Slide: The Accenture Operating Model Gap
**Insert after:** Time to Value slide
**Format:** Case study / industry data

**Accenture Survey Headline (June 2026, Forbes):**
"AI investment surging, but operating models lag."

**Key Findings:**
- Only 23% of enterprises have scaled AI across the enterprise (despite 85% having deployed in at least one function)
- The gap is not technology — it is operating model architecture
- The 5% that succeed share six common capabilities:

**The Six Pillars of Enterprises That Scale AI (Kognitos 2026):**
1. **Clear ownership** — Named executive accountable for AI value, not just AI activity
2. **Shared platform** — Central AI infrastructure that business units consume, not build
3. **Data readiness** — Production-quality data pipelines feeding AI systems (not demo datasets)
4. **Talent model** — Mix of embedded AI engineers + CoE specialists + trained business users
5. **Governance by design** — Security, privacy, and compliance built into the platform, not bolted on
6. **Measurement rigour** — Financial impact tracked with the same discipline as any capital investment

**The 18-Month Roadmap Pattern:**
- Months 1-3: Establish CoE, platform, and governance foundations
- Months 4-6: First 2-3 use cases in production with measured outcomes
- Months 7-12: Scale proven patterns to additional business units
- Months 13-18: Achieve enterprise-wide AI-native operating model

**Facilitator Notes:**
- This is a powerful case-study slide for senior/leadership students. Ask: "Which of the six pillars is your organisation weakest on?"
- For more junior students, focus on the insight that "the technology works — the org doesn't" and what that means for their career positioning.
- Time: 5 minutes
- ⚡ ADVANCED: Discuss how Accenture, McKinsey, and BCG are themselves restructuring around AI delivery — the consulting model is changing too.

---

### [NEW 2026] Slide: Revised Use Case Prioritisation Matrix (2026)
**Insert after:** Original "Use Case Identification" section
**Format:** Updated framework with agentic dimension

**[UPDATE 2026] The Original Matrix (still valid):**
- Value (high/low) × Feasibility (high/low)
- Jobs-to-be-done lens

**The 2026 Extension — Adding the Autonomy Axis:**

```
                    HIGH VALUE
                        │
     ┌──────────────────┼──────────────────┐
     │ COPILOT QUICK    │  AGENTIC         │
     │ WINS             │  TRANSFORMATION  │
     │ (do these first) │  (do these next) │
─────┼──────────────────┼──────────────────┼── HIGH AUTONOMY
     │ NICE-TO-HAVE     │  AUTOMATION      │
     │ (deprioritise)   │  CANDIDATES      │
     │                  │  (steady state)  │
     └──────────────────┼──────────────────┘
                    LOW VALUE
                        │
```

**New Decision Criteria for 2026:**
- What is the **error cost** if AI gets it wrong? (determines autonomy level)
- What is the **data quality** for this workflow? (determines feasibility)
- What is the **current manual cost** per transaction? (determines ROI ceiling)
- Does this require **multi-step reasoning** or simple pattern matching? (determines architectural complexity)

**Facilitator Notes:**
- Use this as the framework for the hands-on activity (Use Case Prioritisation Sprint). Ask students to place 5 use cases from their organisation onto this updated matrix.
- Key teaching point: The top-left quadrant (high-value copilot) is where most 2026 value is being captured. The top-right (agentic transformation) is where 2027-2028 value will come from.
- Time: 5 minutes

---

### [NEW 2026] Slide: Activity — The "Prove It" Sprint (Updated Hands-On)
**Insert after:** Updated Prioritisation Matrix
**Format:** Hands-on activity

**Title:** The "Prove It" Sprint — From Use Case to Business Case in 15 Minutes

**Context:** In the original module, the hands-on was a "Use Case Prioritisation Sprint." This 2026 version adds the ROI measurement dimension.

**Instructions:**
1. **Select one use case** from the prioritisation matrix you just completed (5 min to discuss and choose)
2. **Answer five questions** (provided on a handout):
   - What P&L metric will this move? (be specific: "reduce call handling time by X%")
   - What is the current baseline? (today's number)
   - What is the minimum improvement that would justify the investment?
   - How will we measure it? (data source, cadence, dashboard)
   - What is the 90-day kill criterion? (If we haven't seen X by day 90, we stop)
3. **Present back** in 60 seconds: "We're going to [do X] with AI. Success means [metric] moves from [baseline] to [target] within [timeframe]. If it doesn't, we kill it." (3 min per group)

**Expected Outcome:** Students leave with a 60-second pitch for one AI initiative that speaks the language of executive decision-makers. They've practised the "prove it" framing they'll need to get AI projects funded.

**Facilitator Notes:**
- Groups of 3-4 work best. If individual, have each person write their own and pair-share.
- The hardest part is defining the metric. Coach students away from "improve efficiency" toward specific numbers.
- Common stumbling block: "I don't know the baseline." Response: "That's your first action item — you can't improve what you haven't measured."
- Time: 15 minutes total (5 min choose, 5 min write, 5 min present)

---

### [NEW 2026] Slide: Key Statistics Dashboard — 2026 State of Play
**Insert after:** Module opening / overview section
**Format:** Visual data dashboard (reference slide)

**The Numbers That Define 2026 Enterprise AI:**

| Metric | Number | Source |
|--------|--------|--------|
| Enterprises using AI in ≥1 function | 88% | McKinsey 2025 |
| Enterprises qualified as AI "high performers" | 6% | McKinsey 2025 |
| GenAI pilots producing measurable P&L impact | 5% | MIT NANDA 2025 |
| Enterprise GenAI spending (2025) | $37B | Industry analysis |
| Companies abandoning AI initiatives (2025) | 42% | S&P Global |
| AI pilots reaching production | 12-14% | IDC / Voiceflow 2026 |
| Orgs with standardised AI ROI metrics | 27% | Promethium 2026 |
| Expected time-to-value (2026) | 3-6 months | PwC 2026 |
| Average cost of a failed AI project | $340K | Industry analysis |
| Executives using AI weekly | 82% | Axis Intelligence 2025 |

**Key Takeaway:** The problem is clear — adoption is high, value capture is low. The course teaches you how to be in the top 6%.

**Facilitator Notes:**
- Use this as a reference slide — don't spend time presenting every number. Surface the 2-3 most impactful and let students absorb the rest.
- Update these numbers annually — they shift fast.
- Time: 2 minutes (quick orientation)

---

### [NEW 2026] Slide: The "Rewired" Framework — McKinsey's Scaling Model
**Insert after:** Portfolio Discipline slide
**Format:** Framework summary

**McKinsey's "Rewired" for AI (Updated May 2026):**

Originally published in 2023, updated for the agentic era. The core thesis:

> *"We don't rise to the level of our expectations; we fall to the level of our training."*

**The Six Capabilities That Determine AI Success:**
1. **Align** — Business-led roadmap with prioritised domains
2. **Organize** — Operating model (CoE + embedded teams)
3. **Build** — Talent, skills, and ways of working for AI delivery
4. **Adopt** — Change management, training, workflow integration
5. **Scale** — Platform, MLOps, governance, repeatability
6. **Govern** — Risk, responsible AI, compliance, continuous monitoring

**The 2026 Update:** The framework now explicitly accounts for agentic AI — adding "every team as a transformation engine" (BCG) to the adoption and scaling stages. The implication: you can no longer run AI transformation from a single central team. Every business unit must develop some AI capability.

**Facilitator Notes:**
- For advanced/senior students, this is the strategic "so what" of the module. It explains WHY organisational change, measurement, and operating model matter — they're literally the capabilities that determine whether AI succeeds.
- For beginners, summarise as: "Strategy + People + Platform + Governance = Scale"
- Time: 4 minutes
- Connect to Module 5 (Roadmap) and Module 16 (Governance) for depth.

---

### [NEW 2026] Slide: What "AI-Ready" Actually Means in 2026
**Insert after:** Revised Use Case Prioritisation Matrix
**Format:** Updated readiness checklist

**[UPDATE 2026] The Original "Organisational Readiness" section focused on People, Process, Technology.**

**The 2026 Readiness Checklist (updated for production and agentic realities):**

| Dimension | Ready ✅ | Not Ready ❌ |
|-----------|---------|-------------|
| **Data** | Production-quality pipelines with lineage; not just a data lake | "We have data somewhere" but no quality controls |
| **Platform** | Shared AI infrastructure (model access, evals, guardrails) | Every team building its own stack |
| **Talent** | Mix of AI engineers + trained business users + AI Champions | One data scientist shared across 5 teams |
| **Governance** | Policies defined BEFORE deployment; Responsible AI gates | "We'll figure out governance later" |
| **Measurement** | Pre-defined success metrics with baselines captured | "We'll measure ROI after launch" |
| **Security** | AI-specific threat model; prompt injection awareness; guardrails deployed | Traditional security only; no AI-specific controls |
| **Operating Model** | Clear CoE or equivalent; named AI owner per initiative | "Innovation team" with no production mandate |
| **Change Management** | Champions network; workforce preparation programme | Top-down mandate with no support structure |

**Self-Assessment Question:** "If I could only fix ONE of these dimensions in the next 90 days, which one would unblock the most AI value in my organisation?"

**Facilitator Notes:**
- Use as a closing self-assessment. Ask students to honestly rate their org on each dimension (1-5 scale).
- The most common "stuck" dimensions in 2026: Data quality, Governance, and Operating Model.
- Time: 4 minutes

---

### [NEW 2026] Slide: Discussion — "What Would You Kill?"
**Insert after:** Readiness Checklist slide
**Format:** Group discussion

**Discussion Prompt:**

You've just been appointed Head of AI at your organisation. You have 12 AI pilots running. Budget review is in 90 days. You can only take 3 to production.

**Questions for table discussion (4 min):**
1. What criteria would you use to select the 3 survivors?
2. How would you communicate the "kill" decision to the teams whose projects get cut?
3. What would you need to see in 90 days to confirm your 3 bets are working?

**Debrief Points:**
- Did anyone's criteria include "executive sponsorship"? Why does that matter?
- Did anyone use a measurable metric as a kill criterion? Or was it subjective?
- How did you think about the human/change management dimension of killing projects?

**Facilitator Notes:**
- This discussion synthesises the entire module: prioritisation + measurement + change management + portfolio discipline.
- Works best in groups of 3-4. If time is short, do as a think-pair-share (2 min think, 2 min discuss with neighbour).
- Time: 6 minutes (4 discuss, 2 debrief)
- This replaces or extends the original discussion questions section.

---

### [NEW 2026] Slide: Updated Quiz Questions
**Insert after:** Original Knowledge Check section
**Format:** Assessment

**[UPDATE 2026] Additional Quiz Questions:**

Q6. According to 2025-2026 research, what percentage of enterprises qualify as genuine AI "high performers" with measurable EBIT impact?
- A) 42%
- B) 23%
- C) 6% ✅
- D) 15%

Q7. What is "pilot purgatory"?
- A) Running AI in production without monitoring
- B) Running multiple AI proofs of concept indefinitely without moving any to production ✅
- C) A pilot that fails on the first day
- D) A pilot that costs more than expected

Q8. McKinsey's five-layer AI measurement framework recommends that organisations measure success at which layers?
- A) Layers 1-2 (Activity and Adoption)
- B) Layers 4-5 (Business Outcome and Financial Impact) ✅
- C) Only Layer 3 (Productivity)
- D) All five layers equally

Q9. Which of the following is NOT one of the three proven AI CoE models?
- A) Centralised CoE
- B) Federated (Hub & Spoke) CoE
- C) Autonomous AI Department with no governance ✅
- D) Centre-of-Enablement (Advisory)

Q10. Programs with a single named outcome achieve what typical ROI within 12 months?
- A) 0.5-1×
- B) 2-4× ✅
- C) 10-15×
- D) Negative ROI

---

## FACILITATOR UPDATE BRIEF

---

### 🎤 Top 3 Most Important Additions

1. **The ROI/Measurement Framework** (McKinsey's five-layer model + the "prove it" framing) — This is the single biggest gap in the original. Students will encounter CFO-level accountability for AI spend in 2026. They need the vocabulary and framework to navigate it.

2. **Pilot Purgatory + Portfolio Discipline** — The language has shifted from "how do we start?" to "how do we stop wasting money on pilots that never ship?" Students need to understand this shift and the 90-day kill-gate model.

3. **The AI Operating Model / CoE architecture** — In 2026, "who owns AI?" is answered with a structured operating model. Students need to know the three options and how to recommend one.

---

### 🎤 What's Now Outdated in the Original Module

| Original Content | What's Changed | How to Address |
|-----------------|---------------|----------------|
| "Experiment → Pilot → Scale" as linear journey | In 2026, most orgs are stuck in pilot (not experiment). The journey is "Pilot → Production-or-Kill → Scale" | Update the framing: acknowledge the original model but reframe for the 2026 reality using the "Pilot Purgatory" slide |
| Generic "organisational readiness" checklist | Now replaced by specific operating model options (CoE architectures) | Replace with the three CoE models + updated readiness checklist |
| "Common failure modes" (hallucination, data, sponsorship) | Still valid but incomplete. Add scope creep, governance debt, demo-to-production gap, cost surprise, agentic-specific failures | Keep original as "foundational" failures; add 2026 extended taxonomy |
| No mention of ROI measurement | Now table-stakes in every enterprise AI conversation | Add the ROI Crisis + Five-Layer Framework slides |

---

### 🎤 How to Fit in 60 Minutes (Recommended Sequencing)

**The original 60-min module stays as the core.** The 2026 additions slot in as follows:

| Time | Content | Source |
|------|---------|--------|
| 0-3 min | Welcome + Key Statistics Dashboard [NEW] | Sets urgency |
| 3-10 min | Original: GenAI adoption journey (lightly updated) | Foundation |
| 10-17 min | [NEW] Adoption Paradox + Pilot Purgatory + Adoption Spectrum | The 2026 reality |
| 17-25 min | [NEW] ROI Crisis + Five-Layer Framework | Measurement |
| 25-30 min | Original: Use case identification + [NEW] Updated Prioritisation Matrix | How to choose |
| 30-37 min | [NEW] AI Operating Model + AI Champions | Organisation |
| 37-44 min | [NEW] Failure Taxonomy (extended) + Portfolio Discipline | What goes wrong and the fix |
| 44-52 min | [NEW] "Prove It" Sprint (hands-on activity) | Application |
| 52-57 min | [NEW] "What Would You Kill?" Discussion | Synthesis |
| 57-60 min | Wrap-up + [NEW] Readiness Checklist self-assessment | Close |

**Total: 60 minutes — tight but achievable** if the facilitator keeps each slide to its recommended time.

**Extended version (75-90 min):** If time allows, add:
- The 7 Product Management Mistakes slide (+5 min)
- Change Management for AI Agents slide (+5 min)
- McKinsey "Rewired" Framework slide (+4 min)
- Accenture Operating Model Gap case study (+5 min)
- Extended debrief on the "Prove It" Sprint (+5 min)

---

### 🎤 New Tools/Accounts/Demos to Set Up in Advance

1. **No accounts needed** — this module is framework/strategy-focused, not tool-focused
2. **Prepare a whiteboard** (physical or digital) for the Adoption Spectrum and Prioritisation Matrix exercises
3. **Print handouts** for the "Prove It" Sprint (the 5 questions template)
4. **Bookmark these sources** for live reference during Q&A:
   - McKinsey "From Promise to Impact" (April 2026): https://www.mckinsey.com/capabilities/quantumblack/our-insights/from-promise-to-impact-how-companies-can-measure-and-realize-the-full-value-of-ai
   - Fortune "From Pilot Mania to Portfolio Discipline" (March 2026)
   - Gartner "5 AI Metrics That Actually Prove ROI to Your Board" (May 2026)
5. **Optional demo:** If presenting to a technical audience, show a simple AI project cost calculator (token costs × volume × months) to make the "cost surprise" failure mode tangible.

---

*Module 02 Update — July 2026*
*AI & Agentic AI Training Programme*
