# Module 12 — Multi-Agent Systems & Orchestration
## [AUG-2026 ADDENDUM] Content Refresh — August 12, 2026

---

## A) EXECUTIVE SUMMARY — What Changed Since July 2026

1. **MCP 2026-07-28 spec went FINAL** — The stateless release candidate covered in July's update shipped as the official specification. AWS AgentCore confirmed full support. Migration guides now available from BetterStack and DigitalApplied.

2. **MCP Security Crisis reached structural proportions** — 40+ disclosed CVEs, ~15,930 active public MCP servers, the OWASP MCP Top 10 formalized, and the MCP Dev Summit in Seoul (Aug 13-14, 2026) dedicated entirely to security. This is no longer an emerging risk — it's a permanent operational cost.

3. **Amazon Bedrock Agents Classic enters maintenance mode (July 30, 2026)** — Closed to new customers. All new development directed to Amazon Bedrock AgentCore. Existing customers must migrate. Forbes called it "AWS kills the AI services it launched just two years ago."

4. **Amazon Bedrock AgentCore is the new canonical AWS multi-agent platform** — Managed agent harness GA (June 2026), MCP 2026-07-28 support, unified observability, 5,000-session scaling, and Strands Agents as the open-source SDK.

5. **Anthropic launched Claude Managed Agents (July 2026)** — A hosted multi-agent service with self-hosted sandboxes, MCP tunnels, multiagent coordinator pattern, and a clear "five coordination patterns" framework published June 21.

6. **OpenAI Agents SDK v0.14 introduced Sandbox Agents** — Model-native harness + isolated sandbox execution for long-horizon tasks. Agent Builder/Evals products being wound down by November 2026 in favor of the Agents SDK.

7. **LangGraph reached v1 stable** — Stability-focused release (announced Aug 2026) with refined type safety. Deep Agents package launched for higher-level multi-agent work. Agent Server product matures with built-in persistence and task queues.

8. **Claude Agent SDK released (July 2026)** — Anthropic now has three agent tiers: Claude Code (individual), Claude Agent SDK (developer), Claude Managed Agents (enterprise). The "decoupling the brain from the hands" architecture published.

9. **Strands Agents emerges as AWS's open-source multi-agent framework** — Model-first, MCP-native, designed for AgentCore deployment. Multi-agent social intelligence and collaboration patterns published.

10. **The three-vendor multi-agent stack crystallized** — OpenAI (Agents SDK + Sandbox), Anthropic (Agent SDK + Managed Agents), and AWS (Strands + AgentCore) now each offer complete, opinionated multi-agent platforms. The framework choice is increasingly a vendor choice.

---

## B) NEW SLIDES

---

### [NEW AUG-2026] Slide: The MCP Security Crisis — 40+ CVEs and Counting
**Insert after:** MCP Security Considerations slide (from July update)
**Source:** Forkast.news Aug 11, 2026; Microsoft Security Blog June 30, 2026; OWASP MCP Top 10; The Hacker News Aug 10, 2026

The July update covered theoretical MCP security threats. By August 2026, this is no longer theoretical — it's a full-blown security crisis with structural implications:

**The Numbers (August 2026):**
- **40+ disclosed CVEs** affecting MCP implementations
- **15,930 active public MCP servers** across four major registries
- **600–1,650 exploitable servers** per ZDI scan of 19,000 servers
- **475,865 tools** scanned across 33,563 published MCP server builds — nearly half raised security findings
- **1 in 8 tools** exposed code execution, data deletion, or irreversible actions on first call
- **42% of vulnerable repositories** correlate with AI-generated code

**Root Cause:**
The MCP SDK STDIO transport executes arbitrary commands without sanitization across ALL four official language SDKs (Python, TypeScript, Java, Rust). Anthropic confirmed this is "by design" and declined to modify the protocol, offloading sanitization burden to developers.

**Real Attacks (June–August 2026):**
- Langflow: Two chained vulnerabilities (unauthenticated RCE + IDOR) → LLM provider keys, cloud credentials, database secrets harvested within 20 hours of disclosure
- HashiCorp Terraform MCP server: Three vulnerabilities including SSRF stealing bearer tokens + auth bypass for session hijacking
- Azure MCP CLI: 0-day RCE (ZDI-26-226, CVSS 9.8) active in the wild for months

**The OWASP MCP Top 10 (formalized 2026):**
Ten MCP-specific risks mapped to OWASP LLM categories, covering:
- Tool poisoning / malicious tool injection
- Context spoofing and prompt-state manipulation
- Insecure memory references
- Covert channel abuse
- Cross-server attacks

**Framework Vulnerability Spread:**
DEF CON 34 research: varying the orchestration framework (same underlying model) produced a **2.6× spread in Agent Compromise Rate** — from 11.9% (CrewAI) to 31.1% (SmolAgents). The framework IS the security surface.

**Facilitator Notes:**
- This is URGENT material — students deploying MCP in production need to hear this before they ship
- Key message: "MCP security is not a future concern — it's a current crisis with active exploitation"
- Discussion: "Is anyone in this room running MCP servers in production? What security controls do you have?"
- Link to Module 14 (Security): recommend students read the OWASP MCP Top 10 before deploying
- Demo opportunity: show the OWASP MCP Top 10 GitHub repo and walk through 2-3 attack scenarios
- Time: 6 minutes

---

### [NEW AUG-2026] Slide: Bedrock Agents Classic → AgentCore — The Migration
**Insert after:** Amazon Bedrock Multi-Agent Collaboration slide (from July update)
**Source:** AWS docs July 30, 2026; Forbes July 24, 2026; AWS ML Blog June-August 2026

**CRITICAL UPDATE:** The Bedrock multi-agent content from July needs a major correction. Amazon Bedrock Agents is now **Bedrock Agents Classic** and is in **maintenance mode**.

**Timeline:**
- June 30, 2026: AWS announced ~20 services moving to maintenance mode (including Bedrock Agents, Kendra, Q Business)
- July 30, 2026: Bedrock Agents Classic closed to new customers
- New accounts calling `CreateAgent` get `AccessDeniedException`
- Existing customers can continue using but should plan migration

**Amazon Bedrock AgentCore (the successor):**
```
[AgentCore Harness] — Managed agent runtime
    ├── Define agent in 3 API calls (no orchestration code)
    ├── Declare: model, tools, instructions
    ├── Native MCP 2026-07-28 support
    ├── 5,000-session scaling
    └── Unified observability
```

**Key AgentCore capabilities (GA June-July 2026):**
- **Managed agent harness** — declare agent, run in 3 API calls, zero orchestration code
- **MCP 2026-07-28 Gateway support** — native stateless MCP
- **Behavior & cost controls** — budget caps, tool restrictions, behavioral guardrails
- **Multi-tenant support** — per-tenant isolation for SaaS deployments
- **Broader knowledge + continuous learning** — agents learn from interactions
- **Unified observability** — distributed tracing across agent sessions

**Strands Agents (open-source SDK for AgentCore):**
- Model-first approach — "build agents in a few lines of Python"
- MCP-native tool integration
- Multi-agent collaboration patterns published (July 2026)
- "Social intelligence" patterns for agent coordination

**Migration guidance:**
- Existing Bedrock Agents → map supervisor/sub-agent to AgentCore harness
- Inline Agents patterns → map to AgentCore runtime configuration
- Multi-agent collaboration → use Strands Agents for orchestration layer

**Facilitator Notes:**
- ⚠️ UPDATE THE JULY SLIDE: The previous Bedrock content references an architecture that is now legacy
- For AWS-focused students: this is the #1 action item from this module refresh
- Key message: "If you're building new multi-agent on AWS, start with AgentCore + Strands, not Bedrock Agents Classic"
- Common question: "Do I need to migrate immediately?" — No, existing customers keep access, but no new features
- Time: 5 minutes

---

### [NEW AUG-2026] Slide: Anthropic's Multi-Agent Stack — Three Tiers
**Insert after:** Framework Landscape 2026 slide
**Source:** claude.com/blog July 2026; Anthropic engineering blog; platform.claude.com docs

Anthropic launched a complete multi-agent platform in June-July 2026. It's now three tiers:

**Tier 1: Claude Code (Individual Developer)**
- Agent teams shipped Feb 2026 (experimental)
- TeammateTool for multi-agent coordination
- Subagent patterns for parallelized code work
- CLAUDE.md for per-project agent configuration

**Tier 2: Claude Agent SDK (Developer)**
- Released July 6, 2026
- Build custom agents on top of Claude Code's architecture
- "Decoupling the brain from the hands" — stable interfaces that outlast implementation changes
- Full MCP integration for tool access

**Tier 3: Claude Managed Agents (Enterprise)**
- GA July 10, 2026
- Hosted multi-agent service — go from prototype to production in days
- Self-hosted sandboxes + MCP tunnels (announced same day)
- Multiagent coordinator pattern: one lead agent spawns and manages specialists
- Built-in state, memory, permissions, scheduled execution
- Beta header: `managed-agents-2026-04-01`

**Anthropic's Five Coordination Patterns (published June 21, 2026):**

| Pattern | How It Works | Best For |
|---|---|---|
| **Generator-Verifier** | One generates, one validates in a loop | Quality-critical output with explicit criteria |
| **Orchestrator-Subagent** | Lead plans, delegates bounded subtasks | Clear decomposition, minimal interdependence |
| **Agent Teams** | Long-lived workers claim from shared queue | Independent, sustained multi-step work |
| **Message Bus** | Event-driven pipeline with pub/sub | Growing agent ecosystem, decoupled services |
| **Shared-State** | Agents build on each other's artifacts | Collaborative work, iterative refinement |

**Key design philosophy:**
> *"Start with the simplest pattern that could work, watch where it struggles, and evolve from there."* — Anthropic, June 2026

**Facilitator Notes:**
- This fills a gap: the July update didn't cover Anthropic's multi-agent platform (it was just released)
- Anthropic's five patterns map well to the six canonical patterns from July — highlight the overlap
- The Generator-Verifier pattern = the Coordinator-Specialist-Verifier from July, simplified
- Key difference from OpenAI/AWS: Anthropic explicitly published "when NOT to use multi-agent" guidance alongside the platform launch
- Time: 5 minutes

---

### [NEW AUG-2026] Slide: OpenAI Agents SDK v0.14 — Sandbox Agents & Model-Native Harness
**Insert after:** OpenAI Agents SDK slide (from July update)
**Source:** openai.com/index/the-next-evolution-of-the-agents-sdk/ (April 15, 2026); OpenAI docs

The July update covered handoffs and agents-as-tools. OpenAI has since shipped a major platform evolution:

**Sandbox Agents (v0.14, April 2026 — now GA):**
```python
# pip install "openai-agents>=0.14.0"
from agents.sandbox.sandboxes import UnixLocalSandboxClient

agent = SandboxAgent(
    name="Dataroom Analyst",
    instructions="Answer using only files in data/",
    sandbox=UnixLocalSandboxClient(
        entries=[LocalDir(dataroom, mount_path="/workspace/data")]
    )
)
```

**What Sandbox Agents provide:**
- Isolated Unix-like execution environment
- Filesystem, shell, installed packages, mounted data
- Exposed ports, snapshots, controlled external access
- Agents can inspect files, run commands, edit code
- Long-horizon tasks persist across interrupts

**Model-Native Harness:**
- Instructions, tools, approvals, tracing, handoffs, resume bookkeeping
- Same harness architecture that powers Codex
- Separation of concerns: harness (orchestration) vs sandbox (execution)
- Security: credentials stay outside the sandbox; model-generated code can't access them

**Other August 2026 OpenAI updates:**
- **Agent Builder & Evals winding down** (June 3, 2026 announcement) — discontinued by Nov 30, 2026
- **Workspace Agents in ChatGPT** — multi-agent powered by Codex for enterprise
- **Multi-agent API** — models can spin up and coordinate subagents in parallel via Responses API
- **GPT-5.6 price cuts** — Luna down 80%, Terra down 20% (July 30)

**Platform convergence:**
OpenAI is consolidating everything into: **Agents SDK (code) + Codex (execution) + Responses API (inference)**. Everything else is being deprecated.

**Facilitator Notes:**
- This is a significant shift from the July content — OpenAI's platform is consolidating fast
- Key message: "OpenAI is winding down older tools and going all-in on the Agents SDK"
- The sandbox concept is critical — compare to Anthropic's self-hosted sandboxes (same month!)
- Demo opportunity: show a SandboxAgent analyzing a dataroom (15 lines of code)
- Time: 4 minutes

---

### [NEW AUG-2026] Slide: LangGraph v1 Stable + Deep Agents
**Insert after:** LangGraph Supervisor vs Swarm slide (from July update)
**Source:** docs.langchain.com Aug 2026; langchain.com/blog June 2026

**LangGraph v1 — Stability-Focused Release (August 2026):**

LangGraph hit its first truly stable major version, signaling production maturity:
- Core graph APIs and execution model **unchanged** — stability guarantee
- Refined type safety (strictly typed interrupts at graph construction)
- Improved developer ergonomics and documentation
- Migration guide published for JS/TS developers

**What v1 stability means in practice:**
- No more breaking changes to graph definition APIs
- Enterprise teams can adopt without fear of forced migrations
- IBM watsonx Orchestrate added LangGraph agent integration (May 2026)
- Companies like Uber, LinkedIn, Klarna running LangGraph in production

**Deep Agents (NEW — higher-level package):**
```python
# Built on LangGraph for complex multi-agent tasks
# Agents that can plan, use subagents, and leverage file systems
pip install deep-agents
```
- Higher-level abstraction for teams who don't want raw graph programming
- Automatic planning + subagent coordination
- File system integration for long-running work
- Positioned against CrewAI for ease-of-use with LangGraph's reliability

**Agent Server (production infrastructure):**
- Built-in persistence + task queue
- Deploy, configure, and run assistants at scale
- Changelog shows active development through August 2026
- Factory functions for per-run graph customization

**2026 Framework Comparison Update:**
| | LangGraph | CrewAI | Claude Agent SDK |
|---|---|---|---|
| **Time to working multi-agent** | Slowest | Fastest | Medium |
| **Cost to maintain** | Lowest | Medium | Lowest (managed) |
| **Scaffolding needed** | Most | Medium | Least |

**Facilitator Notes:**
- The v1 stability announcement is important for enterprise audiences — "LangGraph is production-safe"
- Deep Agents is the response to CrewAI's ease-of-use advantage — mention for students wanting simplicity
- Key comparison: LangGraph = React (write more, maintain less), CrewAI = Rails (ship fast, iterate later)
- Time: 4 minutes

---

### [NEW AUG-2026] Slide: CrewAI — August 2026 State of Play
**Insert after:** Framework Landscape slide
**Source:** docs.crewai.com changelog; Medium technical reference May 2026; Atlan architecture review July 2026

**CrewAI v1.14+ (August 2026):**
- **54,000+ GitHub stars** (June 2026)
- **450 million+ agentic workflow runs/month** (self-reported)
- **100,000+ developers certified** via learn.crewai.com
- **60% US Fortune 500** adoption claimed
- Standalone framework — zero LangChain imports since v1.0

**New Features (June–August 2026):**
- **WaitTool** — pause agent execution while waiting on long-running external jobs
- **Execution boundary interception points** — hook into any point in the execution lifecycle
- **Declarative flows on TUI** — run structured workflows via terminal UI
- **Pluggable backends** — swap memory, knowledge, RAG, and flow storage independently
- **CrewAI Discovery** (April 2026) — help companies find what multi-agent workflows to build

**Technical Architecture (v1.14):**
```
CrewAI 
├── No LangChain dependency (standalone since v1.0)
├── Own tool abstractions (BaseTool instances)
├── LLM calls via LiteLLM (model-agnostic)
├── Flows for structured orchestration
├── Crews for role-based multi-agent teams
└── Interception hooks for execution control
```

**When CrewAI wins over LangGraph:**
- Non-engineers prototyping multi-agent systems
- Role-based team metaphor matches the business problem
- Speed to first working demo is critical
- Less fine-grained control is acceptable

**Facilitator Notes:**
- CrewAI's self-reported numbers (450M runs, 60% F500) should be treated with "appropriate skepticism" per technical community — but the order of magnitude is real
- Key shift: CrewAI is no longer "the easy one" — it's becoming a serious production platform
- For students: "If you're a product manager or business analyst building agents, start here. If you're an engineer who'll maintain this for years, consider LangGraph."
- Time: 3 minutes

---

### [NEW AUG-2026] Slide: The Three-Vendor Multi-Agent Platform War
**Insert after:** Anthropic's Multi-Agent Stack slide
**Source:** Multiple (OpenAI, Anthropic, AWS announcements June-August 2026)

By August 2026, three complete multi-agent platforms exist. The framework choice is now a vendor choice:

| Dimension | OpenAI | Anthropic | AWS |
|---|---|---|---|
| **SDK** | Agents SDK v0.14+ | Claude Agent SDK | Strands Agents |
| **Managed Service** | Codex / Workspace Agents | Claude Managed Agents | Bedrock AgentCore |
| **Execution** | Sandbox Agents | Self-hosted Sandboxes | AgentCore Harness |
| **Multi-agent** | Handoffs + Agents-as-tools + Responses API multi-agent | Orchestrator-subagent + Five patterns | Supervisor-collaborator + MCP Gateway |
| **Tool Protocol** | Custom function calling + MCP support | MCP native | MCP 2026-07-28 native |
| **Security** | Sandbox isolation | MCP tunnels + enterprise controls | Guardrails + multi-tenant |
| **Pricing Model** | Per-token + Codex compute | Per-token + managed agent compute | Per-session + model inference |
| **Lock-in Risk** | High (model-native features) | Medium (MCP-first, portable patterns) | Medium (AWS services, but open-source SDK) |

**The open-source middle ground:**
- **LangGraph** — vendor-neutral, works with any model provider
- **CrewAI** — vendor-neutral via LiteLLM
- **AG2** — community fork, vendor-neutral

**Decision framework for students:**
1. Already committed to one model provider? → Use their SDK
2. Need portability across models? → LangGraph or CrewAI
3. Want managed infrastructure with minimal ops? → Claude Managed Agents or AgentCore
4. Need maximum control and debuggability? → LangGraph
5. Enterprise on AWS already? → Strands + AgentCore

**Facilitator Notes:**
- This is the "industry landscape" slide — students leave knowing the terrain
- Key insight: "The multi-agent framework decision is now inseparable from the model vendor decision"
- Emphasize: open-source options (LangGraph, CrewAI) remain the portability play
- Discussion: "Which platform would you choose for your organization and why?"
- Time: 5 minutes

---

### [NEW AUG-2026] Slide: Strands Agents — AWS's Open-Source Multi-Agent SDK
**Insert after:** Bedrock Agents Classic → AgentCore slide
**Source:** AWS ML Blog July 14, 2026; AWS DevOps Blog; AWS Prescriptive Guidance

**What is Strands Agents?**
AWS's open-source SDK for building production AI agents with a model-first approach:

```python
from strands import Agent
from strands.tools.mcp import MCPClient

# Agent in ~5 lines
agent = Agent(
    model="us.amazon.nova-premier-v2:0",
    tools=[MCPClient("http://my-mcp-server/mcp")],
    system_prompt="You are a helpful assistant..."
)
response = agent("What's the status of ticket #1234?")
```

**Key characteristics:**
- **Model-first** — the model drives orchestration decisions, not framework code
- **MCP-native** — first-class MCP client for tool access
- **Multi-agent collaboration** — published patterns for agent teams
- **AgentCore integration** — deploy to managed infrastructure seamlessly
- **Open-source** — not locked to AWS (works with any model)

**Multi-agent patterns with Strands (published July 2026):**
- **Social intelligence** — agents that understand social dynamics and adapt communication
- **Collaboration patterns** — supervisor, peer-to-peer, and hierarchical coordination
- **Meeting intelligence** — multi-agent platform for transcripts → minutes → summaries → PDFs

**Where Strands fits in the landscape:**
- Simpler than LangGraph (less boilerplate, less graph complexity)
- More opinionated than raw SDKs (model-first philosophy)
- Best for: AWS-native teams wanting open-source flexibility with managed deployment
- Think of it as: "CrewAI's simplicity + LangGraph's production-readiness + AWS-native deployment"

**Facilitator Notes:**
- This is NEW since July — Strands barely existed in the July update
- For AWS audiences: "This is your new default starting point for multi-agent on AWS"
- Demo: build a 2-agent system with Strands + MCP in under 20 lines of Python
- Compare: Strands is to AgentCore what Terraform is to AWS CloudFormation — the open-source SDK for the managed service
- Time: 4 minutes

---

### [NEW AUG-2026] Slide: When Multi-Agent Works — Anthropic's Decision Framework
**Insert after:** MAST Failure Taxonomy slide
**Source:** claude.com/blog/building-multi-agent-systems-when-and-how-to-use-them (July 10, 2026)

Anthropic published definitive guidance on when to use (and NOT use) multi-agent systems:

**Use multi-agent when:**
1. **Task naturally decomposes** into independent subtasks with different tool requirements
2. **Context isolation matters** — separate agents prevent information leakage between concerns
3. **Parallel execution** provides meaningful speed improvements
4. **Quality requires verification** by an independent evaluator
5. **The coordination cost is less than the specialization benefit**

**Stay single-agent when:**
- One well-prompted agent with tools can handle the task
- Subtasks are highly interdependent (coordination overhead dominates)
- Context sharing is more important than isolation
- The decomposition is artificial (you're creating agents for agents' sake)
- Total steps < 5 (multi-agent overhead isn't worth it)

**The honest reality (Anthropic, July 2026):**
> *"Multiple coordination patterns exist (agent swarms, capability-based systems, and message bus architectures), but [the orchestrator-subagent pattern] handles 80%+ of production multi-agent needs."*

**The evolution path:**
```
Single agent → Generator-Verifier → Orchestrator-Subagent → Agent Teams → Message Bus
     ↑                                                                          ↑
 Start here                                                        Arrive here only
                                                                 when you NEED it
```

**Key principle:** Each step adds complexity and failure surface. Only evolve when the simpler pattern demonstrably fails.

**Facilitator Notes:**
- This reinforces the July update's message but now with Anthropic's official backing
- The evolution path visual is powerful — draw it on the whiteboard
- Key quote for students: "The best multi-agent system is the one with the fewest agents that still works"
- Activity: have students map their use cases to this evolution path — where should they start?
- Time: 4 minutes

---

### [NEW AUG-2026] Slide: Async Multi-Agent Orchestration Patterns
**Insert after:** Six Canonical Orchestration Patterns slide
**Source:** platform.claude.com/cookbook/patterns-agents-async-multi-agent-orchestration (June 8, 2026)

The July update covered synchronous patterns. Production systems increasingly need **async** multi-agent coordination:

**Pattern A: Fixed N-Agent Team with Message Hub**
```
[Agent 1] ←→ [Shared Hub] ←→ [Agent 2]
                  ↕
             [Agent 3]
```
- Fixed number of pre-configured specialists
- Communicate through a shared message hub (pub/sub)
- Each agent has its own lifecycle and context
- Hub routes messages based on topic/capability
- Best for: stable team compositions with well-defined roles

**Pattern B: Dynamically Spawned Async Subagents**
```
[Orchestrator]
    ├── spawn → [Subagent A] (terminates when done)
    ├── spawn → [Subagent B] (terminates when done)
    └── spawn → [Subagent C] (terminates when done)
         ↓ results collect asynchronously
    [Orchestrator synthesizes]
```
- Orchestrator creates agents on demand
- Subagents run independently, possibly for extended periods
- Results collected asynchronously (no blocking)
- Best for: variable-scope tasks where the number of subtasks isn't known upfront

**Why async matters for production:**
- Synchronous multi-agent blocks on the slowest agent
- Long-running tasks (hours/days) need persistent async coordination
- Event-driven architectures naturally map to async patterns
- Cost efficiency: agents sleep when waiting, don't consume tokens

**Implementation consideration:**
- Need durable execution (survive restarts, handle partial failures)
- LangGraph provides this via persistence + task queues
- AgentCore provides this via managed sessions
- Claude Managed Agents provides this via hosted lifecycle

**Facilitator Notes:**
- This is ADVANCED material — for engineers building production multi-agent systems
- The key insight: "Most tutorials show synchronous patterns, but production is async"
- Connect to distributed systems knowledge: these are the same patterns as microservice orchestration
- Time: 4 minutes

---

### [NEW AUG-2026] Slide: Production Case Study — Taskade's 500,000 Agents
**Insert after:** Production Anti-Patterns slide
**Source:** taskade.com/blog/multi-agent-production (June 29, 2026)

**Company:** Taskade (productivity/collaboration platform)
**Scale:** 500,000+ AI agents deployed in production over 3 years
**Architecture:** Configurable roles, custom tools, persistent memory, inter-agent collaboration

**What they learned:**

| Lesson | Detail |
|---|---|
| **Start with one agent, add carefully** | Every new agent adds coordination complexity quadratically |
| **Persistent memory is non-negotiable** | Agents without memory repeat mistakes, lose context, frustrate users |
| **Custom tools > general-purpose** | Agents with focused, domain-specific tools outperform those with broad access |
| **Inter-agent collaboration needs guardrails** | Without explicit protocols, agents enter loops or produce contradictory outputs |
| **Configurable roles matter** | Same codebase, different personas — the role definition is 80% of performance |

**Architecture decisions that scaled:**
- Each agent: isolated context + shared knowledge base access
- Collaboration: structured message passing (not free-form)
- Roles: declarative configuration (not hard-coded behavior)
- Memory: persistent across sessions, pruned for relevance

**Contrast with the 40% failure rate:**
Taskade succeeded because they started simple (one agent), evolved incrementally, and treated agent specifications as first-class concerns — exactly the approach the MAST taxonomy recommends.

**Facilitator Notes:**
- This is a POSITIVE case study to balance the failure-focused earlier content
- Key message: "Multi-agent works at scale IF you grow into complexity rather than starting with it"
- Discussion: "What's different about Taskade's approach vs the 40% that failed?"
- Answer: incremental evolution, persistent memory, structured protocols, configurable roles
- Time: 3 minutes

---

### [NEW AUG-2026] Slide: The Gartner Numbers — Enterprise Multi-Agent Adoption 2026
**Insert after:** Executive summary / opening section
**Source:** Gartner via ampcome.com; Anthropic/Material survey via calmops.com; Beam.ai

**The market reality (mid-2026):**

| Metric | Number | Source |
|---|---|---|
| Surge in enterprise multi-agent inquiries | **1,445%** (2024→2025) | Gartner |
| Enterprise apps with task-specific agents by end 2026 | **40%** (up from <5% in 2024) | Gartner |
| Organizations deploying agents for multi-stage workflows | **57%** | Anthropic/Material survey of 500+ tech leaders |
| Organizations reporting measurable economic returns | **80%** | Anthropic/Material survey |
| Multi-agent pilots that fail within 6 months | **40%** | Beam.ai production analysis |
| Orgs that feel security posture is ready for agents | **29%** | Cisco State of AI Security 2026 |

**The paradox:**
- Adoption is surging (1,445% inquiry growth)
- Returns are real (80% report measurable ROI)
- But 40% of pilots still fail
- And only 29% feel security-ready

**What separates the 80% with ROI from the 40% that fail:**
1. Started with single-agent, evolved to multi-agent
2. Used structured specifications (not vague prompts)
3. Chose the simplest orchestration pattern that works
4. Invested in observability and monitoring from day 1
5. Treated security as a design constraint, not an afterthought

**Facilitator Notes:**
- Open the module with these numbers — they set the stakes
- The paradox is the key framing: "Multi-agent works, multi-agent fails — what determines which?"
- The rest of the module answers that question
- Time: 3 minutes

---

### [NEW AUG-2026] Slide: MCP Dev Summit Seoul — What's Next (Aug 13-14, 2026)
**Insert after:** MCP Security Crisis slide
**Source:** Forkast.news Aug 11, 2026; modelcontextprotocol.io

**The MCP Dev Summit (Seoul, August 13-14, 2026)** is happening THIS WEEK and is entirely focused on the security inflection point:

**Why it matters:**
- Transformed from "routine industry check-in" to "high-stakes confrontation"
- 40+ CVEs + OWASP MCP Top 10 formalization = the community must respond
- Key question: can MCP's "by design" flexibility coexist with enterprise security?

**Expected outcomes (based on pre-summit signals):**
- Formal security working group within Linux Foundation MCP governance
- Reference implementations with security-by-default configurations
- Certification/audit framework for MCP servers
- NSA/CISA compliance guidance for federal MCP deployments

**The dual-use tension (will be debated):**
- NSA/CISA guidance: per-tool authorization, caller authentication, strict capability boundaries
- Commercial IDEs: "move fast" deployment with minimal authentication
- Same protocol serving both with radically different security postures
- Who bears the cost of closing the gap?

**What to tell students:**
"Watch the outcomes of the MCP Dev Summit. Whatever decisions are made this week in Seoul will shape how you deploy MCP servers for the next 2-3 years."

**Facilitator Notes:**
- This is "breaking news" content — emphasize the timeliness
- If teaching after Aug 14: update with actual summit outcomes
- Key discussion: "Should MCP be secure by default (breaking developer convenience) or flexible by default (shifting security to adopters)?"
- This connects to the broader industry debate about AI safety vs. capability
- Time: 3 minutes

---

### [NEW AUG-2026] Slide: Claude Managed Agents — Self-Hosted Sandboxes & MCP Tunnels
**Insert after:** Anthropic's Multi-Agent Stack slide
**Source:** claude.com/blog/claude-managed-agents-updates (July 10, 2026)

**The enterprise concern:** "I want Anthropic's multi-agent orchestration, but my data can't leave my infrastructure."

**Solution (July 2026):** Self-hosted sandboxes + MCP tunnels

**Self-Hosted Sandboxes:**
- Agent executes tools in YOUR controlled environment
- Sandbox runs within YOUR enterprise security boundary
- Anthropic orchestrates; you provide the execution surface
- Data never leaves your infrastructure for tool execution

**MCP Tunnels:**
- Agent connects to YOUR private MCP servers
- Tunnels route through your network — no public exposure
- Enterprise security controls (VPN, mTLS, etc.) remain intact
- Agent sees only the tools you expose through the tunnel

**Architecture:**
```
[Claude Managed Agent (Anthropic Cloud)]
    ↓ orchestration commands
[MCP Tunnel] → [Your Private MCP Server (Your Network)]
    ↓ tool execution
[Self-Hosted Sandbox (Your Infrastructure)]
    ↓ results
[Claude Managed Agent (synthesizes response)]
```

**Why this matters for multi-agent:**
- Each agent in a multi-agent system can have its own sandboxed execution
- Different security boundaries per agent (principle of least privilege)
- Coordinator runs in cloud; specialists run in your environment
- Addresses the #1 enterprise blocker: data sovereignty

**Facilitator Notes:**
- This is relevant for enterprise/regulated industry students
- Key message: "You can now get managed multi-agent orchestration without giving up data control"
- Compare to AWS approach: AgentCore also offers managed harness + your tools
- The trend: all three vendors (OpenAI sandbox, Anthropic self-hosted, AWS AgentCore) converging on "managed brain + your hands"
- Time: 3 minutes

---

## C) UPDATED CASE STUDIES

### Case Study 1: Taskade — 500,000 Agents in Production (3 years)
- **Source:** taskade.com/blog (June 2026)
- **Key lessons:** Incremental growth, persistent memory, configurable roles, structured collaboration
- **Relevance:** Proof that multi-agent works at scale with discipline

### Case Study 2: Langflow Exploitation — 20-Hour Attack Chain (June 2026)
- **Source:** Sysdig threat research; Forkast.news
- **Key lessons:** MCP security is not theoretical; chained vulnerabilities → credential theft in hours
- **Relevance:** Why security-by-design is non-negotiable in multi-agent deployments

### Case Study 3: OpenAI Internal — Codex as Primary Tool (April 2026)
- **Source:** openai.com/index/how-agents-are-transforming-work/
- **Key insight:** "For the average OpenAI worker, Codex usage now accounts for more than 85% of output tokens"
- **Relevance:** Even AI companies use multi-agent (Codex) as their primary work tool — agents are mainstream

### Case Study 4: AWS Multi-Agent Meeting Intelligence (2026)
- **Source:** AWS Prescriptive Guidance
- **Architecture:** Multi-agent platform using Strands + Fargate: transcripts → minutes → summaries → PDFs
- **Relevance:** Concrete AWS deployment pattern students can replicate

### Case Study 5: Hermes Agent — 87% Tier-1 Resolution Without Escalation (2026)
- **Source:** markaicode.com (June 2026)
- **Key metric:** Multi-agent customer support triage handles 87% without human escalation
- **Relevance:** Clear ROI story for business stakeholders

---

## D) UPDATED TOOLS & RESOURCES

### New Tools (June–August 2026)

| Tool | What It Does | URL |
|---|---|---|
| **Amazon Bedrock AgentCore** | Managed multi-agent harness (replaces Bedrock Agents) | docs.aws.amazon.com/bedrock-agentcore |
| **Strands Agents** | AWS open-source multi-agent SDK | github.com/strands-agents |
| **Claude Managed Agents** | Anthropic hosted multi-agent service | platform.claude.com/docs/managed-agents |
| **Claude Agent SDK** | Anthropic developer agent framework | claude.com/blog/building-agents-with-the-claude-agent-sdk |
| **OpenAI Agents SDK v0.14** | Sandbox Agents + model-native harness | github.com/openai/openai-agents-python |
| **LangGraph Deep Agents** | Higher-level multi-agent on LangGraph | github.com/langchain-ai/langgraph |
| **CrewAI WaitTool** | Pause agents waiting on long-running jobs | docs.crewai.com/changelog |
| **OWASP MCP Top 10** | Security framework for MCP deployments | github.com/OWASP/www-project-mcp-top-10 |

### New Papers & Research

| Paper/Resource | Relevance |
|---|---|
| Anthropic: "Multi-agent coordination patterns" (June 2026) | Definitive 5-pattern framework from a model provider |
| Anthropic: "When to use multi-agent systems" (July 2026) | Official "don't over-engineer" guidance |
| Anthropic: "Decoupling the brain from the hands" (2026) | Architecture philosophy for managed agents |
| MCP Security Crisis coverage (Forkast, Aug 2026) | 40+ CVEs, structural security analysis |
| Microsoft: "State of MCP Security in 2026" (June 2026) | Enterprise security posture for MCP |
| AWS: "Multi-agent social intelligence with Strands" (July 2026) | Production multi-agent patterns on AWS |
| BetterStack: "MCP Goes Stateless" migration guide (Aug 2026) | Practical migration from old to new MCP spec |

### Updated Framework Documentation

| Framework | Current Version | Key Doc |
|---|---|---|
| LangGraph | v1.x stable | docs.langchain.com/oss/python/langgraph |
| CrewAI | v1.14+ | docs.crewai.com |
| OpenAI Agents SDK | v0.14+ | developers.openai.com/api/docs/guides/agents |
| Claude Agent SDK | GA July 2026 | claude.com/blog/building-agents-with-the-claude-agent-sdk |
| Strands Agents | Active | docs.aws.amazon.com/prescriptive-guidance/.../strands-agents |

---

## E) FARIS HADDAD CONTENT INTEGRATION

### Published Content Found:

1. **AWS Machine Learning Blog Author Page**
   - URL: aws.amazon.com/blogs/machine-learning/author/fahaddad/
   - Content: Technical blog posts on AWS AI/ML topics
   - Integration: "As I've written about on the AWS blog, [topic] is something we see repeatedly in customer engagements..."

2. **AWS Big Data Blog Author Page**
   - URL: aws.amazon.com/blogs/big-data/author/fahaddad/
   - Content: Data architecture and analytics posts
   - Integration: Relevant when discussing data pipelines that feed multi-agent systems

3. **ELVTR AI Solutions Architecture Course**
   - URL: uk.elvtr.com/course/ai-solutions-architecture
   - Content: Faris Haddad listed as instructor for AI Solutions Architecture course
   - Integration: "Drawing from my experience teaching AI Solutions Architecture at ELVTR, students often ask..."

4. **Mostly.AI — "Unlock Data Access at Scale with Synthetic Data" (July 2025)**
   - URL: mostly.ai/video/faris-haddad-aws-unlock-data-access-at-scale-with-synthetic-data
   - Content: Presentation on synthetic data for bridging legacy infrastructure and modern AI
   - Integration: Relevant to data preparation for multi-agent knowledge bases: "As I discussed at Mostly.AI's conference, getting quality data to your agents often requires bridging legacy systems..."

### Recommended Integration Points:

- **Opening credibility:** "I've been building and teaching AI architectures across AWS and various platforms, and multi-agent systems are where I see the most excitement — and the most costly mistakes."
- **AWS sections:** "From my work with AWS customers, the Bedrock Agents to AgentCore migration is top-of-mind right now..."
- **Production reality:** "In my experience teaching AI Solutions Architecture, the #1 lesson is: start with one well-built agent before adding more."

---

## F) FACILITATOR REFRESH BRIEF

### 🔥 Top 3 Things That Changed Since July 2026

1. **Bedrock Agents is DEAD (for new customers)** — This is the single biggest AWS update. The July module content about Bedrock multi-agent collaboration now references a legacy service. ALL new development goes to AgentCore + Strands. Students on AWS need to know this immediately.

2. **The MCP Security Crisis went from "emerging" to "structural"** — 40+ CVEs, OWASP MCP Top 10 formalized, MCP Dev Summit (Aug 13-14) entirely focused on security. The July module's security slide was prescient but understated. Update: this is now the #1 operational concern for anyone deploying MCP.

3. **Three complete vendor platforms launched** — In the span of 6 weeks (June-July 2026), OpenAI (Sandbox Agents), Anthropic (Managed Agents + Agent SDK), and AWS (AgentCore + Strands) each launched complete multi-agent platforms. The framework decision is now a VENDOR decision. This reshapes the entire Framework Landscape 2026 slide.

### 📢 What to Emphasise as "Breaking News"

- **"Bedrock Agents Classic is closed to new customers as of July 30"** — If any student is starting a new AWS project, they MUST use AgentCore
- **"40+ CVEs in MCP implementations — the OWASP MCP Top 10 exists now"** — Security-first for any production MCP deployment
- **"The MCP Dev Summit is happening THIS WEEK in Seoul"** — Watch for outcomes that will shape the next 2-3 years
- **"Anthropic published a 'five coordination patterns' guide that should be required reading"** — Best vendor-neutral architectural guidance available
- **"LangGraph hit v1 stable — it's the first major framework to guarantee API stability"** — Enterprise signal

### 🛠️ Demos & Tools to Set Up Fresh

1. **Strands Agents demo** — Replace or supplement the Bedrock Agents console demo with a Strands + AgentCore demo. Build a 2-agent system in <20 lines of Python.

2. **OWASP MCP Top 10 walkthrough** — Pull up github.com/OWASP/www-project-mcp-top-10 and walk through 2-3 attack scenarios. More impactful than the generic security slide.

3. **Claude Managed Agents demo** — If available, show the multiagent coordinator pattern: one lead agent spawning two specialists. Compare directly to Bedrock's supervisor pattern.

4. **OpenAI Sandbox Agent demo** — Show SandboxAgent analyzing a dataroom in ~15 lines. Demonstrates the new paradigm of "managed brain + isolated hands."

5. **Side-by-side comparison** — Build the SAME 2-agent customer service bot in (a) Strands Agents, (b) LangGraph, and (c) OpenAI Agents SDK. Show students the trade-offs live.

### ⏱️ Updated Time Allocation

The August content adds ~35 minutes of new material. Recommended cuts to stay within 90 minutes:

| Cut | Saves |
|---|---|
| Remove original Bedrock Agents content (now legacy) | 4 min |
| Condense July's A2A deep-dive (stable, less news) | 2 min |
| Merge CrewAI slide into framework comparison table | 2 min |
| Shorten activity from 15 to 12 min | 3 min |
| **Total saved** | **11 min** |

Add the highest-priority August slides:
| Add | Time |
|---|---|
| MCP Security Crisis | 6 min |
| Bedrock → AgentCore migration | 5 min |
| Anthropic's multi-agent stack + patterns | 5 min |
| Three-vendor platform comparison | 5 min |
| Gartner numbers (opening) | 3 min |
| **Total added** | **24 min** |

**Net: +13 minutes → fits in 90-minute extended delivery or requires one more cut for 60-minute version.**

For 60-minute delivery, additionally cut:
- Async patterns (advanced) → supplementary reading
- MCP Dev Summit → mention in 30 seconds, point to outcomes post-event
- Strands deep-dive → fold into AgentCore slide

---

*Module 12 August 2026 Refresh — Generated August 12, 2026*
*Sources: MCP spec 2026-07-28 final, Forkast.news MCP Security Crisis (Aug 11), AWS Bedrock/AgentCore docs (July-Aug 2026), Anthropic claude.com/blog (June-July 2026), OpenAI Agents SDK v0.14 docs, LangGraph v1 release notes, CrewAI changelog, OWASP MCP Top 10, Gartner/IDC market data, Taskade production case study*
