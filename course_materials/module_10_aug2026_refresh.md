# Module 10 — AI on AWS: The Bedrock-to-SageMaker Stack
## [NEW AUG-2026] Content Refresh Addendum
### Updated: 12 August 2026

---

## A) EXECUTIVE SUMMARY — What Changed Since July 2026

1. **Amazon deprecates 4 Nova models (July 28)** — Nova Premier, Omni, Reel, and Canvas are being wound down. Amazon is consolidating into a single frontier-model effort led by Pieter Abbeel, due at re:Invent 2026. Nova 2 Pro/Lite remain active for now but the strategic direction has fundamentally shifted.

2. **OpenAI GPT-5.6 family launches (July 9) and hits Bedrock (Aug 4–11)** — Three tiers: Luna (fastest/cheapest, 80% price cut July 30), Terra (balanced, 20% price cut), and Sol (frontier intelligence). Specialized Daybreak Red/Blue cybersecurity variants added Aug 11. Bedrock now has web search built-in for all GPT models.

3. **OpenAI–Amazon strategic partnership deepens (Aug 10–11)** — Co-creation of a Stateful Runtime Environment on Bedrock. Amazon invested $50B in OpenAI. OpenAI Managed Agents now available on AWS. This is a paradigm shift in the platform relationship.

4. **AgentCore Runtime Instances GA (Aug 6)** — Dedicated EC2-backed runtime for agents (not just microVMs). Shared sessions persist up to 14 days. Provides more predictable costs and greater execution control for enterprise agent deployments.

5. **Kiro Crew open-sourced (Aug 4)** — AWS released Kiro Crew under Apache 2.0. Turns Kiro from an interactive coding assistant into a persistent agent platform that works across sessions, machines, and events. Major evolution of the developer tooling story.

6. **Bedrock Web Search GA (Aug 4)** — Built-in web grounding for OpenAI models on Bedrock, using MCP via AgentCore Gateway. Integration is one JSON object: `{"type": "web_search"}`.

7. **Anthropic Claude model explosion** — Claude Fable 5 (June 9), Claude Sonnet 5 (June 30), Claude Opus 5 (July 24), Claude Opus 4.7/4.8 updates. Text watermarking deployed globally (Aug 2). Auto-mode default for Claude Code (Aug 14).

8. **AWS Dogwood: Runtime verification for AI agents (Aug 6)** — Open-source policy language for expressing sequential, temporal, and rate-limited constraints on agent actions. Critical for governance.

9. **DynamoDB native vector search GA (Aug 5)** — Store embeddings alongside operational data. Eliminates need for separate vector databases in many AI application patterns.

10. **AWS Context + Ontology Accelerator** — Knowledge graph service for AI agents (Summit NYC June 17), with Ontology Accelerator GA July 31. Agents can now access governed data relationships and business rules at runtime.

---

## B) NEW SLIDES

---

### [NEW AUG-2026] Slide: The Nova Strategy Reset — What It Means
**Insert after:** Existing Nova model family slide (Slide 2 in July update)
**Source:** Business Insider (July 28, 2026), Reuters, The Next Web, Technology.org

**Content:**

⚠️ **BREAKING: Amazon is winding down most Nova models**

As of July 28, 2026, Amazon has begun deprecating:
- **Nova Premier** (high-end reasoning)
- **Nova Omni** (multimodal)
- **Nova Reel** (video generation)
- **Nova Canvas** (image generation)

**What remains active (for now):**
- **Nova 2 Pro** — balanced workloads, agentic tasks
- **Nova 2 Lite** — cost-efficient automation
- **Nova Act** — browser automation (separate team)

**The new strategy:**
- All resources redirected to a **single frontier model** effort
- Led by **Pieter Abbeel** (UC Berkeley robotics/AI professor recruited to Amazon)
- Expected to debut at **re:Invent 2026** (December)
- Amazon is effectively conceding that a broad portfolio approach didn't work
- The company is betting on one genuinely competitive foundation model

**What this means for architects:**
- Don't build new systems on Nova Premier or Omni — plan migrations
- Nova 2 Pro/Lite remain safe for production use cases *today*
- Bedrock's multi-model approach is MORE important than ever (switch models easily)
- The OpenAI partnership becomes strategically critical as Amazon's own frontier capability regroups

**Facilitator Notes:**
- 🎤 "This is big news that broke just 2 weeks ago. Amazon is admitting that spreading resources across many model variants didn't produce frontier-competitive results. They're going all-in on one bet."
- Student concern: "Should I use Nova at all?" — Nova 2 Lite/Pro are still excellent for cost-efficient agentic workloads. For frontier reasoning, use Claude or GPT-5.6.
- This underscores why Bedrock's model-agnostic architecture matters — you're never locked in.
- Time: 5 minutes

---

### [NEW AUG-2026] Slide: GPT-5.6 on Bedrock — The Three-Tier Intelligence Ladder
**Insert after:** OpenAI on Bedrock slide (Slide 3 in July update)
**Source:** OpenAI (openai.com/index/gpt-5-6), AWS (aboutamazon.com/news/aws/bedrock-openai-models), August 2026

**Content:**

OpenAI's GPT-5.6 family (released July 9, 2026) represents a new pricing/capability paradigm now available on Bedrock:

| Tier | Model | Strengths | Price (Input/Output per 1M tokens) | On Bedrock |
|------|-------|-----------|-------------------------------------|------------|
| Economy | **GPT-5.6 Luna** | Fastest, everyday tasks | ~$0.30/$1.20 (after 80% cut) | ✅ Aug 4 |
| Balanced | **GPT-5.6 Terra** | Knowledge work, coding | ~$2.40/$9.60 (after 20% cut) | ✅ Aug 4 |
| Frontier | **GPT-5.6 Sol** | Complex reasoning, research, cybersecurity | Premium | ✅ Aug 4 |
| Specialist | **GPT-5.6 Cyber** (Daybreak Red) | Offensive cybersecurity | Restricted | ✅ Aug 11 |
| Specialist | **GPT-5.6 Sol** (Daybreak Blue) | Defensive cybersecurity | Restricted | ✅ Aug 11 |

**Key differentiators of GPT-5.6:**
- **Explicit prompt caching** — developer marks which prefixes to cache (1.25× write, discounted reads)
- **State-of-the-art on coding, science, and cybersecurity** benchmarks
- **Fewer tokens for same quality** — more efficient than GPT-5.5
- **Bedrock Web Search integration** — native web grounding

**The pricing revolution:** GPT-5.6 Luna at post-cut pricing is competitive with Nova 2 Lite for many tasks, while offering stronger general intelligence. This changes the cost-performance calculus.

```python
# GPT-5.6 on Bedrock with Web Search
from openai import OpenAI

client = OpenAI(
    base_url="https://bedrock.us-east-1.amazonaws.com/openai/v1",
    api_key="your-bedrock-api-key"
)

response = client.chat.completions.create(
    model="openai.gpt-5.6-sol",
    tools=[{"type": "web_search"}],  # Built-in web grounding
    messages=[{"role": "user", "content": "What's the latest on AWS AI announcements?"}]
)
```

**Facilitator Notes:**
- 🎤 "GPT-5.6 Luna after the price cut is a game-changer for high-volume workloads. It's fast, cheap, and significantly smarter than GPT-4o was. The model selection conversation just got more interesting."
- Common question: "Luna vs Nova 2 Lite?" — Luna is generally stronger on reasoning; Nova 2 Lite is optimised for AWS integration and slightly cheaper. Test on your use case.
- Time: 5 minutes

---

### [NEW AUG-2026] Slide: The OpenAI-Amazon Stateful Runtime Environment
**Insert after:** GPT-5.6 slide
**Source:** OpenAI (openai.com/index/amazon-partnership, openai.com/index/introducing-the-stateful-runtime-environment), AboutAmazon, BusinessWire (Feb 27 + Aug 2026)

**Content:**

The deepest integration between OpenAI and AWS isn't just about hosting models — it's about a **co-created runtime** for agents:

**Stateful Runtime Environment (SRE):**
- Co-developed by OpenAI and AWS specifically for agentic workflows
- Available through Amazon Bedrock
- Provides: **compute, memory, identity, and state** — the primitives agents need
- Models don't start fresh each turn; they maintain running state

**What "stateful" means in practice:**
```
Traditional Bedrock call:
  User → Model → Response (stateless, context via prompt)

Stateful Runtime:
  User → Agent Session (persistent compute + memory + identity)
       → Model reasons over accumulated state
       → Actions happen within a maintained environment
       → State persists across multiple interactions
```

**Strategic implications:**
- Amazon invested **$50 billion** in OpenAI ($15B initial + $35B conditional)
- OpenAI Managed Agents are now available on AWS
- This is NOT just "hosting models" — it's a jointly-built infrastructure layer
- The SRE competes with/complements AgentCore's microVM approach

**How SRE relates to AgentCore:**
| Feature | AgentCore Runtime | OpenAI Stateful Runtime |
|---------|------------------|------------------------|
| Provider | AWS-native | OpenAI × AWS co-created |
| Models | Any Bedrock model | OpenAI models |
| State | MicroVM sessions | Stateful compute environment |
| Session duration | Up to 8 hours | TBD (extended) |
| Best for | Multi-model agents, custom frameworks | OpenAI-native agent patterns |

**Facilitator Notes:**
- 🎤 "This is what a $50 billion partnership looks like in practice. OpenAI isn't just a model provider on Bedrock anymore — they're co-building the agent infrastructure."
- Key insight for students: You now have TWO paths to stateful agents on AWS — AgentCore (model-agnostic, AWS-native) or the OpenAI Stateful Runtime (OpenAI-optimized). Choose based on your model preference.
- Time: 4 minutes
- ⚡ ADVANCED: Discuss how this might evolve — will these converge or remain separate paths?

---

### [NEW AUG-2026] Slide: Bedrock Web Search — Built-in Grounding (GA Aug 4)
**Insert after:** Web Search on AgentCore slide (Slide 17 in July update)
**Source:** AWS (aws.amazon.com/about-aws/whats-new/2026/08/amazon-bedrock-web), bitslovers.com

**Content:**

Web Search on Amazon Bedrock is now **generally available** (August 4, 2026). The entire integration is remarkably simple:

**For OpenAI GPT models on Bedrock:**
```python
# The whole integration — one JSON object
response = client.chat.completions.create(
    model="openai.gpt-5.6-terra",
    tools=[{"type": "web_search"}],
    messages=[{"role": "user", "content": "Latest AWS AI announcements this week"}]
)
# Model decides when to search, returns cited results
```

**For AgentCore agents (via MCP Gateway):**
- Web Search is a built-in connector target using Model Context Protocol (MCP)
- Agent sends natural-language query
- Returns: relevant snippets, source URLs, titles, publication dates
- Model reasons over results to produce grounded responses

**Supported models:** GPT-5.4, GPT-5.5, GPT-5.6 (Sol, Terra, Luna)

**What this replaces:**
- ❌ Custom Serper/Tavily/Bing API integrations
- ❌ Web scraping pipelines
- ❌ Manual search result formatting
- ✅ One config line, fully managed, cited results

**Architecture pattern: Dual grounding**
```
Agent Query
  ├── Knowledge Base (enterprise data, private, governed)
  └── Web Search (public internet, real-time, cited)
      → Agent synthesises both into grounded response
```

**Facilitator Notes:**
- 🎤 "This is the 'just add web search' moment. No API keys, no third-party contracts, no result parsing. One JSON object and your agent has internet access with citations."
- Note: Currently GPT models only. Claude/Nova web search through AgentCore Gateway (different path).
- Time: 3 minutes

---

### [NEW AUG-2026] Slide: AgentCore Runtime Instances — Dedicated Agent Compute (GA Aug 6)
**Insert after:** AgentCore Harness slide (Slide 13 in July update)
**Source:** AWS (aws.amazon.com/about-aws/whats-new/2026/08/aws-bedrock-agentcore-runtime-instances-generally-available), techday.co.uk, itbrief.co.uk

**Content:**

AgentCore now offers **two compute modes** for running agents:

| Feature | Runtime MicroVMs (existing) | Runtime Instances (NEW, GA Aug 6) |
|---------|---------------------------|----------------------------------|
| Compute | Isolated microVM per session | Dedicated EC2 instances |
| Session duration | Up to 8 hours | Up to **14 days** |
| Multi-agent | One agent per VM | **Multiple agents per instance** |
| Cost model | Per-invocation | Reserved capacity (predictable) |
| Best for | Bursty, short-lived sessions | Long-running, enterprise workloads |
| Scaling | Auto (managed) | Customer-managed capacity |

**When to use Runtime Instances:**
- Long-running agent processes (data pipelines, continuous monitoring)
- Predictable workloads where reserved capacity is cheaper
- Multi-agent deployments sharing infrastructure
- Compliance requirements needing dedicated compute

**When to stick with MicroVMs:**
- Variable/bursty workloads
- Short sessions (under 8 hours)
- Maximum isolation requirements
- Pay-per-use cost model preferred

**Key capability:** Shared sessions across multiple agents on the same instance — enables multi-agent collaboration patterns where agents share filesystem and state.

**Facilitator Notes:**
- 🎤 "Think of this as the difference between Lambda (pay-per-invocation) and EC2 (reserved capacity). Same agent code, different hosting model. Choose based on your workload pattern."
- Common question: "Which should I default to?" — Start with microVMs (simpler, auto-scaling). Graduate to Runtime Instances when you have predictable, long-running workloads.
- Time: 3 minutes

---

### [NEW AUG-2026] Slide: Kiro Crew — Autonomous AI Engineering Teams (Aug 4)
**Insert after:** Kiro slide (Slide 10 in July update)
**Source:** Forbes (Aug 6, 2026), kiro.dev/crew, opensourceforu.com, dev.to

**Content:**

On August 4, 2026, AWS open-sourced **Kiro Crew** under Apache 2.0. This transforms Kiro from an interactive assistant into a **persistent agent platform**.

**What Kiro Crew does:**
- Turns AI coding agents into persistent engineering teams
- Continues working **across sessions, machines, and events**
- Remembers context, turns corrections into lasting lessons
- Evolves from work patterns — gets better with use

**Crew vs. Solo Kiro:**
| Aspect | Solo Kiro (IDE) | Kiro Crew (Platform) |
|--------|----------------|---------------------|
| Persistence | Session-based | Cross-session memory |
| Scope | Single developer | Team/org-wide |
| Trigger | Manual prompt | Events, schedules, code changes |
| Learning | Per-session | Accumulates over time |
| Deployment | IDE plugin | Self-hosted (your infra) |

**Why open-source matters:**
- Enterprises get **full governance and security control** via self-hosting
- No vendor lock-in for the orchestration layer
- Community can extend and customize
- BUT: the underlying AgentCore Harness remains closed (AWS manages that)

**Architecture:**
```
Kiro Crew (open-source, self-hosted)
  └── Orchestrates multiple Kiro agent sessions
       └── Each session uses AgentCore Harness (closed, managed)
            └── Model (Claude, GPT, Nova) + Tools + Memory
```

**For this course:** Kiro Crew demonstrates the pattern of "agents managing agents" — directly relevant to multi-agent orchestration covered in Module 12.

**Facilitator Notes:**
- 🎤 "This is the moment AI coding moves from 'assistant that helps when asked' to 'teammate that works while you sleep.' The persistent memory and cross-session learning are key."
- The open-source + closed harness split is interesting strategically — discuss this pattern.
- Time: 4 minutes

---

### [NEW AUG-2026] Slide: Anthropic's Claude Model Landscape (Mid-2026)
**Insert after:** Foundation models section
**Source:** Anthropic (anthropic.com/news), Datacamp, Claude Platform Docs, AWS Bedrock docs

**Content:**

Anthropic's model lineup has expanded dramatically. Here's the current state on Bedrock:

| Model | Released | Tier | Price (In/Out per 1M) | Context | Key Strength |
|-------|----------|------|----------------------|---------|--------------|
| **Claude Fable 5** | June 9, 2026 | Frontier | ~$10/$50 | 1M tokens | Most capable Anthropic model ever, frontier intelligence |
| **Claude Opus 5** | July 24, 2026 | Near-frontier | $5/$25 | 1M tokens | ~Fable 5 performance at half the price |
| **Claude Sonnet 5** | June 30, 2026 | Workhorse | $3/$15 | 1M tokens | Best for coding, agents, professional work at scale |
| **Claude Opus 4.8** | Earlier 2026 | Previous gen | $5/$25 | 200K | Dynamic workflows, large-scale problems |
| **Claude Haiku 4** | 2025 | Fast/cheap | $0.25/$1.25 | 200K | High-throughput, cost-sensitive workloads |

**Key developments:**
- **Text watermarking** (Aug 2, 2026) — Every Claude model now embeds invisible statistical watermarks. First major lab to deploy production-scale text watermarking globally.
- **Claude Code auto-mode default** (Aug 14, 2026) — Background classifier decides which actions are safe to run without human approval. 89% acceptance rate.
- **Claude Mythos 5** — Anthropic's most powerful model, limited availability via "Project Glasswing" (approved customers only). Not on general Bedrock.

**Model selection guidance for this course:**
- **Agents (high-volume):** Claude Sonnet 5 (best price-performance for agentic workloads)
- **Complex reasoning:** Claude Fable 5 or Opus 5 (Opus 5 is the value play)
- **Cost-sensitive automation:** Claude Haiku 4
- **Compare against:** GPT-5.6 Sol (frontier), GPT-5.6 Luna (economy)

**Facilitator Notes:**
- 🎤 "The naming is getting confusing — Fable, Opus, Sonnet, Haiku, Mythos. The key insight: Sonnet 5 is what most of you will use day-to-day for agents. Opus 5 is for when you need frontier intelligence but don't want to pay Fable prices."
- Claude Sonnet 5 on Bedrock: introductory pricing $2/$10 through Aug 31, then $3/$15.
- Time: 4 minutes

---

### [NEW AUG-2026] Slide: AWS Dogwood — Policy Language for Agent Safety
**Insert after:** Guardrails slide (Slide 8 in July update)
**Source:** AWS Open Source Blog (Aug 6, 2026), The New Stack, theaieconomy.substack.com

**Content:**

**Dogwood** is a new open-source runtime verification framework for AI agents, released August 6, 2026.

**The problem it solves:**
Guardrails check content (what the agent *says*). Dogwood checks behavior (what the agent *does*, in what *order*, and how *often*).

**What Dogwood provides:**
- A **policy language** for expressing constraints on agent action sequences
- **Runtime verification** — checks happen during execution, not just before/after
- Constraints on: prerequisites, rate limits, ordering, approvals

**Example policies:**
```
# Require approval before any payment action
policy require_approval_before_payment:
  before: execute_payment
  require: human_approval(type="payment")

# Cap daily spending
policy daily_spend_limit:
  action: execute_payment
  limit: sum(amount) <= 10000 per day

# Never contact external parties after accessing confidential data
policy information_barrier:
  after: access_confidential_data
  block: contact_external_party
  until: session_end
```

**How Dogwood relates to Guardrails:**

| Layer | Tool | What It Checks | When |
|-------|------|---------------|------|
| Content safety | Bedrock Guardrails | What the agent says/generates | Per-message |
| Behavioral safety | **Dogwood** | What the agent does, in what order | Per-action sequence |
| Identity/auth | AgentCore Identity | What the agent is allowed to access | Per-tool-call |

**Why this matters:**
- Individual tool calls can each be "valid" but the *sequence* can be wrong
- Rate limiting prevents runaway agents
- Prerequisite chains enforce human-in-the-loop at critical decision points
- Information barriers prevent data leakage through agent actions

**Facilitator Notes:**
- 🎤 "Guardrails answer 'is this output safe?' Dogwood answers 'is this sequence of actions safe?' Both are needed. An agent can say nice things while doing dangerous things."
- This connects directly to Module 14 (AI Security) — Dogwood is a new layer in defence-in-depth.
- Open source (Apache 2.0) — students can integrate into any framework, not just AgentCore.
- Time: 4 minutes

---

### [NEW AUG-2026] Slide: DynamoDB Vector Search — Embeddings Meet Operational Data
**Insert after:** Managed Knowledge Base slide (Slide 7 in July update)
**Source:** AWS Blog (Aug 5, 2026), SiliconAngle, Futurum Group, InfoWorld

**Content:**

Amazon DynamoDB now supports **native real-time vector search** (GA August 5, 2026).

**What this means:**
- Store vector embeddings **alongside operational data** in DynamoDB
- Perform similarity searches **without a separate vector database**
- Eliminates ETL pipelines between DynamoDB and vector stores
- Embeddings generated via Bedrock embedding models

**Architecture comparison:**

```
BEFORE (separate vector DB):
  App Data (DynamoDB) ──ETL──> Vector DB (OpenSearch/Pinecone)
                                    ↑ query
                               AI Application

AFTER (native vector search):
  App Data + Embeddings (DynamoDB) ← query ← AI Application
  (Single source of truth, real-time, no sync lag)
```

**When to use DynamoDB Vector Search:**
- ✅ Embeddings that change frequently (real-time updates)
- ✅ Applications already on DynamoDB wanting AI search
- ✅ Small-to-medium embedding collections (<millions of vectors)
- ✅ Need for combined metadata + vector queries
- ❌ Massive-scale vector-only workloads (OpenSearch still better at billions)
- ❌ Complex hybrid search with sophisticated ranking

**Comparison with other options:**

| Option | Scale | Managed | Operational Overhead | Best For |
|--------|-------|---------|---------------------|----------|
| Bedrock Managed KB | Any | Fully | None | Standard RAG |
| DynamoDB Vector | Small-Med | Yes | Minimal | App-integrated AI |
| OpenSearch | Large-Massive | Semi | Moderate | Complex search |
| Pinecone/Weaviate | Any | External | External vendor | Multi-cloud |

**Facilitator Notes:**
- 🎤 "This is the 'just add AI to my existing app' story. If you're already on DynamoDB, you don't need a second database for vector search. Store embeddings right next to your data."
- Connects to Module 8 (RAG): Another option in the vector storage decision tree.
- Time: 3 minutes

---

### [NEW AUG-2026] Slide: AWS Context — Knowledge Graphs for AI Agents
**Insert after:** Reference architecture slide (Slide 16 in July update)
**Source:** AWS Summit NYC (June 17, 2026), caylent.com, jayendrapatil.com, thenewstack.io, AWS (July 31 Ontology Accelerator GA)

**Content:**

**AWS Context** (announced Summit NYC, June 17, 2026) is a new service that automatically builds a knowledge graph from organizational data.

**What it provides:**
- Automatically maps relationships across existing data into a **knowledge graph**
- Provides **agentic search** — agents access governed data relationships at runtime
- Understands business rules, domain knowledge, and entity relationships
- **Ontology Accelerator** (GA July 31) — auto-generates the schema/ontology from your data

**The problem it solves:**
> Agents need to know not just *what* information exists, but *how things relate to each other* and *why decisions were made*.

**How it works:**
```
Your Data Sources:
  ├── Databases (RDS, DynamoDB, Redshift)
  ├── Documents (S3, SharePoint)
  ├── SaaS apps (Salesforce, ServiceNow)
  └── Data lakes

     ↓ AWS Context auto-discovers & maps
     
Knowledge Graph:
  ├── Entities (customers, products, teams, processes)
  ├── Relationships (owns, depends-on, approves, contacts)
  ├── Business rules (if X then Y, requires Z approval)
  └── Temporal context (when relationships changed)

     ↓ Agentic Search API
     
AI Agent: "Who needs to approve this procurement?"
  → Context returns: org hierarchy + approval thresholds + delegation rules
```

**Comparison with Knowledge Base:**
| | Bedrock Knowledge Base | AWS Context |
|---|---|---|
| Data type | Documents (text, PDFs) | Structured relationships |
| Search | Semantic similarity | Graph traversal + rules |
| Returns | Relevant passages | Entities, relationships, rules |
| Use case | "What does this doc say?" | "Who relates to whom and why?" |

**Facilitator Notes:**
- 🎤 "Knowledge Base gives agents the ability to read your documents. Context gives agents the ability to understand your organization — its structure, its rules, its relationships."
- This is early-stage (Summit announcement + GA Ontology Accelerator). Set expectations accordingly.
- Connects to Module 11 (Multi-Agent Systems): Agents need organizational context to make good decisions.
- Time: 4 minutes

---

### [NEW AUG-2026] Slide: AWS Continuum — AI-Native Security
**Insert after:** AWS AI services slide (Slide 20 in July update)
**Source:** AWS Summit NYC (June 17, 2026), aboutamazon.com, bankinfosecurity.com, cryptobriefing.com, GeekWire

**Content:**

**AWS Continuum** (announced June 17, gated preview) is an AI-native security service that uses agents to continuously secure applications.

**What it does:**
- Continuously discovers, prioritizes, validates, and remediates security risks
- Covers: penetration testing, code review, threat modeling, vulnerability identification
- Starts in supervised **"learn mode"** — watches patterns, learns codebase
- Transitions to autonomous enforcement only after gaining sufficient context
- Integrates with Anthropic (Claude Code) and OpenAI coding tools (as of Aug 5)

**The agent pattern:**
```
AWS Continuum Agent:
  1. DISCOVER → Scans code, infrastructure, dependencies
  2. PRIORITIZE → Ranks risks by exploitability + impact
  3. VALIDATE → Confirms vulnerabilities are real (not false positives)
  4. REMEDIATE → Proposes/applies fixes within guardrails
  5. LEARN → Gets better at your specific codebase over time
```

**Governance model:**
- Category-by-category permission grants (not all-or-nothing)
- Checkpointing — can roll back autonomous decisions
- "Learn mode" builds trust before autonomy

**Why this belongs in Module 10:**
- Demonstrates a production AI agent pattern (discovery → prioritisation → action)
- Shows the "earn trust" model for autonomous agents
- Real-world integration of AgentCore capabilities in a managed service

**Facilitator Notes:**
- 🎤 "Continuum is what a production AI agent looks like when built by AWS themselves. Notice the 'learn mode first, autonomy later' pattern — this is best practice for any enterprise agent."
- Connects to Module 14 (AI Security): Continuum is both an AI security tool and an example of secure AI agent design.
- Time: 3 minutes

---

### [NEW AUG-2026] Slide: SageMaker HyperPod — Disaggregated Inference & Topology Updates
**Insert after:** SageMaker HyperPod slide (Slide 12 in July update)
**Source:** AWS docs (June–July 2026 release notes)

**Content:**

HyperPod received significant updates in the June–August 2026 window:

**1. Disaggregated Prefill and Decode (DPD) — June 12, 2026**
- Separates the compute-bound prefill phase from the memory-bandwidth-bound decode phase
- Different GPU pools handle each phase
- KV cache transferred between pools over EFA with GPU-Direct RDMA
- Result: **Higher throughput and better GPU utilization** for inference

```
Traditional inference:
  [Same GPUs] → Prefill (compute-heavy) → Decode (memory-heavy)
  
Disaggregated (DPD):
  [Compute GPUs] → Prefill → KV Cache transfer → [Memory GPUs] → Decode
  Each pool optimized for its workload type
```

**2. Partition-Level Topology for Slurm (July 17, 2026)**
- Slurm clusters now support topology-aware scheduling at the partition level
- Better placement of distributed training jobs
- Reduced communication overhead between nodes

**3. Checkpointless Training (existing, now proven at scale)**
- Maintains forward progress despite failures
- Peer-to-peer transfer of model states from healthy accelerators
- **95%+ training goodput** on clusters with thousands of accelerators
- Saves millions on compute costs for large-scale training

**4. Priority-Based Instance Provisioning**
- HyperPod attempts highest-priority instance type first
- Falls back to lower-priority types if capacity unavailable
- Critical for training on scarce accelerators (Trainium3, p5 instances)

**Facilitator Notes:**
- 🎤 "DPD is particularly interesting — it's the same insight that powers disaggregated computing generally: different workload phases have different hardware needs. Don't force them onto the same hardware."
- This is ⚡ ADVANCED content — skip for audiences focused on agent building rather than training infrastructure.
- Time: 3 minutes

---

### [NEW AUG-2026] Slide: Anthropic Text Watermarking — What It Means for Agents
**Insert after:** Guardrails/Dogwood slide
**Source:** Anthropic Help Center, TechTimes (Aug 11, 2026)

**Content:**

As of August 2, 2026, **every Claude model embeds invisible statistical watermarks** in generated text.

**What this means:**
- The watermark is applied globally (not just EU/regulated markets)
- It's invisible — humans can't detect it
- It proves text was **processed by Claude** (not that a specific human authored it)
- Claude is the **first major frontier lab** to deploy production-scale text watermarking

**Implications for enterprise agent systems:**
- Agent outputs can be verified as AI-generated post-hoc
- Useful for audit trails and compliance
- Does NOT prove authorship — proves AI processing occurred
- Watermark survives moderate editing but can be removed by extensive rewriting

**For agentic workflows:**
- Agent-generated emails, reports, and documents carry watermarks
- Enterprises may need disclosure policies for externally-facing agent output
- Internal agents: watermark provides audit trail without explicit labeling
- Consider: Does your compliance framework require AI-generation disclosure?

**Facilitator Notes:**
- 🎤 "This is the 'fingerprint on every output' moment. If your agents are generating customer-facing content with Claude, that content is now watermarked. Plan your disclosure policies accordingly."
- Quick discussion: Is watermarking good or concerning? (Both — accountability vs. privacy)
- Connects to Module 14 (AI Security & Ethics).
- Time: 2 minutes

---

### [NEW AUG-2026] Slide: Updated Model Selection Matrix — August 2026
**Insert after:** Service selection decision tree (Slide 15 in July update)
**Source:** Compiled from all research

**Content:**

The model landscape has shifted significantly. Updated decision framework:

```
WHAT DO YOU NEED?

FRONTIER REASONING (hardest problems, research, complex analysis):
  → Claude Fable 5 ($10/$50) — Anthropic's absolute best
  → GPT-5.6 Sol (premium) — OpenAI's frontier
  → Claude Opus 5 ($5/$25) — 90% of Fable's ability at 50% price ⭐

EVERYDAY AGENT WORKLOADS (coding, tool use, professional work):
  → Claude Sonnet 5 ($3/$15) — Best agentic model for most teams ⭐
  → GPT-5.6 Terra (~$2.40/$9.60) — Strong alternative, web search native

COST-SENSITIVE / HIGH-VOLUME:
  → GPT-5.6 Luna (~$0.30/$1.20) — Incredible value after 80% price cut ⭐
  → Nova 2 Lite ($0.06/$0.24) — Cheapest, good for simple tasks
  → Claude Haiku 4 ($0.25/$1.25) — Fast, lightweight

SPECIALISED:
  → Nova Act — Browser automation (still active)
  → GPT-5.6 Cyber (Daybreak) — Security-specific
  → Claude Code — Software development (auto-mode Aug 14)

⚠️ AVOID FOR NEW PROJECTS:
  → Nova Premier, Nova Omni — Being deprecated
  → Nova Reel, Nova Canvas — Being deprecated
  → GPT-5.5, GPT-5.4 — Superseded by GPT-5.6 family
```

**The ⭐ "default stack" for most students:**
1. **Agent brain:** Claude Sonnet 5 (or GPT-5.6 Terra)
2. **Cheap tasks:** GPT-5.6 Luna
3. **Hard problems:** Claude Opus 5
4. **Browser work:** Nova Act

**Facilitator Notes:**
- 🎤 "Print this. Put it on your desk. The model landscape changes monthly, but this is your August 2026 cheat sheet."
- Emphasise the price-per-quality revolution — GPT-5.6 Luna at $0.30/$1.20 would have been frontier pricing 18 months ago.
- Time: 3 minutes

---

### [NEW AUG-2026] Slide: Bedrock Guardrails Automated Reasoning (June 2026)
**Insert after:** Guardrails multimodal slide (Slide 8 in July update)
**Source:** AWS What's New (June 23, 2026), AWS What's New Guardrails API (June 2026)

**Content:**

Two significant Guardrails updates since the last module refresh:

**1. Automated Reasoning Checks — Policy Refinement Workflows (June 23)**
- Guardrails can now use **formal logic and automated reasoning** (not just ML classifiers)
- New policy refinement workflows let you iteratively test and improve guardrail policies
- Moves from "block bad content" to "verify logical correctness of claims"

**2. New API for Agentic AI Workflows (June 2026)**
- Purpose-built API for agent orchestration frameworks
- Evaluates guardrails at **each step** of an agent's reasoning chain
- Not just input/output — checks intermediate tool calls and reasoning

**Combined with Dogwood:**
```
Layer 1: Bedrock Guardrails (content safety)
  → "Is this text/image harmful?"
  
Layer 2: Guardrails Automated Reasoning (logical correctness)
  → "Is this claim factually supportable?"
  
Layer 3: Dogwood (behavioral policy)
  → "Is this action sequence permitted?"
  
Layer 4: AgentCore Identity (access control)
  → "Is this agent allowed to do this?"
```

**Facilitator Notes:**
- 🎤 "We now have four layers of agent safety, each checking something different. This is what production-grade AI governance looks like in 2026."
- The automated reasoning layer is particularly important for agents making claims about data — it can verify mathematical and logical consistency.
- Time: 3 minutes

---

### [NEW AUG-2026] Slide: The Week That Changed Everything (Aug 4-11, 2026)
**Insert after:** Module overview / breaking news section
**Source:** AWS Weekly Roundup Aug 10, multiple sources

**Content:**

The week of August 4–11, 2026 was one of the densest AWS AI announcement weeks outside re:Invent:

**August 4:**
- ✅ Bedrock Web Search GA (OpenAI GPT models)
- ✅ Kiro Crew open-sourced (Apache 2.0)

**August 5:**
- ✅ DynamoDB native vector search GA
- ✅ AWS Continuum integrates with Claude Code and OpenAI tools

**August 6:**
- ✅ AgentCore Runtime Instances GA
- ✅ Dogwood runtime verification released (open source)
- ✅ Claude Opus 5 support in AWS Help Center noted

**August 10:**
- ✅ OpenAI–Amazon strategic partnership expanded
- ✅ OpenAI Managed Agents announced for AWS

**August 11:**
- ✅ OpenAI GPT-5.6 launch (full family)
- ✅ Daybreak Red/Blue cybersecurity models on Bedrock
- ✅ GPT-5.6 becomes preferred model in Microsoft 365 Copilot
- ✅ GPT-5.6 Luna 80% price reduction, Terra 20% reduction

**Why this matters for students:**
This concentration of announcements signals that the "agentic AI infrastructure" layer is now mature enough for enterprise adoption. The pieces are in place: runtime, web search, vector storage, runtime verification, dedicated compute, and affordable frontier models.

**Facilitator Notes:**
- 🎤 "I'm showing you this timeline to make a point — the pace is accelerating. What we're teaching today will evolve by next month. The skill you need isn't memorizing services; it's knowing the architecture patterns so you can adapt."
- Use as an opening "hook" if teaching this module fresh in late August.
- Time: 2 minutes

---

## C) UPDATED CASE STUDIES

### Case Study 1: The OpenAI-AWS Production Partnership
**Context:** February–August 2026
- Amazon invested $50B in OpenAI
- Co-created Stateful Runtime Environment on Bedrock
- GPT-5.6 family available same-day on Bedrock (Aug 11)
- Specialized cybersecurity models (Daybreak) exclusive to AWS
- **Teaching point:** Even direct competitors collaborate when the market demands it. Bedrock's model-agnostic architecture made this technically possible.

### Case Study 2: Amazon's Nova Model Strategy Pivot
**Context:** July 28, 2026
- Amazon launched Nova family Dec 2024 with high ambitions
- By mid-2026, results didn't reach frontier competitiveness
- Decision: deprecate 4 models, consolidate into one frontier bet
- Led by Pieter Abbeel (world-class AI researcher)
- **Teaching point:** In AI, breadth ≠ quality. Better to have one great model than six mediocre ones. Also demonstrates why model-agnostic architecture (Bedrock) is an insurance policy.

### Case Study 3: AWS Continuum's "Earn Trust" Agent Model
**Context:** June–August 2026
- Starts in learn mode (observes, doesn't act)
- Graduates to autonomous enforcement category-by-category
- Integrates with existing developer tools (Claude Code, Codex)
- **Teaching point:** The gold standard for enterprise agent deployment. Never go full-autonomous from day one. Earn trust incrementally.

---

## D) UPDATED TOOLS & RESOURCES

### New Tools (June–August 2026)

| Tool | Type | Released | Link |
|------|------|----------|------|
| **Kiro Crew** | Open-source agent orchestration | Aug 4, 2026 | github.com/kirodotdev/KiroCrew |
| **Dogwood** | Runtime verification policy language | Aug 6, 2026 | AWS Open Source Blog |
| **AWS Context** | Knowledge graph for agents | June 17, 2026 (Ontology Accelerator GA Jul 31) | aws.amazon.com |
| **Bedrock Web Search** | Built-in web grounding | Aug 4, 2026 GA | Bedrock Console |
| **DynamoDB Vector Search** | Native vector indexing | Aug 5, 2026 GA | DynamoDB Console |
| **Strands Agents Harness SDK** | Production agent harness | Ongoing | github.com/strands-agents/harness-sdk |
| **AgentCore Runtime Instances** | Dedicated agent compute | Aug 6, 2026 GA | AgentCore Console |
| **GPT-5.6 on Bedrock** | Frontier models | Aug 4–11, 2026 | Bedrock Console |
| **Claude Sonnet 5 / Opus 5** | Latest Anthropic models | June–July 2026 | Bedrock Console |

### Updated Documentation
- **AgentCore release notes:** docs.aws.amazon.com/bedrock-agentcore/latest/devguide/release-notes.html
- **Kiro changelog:** kiro.dev/changelog/
- **Nova 2 user guide:** docs.aws.amazon.com/nova/latest/nova2-userguide/
- **Strands Agents docs:** strandsagents.com
- **Bedrock Web Search docs:** docs.aws.amazon.com/bedrock/latest/userguide/web-search.html

### Key Blog Posts for Reading List
1. "Introducing Dogwood: runtime verification for AI agents" — AWS Open Source Blog, Aug 6
2. "Context intelligence for your data and AI agents at scale" — AWS ML Blog, June 17
3. "Amazon DynamoDB now supports real-time vector search at any scale" — AWS Blog, Aug 5
4. "Accelerate cyber defense with OpenAI and AWS: Daybreak Red & Blue" — AWS ML Blog, Aug 11
5. "AWS Open Sources Kiro Crew But Keeps The Agent Harness Closed" — Forbes, Aug 6

---

## E) FARIS HADDAD CONTENT INTEGRATION

### Identified Content

**1. AWS Machine Learning Blog Author Page**
- **URL:** https://aws.amazon.com/blogs/machine-learning/author/fahaddad/
- **Context:** Faris has published on the AWS official ML blog
- **Module relevance:** Reinforces credibility as both practitioner and educator on AWS AI topics
- **In-class reference:** "As someone who's published on the AWS ML blog, I can tell you the pace of change internally is even faster than what you see externally."

**2. ELVTR AI Solutions Architecture Course**
- **URL:** https://uk.elvtr.com/course/ai-solutions-architecture
- **Context:** Faris is listed as instructor for an AI Solutions Architecture course
- **Module relevance:** Establishes domain authority in exactly this module's subject matter
- **In-class reference:** "This module draws from my experience teaching AI architecture to practitioners across enterprise organizations."

**3. Mostly.AI Synthetic Data Talk**
- **URL:** https://mostly.ai/video/faris-haddad-aws-unlock-data-access-at-scale-with-synthetic-data
- **Title:** "Faris Haddad (AWS): Unlock Data Access at Scale with Synthetic Data"
- **Context:** Talk on how AWS uses synthetic data to bridge legacy infrastructure and modern AI
- **Module relevance:** Connects to data preparation for model training (SageMaker + HyperPod section)
- **In-class reference:** "In my talk at Mostly.AI, I discussed how synthetic data bridges the gap between legacy systems and modern AI training — that same principle applies when you're building Knowledge Bases."

### Suggested Integration Points
- **Module opener:** Reference the ELVTR course and AWS blog publications to establish authority
- **Knowledge Base section:** Reference the synthetic data talk as an example of data strategy for AI
- **Throughout:** Use first-person "As I've seen in production deployments..." framing that builds on published work

---

## F) FACILITATOR REFRESH BRIEF

### 🔥 Top 3 Things That Changed Since July 2026

1. **Amazon killed 4 Nova models and bet everything on one frontier effort (July 28)**
   - This completely changes the "Amazon's model strategy" narrative in the existing slides
   - Previous update positioned Nova as a broad competitive family — that's no longer true
   - Update the narrative to: "Bedrock is the model marketplace; Amazon is building one frontier model, not a portfolio"

2. **The OpenAI-AWS partnership became real infrastructure, not just model hosting (Aug 4–11)**
   - Stateful Runtime Environment = co-built agent infrastructure
   - GPT-5.6 on Bedrock same-day with web search = deep integration
   - $50B investment = this isn't a casual partnership
   - Daybreak cybersecurity models = exclusive AWS capabilities

3. **Kiro Crew + Dogwood + AgentCore Runtime Instances = the agent production stack matured (Aug 4–6)**
   - Autonomous engineering teams (Kiro Crew)
   - Behavioral policy enforcement (Dogwood)
   - Dedicated long-running compute (Runtime Instances)
   - These three together close the "how do I actually run agents in production?" gap

### 📢 What to Emphasise as "Breaking News"

- **"Amazon just deprecated most of its own models"** — Lead with this. It's surprising, recent, and sets the context for why Bedrock's multi-model approach matters more than ever.
- **"GPT-5.6 Luna costs $0.30 per million input tokens"** — The price-performance frontier moved dramatically. What cost $15 eighteen months ago now costs 30 cents.
- **"Agents now have runtime verification"** — Dogwood is the answer to "how do I trust an autonomous agent?" This is directly actionable for students building agents.

### 🛠️ Demos & Tools to Set Up Fresh

1. **Update Bedrock model access:** Enable GPT-5.6 Luna, Terra, Sol + Claude Sonnet 5 + Claude Opus 5 in your account
2. **Test Bedrock Web Search:** Create a simple `{"type": "web_search"}` integration to demo live
3. **Install Kiro Crew:** Clone github.com/kirodotdev/KiroCrew for a demo of autonomous agent orchestration
4. **Set up Dogwood:** Write 2-3 example policies to demo runtime verification concepts
5. **DynamoDB Vector Search:** Pre-create a table with embeddings for a quick demo
6. **AgentCore Runtime Instances:** Have one pre-provisioned to show the dedicated compute path
7. **REMOVE FROM DEMOS:** Any Nova Premier/Omni/Reel/Canvas references — these are deprecated

### ⏱️ Updated 60-Min Schedule (Incorporating August Updates)

| Time | Content | Slides |
|------|---------|--------|
| 0–3 min | "The week that changed everything" + Nova strategy reset | NEW AUG slides |
| 3–10 min | Model landscape: GPT-5.6 tiers + Claude family + selection matrix | NEW AUG slides |
| 10–15 min | OpenAI-AWS partnership + Stateful Runtime | NEW AUG slide |
| 15–27 min | AgentCore deep-dive: Harness + Runtime Instances + Web Search | July slides + NEW AUG |
| 27–35 min | Safety stack: Guardrails + Automated Reasoning + Dogwood | July + NEW AUG slides |
| 35–40 min | Knowledge: Managed KB + DynamoDB Vector + AWS Context | July + NEW AUG slides |
| 40–45 min | Developer tools: Strands + Kiro + Kiro Crew | July + NEW AUG slides |
| 45–50 min | SageMaker AI + HyperPod DPD + Silicon | July + NEW AUG slides |
| 50–55 min | Decision tree + reference architecture (updated) | July slides (updated) |
| 55–60 min | Continuum demo + wrap-up + Q&A | NEW AUG + close |

---

*Module 10 August 2026 Refresh Addendum*
*Compiled: 12 August 2026*
*Research sources: AWS official announcements, OpenAI blog, Anthropic blog, Forbes, Business Insider, Reuters, The Next Web, AWS Weekly Roundup (Aug 10, 2026), AWS Summit NYC recap, AWS documentation, AWS Open Source Blog*
