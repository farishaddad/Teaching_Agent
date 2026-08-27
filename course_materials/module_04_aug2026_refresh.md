# Module 04 — Data Foundations for AI
## [AUG-2026 ADDENDUM] — Content Refresh & New Developments

**Date:** 12 August 2026  
**Track:** Foundation  
**Covers:** Developments from June–August 2026 (since July 2026 module update)

---

## A) EXECUTIVE SUMMARY

**Top 10 developments since the July 2026 update:**

1. **Amazon Bedrock Managed Knowledge Base went GA** (17 June 2026) — Fully managed RAG with agentic retrieval for multi-hop reasoning, 6 native connectors, GraphRAG via Neptune Analytics, and automatic hybrid search. Eliminates the need to manage vector DBs, pipelines, or retrieval infrastructure.

2. **RAGU: 7B model beats 32B on knowledge graph extraction** (11 August 2026) — A purpose-built 7B parameter model (Meno-Lite-0.1) outperforms Qwen2.5-32B by 12.5% relative harmonic mean on KG construction, proving that domain-adapted compact models can beat general-purpose large models on specific data tasks.

3. **Databricks launches LTAP + Lakehouse//RT** (16 June 2026, Data+AI Summit) — Lake Transactional/Analytical Processing architecture unifies transactions, analytics, streaming, and operational data on a single copy. Lakehouse//RT delivers sub-100ms latency with up to 16x performance improvement vs. separate real-time stacks.

4. **OpenAI launches ChatGPT Agent + GPT-5 family** (11 August 2026) — ChatGPT can now navigate websites, run code, conduct analysis, and deliver editable outputs autonomously. Workspace agents automate multi-step business processes. GPT-5.6 Sol is the new frontier model.

5. **Anthropic context engineering revolution** (24 July 2026) — Anthropic removed 80% of Claude Code's system prompt for Claude 5 with no performance loss, establishing "less context = better results" as the new paradigm for data feeding to models.

6. **MCP reaches enterprise production** (H1 2026) — 97M monthly SDK downloads; 41% of surveyed software orgs in production with MCP servers; 28% of Fortune 500 have implemented MCP servers for AI-data integration.

7. **Gartner: "Unstructured data is THE missing ingredient for AI-ready data"** (July 2026) — New Gartner report on preparing unstructured data for RAG and agentic analytics published 29 July 2026, defining systematic semantic context processing for the first time.

8. **Knowledge graphs validated as agent memory layer** (July 2026) — "Codebase knowledge graph for AI agents" became a crowded open-source category (ECC, Graphify, Understand-Anything, CodeGraph). KG-as-agent-memory is now a multi-builder movement.

9. **SynAE framework for synthetic data quality** (May 2026) — First comprehensive framework measuring synthetic data quality across validity, fidelity, and diversity axes specifically for tool-calling agent evaluations. Shows no single metric is sufficient.

10. **Vector DB landscape consolidation** (mid-2026) — pgvector wins <10M vectors on simplicity/cost; Weaviate wins schema flexibility + hybrid search; Pinecone wins managed UX at scale; Qdrant wins raw performance. Hybrid search (vector + BM25 + reranker) is now the undisputed default.

---

## B) NEW SLIDES

---

### [NEW AUG-2026] Slide: Amazon Bedrock Managed Knowledge Base — The Fully Managed RAG Stack
**Insert after:** Unstructured Data Pipelines slide  
**Source:** https://aws.amazon.com/jp/about-aws/whats-new/2026/06/amazon-bedrock-managed-knowledge-base/

**Content:**

**GA: 17 June 2026 (AWS Summit New York)**

Amazon Bedrock Managed Knowledge Base eliminates the build-it-yourself RAG stack entirely:

| Component | Before (Self-Managed) | After (Managed KB) |
|---|---|---|
| Data ingestion | Custom ETL pipelines | 6 native connectors (S3, SharePoint, Confluence, Web Crawler, Google Drive, OneDrive) |
| Document parsing | Multiple tools (Textract, Tika, custom) | Automatic smart parsing |
| Embedding generation | Choose model, manage inference | Service-managed by default |
| Vector storage | Deploy & manage vector DB | Managed, auto-scaling |
| Retrieval | Build hybrid search logic | Built-in hybrid search + reranking |
| Multi-hop reasoning | Custom orchestration code | Agentic Retriever (auto query planning) |
| GraphRAG | Neptune + custom integration | Integrated with Neptune Analytics |

**Key Capabilities:**
- **Agentic Retrieval API**: Automatically orchestrates query planning, interim response evaluation, and re-ranking for complex multi-hop queries
- **Multi-modal ingestion**: Documents, images, audio processed natively
- **3,000 page document limit** (up from previous limits)
- **Custom vocabulary support** for domain-specific terminology
- **GraphRAG built-in** via Neptune Analytics for relationship-aware retrieval

**When to use Managed KB vs. self-built:**
- ✅ Managed KB: Standard enterprise RAG, time-to-value priority, <50M documents
- ✅ Self-built: Custom retrieval logic, exotic data sources, extreme scale, cost optimisation

**Facilitator Notes:**
- 🎤 "AWS essentially productised the entire pipeline we showed in the unstructured data slide. If you're on AWS, this is now your starting point — not your stretch goal."
- Demo: Show the console setup flow — emphasise how 6 connectors + auto-parsing + managed vector store eliminates weeks of engineering
- For advanced students: discuss when self-managed still wins (custom chunking strategies, multi-cloud, cost at scale)
- Time: 6 minutes

---

### [NEW AUG-2026] Slide: RAGU — Small Models Beat Large Models on Knowledge Graph Extraction
**Insert after:** GraphRAG slide  
**Source:** https://aiweekly.co/alerts/ragu-releases-7b-graphrag-model-that-tops-qwen25-32b-by-125; https://arxiv.org/abs/2607.11683

**Content:**

**The RAGU Paper (August 2026):**

A 7B parameter model, purpose-built for knowledge graph extraction, beats a 32B general-purpose model on the specific job of turning documents into structured knowledge graphs.

| Model | Size | KG Construction Score | GraphRAG Task Score |
|---|---|---|---|
| Qwen2.5-32B (general purpose) | 32B | Baseline | Baseline |
| Meno-Lite-0.1 (RAGU, extraction-tuned) | 7B | **+12.5% relative** | Matches 32B |

**Why This Matters for Data Foundations:**
1. **Building knowledge graphs just got 4x cheaper** — you can run graph extraction on a 7B model instead of needing 32B+ inference
2. **Multi-step extraction > single-pass** — RAGU uses iterative refinement rather than asking the LLM to extract everything in one shot
3. **Language skills ≠ world knowledge** — graph extraction is a language skill (recognising entities, relationships) that doesn't require the model to "know" facts

**The Inverted LLM Usage Pattern (from AssetOpsBench, KDD 2026):**
Instead of asking the LLM to reason over raw data, you ask it to:
1. Generate structured queries from a typed schema
2. Let the graph execute deterministically
3. Result: 100% accuracy on deterministic handlers (467/467 scenarios)

> "The graph executes deterministically. The LLM just translates." — AssetOpsBench paper

**Practical Implication:** Enterprise KG construction is now feasible without massive GPU budgets. A fine-tuned 7B model + structured graph storage = deterministic, auditable, accurate retrieval.

**Facilitator Notes:**
- 🎤 "The insight is: you don't need GPT-4-class intelligence to build a knowledge graph. You need a model that's really good at one specific skill — finding entities and relationships. That's a much cheaper problem."
- Connects to cost discussions: graph extraction at 7B-model cost makes enterprise KG construction viable
- For advanced: discuss the multi-step extraction pipeline (extract → refine → validate → store)
- Time: 5 minutes

---

### [NEW AUG-2026] Slide: Databricks LTAP — The Lakehouse Goes Real-Time
**Insert after:** Real-Time Data for AI Agents slide  
**Source:** https://www.databricks.com/company/newsroom/press-releases/databricks-launches-ltap-first-lake-transactionalanalytical

**Content:**

**Data+AI Summit, 16 June 2026:**

Databricks introduced two transformative capabilities that directly address the real-time data gap for agents:

**1. LTAP (Lake Transactional/Analytical Processing):**
A new architecture that unifies transactions, analytics, streaming, and operational data on a **single copy** of storage:

```
Traditional Architecture:          LTAP Architecture:
┌──────────┐ ┌──────────┐        ┌──────────────────────┐
│ OLTP DB  │ │ OLAP DW  │        │     Single Lake      │
│(transact)│ │(analytics)│        │  (transactions +     │
└────┬─────┘ └────┬─────┘        │   analytics +        │
     │ CDC         │ ETL          │   streaming +        │
     │ pipeline    │ pipeline     │   operational)       │
     └──────┬──────┘              └──────────────────────┘
            │                              │
     ┌──────┴──────┐              No sync. No CDC.
     │  AI Agent   │              No separate real-time
     │ (stale data)│              serving layer.
     └─────────────┘              
```

**2. Lakehouse//RT (Real-Time):**
- Sub-100ms query latency directly on Delta Lake and Apache Iceberg tables
- Up to **16x better performance** than separate real-time serving stacks
- Response times as low as **10ms** on smaller datasets
- Runs within Unity Catalog governance — no separate permissions layer

**Why This Matters for Agentic Systems:**
- Eliminates the "stale data" problem from the July module case study
- Agents query the same governed data copy as analytics — no sync lag
- Real-time + governance in one layer = safe autonomous decision-making

**Facilitator Notes:**
- 🎤 "Remember our case study about the logistics agent that acted on 4-day-old data? LTAP is the architecture that makes that impossible. One copy of data, always current, always governed."
- Connect to the July module's "Real-Time Data for Agents" slide — this is the concrete implementation
- For advanced: discuss how LTAP compares to traditional Lambda/Kappa architectures
- Time: 5 minutes

---

### [NEW AUG-2026] Slide: Model Context Protocol (MCP) — The Universal Data Interface for Agents
**Insert after:** Semantic Layer slide  
**Source:** https://www.anthropic.com/news/model-context-protocol; https://www.digitalapplied.com/blog/mcp-ecosystem-h1-2026-retrospective-adoption-data-points

**Content:**

**What is MCP?**
An open standard (launched by Anthropic, Nov 2024) that standardises how AI agents connect to data sources and tools. Think "USB-C for AI" — one protocol, any data source, any agent.

**2026 Adoption Explosion:**
- **97 million** monthly SDK downloads (970x growth in 18 months)
- **41%** of surveyed software organisations in production with MCP servers
- **28%** of Fortune 500 have implemented MCP servers
- Adopted by: ChatGPT, Claude, Cursor, Gemini, Microsoft Copilot

**Why MCP Matters for Data Foundations:**

| Without MCP | With MCP |
|---|---|
| N agents × M data sources = N×M custom integrations | N agents × 1 MCP server per data source = N+M integrations |
| Each agent team builds its own data connector | Data team publishes one MCP server; all agents use it |
| No standard security/auth model | OAuth 2.1 + scoped permissions built into the protocol |
| No discoverability | Agents can discover available tools/data at runtime |

**MCP Architecture:**
```
Agent (MCP Client) ←→ MCP Server (your data/tool)
                         ↓
                    Your database, API, 
                    file system, SaaS tool
```

**The Data Team's New Responsibility:**
In 2026, data teams don't just serve dashboards — they publish MCP servers that make governed data accessible to AI agents.

**Enterprise Concerns (H1 2026):**
- Context window consumption: MCP tool definitions can use 72%+ of context
- Auth/governance maturity: still catching up to production needs
- Solution: Progressive disclosure, lean tool descriptions, server-side filtering

**Facilitator Notes:**
- 🎤 "If the semantic layer is the API contract for metric definitions, MCP is the API contract for everything else — files, databases, tools, SaaS apps. Together, they make your data estate agent-accessible."
- Draw connection: Semantic Layer (defines metrics) + MCP (provides access) = complete agent data infrastructure
- For beginners: focus on the USB-C analogy and the N×M → N+M reduction
- For advanced: discuss auth models, context window budgeting, and progressive tool disclosure
- Time: 6 minutes

---

### [NEW AUG-2026] Slide: Context Engineering — Less Data = Better Results
**Insert after:** Data Flywheel slide  
**Source:** https://claude.com/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models/

**Content:**

**The Counterintuitive Lesson (July 2026):**

Anthropic removed **80% of Claude Code's system prompt** for their most advanced models (Claude Opus 5, Claude Fable 5) — with **no measurable performance loss**.

> "More context doesn't always mean better results. For advanced models, excessive instructions actively hurt performance." — Anthropic engineering blog, 24 July 2026

**What This Means for Data Foundations:**

| Old Paradigm (2024) | New Paradigm (2026) |
|---|---|
| Stuff the context window with everything | Curate the minimal high-signal information |
| More retrieved documents = better | Fewer, higher-quality documents = better |
| Verbose system prompts with rules | Concise guidance; trust the model's judgment |
| Flat document dumps | Structured, hierarchical context |

**The Context Engineering Principles for Data:**
1. **Quality over quantity** — 3 highly relevant chunks > 20 loosely related ones
2. **Progressive disclosure** — provide data on demand, not all upfront
3. **Structured references** — code, schemas, and examples > verbose descriptions
4. **Freshness signals** — mark data with timestamps so the agent knows what's current
5. **Compaction** — summarise long histories; keep only decision-relevant facts

**Practical Impact on RAG:**
- Retrieval systems should be **precise**, not recall-maximising
- Reranking is critical — better to return 3 perfect results than 10 mediocre ones
- Cross-encoder reranking (33-40% accuracy boost) is now mandatory, not optional

**Facilitator Notes:**
- 🎤 "The biggest surprise of 2026: the team that built Claude found that giving it LESS information made it work BETTER. This completely changes how we think about feeding data to AI systems."
- This connects to the retrieval quality discussion — precision matters more than recall
- Ask students: "Are you optimising your RAG pipeline for 'find everything vaguely related' or 'find the 3 most relevant documents'?"
- Time: 5 minutes

---

### [NEW AUG-2026] Slide: OpenAI ChatGPT Agent — What Autonomous Data Consumption Looks Like
**Insert after:** Data Architecture for Multi-Agent Systems slide  
**Source:** https://openai.com/index/introducing-chatgpt-agent/; https://openai.com/index/introducing-workspace-agents-in-chatgpt/

**Content:**

**11 August 2026: The Agent Goes Mainstream**

OpenAI launched ChatGPT Agent and Workspace Agents — autonomous systems that:
- Navigate websites and filter results
- Run code and conduct data analysis
- Deliver editable slideshows and spreadsheets
- Prompt for login credentials when needed
- Break complex projects into steps and complete them independently

**Also released:** GPT-5, GPT-5.2, GPT-5.5, GPT-5.6 Sol — each successive model with improved data reasoning, multi-step planning, and tool use.

**What This Shows About Data Requirements:**
1. **Agents now consume data from the open web** — not just your curated enterprise corpus
2. **Multi-format output** — agents create structured data (spreadsheets, slides), not just text
3. **Human-in-the-loop for sensitive access** — agent asks permission before login, purchases, etc.
4. **Long-running processes** — agents can work for hours on complex multi-step data tasks

**Workspace Agents (Enterprise):**
Pre-configured agents for specific business processes:
- Software review agent (triages requests, enforces policy, routes approvals)
- Custom agents per department consuming department-specific data

**The Data Foundation Implication:**
Every workspace agent needs a **governed data layer** underneath it. Without one:
- The software review agent might enforce outdated policies
- The sales agent might quote prices from last quarter
- The compliance agent might miss regulatory changes

**Facilitator Notes:**
- 🎤 "This is what 'the agent era' looks like in practice. As of yesterday, ChatGPT can run for hours, navigating the web and creating deliverables autonomously. Every lesson we've taught about data quality, freshness, and governance? This is why it matters."
- Reference to Module 4's core thesis: good data foundations enable safe, effective agents
- For beginners: focus on the "permission before login" pattern — shows human-in-the-loop for data access
- Time: 4 minutes

---

### [NEW AUG-2026] Slide: SynAE — Measuring Synthetic Data Quality for Agent Evaluation
**Insert after:** Synthetic Data Generation at Scale slide  
**Source:** https://arxiv.org/html/2605.22564; https://github.com/synae-cais-2026/synae-code

**Content:**

**The Problem:** Organisations generate synthetic data to test AI agents, but how do you know if the synthetic data is *good enough* to trust the test results?

**SynAE Framework (May 2026):**
The first comprehensive framework specifically designed to measure synthetic data quality for **tool-calling agent evaluations**.

**Three Quality Pillars:**

| Pillar | Measures | Why It Matters |
|---|---|---|
| **Validity** | Are tool calls syntactically correct? Do they use valid parameters? | Invalid test data gives false failures |
| **Fidelity** | Does synthetic data match real-world distributions? | Unrealistic data gives false confidence |
| **Diversity** | Does the dataset cover edge cases and variations? | Low diversity misses real-world failures |

**Four Evaluation Categories:**
1. Task instructions and intermediate responses
2. Tool calls (format, parameters, sequences)
3. Final outputs (answers, actions, recommendations)
4. Downstream agent evaluation (end-to-end performance)

**Key Finding:** No single metric is sufficient to characterise synthetic data quality. You need all three pillars measured across all four categories.

**Also published (Aug 2026):** "Improving the Realism of Synthetic Clinical Benchmarks Under Utility Constraints" — shows that synthetic benchmarks can pass existing utility checks and still remain structurally unrealistic in privacy-sensitive settings.

**Practical Implication:** 
- If you're generating synthetic data to evaluate agents → use SynAE's multi-axis framework
- A synthetic eval dataset that passes validity checks but fails diversity checks will miss real production failures

**Facilitator Notes:**
- 🎤 "Synthetic data for testing is only as good as your quality framework. SynAE tells us: measure validity, fidelity, AND diversity — if you only check one, your tests will lie to you."
- Connects to the July module's synthetic data risks section — adds the "how to verify quality" dimension
- For advanced: discuss how SynAE could be applied to their own test data generation
- Time: 4 minutes

---

### [NEW AUG-2026] Slide: Vector Database Landscape — The 2026 Consolidation
**Insert after:** Hybrid Search slide  
**Source:** https://www.groovyweb.co/blog/vector-database-comparison-2026; https://internative.net/insights/blog/best-vector-databases-2026-comparison

**Content:**

**The Market Has Settled (Mid-2026):**

After 2 years of rapid fragmentation, the vector DB market has consolidated around clear use-case winners:

| Use Case | Winner | Why | Scale Sweet Spot |
|---|---|---|---|
| **Simplicity + SQL integration** | pgvector | Already in your Postgres; no new infra | <10M vectors |
| **Schema flexibility + hybrid search** | Weaviate | Best-in-class multi-modal + BM25 | 10M–100M |
| **Managed UX + low-latency at scale** | Pinecone | Zero-ops serverless; optimised for agentic workloads | 10M–1B |
| **Raw performance** | Qdrant | Fastest p99 latency; Rust-native | 50M–1B+ |
| **Multimodal (video, image, text)** | Milvus/Zilliz | Strongest multi-vector support | 100M+ |

**Production Benchmarks (2026):**

| Scale | pgvector | Qdrant | Pinecone | Weaviate |
|---|---|---|---|---|
| 1M vectors, p95 latency | 12ms | 4ms | 8ms | 10ms |
| 10M vectors, p95 latency | 45ms | 9ms | 12ms | 18ms |
| 100M vectors, p95 latency | Struggles | 22ms | 18ms | 35ms |

**2026 Consensus:**
- **<10M vectors:** Just use pgvector. Don't overcomplicate it.
- **10-50M vectors:** Weaviate or Qdrant depending on hybrid search needs
- **50M+ vectors:** Purpose-built DBs (Qdrant, Pinecone, Milvus) consistently beat pgvector on throughput and tail latency
- **All scales:** Hybrid search (vector + BM25 + reranker) is mandatory

**Key Trend:** Vector DBs are converging with analytical databases. Snowflake, Databricks, BigQuery all have native vector search. The standalone vector DB may become a feature, not a product.

**Facilitator Notes:**
- 🎤 "Stop agonising over which vector DB. Here's the answer: if you have Postgres and less than 10M vectors, use pgvector. If you need more, pick based on your scale and whether you need hybrid search. The days of 'which vector DB?' being a research project are over."
- Update from the July module: this replaces the generic "hybrid search is default" with specific product recommendations
- Time: 4 minutes

---

### [NEW AUG-2026] Slide: Knowledge Graphs as Agent Memory
**Insert after:** Knowledge Graphs — The Missing Data Layer slide  
**Source:** https://enterprisedna.co/resources/ai-pulse/ai-pulse-2026-07-24-knowledge-graph-as-agent-memory-is-having-a-genuine-multi-bu/; https://neo4j.com/blog/developer/what-40-ai-agents-revealed-about-the-future-of-graph-intelligence/

**Content:**

**July 2026: KG-as-Agent-Memory Is Now a Category**

Knowledge graphs are no longer just for retrieval — they're becoming the **persistent memory layer** for AI agents:

**The Pattern:**
```
Agent Session
    ├── Short-term: Context window (conversation history)
    ├── Medium-term: Vector store (semantic search over past interactions)  
    └── Long-term: Knowledge Graph (structured relationships, decisions, outcomes)
```

**Why Agents Need Graph Memory (Not Just Vector Memory):**
- Vector search: "Find similar past conversations" ✓
- Graph memory: "What did we decide about Project X, and which stakeholder objects?" ✓✓✓
- Graph memory enables: temporal reasoning, causal chains, relationship evolution

**The Open Source Explosion (July 2026):**
Multiple independent teams converged on the same architecture simultaneously:
- **ECC, Graphify, Understand-Anything, CodeGraph** — codebase knowledge graphs for coding agents
- **Neo4j NODES AI 2026** — 40+ agent applications built on graph intelligence (healthcare, finance, cybersecurity, agriculture)
- **Semiont** — Graph-based AI-native wiki using W3C Web Annotation standard

**Key Insight from Neo4j's NODES AI 2026:**
> "Developers from around the world built knowledge-graph-powered AI applications across healthcare, finance, cybersecurity, geospatial intelligence, misinformation analysis, agriculture, and fitness."

**When Agents Need Graph Memory vs. Vector Memory:**

| Signal | Use Vector Memory | Use Graph Memory |
|---|---|---|
| "Find similar" queries | ✅ | |
| Multi-hop reasoning | | ✅ |
| Decision audit trail | | ✅ |
| Relationship tracking | | ✅ |
| Quick semantic lookup | ✅ | |
| Long-term learning across sessions | | ✅ |

**Facilitator Notes:**
- 🎤 "Think about it this way: vector memory is like searching your notes. Graph memory is like having a map of all the decisions you've ever made and how they connect. Agents that learn across sessions need both."
- Connect to Module 12 (multi-agent systems): shared graph memory is how agents coordinate without direct communication
- Time: 5 minutes

---

### [NEW AUG-2026] Slide: Gartner's Framework for Agentic-Ready Unstructured Data
**Insert after:** Unstructured Data Pipelines slide  
**Source:** https://www.gartner.com/en/documents/8196429; https://www.gartner.com/en/documents/7896677

**Content:**

**Two Critical Gartner Reports (2026):**

1. **"How to Prepare and Process Unstructured Data for RAG and Agentic Analytics"** (29 July 2026)
2. **"Advanced AI Text Processing Improves Unstructured Data Management"** (22 May 2026)

**Gartner's Key Finding:**
> "Nearly three-quarters of organisations report that less than 50% of their unstructured data is discoverable and can be used to inform decisions." — BARC Research, June 2026

**Gartner's Systematic Approach for Agentic-Ready Data:**

| Stage | From (Gen 1) | To (Gen 2 — Agentic) |
|---|---|---|
| Ingestion | Batch document loading | Context-aware continuous ingestion |
| Processing | Keyword extraction, basic NER | Semantic context processing |
| Governance | Post-hoc classification | Inline governance + PII filtering |
| Autonomy | Human-driven pipeline triggers | Agentic data coding (agents manage their own data prep) |
| Quality | Schema validation only | Multi-axis quality (validity, fidelity, diversity) |

**The "Agentic Data Coding" Concept (Gartner, July 2026):**
Agents that can create and manage their own data processing code from user intent:
- Agent recognises it needs structured data from a PDF
- Agent writes extraction code, validates output, handles errors
- Human approves the pipeline once; agent runs it continuously

**Data Engineering 2.0 (Gartner, April 2026):**
The data engineering discipline is being reshaped with focus on:
1. Agentic automation of pipeline creation
2. Context engineering (feeding the right data to agents)
3. Managing unstructured data at scale

**Facilitator Notes:**
- 🎤 "Gartner is now saying what we've been teaching: unstructured data is THE missing ingredient. But they're adding something new — agents that manage their own data preparation. That's Data Engineering 2.0."
- For leaders/PMs: focus on the <50% discoverability statistic — massive opportunity gap
- For engineers: focus on the Gen 1 → Gen 2 evolution table
- Time: 5 minutes

---

### [NEW AUG-2026] Slide: The AssetOpsBench Pattern — Deterministic Graphs + LLM Translation
**Insert after:** RAGU slide  
**⚡ ADVANCED**  
**Source:** https://arxiv.org/abs/2605.26874

**Content:**

**KDD 2026 Paper: "Knowledge Graphs as the Missing Data Layer for LLM-Based Industrial Operations"**

**The Key Finding:**
GPT-4 agents achieve only **65%** on industrial maintenance scenarios when reasoning directly over raw data.  
With a knowledge graph + deterministic execution: **100%** (467/467 scenarios, avg score 0.848).

**The Inverted Architecture:**
```
Traditional:   User Query → LLM reasons over data → Answer (65% accuracy)

Inverted:      User Query → LLM generates structured query → 
               Graph executes deterministically → Answer (100% accuracy)
```

**Why This Works:**
1. The LLM is great at *translating* natural language to structured queries (language skill)
2. The LLM is mediocre at *reasoning* over complex relational data (world knowledge)
3. The graph is perfect at *executing* structured traversals (deterministic)
4. Separation of concerns: LLM for translation, graph for computation

**40 Graph-Native Scenarios Tested:**
- Multi-hop dependency queries
- Vector similarity (within graph)
- PageRank criticality analysis
- 6 industrial domains

**Design Principle for Enterprise AI:**
> "Don't ask the LLM to think about your data. Ask it to query your data."

This means:
- Build the graph (structured, schema-driven)
- Let the LLM translate questions into graph queries
- Execute deterministically with full audit trail
- Best of both worlds: natural language interface + structured execution

**Facilitator Notes:**
- 🎤 "The single most important architecture insight of 2026 might be this: stop asking LLMs to reason over data. Instead, ask them to generate queries, and let your database do what databases do — execute deterministically."
- This is advanced but transformative. For engineers: discuss schema design for graph-native scenarios.
- Skip for beginners.
- Time: 5 minutes

---

### [NEW AUG-2026] Slide: BigQuery Search — Unifying Structured + Unstructured in the Warehouse
**Insert after:** Data Lakehouse section  
**Source:** https://cloud.google.com/blog/products/data-analytics/bigquery-search-innovations-unify-structured-unstructured-data

**Content:**

**Google Cloud Announcement (21 July 2026):**

BigQuery now natively processes PDFs, audio files, images, and unstructured text without moving data out of the warehouse:

**What Changed:**
- Previously: Move data out → LLM pipeline → separate search index → move results back
- Now: Upload unstructured data to BigQuery → query with SQL + vector search + full-text search in place

**The Convergence Trend:**
Every major data platform is absorbing vector search and unstructured processing:

| Platform | Vector Search | Unstructured Processing | Graph |
|---|---|---|---|
| **BigQuery** (Google) | Native | Native (July 2026) | BigQuery Graph |
| **Snowflake** | Cortex Search | Document AI | Coming |
| **Databricks** | Vector Search | AI Document Parsing | Unity Catalog |
| **AWS** | Bedrock KB | Bedrock Data Automation | Neptune Analytics |

**What This Means:**
The "separate vector database" may become optional for many use cases. If your data is already in a lakehouse/warehouse, the retrieval layer is being absorbed into your existing platform.

**Implication for Data Strategy:**
- Short-term: Choose the vector solution that fits your existing stack
- Medium-term: Expect your warehouse/lakehouse to handle most retrieval natively
- Long-term: Standalone vector DBs will serve niche high-performance use cases only

**Facilitator Notes:**
- 🎤 "The vector database wars may end with a whimper rather than a bang. Your warehouse is becoming your vector store. If you're already on BigQuery, Snowflake, or Databricks — check what they now offer natively before spinning up a separate Pinecone or Weaviate."
- Connects to the vector DB comparison slide — adds the "platform convergence" dimension
- Time: 4 minutes

---

### [NEW AUG-2026] Slide: Five Failure Modes When Batch Pipelines Feed AI Agents
**Insert after:** Real-Time Data for AI Agents slide  
**Source:** https://techblog.comsoc.org/2026/05/14/why-batch-pipelines-break-ai-agents-the-case-for-streaming-first-network-operations/

**Content:**

**IEEE ComSoc Research (May 2026):**

When AI agents consume data from batch-oriented pipelines designed for dashboards, five distinct failure modes emerge:

| # | Failure Mode | What Happens | Example |
|---|---|---|---|
| 1 | **Stale data** | Agent acts on outdated state | Inventory agent sells stock that was sold 2 hours ago |
| 2 | **Memory gaps** | Agent loses context between batch windows | Customer called twice — agent only sees the morning call |
| 3 | **Delete blindness** | Batch loads don't propagate deletions properly | Agent keeps recommending a product that was recalled |
| 4 | **Schema fragility** | Schema changes break agent's assumptions | A column rename causes agent to return null for a critical field |
| 5 | **Coordination failure** | Multiple agents read the same stale batch | Two agents both try to fulfil the same order |

**The Fix: Streaming-First Architecture for Agents**

```
Event Source → CDC Stream → Stream Processor → Agent Context Store
                                                      ↓
                                            Agent reads CURRENT state
                                            (not yesterday's snapshot)
```

**Key Design Principle:**
- Batch pipelines were designed for *humans reviewing dashboards* (latency tolerance: hours)
- Agents were designed for *autonomous action* (latency tolerance: seconds)
- You cannot safely serve the second with infrastructure built for the first

**When Batch Is Still Fine:**
- Research agents that summarise historical trends
- Report-generation agents (the report IS a point-in-time snapshot)
- Any agent with a human approval step before action

**Facilitator Notes:**
- 🎤 "This extends our July slide on batch vs. streaming. These 5 failure modes are what ACTUALLY breaks in production. If you're planning to deploy action-taking agents on batch pipelines, expect to hit at least 3 of these."
- Interactive: "Which of your current data pipelines feeds an agent? Is it batch or streaming? Which failure mode are you most exposed to?"
- Time: 4 minutes

---

### [NEW AUG-2026] Slide: Data Sovereignty and the "Reverse Information Paradox"
**Insert after:** Data Governance Maturity Model slide  
**Source:** Forbes/Moor Insights & Strategy, 11 August 2026

**Content:**

**The New Data Governance Challenge (August 2026):**

Microsoft CEO Satya Nadella's "Reverse Information Paradox" (went viral August 2026):
> Users pay for AI twice: first for the tool, and second by sharing valuable information that makes the models better.

**Why This Matters for Data Foundations:**
- Enterprises know their data, expertise, and know-how is a source of differentiation
- Regulatory bodies (national, local, sector-specific) are enforcing data sovereignty
- Open-source tools and open-weight models are improving → local AI becomes viable
- The question is no longer "cloud or not?" but "which data stays local?"

**The Data Sovereignty Decision Framework:**

| Data Type | Cloud AI OK? | Local AI Needed? | Rationale |
|---|---|---|---|
| Public-facing content | ✅ | | No competitive sensitivity |
| Internal processes | ⚠️ | Consider | Operational exposure |
| Customer data | ⚠️ | Consider | Regulatory + trust |
| IP / trade secrets | ❌ | ✅ | Competitive risk |
| Training signal | ❌ | ✅ | Model improvement = giving away value |

**Practical Implications for Data Architecture:**
1. **Data classification** must now include "AI inference sensitivity" as a dimension
2. **Hybrid architectures** — some data stays local, some goes to cloud AI
3. **Synthetic data** as a bridge — train on synthetic versions of sensitive data
4. **Audit trail** — which data was sent to which model, when?

**Facilitator Notes:**
- 🎤 "This is the data governance question of 2026 that nobody taught in 2024: when you send your data to an AI API, you're potentially training your competitor's model. How do you decide what data is safe to send?"
- Connects to Module 16 (Governance) — adds the sovereignty dimension
- Politically sensitive: focus on the decision framework, not on specific vendor criticism
- Time: 4 minutes

---

### [NEW AUG-2026] Slide: Updated Tool Landscape — August 2026
**Insert after:** Tools & Resources section  
**Source:** Multiple

**Content:**

**New & Updated Tools Since July 2026:**

| Category | Tool | What's New | Link |
|---|---|---|---|
| **Managed RAG** | AWS Bedrock Managed Knowledge Base | GA June 2026; fully managed RAG, GraphRAG, agentic retrieval | aws.amazon.com/bedrock/knowledge-bases |
| **Real-Time Lakehouse** | Databricks Lakehouse//RT | Sub-100ms on Delta/Iceberg; 16x vs. separate serving | databricks.com |
| **KG Extraction** | RAGU (Meno-Lite-0.1) | 7B model beats 32B on KG construction | arxiv.org/abs/2607.11683 |
| **Agent Interface** | MCP (v1.x) | 97M downloads; enterprise auth patterns maturing | modelcontextprotocol.io |
| **Context Engineering** | Claude Doctor | Audit agent prompts for Claude 5 optimisation | Built into Claude Code |
| **Unstructured Processing** | BigQuery Search | Native PDF/audio/image processing in-warehouse | cloud.google.com |
| **Synthetic Data Quality** | SynAE | Multi-axis eval framework for agent test data | github.com/synae-cais-2026 |
| **Graph Intelligence** | Oracle AI Database 26ai | GraphRAG + vector search in one SQL database | oracle.com |
| **Streaming for Agents** | Conduktor Agentic Pipelines | Pre-built Kafka patterns for agent data feeds | conduktor.io |
| **Agent Memory** | Semiont | W3C-standard graph-based agent wiki | neo4j.com |

**Facilitator Notes:**
- 🎤 Walk through the top 3-4 most relevant to the audience
- For demos: Bedrock Managed KB is the easiest to show live (console walkthrough, ~5 min setup)
- Time: 3 minutes (reference slide, not deep-dive)

---

## C) UPDATED CASE STUDIES

### Case Study 1: Databricks Customer — 16x Real-Time Performance Improvement

**Context:** Databricks Lakehouse//RT preview customers reported up to 16x better performance than existing real-time serving stacks, with response times as low as 10ms on smaller datasets and sub-100ms on larger ones.

**Relevance:** Directly addresses the July module's case study about stale data costing $2.3M. LTAP architecture makes that scenario architecturally impossible — no separate real-time stack means no sync lag.

**Use in class:** "Remember our logistics case study? Here's the architecture that prevents it — and it's now generally available."

---

### Case Study 2: RAGU Industrial Operations — 65% → 100% with Graph Architecture

**Context:** The KDD 2026 paper (AssetOpsBench) tested GPT-4 agents on 139 industrial maintenance scenarios. Direct LLM reasoning achieved 65%. With knowledge graph + deterministic execution: 100% accuracy on 467 expanded scenarios.

**Relevance:** Proves the "inverted LLM usage" pattern — don't ask the model to reason over data; ask it to query structured data. This is the strongest evidence yet for knowledge graphs as the data layer for agents.

**Use in class:** "When the LLM just translates and the graph executes, you get 100% accuracy. When the LLM tries to reason, you get 65%. That's not a subtle difference — it's the difference between production-ready and demo-only."

---

### Case Study 3: Perplexity MCP Context Window Challenge

**Context:** In March 2026, Perplexity CTO Denis Yarats announced Perplexity was moving away from MCP, citing that MCP tool definitions consumed 72% of their context window. This briefly sparked "MCP is dead" discourse.

**Resolution:** The ecosystem responded with progressive disclosure patterns and lean tool descriptions. By mid-2026, MCP was back as the default enterprise integration standard with improved efficiency.

**Relevance to Data Foundations:** Illustrates that how you describe your data tools to agents matters as much as the data itself. Context is a finite resource — data descriptions must be parsimonious.

---

## D) UPDATED TOOLS & RESOURCES

### New Papers (June–August 2026)

| Paper | Key Contribution | Link |
|---|---|---|
| "Knowledge Graphs as the Missing Data Layer" (KDD 2026) | Proves inverted LLM usage: LLM translates, graph executes deterministically (100% vs. 65%) | arxiv.org/abs/2605.26874 |
| RAGU: Multi-Step GraphRAG Engine | 7B model outperforms 32B on KG construction by 12.5% | arxiv.org/abs/2607.11683 |
| SynAE Framework | Multi-axis synthetic data quality evaluation for agent testing | arxiv.org/html/2605.22564 |
| "Improving Realism of Synthetic Clinical Benchmarks" | Shows synthetic benchmarks can pass utility but fail realism | arxiv.org/abs/2608.06265 |
| "Query-Efficient Agentic Graph Extraction Attacks on GraphRAG" (ACL 2026) | Security: GraphRAG systems vulnerable to structured extraction attacks | aclanthology.org |
| "Context Engineering for Claude 5" (Anthropic) | Less context = better for advanced models | claude.com/blog/... |

### New Frameworks & Tools

| Tool | Category | Why It Matters |
|---|---|---|
| **AWS Bedrock Managed Knowledge Base** | Managed RAG | Eliminates entire RAG infra stack |
| **Databricks LTAP + Lakehouse//RT** | Real-time data | Unifies OLTP+OLAP+streaming for agents |
| **RAGU / Meno-Lite-0.1** | KG extraction | Affordable enterprise KG construction |
| **SynAE** | Data quality | Standard for evaluating synthetic agent test data |
| **Claude Doctor** | Context engineering | Audit and optimise agent context for Claude 5+ |
| **BigQuery Search** | Unstructured processing | In-warehouse PDF/image/audio processing |
| **Oracle AI Database 26ai** | Converged DB | SQL + Graph + Vector in one database |
| **Conduktor Agentic AI Pipelines** | Streaming | Kafka patterns pre-built for agent data feeds |

### Updated Documentation

| Resource | What's New |
|---|---|
| AWS Bedrock Knowledge Bases docs | Managed KB setup, GraphRAG with Neptune, Agentic Retrieval API |
| Anthropic Context Engineering Guide | New rules for Claude 5 generation; progressive disclosure patterns |
| Gartner "Data Engineering 2.0" | Agentic automation, context engineering, unstructured data at scale |
| Gartner "Agentic-Ready Data Products" | Machine-verifiable data contracts for AI/agentic AI |
| MCP Specification (v1.x) | OAuth 2.1 auth, enterprise governance patterns |

---

## E) FARIS HADDAD CONTENT INTEGRATION

**Search Results:**

A direct search for "Faris Haddad" published content related to AI/agentic topics returned one confirmed association:

- **ELVTR AI Solutions Architecture Course** (uk.elvtr.com/course/ai-solutions-architecture) — Faris Haddad is listed as the instructor for this course, which covers AI solutions architecture.

**No directly attributable LinkedIn articles, blog posts, or Medium publications were found in the June–August 2026 timeframe specifically authored by Faris Haddad on data foundations or agentic AI topics.**

**Recommendation for Facilitator:**
- If Faris has unpublished drafts or internal articles on these topics, reference them as: "As I've been discussing in my recent work on [topic]..."
- The ELVTR course association can be referenced as: "This connects to what I teach in my AI Solutions Architecture course — data foundations ARE the architecture."
- Consider publishing a short LinkedIn post on one of the August developments (e.g., the RAGU finding or Bedrock Managed KB) to create a citable reference for future modules.

---

## F) FACILITATOR REFRESH BRIEF

### 🎯 Top 3 Things That Changed Since July 2026

1. **AWS Bedrock Managed Knowledge Base went GA** — The entire RAG pipeline we taught in July (unstructured data → extraction → chunking → embedding → vector store → retrieval) is now a managed service. You can set it up in the console in minutes. This doesn't make the pipeline knowledge obsolete — students still need to understand it — but the "do I build or buy?" answer just shifted heavily toward buy for most use cases.

2. **The "Less Context = Better" paradigm** — Anthropic's July 24th revelation that 80% less system prompt = same or better results fundamentally changes how we think about feeding data to agents. Our teaching on RAG should now emphasise PRECISION over recall. 3 perfect results > 20 mediocre ones. Reranking is no longer optional.

3. **LTAP + Lakehouse//RT makes real-time data accessible** — Databricks' LTAP architecture eliminates the "separate real-time serving layer" problem. For the first time, agents can query governed lakehouse data with sub-100ms latency without data movement. This makes our "batch vs. streaming" framing more nuanced — it's now "batch vs. streaming vs. lakehouse-native real-time."

### 📢 What to Emphasise as "Breaking News"

- **"As of yesterday (11 August), OpenAI launched ChatGPT Agent"** — fully autonomous web navigation, code execution, multi-format output creation. This is the most visible proof point that the agentic era has arrived at consumer scale.
- **"A 7B model beats a 32B model on knowledge graph extraction"** — RAGU paper (11 August). Shows that purpose-built small models > general-purpose large models for specific data tasks. Cost of enterprise KG construction just dropped 4x.
- **"Gartner now says unstructured data is THE missing ingredient"** — validates our module's thesis. 75% of orgs have less than 50% of unstructured data discoverable.

### 🛠️ Demos & Tools to Set Up Fresh

| Demo | Setup | Time to Prep | Impact |
|---|---|---|---|
| **AWS Bedrock Managed KB** | Console walkthrough: S3 bucket → Managed KB → query | 15 min | HIGH — shows managed RAG in action |
| **Databricks Lakehouse//RT** | Pre-record or use Databricks demo environment | 20 min | MEDIUM — impressive but requires Databricks access |
| **SynAE** | Clone repo, run on sample agent traces | 30 min | MEDIUM — shows quality evaluation in action |
| **MCP Server** | Build a simple MCP server exposing a CSV file | 20 min | HIGH — students see how data becomes agent-accessible |
| **Claude Doctor** | Run on a bloated CLAUDE.md file, show optimisation suggestions | 5 min | LOW effort, HIGH insight — shows context engineering |

### ⚠️ Corrections to July Module

| July Content | Correction Needed |
|---|---|
| "Tools (2026): Cube.dev, AtScale, dbt Semantic Layer, Looker Metrics Layer" in Semantic Layer slide | Add: "MCP servers for semantic layer exposure" — this is now the primary way agents access semantic layers |
| "Amazon Neptune + Bedrock Knowledge Bases" in GraphRAG tools | Update to: "Amazon Bedrock Managed Knowledge Base with integrated GraphRAG (GA June 2026)" |
| Vector DB discussion | Add convergence trend: warehouses absorbing vector search (BigQuery, Snowflake Cortex, Databricks) |
| Real-time architecture tools | Add: "Databricks Lakehouse//RT, Databricks LTAP" alongside Kafka/Kinesis/Flink |

---

*Module 04 August 2026 Addendum — AI & Agentic AI Training Programme*  
*Prepared: 12 August 2026*  
*Next refresh due: September 2026*
