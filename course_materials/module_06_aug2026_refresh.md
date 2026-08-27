# Module 06 — AI Development Lifecycle (AI-DLC)
## 🔄 [NEW AUG-2026] Content Refresh Addendum
### Track: Strategy | Date: 12 August 2026

---

## A) EXECUTIVE SUMMARY — What Changed Since July 2026

1. **Claude Code defaults to auto mode (Aug 14, 2026):** Anthropic is making auto mode the default for all Pro, Max, and Team plans — a background classifier decides which actions are safe to run without developer approval. This fundamentally shifts the human-in-the-loop model for AI-assisted development.

2. **OpenAI Codex reaches GA (Aug 11, 2026):** Codex is now generally available across editor, terminal, cloud, and mobile — serving 40+ trillion tokens since GPT-5-Codex launch. Daily usage grew 10x in early August. Non-developers now make up 20% of users and growing 3x faster than developers.

3. **Kiro reaches GA with parallel agents and property-based testing:** AWS's successor to Amazon Q Developer is now generally available with spec-driven development, parallel agent execution, and property-based tests that catch edge cases unit tests miss. Amazon Q Developer new signups blocked (May 15, 2026); full sunset April 30, 2027.

4. **Cursor 3 + Grok Bot (Aug 11, 2026):** SpaceXAI (formerly xAI) partnered with Cursor to launch "Grok Bot" — always-on AI agents that persist across sessions, coordinate with each other, and run when your laptop is closed. Cursor now at $500M ARR / $10B valuation (pre-acquisition: SpaceX bidding $60B).

5. **GitHub Copilot app goes agent-native (June 2026):** New standalone desktop app with "My Work" view showing active sessions, issues, PRs, and background automations. Copilot coding agent (GA since March 2026) works asynchronously — issue-to-PR without developer interaction.

6. **"MLOps is Dead" enters mainstream (Forbes, Aug 10):** Forbes declared traditional MLOps obsolete, replaced by "AgentOps" — observability, tracing, evaluation, cost monitoring for multi-step AI agents rather than single model inference.

7. **Context Engineering solidifies as THE skill of 2026:** Multiple major publications and practitioners (Sourcegraph, Augment Code, Anthropic) now position context engineering — not prompt engineering — as the defining developer skill. Agents complete an average of 20 autonomous actions before requiring human input.

8. **46% of all new code is AI-generated (GitHub, July 2026):** Up from 41% cited in July update. Gartner expects 60% by end of 2026. Google reports 25% of its own codebase is AI-assisted.

9. **Claude Opus 5 released (July 2026):** 1M context window, dynamic workflows for large-scale problems, nested subagents. Default Opus model in Claude Code.

10. **GPT-5.6 "Sol" released (Aug 11, 2026):** State-of-the-art across coding, knowledge work, cybersecurity, and science. Outperforms previous frontier models with fewer tokens at lower cost.

---

## B) NEW SLIDES

---

### [NEW AUG-2026] Slide: The Auto-Mode Paradigm Shift — From Human Approval to Classifier Gating
**Insert after:** [NEW 2026] The Agentic SDLC — AI as Participant, Not Just Product
**Source:** https://claude.com/blog/auto-mode-default-in-claude-code | https://www.theregister.com/ai-and-ml/2026/08/10/claude-code-puts-auto-mode-in-the-drivers-seat/

**Content:**

On August 14, 2026, Anthropic flips the default: Claude Code sessions no longer ask developers to approve each action. Instead, a **background classifier** decides in real-time which actions are safe to execute autonomously.

**What changed:**
```
BEFORE (pre-Aug 14):    Developer prompt → Agent proposes action → Human approves → Execute
AFTER (Aug 14 default): Developer prompt → Agent proposes action → Classifier approves → Execute
                                                                         ↓ (if risky)
                                                                    Human approves → Execute
```

**The numbers:**
- 89% of actions the classifier auto-approves match what a human would have approved
- 11% "miss rate" — actions the classifier flags that a human would have let through (conservative)
- Anthropic claims the classifier is "as safe or safer than an average user clicking through prompts"

**Why this matters for AI-DLC:**
- The **governance model** shifts from manual gates to algorithmic gates
- Organisations need to define what "safe to auto-approve" means in their context
- Enterprise plans remain opt-in — regulatory/compliance teams keep manual approval
- This is the direction ALL agentic tools are heading: human oversight → machine oversight with human escalation

**The broader pattern (Aug 2026):**
| Tool | Autonomy Model |
|---|---|
| Claude Code (Aug 14) | Classifier-gated auto mode |
| Cursor Cloud Agents | Full autonomy in cloud VMs |
| GitHub Copilot coding agent | Issue-to-PR, async, no human until review |
| OpenAI Codex | Always-on agents with memory |
| Kiro | Spec-gated autonomy (spec = boundary) |

**AI-DLC implication:** Stage 7 (GOVERN) must now include governance of the **automation classifiers themselves** — not just the AI outputs.

**Facilitator Notes:**
- This is breaking news — announced August 7, taking effect August 14. Frame as "happening right now."
- The 11% miss rate is a great discussion point: "Is 11% false-positive acceptable? What about for your codebase?"
- Common question: "Can I turn it off?" Answer: Yes. Enterprise plans stay opt-in. But the trend is clear.
- Time: 5 minutes

---

### [NEW AUG-2026] Slide: OpenAI Codex GA — The Multi-Surface Agent
**Insert after:** [NEW 2026] AI-Assisted Development Across the Lifecycle
**Source:** https://openai.com/index/codex-now-generally-available/ | https://openai.com/index/introducing-the-codex-app/

**Content:**

On August 11, 2026, OpenAI made Codex generally available — not as a code completion tool, but as a **full lifecycle development agent** available everywhere:

**Surfaces:**
- **Codex App** (standalone): Multi-agent workspace, project-organized threads, PR review, file viewing, SSH to remote devboxes, in-app browser
- **Terminal/CLI**: Always-on coding agent
- **IDE integration**: VS Code, JetBrains
- **Web (ChatGPT)**: Accessible to non-developers
- **Mobile (iOS)**: Task supervision on the go

**Key stats:**
- 40+ trillion tokens served in first 3 weeks of GPT-5-Codex
- 10x daily usage growth in early August 2026
- 20% of users are non-developers (growing 3x faster than developers)
- GPT-5.6 "Sol" powers the latest version — SOTA on coding benchmarks

**What this means for AI-DLC:**
1. **Non-developers entering the lifecycle:** 20% of Codex users aren't engineers. The AI-DLC must accommodate participants who don't read code but can specify intent.
2. **Multi-surface means multi-governance:** The same agent works in terminal (high trust), web (medium trust), and mobile (low bandwidth for review). Governance must adapt to surface.
3. **Always-on background agents:** Like Cursor Cloud Agents, Codex persists across sessions. Work continues when humans aren't watching.

**Competitive landscape (August 2026):**
| Agent | GA Date | Background Work | Multi-Model |
|---|---|---|---|
| GitHub Copilot coding agent | March 2026 | Yes (issue-to-PR) | Yes (Claude, GPT-5) |
| Cursor Cloud Agents | May 2026 | Yes (cloud VMs) | Yes (multi-model) |
| OpenAI Codex | August 2026 | Yes (always-on) | GPT-5.x family |
| Claude Code | GA (auto-mode Aug 14) | Yes (nested subagents) | Claude family |
| Kiro | GA (July 2026) | Yes (parallel agents) | Bedrock models |

**Facilitator Notes:**
- The "non-developers are 20% of users" stat is the headline to emphasise. It changes who participates in AI-DLC.
- Demo idea: Show the Codex app's multi-agent workspace if possible.
- Common question: "Which one should I use?" Answer: Depends on your ecosystem. GitHub-native → Copilot. AWS → Kiro. Model flexibility → Cursor. OpenAI ecosystem → Codex.
- Time: 5 minutes

---

### [NEW AUG-2026] Slide: Kiro GA — Spec-Driven Development Goes Mainstream
**Insert after:** [NEW 2026] Spec-Driven Development (SDD)
**Source:** https://kiro.dev/ | https://kiro.dev/blog/general-availability/

**Content:**

Kiro, AWS's spec-driven IDE (successor to Amazon Q Developer), reached general availability in mid-2026 with a clear thesis: **"Move beyond AI coding to agentic engineering."**

**What Kiro does differently:**
```
Traditional AI coding:  Prompt → Code → Hope it works
Kiro's approach:        Prompt → Requirements → Architecture → Tasks → Parallel agents → Property-based tests → Verified code
```

**Key capabilities (GA, August 2026):**
1. **Spec generation from prompts:** Prompts become requirements, architectural designs, and sequenced tasks automatically
2. **Parallel agent execution:** Independent tasks run simultaneously (e.g., 6 independent endpoints built in parallel)
3. **Property-based testing:** Tests that catch edge cases unit tests miss — generated automatically from specs
4. **Hooks:** Event-driven automations triggered on file save/create/delete (like CI but in-IDE)
5. **IDE 1.0 permissions:** Capability-based permission system — agent asks before performing operations you haven't explicitly allowed

**The Amazon Q → Kiro migration:**
- New Q Developer signups blocked: May 15, 2026
- Q Developer full sunset: April 30, 2027
- Migration path: Q's inline suggestions → Kiro's spec-driven approach
- Key difference: Q completed code; Kiro completes *projects*

**Why property-based testing matters:**
```python
# Unit test: checks one specific case
def test_add(): assert add(2, 3) == 5

# Property-based test: checks ALL cases that satisfy a property
@given(st.integers(), st.integers())
def test_add_commutative(a, b): assert add(a, b) == add(b, a)
```
Property-based tests generated from specs catch the bugs that pass unit tests but break in production.

**AI-DLC connection:** Kiro embeds the full AI-DLC (Specify → Design → Develop → Evaluate) inside the IDE. It's the first tool to make the lifecycle a single-tool experience.

**Facilitator Notes:**
- This updates the SDD slide from July — Kiro is now GA, not preview.
- Key talking point: "Amazon is betting so heavily on spec-driven development that they're sunsetting their existing AI coding tool (Q Developer) in favour of it."
- For AWS-focused students: This is now THE tool for their ecosystem.
- Time: 4 minutes

---

### [NEW AUG-2026] Slide: The Background Agent Revolution — Async Development is Here
**Insert after:** [NEW 2026] GitHub Agentic Workflows
**Source:** https://startdebugging.net/2026/07/cursor-cloud-agents-vs-github-copilot-coding-agent-for-background-prs/ | https://github.com/features/copilot/agents

**Content:**

By August 2026, all major AI development tools support **background agents** — coding agents that work asynchronously while you do other things:

**The async development pattern:**
```
OLD:  Developer writes code → Opens PR → Waits for review
NOW:  Developer assigns issue → Goes to lunch → Comes back to PR ready for review
```

**How each tool implements background work (August 2026):**

| Tool | Launch Method | Runtime | Output | Limit |
|---|---|---|---|---|
| GitHub Copilot | Assign issue or chat | GitHub infrastructure | PR with tests | 59 min per run |
| Cursor Cloud | Plan mode → "Send to cloud" | Isolated cloud VM | PR with demo artifacts | No fixed limit |
| Claude Code | Nested subagents / dynamic workflows | Local + cloud | Code changes in session | Context window |
| OpenAI Codex | Task in Codex app | OpenAI cloud | PR or code changes | Session-based |
| Kiro | Spec tasks → parallel agents | IDE + cloud | Verified implementations | Task-based |

**What this changes about AI-DLC:**
1. **Stage 4 (DEVELOP) becomes asynchronous:** Developers don't sit and watch code get written anymore
2. **Stage 5 (EVALUATE) must be automated:** If code is generated in the background, eval gates must run automatically — no human is watching
3. **Stage 6 (MONITOR) starts at generation time:** You need observability into what agents are doing while you're away
4. **New concern: "Agent drift"** — background agents may solve the wrong problem if specs aren't tight enough

**Real-world example (Faire, 2026):**
- 2,000+ autonomous agent runs per week using Cursor Cloud Agents
- Automated: bug report triage from Slack, CI failure fixes, code review routing
- Replaced an in-house background agent system with Cursor as "recommended platform for agentic development"

**Facilitator Notes:**
- This is where the "Agentic SDLC" becomes visceral — it's not theoretical, it's how companies work today.
- The 59-minute limit on GitHub Copilot is a great discussion point: "What does your agent do if it can't finish in an hour?"
- Common question: "How do I trust code written when I wasn't looking?" Answer: Automated eval gates, property-based tests, and mandatory human review before merge.
- Time: 5 minutes

---

### [NEW AUG-2026] Slide: Context Engineering — The Defining AI Developer Skill of 2026
**Insert after:** [NEW 2026] Key Terminology Update
**Source:** https://sourcegraph.com/blog/context-engineering | https://blog.getbind.co/context-engineering-in-2026-the-complete-developers-guide/

**Content:**

**Context engineering** has displaced prompt engineering as the defining skill for AI-assisted development.

**Andrej Karpathy's metaphor (June 2025):** "The LLM is a CPU, the context window is RAM, and you are the operating system responsible for loading exactly the right information for each task."

**The hierarchy (2026):**
```
Context Engineering (systems-level)
  └── Prompt Engineering (message-level)
        └── Prompt Writing (text-level)
```

**The six layers of context engineering (Sourcegraph, 2026):**
| Layer | What It Controls | Example |
|---|---|---|
| 1. System instructions | Agent persona, constraints, format | CLAUDE.md, .cursorrules |
| 2. Retrieved knowledge | RAG, docs, code search | Codebase indexing, doc retrieval |
| 3. Conversation history | What to keep, compress, or discard | Context compression strategies |
| 4. Tool definitions | Available capabilities and schemas | MCP servers, function schemas |
| 5. Working memory | Short-term state across turns | Agent scratchpads, variable tracking |
| 6. Long-term memory | Learned preferences, project patterns | Memory systems, preference stores |

**Why context > prompts:**
- A perfect prompt inside a bad context still produces bad results
- Agents complete **20 autonomous actions** before requiring human input (Anthropic 2026)
- With 200K–1M token windows, the question isn't capacity — it's what to *include*

**Context engineering in practice:**
```markdown
# CLAUDE.md (project root)
## Project Context
- Framework: Next.js 14 with App Router
- Database: PostgreSQL with Prisma ORM
- Auth: NextAuth.js v5

## Code Conventions
- Use server actions for mutations
- All API routes return typed responses
- Tests use Vitest + Testing Library

## Known Issues
- The payment module uses a legacy API (don't refactor)
- Rate limiting is handled at the edge (Cloudflare)
```

**AI-DLC connection:** Context engineering is how you make Stage 2 (SPECIFY) work in practice. The spec + context files together give agents everything they need to produce correct code.

**Facilitator Notes:**
- This extends the "prompt engineering as a development discipline" section — frame as evolution, not replacement.
- The Karpathy quote is memorable: "The LLM is a CPU, context is RAM, you are the OS."
- Live demo idea: Show a CLAUDE.md or .cursorrules file and how it changes agent behaviour.
- For beginners: Focus on the metaphor. For advanced: Discuss context compression for long agent sessions.
- Time: 5 minutes

---

### [NEW AUG-2026] Slide: The "MLOps is Dead" Moment — From MLOps to AgentOps
**Insert after:** [NEW 2026] LLMOps in 2026 — The Six-Layer Stack
**Source:** https://www.forbes.com/sites/nishatalagala/2026/08/10/mlops-is-dead-long-live-the-new-mlops/ | https://github.com/dyronrh/awesome-agentops-landscape

**Content:**

On August 10, 2026, Forbes declared: **"MLOps is Dead. Long Live The New MLOps."** The article crystallised what practitioners have been experiencing: the operational challenge is no longer managing models — it's managing agents.

**The shift:**
```
MLOps (2019-2024):    Model → Train → Validate → Deploy → Monitor drift
LLMOps (2024-2026):   Prompt → Eval → Deploy → Monitor quality + cost
AgentOps (2026+):     Agent → Multi-step trace → Span-level eval → Tool monitoring → Coordination
```

**Why agents break MLOps assumptions:**
| MLOps Assumption | Agent Reality |
|---|---|
| Single model inference | Multi-model orchestration with routing |
| Request → Response | Multi-turn, multi-tool, branching workflows |
| Deterministic pipeline | Non-deterministic, path-dependent |
| Monitor model drift | Monitor agent behaviour, tool failures, coordination bugs |
| Cost per training run | Cost per agentic session (variable, unpredictable) |

**The AgentOps tool landscape (Aug 2026):**
- **66+ tools** now claim to solve AI observability (Latitude.so analysis)
- **Key platforms:** Arize AX/Phoenix, LangSmith, Langfuse, Braintrust, Confident AI, Helicone, Latitude, Datadog LLM Observability
- **New category: Agent simulation** — running agents through synthetic conversations before production (FutureAGI, Galileo)
- **CIO.com identified 19 AgentOps tools** as required enterprise infrastructure (July 2026)

**What AgentOps adds to the LLMOps 6-layer stack:**
- **Span-level tracing:** Trace each step in a multi-step agent workflow
- **Tool call monitoring:** Which tools are agents using? Are they failing?
- **Coordination observability:** When multi-agent systems interact, who did what?
- **Session-level cost attribution:** What did this entire agent session cost?
- **Anomaly detection on agent behaviour:** Not just output quality — is the agent doing unexpected things?

**Facilitator Notes:**
- The Forbes headline makes a great opening: "Forbes just said MLOps is dead. What does that mean for us?"
- This extends the July 2026 LLMOps 6-layer stack — add AgentOps as an evolution, not replacement.
- For teams still doing traditional ML: "MLOps isn't literally dead for your use case. But if you're building agents, you need AgentOps."
- Time: 5 minutes

---

### [NEW AUG-2026] Slide: The AI Code Generation Security Update — 46% and Rising
**Insert after:** [NEW 2026] The Security Gap in AI-Generated Code
**Source:** https://vibecoding.app/blog/vibe-coding-complete-guide | https://www.ibm.com/think/insights/vibe-coding-security-risks

**Content:**

**Updated data (July-August 2026):**
- **46% of all new code is AI-generated** (GitHub, July 2026) — up from 41% in our last update
- **Gartner expects 60% by end of 2026**
- Google: 25% of its own codebase is AI-assisted
- IBM now distinguishes between "vibe coding security risks" and "ordinary security risks" — they're fundamentally different threat profiles

**IBM's insight (July 2026): "Vibe coding security risks aren't like ordinary security risks"**

The difference:
| Ordinary Security Risk | Vibe Coding Security Risk |
|---|---|
| Developer understood the code, made a mistake | No one fully understands the generated code |
| Fix requires understanding the intent | Fix requires understanding code you didn't write |
| Knowledge exists in the team | Knowledge exists only in the model's training data |
| Single point of failure | Systematic vulnerability patterns across codebases |

**New mitigation: The "three-month wall" (Augment Code, June 2026):**
- Vibe-coded projects hit a documented pattern: rapid progress for ~3 months, then technical debt compounds into significant maintenance overhead
- Root cause: Generated code lacks the architectural coherence that comes from human design intent
- Solution: Spec-driven development provides the architectural intent that prevents the wall

**Updated AI-DLC security principle:** Every vibe-coded project must have a **planned transition point** from vibe coding (exploration) to spec-driven development (production governance) before the three-month wall hits.

**Facilitator Notes:**
- Update the 45% stat from July to 46% (GitHub's latest)
- The IBM distinction between vibe coding security and ordinary security is a powerful framing
- The "three-month wall" is new and very practical — students building with AI will recognise this
- Time: 3 minutes (update existing slide, don't extend the module)

---

### [NEW AUG-2026] Slide: Grok Bot & The "Always-On Agent" Arms Race
**Insert after:** [NEW AUG-2026] The Background Agent Revolution
**Source:** https://www.macrumors.com/2026/08/11/grok-bot-macos-ios/ | https://startupfortune.com/spacexai-and-cursor-launch-grok-bot-an-always-on-team-of-ai-agents/

**Content:**

On August 11, 2026, SpaceXAI (formerly xAI) and Cursor launched **Grok Bot** — "a team of always-on agents" that:
- Sign into apps and retain memory across tasks
- Coordinate with each other on complex work
- Run in the cloud when your laptop is closed
- Work across tools, websites, and applications

**The competitive dynamics (Aug 2026):**
```
              AUTONOMY
                 ↑
                 │  Grok Bot (always-on, multi-app)
                 │  OpenAI Codex (always-on, multi-surface)
                 │  Cursor Cloud (background VMs)
                 │  Claude Code auto-mode (classifier-gated)
                 │  GitHub Copilot agent (async, PR-scoped)
                 │  Kiro (spec-bounded)
                 │
                 └──────────────────────────────→ GOVERNANCE
```

**The pattern:** Every major player is racing toward MORE agent autonomy, LESS human intervention. The differentiation is in governance models:
- **Spec-bounded** (Kiro): Agent freedom within spec constraints
- **Classifier-gated** (Claude Code): ML model decides what's safe
- **Time-bounded** (GitHub): 59-minute sessions with defined scope
- **Infrastructure-bounded** (Cursor): Isolated VMs, can't escape sandbox
- **Always-on** (Grok Bot, Codex): Maximum autonomy, memory persistence

**AI-DLC implication:** Your lifecycle governance must match your tool's autonomy level. Higher autonomy → more automated gates → more robust eval infrastructure.

**The financial signal:** SpaceX is bidding $60B to acquire Cursor. This is the biggest-ever bet on AI-assisted development tooling.

**Facilitator Notes:**
- This is the "wow, things are moving fast" slide. Three major announcements in a single week (Aug 11).
- Discussion question: "Where on the autonomy-governance spectrum does YOUR organisation need to be?"
- For regulated industries: "Always-on agents may not be appropriate yet. Spec-bounded or classifier-gated may be your ceiling."
- Time: 4 minutes
- SKIP FOR BEGINNERS if running short on time.

---

### [NEW AUG-2026] Slide: CI/CD for AI Agents — The 2026 Reference Architecture
**Insert after:** [NEW 2026] Evals-as-Code — Automated LLM Testing in CI/CD
**Source:** https://techcommunity.microsoft.com/blog/educatordeveloperblog/cicd-for-ai-agents-on-microsoft-foundry/4522218 | https://futureagi.com/blog/ci-cd-for-ai-agents-best-practices-2026/

**Content:**

Microsoft's Foundry team published the definitive reference architecture for agent CI/CD (May 2026). Key insight: **"Promotion happens at the agent version level, and release gates are driven by evaluation outcomes, not just test results."**

**The agent deployment unit:**
```
AGENT VERSION (immutable artifact)
├── Model selection (which LLM)
├── System instructions (persona, constraints)
├── Tool definitions (APIs, functions)
├── Configuration (temperature, routing, limits)
└── Eval baseline (expected performance scores)
```

**The three-gate evaluation framework:**
| Gate | What It Tests | Threshold |
|---|---|---|
| Quality | Answer correctness, task completion, hallucination rate | Team-defined |
| Safety | Grounded responses, policy compliance, tool usage validation | Zero-tolerance |
| Performance | Token usage per query, P95 response latency | SLA-driven |

**Two-lane CI pipeline pattern (GetAutonoma, July 2026):**
```
FAST LANE (every commit):        SLOW LANE (merge to main + nightly):
├── Deterministic format checks   ├── Full LLM-as-judge eval suite
├── Schema validation             ├── Multi-run scoring (average 3+ runs)
├── Heuristic rules               ├── Statistical significance tests
└── < 30 seconds, $0              └── 4-10 minutes, $3-50
```

**The $3.20 problem (FutureAGI, May 2026):**
> "The eval workflow runs 247 LLM-as-judge calls across nine rubrics on 200 examples. Four minutes, $3.20, green check. Twelve hours later, the support agent starts refusing valid questions on a class of queries the dataset never covered."

**Lesson:** Golden datasets must be continuously expanded with production failures. Evals are only as good as your test coverage.

**Tools for agent CI/CD (August 2026):**
- **Confident AI** — best for release gates, regression detection, failure insights
- **Red Hat InstructLab CLI** — CI/CD-first eval surface, machine-parseable output
- **Microsoft Foundry** — native agent lifecycle management with eval promotion
- **Braintrust** — eval CI/CD with dataset management and canary support
- **FutureAGI** — agent simulation + eval in CI

**Facilitator Notes:**
- This extends the Evals-as-Code slide with the full reference architecture.
- The "$3.20 problem" quote is a great teaching moment: evals pass, but production fails. Why?
- Common question: "How often should I update my golden dataset?" Answer: Every production failure becomes a new test case. Budget 30 minutes/week.
- Time: 5 minutes

---

### [NEW AUG-2026] Slide: The GitHub Copilot Desktop App — Agent-Native UX
**Insert after:** [NEW AUG-2026] OpenAI Codex GA
**Source:** https://github.blog/news-insights/product-news/github-copilot-app-the-agent-native-desktop-experience/ | https://github.blog/changelog/2026-07-07-codex-as-agent-provider-and-agentic-enhancements-in-jetbrains-ides/

**Content:**

In June 2026, GitHub shipped the **Copilot App** — a standalone desktop experience built around agents, not files:

**Key features:**
- **"My Work" view:** Active sessions, issues, PRs, and background automations in one dashboard
- **Copilot CLI agent (June 2026):** Terminal-first agentic experience with agent picker, slash commands, debug panel
- **Codex as agent provider (July 2026):** OpenAI's Codex model available as an agent provider alongside Claude and GPT models
- **Custom model support:** Enterprise admins configure which models are available
- **Multi-model harness:** Routes to claude-opus-4-8, claude-sonnet-4-6, GPT-5.x depending on task

**The shift from "pair programmer" to "project manager":**
```
Copilot 2024:  You code → Copilot suggests next line
Copilot 2026:  You assign issue → Copilot plans, codes, tests, opens PR → You review
```

**Copilot in the enterprise (July 2026):**
- Agentic AI features integrated with existing branch protection, CODEOWNERS, and governance controls
- Enterprise docs: "Integrating agentic AI into your enterprise's software development lifecycle"
- Hooks support (July 2026): Custom automation triggers within Copilot workflows
- MCP server management: Richer configuration for tool access

**Facilitator Notes:**
- Key message: "The IDE is no longer the center of the developer experience. The agent dashboard is."
- This connects to Cursor's same shift: "Cursor 3 is no longer about the editor — it's about the agents."
- For enterprise students: GitHub's governance integration (branch protection + CODEOWNERS + Copilot agents) is the enterprise-ready story.
- Time: 3 minutes

---

### [NEW AUG-2026] Slide: Cursor 3 — The Agent-Native IDE at Scale
**Insert after:** [NEW AUG-2026] The Background Agent Revolution
**Source:** https://cursor.com/blog/cursor-3 | https://cursor.com/blog/faire

**Content:**

Cursor 3 (April 2026) redefined what an IDE is: **a workspace for supervising agents, not editing files.**

**Key capabilities (as of August 2026):**

| Feature | What It Does |
|---|---|
| Agents Window | Run many agents in parallel across repos and environments |
| Cloud Agents | Isolated VMs with terminal, browser, desktop — work while offline |
| Composer 2.5 (May 2026) | Sustained long-running tasks, complex instruction following |
| Side Chats (July 2026) | Multiple parallel conversations with shared project context |
| Cloud Hooks (July 2026) | Automations triggered by cloud events |
| Self-hosted cloud agents | Run in your own infrastructure for compliance |
| Agent computer use | Agents control their own remote desktop |

**Enterprise adoption signal (Faire case study, May 2026):**
- 2,000+ autonomous agent runs per week
- Replaced in-house background agent system
- Use cases: Bug triage from Slack, CI failure fixes, code review routing
- "Cursor is now Faire's recommended platform for agentic development"

**Financial signal:**
- $500M ARR (2025)
- $10B valuation
- SpaceX bidding $60B for acquisition
- Over half of Fortune 500 adopted

**Cursor's plugin ecosystem (August 2026):**
- Gmail, Google Drive, Calendar, Docs, Sheets integration
- Direct access from coding agents — no context switching
- "Pull context, draft and update files, and manage your inbox and calendar without leaving Cursor"

**AI-DLC connection:** Cursor embodies the full Agentic SDLC in a single tool — spec (plan mode) → generate (cloud agents) → test (agent computer use) → deploy (PR output). The lifecycle is now a single-IDE experience.

**Facilitator Notes:**
- $60B acquisition bid is the attention-grabber. "This is how seriously the market takes AI-assisted development."
- Faire's 2,000 runs/week is a concrete enterprise example students can relate to.
- For teams evaluating tools: "Cursor if you want maximum flexibility and agent power. GitHub Copilot if you want platform integration. Kiro if you want spec-driven discipline."
- Time: 4 minutes

---

### [NEW AUG-2026] Slide: The AI Agent Observability Landscape — 66+ Tools and Counting
**Insert after:** [NEW AUG-2026] The "MLOps is Dead" Moment
**Source:** https://arize.com/blog/best-ai-observability-tools-for-autonomous-agents-in-2026/ | https://latitude.so/blog/ai-agent-observability-tools-comparison-2026

**Content:**

**The problem:** 66+ tools now claim to solve AI observability. Most were built for a simpler problem — logging individual LLM calls. Agent observability is fundamentally harder.

**Why agent observability ≠ LLM observability:**
```
LLM call:    Request → Response → Log latency, tokens, cost
Agent run:   Request → Plan → Tool call → Result → Think → Tool call → ... → Final output
             ↑ Each step needs: trace ID, span, eval, cost attribution, error handling
```

**The 2026 agent observability stack:**

| Layer | What to Monitor | Key Tools |
|---|---|---|
| Trace-level | Full agent session, branching paths | Arize AX, LangSmith, Langfuse |
| Span-level | Individual steps within a trace | Phoenix, Braintrust, Confident AI |
| Tool-level | Which tools called, success/failure rates | Helicone, Portkey |
| Cost-level | Token usage per session, per agent, per tool | Helicone, Braintrust |
| Quality-level | Output eval scores over time, drift | Confident AI, Latitude |
| Safety-level | Policy violations, hallucination rate | Galileo, Confident AI |

**Selection criteria (August 2026):**
1. Does it support multi-turn, multi-agent traces?
2. Can you attach evals to individual spans (not just final output)?
3. Does it detect anomalies in agent behaviour patterns?
4. Can you go from production trace → dataset → CI eval (closed loop)?
5. What's the instrumentation overhead on latency?

**Key insight (AIMResearch, July 2026):** "Tools offering deeper, step-level observability exhibited higher latency overhead, while lighter tracing approaches remained closer to baseline." — Choose depth vs. performance based on your use case.

**Facilitator Notes:**
- This extends the LLMOps Layer 4 (Observability) slide with agent-specific guidance.
- Don't try to cover all 66 tools. Focus on the 3-4 most relevant for your audience.
- For teams just starting: "Start with Langfuse (open-source, self-hosted) and add commercial tools as you scale."
- Time: 4 minutes

---

### [NEW AUG-2026] Slide: GPT-5.6 "Sol" and Claude Opus 5 — The August 2026 Model Landscape
**Insert after:** [NEW 2026] The AI Artifact Registry
**Source:** https://openai.com/index/gpt-5-6/ | https://support.claude.com/en/articles/12138966-release-notes

**Content:**

Two major model releases in the same week reshape what's possible in AI development:

**GPT-5.6 "Sol" (August 11, 2026):**
- SOTA across coding, knowledge work, cybersecurity, and science
- Outperforms previous frontier models with **fewer tokens at lower cost**
- Powers OpenAI Codex — the "fast and efficient" model optimised for agentic coding
- GPT-5.2-Codex variant: optimised for long-horizon work, context compaction, large refactors

**Claude Opus 5 (July 2026):**
- 1M token context window
- Near frontier intelligence of Claude Fable 5 at half the price
- Default model in Claude Code
- Dynamic workflows for large-scale problems
- Nested subagents for complex multi-step tasks
- Fast mode: 2.5× speed, now 3× cheaper than previous models

**What this means for AI-DLC:**
1. **Longer context = better spec understanding:** 1M tokens means entire codebases fit in context — specs + code + tests together
2. **Cheaper evals:** If models are cheaper, running eval suites in CI becomes more affordable
3. **Context compaction:** GPT-5.2-Codex explicitly optimises for maintaining coherence across long agent sessions
4. **Model routing becomes more complex:** With GPT-5.6, Claude Opus 5, and Gemini all offering different trade-offs, model selection is a first-order engineering decision

**The model router pattern (essential for FinOps):**
```
Incoming task → Classifier determines complexity →
  Simple → Cheap/fast model (Haiku, GPT-5-mini)
  Medium → Mid-tier (Sonnet, GPT-5.5)
  Complex → Frontier (Opus 5, GPT-5.6 Sol)
```

**Facilitator Notes:**
- Don't deep-dive on model capabilities — that's a different module. Focus on AI-DLC implications.
- The model router pattern connects directly to the FinOps slide.
- Key message: "Model choice is no longer set-and-forget. It's a dynamic routing decision in your pipeline."
- Time: 3 minutes

---

### [NEW AUG-2026] Slide: The Vibe Coding Maturity Model — Where Does Your Team Sit?
**Insert after:** [NEW 2026] Vibe Coding — The Spectrum from Exploration to Discipline
**Source:** https://vibecoding.app/blog/vibe-coding-complete-guide | https://www.augmentcode.com/guides/vibe-coding-vs-spec-driven-development

**Content:**

By August 2026, the vibe coding conversation has matured. It's no longer "good or bad" — it's "at which maturity level?"

**The Vibe Coding Maturity Model (VCMM):**

| Level | Name | Characteristics | Best For |
|---|---|---|---|
| 1 | Raw Vibe | Prompt-and-pray, no review, ship immediately | Personal projects, throwaway demos |
| 2 | Guided Vibe | Rules files (.cursorrules), structured prompts, manual testing | Prototypes, hackathons, MVPs |
| 3 | Validated Vibe | Research-Plan-Implement framework, test after every change, CI basics | Internal tools, low-risk features |
| 4 | Spec-Bounded | Spec first, agents execute, property-based tests, eval gates | Production features, team projects |
| 5 | Agentic Engineering | Full AI-DLC, automated governance, continuous eval, multi-agent coordination | Enterprise, regulated, critical systems |

**Real-world signals (August 2026):**
- 25% of Y Combinator W25 startups are **95% AI-generated code**
- Pieter Levels: shipped a $1M revenue game in 17 days (Level 2-3)
- Lovable: hit $100M ARR in 8 months helping non-coders build apps (Level 1-2)
- Enterprise adoption requires Level 4-5 minimum

**The Research-Plan-Implement framework (2026 best practice for Level 3+):**
1. **Research:** Have the AI explore the problem space, existing patterns, dependencies
2. **Plan:** Generate a structured plan before any code is written
3. **Implement:** Execute the plan with checkpoints
4. **Validate:** Test after every change, not just at the end

**AI-DLC mapping:** The maturity model maps directly to AI-DLC governance requirements:
- Levels 1-2: No AI-DLC needed (exploration, throwaway)
- Level 3: Lightweight AI-DLC (basic eval, manual gates)
- Level 4: Standard AI-DLC (spec-driven, automated eval gates)
- Level 5: Full AI-DLC (all 7 stages, multi-agent governance)

**Facilitator Notes:**
- Ask students: "Which level does your team operate at today? Which level should you be at?"
- Most enterprise students will say Level 2-3 and recognise they need Level 4-5.
- The YC stat (25% of startups at 95% AI-generated) is provocative — startups can accept Level 1-2 risk that enterprises cannot.
- Time: 4 minutes

---

### [NEW AUG-2026] Slide: Lab Update — Add Background Agents to Your Pipeline Design
**Insert after:** [NEW 2026] Lab Extension — Design Your AI-DLC Pipeline
**Source:** Synthesised from multiple August 2026 sources

**Content:**

**Lab Extension (5 additional minutes):**

Add a sixth section to the pipeline design lab:

**6. Background Agent Strategy**

Your customer support AI agent team now has access to background coding agents (GitHub Copilot, Cursor Cloud, or Kiro). Design your governance for agent-generated code:

a) **Which tasks can background agents handle unsupervised?**
   - [ ] Bug fixes from customer reports
   - [ ] Documentation updates
   - [ ] Test generation
   - [ ] Feature implementation from specs
   - [ ] Infrastructure changes
   - [ ] Other: _______

b) **What eval gates must pass before agent-generated PRs are merged?**
   - Gate 1: _______
   - Gate 2: _______
   - Gate 3: _______

c) **What's your escalation path when an agent can't complete a task?**
   - Timeout threshold: ___ minutes
   - Escalation to: _______
   - Fallback behaviour: _______

d) **How do you handle the "always-on" governance challenge?**
   - Agents running at 3am on a Sunday — who reviews?
   - Maximum autonomous changes before human review required: ___
   - Monitoring dashboard for background agent activity: Yes / No / Planned

**Facilitator Notes:**
- This extension makes the lab current with August 2026 reality.
- Students who haven't used background agents will benefit from thinking through the governance implications.
- Time: 5 minutes added to existing 20-minute lab (total: 25 minutes)

---

## C) UPDATED CASE STUDIES

### Case Study 1: Faire — 2,000 Agent Runs Per Week (May 2026)
**Source:** https://cursor.com/blog/faire

Faire (wholesale marketplace) replaced their in-house background agent system with Cursor Cloud Agents:
- **2,000+ autonomous agent runs per week**
- **Use cases:** Bug report triage from Slack, CI failure fixes, code review routing
- **Result:** Cursor is now Faire's "recommended platform for agentic development"
- **AI-DLC relevance:** Shows a real enterprise embedding background agents across multiple SDLC stages simultaneously

### Case Study 2: Claude Code Auto-Mode at Scale (August 2026)
**Source:** https://claude.com/blog/auto-mode-default-in-claude-code

Anthropic's own internal data on classifier-gated autonomy:
- **89% alignment** between classifier decisions and what humans would have approved
- **11% conservative miss rate** — classifier flags things humans would allow (safe direction)
- Moving from "opt-in automation" to "opt-out manual" as the default
- **AI-DLC relevance:** Shows how the governance layer of AI-DLC can be partially automated — but requires the right tooling and thresholds

### Case Study 3: Singapore Universities Adopt Kiro for Workforce-Ready Skills (May 2026)
**Source:** https://press.aboutamazon.com/aws/2026/5/aws-brings-professional-grade-ai-developer-tool-kiro-to-singapore-ihls-to-build-workforce-ready-software-skills

AWS partnered with Singapore Institutes of Higher Learning to teach spec-driven development:
- Teaching students to "specify up-front their intent and requirements" before AI generates code
- Result: "production-ready applications with built-in documentation and automated tests — something a professional team can maintain"
- **AI-DLC relevance:** Shows AI-DLC being taught at educational level — the next generation of developers will expect spec-driven workflows

---

## D) UPDATED TOOLS & RESOURCES

### New Tools (June–August 2026)

| Tool | Category | What's New | URL |
|---|---|---|---|
| **Kiro IDE 1.0** | Spec-driven IDE | GA with parallel agents, property-based testing, hooks | kiro.dev |
| **OpenAI Codex (GA)** | Multi-surface agent | Terminal, IDE, web, mobile — 40T tokens served | openai.com/codex |
| **Grok Bot** | Always-on agents | SpaceXAI + Cursor, persistent memory, multi-app | Via Cursor |
| **GitHub Copilot App** | Agent-native desktop | My Work view, background automations dashboard | github.com/features/copilot |
| **Claude Code auto-mode** | Classifier-gated autonomy | Default Aug 14 for Pro/Max/Team | code.claude.com |
| **Claude Opus 5** | Frontier model | 1M context, dynamic workflows, nested subagents | anthropic.com |
| **GPT-5.6 "Sol"** | Frontier model | SOTA, cheaper, fewer tokens | openai.com |
| **Cursor 3.11** | IDE update | Side Chats, Conversation Search, Cloud Hooks | cursor.com |
| **Red Hat InstructLab CLI** | CI/CD eval tool | Machine-parseable eval output for pipelines | developers.redhat.com |
| **Microsoft Foundry** | Agent CI/CD | Reference architecture for agent lifecycle management | github.com/foundry-agents-lifecycle |

### New Frameworks & References

| Resource | Type | Relevance |
|---|---|---|
| Forbes "MLOps is Dead" (Aug 10) | Industry analysis | Validates AgentOps framing |
| awesome-agentops-landscape (GitHub) | Curated tool list | 66+ tools catalogued with feature comparison |
| Sourcegraph Context Engineering Guide | Technical guide | Definitive context engineering architecture |
| Microsoft "CI/CD for AI Agents on Foundry" | Reference architecture | Production-ready agent CI/CD patterns |
| GetAutonoma "Two-Lane CI Pipeline" | Best practice | Fast/slow lane eval pattern |
| IBM "Vibe Coding Security Risks" (July 2026) | Security analysis | Distinguishes AI security from traditional security |

---

## E) FARIS HADDAD CONTENT INTEGRATION

**Search results:** No specific LinkedIn posts, blog articles, or Medium posts by Faris Haddad were found in the public web search results for June-August 2026.

**Recommendation:** If Faris has posted content on LinkedIn or other platforms during this period related to:
- AI-DLC or agentic SDLC
- Spec-driven development experiences
- Context engineering practices
- AI coding tool evaluations

These can be integrated as facilitator references:
- *"As I discussed in my recent [LinkedIn post / article] on [topic]..."*
- Insert as personal experience/opinion within relevant slides

**Note:** Faris's association with the Elvtr AI Solutions Architecture course (found at uk.elvtr.com/course/ai-solutions-architecture) suggests relevant content may exist on that platform. If Faris has course materials, interviews, or promotional content from Elvtr during this period, it could reinforce the AI-DLC module's credibility with students.

**Action item:** Check Faris's LinkedIn directly for any posts from June-August 2026 that can be cited.

---

## F) FACILITATOR REFRESH BRIEF

### 🔥 Top 3 Things That Changed Since July 2026

1. **Claude Code auto-mode default (Aug 14):** The biggest governance shift — human approval is no longer the default in the most popular agentic coding tool. Frame as: "The industry is moving from human-gates to classifier-gates. Your AI-DLC governance framework must adapt."

2. **OpenAI Codex GA + Grok Bot (Aug 11):** The "always-on agent" category crystallised in a single week. Three major players (OpenAI, Anthropic, SpaceXAI/Cursor) all announced background/persistent agents within days. Frame as: "Background agents are no longer experimental — they're the new normal."

3. **46% code is AI-generated + Forbes "MLOps is Dead":** The statistics and industry narrative both crossed a tipping point. Frame as: "We're past the early-adopter phase. The question isn't whether to use AI in your lifecycle — it's how to govern the AI that's already there."

### 📣 What to Emphasise as "Breaking News"

- **"As of two days ago (Aug 14), Claude Code stopped asking developers for permission by default."** — This happened during your students' preparation for this class. It's immediate.
- **"OpenAI Codex went GA on Aug 11 — same day as Grok Bot, same day as GPT-5.6."** — The pace of change is extraordinary. Three major announcements in one day.
- **"Amazon is sunsetting Q Developer and going all-in on spec-driven development with Kiro."** — AWS made a strategic bet that specs > prompts for enterprise development.

### 🛠️ Demos & Tools to Set Up Fresh

1. **Claude Code auto-mode demo:** Show the classifier in action — what it approves vs. what it escalates. (Requires Claude Pro/Max account after Aug 14)
2. **Kiro IDE quick demo:** Show the prompt → requirements → architecture → parallel agents → property-based tests pipeline. (Free at kiro.dev)
3. **GitHub Copilot coding agent:** Assign an issue and show the async PR generation. (Requires GitHub Enterprise or Copilot Business)
4. **Cursor Cloud Agents:** Send a plan to the cloud and show it working in the background. (Requires Cursor Pro subscription)
5. **Context engineering file:** Show a CLAUDE.md or .cursorrules file and demonstrate how it changes agent behaviour (free, immediate)

### ⏱️ Updated Timing Guidance

With August 2026 content added:
- **60-minute version:** Use 3 new slides (Auto-Mode Shift, Background Agents, Context Engineering) + updated stats. Replace older content as needed.
- **90-minute version:** Add all new slides + updated lab extension. This is the recommended format.
- **120-minute version (new option):** Full deep-dive including AgentOps landscape, model comparison, and full 25-minute lab. Ideal for technical audiences who want tool selection guidance.

### 📋 Updated Pre-Reading Recommendation

Replace or supplement July's pre-reading with:
- "Auto mode is now the default in Claude Code" (Anthropic blog, Aug 7, 2026) — 5 minute read
- "Context Engineering: A Practical Guide for AI Agents" (Sourcegraph, April 2026) — 15 minute read

Both set up the key tension: more agent autonomy requires better context engineering and governance.

---

*Module 06 August 2026 Refresh — AI & Agentic AI Training Programme — 12 August 2026*
