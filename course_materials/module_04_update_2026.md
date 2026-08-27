# Module 04 — Data Foundations for AI
## [2026 UPDATE] — New Content, Gap Analysis & Facilitator Notes

---

## Gap Analysis

Based on the latest research (2025–2026), here are the critical gaps in the original Module 04:

1. **No coverage of data for agentic systems** — The module treats data as input to models but doesn't address how autonomous agents consume, verify, and act on data in real time. TDWI's May 2026 benchmark found only 47% of organizations report trusted structured data and just 27% have a governed semantic layer — the #1 blocker for scaling agentic AI.

2. **Missing: Knowledge Graphs and GraphRAG** — Microsoft's GraphRAG research showed 3.4× improvement on multi-hop reasoning (16.7% → 56.2%) by grounding LLMs in knowledge graphs. This is now standard enterprise architecture. Not mentioned in original.

3. **Missing: The Data Flywheel Pattern** — The self-reinforcing loop where production usage generates feedback that improves the system. MAPE control loops (Monitor-Analyze-Plan-Execute) are now the standard architecture for continuous AI improvement. Original module treats data as static.

4. **Missing: Multimodal Embeddings (ColPali, VLMs)** — The original covers text embeddings but not the 2025–2026 shift to vision-language embeddings that process documents as images, eliminating OCR pipelines entirely.

5. **Missing: The Semantic Layer for AI** — MIT CISR (May 2026) formalised the semantic layer as the critical interface between data warehouses and AI agents. Only 27% of enterprises have one. Agents without semantic layers invent their own metric definitions.

6. **Missing: Real-Time/Event-Driven Data for Agents** — IBM acquired Confluent for $11B in March 2026 specifically to provide "the engine of enterprise AI and agents." Agents need streaming, not batch.

7. **Missing: Synthetic Data Generation at Scale** — Coverage of synthetic data taxonomy exists but not the 2025–2026 advances: LLM-generated training data, self-play data generation, iterative refinement pipelines, and the risks (model collapse, data contamination).

8. **Missing: Data Quality Failure Modes for AI** — The 5 data quality issues that break AI agents (per Delphina.ai 2026): duplicate/fragmented entities, inconsistent IDs, free-text in categorical fields, timezone inconsistencies, stale data from silent pipeline failures.

9. **Outdated: Vector store landscape** — The original covers basic vector stores but the 2026 landscape has shifted to hybrid search as default, with vector DBs converging with analytical databases.

10. **Missing: Unstructured Data Processing Pipelines** — 90% of the 175 zettabytes of global data is unstructured. The original mentions unstructured data but doesn't cover production pipelines for processing PDFs, images, video, and audio at enterprise scale.

---

## NEW SLIDES

---

### [NEW 2026] Slide: The Data Readiness Gap for Agentic AI
**Insert after:** Why Data Quality Determines AI Quality section
**Format:** Concept explanation with data points

**Content:**

The TDWI Benchmark Report (May 2026, 161 organisations) reveals a stark reality:

| Readiness Dimension | Score (out of 20) |
|---|---|
| Technology infrastructure | 15/20 |
| Governance | 14/20 |
| Data readiness | 13/20 |
| Organisational readiness | 13/20 |

**Key findings:**
- Only **47%** of organisations report broadly trusted structured data
- Just **27%** have a governed, machine-consumable semantic layer
- Fewer than **10%** have multi-agent systems in production
- The gap: strong compute/tooling sitting on **shaky data foundations**

> "An intelligent agent acting on fragmented, delayed or conflicting records does not remove operational problems. It automates them." — Nerdbot AI, June 2026

**Why this matters now:** Unlike chatbots that answer questions, agents **take actions** — placing orders, changing schedules, allocating inventory. Bad data no longer produces a bad answer; it produces a bad action with real-world consequences.

**Facilitator Notes:**
- 🎤 Open with: "The thing about agents is that they don't just read your data — they act on it. So data quality is no longer an analytics problem. It's an operations safety problem."
- Common question: "How do we get from 47% trusted data to a level that supports agents?" → Point to Module 5 (AI Roadmap) for the prioritisation framework
- For beginners: focus on the "agents automate bad decisions" insight. For advanced: discuss the governance scoring dimensions
- Time: 5 minutes

---

### [NEW 2026] Slide: The 5 Data Quality Issues That Break AI Agents
**Insert after:** Data Readiness Gap slide
**Format:** Table with examples

**Content:**

Per Delphina.ai's 2026 production analysis, these five data quality issues cause the most agent failures:

| # | Issue | What Breaks | Example |
|---|---|---|---|
| 1 | **Duplicate/fragmented entity records** | Agent gets conflicting context about the same customer | "Acme Corp" / "ACME Corporation" / "Acme Corp." treated as 3 different entities |
| 2 | **Inconsistent IDs and broken joins** | Agent can't link related data; partial context leads to wrong actions | Order table uses `customer_id`, support table uses `client_ref`, no mapping |
| 3 | **Free-text in categorical fields** | Agent can't filter or aggregate reliably | "Status" column has: "active", "Active", "ACTIVE", "yes", "live", "1" |
| 4 | **Time & timezone inconsistencies** | Agent makes time-sensitive decisions on wrong timestamps | UTC timestamps mixed with local times; `2026-07-05` vs `07/05/2026` vs `5-Jul-26` |
| 5 | **Stale data from silent pipeline failures** | Agent acts on outdated information as if it were current | ETL job failed 3 days ago; inventory agent keeps selling sold-out stock |

**The multiplier effect:** A 10-step agentic process with 99% per-step data accuracy still has only ~90.4% end-to-end success. Data errors compound across agent reasoning chains.

**Facilitator Notes:**
- 🎤 "These aren't theoretical — they're the specific issues that production teams report as their #1 cause of agent failures in 2026"
- Ask students: "Which of these have you seen in your own data estate?" (drives engagement)
- For advanced: discuss how each maps to a specific data governance control
- Time: 5 minutes

---

### [NEW 2026] Slide: Knowledge Graphs — The Missing Data Layer
**Insert after:** Embeddings and Vector Representations section
**Format:** Concept explanation with comparison

**Content:**

**The Problem Vector Search Can't Solve:**
Vector similarity finds semantically similar passages. But enterprises need to reason over **relationships**: customers → contracts → products → policies → events.

**Knowledge Graphs for AI:**
A knowledge graph represents information as **nodes** (entities) and **edges** (relationships), enabling:
- Multi-hop reasoning: "Which customers of Product X also have an open support ticket about feature Y?"
- Structured traversal of organisational knowledge
- Provenance tracking: every answer cites its source path

**The Evidence (2025–2026):**
- Microsoft GraphRAG: accuracy on multi-hop reasoning improved from **16.7% to 56.2%** (3.4× improvement)
- CFR regulatory benchmark: Knowledge Graph-enhanced approach achieved **70% accuracy improvement** over standard vector-based RAG
- Cross-encoder reranking adds 33-40% retrieval accuracy for ~120ms added latency

```
Vector DB                    Knowledge Graph
─────────────────────       ──────────────────────
"Find similar text"          "Find connected entities"
Good for: semantic search    Good for: relationship queries
Weakness: no structure       Weakness: requires schema
Scales: easily               Scales: with effort
───────────────────────────────────────────────
         BEST PRACTICE 2026: USE BOTH
         (Hybrid retrieval: vector + graph)
```

**Facilitator Notes:**
- 🎤 "If vector search is like Google — finding things that are about the same topic — knowledge graphs are like Wikipedia's link structure. They tell you how things connect."
- Common question: "Do we need to build a KG from scratch?" → No — LLMs can now extract triples from unstructured text automatically (see GraphRAG tools)
- For beginners: focus on the intuition. For advanced: discuss schema design and triple extraction
- Time: 6 minutes

---

### [NEW 2026] Slide: GraphRAG — How Knowledge Graphs Enhance RAG
**Insert after:** Knowledge Graphs slide
**Format:** Architecture diagram + comparison
**⚡ ADVANCED**

**Content:**

**GraphRAG Architecture:**
```
Document Corpus
    │
    ▼
┌─────────────────────────┐
│ 1. Entity Extraction    │ ← LLM extracts entities & relationships
│ 2. Community Detection  │ ← Graph clustering identifies themes
│ 3. Community Summaries  │ ← LLM summarises each cluster
└─────────────────────────┘
    │
    ▼
┌─────────────────────────┐
│  Knowledge Graph Index   │
│  + Community Summaries   │
└─────────────────────────┘
    │
    ▼
Query → Retrieve relevant communities → Synthesise answer
```

**Three Retrieval Modes:**

| Mode | How It Works | Best For |
|---|---|---|
| **Local Search** | Retrieves entities + their immediate neighbourhood | Specific factual questions |
| **Global Search** | Synthesises across community summaries | Broad/abstract questions ("What are the main themes?") |
| **Hybrid** | Combines local entity retrieval with global summaries | Enterprise use cases requiring both precision and coverage |

**Tools & Platforms (2026):**
- Microsoft GraphRAG (open source)
- LightRAG (lightweight alternative)
- Neo4j + LangChain GraphRAG integration
- Amazon Neptune + Bedrock Knowledge Bases

**Facilitator Notes:**
- 🎤 "GraphRAG is the reason knowledge graphs have had a renaissance in 2025-2026. LLMs solved the hardest part — building the graph from unstructured text."
- Skip for beginners unless they have a strong data background
- Demo suggestion: show a Microsoft GraphRAG notebook on a small corpus
- Time: 6 minutes

---

### [NEW 2026] Slide: The Semantic Layer — Data's Interface for AI Agents
**Insert after:** Building a Data Strategy section
**Format:** Concept with architecture diagram

**Content:**

**What is a Semantic Layer?**
A governed, machine-consumable translation layer between raw data tables and the things consuming data — dashboards, notebooks, and now **AI agents**.

> "The next phase of AI adoption will be defined not by models or tooling, but by semantics — who controls the definitions, context, and relationships AI systems rely on to reason." — Tony Baer, Data 2026 Outlook

**Why Agents Need a Semantic Layer:**
Without one, every AI agent invents its own definition of "revenue," "active customer," or "churn rate." You get:
- Dashboard says £4.2M revenue; agent says £3.8M → trust erodes
- Agent makes decisions using a metric it defined differently from finance → costly errors
- No auditability: "What definition of revenue did the agent use?"

**Architecture:**
```
┌──────────────────────────────────┐
│          AI Agent / LLM          │
└────────────┬─────────────────────┘
             │ queries governed metrics
             ▼
┌──────────────────────────────────┐
│        SEMANTIC LAYER            │
│  • Business metric definitions   │
│  • Entity relationships          │
│  • Access policies               │
│  • Query validation rules        │
│  Accessible via: SQL, REST,      │
│  GraphQL, MCP                    │
└────────────┬─────────────────────┘
             │
             ▼
┌──────────────────────────────────┐
│     Data Warehouse / Lake        │
│   (Snowflake, Redshift, etc.)    │
└──────────────────────────────────┘
```

**Tools (2026):** Cube.dev, AtScale, dbt Semantic Layer, Looker Metrics Layer

**Facilitator Notes:**
- 🎤 "Think of the semantic layer as the API contract between your data and your AI. Without it, every agent writes its own SQL — and gets its own slightly different answer."
- Tie back to Module 16 (Governance): semantic layer is where governance meets AI consumption
- Common question: "How is this different from a data catalog?" → Catalog documents; semantic layer governs and serves. Both needed.
- Time: 5 minutes

---

### [NEW 2026] Slide: The Data Flywheel — Continuous AI Improvement
**Insert after:** Building a Data Strategy section (after Semantic Layer)
**Format:** Concept with diagram

**Content:**

**What is a Data Flywheel?**
A self-reinforcing loop where production usage generates data that improves the system, which attracts more usage, generating more improvement data.

```
         ┌──────────────┐
         │  Better AI   │
         │  Performance  │
         └──────┬───────┘
                │ attracts more usage
                ▼
         ┌──────────────┐
         │  More User   │
         │  Interactions │
         └──────┬───────┘
                │ generates feedback data
                ▼
         ┌──────────────┐
         │  Richer      │
         │  Training    │
         │  Signal      │
         └──────┬───────┘
                │ improves the model
                ▼
         ┌──────────────┐
         │  Better AI   │  ← cycle repeats
         │  Performance  │
         └──────────────┘
```

**The MAPE Control Loop (2025 research):**
Production-grade flywheels follow the MAPE architecture:
1. **Monitor** — Capture user interactions, agent actions, outcomes
2. **Analyze** — Identify failures, patterns, and opportunities in the data
3. **Plan** — Prioritise improvements (which failures to fix first)
4. **Execute** — Retrain, update retrieval index, adjust guardrails

**Data Flywheel Failure Modes:**
- Leakage: feedback loop appears to spin but amplifies bias
- Stale patterns: optimising a proxy that diverges from real objective
- Sparse feedback: thumbs-up/thumbs-down without context tells you nothing useful
- "Three months later, the model has not improved" — common anti-pattern

**Facilitator Notes:**
- 🎤 "Amazon's retail flywheel is the origin of this concept. In AI, the flywheel is: more usage → more data → better model → more usage. But most teams fail to close the loop."
- Ask: "Who has a feedback mechanism in production today? Is it actually being used to improve the model?"
- Time: 5 minutes

---

### [NEW 2026] Slide: Real-Time Data for AI Agents
**Insert after:** Data Pipelines section
**Format:** Concept with architecture comparison

**Content:**

**Why Agents Need Streaming, Not Batch:**
Traditional AI systems query a data warehouse updated nightly. Agents make decisions in real time. An inventory agent selling stock that was sold out 3 hours ago creates real business harm.

> IBM validated this at $11 billion scale when it acquired Confluent in March 2026, calling real-time data streaming "the engine of enterprise AI and agents."

**Batch vs. Streaming for Agents:**

| Dimension | Batch Architecture | Streaming Architecture |
|---|---|---|
| Latency | Hours to days | Milliseconds to seconds |
| Freshness | Point-in-time snapshot | Continuous | 
| Agent suitability | Read-only Q&A | Action-taking agents |
| Example | "What were sales yesterday?" | "A customer just churned — take action" |
| Cost | Lower compute | Higher compute, lower error cost |

**Event-Driven Agent Architecture:**
```
Events → Message Bus (Kafka/Kinesis) → Streaming DB → Agent Context
                                                          │
                                                          ▼
                                                    Agent Action
```

**Key Design Principle:** Agents should be triggered by events, not polling. Sub-second latency with HMAC security and structured payloads.

**Tools (2026):** Apache Kafka, AWS Kinesis, Confluent, RisingWave (streaming DB), Apache Flink

**Facilitator Notes:**
- 🎤 "If your agent is making decisions on data that's 24 hours old, it's not an agent — it's a report that takes actions based on yesterday's world."
- For beginners: focus on the batch vs. streaming table. For advanced: discuss CDC patterns and event schemas.
- Common question: "Do ALL agents need real-time data?" → No. Read-only research agents are fine with batch. Action-taking agents need freshness.
- Time: 5 minutes

---

### [NEW 2026] Slide: Multimodal Embeddings — Beyond Text
**Insert after:** Embeddings and Vector Representations section
**Format:** Concept with comparison
**⚡ ADVANCED**

**Content:**

**The 2024–2026 Shift: From Text Extraction to Visual Understanding**

Traditional pipeline:
```
PDF → OCR → Text extraction → Chunking → Text embeddings → Vector DB
```

Modern pipeline (ColPali/VLM approach):
```
PDF → Page images → Vision-Language Model → Multimodal embeddings → Vector DB
```

**Why this matters:**
- OCR loses table structure, chart data, layout semantics
- Visual embeddings capture everything the human eye sees
- Eliminates 4 fragile processing steps

**ColPali (2024 paper, now production-ready):**
- Uses PaliGemma-3B vision-language model
- Produces embeddings directly from page images
- Late-interaction retrieval (ColBERT-style) for region-level matching
- 3× faster indexing than traditional OCR pipelines

**When to use which:**

| Approach | Best For | Weakness |
|---|---|---|
| Text embeddings | Clean text documents, code | Loses visual structure |
| Multimodal (ColPali) | PDFs, slides, forms, invoices | Higher compute cost |
| Hybrid | Enterprise with mixed document types | Complexity |

**Facilitator Notes:**
- 🎤 "The insight is simple: why extract text from a document when you can just look at it? That's what VLMs do — they see the page the way a human does."
- Demo suggestion: show ColPali on a complex PDF with tables and charts vs. traditional OCR pipeline
- Skip for beginners unless they work with document processing
- Time: 5 minutes

---

### [NEW 2026] Slide: Synthetic Data Generation at Scale
**Insert after:** Data Taxonomy section (within the synthetic data coverage)
**Format:** Concept with techniques table

**Content:**

**Why Synthetic Data Has Exploded (2025–2026):**
- Real data is limited, expensive, and privacy-restricted
- LLMs can generate realistic, diverse training examples
- Research shows 76.4% of synthetic data techniques involve LLM prompting

**Key Techniques:**

| Technique | How It Works | Use Case |
|---|---|---|
| **Prompt-based generation** | LLM generates examples from instructions | Quick prototyping, few-shot datasets |
| **Self-instruct / Evol-Instruct** | LLM creates progressively harder examples from seed data | Instruction-following fine-tuning |
| **Retrieval-augmented synthesis** | LLM uses retrieved context to generate grounded examples | Domain-specific training data |
| **Iterative self-refinement** | LLM generates → evaluates → improves its own outputs | High-quality distillation datasets |
| **Multi-agent synthesis** | Multiple LLMs generate and critique data cooperatively | Alignment and preference data |
| **Self-play** | Agent generates both questions and answers, verifying each | Reasoning and math datasets |

**Risks to Teach:**
- **Model collapse:** Training on synthetic data from the same model family leads to distribution narrowing
- **Data contamination:** Synthetic data may leak benchmark answers
- **Bias amplification:** LLMs reproduce and amplify existing biases
- **Quality ceiling:** Synthetic data rarely exceeds the quality of the generating model

**Production Pattern:** Seed with real data → Generate synthetic variants → Filter with quality checks → Mix synthetic + real at ratio (typically 70/30 to 90/10)

**Facilitator Notes:**
- 🎤 "Synthetic data used to mean 'fake data for testing.' Now it means 'generated training signal that makes models better.' But it comes with real risks."
- For beginners: focus on the why and the risks. For advanced: discuss Evol-Instruct and self-play.
- Common question: "Can I just generate all my training data?" → No. Model collapse is real. Always mix with real data.
- Time: 5 minutes

---

### [NEW 2026] Slide: Unstructured Data Pipelines for Enterprise AI
**Insert after:** Data Pipelines section
**Format:** Architecture walkthrough

**Content:**

**The Scale of the Problem:**
- 175+ zettabytes of global data by 2026
- 90% is unstructured (PDFs, images, video, emails, audio)
- 88% of organisations use AI; only 39% report measurable impact — unstructured data is a key blocker

**The Modern Unstructured Data Pipeline:**

```
┌─────────────────────────────────────────────────────────────┐
│                    INGESTION LAYER                            │
│  PDFs │ Emails │ Images │ Audio │ Video │ Web pages │ Code  │
└────────────────────────┬────────────────────────────────────┘
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   EXTRACTION LAYER                            │
│  • Document parsing (Apache Tika, Unstructured.io)           │
│  • OCR (Textract, Tesseract) or VLM (ColPali)              │
│  • Audio transcription (Whisper, Transcribe)                 │
│  • Video frame extraction + caption generation               │
└────────────────────────┬────────────────────────────────────┘
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                  TRANSFORMATION LAYER                         │
│  • Chunking (semantic, fixed, parent-child)                  │
│  • Entity extraction & metadata enrichment                   │
│  • Classification & tagging                                  │
│  • Knowledge graph triple extraction                         │
└────────────────────────┬────────────────────────────────────┘
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    INDEXING LAYER                             │
│  • Vector embeddings → Vector DB                             │
│  • Full-text index → Search engine                           │
│  • Graph triples → Knowledge graph                           │
│  • Structured metadata → Data warehouse                      │
└─────────────────────────────────────────────────────────────┘
```

**Tools (2026):** Unstructured.io, LlamaIndex, LangChain, Amazon Textract, Apache Tika, Docling

**Facilitator Notes:**
- 🎤 "Most AI teams spend 60-80% of their time in data preparation. This pipeline is where that time goes. Understanding it means understanding where AI projects actually succeed or fail."
- Draw this on a whiteboard; walk through each layer with a specific document (e.g., a customer contract PDF)
- Time: 6 minutes

---

### [NEW 2026] Slide: Vector DB vs. Knowledge Graph — The Decision Matrix
**Insert after:** GraphRAG slide
**Format:** Comparison table / decision framework

**Content:**

| Dimension | Vector Database | Knowledge Graph | Use Both |
|---|---|---|---|
| **Query type** | "Find similar" | "Find connected" | Complex enterprise queries |
| **Best for** | Semantic search, Q&A | Multi-hop reasoning, compliance | Full RAG pipeline |
| **Data shape** | Flat documents | Entities + relationships | Mixed document types |
| **Setup effort** | Low (embed & index) | High (schema + extraction) | Medium (automated extraction) |
| **Hallucination risk** | Moderate | Low (structured paths) | Lowest |
| **Explainability** | Low (similarity score) | High (traversal path) | High |
| **Scalability** | Excellent | Moderate | Architecture-dependent |
| **Example tools** | Pinecone, Weaviate, Qdrant, pgvector | Neo4j, Amazon Neptune, TigerGraph | LangChain + Neo4j + Pinecone |

**Decision Heuristic:**
- ✅ Vector DB alone: simple Q&A, single-document retrieval, semantic search
- ✅ Knowledge Graph alone: compliance, audit trail, relationship-heavy domains
- ✅ Both (hybrid): enterprise RAG, agentic systems, multi-source reasoning

**2026 Data Point:** Microsoft GraphRAG moved accuracy on multi-hop questions from 16.7% to 56.2% — a 3.4× improvement over vector-only retrieval.

**Facilitator Notes:**
- 🎤 "This isn't a 'pick one' decision. The 2026 best practice is hybrid — vector for similarity, graph for relationships. The question is: which do you start with?"
- For beginners: "If you only have budget for one, start with vector. Add graph when you need relationship reasoning."
- Time: 4 minutes

---

### [NEW 2026] Slide: Data Architecture for Multi-Agent Systems
**Insert after:** Real-Time Data for Agents slide
**Format:** Architecture diagram
**⚡ ADVANCED**

**Content:**

Multi-agent systems have unique data requirements that single-model architectures don't face:

```
┌──────────────────────────────────────────────────────────┐
│                   AGENT LAYER                              │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐    │
│  │ Agent A │  │ Agent B │  │ Agent C │  │ Agent D │    │
│  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘    │
│       │             │             │             │          │
└───────┼─────────────┼─────────────┼─────────────┼────────┘
        │             │             │             │
        ▼             ▼             ▼             ▼
┌──────────────────────────────────────────────────────────┐
│              SHARED DATA INFRASTRUCTURE                    │
│                                                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │ Semantic     │  │ Event        │  │ State        │   │
│  │ Layer        │  │ Bus          │  │ Store        │   │
│  │ (definitions)│  │ (real-time)  │  │ (memory)     │   │
│  └──────────────┘  └──────────────┘  └──────────────┘   │
│                                                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │ Vector       │  │ Knowledge    │  │ Audit        │   │
│  │ Index        │  │ Graph        │  │ Log          │   │
│  │ (retrieval)  │  │ (relations)  │  │ (provenance) │   │
│  └──────────────┘  └──────────────┘  └──────────────┘   │
└──────────────────────────────────────────────────────────┘
```

**Key Principles:**
1. **Shared state, not shared context** — agents access common data stores rather than passing large contexts between them
2. **Event-driven coordination** — agents communicate via events, not direct calls
3. **Semantic governance** — all agents query the same metric definitions (semantic layer)
4. **Audit by default** — every data access and action is logged for compliance
5. **Freshness guarantees** — each data source declares its staleness tolerance

**Facilitator Notes:**
- 🎤 "This is where data foundations meets Module 12 (multi-agent orchestration). The data architecture IS the coordination architecture."
- For advanced students only; skip for beginners
- Draw the connection: "Module 4 teaches you the infrastructure. Modules 11–13 teach you the agents that consume it."
- Time: 5 minutes

---

### [NEW 2026] Slide: Data Governance for AI — The 2026 Maturity Model
**Insert after:** Data Governance Basics section
**Format:** Maturity model table

**Content:**

**From "Nice to Have" to "Agent Safety Requirement":**

In 2024, data governance was about compliance. In 2026, it's about **preventing autonomous agents from taking harmful actions on bad data**.

| Level | Name | Characteristics | AI Capability |
|---|---|---|---|
| 1 | **Ad hoc** | No formal governance; tribal knowledge | Chatbot demos only |
| 2 | **Documented** | Data catalog exists; ownership defined | Simple RAG systems |
| 3 | **Measured** | Quality metrics tracked; lineage visible | Production AI features |
| 4 | **Governed** | Semantic layer; access policies enforced; automated quality | Supervised agents |
| 5 | **Autonomous** | Self-healing data; real-time quality; full provenance | Autonomous multi-agent systems |

**The 2026 Requirements Stack:**
- **Data Lineage**: Where did this data come from? (Required for EU AI Act high-risk systems)
- **Quality SLAs**: What freshness/accuracy is guaranteed? (Required for agent decision-making)
- **Access Policies**: Who/what can read/write? (Required for agent sandboxing)
- **Semantic Definitions**: What does "revenue" mean? (Required for consistent agent behaviour)
- **Provenance Tracking**: What path did the agent follow to reach its conclusion? (Required for audit)

**Facilitator Notes:**
- 🎤 "Where is your organisation on this scale? Be honest. Most are at level 2. The question is: what AI ambitions require level 4 or 5?"
- Interactive: ask students to self-assess their org's level
- Connects to Module 16 (Governance) for the regulatory dimension
- Time: 5 minutes

---

### [NEW 2026] Slide: Building a Data Strategy for the Agentic Era
**Insert after:** Data Governance Maturity Model slide
**Format:** Framework / checklist

**Content:**

**The 3-Layer Data Strategy for AI:**

| Layer | Question | Deliverable |
|---|---|---|
| **Foundation** | "Is our data trustworthy?" | Quality SLAs, lineage, ownership, deduplication |
| **Accessibility** | "Can AI consume our data?" | Semantic layer, vector index, knowledge graph, APIs |
| **Feedback** | "Does usage improve the system?" | Data flywheel, monitoring, MAPE loops, human feedback capture |

**Data Strategy Checklist for Agentic AI Readiness:**

- [ ] Core entities deduplicated and reconciled
- [ ] Semantic layer with business metric definitions published
- [ ] Vector embeddings generated for key document corpus
- [ ] Knowledge graph of entity relationships maintained
- [ ] Real-time event stream available for time-sensitive decisions
- [ ] Data quality monitoring with automated alerting
- [ ] Feedback capture mechanism in production
- [ ] Access policies defined per data source (agent-consumable)
- [ ] Provenance/lineage tracking for regulatory compliance
- [ ] Synthetic data pipeline for testing and evaluation

**Facilitator Notes:**
- 🎤 "This is your homework slide. Take a photo of this checklist and score your organisation. Each unchecked box is a risk to your AI deployment."
- Have students work in pairs to score their organisation (2 minutes)
- Connects the module back to practical action
- Time: 4 minutes

---

### [NEW 2026] Slide: Case Study — How Stale Data Cost an AI Agent $2.3M
**Insert after:** Real-World Examples section
**Format:** Case study / narrative

**Content:**

**The Setup:**
A logistics company deployed an AI agent to optimise warehouse inventory allocation across 12 regional distribution centres. The agent consumed sales forecast data, current inventory levels, and shipping capacity.

**The Failure:**
The sales forecast ETL pipeline failed silently on a Thursday evening. By Monday morning, the agent had redistributed $8.4M of inventory based on 4-day-old forecasts that didn't account for a major weekend promotional event.

**The Consequence:**
- 3 distribution centres were overstocked with slow-moving items
- 2 centres ran out of promoted products → lost £2.3M in weekend sales
- Emergency overnight shipping to rebalance cost £180K
- Customer NPS dropped 12 points in affected regions

**Root Causes:**
1. No staleness check on input data (agent assumed freshness)
2. No alerting on pipeline failure (ETL failed silently)
3. No human-in-the-loop for decisions above threshold (> £500K reallocation)
4. No semantic layer defining "current inventory" freshness SLA

**Lessons:**
- Agents MUST validate data freshness before acting
- Every data source needs a declared staleness tolerance
- High-impact actions need human confirmation thresholds
- Silent pipeline failures are the #1 agentic risk

**Facilitator Notes:**
- 🎤 Tell this as a story — pause before the consequence for effect. "What do you think happened next?"
- Ask: "How would you prevent this?" → leads naturally into the governance and freshness monitoring content
- Time: 4 minutes

---

### [NEW 2026] Slide: The Unstructured Data Opportunity
**Insert after:** Data Taxonomy section
**Format:** Data visualisation concept + statistics

**Content:**

**The Scale:**
- 175+ zettabytes of data globally by 2026
- **90% is unstructured** — PDFs, emails, images, video, audio, code, logs
- Only 18% of enterprise unstructured data has been made AI-consumable (estimated)
- This means **82% of enterprise knowledge is invisible to AI systems**

**Why This Is the Biggest Opportunity:**
Every organisation has decades of knowledge locked in:
- Customer contracts and legal agreements
- Engineering documentation and design specs
- Meeting recordings and video content
- Email threads with institutional decisions
- Handwritten notes and whiteboard photos
- Financial reports and compliance documents

**The Unlock: Multimodal AI Processing**
2025–2026 advances make processing ALL these formats feasible:
- Vision-Language Models (VLMs) understand documents as images
- Whisper/Transcribe handle audio → text at production scale
- LLMs extract structured data from free text reliably
- Multimodal embeddings capture text + visual semantics together

**Facilitator Notes:**
- 🎤 "The biggest competitive advantage in AI right now is not a better model — it's access to more of your own data. 82% of enterprise knowledge is sitting there, unprocessed."
- Rhetorical question: "If you could make ALL your company's documents searchable and queryable by AI tomorrow, what would you build?"
- Time: 4 minutes

---

### [NEW 2026] Slide: Embedding Models — The 2026 Landscape
**Insert after:** Embeddings and Vector Representations section
**Format:** Comparison table
**[UPDATE 2026]**

**Content:**

The embedding model landscape has evolved significantly since 2024:

| Model | Dimensions | Context | Best For | Released |
|---|---|---|---|---|
| OpenAI text-embedding-3-large | 3,072 | 8K tokens | General purpose text | 2024 |
| Cohere Embed v3 | 1,024 | 512 tokens | Multilingual, short docs | 2024 |
| Amazon Titan Embeddings V2 | 1,024 | 8K tokens | AWS-native, multilingual | 2024 |
| Voyage AI 3 | 1,024 | 32K tokens | Code + long documents | 2025 |
| GTE-Qwen2 (open source) | 768-1,024 | 8K tokens | Open-source alternative | 2025 |
| Nomic Embed v2 | 768 | 8K tokens | Long-context, open source | 2025 |
| ColPali/ColQwen2 | Multi-vector | Page image | Visual documents | 2024–2025 |
| Jina Embeddings v3 | 1,024 | 8K tokens | Task-specific (retrieval, classification) | 2025 |

**Key Trends (2026):**
- **Matryoshka embeddings** — variable-dimension outputs; choose precision vs. speed at query time
- **Late interaction** — multi-vector per document for fine-grained matching (ColBERT-style)
- **Instruction-tuned embeddings** — tell the model what you're embedding for ("retrieve documents about...")
- **Multimodal embeddings** — same vector space for text, images, audio

**Facilitator Notes:**
- 🎤 "Embeddings are the unsung hero of modern AI. Choosing the right model for your use case can be the difference between 70% and 95% retrieval accuracy."
- For beginners: focus on "what embeddings do" and the key factors (dimensions, context length). For advanced: discuss Matryoshka and late interaction.
- Time: 4 minutes

---

### [NEW 2026] Slide: Hybrid Search — The 2026 Default
**Insert after:** Embedding Models slide
**Format:** Concept with comparison

**Content:**

**The Shift: Vector Search Is No Longer Enough**

2024: "Just use vector search"
2026: "Always combine vector + keyword (BM25) + optionally graph"

**Why Hybrid Wins:**
- Vector search excels at semantic similarity but misses exact matches ("error code E-4207")
- Keyword search (BM25) excels at exact matching but misses semantics ("car" vs "automobile")
- Combining them with a reranker gives the best of both

**Hybrid Search Architecture:**
```
Query
  ├── Vector search → top-K semantically similar
  ├── BM25 keyword search → top-K exact matches
  └── (Optional) Graph traversal → related entities
         │
         ▼
    Reciprocal Rank Fusion (RRF) or Cross-Encoder Reranker
         │
         ▼
    Final ranked results
```

**Data Point:** Cross-encoder reranking adds 33–40% retrieval accuracy for roughly 120ms of added latency.

**Default 2026 Stack:** Vector DB with hybrid search built in (Weaviate, Qdrant, pgvector + tsvector, OpenSearch)

**Facilitator Notes:**
- 🎤 "In 2024, vector search was the cutting edge. In 2026, it's a component. The default is hybrid search — and if you're not doing it, you're leaving accuracy on the table."
- Time: 4 minutes

---

### [NEW 2026] Slide: Data for Evaluation — Building Eval Datasets
**Insert after:** Data Strategy Checklist slide
**Format:** Process + guidance

**Content:**

**The Most Overlooked Data Requirement:**
Teams build data pipelines for training and retrieval but forget they also need **evaluation data** — curated datasets that prove the AI system works.

**What You Need:**

| Eval Type | Dataset Required | Example |
|---|---|---|
| Retrieval quality | Query-document relevance pairs | "For query X, documents A and C are relevant" |
| Generation quality | Query + golden answer pairs | "For question X, the correct answer is Y" |
| End-to-end | User scenarios with expected outcomes | "Given this customer complaint, agent should..." |
| Regression | Historical production outputs | "These 500 prod answers were rated good" |

**How to Build Eval Datasets:**
1. **Mine production** — Capture real user queries + human judgments (thumbs up/down, corrections)
2. **Expert annotation** — Domain experts label a small set (50–200 examples is often enough)
3. **LLM-as-judge calibration** — Use expert labels to calibrate an LLM judge, then scale
4. **Synthetic expansion** — Generate variants of real queries for coverage

**Rule of Thumb:** Start with 50 hand-curated examples. You can evaluate meaningfully from day one.

**Facilitator Notes:**
- 🎤 "If you don't have eval data, you can't prove your AI works, you can't measure improvement, and you can't catch regressions. This is the data most teams forget to build."
- Connects to Module 15 (Observability) — eval data is the foundation of the evaluation practices taught there
- Time: 4 minutes

---

### [NEW 2026] Slide: Hands-On Activity Update — Data Readiness Assessment v2
**Insert after:** Hands-On Activity section
**Format:** Activity update
**[UPDATE 2026]**

**Content:**

**Updated Activity: AI Data Readiness Assessment (v2)**

Add these 2026-specific dimensions to the existing Data Readiness Assessment:

**New Scorecard Dimensions:**

| Dimension | Score 1 (Poor) | Score 3 (Adequate) | Score 5 (Excellent) |
|---|---|---|---|
| **Semantic layer** | No shared definitions | Partial coverage, BI-only | Machine-consumable, agent-ready |
| **Real-time capability** | Batch only (daily/weekly) | Near-real-time (hourly) | Event-driven streaming |
| **Entity resolution** | Widespread duplicates | Key entities deduplicated | Automated entity matching |
| **Knowledge graph** | None | Exists but not AI-connected | Integrated with retrieval |
| **Eval datasets** | None curated | Small set exists | Production-mined, continuously updated |
| **Data flywheel** | No feedback loop | Feedback captured but unused | Active MAPE loop improving system |

**Extended Scenario:** Give students a scenario where they're evaluating a company's readiness to deploy an agentic AI system that manages customer support escalation, including: reading support tickets (unstructured), checking customer history (structured), escalating to the right team (knowledge graph), and learning from resolutions (flywheel).

**Facilitator Notes:**
- 🎤 Add 5 minutes to the activity for the new dimensions
- Students often score themselves higher on the original dimensions and lower on the new 2026 ones — use this contrast to motivate continued learning
- Time: additional 5 minutes on top of existing activity

---

### [NEW 2026] Slide: Discussion Questions — 2026 Additions
**Insert after:** Discussion Questions section
**Format:** Discussion
**[UPDATE 2026]**

**Content:**

Add these discussion questions to the existing set:

6. **"An agent that acts on 24-hour-old data versus an agent that acts on real-time data — how should you decide which your use case needs? What's the cost-benefit framework?"**

7. **"Your organisation has 10 years of customer contracts in PDF format. How would you make this knowledge accessible to an AI agent? Walk through the pipeline."**

8. **"A semantic layer ensures all agents use the same definition of 'revenue.' But who should own and maintain those definitions — data engineering, finance, or AI teams? Why?"**

**Facilitator Notes:**
- 🎤 Questions 6-8 bring the module into the 2026 agentic context
- Question 7 is excellent for engineers; Question 8 is better for leaders/PMs
- Time: 3-4 minutes for one additional question

---

### [NEW 2026] Slide: Knowledge Check — Additional Questions
**Insert after:** Knowledge Check section
**Format:** Quiz
**[UPDATE 2026]**

**Content:**

Add these questions:

Q6. What did Microsoft's GraphRAG research demonstrate about knowledge graphs?
- A) They are 10× faster than vector databases
- B) They improved multi-hop reasoning accuracy from 16.7% to 56.2% ✅
- C) They eliminated the need for embeddings entirely
- D) They reduced LLM costs by 80%

Q7. According to the TDWI 2026 benchmark, what percentage of organisations have a governed, machine-consumable semantic layer?
- A) 72%
- B) 53%
- C) 27% ✅
- D) 11%

Q8. What is a "data flywheel" in the context of AI systems?
- A) A technique for compressing training data
- B) A self-reinforcing loop where production usage generates data that improves the system ✅
- C) A method for rotating encryption keys on data stores
- D) A scheduling algorithm for batch processing

**Facilitator Notes:**
- 🎤 These test the new 2026 content specifically
- Time: 2 minutes additional

---

## Facilitator Update Brief

### 🎯 Top 3 Most Important Additions

1. **Data Quality for Agentic Systems** (Slides: Data Readiness Gap + 5 Issues That Break Agents + Case Study) — This is THE message of the 2026 update. Students need to understand that agents don't just read data; they act on it. Bad data → bad actions → real harm. The TDWI statistics and the $2.3M case study make this concrete.

2. **Knowledge Graphs + GraphRAG** (Slides: Knowledge Graphs + GraphRAG + Decision Matrix) — This is no longer a niche topic. Microsoft's 3.4× improvement on multi-hop reasoning has made GraphRAG an expected part of enterprise RAG architecture. Students will encounter it in the wild.

3. **The Semantic Layer** (Slide: Semantic Layer for AI Agents) — MIT CISR formalised this in May 2026. Only 27% of enterprises have one. It's the critical interface between data and AI agents. Without it, every agent invents its own metric definitions.

### 📝 What's Now Outdated

| Original Content | Issue | How to Address |
|---|---|---|
| Vector store section | Presented as cutting edge; now table stakes | Reframe as "baseline" and add hybrid search as the new default |
| Data governance basics | Treated as compliance-driven only | Update framing: governance is now an agent safety requirement, not just regulatory |
| Embedding coverage | Only text embeddings discussed | Add multimodal embeddings section; acknowledge ColPali and VLM approaches |
| Data strategy | Static, warehouse-centric | Add streaming, flywheel, and semantic layer dimensions |

### ⏱️ Timing Guidance

The original module is 60 minutes. With all new slides, the full expanded version is approximately **85–90 minutes**.

**Recommended approaches:**

| Audience | Approach | Time |
|---|---|---|
| **Mixed audience** | Deliver original + top 3 additions (agentic data quality, knowledge graphs, semantic layer) | 75 min |
| **Engineers/architects** | Add GraphRAG, multimodal embeddings, hybrid search, event-driven architecture | 90 min |
| **Leaders/PMs** | Focus on data readiness gap, semantic layer, flywheel, case study | 70 min |
| **Beginners** | Deliver original + data readiness gap only; skip ⚡ ADVANCED slides | 65 min |

### 🛠️ New Tools / Demos to Set Up

| Tool | Purpose | Setup Needed |
|---|---|---|
| Microsoft GraphRAG | Demo knowledge graph construction from text | `pip install graphrag`; prepare a small document corpus (5-10 pages) |
| ColPali | Demo multimodal document embeddings | Hugging Face account; GPU access recommended |
| Neo4j Aura Free | Show knowledge graph exploration | Free cloud account at neo4j.com/cloud |
| Unstructured.io | Demo document parsing pipeline | Free API key at unstructured.io |
| RisingWave | Show streaming SQL for real-time agent data | Docker or free cloud tier |

---

*Module 04 Update — AI & Agentic AI Training Programme — July 2026*
