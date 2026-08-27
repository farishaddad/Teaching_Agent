# Module 12 — Multi-Agent Systems & Orchestration
## [2026 UPDATE] Gap Analysis, New Slides & Facilitator Delivery Notes

---

## GAP ANALYSIS

The original module covered multi-agent architectures (supervisor/peer-to-peer/hierarchical), agent roles, A2A/MCP/tool calling, handoff patterns, Bedrock Agents multi-agent, and reliability patterns. Based on web research of the 2025–2026 landscape, the following gaps exist:

1. **MCP has undergone a major architecture shift** — The 2026-07-28 release candidate makes MCP stateless, removes session management, adds the Extensions framework, MCP Apps (server-rendered UIs), and Tasks. The original module only covered basic MCP tool calling.

2. **A2A has reached v1.0 and is now Linux Foundation-governed** — Google's Agent-to-Agent protocol went from announcement (April 2025) to 150+ organisations in production by June 2026. The original module mentioned A2A but didn't cover its maturity, Agent Cards, gRPC support, or how it complements MCP.

3. **The MCP vs A2A clarity is now critical** — The "MCP gives agents hands, A2A gives agents colleagues" framing is industry consensus in 2026. Students will encounter both in production and need a decision framework.

4. **Multi-agent failure taxonomy is now well-documented** — The MAST taxonomy (NeurIPS 2025) identifies 14 failure modes across 1,600+ execution traces. 41% of failures are specification problems, 37% coordination, 21% verification gaps. The original module covered reliability patterns but not this systematic taxonomy.

5. **Production failure rates are alarmingly high** — 40-87% of multi-agent pilots fail within 6 months. The original module was optimistic about multi-agent systems without covering the "when NOT to use multi-agent" question.

6. **OpenAI Agents SDK replaced Swarm** — The production successor to Swarm introduced handoffs and agents-as-tools as first-class patterns. The original module referenced Swarm which is now deprecated.

7. **AutoGen is in maintenance mode** — Microsoft merged AutoGen with Semantic Kernel into the Microsoft Agent Framework (Oct 2025). AG2 forked as the community continuation. The original module discussed AutoGen as a current option.

8. **CrewAI v1.0+ removed LangChain dependency** — CrewAI now builds its own tool abstractions and has Flows for structured orchestration. 54K+ GitHub stars by mid-2026.

9. **LangGraph is the production default** — Enterprise consensus in 2026: "Pick LangGraph unless you have an explicit reason for the other two." State-graph orchestration with MCP for tools is the dominant architecture.

10. **Amazon Bedrock multi-agent collaboration is GA with Inline Agents** — Dynamic runtime behaviour adjustment, Amazon Nova models for multi-agent, Managed Agents preview. The original module predated GA.

---

## NEW & UPDATED SLIDES

---

### [NEW 2026] Slide: The Protocol Layer — MCP + A2A as Complements
**Insert after:** Communication protocols section
**Format:** Concept explanation with comparison table

The 2026 consensus is clear: MCP and A2A are **complements, not competitors**. They solve different problems at different layers:

| Dimension | MCP (Model Context Protocol) | A2A (Agent-to-Agent) |
|---|---|---|
| **What it connects** | An agent to tools, data, and services | An agent to other agents |
| **Analogy** | "Gives your agent hands" | "Gives your agent colleagues" |
| **Communication model** | Client-server (agent calls tool) | Peer-to-peer (agent delegates to agent) |
| **Visibility** | Agent sees tool internals (schemas, parameters) | Agent sees only the capability card — black box |
| **Primary use case** | Tool access and context injection | Task delegation and cross-framework interop |
| **Protocol basis** | JSON-RPC 2.0 | HTTP + JSON-RPC (gRPC as of July 2025) |
| **Governance** | Linux Foundation (donated Dec 2025) | Linux Foundation (donated June 2025) |
| **Adoption (mid-2026)** | 97M monthly SDK downloads, 10K+ servers | 150+ orgs routing real tasks in production |

**Decision framework:**
- Single agent needing to access tools/APIs → **MCP**
- Multiple agents from different frameworks coordinating → **A2A**
- Production system doing both tool access and agent coordination → **Both (MCP + A2A)**

> *"MCP answers 'how does one agent reach the systems it needs.' A2A answers 'how do two agents that don't share a codebase work together.'"* — Beam.ai, 2026

**Facilitator Notes:**
- Open with the question: "If MCP and A2A both handle agent communication, why do we need both?" Let students discuss for 2 min before revealing the layer distinction
- Common confusion: students think A2A replaces MCP or vice versa. The Oracle blog has the clearest framing: "agents use A2A for coordination and MCP for tool access"
- Draw the stack on a whiteboard: Application → A2A layer (agent-to-agent) → MCP layer (agent-to-tool) → External services
- Time: 5 minutes

---

### [NEW 2026] Slide: MCP 2026 — The Stateless Revolution
**Insert after:** MCP + A2A as Complements slide
**Format:** Technical explanation with before/after code

The MCP 2026-07-28 specification release candidate (shipping July 2026) is the largest revision since launch. The headline change: **MCP is now stateless at the protocol layer.**

**What changed:**
- ❌ `initialize` / `initialized` handshake → **removed**
- ❌ `Mcp-Session-Id` header → **removed**
- ✅ Every request is self-contained — any server instance can handle it
- ✅ Protocol version + client info now travels in `_meta` on every request
- ✅ Routing via `Mcp-Method` and `Mcp-Name` headers (no body inspection needed)
- ✅ Caching with `ttlMs` and `cacheScope` on list responses
- ✅ W3C Trace Context propagation (OpenTelemetry integration)

**Before (2025-11-25):**
```http
POST /mcp HTTP/1.1
Mcp-Session-Id: 1868a90c-3a3f-4f5b

{"jsonrpc":"2.0","id":2,"method":"tools/call",
 "params":{"name":"search","arguments":{"q":"otters"}}}
```
Required sticky sessions + shared session store + deep packet inspection.

**After (2026-07-28):**
```http
POST /mcp HTTP/1.1
MCP-Protocol-Version: 2026-07-28
Mcp-Method: tools/call
Mcp-Name: search

{"jsonrpc":"2.0","id":1,"method":"tools/call",
 "params":{"name":"search","arguments":{"q":"otters"},
           "_meta":{"io.modelcontextprotocol/clientInfo":{"name":"my-app","version":"1.0"}}}}
```
Runs behind plain round-robin load balancer. No sticky sessions needed.

**New Extensions framework:**
- **MCP Apps** — servers can ship interactive HTML UIs rendered in sandboxed iframes
- **Tasks** — long-running work with lifecycle management (graduated from experimental to extension)
- Extensions identified by reverse-DNS IDs, versioned independently of spec

**Facilitator Notes:**
- This is dense — focus on WHY it matters (horizontal scaling) rather than the full HTTP details
- Key takeaway for students: "MCP is now as scalable as any REST API — this was the main complaint in production"
- ⚡ ADVANCED: The `requestState` pattern for multi-round-trip requests is elegant — show the elicitation flow for advanced audiences
- Common question: "Does stateless mean my agent can't have state?" Answer: No — you just manage it explicitly (mint a handle from a tool, pass it back as argument)
- Time: 5 minutes

---

### [NEW 2026] Slide: A2A Protocol Deep-Dive — Agent Cards & Task Lifecycle
**Insert after:** MCP 2026 slide
**Format:** Technical concept with diagrams

Google's Agent-to-Agent protocol reached v1.0 in 2026 under Linux Foundation governance. Key concepts:

**Agent Card (Discovery):**
Every A2A-compliant agent publishes a JSON "Agent Card" at a well-known URL describing:
- Agent name, description, capabilities
- Accepted input formats and output formats
- Authentication requirements
- Supported task types

Think of it as a resume that other agents can read to decide whether to delegate a task.

**Task Lifecycle:**
```
[Client Agent] --sends task--> [Remote Agent]
         ↓
    Task Created (pending)
         ↓
    Task Working (streaming updates via SSE)
         ↓
    Task Completed (returns artifacts)
         or
    Task Failed / Input Required
```

**Key A2A v1.0 features (2026):**
- gRPC support (added July 2025) for high-throughput scenarios
- Cryptographically signed security cards
- Extended Python SDK
- Support for streaming partial results during long-running tasks
- Artifact sharing between agents

**Production reality (June 2026):**
- 150+ organisations routing real tasks between agents in production
- Google ADK (Agent Development Kit) natively supports A2A
- Cross-language coordination demonstrated (Python agent + Go agent in one pipeline)

**Facilitator Notes:**
- Demo opportunity: show an Agent Card JSON and walk through each field
- The Task lifecycle is intuitive — compare it to a Jira ticket (pending → in progress → done)
- For advanced: discuss the security implications of agent discovery — how do you trust an Agent Card?
- Time: 4 minutes

---

### [NEW 2026] Slide: The MAST Failure Taxonomy — Why Multi-Agent Systems Break
**Insert after:** Designing for reliability section
**Format:** Concept explanation with data

Research from NeurIPS 2025 (Datasets & Benchmarks Track spotlight) analyzed 1,600+ execution traces across seven popular multi-agent frameworks and identified 14 failure modes in three categories:

**The Numbers:**
- Multi-agent LLM systems fail at rates between **41–87%** in production
- **40% of multi-agent pilots fail** within 6 months of deployment
- These two failure categories account for **79% of all breakdowns**

**MAST Taxonomy — Three Root Categories:**

| Category | % of Failures | What Goes Wrong | Fix |
|---|---|---|---|
| **Specification Problems** | 41.8% | Role ambiguity, unclear task definitions, missing constraints — agents "figure it out" incorrectly | Treat specs like API contracts. JSON schemas for everything. Explicit ownership. |
| **Coordination Failures** | 36.9% | Communication breakdowns, state sync issues, conflicting objectives | Structured protocols (MCP/A2A). Typed messages. Schema validation on every exchange. |
| **Verification Gaps** | 21.3% | No testing, missing validation, absent output quality checks | Independent verifier agent. Rules-based + LLM-as-judge dual validation. |

**The honest truth:**
> *"Most of what looked like 'more agents means more intelligence' was just redundant rearrangement of the same information."* — Lanham, 2026

**When to NOT use multi-agent:**
- Task can be solved by one well-prompted agent
- Information doesn't need to be partitioned for security/access control
- Coordination cost would exceed the benefit of specialisation
- Total steps < 5 (overhead isn't worth it)

**Facilitator Notes:**
- This slide is crucial — it rebalances the module from "multi-agent is great" to "multi-agent is powerful but treacherous"
- Lead with the failure rates to create urgency before the taxonomy
- Discussion prompt: "Has anyone shipped a multi-agent system that failed in a way they can now categorise?"
- Common student reaction: "So should I just use a single agent?" — Guide to "single agent first, multi-agent when you have a clear decomposition reason"
- Time: 6 minutes

---

### [NEW 2026] Slide: Six Canonical Orchestration Patterns (2026)
**Insert after:** MAST Failure Taxonomy slide
**Format:** Comparison table with use case mapping

Production multi-agent systems in 2026 map to six canonical patterns:

| Pattern | How It Works | Best For | Failure Mode | Cost Profile |
|---|---|---|---|---|
| **Sequential (Pipeline)** | A → B → C linear chain | Document processing, ETL | Single point of failure; bottleneck at slowest stage | Low (sequential token use) |
| **Parallel (Fan-out/Fan-in)** | Spawn N agents, merge results | Research, batch extraction | Merge conflicts; inconsistent outputs | High (concurrent token use) |
| **Supervisor-Worker** | One agent plans, others execute | Complex tasks with clear decomposition | Supervisor becomes bottleneck; workers idle-wait | Medium |
| **Hierarchical** | Multi-level delegation tree | Enterprise workflows, large-scale ops | Coordination cost scales exponentially past 3 levels | High |
| **State-Graph** | Nodes + edges with explicit transitions (LangGraph) | Stateful workflows needing retries/branching | Graph complexity; hard to debug large graphs | Medium |
| **Swarm (Peer-to-Peer)** | Agents hand off dynamically via context | Customer service, adaptive routing | Context loss at handoff; circular routing | Variable |

**Decision framework for choosing:**
1. Is the task decomposable into independent subtasks? → **Parallel**
2. Does task ordering matter? → **Sequential**
3. Is there a natural planning/execution split? → **Supervisor-Worker**
4. Do you need retries, branching, and state? → **State-Graph**
5. Is the routing dynamic and context-dependent? → **Swarm**
6. Is the org structure itself hierarchical? → **Hierarchical**

**Facilitator Notes:**
- Students need to match patterns to their real-world problems — ask them to categorise their planned use cases
- Key insight: "Most production systems in 2026 are hybrids — they use 2-3 patterns at different levels"
- Emphasise: "Past 3 agents, coordination costs scale exponentially" — this is the #1 production lesson
- Time: 5 minutes

---

### [NEW 2026] Slide: Framework Landscape 2026 — What Actually Survived Production
**Insert after:** Six Patterns slide
**Format:** Comparison table

| Framework | Status (mid-2026) | Architecture | Best For | Key Gotcha |
|---|---|---|---|---|
| **LangGraph** | ✅ Production default | State-graph (nodes + edges); explicit control flow | Planner-executor, hierarchical, anything needing retries/debugging | Graph complexity grows fast; steep learning curve |
| **CrewAI** | ✅ Active (v1.14+) | Role-based teams; manager + workers | Quickest path to role-based multi-agent; easiest for non-engineers | Removed LangChain dep in v1.0; less fine-grained control than LangGraph |
| **OpenAI Agents SDK** | ✅ Production (replaced Swarm) | Code-first; Runner class; handoffs + agents-as-tools | OpenAI model users wanting native multi-agent | Vendor lock-in; handoff patterns only |
| **AutoGen** | ⚠️ Maintenance mode | Event-driven, actor model (v0.4) | Research; collaborative conversation patterns | Microsoft merged into Agent Framework (Oct 2025); no new features |
| **AG2** | ✅ Community fork of AutoGen | AgentOS; orchestration + observability + governance | Production successor for AutoGen users | Smaller community than LangGraph |
| **Amazon Bedrock Agents** | ✅ GA multi-agent collaboration | Supervisor-sub agent; inline agents for runtime flexibility | AWS-native shops; managed infra | Less customisable than open-source options |

**2026 Enterprise consensus:**
> *"Pick LangGraph + MCP for tools unless you have an explicit reason for the other two."* — Internative.net framework comparison, June 2026

**Key shifts from 2024–2025:**
- AutoGen → maintenance mode (biggest surprise)
- Swarm → replaced by OpenAI Agents SDK (same patterns, production-grade)
- CrewAI → removed LangChain, went GA, 54K+ GitHub stars
- LangGraph → became the "React of multi-agent" — dominant through developer experience

**Facilitator Notes:**
- This landscape changes fast — flag the date of this information (mid-2026) and remind students to verify
- Common question: "Should I learn LangGraph or CrewAI?" → Answer depends on role: engineers → LangGraph; product teams prototyping → CrewAI
- ⚡ ADVANCED: Discuss why AutoGen's maintenance announcement matters — what it means for choosing frameworks with long-term support
- Time: 5 minutes

---

### [NEW 2026] Slide: OpenAI Agents SDK — Handoffs vs Agents-as-Tools
**Insert after:** Framework Landscape slide
**Format:** Technical comparison with code

OpenAI's Agents SDK (successor to the experimental Swarm framework) provides two multi-agent patterns:

**Pattern 1: Handoffs (Delegation Chain)**
Agent finishes its piece and explicitly transfers control. The receiving agent responds directly to the user.
```python
from agents import Agent, handoff

triage_agent = Agent(
    name='Triage',
    instructions='Route to the right specialist',
    handoffs=[
        handoff(billing_agent),
        handoff(technical_agent)
    ]
)
```
- Specialist becomes the active agent for the rest of the turn
- Like a relay race — baton passes, previous runner stops
- Best for: customer service routing, triage → specialist flows

**Pattern 2: Agents-as-Tools (Orchestrator)**
Orchestrator calls specialists as tools — they return results but don't take over the conversation.
```python
from agents import Agent, agent_tool

researcher = Agent(name='Researcher', instructions='...')
writer = Agent(name='Writer', instructions='...')

orchestrator = Agent(
    name='Orchestrator',
    tools=[agent_tool(researcher), agent_tool(writer)]
)
```
- Orchestrator maintains control throughout
- Specialists handle bounded subtasks and return results
- Best for: complex workflows where one agent needs to synthesise across multiple specialist outputs

**When to use which:**
| Signal | Use Handoffs | Use Agents-as-Tools |
|---|---|---|
| Specialist should respond directly | ✅ | ❌ |
| Need to combine multiple specialist outputs | ❌ | ✅ |
| Want focused, swapped-out instructions | ✅ | ❌ |
| Orchestrator must narrate/synthesise | ❌ | ✅ |

**Facilitator Notes:**
- Live demo opportunity: build a 3-agent customer service system with one triage agent and two specialists
- Key insight: "Handoffs are simpler but you lose orchestrator control; agents-as-tools keep control but add token cost"
- Compare to CrewAI's manager pattern (similar to agents-as-tools) and LangGraph's graph edges (similar to handoffs)
- Time: 5 minutes

---

### [NEW 2026] Slide: Amazon Bedrock Multi-Agent Collaboration (GA)
**Insert after:** OpenAI Agents SDK slide
**Format:** Technical overview with architecture

Amazon Bedrock multi-agent collaboration went **GA in March 2025** with key capabilities:

**Architecture:**
```
[Supervisor Agent]
    ├── [Sub-Agent 1: Flight Search]
    ├── [Sub-Agent 2: Hotel Booking]  
    └── [Sub-Agent 3: Itinerary Planning]
```
Bedrock handles orchestration, task delegation, and inter-agent communication automatically.

**Inline Agents (2025):**
Dynamically adjust agent behaviour at runtime — no redeployment needed:
- Change instructions, tools, guardrails, knowledge bases, prompts, and foundation model at runtime
- Enable rapid prototyping (eliminate create/update/prepare cycles)
- Support role-based access: same codebase, different capabilities per user

**Amazon Nova models for multi-agent (2026):**
- Amazon Nova 2 Lite + Amazon Nova Act designed for multi-agent coordination
- One agent plans and communicates with user; others handle specific tasks
- Simple message-based inter-agent communication

**Managed Agents (Limited Preview, April 2026):**
- Bedrock now offers OpenAI models + Codex alongside Anthropic/Mistral/Amazon Nova
- Managed lifecycle — Bedrock handles scaling, versioning, deployment

**When to choose Bedrock multi-agent:**
- Already on AWS and want managed infrastructure
- Need guardrails enforcement across all agents (centralised)
- Want runtime flexibility (Inline Agents)
- Don't need the fine-grained graph control of LangGraph

**Facilitator Notes:**
- For AWS-centric audiences, this is the "production path of least resistance" — emphasise operational simplicity
- Demo: walk through creating a supervisor + 2 sub-agents in the Bedrock console
- Compare: Bedrock multi-agent is more opinionated (supervisor pattern enforced) vs LangGraph (any pattern)
- Time: 4 minutes

---

### [NEW 2026] Slide: Specification-Driven Multi-Agent Design
**Insert after:** MAST Failure Taxonomy slide
**Format:** Best practice with code example

Since 41.8% of multi-agent failures come from specification problems, production teams now treat agent specifications like **API contracts**, not documentation:

**Anti-pattern (vague prose):**
> "The research agent should find relevant information and pass it to the writer."

**Production pattern (schema-driven):**
```json
{
  "agent_id": "researcher_01",
  "role": "Find and validate data from approved sources",
  "capabilities": ["web_search", "pdf_extraction", "fact_checking"],
  "constraints": {
    "max_iterations": 5,
    "timeout_seconds": 120,
    "approved_sources": ["arxiv.org", "nature.com", "*.gov"],
    "forbidden_actions": ["modify_files", "send_emails"]
  },
  "success_criteria": [
    "At least 3 cited sources per claim",
    "All facts cross-referenced against second source",
    "Output schema: {title, summary, sources[], confidence_score}"
  ],
  "handoff_protocol": {
    "output_format": "structured_json",
    "max_output_tokens": 2000,
    "required_fields": ["findings", "confidence", "sources"]
  }
}
```

**Key principles:**
1. **Explicit ownership** — Every resource, tool, and output has exactly one owner
2. **Schema validation** — Inputs and outputs validated at every boundary
3. **Constraint enforcement** — Max iterations, timeouts, and forbidden actions prevent runaway agents
4. **Success criteria** — Measurable, checkable conditions (not "do a good job")
5. **Living specs** — Specification updates as agents complete work; drift eliminated

**PwC production result:** 7× accuracy gains through structured orchestration vs unstructured.

**Facilitator Notes:**
- This is the single highest-ROI practice for multi-agent reliability
- Activity opportunity: have students write a specification for a 3-agent system using this template
- Common pushback: "This is too rigid" — counter with "41% of failures come from NOT doing this"
- Time: 5 minutes

---

### [NEW 2026] Slide: The Coordinator-Specialist-Verifier Pattern
**Insert after:** Specification-Driven Design slide
**Format:** Architecture pattern

The three most reliable production multi-agent systems (per NeurIPS MAST study) all use a variation of this three-role pattern:

```
┌─────────────────────────────────────┐
│          COORDINATOR                │
│  Plans work, assigns tasks,         │
│  manages state, resolves conflicts  │
└────────┬──────────────┬─────────────┘
         │              │
    ┌────▼────┐   ┌────▼────┐
    │SPECIALIST│   │SPECIALIST│   (N specialists)
    │ Domain   │   │ Domain   │
    │ expert   │   │ expert   │
    └────┬────┘   └────┬────┘
         │              │
         └──────┬───────┘
         ┌──────▼───────┐
         │   VERIFIER   │
         │ Independent  │
         │ quality gate │
         └──────────────┘
```

**Why this works:**
- **Coordinator** eliminates specification ambiguity (41.8% of failures) by providing explicit, structured task assignments
- **Structured protocols** between roles eliminate coordination failures (36.9% of failures)
- **Verifier** eliminates verification gaps (21.3% of failures) through independent validation

**The Verifier is not optional:**
- Must be a SEPARATE agent (not the coordinator checking its own work)
- Should use a different model or temperature than specialists (independence)
- Implements both rules-based checks AND LLM-as-judge assessment
- Returns {pass, fail, revise} with structured feedback

**Facilitator Notes:**
- This maps directly to the MAST taxonomy — each role addresses one failure category
- Discussion: "Why must the verifier be independent?" (Same reason auditors can't audit themselves)
- For advanced: discuss how to implement this in LangGraph (coordinator = entry node, specialists = parallel nodes, verifier = gate node before output)
- Time: 4 minutes

---

### [NEW 2026] Slide: Production Anti-Patterns — Lessons from 2025-2026
**Insert after:** Coordinator-Specialist-Verifier slide
**Format:** Anti-patterns list with corrections

| Anti-Pattern | What Happens | Fix |
|---|---|---|
| **"More agents = more intelligence"** | Redundant rearrangement of same information; coordination cost > value | Start with 1 agent. Add agents only when decomposition creates clear value. |
| **Stateless handoffs** | Context lost at agent boundaries; receiving agent hallucinates due to missing state | Include structured context summary at every handoff. Schema-validate handoff payloads. |
| **Free-form inter-agent messaging** | Agents misinterpret intent; 37% coordination failures | Typed messages (request/inform/commit/reject). Schema validation on every exchange. |
| **The MIT "Stalled Pilot" syndrome** | 95% of AI agent pilots stalled in 2025. Same three root causes: stateless handoffs, race conditions, infinite loop drift | Design for failure from day 1. Max iteration caps. Deadlock detection. Circuit breakers. |
| **Circular routing** | Agent A delegates to Agent B, which delegates back to A | Explicit delegation graphs with no-return-to-sender rule. Track delegation chain. |
| **Exponential coordination past 3 agents** | Token waste explodes; outputs break silently | Hard limit: justify every agent beyond 3. Use single agent with multiple tools instead. |

**The honest number:**
> *"Past 3 agents, coordination costs scale exponentially. Token waste explodes. Outputs break silently."* — MIT multi-agent study, 2025

**Facilitator Notes:**
- Lead with "What's the worst multi-agent failure you've seen or read about?" to collect real examples
- The "more agents = more intelligence" anti-pattern is the most common misconception in the room
- Emphasise: "The best multi-agent system is the one with the fewest agents that still works"
- SKIP FOR BEGINNERS: the MIT stalled pilot details are advanced
- Time: 4 minutes

---

### [NEW 2026] Slide: LangGraph Supervisor vs Swarm — Live Comparison
**Insert after:** Framework Landscape slide
**Format:** Technical comparison with code snippets

LangGraph offers two production multi-agent patterns. Here's the same customer service scenario built both ways:

**Supervisor Pattern:**
```python
from langgraph.prebuilt import create_react_agent
from langgraph.graph import StateGraph

# Define specialist agents
billing_agent = create_react_agent(model, tools=[lookup_invoice, process_refund])
tech_agent = create_react_agent(model, tools=[check_status, restart_service])

# Supervisor routes based on intent
supervisor = StateGraph(...)
supervisor.add_node("billing", billing_agent)
supervisor.add_node("technical", tech_agent)
supervisor.add_conditional_edges("router", route_by_intent)
```
- Explicit control flow (graph edges define routing)
- Maximum debuggability (can visualise the graph)
- Supervisor sees all state; can override/retry

**Swarm Pattern:**
```python
from langgraph.prebuilt import create_swarm

agents = [billing_agent, tech_agent, general_agent]
swarm = create_swarm(agents, default=general_agent)
# Agents hand off via tool calls — dynamic routing
```
- Agents decide who handles next (via handoff tools)
- More flexible but less predictable
- Good for: open-ended conversations where routing is context-dependent

**When to use which:**
- Known routing rules → **Supervisor** (graph edges encode the rules)
- Dynamic/context-dependent routing → **Swarm** (let agents decide)
- Need retries and error handling → **Supervisor** (graph has retry edges)
- Rapid prototyping → **Swarm** (less boilerplate)

**Facilitator Notes:**
- ⚡ ADVANCED — this slide is for engineers who will implement
- Live coding demo: build the supervisor version in 15 lines, show the graph visualisation
- Key insight: "Supervisor is just a state machine where the LLM picks transitions"
- Common question: "Can I mix both?" — Yes, supervisor at top level, swarm within a specialist subgraph
- Time: 5 minutes

---

### [NEW 2026] Slide: MCP Security Considerations for Multi-Agent
**Insert after:** Production Anti-Patterns slide
**Format:** Security focus

As MCP becomes the standard tool layer, new attack surfaces emerge:

**MCP-specific threats in multi-agent systems:**
1. **Tool poisoning** — Malicious MCP server returns manipulated data to influence agent behaviour
2. **Privilege escalation via tool chaining** — Agent A has tool access that Agent B shouldn't have; if A delegates to B with A's MCP session, B inherits A's privileges
3. **Schema manipulation** — MCP server changes tool schema mid-session to trick agent into passing sensitive data
4. **Rug-pull attacks** — Agent Card advertises safe capabilities, then serves different tools after trust is established

**MCP 2026 mitigations:**
- Server-initiated requests only allowed while processing a client request (no surprise prompts)
- W3C Trace Context propagation for full audit trail
- OAuth + OpenID Connect alignment for enterprise auth
- Tool annotations mark read-only vs destructive operations

**Multi-agent security principles:**
- Each agent gets its own MCP connection with minimum privilege
- Inter-agent messages must be schema-validated (never pass raw text between agents)
- Verify Agent Cards against a trusted registry before delegation
- Monitor for circular delegation and unexpected tool access patterns

**Facilitator Notes:**
- Connect to Module 14 (AI Security & Trust) — this is the multi-agent extension of prompt injection
- Key point: "The more agents you have, the larger your attack surface — each agent is a potential entry point"
- For advanced: discuss the "confused deputy" problem in multi-agent contexts
- Time: 4 minutes

---

### [NEW 2026] Slide: Observability for Multi-Agent Systems
**Insert after:** MCP Security slide
**Format:** Technical best practice

Standard APM doesn't work for multi-agent systems. What you need:

**The Multi-Agent Observability Stack:**
```
┌──────────────────────────────────────────┐
│ Distributed Traces (OpenTelemetry)       │  ← One trace per user request,
│ Spans per agent turn, tool call, handoff │    spans across all agents
├──────────────────────────────────────────┤
│ Token/Cost Attribution                   │  ← Per-agent, per-task cost
│ Which agent is burning budget?           │    tracking
├──────────────────────────────────────────┤
│ Semantic Metrics                         │  ← Coordination success rate,
│ Handoff accuracy, delegation quality     │    verification pass rate
├──────────────────────────────────────────┤
│ State Machine Replay                     │  ← Replay any multi-agent
│ Full execution trace with decisions      │    conversation for debugging
└──────────────────────────────────────────┘
```

**What to instrument:**
- Coordination overhead ratio: (coordination tokens) / (useful work tokens)
- Handoff success rate: % of handoffs that don't require retries
- Circular delegation detection: alert on A→B→A patterns
- Time-to-completion by pattern: supervisor vs swarm vs sequential
- Agent utilisation: which agents are idle-waiting?

**MCP 2026 helps:** W3C Trace Context propagation means a single trace follows a request from the user through the orchestrator, through each agent's MCP tool calls, and back — as one span tree in any OpenTelemetry backend.

**Facilitator Notes:**
- Connect to Module 15 (Observability) — this is the multi-agent specific extension
- Key insight: "The coordination overhead ratio is the single best metric for knowing if you have too many agents"
- Demo: show a Langfuse or Phoenix trace of a multi-agent execution
- Time: 4 minutes

---

### [NEW 2026] Slide: Hands-On Activity — Design a Multi-Agent System
**Insert after:** All content slides
**Format:** Lab / activity

**Activity: Multi-Agent Architecture Decision Lab (15 min)**

**Scenario:** Your company's customer support receives 10,000 tickets/day across billing, technical, and account management. You've been asked to design a multi-agent system to handle tier-1 resolution.

**Instructions:**
1. Choose an orchestration pattern from the six canonical patterns (justify why)
2. Define your agent roles using the specification schema template (3 agents minimum)
3. Decide: MCP for tools, A2A for agent communication, or both?
4. Draw the communication flow (who talks to whom, in what order)
5. Identify the top 3 failure modes from MAST taxonomy that could hit your design
6. Add a Verifier — what does it check, and when?
7. Specify your observability: what 3 metrics would you alert on?

**Expected Deliverable:** One-page architecture diagram + specification for each agent + failure mode analysis

**Facilitator Notes:**
- Have students work in pairs or small groups
- Walk the room — common mistake is over-engineering (too many agents)
- Best answers will justify "we only need 3 agents because..."
- Share one group's answer with the class for 3-min discussion
- Time: 15 minutes total (10 work + 5 share)

---

### [UPDATE 2026] Slide: Updated Recommended Resources
**Insert after:** Original resources section
**Format:** Resource list

**Replace/supplement the original resources with these 2026-current sources:**

| Category | Resource |
|---|---|
| **Specification** | MCP Spec 2026-07-28 RC — blog.modelcontextprotocol.io |
| **Specification** | A2A v1.0 Spec — github.com/a2aproject/A2A |
| **Framework** | LangGraph Multi-Agent Docs — langchain-ai.github.io/langgraph |
| **Framework** | CrewAI v1.14 Docs — docs.crewai.com |
| **Framework** | OpenAI Agents SDK — github.com/openai/openai-agents-python |
| **AWS** | Amazon Bedrock Multi-Agent Collaboration — docs.aws.amazon.com/bedrock |
| **Research** | MAST: Multi-Agent System Failure Taxonomy (NeurIPS 2025) |
| **Research** | "LLM-Based Multi-Agent Orchestration: A Survey" — preprints.org (July 2026) |
| **Production** | "Multi-Agent in Production 2026: What Actually Survived" — Medium |
| **Blog** | "The Agent Communication Matrix" — Oracle Developers Blog (June 2026) |
| **Blog** | "A Year of A2A" — Google Open Source Blog (April 2026) |
| **Comparison** | "LangGraph vs CrewAI vs AutoGen: 2026 Framework Comparison" — Internative.net |

**Facilitator Notes:**
- The MCP and A2A specs are must-reads for engineers
- The MAST taxonomy paper is the most citable academic reference for "why multi-agent fails"
- The Internative.net comparison is the most balanced framework comparison available
- Time: 1 minute (quick slide, hand out as reading list)

---

## FACILITATOR UPDATE BRIEF

### 🔥 Top 3 Most Important Additions

1. **MAST Failure Taxonomy + Production Failure Rates** — This rebalances the module from "multi-agent is exciting" to "multi-agent is powerful but fails 40-87% of the time in production without discipline." The Coordinator-Specialist-Verifier pattern and specification-driven design directly address the top causes.

2. **MCP 2026 (Stateless) + A2A v1.0 as complements** — Students will encounter both protocols in the wild. The "MCP = agent-to-tool, A2A = agent-to-agent" framing is now consensus and should be taught as the primary mental model for multi-agent communication.

3. **Framework landscape shift** — AutoGen is in maintenance mode, OpenAI Agents SDK replaced Swarm, LangGraph is the production default. This needs updating because students will Google frameworks and get confused by outdated content recommending AutoGen.

### ⚠️ What's Now Outdated in the Original Module

| Original Content | Status | How to Address |
|---|---|---|
| AutoGen as a current framework option | ❌ Maintenance mode (Oct 2025) | Mention it historically; redirect to AG2 or LangGraph |
| OpenAI Swarm as a framework | ❌ Deprecated | Replace with OpenAI Agents SDK (same patterns, production-grade) |
| MCP as a basic tool calling protocol | 🔄 Significantly evolved | Update to MCP 2026 (stateless, extensions, apps, tasks) |
| A2A as "emerging/new" | 🔄 Now GA v1.0 | Update to A2A v1.0 with Linux Foundation governance, 150+ orgs |
| Bedrock multi-agent as preview | 🔄 Now GA | Update to GA status with Inline Agents + Amazon Nova |

### ⏱️ Time Allocation for 60-Minute Module

The new content expands this significantly. Recommended approach:

**Standard delivery (60 min):**
- Cut original framework details on AutoGen/Swarm (saves 5 min)
- Add MCP+A2A complement slide (5 min)
- Add MAST taxonomy + anti-patterns (6 min)
- Add framework landscape 2026 (5 min)
- Add specification-driven design (5 min)
- Keep hands-on activity (15 min)
- Net: fits in 60 min with tighter original pacing

**Extended delivery (90 min — RECOMMENDED):**
- All original content (updated)
- All new slides
- Extended hands-on activity (20 min instead of 15)
- 5-min discussion on "lessons from your org's multi-agent attempts"

### 🛠️ New Tools/Accounts/Demos to Set Up

1. **LangGraph Studio** — Free desktop app for visualising and debugging multi-agent graphs. Set up a 3-agent demo before class.
2. **MCP Inspector** — CLI tool for testing MCP servers. Show the stateless request/response.
3. **AWS Console** — Bedrock multi-agent collaboration demo with 2 sub-agents. Pre-create and test.
4. **A2A Playground** — github.com/a2aproject has sample implementations. Pre-run the Python example.
5. **Langfuse or Phoenix** — Set up a multi-agent trace demo showing spans across agents (connects to Module 15).

---

*Module 12 Update — Generated July 2026*
*Sources: MCP spec blog, Google A2A docs, NeurIPS 2025 MAST paper, Augment Code production analysis, Internative.net framework comparison, AWS Bedrock documentation, OpenAI Agents SDK docs*
