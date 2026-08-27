# Module 13 — Memory, State & Long-Running Agents
## [NEW AUG-2026] Content Refresh Addendum
### AI & Agentic AI Training Programme — August 12, 2026

---

## A) EXECUTIVE SUMMARY — What Changed Since July 2026

1. **OpenAI shipped "Dreaming V3" (August 6, 2026)** — A completely new memory synthesis architecture for ChatGPT that runs between sessions, resolves staleness, and produces a reviewable "memory summary page." Now the default for Plus/Pro users. Both Anthropic AND OpenAI use the same term "Dreaming" for async memory consolidation — this convergence validates the pattern.

2. **Oracle published "Agent Memory is a Database Problem" (August 10, 2026)** — A technical report achieving 93.8% on LongMemEval with 10.7× fewer tokens than flat history. Positions memory as a first-class database problem with governance built in. This is the strongest enterprise-grade entry in the market.

3. **OpenAI–AWS Strategic Partnership: Stateful Runtime Environment (August 10–11, 2026)** — OpenAI models will power a "Stateful Runtime Environment" on Amazon Bedrock, explicitly designed for agentic workflows with built-in state, reliability, and governance. Amazon invested $50B in OpenAI. Memory/state for agents is now the central infrastructure play.

4. **Mem0 v3 algorithm shipped (July 31, 2026)** — Ground-up redesign scoring 91.6% on LoCoMo (+20 points) and 93.4% on LongMemEval (+26 points), with temporal reasoning added bringing scores to 92.5/94.4. Extraction latency cut in half.

5. **LangChain "Managed Deep Agents" entered public beta (August 7, 2026)** — Production-grade managed runtime with filesystem-based memory, durable memory backed by PostgreSQL, async subagents, and one-command deployment. Memory architecture converges with Anthropic's: "memory is files."

6. **Anthropic's Claude Managed Agents Memory entered GA maturity (July 22, 2026 API update)** — Paginated memory listing, shared stores across agents with scoped permissions, audit logs. Rakuten: 97% fewer first-pass errors, 27% lower cost, 34% lower latency.

7. **Claude Sonnet 5 launched (June 30, 2026)** — 1M-token context window as default, "most agentic Sonnet yet," scores 63.2% on SWE-bench Pro. Designed for long-running autonomous work with improved memory utilisation.

8. **Letta's MemFS (git-backed memory) and Context Repositories** — Every memory change is versioned with git, enabling concurrent multi-subagent memory with conflict resolution via standard git operations. The "memory is files + git" pattern is now cross-vendor.

9. **ChatGPT Atlas shutdown (August 9, 2026)** — OpenAI's AI-native browser that introduced "Browser memories" (contextual memory from web browsing) was discontinued < 10 months after launch. Lesson: memory features don't save products without core utility.

10. **AI agent memory market now exceeds $10.9B in 2026** — Up from $6.27B estimate earlier this year, reflecting the explosive growth and enterprise adoption.

---

## B) NEW SLIDES

---

### [NEW AUG-2026] Slide: OpenAI Dreaming V3 — The Other "Dreaming"
**Insert after:** Google Memory Bank (I/O 2026) slide
**Source:** https://openai.com/nl-NL/index/chatgpt-memory-dreaming/ (August 6, 2026)

**Critical Update: Both Major Labs Now Use "Dreaming"**

As of August 2026, BOTH Anthropic AND OpenAI ship a feature called "Dreaming" for background memory consolidation. The term has become the industry standard for async, between-session memory synthesis.

**OpenAI's Dreaming V3 (August 6, 2026):**

| Dimension | Saved Memories (2024) | Dreaming V0 (2025) | Dreaming V3 (2026) |
|-----------|---------------------|-------------------|-------------------|
| Trigger | Explicit ("remember X") | Background + explicit | Background-only, always on |
| Scope | Single conversation | Multi-conversation | Full user history |
| Staleness | High (never updated) | Medium (supplements) | Low (auto-refreshes) |
| Output | List of saved items | Supplementary context | Full memory summary |
| User control | Delete individual items | Limited | Review, correct, set topic preferences |

**Three Visible User Controls:**
1. **Memory summary page** — Shows synthesised understanding of the user
2. **Correction controls** — Users can update or fix any memory entry
3. **Topic preferences** — Users decide what ChatGPT should/shouldn't bring up unprompted

**How Dreaming V3 Evaluates Itself (OpenAI's 3 Criteria):**
1. **Carry forward useful context** — Tell once, remembered in future chats
2. **Follow preferences and constraints** — Dietary restrictions, communication style
3. **Stay current over time** — "Planning birthday for next Saturday" expires after Sunday

**Key Difference from Anthropic's Dreaming:**

| | Anthropic Dreaming | OpenAI Dreaming V3 |
|---|---|---|
| Target | Agent-to-agent (developer platform) | Consumer (ChatGPT users) |
| Scale | Per-agent, developer-managed | Hundreds of millions of users |
| Memory format | Files in /mnt/memory/ | Internal memory model |
| Developer control | Full API access, export, audit | User-facing only |
| Consolidation model | Agent reviews + rewrites its own store | System-level background synthesis |

**Facilitator Notes:**
- 🎤 "BREAKING: Both major labs now call their background memory consolidation 'Dreaming.' This validates the pattern we covered in the July update. The difference: Anthropic's is for developers building agents. OpenAI's is for end-user ChatGPT. The architecture is the same — async, between-session, synthesising."
- Show the memory summary page screenshot if available
- Common question: "Which is better?" Different targets. If you're building agents → Anthropic's. If you're using ChatGPT → OpenAI's. The architectural insight is identical.
- Time: 5 minutes

---

### [NEW AUG-2026] Slide: Oracle Agent Memory — The Database-Native Approach
**Insert after:** Agent Memory Landscape (2026) slide
**Source:** https://blogs.oracle.com/developers/agent-memory-is-a-database-problem-oracle-research-makes-the-case (August 10, 2026); arXiv:2607.13157

**The Thesis: Agent Memory IS a Database Problem**

Oracle's research team argues that the requirements for agent memory — persistence, indexing, scoped retrieval, transactions, governance — are literally a database requirements list. Why reinvent it?

**Benchmark Results (LongMemEval, August 2026):**

| Metric | Oracle Agent Memory | Flat History Baseline | Improvement |
|--------|-------------------|--------------------|-------------|
| LongMemEval accuracy | **93.8%** (469/500) | Baseline | State-of-the-art |
| Single-session recall | **100%** | — | Perfect |
| Temporal reasoning | **96.2%** | — | Near-perfect |
| Multi-session reasoning | **88%** | — | Honest low point |
| Tokens at turn 80 | ~1,300 | ~13,900 | **10.7× fewer** |
| BEAM (1M-token scale) | 0.680 | — | Leader |
| Pairwise judging | 48 wins | 13 wins (19 ties) | 3.7× win ratio |

**Three Memory Categories:**
```
┌─────────────────────────────────────────────────┐
│           ORACLE AGENT MEMORY                    │
├─────────────────────────────────────────────────┤
│  WORKING MEMORY                                  │
│  Thread summaries + context cards                │
│  Compact enough for prompt injection             │
├─────────────────────────────────────────────────┤
│  LONG-TERM FACTUAL MEMORY                       │
│  Durable facts, preferences, profiles            │
│  Persists across sessions, user+agent scoped     │
├─────────────────────────────────────────────────┤
│  PROCEDURAL MEMORY                               │
│  Lessons, strategies, guidelines from outcomes   │
│  What agent has learned to DO                    │
└─────────────────────────────────────────────────┘
        ↕ All stored in Oracle AI Database
        ↕ Transactions, vectors, JSON, policy
```

**Why This Matters for Enterprise:**
- Memory inherits existing DB governance (access control, audit, retention)
- No "shadow data store" to manage separately
- Deep Data Security: denied records never appear in retrieval
- Standard SQL + vector + JSON in one substrate

**Facilitator Notes:**
- 🎤 "This is the enterprise play. Oracle is saying: stop bolting vector stores onto your agent stack. Put memory in the database where governance already lives. The 93.8% on LongMemEval with 10.7× fewer tokens is the highest reported by any vendor this month."
- For enterprise audiences: emphasise the governance angle. For technical audiences: the 10.7× token reduction and lifecycle architecture.
- ⚡ ADVANCED for the full architecture. All audiences: the key insight is "memory is a database problem, not a vector store problem."
- Time: 5 minutes

---

### [NEW AUG-2026] Slide: Mem0 v3 — The Benchmark Leader Reinvents Itself
**Insert after:** Oracle Agent Memory slide
**Source:** https://docs.mem0.ai/migration/platform-v2-to-v3 (July 31, 2026); https://mem0.ai/blog/the-token-efficient-memory-algorithm-now-has-temporal-reasoning

**Ground-Up Algorithm Redesign (July 31, 2026):**

| Metric | Mem0 v2 | Mem0 v3 | Improvement |
|--------|---------|---------|-------------|
| LoCoMo | 71.4% | **91.6%** → 92.5% (with temporal) | +20 points |
| LongMemEval | 67.8% | **93.4%** → 94.4% (with temporal) | +26 points |
| Extraction latency | Baseline | **~50% reduction** | 2× faster |
| Tokens per retrieval | ~25,000+ (full context) | **~7,000** | 3.5× fewer |
| p95 latency | 17.12s | **1.44s** | 91% reduction |

**What Changed in v3:**
- New extraction model (completely rewritten, not incremental)
- Temporal reasoning added: time-aware memory and queries
- Memory Decay: search-time ranking that boosts recently-used memories, dampens stale ones (scaling factor 0.3×–1.5×)
- Agent-generated facts are first-class (actions confirmed by agent stored with equal weight)
- Oracle AI Vector Search provider added

**Breaking Changes (Students Should Know):**
- Renamed parameters, removed parameters, changed defaults
- Fundamentally different extraction model
- Migration guide required for existing deployments

**Updated Market Position (August 2026):**

| Framework | LoCoMo | LongMemEval | Tokens/Query |
|-----------|--------|-------------|--------------|
| Mem0 v3 (with temporal) | 92.5% | 94.4% | ~7,000 |
| Oracle Agent Memory | — | 93.8% | ~1,300 |
| Zep/Graphiti | — | 63.8% (2025 data) | — |

**⚠️ Benchmark Caveat (Codebridge, July 2026):**
> "Mem0 reports 92.5% on LoCoMo on its own site. An independent reimplementation on the same benchmark measured 29.3%, more than sixty points lower."
> 
> Vendor benchmarks should be validated independently. The gap between managed platform and open-source SDK is significant.

**Facilitator Notes:**
- 🎤 "Mem0 v3 is a genuine leap — but note the benchmark caveat. Managed platform scores ≠ open-source scores. Always validate on YOUR data. The temporal reasoning addition is the headline feature: memories now understand 'when.'"
- For the July update: Mem0 was listed at 49% on LongMemEval (2025 data). The v3 upgrade is dramatic. Update the comparison table accordingly.
- Time: 4 minutes

---

### [NEW AUG-2026] Slide: The "Memory is Files" Convergence
**Insert after:** Claude Code's 3-Tier Memory Hierarchy slide
**Source:** LangChain Deep Agents docs (August 2026); Anthropic Managed Memory (July 2026); Letta MemFS docs

**The 2026 Discovery: Three Major Platforms Independently Chose "Files"**

| Platform | Memory as Files | How It Works |
|----------|----------------|--------------|
| **Anthropic (Claude Managed Agents)** | `/mnt/memory/` directory per agent | Agent reads/writes with same bash/file tools it uses for everything else |
| **LangChain (Deep Agents)** | Filesystem abstraction + `/memories/agent/` | `write_file`, `read_file` tools; backend-agnostic (local, S3, PostgreSQL) |
| **Letta (MemFS)** | Git-backed filesystem | Every memory change is a git commit; concurrent multi-subagent with conflict resolution |

**Why Files?**
1. **Models already know how to use files** — No new tool ontology needed
2. **Inspectable** — Humans can `cat` the memory store, edit it, version-control it
3. **Composable** — Same read/write primitives work for code, memory, and artifacts
4. **Exportable** — No vendor lock-in; memory is portable markdown/JSON
5. **Auditable** — Git history or API audit logs track every change

**The Cross-Framework Memory Bus (July 2026 Pattern):**

> "LangChain's DeepAgents and Anthropic's managed memory arrived at the same idea from opposite directions: memory is files. DeepAgents makes memory filesystem-backed. Anthropic's managed memory stores mount as directories inside a session sandbox."
> — Rick High, "Building a Cross-Framework Memory Bus" (July 16, 2026)

**Implication for Students:**
If you're designing agent memory in 2026, the default starting point is: **filesystem-backed, inspectable, versionable.** Only add vector stores, graph databases, or specialised infrastructure when you have a specific retrieval requirement that files can't meet.

**Facilitator Notes:**
- 🎤 "This is the surprise convergence of 2026. Three competing platforms independently chose 'just use files.' It's the simplest approach that works at scale. The lesson: start with files, add complexity only when you need it."
- Demo opportunity: Show how Claude Managed Agent memory appears as files in the console
- Connect to the "12 Agentic Harness Patterns" slide: pattern #9 (filesystem as memory) is now the default, not an advanced option
- Time: 4 minutes

---

### [NEW AUG-2026] Slide: AWS + OpenAI Stateful Runtime Environment
**Insert after:** Production Checkpointing Patterns slide
**Source:** https://openai.com/index/introducing-the-stateful-runtime-environment-for-agents-in-amazon-bedrock/ (August 3, 2026)

**The Biggest Infrastructure Announcement of August 2026:**

Amazon and OpenAI are co-creating a **Stateful Runtime Environment** on Amazon Bedrock — purpose-built for agentic workflows with:
- Built-in **state persistence** across sessions
- **Reliability** guarantees for long-running agents
- Enterprise **governance** (IAM, audit, compliance)
- Powered by OpenAI models (GPT-5.6), optimised for AWS infrastructure

**What This Means for Agent Memory:**
```
BEFORE (2025): Build your own state management
  → Choose framework → Add checkpointer → Wire persistence
  → Handle failures → Manage governance separately

AFTER (Aug 2026): Managed stateful runtime
  → State, reliability, governance built into the platform
  → Focus on agent logic, not infrastructure
```

**Context: Amazon's $50B investment in OpenAI + AWS partnership**

This signals that **stateful agents are the central enterprise infrastructure play of 2026**. The industry is moving from "agents are stateless functions you call" to "agents are persistent processes with durable state."

**Market Implication:**
- AWS AgentCore Memory (existing) + OpenAI Stateful Runtime (new) = two stateful agent paths on AWS
- LangChain Managed Deep Agents (public beta, Aug 7) = third option
- Anthropic Claude Managed Agents = fourth option
- Enterprise teams now have managed stateful runtimes from every major provider

**Facilitator Notes:**
- 🎤 "This is the 'state has won' moment. When AWS and OpenAI jointly build a managed stateful runtime and call it the centrepiece of a $50B partnership, the debate is over. Agents need persistent state. The question is now which managed platform, not whether to build your own."
- For enterprise students: this changes the build-vs-buy calculus entirely
- Time: 4 minutes

---

### [NEW AUG-2026] Slide: LangChain Deep Agents — The New Memory Architecture
**Insert after:** LangGraph DeltaChannel slide
**Source:** https://docs.langchain.com/oss/javascript/deepagents/long-term-memory (August 2026); https://www.langchain.com/blog/managed-deep-agents-is-now-in-public-beta (August 7, 2026)

**LangChain's Next-Generation Agent Runtime (Public Beta, Aug 7, 2026):**

Deep Agents replaces the "LangGraph + memory add-ons" pattern with an integrated runtime:

**Memory Architecture:**
```
┌──────────────────────────────────────────────┐
│           DEEP AGENTS RUNTIME                 │
├──────────────────────────────────────────────┤
│  FILESYSTEM ABSTRACTION                       │
│  • read_file, write_file, search, glob        │
│  • Image files returned as multimodal blocks  │
│  • Pluggable backends (local, S3, PostgreSQL) │
├──────────────────────────────────────────────┤
│  SHORT-TERM MEMORY                            │
│  • Conversation history in context            │
│  • Loaded at startup from filesystem          │
├──────────────────────────────────────────────┤
│  LONG-TERM (DURABLE) MEMORY                   │
│  • /memories/agent/ tree                      │
│  • Shared across threads and sessions         │
│  • Backed by PostgreSQL                       │
│  • Opt-in (not enabled by default)            │
├──────────────────────────────────────────────┤
│  SKILLS (on-demand loading)                   │
│  • Descriptions loaded at startup             │
│  • Full skill file loaded only when matched   │
│  • JIT pattern applied to procedural memory   │
└──────────────────────────────────────────────┘
```

**Key Design Choices:**
- MIT licensed, open-source
- Agents exposed via open protocols (MCP, A2A)
- Memory lives in YOUR PostgreSQL
- Async subagents (v0.5, April 2026): delegate work to background agents
- Managed runtime: one-command deploy to production

**How This Updates the Module's Framework Table:**

| Framework | 2026 Status | Memory Model |
|-----------|-------------|--------------|
| LangGraph (v1.x) | Stable, graph-based | DeltaChannel checkpointing |
| Deep Agents | Public beta, integrated runtime | Filesystem + durable memory + skills |
| Managed Deep Agents | Public beta (Aug 7) | Hosted Deep Agents with managed infra |

**Facilitator Notes:**
- 🎤 "LangChain has bifurcated: LangGraph for graph-based orchestration, Deep Agents for integrated runtime with built-in memory. If students are starting new projects in August 2026, Deep Agents is the recommended starting point for LangChain users."
- Note: DeltaChannel is still relevant for LangGraph users. Deep Agents is an alternative, not a replacement.
- Time: 4 minutes

---

### [NEW AUG-2026] Slide: Anthropic Managed Agents Memory — Production Maturity
**Insert after:** Dreaming slide (existing)
**Source:** https://claude.com/blog/claude-managed-agents-memory (April 23, 2026); Platform docs update July 22, 2026

**From Beta to Production (April → August 2026):**

**Architecture:**
```
Agent Session → /mnt/memory/ (filesystem mount)
                    ↓
Claude reads/writes with same bash/file tools
                    ↓
Memory Stores (scoped, shared, auditable)
    ├── Org-wide store (read-only for agents)
    ├── Per-user stores (read/write)
    └── Per-agent stores (isolated)
```

**Key Capabilities (GA as of July 2026):**
- **Shared stores** across multiple agents with different access scopes
- **Concurrent writes** — multiple agents work against same store without overwrites
- **Full audit trail** — which agent, which session, what was learned
- **Export/rollback** — memories are files, exportable, version-controllable
- **Paginated API** (July 22 update) — production-scale memory listing

**Production Results (Named Customers):**

| Company | Use Case | Result |
|---------|----------|--------|
| **Rakuten** | Long-running task agents | 97% fewer first-pass errors, 27% lower cost, 34% lower latency |
| **Netflix** | Cross-session context retention | Eliminated manual prompt/skill updates |
| **Wisedocs** | Document verification pipeline | 30% faster verification via pattern memory |
| **Ando** | Workplace messaging | Replaced custom memory infrastructure entirely |

**The Design Principle:**
> "Agents are most effective with memory when it builds on the tools they already use."

Memory mounts as a filesystem → agent uses bash and code tools it already knows → no new memory-specific API to learn.

**Facilitator Notes:**
- 🎤 "This is the most production-proven agent memory system as of August 2026. Rakuten's 97% error reduction is the stat that sells memory to executives. The filesystem-mount design is elegant: the agent doesn't need to learn a memory API — it just reads and writes files."
- Common question: "Can I use this without Anthropic's platform?" The design pattern (memory as files) is portable. The managed service (audit, scoping, concurrent access) requires Claude Managed Agents.
- Time: 4 minutes

---

### [NEW AUG-2026] Slide: Claude Sonnet 5 — 1M Tokens + Agentic Memory
**Insert after:** Long-Context Trap slide
**Source:** https://www.anthropic.com/news/claude-sonnet-5 (June 30, 2026)

**The Long-Context + Memory Combined Approach:**

Claude Sonnet 5 (June 30, 2026) ships with:
- **1M-token context window** as the DEFAULT (no smaller variant)
- 128K max output tokens
- "Most agentic Sonnet yet" — plans, uses tools, runs autonomously
- SWE-bench Pro: 63.2% (vs Opus 4.8 at 69.2%)
- Price: $2/$10 per million tokens (introductory through Aug 31)

**What This Means for the Module's "Long Context vs Memory" Discussion:**

The question is NO LONGER "long context OR memory." The answer is:
```
1M-token window (Sonnet 5)
    + Filesystem-backed persistent memory (Claude Managed Agents)
    + Dreaming (async consolidation)
    = Full memory stack
```

**Updated Decision Framework:**
```
┌─────────────────────────────────────────────────┐
│  WITHIN A SESSION (< 1M tokens total)           │
│  → Use the context window directly              │
│  → Position critical info at start/end          │
│  → Use compaction after ~50 turns               │
├─────────────────────────────────────────────────┤
│  ACROSS SESSIONS                                │
│  → Persistent memory (files, stores)            │
│  → Dreaming for consolidation                   │
│  → Temporal memory for evolving facts           │
├─────────────────────────────────────────────────┤
│  AT SCALE (10K+ concurrent agents)              │
│  → Managed runtime (AWS, Anthropic, LangChain)  │
│  → Database-native memory (Oracle, PostgreSQL)  │
│  → Governance built into the substrate          │
└─────────────────────────────────────────────────┘
```

**Facilitator Notes:**
- 🎤 "Sonnet 5 gives you 1M tokens AND memory. This isn't either/or anymore. The 1M window handles within-session work. Memory handles cross-session learning. Together, they solve the full problem."
- Update from July module: the "Long-Context Trap" slide is still valid — but now we can say "even with 1M tokens, you still need external memory for cross-session continuity."
- Time: 3 minutes

---

### [NEW AUG-2026] Slide: Letta MemFS — Git-Backed Agent Memory
**Insert after:** Letta (MemGPT) slide (existing)
**Source:** https://docs.letta.com/concepts/memfs; https://www.letta.com/blog/context-repositories/ (February 2026)

**Evolution: From OS-Inspired to Git-Backed**

Letta's latest innovation: **MemFS** — a git-backed filesystem where every memory change is a versioned commit.

**Architecture:**
```
┌─────────────────────────────────────────────────┐
│              LETTA MemFS                         │
├─────────────────────────────────────────────────┤
│  Git Repository (local or remote)               │
│  ├── memory/                                    │
│  │   ├── core/         (always loaded)          │
│  │   ├── episodic/     (searchable)             │
│  │   └── procedural/   (skills, learned)        │
│  ├── context/          (project context)        │
│  └── .git/             (full version history)   │
├─────────────────────────────────────────────────┤
│  OPERATIONS                                      │
│  • /init — bootstrap memory for new project     │
│  • Commit — every memory write is versioned     │
│  • Branch — subagents can diverge               │
│  • Merge — conflict resolution via git ops      │
│  • Blame — trace any memory to its origin       │
│  • Revert — undo bad consolidation              │
└─────────────────────────────────────────────────┘
```

**Why Git for Memory:**
- **Versioning**: Every change has history; rollback is trivial
- **Concurrency**: Multiple subagents branch, work, merge — standard git workflows
- **Provenance**: `git blame` tells you which session/agent created any memory
- **Collaboration**: Teams can PR-review an agent's learned memories
- **Portability**: Memory is a repo; move it anywhere

**Context Repositories (February 2026):**
> "Context Repositories are git-backed, so every change to memory is automatically versioned with informative commit messages. Git tracking also enables concurrent, collaborative work across multiple subagents."

**Recommended Models (August 2026):**
- Opus 4.5 and GPT-5.2 for best performance (per Letta's model leaderboard)
- Model-agnostic: works with any provider

**Facilitator Notes:**
- 🎤 "Letta took the filesystem-as-memory idea one step further: filesystem + git. Now you have full version control over what an agent remembers. This is the most transparent memory system available — you can literally `git log` an agent's learning history."
- Demo: Show `git log` on a Letta agent's memory repo
- Connect to existing Ralph Loop slide: the Ralph Loop uses git for continuity. Letta formalises this into the memory architecture itself.
- Time: 4 minutes

---

### [NEW AUG-2026] Slide: The Memory Benchmark Reality Check
**Insert after:** Memory Evaluation slide (existing)
**Source:** https://agent-memory-context-management.hashnode.dev/the-state-of-ai-memory-in-2026-claimed-vs-observed (July 28, 2026); https://www.codebridge.tech/articles/best-ai-memory-frameworks (July 20, 2026)

**"AI memory is the most-benchmarked, least-reproduced category in the AI tooling stack." (Hashnode, July 2026)**

**The Claimed vs. Observed Problem:**

| Framework | Vendor-Claimed (LoCoMo) | Independent Reproduction | Gap |
|-----------|------------------------|-------------------------|-----|
| Mem0 v3 (managed) | 92.5% | 29.3% (Codebridge, open-source SDK) | **63 points** |
| Oracle Agent Memory | 93.8% (LongMemEval) | Not independently verified yet | — |

**Why the Gap Exists:**
1. **Managed platform ≠ open-source SDK** — Managed platforms include proprietary optimisations not in the SDK
2. **Benchmark configuration varies** — Temperature, retrieval budget, chunking strategy all matter
3. **Test set contamination** — Some frameworks may over-optimise for known benchmark questions
4. **Partial vs. full evaluation** — Some publish only their strong dimensions

**What Students Should Actually Do:**
```
1. Never trust vendor benchmarks alone
2. Run LoCoMo/LongMemEval on YOUR data, YOUR configuration
3. Measure the four dimensions independently:
   - Recall (can it find stored facts?)
   - Freshness (does it use the latest version?)
   - Contradiction handling (new fact overrides old?)
   - Forgetting (does it drop irrelevant info?)
4. Measure operational metrics too:
   - Tokens per retrieval
   - p95 latency
   - Cost per 1000 memory operations
```

**Facilitator Notes:**
- 🎤 "This is the skepticism slide. The benchmark numbers are real — on the vendor's managed platform, with their configuration. Your results WILL be different. The lesson: always validate on your own data. A 60-point gap between claimed and reproduced is... sobering."
- This updates and strengthens the July module's Memory Evaluation slide
- Common question: "So which one is actually best?" The honest answer: it depends on your setup. Run the benchmarks yourself.
- Time: 4 minutes

---

### [NEW AUG-2026] Slide: The Cost-Performance Tradeoff (New Data)
**Insert after:** Long-Context Trap slide
**Source:** arXiv:2603.04814 (March 2026); Atlan (June 2026); Tianpan.co (April 2026)

**Hard Numbers on Long-Context vs. External Memory (2026):**

| Metric | Full Context (100K tokens) | External Memory (Mem0-class) | Difference |
|--------|--------------------------|------------------------------|------------|
| Accuracy | Baseline | **+26% better** | External wins |
| p95 latency | 17.12s | **1.44s** | 91% reduction |
| Tokens per query | 25,000+ | **~7,000** | 70% fewer |
| Cost break-even | — | **After ~10 interaction turns** | Memory pays for itself quickly |

**The Break-Even Analysis (arXiv, March 2026):**
> "At a context length of 100K tokens, the memory system becomes cheaper after approximately ten interaction turns, with the break-even point decreasing as context length grows."

**Production Cost Reality (Tianpan.co, 2026):**
- Production agents consume ~100 input tokens per 1 output token
- Unconstrained software-engineering agent: $5–8 per task
- At 10,000 daily interactions: $250K/year unoptimised
- With 60% compression from memory: $102K/year
- **Savings: $148K/year from memory alone**

**Decision Matrix (Updated August 2026):**

| Scenario | Best Approach | Why |
|----------|--------------|-----|
| < 10 turns, single session | Full context | Overhead of memory isn't worth it |
| > 10 turns, single session | Context + compaction | Latency and cost benefit kicks in |
| Multi-session | External memory | No alternative for cross-session |
| Enterprise (governance required) | Database-native memory | Oracle/PostgreSQL with access control |

**Facilitator Notes:**
- 🎤 "The 10-turn break-even point is the number to remember. After 10 turns, external memory is cheaper than long context. Most production agents exceed 10 turns. Therefore, most production agents should use external memory."
- This replaces generic "long context vs memory" discussion with hard economics
- Time: 4 minutes

---

### [NEW AUG-2026] Slide: Memory Security Update — Shared Stores & Attack Surface
**Insert after:** Memory Poisoning slide (existing)
**Source:** https://rickhigh.substack.com/p/claude-managed-agents-viii-your-agent (August 10, 2026)

**New Attack Surface: Shared Memory Stores (August 2026)**

As memory stores become shared across multiple agents (Anthropic, LangChain, Oracle), the security model compounds:

**The Shared Store Threat Model:**
```
SINGLE AGENT (July 2026 model):
  Attacker → poisons Agent A's memory → Agent A acts on poison

SHARED STORE (August 2026 reality):
  Attacker → poisons shared store → ALL agents reading that store
  act on poison → Cross-agent contamination → Organisation-wide impact
```

**Anthropic's Scoped Access Model:**

| Store Type | Access | Risk Level |
|------------|--------|------------|
| Org-wide store | Read-only for agents | LOW (agents can't write poison) |
| Per-user store | Read/write per user | MEDIUM (user can poison their own agent) |
| Shared agent store | Read/write by multiple agents | HIGH (one agent's bad learning spreads) |

**New Mitigations (August 2026):**
- **Write scope separation** — Not all agents can write to shared stores
- **Memory provenance in audit logs** — Track which agent/session created each memory
- **Rollback capability** — Revert store to previous state if contamination detected
- **Default access mode matters** — "The default access mode quietly decides whether that memory is also an attack surface" (Rick High)

**Updated Security Checklist:**
1. ☐ Memory stores have explicit access scopes defined
2. ☐ Org-wide stores are read-only for agents (human-write only)
3. ☐ Per-user stores are isolated (user A can't read user B's memories)
4. ☐ Audit log is enabled and regularly reviewed
5. ☐ Rollback procedure is documented and tested
6. ☐ High-impact memory writes require human approval gate
7. ☐ Cross-agent memory propagation has a validation step

**Facilitator Notes:**
- 🎤 "The July module covered memory poisoning for single agents. Now that shared stores are production-ready, the attack surface multiplied. One poisoned memory in a shared store can corrupt every agent that reads it. The mitigation: strict write scopes and audit trails."
- This builds on the existing Memory Poisoning slide — reference it directly
- Time: 3 minutes

---

### [NEW AUG-2026] Slide: The August 2026 Framework Landscape (Updated)
**Insert after:** Memory Architecture Selection Decision Tree
**Source:** Multiple sources aggregated

**Updated Comparison Table (August 2026):**

| Framework | LoCoMo | LongMemEval | Architecture | Latest Update |
|-----------|--------|-------------|--------------|---------------|
| **Mem0 v3** | 92.5% | 94.4% | Vector + temporal | Jul 31: v3 algorithm |
| **Oracle Agent Memory** | — | 93.8% | Database-native (Oracle AI DB) | Aug 10: arXiv report |
| **Anthropic Managed Memory** | — | — (internal) | Filesystem mount | Jul 22: paginated API |
| **LangChain Deep Agents** | — | — | Filesystem + PostgreSQL | Aug 7: managed beta |
| **Letta MemFS** | — | — | Git-backed filesystem | Ongoing: Opus 4.5 recommended |
| **AWS AgentCore Memory** | — | — | Managed cloud service | May: strictly consistent metadata |
| **Zep/Graphiti** | — | 63.8% (2025) | Temporal knowledge graph | SOC2/HIPAA/GDPR certified |
| **OpenAI Dreaming** | — | — | Background synthesis (consumer) | Aug 6: Dreaming V3 |

**The 2026 Platform Wars:**

| If You're On... | Memory Path |
|-----------------|-------------|
| AWS | AgentCore Memory OR OpenAI Stateful Runtime (new) |
| Anthropic | Claude Managed Agents Memory (filesystem) |
| LangChain | Deep Agents (filesystem + PostgreSQL) |
| Self-hosted | Mem0 v3 OR Letta MemFS |
| Enterprise (governance-first) | Oracle Agent Memory OR AWS AgentCore |
| Multi-framework | Cross-framework bus pattern (files as common substrate) |

**Facilitator Notes:**
- 🎤 "This table replaces the July version. The landscape moved significantly in one month: Mem0 v3, Oracle's entry, LangChain Managed Deep Agents, and the AWS+OpenAI partnership all landed. The key trend: every major platform now offers managed memory."
- Print this as an updated handout
- Time: 3 minutes

---

### [NEW AUG-2026] Slide: Updated Knowledge Check Questions
**Insert after:** Existing Knowledge Check section

**Additional Quiz Questions [NEW AUG-2026]:**

Q11. What does OpenAI's "Dreaming V3" (August 2026) do?
- A) Fine-tunes the model on user data
- B) Synthesises memory between sessions, producing a reviewable memory summary ✅
- C) Generates images from text descriptions
- D) Trains a personal model for each user

Q12. Oracle Agent Memory achieved what score on LongMemEval?
- A) 63.8%
- B) 73.2%
- C) 93.8% ✅
- D) 100%

Q13. What did three major platforms (Anthropic, LangChain, Letta) independently converge on for agent memory?
- A) Vector databases
- B) Graph databases
- C) Filesystem-backed memory ("memory is files") ✅
- D) In-context only

Q14. After how many interaction turns does external memory become cheaper than full-context approaches (at 100K tokens)?
- A) 1 turn
- B) ~10 turns ✅
- C) ~50 turns
- D) ~100 turns

Q15. What is the key risk of shared memory stores across multiple agents?
- A) Increased latency
- B) One agent's poisoned memory can contaminate all agents reading the shared store ✅
- C) Higher storage costs
- D) Reduced accuracy

---

## C) UPDATED CASE STUDIES

### Case Study 1: Rakuten — Memory in Production at Scale
**Source:** Anthropic blog (April 2026), updated metrics (August 2026)
- **Context:** Long-running task agents for business operations
- **Memory approach:** Claude Managed Agents with persistent filesystem memory
- **Results:** 97% fewer first-pass errors, 27% lower cost, 34% lower latency
- **Key insight:** "Continuous learning stays under our control" — workspace-scoped, observable memory with audit trails
- **Module connection:** Validates the Dreaming pattern + filesystem memory approach

### Case Study 2: Netflix — Cross-Session Agent Learning
**Source:** Anthropic blog (April 2026)
- **Context:** Agents carrying context across sessions, including multi-turn insights
- **Memory approach:** Claude Managed Agents memory
- **Before:** Manually updating prompts and skills after each session
- **After:** Agents automatically retain insights and human corrections
- **Module connection:** Shows the "self-improving memory" pattern in production at a major tech company

### Case Study 3: Oracle — Enterprise-Grade Memory at 93.8% Accuracy
**Source:** arXiv:2607.13157 (July 14, 2026); Oracle blog (August 10, 2026)
- **Context:** Database-native memory substrate for enterprise AI agents
- **Memory approach:** Working + long-term + procedural memory on Oracle AI Database
- **Results:** 93.8% LongMemEval, 10.7× token reduction, 3.7× win ratio vs flat history
- **Key insight:** "Bounded, relevant context beat complete, unfocused context" — less is more
- **Module connection:** Validates the enterprise need for governance-first memory

### Case Study 4: ChatGPT Atlas — Memory Features Don't Save Products
**Source:** OpenAI (August 9, 2026 shutdown)
- **Context:** AI-native browser with "Browser memories" — contextual memory from web browsing
- **Launched:** Late 2025. **Shutdown:** August 9, 2026 (< 10 months)
- **Lesson:** Memory is necessary but not sufficient. Core product-market fit matters more than memory features.
- **Module connection:** Counterpoint to "just add memory and everything works" — memory must serve a real user need

---

## D) UPDATED TOOLS & RESOURCES

### New Releases (June–August 2026)

| Tool/Resource | What's New | Relevance |
|---------------|-----------|-----------|
| **Mem0 v3** (Jul 31) | New algorithm: 92.5% LoCoMo, 94.4% LongMemEval, temporal reasoning | Updated memory layer benchmark leader |
| **Oracle Agent Memory** (Aug 10) | Database-native memory substrate, 93.8% LongMemEval | Enterprise-grade, governance-built-in |
| **LangChain Deep Agents** (Aug 7) | Managed runtime with filesystem memory, PostgreSQL-backed durable memory | New default for LangChain ecosystem |
| **OpenAI Dreaming V3** (Aug 6) | Background memory synthesis for ChatGPT, memory summary page | Consumer memory architecture reference |
| **AWS + OpenAI Stateful Runtime** (Aug 3-11) | Managed stateful environment on Amazon Bedrock | Enterprise agent state management |
| **Claude Sonnet 5** (Jun 30) | 1M-token default context window, most agentic Sonnet | Long-context + memory combined approach |
| **Anthropic Managed Memory API update** (Jul 22) | Paginated memory listing, production-scale | API maturity for production deployment |
| **Letta** (ongoing) | MemFS git-backed memory, Opus 4.5/GPT-5.2 recommended | Git-versioned agent memory |
| **AgeMem** (arXiv, Jul 23) | Unified long-term + short-term memory management for LLM agents | Research: automated tier management |

### Papers (June–August 2026)

| Paper | Key Finding |
|-------|-------------|
| "Oracle Agent Memory as Enterprise Substrate" (arXiv:2607.13157, Jul 14) | Database-native memory achieves SOTA with governance |
| "A Cost-Performance Analysis of Fact-Based Memory vs. Long-Context" (arXiv:2603.04814) | Memory cheaper after ~10 turns at 100K context |
| "A Survey of Agent Memory in the Second Half" (arXiv:2602.06052, Aug 4 update) | Comprehensive taxonomy of memory architectures |
| "Learning Unified Long-Term and Short-Term Memory Management" (arXiv:2601.01885, Jul 23) | AgeMem: automated memory tier management |

### Documentation Updates

- **Claude Memory Docs:** https://code.claude.com/docs/en/memory (August 5, 2026 update)
- **LangChain Deep Agents Long-Term Memory:** https://docs.langchain.com/oss/javascript/deepagents/long-term-memory
- **Mem0 v3 Migration Guide:** https://docs.mem0.ai/migration/platform-v2-to-v3
- **Oracle Agent Memory:** https://www.oracle.com/database/ai-agent-memory/
- **AWS AgentCore Memory Types:** https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory-types.html

---

## E) FARIS HADDAD CONTENT INTEGRATION

**Search Results:** No publicly discoverable LinkedIn posts, articles, blog posts, or Medium articles by Faris Haddad specifically on AI/agentic topics were found in the June–August 2026 timeframe via web search.

**Recommendation:** If Faris has published or shared relevant content on LinkedIn, internal Slack, or other channels that isn't publicly indexed, the facilitator should:
1. Check LinkedIn directly for recent posts about agent memory or context engineering
2. Reference the ELVTR AI Solutions Architecture course listing (found at uk.elvtr.com/course/ai-solutions-architecture) as a credential/authority signal
3. Use the framing: "Based on what we're seeing in production with our clients..." rather than citing specific published articles

**Alternative Integration Points:**
- The module content itself (this update series) represents Faris's expertise. Frame it as: "As I've been researching and building this curriculum, these are the patterns I'm seeing converge..."
- If teaching AWS-adjacent audiences, reference the AWS + OpenAI Stateful Runtime partnership as an area of direct professional relevance

---

## F) FACILITATOR REFRESH BRIEF

### 🎤 Top 3 Things That Changed Since July 2026

1. **OpenAI's Dreaming V3 validates the consolidation pattern universally** (Aug 6)
   - Both major labs now ship "Dreaming" — the between-session memory consolidation pattern is the industry standard
   - The July module covered Anthropic's version. Now add OpenAI's consumer-facing version for completeness
   - Key stat: "hundreds of millions of users" — this isn't experimental anymore

2. **The "Memory is Files" convergence is now undeniable** (Aug 7)
   - Anthropic (filesystem mount), LangChain Deep Agents (filesystem abstraction), Letta (git-backed filesystem) — three independent platforms chose files
   - Update the module's advice: the default starting architecture for memory is now "files with version control"
   - Old advice: "start with Mem0 for simplicity." New advice: "start with files, add specialised memory only when needed"

3. **Managed stateful runtimes are the new default** (Aug 3–11)
   - AWS + OpenAI Stateful Runtime Environment, LangChain Managed Deep Agents, Anthropic Managed Agents — every major platform now offers managed agent state
   - The "build your own persistence" era is ending for most teams
   - Update the Production Checkpointing slide: managed runtimes now handle this

### What to Emphasise as "Breaking News"

- **The $50B signal:** AWS + OpenAI partnership with stateful runtime as centrepiece. Memory/state for agents is the #1 enterprise infrastructure investment area.
- **Mem0 v3's +26 point jump on LongMemEval** with the caveat about vendor vs. independent benchmarks (63-point gap reported by Codebridge)
- **Oracle's 93.8% entry** — the "memory is a database problem" framing is powerful for enterprise audiences
- **ChatGPT Atlas shutdown** — counterexample showing memory features alone don't save products

### Demos & Tools to Set Up Fresh

| Demo | What to Show | Setup |
|------|-------------|-------|
| **OpenAI Memory Summary** | Show Dreaming V3's memory summary page in ChatGPT | Requires Plus/Pro account (US) |
| **LangChain Deep Agents** | Deploy a memory-enabled agent with one command | `pip install langchain-deepagents`; follow managed beta docs |
| **Mem0 v3 temporal queries** | Show time-aware memory retrieval | Upgrade to Mem0 v3 SDK; run temporal memory demo |
| **Letta git log** | Show `git log` on an agent's memory repository | Letta cloud account or local install |
| **Oracle Agent Memory** | Show token reduction in action (1,300 vs 13,900) | Oracle Cloud account + oracleagentmemory SDK |

### Timing Adjustments

The August additions add ~35 minutes of new content. Recommended integration:

**For 60-minute delivery:** Replace the following July slides with August updates:
- Replace "Google Memory Bank" → "OpenAI Dreaming V3" (more documented, more relevant)
- Replace "Cross-Agent Organisational Memory" → "Memory is Files Convergence" (more practical)
- Compress "Framework Landscape" → use August 2026 updated table (one slide)
- Add "Benchmark Reality Check" as a 2-minute caveat after Memory Evaluation

**For 75-minute delivery (recommended):**
- Add: OpenAI Dreaming V3, Oracle Agent Memory, Mem0 v3, Memory is Files Convergence, Cost-Performance Tradeoff
- Skip: LangChain Deep Agents deep-dive (mention only), Claude Sonnet 5 (reference in passing)

**For 90-minute deep-dive:**
- All August slides included
- Add live demo: Mem0 v3 temporal queries
- Add discussion: "Is memory a database problem or a file problem?" (Oracle vs. Filesystem approaches)

---

*Module 13 August 2026 Refresh Complete — AI & Agentic AI Training Programme*
*Compiled: August 12, 2026*
