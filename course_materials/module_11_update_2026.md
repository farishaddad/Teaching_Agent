# Module 11 — Introduction to AI Agents & Agentic Patterns
## [2026 UPDATE] Gap Analysis + New Slides + Facilitator Notes

---

## GAP ANALYSIS — What's Missing or Outdated

1. **❌ "Agent Anatomy" framing is outdated.** The field has converged on the term **"agent harness"** — the complete software infrastructure wrapping an LLM (orchestration loop, tools, memory, context management, guardrails, verification). The harness IS the agent minus the model. Anthropic, OpenAI, LangChain, and Databricks all use this framing as of mid-2026.

2. **❌ Context engineering is missing entirely.** The module covers prompt engineering but not the discipline that has superseded it for agentic systems. Context engineering (what goes INTO the context window, when, and in what order) is now considered the #1 skill for agent builders. Endorsed by Tobi Lütke (Shopify CEO) and Andrej Karpathy since mid-2025.

3. **❌ Computer-use agents are absent.** Anthropic Claude Computer Use (production March 2026), OpenAI Operator/CUA, and Gemini all offer screen-based agent interaction — a fundamentally new modality not covered in the original module.

4. **❌ Coding agents as the dominant agentic application are missing.** Claude Code (Anthropic), OpenAI Codex (2026 version), Cursor — these are the most widely deployed agentic systems and represent the best public case studies of harness engineering in practice.

5. **❌ Agent benchmarks have matured.** SWE-bench Verified now at 80-95% (Claude Fable 5 at 95%), TerminalBench 2.0, WebArena, AgentBench v3.0, OSWorld, Tau-Bench — none are covered. OpenAI published a post in June 2026 arguing SWE-bench Verified no longer measures frontier capabilities.

6. **❌ Managed/hosted agent infrastructure is missing.** Anthropic Managed Agents (launched April 2026), OpenAI Codex cloud sandboxes — these represent "harness-as-a-service" and change how teams deploy agents.

7. **❌ The three-level engineering hierarchy is missing.** Prompt engineering → Context engineering → Harness engineering — this is the defining progression that students need to understand their own skill development path.

8. **❌ Design patterns have expanded from 4 to 6+ canonical patterns.** Andrew Ng's original 4 (Reflection, Tool Use, Planning, Multi-Agent Collaboration) have been extended with Orchestrator-Worker and Evaluator-Optimizer. A 2026 paper on arxiv catalogues 21 patterns in 5 families.

9. **❌ Verification loops and doom loop prevention are missing.** Production agents require verification (rules-based, visual, LLM-as-judge) and circuit breakers to prevent infinite loops — critical operational patterns not covered.

10. **❌ The Von Neumann analogy is absent.** Beren Millidge's "Scaffolded LLMs as Natural Language Computers" framing (LLM=CPU, context window=RAM, external DB=disk, tools=device drivers, harness=OS) is now the standard mental model used in the field.

---

## NEW SLIDES

---

### [NEW 2026] Slide: The Agent Harness — A New Mental Model
**Insert after:** Agent Anatomy (LLM brain, tools, memory, environment)
**Format:** Concept explanation

#### The Agent ≠ The Model. The Agent = The Harness + The Model.

The field has converged on a critical distinction:

| Term | Meaning |
|------|---------|
| **The Agent** | The emergent behaviour: goal-directed, tool-using, self-correcting entity |
| **The Harness** | The complete software infrastructure producing that behaviour |
| **The Model** | The LLM providing intelligence (one component inside the harness) |

> *"If you're not the model, you're the harness."* — Vivek Trivedy, LangChain

**Why this matters:** When someone says "I built an agent," they mean they built a harness and pointed it at a model. LangChain proved this in early 2026: same model, same weights, harness rebuilt → jumped from outside top 30 to **rank 5 on TerminalBench 2.0.**

A separate research project hit **76.4% pass rate** by having an LLM optimise the infrastructure itself — not the model weights.

**The binding constraint is the harness, not the model.**

**Facilitator Notes:**
- 🎤 This is the most important conceptual reframe in the module. Spend time here. Ask: "When you hear 'our agent doesn't work,' what component do you now suspect first?"
- Common student question: "So should I spend less time choosing models?" → Answer: Model choice matters, but after a capability threshold, harness engineering has more leverage
- Time: 5 minutes
- For beginners: use the analogy "the model is the brain, the harness is the body + nervous system + senses"

---

### [NEW 2026] Slide: The Von Neumann Analogy
**Insert after:** The Agent Harness slide
**Format:** Concept explanation / comparison table

#### LLMs as Natural Language Computers

Beren Millidge's framing (2023, now industry-standard):

```
┌─────────────────────────────────────────┐
│            AGENT HARNESS                │
│  ┌─────────────────────────────────┐    │
│  │     CONTEXT WINDOW = RAM        │    │
│  │  (fast but limited capacity)    │    │
│  │  ┌─────────────────────────┐    │    │
│  │  │    LLM = CPU            │    │    │
│  │  │  (processes tokens)     │    │    │
│  │  └─────────────────────────┘    │    │
│  └─────────────────────────────────┘    │
│  External DB = DISK (large but slow)    │
│  Tools = DEVICE DRIVERS                 │
│  Harness = OPERATING SYSTEM             │
└─────────────────────────────────────────┘
```

| Computer Component | Agent Equivalent | Key Property |
|---|---|---|
| CPU | LLM | Processes information |
| RAM | Context window | Fast, limited capacity |
| Disk | Vector DB / long-term memory | Large, higher latency |
| Device drivers | Tool integrations | Interface to external systems |
| Operating System | The harness | Orchestrates everything |

> *"We have reinvented the Von Neumann architecture because it's a natural abstraction for any computing system."* — Beren Millidge

**Facilitator Notes:**
- 🎤 This clicks instantly for anyone with systems background. For non-engineers, focus on RAM vs Disk trade-off (context window is fast but fills up → need to be strategic about what goes in)
- Common question: "Does this mean bigger context windows solve everything?" → No, because of context rot (30%+ performance degradation in mid-window positions)
- Time: 3 minutes

---

### [NEW 2026] Slide: Three Levels of Engineering
**Insert after:** Von Neumann Analogy
**Format:** Concept explanation / hierarchy diagram

#### The Engineering Skill Progression for Agent Builders

```
┌─────────────────────────────────────────────┐
│           HARNESS ENGINEERING               │
│  The complete system: tool orchestration,   │
│  state persistence, error recovery,         │
│  verification loops, safety enforcement,    │
│  lifecycle management                       │
│  ┌─────────────────────────────────────┐    │
│  │       CONTEXT ENGINEERING           │    │
│  │  What the model SEES and when —     │    │
│  │  the most underrated skill of 2026  │    │
│  │  ┌───────────────────────────────┐  │    │
│  │  │    PROMPT ENGINEERING         │  │    │
│  │  │  Crafting the instructions    │  │    │
│  │  │  the model receives           │  │    │
│  │  └───────────────────────────────┘  │    │
│  └─────────────────────────────────────┘    │
└─────────────────────────────────────────────┘
```

| Level | Focus | Skill |
|---|---|---|
| **Prompt Engineering** | The instructions the model receives | Crafting clear, effective prompts |
| **Context Engineering** | What the model sees, when, and in what order | Managing the context window strategically |
| **Harness Engineering** | The complete system infrastructure | Building reliable agent systems |

> *"2024 was prompt engineering. 2025 was context engineering. 2026 is harness engineering."* — Sezen Erdem

**Key insight:** Most AI training teaches Level 1. Production agent work happens at Level 3. This course takes you through all three.

**Facilitator Notes:**
- 🎤 Frame this as "here's your personal skill development roadmap." Module 7 covered Level 1. This module introduces Levels 2 and 3. Modules 12-13 go deeper.
- Ask students: "What level are you currently at? What would it take to move up?"
- Time: 4 minutes

---

### [NEW 2026] Slide: Context Engineering — The #1 Skill for Agent Builders
**Insert after:** Three Levels of Engineering
**Format:** Concept explanation with examples

#### What Is Context Engineering?

**Definition (Andrej Karpathy):** *"The LLM is the CPU and the context window is RAM. Context engineering is the art of filling that RAM with exactly the right information for the next step."*

**Definition (Tobi Lütke, Shopify CEO):** *"Context engineering is the delicate art and science of filling the context window with just the right information for the next step."*

#### Prompt Engineering vs Context Engineering

| Dimension | Prompt Engineering | Context Engineering |
|---|---|---|
| **Focus** | The instruction/query itself | The entire input payload |
| **Scope** | Single turn | Across turns, tools, and memory |
| **What you control** | Wording, structure, examples | What goes in, what stays out, ordering |
| **Value** | ~60% of potential quality | The remaining ~40% that separates demos from deployed systems |
| **For agents specifically** | "What should the model do?" | "What should the model know before deciding what to do?" |

#### Why This Matters for Agents

Your agent is not failing at its steps — it is failing *between* them because the wrong information is present at each node.

**Context engineering strategies for agents:**
- **Compaction:** Summarise old context to preserve key decisions
- **Just-in-time retrieval:** Load data only when needed (not pre-loaded)
- **Observation masking:** Hide old tool outputs, keep tool calls visible
- **Position awareness:** Key info at beginning/end of window (Lost in the Middle effect)
- **Sub-agent delegation:** Each sub-agent returns only condensed summaries

**Facilitator Notes:**
- 🎤 This is the single most important new concept since the course was first designed. Make it concrete: "Your agent has 200K tokens of context. A codebase is 500K. What goes in? What order? What gets evicted?"
- Common question: "Isn't this just RAG?" → RAG is one implementation of context engineering for retrieval. Context engineering is the broader discipline.
- Time: 6 minutes

---

### [NEW 2026] Slide: The 12 Components of a Production Agent Harness
**Insert after:** Context Engineering slide
**Format:** Reference table / framework

#### What's Inside a Real Agent Harness?

Synthesised from Anthropic, OpenAI, LangChain, and Databricks documentation (2026):

| # | Component | What It Does |
|---|---|---|
| 1 | **Orchestration Loop** | The TAO cycle (Thought-Action-Observation). The heartbeat. |
| 2 | **Tools** | Schema-defined capabilities: file ops, web, code execution, APIs |
| 3 | **Memory** | Short-term (session) + long-term (cross-session) persistence |
| 4 | **Context Management** | What goes in the window, compaction, eviction policies |
| 5 | **Prompt Construction** | Hierarchical assembly of system prompt + schemas + history |
| 6 | **Output Parsing** | Tool call detection, structured output validation, termination |
| 7 | **State Management** | Conversation persistence, checkpointing, restart safety |
| 8 | **Error Handling** | Classification (transient/LLM-recoverable/user-fixable/unexpected) |
| 9 | **Guardrails & Safety** | Input/output/tool guardrails, permission enforcement, tripwires |
| 10 | **Verification Loops** | Rules-based, visual, LLM-as-judge (2-3× quality improvement) |
| 11 | **Sub-agent Orchestration** | Fork, teammate, worktree execution models |
| 12 | **Lifecycle Management** | Startup, warm-up, graceful shutdown, restart recovery |

**Key insight:** A basic scaffold achieves 23% on SWE-bench. An optimised 250-turn scaffold on the same model achieves 45%+. That's a 22-point swing from harness engineering alone.

**Facilitator Notes:**
- 🎤 Don't rush through this table — this IS the curriculum map for Modules 11-13. Point out which components are covered in which module.
- For beginners: "You don't need to build all 12 on day one. Start with 1 (loop) + 2 (tools) + 5 (prompt construction). Add complexity as you need reliability."
- Time: 5 minutes

---

### [NEW 2026] Slide: Agentic Design Patterns — The 2026 Expanded Catalog
**Insert after:** Core Agentic Patterns (ReAct, Plan-and-Execute, Reflection, MRKL)
**Format:** Comparison table

#### From 4 to 6+ Canonical Patterns

Andrew Ng's original 4 patterns (2024) have been extended. The 2026 practitioner consensus recognises 6 core patterns:

| Pattern | What It Does | When to Use | Example |
|---|---|---|---|
| **Reflection** | Agent critiques its own output and iterates | Quality-critical tasks; writing, code review | Code agent runs tests after editing, fixes failures |
| **Tool Use** | Agent calls external tools/APIs to gather info or take action | Any task requiring real-world interaction | Agent searches web, reads files, calls APIs |
| **Planning** | Agent decomposes complex task into sub-steps before executing | Multi-step tasks with dependencies | "Refactor auth module" → plan 6 steps → execute sequentially |
| **Multi-Agent Collaboration** | Multiple specialised agents coordinate | Complex tasks requiring diverse expertise | Researcher + Coder + Reviewer work together |
| **Orchestrator-Worker** | Central agent delegates to workers, aggregates results | Parallelisable work; batch processing | Manager assigns 10 files to 10 worker agents |
| **Evaluator-Optimizer** | One agent generates, another evaluates, loop until quality threshold | Optimization tasks; iterative improvement | Writer drafts → Critic scores → Writer revises |

**2026 addition — the paper perspective:** A January 2026 arxiv paper (2601.19752) catalogues agentic design patterns formally. Taskade's field guide identifies 21 patterns in 5 families (Core, Advanced, System, Optimization, Strategic).

**Decision framework:**
- Single step? → Just prompt
- Multiple steps, one skill? → Tool Use + Reflection
- Multiple steps, needs plan? → Planning
- Diverse expertise needed? → Multi-Agent
- Parallelisable? → Orchestrator-Worker
- Iterative quality? → Evaluator-Optimizer

**Facilitator Notes:**
- 🎤 The original 4 patterns from Andrew Ng are still valid and foundational. The 2026 update adds Orchestrator-Worker and Evaluator-Optimizer as production patterns that emerged from real deployments.
- Activity idea: Give students a use case and have them argue which pattern(s) apply
- Time: 5 minutes

---

### [NEW 2026] Slide: Computer-Use Agents — A New Modality
**Insert after:** Agentic Design Patterns
**Format:** Concept explanation + comparison table

#### Agents That See and Click

As of mid-2026, three major labs offer production APIs for screen-based agent interaction:

| Platform | Product | How It Works | Launched |
|---|---|---|---|
| **Anthropic** | Claude Computer Use | Screenshot + mouse/keyboard tool; portable across VMs, containers, remote desktops | Oct 2024 (beta), March 2026 (production) |
| **OpenAI** | Operator / CUA | GPT-4o vision + RL-trained GUI interaction; reinforcement learning on GUIs | Jan 2025 (beta), 2026 (production) |
| **Google** | Gemini agent mode | Multimodal vision + action capabilities | 2025-2026 |

#### How Computer-Use Agents Work

```
1. SCREENSHOT → Agent "sees" the current screen state
2. REASON → Agent decides what action to take (click, type, scroll)
3. ACT → Agent sends mouse/keyboard commands
4. VERIFY → Agent takes another screenshot to confirm result
5. REPEAT → Until task is complete
```

#### Use Cases in Production
- Form filling and data entry across legacy systems
- Testing UI workflows (QA automation without writing test scripts)
- Cross-application workflows that have no API
- "Last mile" automation for processes that resist API integration

#### Limitations (be honest with students)
- Slower than API-based automation (each step requires a screenshot round-trip)
- Brittle to UI changes (layout changes break workflows)
- Security implications (agent has screen access → sees everything)
- Not a replacement for well-designed APIs — a fallback for when APIs don't exist

**Facilitator Notes:**
- 🎤 This is genuinely new — none of this existed 18 months ago. Frame it as "the agent can now use ANY software the way a human would, with the same limitations humans have"
- Common question: "Should I build all my agents as computer-use agents?" → No! API-based tool use is faster, cheaper, and more reliable. Computer use is for the last mile where APIs don't exist.
- Demo suggestion: Show a 30-second video of Claude Computer Use navigating a web form
- Time: 5 minutes

---

### [NEW 2026] Slide: Coding Agents — The Dominant Agentic Application
**Insert after:** Computer-Use Agents
**Format:** Comparison table + case study

#### The State of Coding Agents (Mid-2026)

Coding agents are the most mature, widely deployed, and well-benchmarked category of agentic AI:

| Agent | Model | Architecture | Key Strength |
|---|---|---|---|
| **Claude Code** | Claude Opus 4.8 | Terminal-native, local; MCP support; multi-agent | Multi-file refactoring; 1M token context on large codebases; SWE-bench Pro 64.3% |
| **OpenAI Codex** (2026) | GPT-5.5 | Cloud-native, async sandboxes; multi-surface | Parallel task execution; browser/computer use; ChatGPT integration |
| **Cursor** | Multiple (Claude, GPT) | IDE-native; inline completions + agent mode | Tightest editor integration; works within existing workflow |

#### What Makes Coding Agents Excellent Case Studies

They demonstrate every harness component in action:
- **Orchestration loop:** Read code → plan change → edit → run tests → fix failures → verify
- **Tools:** File read/write, terminal execution, search, web browsing
- **Context management:** How do you fit a 500K-token codebase into 200K context?
- **Verification:** Automated tests as verification loops
- **Error handling:** Test failures → retry with different approach
- **Sub-agents:** Parallel feature development using git worktrees

#### Production Data Points
- Claude Code: Gather-Act-Verify cycle; treats memory as "hint" and verifies against actual state
- Codex: Runs in isolated cloud sandboxes; tasks can span hours to weeks
- SWE-bench Verified: Top agents now at 80-95% (Claude Fable 5 at 95.0%)
- OpenAI argues (June 2026) that SWE-bench Verified no longer measures frontier capabilities

**Facilitator Notes:**
- 🎤 If students have used any of these tools, ask them to share. Many will have. Use their experience to make the "harness engineering" concept concrete.
- Key point: These agents use the SAME models as chatbots — the difference is entirely in the harness engineering
- Time: 5 minutes
- ⚡ ADVANCED: Discussion on SWE-bench contamination concerns and what that means for benchmarking

---

### [NEW 2026] Slide: Agent Benchmarks — How We Measure Agentic Capability
**Insert after:** Coding Agents
**Format:** Reference table

#### The Agent Benchmark Landscape (Mid-2026)

Traditional LLM benchmarks (MMLU, HumanEval) don't measure what matters for agents. Agent benchmarks simulate real-world scenarios requiring multi-step action:

| Benchmark | What It Measures | Top Score (Mid-2026) | Notes |
|---|---|---|---|
| **SWE-bench Verified** | Fix real GitHub issues in real repos | 95.0% (Claude Fable 5) | OpenAI argues it's now saturated; contamination concerns |
| **SWE-bench Pro** | Harder, less-contaminated version | 64.3% (Claude Code) | Better proxy for real-world coding capability |
| **TerminalBench 2.0** | End-to-end terminal task completion | 82.7% (GPT-5.5) | LangChain went from outside top 30 → rank 5 by changing only harness |
| **WebArena** | Web navigation and task completion | ~22.5% | Still very hard; requires multi-step web interaction |
| **AgentBench v3.0** | Multi-domain agent evaluation | — | 8 environments: web, DB, code, OS, games |
| **OSWorld** | Desktop/OS task completion | — | Cross-platform (Mac, Windows, Linux) |
| **Tau-Bench** | Tool-augmented understanding | — | Measures tool selection and orchestration |

#### Key Insight: The Harness Effect on Benchmarks

Same model + different harness = wildly different benchmark scores. This is the clearest empirical evidence that harness engineering matters:

- Basic scaffold on SWE-bench: **23%**
- Optimised 250-turn scaffold, same model: **45%+**
- **22-point swing from harness engineering alone**

**Facilitator Notes:**
- 🎤 The benchmark landscape is moving fast. Don't memorise numbers — understand what each benchmark tests and why the harness effect is so large
- Common question: "Which benchmark should I use for my agents?" → Depends on domain. For code: SWE-bench Pro. For web: WebArena. For general: AgentBench.
- Time: 4 minutes
- ⚡ ADVANCED: Discuss contamination concerns (arxiv 2512.10218 — models 6× better at finding edited files in SWE-bench vs novel benchmarks)

---

### [NEW 2026] Slide: Managed Agent Platforms — Harness-as-a-Service
**Insert after:** Agent Benchmarks
**Format:** Concept explanation + comparison

#### The Rise of Managed Agent Infrastructure

Instead of building your own agent loop, tool execution, sandbox, and persistence, cloud platforms now offer this as a managed service:

| Platform | Product | What It Manages | Launched |
|---|---|---|---|
| **Anthropic** | Claude Managed Agents | Agent loop + tool execution + sandbox container + state persistence + multi-agent coordination | April 8, 2026 (public beta) |
| **OpenAI** | Codex Cloud Sandboxes | Isolated execution environments + async task management + multi-surface delivery | 2026 |
| **AWS** | Bedrock Agents | Orchestration + knowledge bases + action groups + guardrails + session management | 2023, major updates 2025-2026 |

#### Anthropic Managed Agents (the newest entrant)

> *"Decoupling the brain from the hands."* — Anthropic Engineering Blog

Key features:
- **Long-running sessions:** Agents operate autonomously for hours
- **Multi-agent coordination:** Agents can spin up and direct other agents
- **Managed infrastructure:** REST API bundles loop + tools + sandbox + state
- **Progress persistence:** Sessions survive disconnections
- **Simple integration:** `managed-agents-2026-04-01` beta header in API

**The trade-off:**
- ✅ 10× faster to production (no infrastructure to build)
- ✅ Managed security, scaling, and reliability
- ❌ Less customisation of the harness
- ❌ Vendor lock-in to a specific provider's agent architecture
- ❌ Cost implications at scale

**Decision framework:**
- Prototyping? → Managed agents
- Production with standard patterns? → Managed agents
- Novel architectures or extreme customisation? → Build your own harness
- Multi-model or multi-provider? → Build your own harness

**Facilitator Notes:**
- 🎤 Frame this as "the cloud moment for agents" — just as EC2 meant you don't build your own data centre, managed agents mean you don't build your own orchestration loop
- Common question: "Should I still learn to build a harness if managed options exist?" → Yes! Understanding the harness is how you debug, evaluate, and evolve managed agents. Same as understanding Linux even if you use managed Kubernetes.
- Time: 5 minutes

---

### [NEW 2026] Slide: Verification Loops — The Quality Multiplier
**Insert after:** 12 Components table
**Format:** Concept explanation with examples

#### Why Verification Is the Highest-Leverage Harness Component

> *Giving the model a way to verify its own work improves quality by 2-3×.* — Boris Cherny, creator of Claude Code

#### Three Verification Approaches

| Approach | How It Works | Best For | Example |
|---|---|---|---|
| **Rules-based** | Automated checks: tests, linters, type checkers | Code, data validation, format compliance | Run `pytest` after every code edit |
| **Visual** | Screenshot comparison via vision model | UI tasks, design compliance | Playwright screenshot → "does this match the mockup?" |
| **LLM-as-judge** | Separate model evaluates output quality | Creative tasks, quality assessment | Critic agent rates response on 5 criteria |

#### The Gather-Act-Verify Cycle (Claude Code Pattern)

```
GATHER → Read code, search files, understand context
  ↓
ACT → Edit files, run commands
  ↓
VERIFY → Run tests, check output, validate result
  ↓
(If verification fails → loop back to GATHER with error context)
```

#### Why 99% Per-Step Isn't Enough

A 10-step process with 99% per-step success has only **~90.4% end-to-end success**. Errors compound exponentially. Verification loops catch errors early before they propagate.

**Facilitator Notes:**
- 🎤 This is counter-intuitive: "Why verify when the model is already smart?" Because even a 99% success rate compounds to 90% over 10 steps. Verification is cheap insurance.
- Ask students: "What verification loops exist in your current development process?" → Tests, code review, QA. Agents need the same thing.
- Time: 4 minutes

---

### [NEW 2026] Slide: Doom Loop Prevention & Circuit Breakers
**Insert after:** Verification Loops
**Format:** Concept explanation + patterns

#### What Is a Doom Loop?

An agent stuck in an infinite retry cycle — making the same mistake, getting the same error, retrying the same approach. Burns tokens, wastes time, never converges.

#### Prevention Strategies

| Strategy | Implementation | Example |
|---|---|---|
| **Turn limits** | Hard cap on loop iterations | Max 25 turns per task |
| **Token budget** | Maximum tokens spent before escalation | 100K token budget per session |
| **Retry caps** | Max 2 retries per error type (Stripe pattern) | Same error 3× → stop and escalate |
| **Loop detection** | Detect repeated identical tool calls | Hash last 3 tool calls; if identical → break |
| **Reasoning budget** | Track and cap extended thinking time | Limit "thinking" tokens per turn |
| **Escalation to human** | Human-in-the-loop as circuit breaker | After 3 failures → notify user for guidance |

#### Error Classification (LangGraph Pattern)

| Error Type | Response |
|---|---|
| **Transient** | Retry with exponential backoff |
| **LLM-recoverable** | Return error as tool message; model adjusts approach |
| **User-fixable** | Interrupt for human input |
| **Unexpected** | Log, notify, halt gracefully |

**Facilitator Notes:**
- 🎤 Every student who has built an agent has hit a doom loop. Ask: "Who has seen their agent burn $5 doing the same thing over and over?" Get stories. Then show these patterns as the fix.
- Key production insight: Stripe caps retry attempts at 2. Not 5. Not 10. Two. Then escalate.
- Time: 3 minutes
- ⚡ ADVANCED: Discuss reasoning budget management — how to cap extended thinking tokens per turn

---

### [NEW 2026] Slide: The Agentic Maturity Ladder — 2026 Updated Version
**Insert after:** Doom Loop Prevention (or update existing maturity ladder)
**Format:** Updated framework

#### From Chatbot to Autonomous System — The 2026 Ladder

| Level | Name | Characteristics | Example |
|---|---|---|---|
| 0 | **Chat** | Single-turn Q&A; no tools, no memory | ChatGPT basic conversation |
| 1 | **Tool-augmented** | Can call tools in response to queries; single turn | RAG chatbot; function-calling |
| 2 | **Loop agent** | Multi-turn orchestration loop; plans and executes | ReAct agent that retries on failure |
| 3 | **Verified agent** | Adds verification loops; self-corrects | Coding agent that runs tests and fixes |
| 4 | **Managed agent** | Persists across sessions; managed infrastructure | Claude Managed Agents; Bedrock Agents |
| 5 | **Multi-agent system** | Multiple agents coordinate; specialisation + delegation | Orchestrator → researchers + coders + reviewers |
| 6 | **Autonomous system** | Self-improving; monitors own performance; minimal human oversight | Production coding agent improving its own harness |

**Where most enterprises are today (mid-2026):**
- Most deployed systems: Level 1-2
- Cutting edge production: Level 3-4
- Research/experimental: Level 5-6

**Your career opportunity:** Levels 3-5 have the most demand and the fewest qualified practitioners.

**Facilitator Notes:**
- 🎤 Ask students to self-assess: "What level are the AI systems at your organisation?" Most will say 1-2. Frame the course as taking them to level 3-5 capability.
- This replaces/extends the original "agentic maturity ladder" slide with 2026 terminology and examples
- Time: 4 minutes

---

### [NEW 2026] Slide: Production Case Study — How Claude Code's Harness Works
**Insert after:** Agentic Maturity Ladder
**Format:** Case study / walkthrough

#### Claude Code: The Most Documented Production Harness

Anthropic has published extensive documentation of Claude Code's harness, making it the best public case study available:

**Architecture:**
```
┌──────────────────────────────────────────────┐
│  CLAUDE CODE HARNESS                         │
│                                              │
│  Orchestration: "Dumb loop" — all            │
│  intelligence lives in the model             │
│                                              │
│  Cycle: GATHER → ACT → VERIFY → REPEAT      │
│                                              │
│  Tools (6 categories):                       │
│  • File operations (read, write, search)     │
│  • Search (grep, glob, head, tail)           │
│  • Execution (terminal commands)             │
│  • Web access (documentation lookup)         │
│  • Code intelligence (LSP integration)       │
│  • Sub-agent spawning (Fork, Teammate,       │
│    Worktree models)                          │
│                                              │
│  Memory:                                     │
│  • Tier 1: Lightweight index (~150 chars)    │
│  • Tier 2: Detailed topic files (on-demand)  │
│  • Tier 3: Raw transcripts (search-only)     │
│                                              │
│  Context Management:                         │
│  • Preserves architectural decisions         │
│  • Discards redundant tool outputs           │
│  • JIT retrieval (grep/glob, not full load)  │
│                                              │
│  Verification:                               │
│  • Automated tests after every edit          │
│  • "Treat memory as hint, verify against     │
│    actual state before acting"               │
│                                              │
│  Permission Model:                           │
│  • ~40 discrete tool capabilities gated      │
│  • Three stages: trust establishment →       │
│    permission check → explicit confirmation  │
└──────────────────────────────────────────────┘
```

**Key design principles:**
1. The runtime is a "dumb loop" — complexity lives in model prompting, not loop logic
2. Memory is treated as a *hint* — always verify against actual state before acting
3. Context management via grep/glob rather than loading full files
4. Sub-agents return only 1,000-2,000 token condensed summaries

**Facilitator Notes:**
- 🎤 This is the most complete public example of production harness engineering available. Use it as the "worked example" that makes all 12 components concrete.
- Ask: "Which of the 12 components can you identify in this architecture?"
- For advanced students: Discuss the "dumb loop" philosophy — why does Anthropic argue against complex orchestration logic?
- Time: 5 minutes

---

### [NEW 2026] Slide: When NOT to Use Agents — The Decision Framework
**Insert after:** Production Case Study
**Format:** Decision tree / framework

#### The Agent Necessity Test

Not everything needs to be agentic. Over-engineering with agents is the most common mistake of 2025-2026:

| Question | If YES | If NO |
|---|---|---|
| Does the task require multiple steps with branching logic? | Consider agents | Use simple prompt/chain |
| Does the task require tool use (APIs, file access, web)? | Consider agents | Use prompt only |
| Does the task require reasoning about its own output? | Consider agents | Single-shot is fine |
| Is the task open-ended (not deterministic)? | Consider agents | Use deterministic code |
| Does the task run for more than one LLM call? | Consider agents | Direct API call |

#### The Anthropic Principle: "Maximise a Single Agent First"

Before building multi-agent systems:
1. Can a single agent with better tools solve this?
2. Can a single agent with better context solve this?
3. Can a single agent with verification loops solve this?

Only if ALL THREE are "no" → consider multi-agent.

#### When Simpler Approaches Win

| Approach | Use When | Advantage Over Agents |
|---|---|---|
| Direct API call | Deterministic, single-step | Faster, cheaper, more reliable |
| Chain/pipeline | Fixed sequence of steps | Predictable, debuggable |
| RAG + prompt | Knowledge retrieval + generation | No loop overhead |
| Human-in-the-loop | High stakes, rare edge cases | Accountability |

**Facilitator Notes:**
- 🎤 This is the slide that prevents students from over-engineering. Emphasise: "The best engineers reach for agents LAST, not first"
- Ask: "What problems at your organisation are currently being solved with agents that probably shouldn't be?"
- Mitchell Hashimoto quote: "Build as little agent as possible. Add agentic behaviour only when simpler approaches have failed."
- Time: 4 minutes

---

### [NEW 2026] Slide: The 7 Harness Design Decisions
**Insert after:** When NOT to Use Agents
**Format:** Framework / design checklist

#### Every Agent Builder Must Answer These 7 Questions

| # | Decision | Spectrum | Guidance |
|---|---|---|---|
| 1 | **How thick is your harness?** | Minimal scaffold ←→ Full framework | Start thin; add components as failure modes appear |
| 2 | **How will you manage context growth?** | Compaction ←→ Just-in-time retrieval | JIT for large data; compaction for conversation history |
| 3 | **What memory architecture?** | In-context only ←→ External persistence | Session memory first; add external only when context overflows |
| 4 | **How are errors classified and handled?** | Retry all ←→ Typed error routing | Always classify: transient / LLM-recoverable / user-fixable / unexpected |
| 5 | **What verification loops?** | None ←→ Multi-layer verification | At minimum: automated test/lint after every mutation |
| 6 | **Will you use sub-agents?** | Single agent ←→ Multi-agent fleet | Single agent with good tools first; sub-agents for parallelism |
| 7 | **How is safety enforced?** | Model-level only ←→ Architectural separation | Always separate permission from reasoning (Anthropic principle) |

**Design principle (Mitchell Hashimoto):**
> *"Harness engineering is the practice of engineering a solution every time an agent makes a mistake, ensuring it never makes that specific mistake again."*

This means your harness is never "done" — it grows incrementally based on observed failures.

**Facilitator Notes:**
- 🎤 Frame this as the "architect's checklist" — before building any agent, write down your answer to each of these 7 questions
- Hands-on activity: Give students a use case and have them write their 7 answers. Compare in groups.
- Time: 5 minutes (or extend to 15 min as hands-on activity)

---

### [NEW 2026] Slide: Hands-On Activity — Design Your Agent Harness
**Insert after:** The 7 Harness Design Decisions
**Format:** Hands-on activity

#### Activity: "Harness Design Workshop" (15 min)

**Scenario:** You are building an agent that automates customer support ticket triage and response drafting for a B2B SaaS company. The agent must:
- Read incoming support tickets from a queue
- Classify severity and route to appropriate team
- Draft initial responses using knowledge base content
- Escalate to human when confidence is low

**Instructions:**
1. Choose your position on the agentic maturity ladder (Level 2-5)
2. Identify which of the 12 harness components you need
3. Answer the 7 design decisions for your specific case
4. Draw a simple architecture diagram (boxes + arrows)
5. Identify the top 3 failure modes and how your harness prevents them

**Deliverable:** A one-page harness design document

**Discussion questions after:**
- Who chose single-agent vs multi-agent? Why?
- What verification loops did you include?
- Where did you put human-in-the-loop?
- How would you know if your agent is working well in production?

**Facilitator Notes:**
- 🎤 This is the capstone activity for the module. Let groups of 3-4 work together. Walk around and probe: "What happens when the knowledge base doesn't have the answer?" "What happens when the agent drafts something incorrect?"
- Expect 10 min working + 5 min sharing
- For advanced groups: Ask them to add an observability plan (Module 15 preview)
- Time: 15 minutes

---

### [NEW 2026] Slide: The Evolution from ReAct to Production Patterns
**Insert after:** Core Agentic Patterns section
**Format:** Timeline / evolution diagram

#### How Agentic Patterns Have Evolved (2022-2026)

```
2022: ReAct Paper (Yao et al.)
  └─→ Thought → Action → Observation cycle
      Simple but foundational

2023: Plan-and-Execute, Reflection, MRKL
  └─→ Agents that plan before acting, check their work
      More sophisticated single-agent patterns

2024: Andrew Ng's 4 Patterns (DeepLearning.AI)
  └─→ Reflection + Tool Use + Planning + Multi-Agent
      Canonical taxonomy adopted widely

2025: Context Engineering emerges
  └─→ Focus shifts from "what the model does" to
      "what information reaches the model"
      Karpathy + Lütke endorse the framing

2026: Harness Engineering + Managed Agents
  └─→ The harness IS the product; model is a component
      Anthropic Managed Agents, OpenAI Codex cloud
      21 patterns catalogued in 5 families
      Verification and doom loop prevention become
      first-class architectural concerns
```

**The pattern:** Each year, the focus moves further from the model and closer to the system surrounding it.

**Facilitator Notes:**
- 🎤 Use this to orient students in time — "where we are in the evolution" — and to validate that the ReAct/planning patterns they learned earlier are still relevant but are now components within a larger system
- Common reaction: "Isn't this just software engineering?" → Yes! That's exactly the point. The model provides intelligence; everything else is engineering.
- Time: 3 minutes

---

### [NEW 2026] Slide: Agent Security Surface Area — Preview
**Insert after:** 7 Harness Design Decisions
**Format:** Awareness / preview

#### Why "Agent" Means "Attack Surface"

Every tool an agent can call is an attack vector. Every piece of context is a potential injection point:

| Component | Attack Vector | Example |
|---|---|---|
| Tools | Tool can be tricked into harmful action | Agent told to "delete all files matching pattern" via injected context |
| Memory | Poisoned memories persist across sessions | Attacker plants false info in long-term memory |
| Context window | Indirect prompt injection via retrieved content | Malicious instruction hidden in a document the agent reads |
| Sub-agents | Confused deputy attacks | Sub-agent follows instructions from untrusted source |
| Computer use | Full system access | Screen-reading agent captures credentials |

**Key principle (Anthropic):** Separate permission enforcement from model reasoning architecturally. The model decides what to attempt; the tool system decides what's allowed.

**This is covered in depth in Module 14 (AI Security & Trust).** This slide is a preview — enough for students to know the attack surface exists and to build with security in mind from the start.

**Facilitator Notes:**
- 🎤 Don't deep-dive security here — just plant the seed. "Every component we discussed is also an attack surface. Module 14 will teach you how to defend each one."
- Time: 2 minutes
- Purpose: Set up Module 14 and ensure students don't build insecure agents because they weren't thinking about it

---

### [NEW 2026] Slide: Key Takeaways — The 2026 Agent Builder's Manifesto
**Insert after:** Hands-on Activity (closing slide)
**Format:** Summary / manifesto

#### 10 Things Every Agent Builder Should Know in 2026

1. **The harness IS the agent.** Model quality matters, but harness engineering has more leverage after a capability threshold.

2. **Context engineering > prompt engineering** for agents. What goes INTO the window determines success more than how you phrase the question.

3. **Maximise a single agent before going multi-agent.** Better tools + better context + verification loops first.

4. **Verification loops improve quality 2-3×.** Build them from day one, not as an afterthought.

5. **Doom loops are the #1 operational risk.** Every agent needs circuit breakers: turn limits, token budgets, retry caps.

6. **Computer-use is a new modality, not a replacement.** API-based tools are faster and cheaper. Computer use is for the last mile.

7. **Production means error classification.** Not all failures are the same. Transient ≠ LLM-recoverable ≠ user-fixable.

8. **Memory is a hint, not truth.** Always verify against actual state before acting.

9. **Start with the lightest harness that works.** Add complexity only when failure modes demand it.

10. **The benchmark that matters is your task, not SWE-bench.** Build evaluation that measures success on YOUR domain.

**Facilitator Notes:**
- 🎤 End strong. Read these out. Ask students to star the 3 that are most relevant to their current work.
- Time: 3 minutes (closing)

---

## FACILITATOR UPDATE BRIEF

### Top 3 Most Important Additions

1. **Agent Harness as the central framework** — This is the #1 conceptual upgrade. The entire module should be reframed around "you're building a harness, not just picking a model." It changes how students think about where value lives and where to invest their engineering time.

2. **Context Engineering as a named discipline** — Students who took the course before will know "prompt engineering." Context engineering extends this to the agentic world and is now considered the #1 skill for agent builders. It directly sets up Module 13 (Memory/State).

3. **Computer-Use Agents + Coding Agents as concrete examples** — These make the abstract concrete. Every student has either used Claude Code/Codex or heard of them. They are the best available case studies of harness engineering in practice.

### What's Now Outdated in the Original Module

| Original Content | Status | How to Address |
|---|---|---|
| "Agent anatomy: LLM brain, tools, memory, environment" | **Partially outdated** | Reframe as "the harness" — same components, better organizing model |
| ReAct as the primary pattern | **Still valid** | Keep but context as one component of the orchestration loop, not the whole story |
| "Agentic maturity ladder" (original) | **Needs update** | Replace with 7-level ladder (Level 0-6) that includes managed agents |
| No mention of verification/guardrails | **Gap** | Add as critical harness component — 2-3× quality multiplier |
| No coding agent examples | **Major gap** | Claude Code and Codex are now the best public case studies |

### How to Fit New Content in 60 Minutes

**The honest answer:** This module now warrants **75-90 minutes** for the full 2026 treatment. For a strict 60-minute version:

**60-minute version (prioritised):**
- Keep: Original ReAct/patterns content (abbreviated to 10 min)
- Add: Agent harness concept + Von Neumann + 3 levels (10 min)
- Add: Context engineering (5 min)
- Add: 12 components overview (5 min)
- Add: Coding agents case study (5 min)
- Add: Verification + doom loops (5 min)
- Add: 7 design decisions (5 min)
- Activity: Harness design workshop (15 min)

**Skip for beginners (move to appendix):**
- Agent benchmarks detail (mention in passing)
- Managed agents platforms (brief mention only)
- Security surface area (defer entirely to Module 14)

**75-minute extended version adds:**
- Computer-use agents (5 min)
- Agent benchmarks deep-dive (5 min)
- Managed agents comparison (5 min)

### New Tools/Accounts/Demos to Set Up

1. **Claude Code access** — For live demo of Gather-Act-Verify cycle (Anthropic Pro/Max subscription)
2. **OpenAI Codex** — For comparison demo of cloud-native agent architecture (ChatGPT Plus/Team)
3. **Video clips** — Prepare 30-second clips of:
   - Claude Computer Use navigating a web form
   - Claude Code solving a GitHub issue end-to-end
   - A doom loop occurring (before circuit breaker) vs being caught
4. **SWE-bench leaderboard** — Bookmark https://www.swebench.com/verified.html for live reference
5. **Anthropic Managed Agents docs** — Have the quickstart open for the "what exists now" demo

---

*Module 11 Update — Completed July 2026*
*Research sources: Anthropic, OpenAI, LangChain, Databricks, arxiv, practitioner blogs*
