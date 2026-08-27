# 📚 Supplementary Reading — Agentic Track
## Additions to Modules 11, 12 & 13

---

> **How to use this document:** The sections below are designed to be inserted into the existing lesson plans for Modules 11, 12, and 13. Each section specifies exactly where it should be added (after which existing section) and how it should be used (pre-reading, in-class reference, extended lab, or case study).

---

## MODULE 11 — Introduction to AI Agents & Agentic Patterns
### Supplementary Reading Addition

**Insert after:** *Recommended Resources* section

---

### 📖 Featured Reading: The Anatomy of an Agent Harness

**Source:** Akshay Pachaar (@akshay_pachaar), X/Twitter Article, 2026  
**Length:** ~25 min read  
**Audience fit:** All students — accessible to non-engineers, deeply rewarding for engineers  
**Relevance:** ⭐⭐⭐⭐⭐ Core reading for this module

---

#### Why This Article Matters

This article is the best single-source treatment of what actually separates a toy demo from a production agent. It introduces and formalises the concept of the **agent harness** — a term now used by Anthropic, OpenAI, LangChain, and the broader practitioner community to describe the complete software infrastructure wrapping an LLM.

> *"If you're not the model, you're the harness."* — Vivek Trivedy, LangChain

This reframing is important: when someone says "I built an agent," what they actually built is a harness and pointed it at a model. The harness is the machinery; the agent is the emergent behaviour.

---

#### Key Concepts to Extract (Pre-reading Focus Questions)

Before reading, hold these questions in mind:

1. What is the difference between "the agent" and "the harness"? Why does this distinction matter for how you design and debug AI systems?
2. The article describes three levels of engineering: prompt engineering, context engineering, and harness engineering. How does each level relate to what you've learned so far in this course?
3. The article identifies 12 components of a production harness. As you read, map each component to the agent anatomy we covered in class (LLM brain, tools, memory, environment). Where does the article extend or challenge that model?
4. LangChain improved their TerminalBench ranking from outside top 30 to #5 by changing only the harness — same model, same weights. What does this tell you about where the value in agentic systems actually lives?

---

#### The 12 Components of a Production Harness (Summary)

| # | Component | What It Does | Where It Fits in Our Framework |
|---|---|---|---|
| 1 | **Orchestration Loop** | The TAO (Thought-Action-Observation) heartbeat; a while loop managing turns | Core of the ReAct pattern |
| 2 | **Tools** | Schemas injected into context; handles registration, validation, sandboxed execution | Tool use / function calling |
| 3 | **Memory** | Short-term (session), long-term (cross-session); Claude.md, MEMORY.md, LangGraph Stores | Module 13 deep-dive |
| 4 | **Context Management** | Compaction, observation masking, JIT retrieval — fighting context rot | Module 13 deep-dive |
| 5 | **Prompt Construction** | Hierarchical assembly: system prompt + tool schemas + memory + history + user message | Module 7 connection |
| 6 | **Output Parsing** | Native tool_calls objects; structured output schemas; termination detection | Engineering reliability |
| 7 | **State Management** | Conversation persistence across turns; lightweight ID chaining vs. git checkpoints | Module 13 deep-dive |
| 8 | **Error Handling** | 4 error types: transient, LLM-recoverable, user-fixable, unexpected; retry caps | Production reliability |
| 9 | **Guardrails & Safety** | Input/output/tool guardrails; tripwire mechanisms; permission vs. reasoning separation | Module 14 connection |
| 10 | **Verification Loops** | Rules-based, visual, LLM-as-judge; gives model a way to check its own work | 2–3× quality improvement |
| 11 | **Subagent Orchestration** | Fork, Teammate, Worktree models; agents-as-tools vs. handoffs | Module 12 deep-dive |
| 12 | **Lifecycle Management** | Startup, warm-up, graceful shutdown; restart-safe design | Production operations |

---

#### Three Levels of Engineering — Class Discussion Framework

The article introduces a crucial hierarchy that extends beyond what most introductory AI courses cover:

```
┌─────────────────────────────────────────────┐
│           HARNESS ENGINEERING               │  ← Complete system:
│  Tool orchestration, state persistence,     │    tool calling, error
│  error recovery, verification, safety       │    recovery, lifecycle
│  ┌─────────────────────────────────────┐    │
│  │       CONTEXT ENGINEERING           │    │  ← What the model SEES
│  │  What goes in the window, when,     │    │    and when — the
│  │  where, and in what order           │    │    most underrated skill
│  │  ┌───────────────────────────────┐  │    │
│  │  │    PROMPT ENGINEERING         │  │    │  ← The instructions
│  │  │  Crafting the instructions    │  │    │    the model receives
│  │  │  the model receives           │  │    │
│  │  └───────────────────────────────┘  │    │
│  └─────────────────────────────────────┘    │
└─────────────────────────────────────────────┘
```

> **Discussion question:** Most AI training focuses on prompt engineering. The article argues that context engineering and harness engineering are where the real leverage is. Do you agree? Where have you seen this play out in practice?

---

#### The Von Neumann Analogy (Conceptual Anchor)

Beren Millidge's framing from his 2023 essay *"Scaffolded LLMs as Natural Language Computers"* provides a useful conceptual anchor:

| Computer Component | Agent Harness Equivalent |
|---|---|
| CPU | The LLM |
| RAM | The context window |
| Disk storage | External databases / long-term memory |
| Device drivers | Tool integrations |
| Operating System | The harness itself |

This analogy explains why harness engineering feels like systems programming — because it is.

---

#### Extended Lab Activity (Optional — 30 min add-on)

**"Design Your Harness" Workshop**

Using the 12-component framework and the 7 decisions the article describes, students design the harness for a specific agentic use case of their choosing.

**The 7 Harness Design Decisions (from the article):**
1. How thick should your harness be? (minimal scaffold vs. full framework)
2. How will you manage context as it grows?
3. What memory architecture will you use?
4. How will errors be classified and handled?
5. What verification loops are appropriate for this use case?
6. Will you use subagents? If so, which orchestration model?
7. How will safety and guardrails be enforced?

**Deliverable:** A one-page harness design document specifying each of the 7 decisions for their chosen use case, with justifications.

---

#### Real-World Data Points Worth Noting

- LangChain jumped from outside top 30 to **rank 5 on TerminalBench 2.0** by changing only the harness (same model, same weights)
- A research project hit **76.4% pass rate** by having an LLM optimise the infrastructure itself
- Model performance degrades **30%+** when key content falls in mid-window positions ("Lost in the Middle" — Stanford/Chroma research)
- A 10-step process with **99% per-step success** still has only ~90.4% end-to-end success — errors compound fast
- Giving a model a way to verify its own work improves quality **2–3×** (Boris Cherny, creator of Claude Code)

---

---

## MODULE 13 — Memory, State & Long-Running Agents
### Supplementary Reading Addition

**Insert after:** *Recommended Resources* section

---

### 📖 Featured Reading: The Anatomy of an Agent Harness (Components 3, 4 & 7)

**Same source as Module 11** — this reading covers different sections in more depth.  
**Focus sections:** Memory (Component 3), Context Management (Component 4), State Management (Component 7)  
**Relevance:** ⭐⭐⭐⭐⭐ Core reading for memory and context content

---

#### Memory Architecture in Production: Claude Code's Three-Tier Model

The article provides the clearest real-world example of a production memory architecture available in the public domain:

```
TIER 1 — Lightweight Index
  ~150 characters per entry
  Always loaded into context
  Used for: key facts, active tasks, important file locations

TIER 2 — Detailed Topic Files  
  Pulled in on demand (JIT)
  Used for: project context, coding standards, decisions

TIER 3 — Raw Transcripts
  Accessed via search only (grep, glob)
  Used for: historical reference, rarely accessed detail
```

**Design principle:** The agent treats its own memory as a *hint* and **verifies against actual state before acting** — a critical production safety pattern.

> **Class discussion:** Why is "treat memory as a hint, verify before acting" such an important principle? What could go wrong if an agent trusted its memory implicitly?

---

#### Context Rot — A Named Failure Mode

The article names and quantifies a failure mode that causes many production agents to underperform silently:

**Context Rot:** Model performance degrades 30%+ when key content falls in mid-window positions — even with million-token context windows.

*Source: Chroma research, corroborated by Stanford's "Lost in the Middle" study*

**Production mitigation strategies:**

| Strategy | How It Works | Used By |
|---|---|---|
| **Compaction** | Summarise conversation history approaching limits; preserve architectural decisions, discard redundant tool outputs | Claude Code |
| **Observation masking** | Hide old tool outputs while keeping tool calls visible | JetBrains Junie |
| **Just-in-time retrieval** | Maintain lightweight identifiers; load data dynamically with grep/glob/head/tail rather than loading full files | Claude Code |
| **Sub-agent delegation** | Each subagent explores extensively but returns only 1,000–2,000 token condensed summaries | Anthropic |
| **Structured scratchpads** | Progress files and git commits as external state rather than relying on in-context memory | OpenAI Codex |

> **Anthropic's stated goal:** *"Find the smallest possible set of high-signal tokens that maximise the likelihood of the desired outcome."*

---

#### The Ralph Loop — Long-Running Agent Pattern

For agents that need to operate across multiple context windows (a task that takes longer than a single context can hold), Anthropic developed the **Ralph Loop**:

```
Phase 1 — Initializer Agent
  ├── Sets up environment
  ├── Creates init script
  ├── Writes progress file
  ├── Creates feature list
  └── Makes initial git commit

Phase 2 — Coding Agent (runs in every subsequent session)
  ├── Reads git logs to orient itself
  ├── Reads progress file for current state
  ├── Picks highest-priority incomplete feature
  ├── Works on it
  ├── Commits
  └── Writes summary → loops back to start
```

**Key insight:** The filesystem provides continuity across context windows. External state (git commits, progress files) replaces in-context memory for long-running tasks.

> **Lab extension:** Redesign the Module 13 hands-on activity to include designing a Ralph Loop for a multi-session research agent. Students spec the Initializer Agent outputs and the Coding Agent's orientation sequence.

---

#### State Management Comparison Across Frameworks

| Framework | State Approach | Persistence Model |
|---|---|---|
| **Anthropic Claude SDK** | Git commits as checkpoints + progress files as structured scratchpads | Filesystem |
| **OpenAI Agents SDK** | Lightweight `previous_response_id` chaining | In-memory or external DB |
| **LangGraph** | Namespace-organised JSON Stores; sessions backed by SQLite or Redis | Configurable |
| **Claude Code** | Three-tier memory hierarchy (index → topic files → transcripts) | Filesystem |

---

---

## MODULE 12 — Multi-Agent Systems & Orchestration
### Supplementary Reading Addition

**Insert after:** *Recommended Resources* section

---

### 📖 Supporting Reading: The Anatomy of an Agent Harness (Component 11 & Framework Comparisons)

**Same source** — focus on subagent orchestration and framework-level implementation.  
**Focus sections:** Subagent Orchestration (Component 11), "How Real Frameworks Implement the Pattern"  
**Relevance:** ⭐⭐⭐⭐ Strong supporting material

---

#### Subagent Execution Models — Production Patterns

The article documents three execution models used in production:

| Model | How It Works | Best For |
|---|---|---|
| **Fork** | Byte-identical copy of parent context; subagent explores independently | Parallel exploration tasks |
| **Teammate** | Separate execution environment with file-based mailbox communication | Concurrent specialised subtasks |
| **Worktree** | Own git worktree; isolated branch per agent | Code generation; parallel feature development |

*Source: Claude Code's documented subagent architecture*

---

#### Framework Architecture Comparison

| Framework | Orchestration Model | Key Characteristic |
|---|---|---|
| **Anthropic Claude Agent SDK** | "Dumb loop" — all intelligence in the model | query() returns async iterator; Gather-Act-Verify cycle |
| **OpenAI Agents SDK** | Code-first; Runner class with async/sync/streamed modes | Agents-as-tools OR handoffs; no graph DSL |
| **LangGraph** | Graph nodes and edges for explicit control flow | Maximum visibility and debuggability |
| **CrewAI** | Role-based; agents as crew members with defined responsibilities | Team metaphor; easiest for non-engineers to design |
| **AutoGen** | 5 orchestration patterns; conversation-based coordination | Research-grade; most flexible |

---

#### OpenAI Three-Layer Harness Architecture (Codex)

A concrete example of how production multi-agent systems are structured:

```
Layer 1: Codex Core
  Agent code + runtime

Layer 2: App Server  
  Bidirectional JSON-RPC API

Layer 3: Client Surfaces
  CLI  |  VS Code  |  Web App
  
→ All surfaces share the same harness
→ "Codex models feel consistent across surfaces" — because they are
```

**Lesson:** Separating the harness from the surface is what enables multi-surface deployment. This is a key architectural principle for teams building internal AI platforms.

---

#### Connection to MCP (Model Context Protocol)

The article's treatment of tool calling and subagent communication connects directly to the MCP content in Module 12. OpenAI's Agents SDK supports **MCP server tools** natively alongside function tools and hosted tools — meaning the communication protocol content in this module is the foundation for how production frameworks actually wire tools to agents.

---

*Supplementary Reading document — AI & Agentic AI Training Programme*  
*Source article: "The Anatomy of an Agent Harness" by Akshay Pachaar (@akshay_pachaar), 2026*
