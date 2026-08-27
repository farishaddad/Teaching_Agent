# Module 08 — RAG: Retrieval-Augmented Generation
## [2026 UPDATE] New Slides, Gap Analysis & Facilitator Delivery Notes

---

## GAP ANALYSIS

The original Module 08 covered the foundational RAG pipeline well but is now missing several significant 2025–2026 developments:

1. **Context Engineering for RAG is the new framing** — The industry has shifted from thinking about "prompt engineering for RAG" to "context engineering": what goes into the window, when, and in what order. The original module treats this as implicit.

2. **Agentic RAG has matured from concept to production pattern** — The original mentions "Agentic RAG" as an evolution but doesn't cover the specific architecture: control loops, retrieval evaluation, query rewriting, iteration caps, or the Self-RAG/CRAG/Adaptive RAG taxonomy.

3. **Contextual Retrieval (Anthropic) is missing entirely** — Launched September 2024, now production-standard. Reduces retrieval failures by 49% (67% with reranking). Available on AWS Bedrock Knowledge Bases since June 2025.

4. **Late Chunking is missing entirely** — Jina AI's technique (2024) that embeds the full document first, chunks after the transformer, preserving cross-chunk context. Now in Elasticsearch and production systems.

5. **ColPali / Multimodal RAG is missing** — Vision-language model approach to document retrieval (skips OCR entirely, embeds page images directly). A paradigm shift for document-heavy enterprise RAG.

6. **GraphRAG is underrepresented** — Microsoft's GraphRAG (knowledge graph + community summaries) is now the standard for entity-rich, relational queries. The original mentions it only in passing.

7. **RAG evaluation has matured dramatically** — RAGAS has become the de facto eval framework with specific metrics (faithfulness, context precision, answer relevancy). The original covers evaluation conceptually but lacks the specific metric definitions and production targets.

8. **Production failure modes are now well-documented** — Research shows 64% of RAG failures come from retrieval, 23% from chunking. The "10 retrieval failure modes" framework is now standard knowledge.

9. **MCP as retrieval surface is missing** — Model Context Protocol (donated to Linux Foundation Dec 2025) is now the standard tool interface for retrieval tools in agentic systems.

10. **Cost/latency reality of advanced RAG is not addressed** — Agentic RAG costs 3-10x more tokens and 2-5x latency. Students need the decision framework for when this cost is justified.

---

## NEW SLIDES

---

### [NEW 2026] Slide 1: The RAG Landscape Has Shifted — 2024 vs 2026

**Insert after:** "Why RAG Exists" section  
**Format:** Comparison table

**Content:**

The RAG landscape has fundamentally evolved in 24 months. What was cutting-edge in 2024 is now baseline:

| Dimension | 2024 Reality | 2026 Reality |
|---|---|---|
| **Tool protocol** | Custom tool wrappers per framework | MCP (Linux Foundation standard, Dec 2025) |
| **Provider retrieval** | None | Anthropic Citations API, OpenAI File Search, Gemini Grounding |
| **Reranker leader** | Cohere Rerank v3 | Voyage AI rerank-2.5 (10-12% lift over Cohere v3.5) |
| **Eval surface** | Manual LLM-judge | RAGAS + Phoenix + Langfuse with golden-set discipline |
| **Default orchestration** | LangChain sequential chains | LangGraph stateful graphs |
| **Multi-hop** | Manual chain-of-thought | Self-RAG, CRAG, Adaptive RAG patterns |
| **Chunking** | Fixed-size with overlap | Contextual Retrieval, Late Chunking, semantic boundary detection |
| **Document understanding** | OCR → text → embed | ColPali visual embedding (skip OCR) |

> *"A 2024 RAG project that took two engineers six weeks now takes one engineer four weeks at the same quality. The upgraded (agentic, evaluated, observable) version takes six weeks and costs 3-10x more in tokens at runtime."* — MarsDevs Production Guide, 2026

**Facilitator Notes:**
- Open with: "If you built RAG in 2024, your architecture is already a generation behind. Let's see what's changed."
- Common student question: "Do I need to rebuild my existing RAG?" — Answer: Not necessarily. Contextual retrieval and better rerankers can be added incrementally. Agentic patterns are an architectural shift.
- Time: 4 minutes
- Emphasise: the tool protocol shift (MCP) and eval maturity are the biggest structural changes

---

### [NEW 2026] Slide 2: Production RAG Failure Modes — Where Things Actually Break

**Insert after:** RAG pipeline overview section  
**Format:** Data-driven concept slide

**Content:**

Research in 2026 has definitively mapped where RAG systems fail in production:

```
┌────────────────────────────────────────────────────────────┐
│           WHERE RAG ACTUALLY FAILS (2026 DATA)             │
├────────────────────────────────────────────────────────────┤
│                                                            │
│   ████████████████████████████████  64% — RETRIEVAL        │
│   Relevance filtering, semantic mismatch,                  │
│   wrong docs in top-K                                      │
│                                                            │
│   ████████████████  23% — CHUNKING                         │
│   Bad splits, lost context, broken tables                  │
│                                                            │
│   █████  8% — GENERATION                                   │
│   Hallucination despite good context                       │
│                                                            │
│   ███  5% — OTHER                                          │
│   Latency, cost, staleness                                 │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

**Key insight:** *Teams obsess over which LLM to use while the actual problem sits upstream in how data is ingested, chunked, and indexed.*

**The 10 Production Retrieval Failure Modes:**
1. Semantic mismatch (query and docs use different terminology)
2. Missing context (answer spans multiple documents)
3. Ambiguous queries (multiple valid interpretations)
4. Stale embeddings (source updated, index not)
5. Metadata gaps (no filtering by date/source/type)
6. Chunking artifacts (tables split, headers orphaned)
7. Embedding drift (model updated, old vectors incompatible)
8. Reranking bottleneck (p95 latency spikes)
9. Over-retrieval (too many chunks dilute signal)
10. Permission leakage (user sees content they shouldn't)

**Facilitator Notes:**
- This is a "wake-up call" slide. Students often think RAG problems = LLM problems. The data says otherwise.
- Common question: "How do I know which failure mode I have?" — Answer: instrument retrieval separately from generation. RAGAS context_precision metric exposes retrieval failures directly.
- Time: 5 minutes
- Ask students: "In your RAG systems, where do you see the most failures?" (poll)

---

### [NEW 2026] Slide 3: Contextual Retrieval (Anthropic) — The 49% Fix

**Insert after:** Chunking strategies section  
**Format:** Concept explanation with before/after

**Content:**

**The Problem:** Traditional chunking creates "orphan chunks" — fragments that lose the context of their parent document. A chunk saying "The company reported $2.3B revenue" is meaningless without knowing *which* company.

**Anthropic's Solution: Contextual Retrieval (September 2024)**

Before embedding each chunk, use an LLM to prepend a short contextual summary that anchors it to the source document:

```
BEFORE (standard chunking):
"The company reported $2.3B revenue in Q4, representing 
a 15% increase year-over-year."

AFTER (contextual retrieval):
"[This chunk is from Acme Corp's 2024 Annual Report, 
specifically the Financial Highlights section discussing 
Q4 performance.] The company reported $2.3B revenue in 
Q4, representing a 15% increase year-over-year."
```

**Results (Anthropic's benchmarks):**
- Contextual Embeddings alone: **35% reduction** in top-20 retrieval failures
- Contextual Embeddings + BM25 (hybrid): **49% reduction** in retrieval failures
- Contextual Embeddings + BM25 + Reranking: **67% reduction** in retrieval failures

**Implementation notes:**
- Uses Claude (or any capable LLM) to generate ~50-100 token context prefix per chunk
- Available natively on **AWS Bedrock Knowledge Bases** since June 2025
- Cost: ~$1.50 per 1M tokens for context generation (one-time at index time)
- Trade-off: higher indexing cost, much better retrieval quality

**Facilitator Notes:**
- This is one of the highest-impact slides. Students can implement this in existing pipelines immediately.
- Common question: "Isn't this expensive?" — Answer: It's a one-time cost at indexing. The quality improvement typically pays for itself in reduced hallucination incidents.
- Demo suggestion: Show the AWS Bedrock Knowledge Bases contextual retrieval configuration
- Time: 5 minutes

---

### [NEW 2026] Slide 4: Late Chunking — Embed First, Chunk Second

**Insert after:** Contextual Retrieval slide  
**Format:** Concept explanation with diagram

**Content:**

**The Insight:** Standard RAG embeds each chunk independently — each chunk is an island with no awareness of its neighbours. Late Chunking inverts the order.

**Standard Chunking:**
```
Document → [split into chunks] → [embed each chunk independently] → store
```

**Late Chunking (Jina AI, 2024):**
```
Document → [embed ALL tokens with long-context model] → [split after transformer] → store
```

**How it works:**
1. Feed the entire document (up to 8,192 tokens) through a long-context embedding model
2. The transformer's attention mechanism captures cross-chunk dependencies
3. *After* the transformer forward pass, apply chunking boundaries
4. Mean-pool within each chunk to get per-chunk embeddings
5. Each chunk embedding now "remembers" its context from the full document

**Key research finding (Vectara, NAACL 2025):**
> Chunking configuration had **as much or more influence** on retrieval quality as the choice of embedding model. Getting chunking wrong drops context precision by 15-30%.

**Late Chunking vs Contextual Retrieval:**
| Dimension | Late Chunking | Contextual Retrieval |
|---|---|---|
| How context is preserved | Via transformer attention | Via LLM-generated prefix |
| Compute cost | Single embedding pass | LLM call per chunk |
| Scalability | Very high (no LLM at index time) | Moderate (LLM cost at index) |
| Context quality | Implicit (attention patterns) | Explicit (readable prefix) |
| Best for | High-volume, cost-sensitive | High-stakes, quality-critical |

**Available in:** Jina Embeddings v2+, Elasticsearch (via Jina plugin)

**Facilitator Notes:**
- This is a more technical slide. Beginners can understand the "embed first, chunk second" intuition; advanced students will want to discuss the attention mechanism details.
- Common question: "Which is better, late chunking or contextual retrieval?" — They solve the same problem differently. Late chunking is cheaper at scale; contextual retrieval produces more interpretable context.
- Time: 4 minutes
- ⚡ ADVANCED — can be briefly summarised for beginner audiences

---

### [NEW 2026] Slide 5: ColPali — Multimodal RAG Without OCR

**Insert after:** Late Chunking slide  
**Format:** Concept explanation with architecture comparison

**Content:**

**The paradigm shift:** What if you didn't need OCR at all?

**ColPali** (2024, ICLR 2025) uses a Vision Language Model (PaliGemma-3B) to embed document *images* directly — no text extraction, no chunking, no OCR pipeline.

**Traditional Document RAG:**
```
PDF → OCR → text extraction → chunking → embedding → retrieval
     (lossy) (slow)         (destroys   (context-free)
                            layout)
```

**ColPali Document RAG:**
```
PDF → render page images → visual embedding → late interaction retrieval
     (lossless)          (layout-aware)      (patch-level matching)
```

**Why this matters:**
- OCR loses table structure, diagram content, and spatial relationships
- Complex documents (financial reports, scientific papers, engineering drawings) are poorly served by text-only RAG
- ColPali produces patch-level embeddings from page images, enabling retrieval based on visual similarity

**Performance:**
- Outperforms traditional OCR + text embedding pipelines on ViDoRe benchmark
- Dramatically simpler pipeline (fewer failure points)
- Works for any document type including handwritten, scanned, or graphically complex

**When to use ColPali vs text-based RAG:**
| Use Case | Recommendation |
|---|---|
| Text-heavy documents (contracts, emails) | Text-based RAG (cheaper, mature) |
| Tables, charts, mixed-format PDFs | ColPali |
| Scanned/handwritten documents | ColPali |
| Engineering drawings, diagrams | ColPali |
| Multi-language documents | ColPali (no language-specific OCR needed) |

**Available via:** HuggingFace Transformers, custom deployment on GPU

**Facilitator Notes:**
- This is a "wow moment" slide — students are often surprised you can skip OCR entirely
- Common question: "Is this production-ready?" — Answer: Yes for retrieval. The generation still uses text, but you can pair ColPali retrieval with a VLM (GPT-4V, Claude 3.5) for generation.
- Demo idea: Show side-by-side retrieval on a complex PDF (financial table) — text-based vs ColPali
- Time: 4 minutes
- ⚡ ADVANCED — can be briefly mentioned as "emerging" for beginner audiences

---

### [NEW 2026] Slide 6: GraphRAG — When Relationships Matter More Than Similarity

**Insert after:** Advanced RAG patterns section  
**Format:** Concept + architecture diagram

**Content:**

**The limitation of vector RAG:** Embedding similarity finds *topically related* content. It cannot answer questions that require understanding *relationships between entities* across a corpus.

**Example:** "How does Company X's partnership with Company Y affect their joint strategy in market Z?" — No single chunk contains this answer. It requires synthesising across multiple documents.

**Microsoft's GraphRAG (2024, open-source):**
1. **Index time:** LLM extracts entities and relationships → builds knowledge graph → creates hierarchical community summaries
2. **Query time:** Two retrieval modes:
   - **Local Search:** Finds specific entities and traverses their graph neighbourhood
   - **Global Search:** Uses pre-built community summaries for corpus-wide questions

**Architecture:**
```
Documents → [Entity Extraction] → Knowledge Graph
                                       │
                 ┌─────────────────────┼─────────────────────┐
                 │                     │                     │
           Community 1           Community 2           Community 3
           (summary)             (summary)             (summary)
                 │                     │                     │
           Sub-communities       Sub-communities       Sub-communities
```

**When GraphRAG beats Vector RAG:**
- Entity-rich domains (org charts, supply chains, legal cases)
- Multi-hop questions requiring relationship traversal
- "Compare and contrast" or "how does X relate to Y" queries
- Corpus-wide synthesis ("What are the main themes across all documents?")

**When Vector RAG is still better:**
- Simple factual lookups
- Topical search (find content about X)
- Speed-critical applications (GraphRAG indexing is expensive)

**Production reality:**
- GraphRAG indexing costs: ~$5-15 per 1000 documents (LLM extraction)
- Query latency: 3-8 seconds for global search
- Best used as a *complement* to vector RAG, not a replacement

**Available:** Microsoft GraphRAG (open source on GitHub), Neo4j + LangChain integration, Amazon Neptune

**Facilitator Notes:**
- Sketch the graph on whiteboard during explanation — visual representation makes this click
- Common question: "Isn't this just a knowledge graph?" — Answer: Yes, but auto-generated by LLMs and with hierarchical community summaries specifically designed for RAG. The "RAG" part is the query-time summarisation over communities.
- Time: 5 minutes
- Emphasise the cost: GraphRAG is powerful but expensive to index. Right tool for right job.

---

### [NEW 2026] Slide 7: Agentic RAG — From Pipeline to Control Loop

**Insert after:** "Naive vs Advanced vs Agentic RAG" section  
**Format:** Architecture deep-dive

**Content:**

**The core shift:** Traditional RAG is a function call. Agentic RAG is a state machine.

```
TRADITIONAL RAG (pipeline):
  Query → Embed → Retrieve → Generate → Answer
  
AGENTIC RAG (control loop):
  Query → Plan → Retrieve → Evaluate → [Good enough?]
                                            │
                              ┌──────────── NO ────────────────┐
                              │                                 │
                         Rewrite Query                    Try Different Tool
                              │                                 │
                              └──── Retrieve Again ─────────────┘
                                            │
                              ┌──────────── YES ───────────────┐
                              │                                 │
                         Generate Answer                        │
                              │                                 │
                         Self-Verify ──── [Supported?] ── NO ──┘
                              │
                             YES
                              │
                         Return Answer
```

**Four capabilities that make RAG "agentic":**

1. **Retrieval decisions** — Agent decides *when* to retrieve (some questions don't need it)
2. **Relevance evaluation** — Agent scores retrieved docs; low-confidence triggers retry
3. **Query rewriting** — When retrieval fails, agent reformulates (e.g., "AI evidence" → "algorithmic testimony admissibility")
4. **Self-verification** — Before returning, agent checks answer is supported by evidence

**The cost reality:**
| Dimension | Traditional RAG | Agentic RAG |
|---|---|---|
| Retrieval calls/query | 1 | 2-6 (cap recommended) |
| Latency p50 | 1-2 seconds | 4-8 seconds |
| Latency p95 | 2-4 seconds | 10-15 seconds |
| Token cost | 1x | 3-10x |
| Multi-hop support | Poor | Strong |

**When agentic RAG earns its cost:**
- ✅ Multi-hop questions, ambiguous queries, high-stakes domains (legal, medical, financial)
- ❌ FAQ bots, single-fact lookups, sub-3-second UX requirements

**Facilitator Notes:**
- Draw the control loop on whiteboard. Emphasise the evaluation step as the key differentiator.
- Key message: "Agentic doesn't mean 'more complex.' It means 'can recognise and recover from retrieval failure.'"
- Common question: "How many iterations should I allow?" — Answer: Cap at 5-6. Diminishing returns beyond that; set a confidence threshold.
- Time: 6 minutes

---

### [NEW 2026] Slide 8: Self-RAG — Teaching the Model to Critique Itself

**Insert after:** Agentic RAG slide  
**Format:** Technical concept with token diagram

**Content:**

**Self-RAG** (Asai et al., ICLR 2024, top 1% of submissions) trains the LLM itself to decide when retrieval is needed and to critique its own outputs using special reflection tokens:

| Token | Purpose | Values |
|---|---|---|
| `[Retrieve]` | Should I search for more information? | Yes / No / Continue |
| `[ISREL]` | Is this retrieved document relevant? | Relevant / Irrelevant |
| `[ISSUP]` | Is my generation supported by evidence? | Fully / Partially / None |
| `[ISUSE]` | Is my overall response useful? | 5 / 4 / 3 / 2 / 1 |

**How it works in practice:**
```
User: "What's the capital of the newest EU member state?"

Model: [Retrieve=Yes] → retrieves 5 docs
  Doc 1: Croatia EU accession 2013 → [ISREL=Relevant]
  Doc 2: EU expansion history → [ISREL=Irrelevant] (discarded)
  Doc 3: Croatia capital Zagreb → [ISREL=Relevant]
  
Model generates: "Zagreb, the capital of Croatia"
  [ISSUP=Fully] — every claim traces to source
  [ISUSE=5] — directly answers question
```

**Key advantage:** Retrieval and quality decisions happen in a *single forward pass* rather than separate LLM calls. Faster and cheaper than external evaluation loops.

**Limitation:** Requires fine-tuning. If using proprietary APIs, approximate with structured prompting (captures ~80% of the benefit).

**Follow-on work:**
- **RAG-EVO** (2025): Evolutionary learning + persistent vector memory → 92.6% composite accuracy
- **A-RAG** (Feb 2026): Exposes retrieval tools directly to agent → 5-13% QA accuracy improvement

**Facilitator Notes:**
- This slide bridges Module 08 (RAG) and Module 11 (Agents). The model is becoming its own quality controller.
- Common question: "Can I do this with GPT-4 / Claude?" — Not natively (they don't have reflection tokens). But you can approximate with structured prompting that asks the model to score relevance and support.
- Time: 5 minutes
- ⚡ ADVANCED — briefly summarise for beginners ("models can learn to check their own retrieval quality")

---

### [NEW 2026] Slide 9: Corrective RAG (CRAG) — The Three-Action Framework

**Insert after:** Self-RAG slide  
**Format:** Architecture decision tree

**Content:**

**CRAG** (Yan et al., 2024) adds a lightweight retrieval evaluator that routes to three corrective actions:

```
Retrieved Documents
       │
  ┌────┴────┐
  │ Evaluate │ (retrieval quality score)
  └────┬────┘
       │
  ┌────┼──────────────────────────┐
  │    │                          │
HIGH   MEDIUM                    LOW
  │    │                          │
  ▼    ▼                          ▼
CORRECT   AMBIGUOUS            INCORRECT
  │    │                          │
Strip    Refine local docs        Discard all
irrelevant  + web search          Fall back to
sentences   Blend results         web search only
  │    │                          │
  └────┼──────────────────────────┘
       │
  ┌────┴────┐
  │ Generate │
  └─────────┘
```

**The three paths:**
1. **Correct** (high confidence): Strips irrelevant sentences, keeps only "knowledge strips" that address the query
2. **Ambiguous** (medium): Refines local docs AND searches the web, blends both
3. **Incorrect** (low): Discards retrieved docs entirely, falls back to web search

**Production characteristics:**
- Evaluator: fine-tuned T5-large (lightweight, fast)
- Added latency: 100-800ms depending on whether web search is triggered
- Plug-and-play: can be added to any existing RAG pipeline

**Key benchmark:** Meta CRAG Benchmark showed SOTA RAG solutions only answer 63% without hallucination. CRAG patterns push this significantly higher.

**Facilitator Notes:**
- Draw the three-path decision tree. Students find it very intuitive once visualised.
- Key message: "CRAG is the simplest agentic RAG pattern to implement — it's just a confidence router."
- Common question: "How do I set the confidence thresholds?" — Start with 0.7 (correct) and 0.3 (incorrect), tune from there based on your eval metrics.
- Time: 4 minutes

---

### [NEW 2026] Slide 10: Adaptive RAG — When to Retrieve vs When Not To

**Insert after:** CRAG slide  
**Format:** Decision framework

**Content:**

**Not every question needs retrieval.** Adaptive RAG adds an upfront router that classifies queries before the pipeline runs:

| Query Type | Action | Example |
|---|---|---|
| **Simple factual** | Parametric answer (no retrieval) | "What year was Python created?" |
| **Complex factual** | Standard retrieval | "What are the main features of Python 3.12?" |
| **Multi-hop** | Iterative/agentic retrieval | "Compare Python's GIL changes across versions and their performance impact" |
| **Generative/creative** | No retrieval needed | "Write a Python haiku" |
| **Ambiguous** | Clarification + targeted retrieval | "Tell me about Python" (language? snake? film?) |

**The router taxonomy (Singh et al., 2025 survey — arXiv:2501.09136):**
- **Single-agent adaptive** — one agent, conditional retrieval
- **Multi-agent** — specialist agents for different query types
- **Hierarchical** — router → sub-routers → specialists
- **Corrective** — retrieve, evaluate, correct (CRAG pattern)
- **Graph-based** — entity/relationship queries → GraphRAG path

**Production pattern:** Use a lightweight classifier (fine-tuned small model or even rules-based) as a query router. Route simple queries directly to LLM (saving latency and cost) and complex queries through the full agentic pipeline.

**Facilitator Notes:**
- This is a money-saving slide. Students realise they don't need agentic RAG for everything.
- Key message: "Route complexity appropriately. Don't pay 10x tokens for a simple factual lookup."
- Time: 3 minutes

---

### [NEW 2026] Slide 11: The 2026 RAG Evaluation Stack

**Insert after:** "Evaluating RAG Quality" section  
**Format:** Framework overview with metrics

**Content:**

**Production evaluation targets (2026 standard):**
| Metric | What It Measures | Target | Tool |
|---|---|---|---|
| **Faithfulness** | Is the answer supported by retrieved context? | ≥0.90 | RAGAS |
| **Answer Relevancy** | Does the answer address the question? | ≥0.85 | RAGAS |
| **Context Precision** | Are retrieved chunks actually relevant? | ≥0.80 | RAGAS |
| **Context Recall** | Did we retrieve all relevant chunks? | ≥0.75 | RAGAS |
| **Hallucination Rate** | % of claims not in context | ≤10% | Langfuse / Phoenix |
| **Latency p95** | Worst-case response time | <10s | Tracing |
| **Cost per query** | Token spend per interaction | Budget-dependent | Langfuse |

**The 2026 eval stack:**
```
┌─────────────────────────────────────────────────────────┐
│  RAGAS (metrics layer)                                  │
│  faithfulness, relevancy, precision, recall             │
├─────────────────────────────────────────────────────────┤
│  Langfuse / Arize Phoenix (observability layer)         │
│  traces, spans, cost attribution, per-query metrics     │
├─────────────────────────────────────────────────────────┤
│  Golden Test Set (ground truth)                          │
│  50-200 curated Q&A pairs with expected source docs     │
└─────────────────────────────────────────────────────────┘
```

**Critical insight (Stanford, 2025):** Poorly evaluated RAG systems hallucinate in up to **40% of responses**, even when they retrieve correct information. Evaluation is not optional.

**Facilitator Notes:**
- Make this actionable: "Your first task after building any RAG system is creating a golden test set of 50+ Q&A pairs."
- Common question: "What if faithfulness is high but relevancy is low?" — Your retrieval is working but your generation prompt needs fixing. These metrics isolate the problem.
- Time: 5 minutes

---

### [NEW 2026] Slide 12: MCP as Retrieval Surface — The New Standard

**Insert after:** RAG evaluation slide  
**Format:** Architecture concept

**Content:**

**Model Context Protocol (MCP)** — donated by Anthropic to the Linux Foundation's Agentic AI Foundation in December 2025, adopted by OpenAI and Google — is now the standard interface for connecting LLMs to retrieval tools.

**What this means for RAG:**
- Your vector database, knowledge base, or search index is now exposed as an **MCP tool**
- The LLM decides *when* and *how* to call retrieval (not hardcoded in the pipeline)
- Multiple retrieval sources can be composed as different MCP tools

```python
# Example: RAG via MCP tool definition
{
  "name": "search_knowledge_base",
  "description": "Search the company knowledge base for relevant documents",
  "parameters": {
    "query": {"type": "string", "description": "Search query"},
    "filters": {"type": "object", "description": "Metadata filters"},
    "top_k": {"type": "integer", "default": 5}
  }
}
```

**Provider-side retrieval (new in 2025-2026):**
- **Anthropic Citations API** — Guaranteed source pointers; cited_text doesn't count against output tokens
- **OpenAI File Search Tool** — Managed retrieval over uploaded files via Responses API
- **Amazon Bedrock Knowledge Bases** — Managed RAG with contextual retrieval built-in

**Implication:** The line between "RAG system" and "agent with retrieval tools" is blurring. MCP makes retrieval a first-class tool rather than a hardcoded pipeline step.

**Facilitator Notes:**
- Connect this to Module 12 (Multi-Agent/MCP). RAG is increasingly an agentic capability, not a standalone architecture.
- Common question: "Does this replace my vector database?" — No. Your vector DB is still the retrieval backend. MCP is the interface layer between the LLM and your retrieval infrastructure.
- Time: 4 minutes

---

### [NEW 2026] Slide 13: Multi-Hop Retrieval — Decompose, Retrieve, Synthesise

**Insert after:** Agentic RAG architecture section  
**Format:** Worked example

**Content:**

**Multi-hop retrieval** handles questions that cannot be answered from a single retrieval step:

**Example:** "How has Acme Corp's cloud spending changed since they partnered with DataCo?"

**Single-shot retrieval fails because:**
- No single document contains both the partnership timeline AND the spending data
- The answer requires correlating information from at least 3 sources

**Multi-hop decomposition:**
```
Original Query: "How has Acme Corp's cloud spending changed since they partnered with DataCo?"

Step 1 — Decompose:
  Sub-query A: "When did Acme Corp partner with DataCo?"
  Sub-query B: "What was Acme Corp's cloud spending before [date from A]?"
  Sub-query C: "What is Acme Corp's current cloud spending?"
  
Step 2 — Retrieve sequentially:
  A → retrieves partnership announcement → "January 2024"
  B → retrieves 2023 financial report → "$12M cloud spend"
  C → retrieves 2025 financial report → "$28M cloud spend"
  
Step 3 — Synthesise:
  "Since partnering with DataCo in January 2024, Acme Corp's cloud 
  spending has increased from $12M to $28M (133% increase)."
```

**Key pattern:** Later sub-queries depend on results from earlier ones. This is why agentic RAG needs a *stateful loop*, not a parallel fan-out.

**Facilitator Notes:**
- Walk through the worked example step by step. Multi-hop is where agentic RAG shines.
- Common question: "How many hops is too many?" — In practice, 2-4 hops. Beyond that, the question is probably too complex for automated answering and should involve a human.
- Time: 4 minutes

---

### [NEW 2026] Slide 14: The RAG Decision Matrix — Which Pattern When?

**Insert after:** Multi-hop retrieval slide  
**Format:** Decision framework / table

**Content:**

| Scenario | Recommended Pattern | Retrieval Calls | Latency | Cost |
|---|---|---|---|---|
| FAQ / simple lookup | Naive RAG (single-shot) | 1 | <2s | 1x |
| Domain-specific Q&A | Advanced RAG (reranking + hybrid) | 1 | 2-3s | 1.5x |
| Multi-hop reasoning | Agentic RAG (iterative) | 2-6 | 4-8s | 3-10x |
| Entity relationships | GraphRAG + vector | 1-3 | 3-8s | 2-5x |
| Document-heavy (tables, diagrams) | ColPali + VLM | 1 | 2-4s | 2x |
| High-stakes (legal, medical) | CRAG + verification | 2-4 | 5-10s | 4-8x |
| Corpus-wide synthesis | GraphRAG global search | 1 | 5-15s | 3-6x |
| Cost-sensitive at scale | Adaptive router + tiered | 1-3 | 1-8s | 1-3x avg |

**The decision tree:**
```
Is the query simple and factual?
├── YES → Naive RAG (or skip retrieval entirely)
└── NO → Does it involve entity relationships?
    ├── YES → GraphRAG
    └── NO → Does it require multiple sources?
        ├── YES → Agentic RAG (multi-hop)
        └── NO → Does it involve visual/tabular documents?
            ├── YES → ColPali
            └── NO → Advanced RAG with reranking
```

**Facilitator Notes:**
- This is the "take-home" slide students will photograph. It's a practical decision framework.
- Key message: "Start with the simplest pattern that works. Escalate complexity only when evaluation proves it necessary."
- Time: 4 minutes
- Hands-on activity connection: students map their own use cases to this matrix

---

### [NEW 2026] Slide 15: Chunking Strategy 2026 — What Actually Works

**Insert after:** Chunking strategies section  
**Format:** Practical reference with data

**Content:**

**2026 defaults (backed by benchmarks):**

| Strategy | Chunk Size | Overlap | Best For | Notes |
|---|---|---|---|---|
| **Recursive (baseline)** | 400-800 tokens | 10-20% | General text | Still the production default |
| **Semantic boundary** | Variable | N/A | Long-form content | Split at topic shifts using small LM |
| **Document-aware** | Respects structure | N/A | Tables, headers, code | 40%+ accuracy improvement on structured content |
| **Contextual Retrieval** | 400-800 + context prefix | 10-20% | Quality-critical | +49% retrieval accuracy |
| **Late Chunking** | Variable | N/A | High-volume | Cheapest way to preserve context |
| **Parent-child** | Small retrieval / large context | N/A | Precision + context | Retrieve on small, feed LLM the parent |

**Key finding (NAACL 2025):** Chunk overlap adds **no measurable benefit** in systematic testing. The most common default (20% overlap) may be wasted compute.

**Starting recipe:**
1. Start with recursive chunking, 512 tokens, 10% overlap
2. Measure context_precision with RAGAS
3. If precision < 0.8: try contextual retrieval or late chunking
4. If structured documents: switch to document-aware chunking
5. If budget allows: add Voyage AI rerank-2.5 (10-12% lift)

**Facilitator Notes:**
- Controversial finding: overlap may not help. Present the NAACL 2025 data and let students discuss.
- Common question: "What's the best chunk size?" — There is no universal answer. Start at 512, measure, adjust. The only wrong answer is not measuring.
- Time: 4 minutes

---

### [NEW 2026] Slide 16: Hybrid Search 2026 — Dense + Sparse + Reranking Stack

**Insert after:** Re-ranking and hybrid search section  
**Format:** [UPDATE 2026] Technical update to existing content

**Content:**

**The 2026 production retrieval stack:**
```
User Query
    │
    ├─── Dense Search (embedding similarity)
    │    └── text-embedding-3-large / Cohere Embed v4 / jina-embeddings-v3
    │
    ├─── Sparse Search (BM25 / keyword)
    │    └── Elasticsearch / OpenSearch BM25
    │
    └─── [Optional] Structured filters
         └── Metadata: date, source, department, classification
    
    │── Reciprocal Rank Fusion (merge results)
    │
    ├─── Cross-encoder Reranker
    │    └── Voyage AI rerank-2.5 (current leader, 10-12% over Cohere v3.5)
    │    └── Cohere Rerank v3.5 (strong alternative)
    │    └── BGE-reranker-v2.5-gemma2 (open-source option)
    │
    └─── Top-K selection → LLM context
```

**What's changed since 2024:**
- Voyage AI rerank-2.5 now leads benchmarks (10-12% over previous leader)
- Reranking is no longer optional — it's the single highest-ROI improvement you can add
- Embedding models now support instruction-prefixed queries (tell the model what you're looking for)
- Reciprocal Rank Fusion (RRF) beats learned fusion for combining dense + sparse

**Production tip:** If you change ONE thing in your RAG system, add a reranker. It consistently provides the biggest quality lift for the least engineering effort.

**Facilitator Notes:**
- If students remember one thing: "Add a reranker." It's the highest ROI improvement available.
- Demo option: Show retrieval quality before/after reranking using RAGAS context_precision metric
- Time: 4 minutes

---

### [NEW 2026] Slide 17: The "From 61% to 97%" Pipeline — A Production Case Study

**Insert after:** Real-world case studies section  
**Format:** Case study

**Content:**

**Case Study: Six-Stage RAG Pipeline That Survived Production**
*Source: Anil S. Prasad, production deployment, 2026*

**Starting point:** 61% accuracy on domain-specific questions

**Failure analysis:**
- 64% of failures came from retrieval (wrong docs in top-K)
- 23% from chunking (documents split badly at indexing)
- Only 13% from generation

**The six-stage fix:**
| Stage | What | Impact |
|---|---|---|
| 1. Document-aware chunking | Respect headers, tables, code blocks | Chunking failures: -80% |
| 2. Contextual enrichment | Add source context to each chunk | Retrieval failures: -40% |
| 3. Hybrid retrieval | Dense + BM25 + metadata filters | Recall: +25% |
| 4. Cross-encoder reranking | Voyage AI rerank-2.5 | Precision: +15% |
| 5. Relevance threshold | Discard chunks below 0.7 score | Hallucination: -30% |
| 6. Answer verification | LLM-as-judge on faithfulness | Remaining hallucination: -50% |

**Result:** 61% → 97% accuracy on same test set

**Key lesson:** "Each stage addresses a different failure mode. No single fix would have gotten us there. The order matters: fixing retrieval first (stages 1-4) unlocked the gains in generation quality (stages 5-6)."

**Facilitator Notes:**
- This is the most impactful case study. Walk through each stage and ask: "Which of these would help YOUR current system?"
- Time: 5 minutes
- Connect back to the failure modes slide — this case study validates the "64% retrieval / 23% chunking" data

---

### [NEW 2026] Slide 18: RAG Security — Permission-Aware Retrieval

**Insert after:** Production case study  
**Format:** Security concept (connects to Module 14)

**Content:**

**The hidden failure mode:** Production RAG can leak sensitive information across user boundaries.

**Permission-aware retrieval requirements:**
1. **Document-level ACLs** — Each indexed chunk carries the access permissions of its source document
2. **Query-time filtering** — Before returning results, filter by the requesting user's permissions
3. **No semantic leakage** — Embedding similarity should not surface content the user can't see in plain text
4. **Audit trail** — Log which chunks were retrieved for which user (compliance requirement)

**Architecture pattern:**
```
User Query + User Identity
    │
    ├── Retrieve top-K candidates (vector search)
    │
    ├── Filter by user permissions (ACL check)
    │
    ├── Rerank filtered set
    │
    └── Return only permitted context to LLM
```

**Common mistakes:**
- ❌ Filtering AFTER generation (LLM already saw restricted content)
- ❌ Relying on the LLM to "not mention" restricted content (unreliable)
- ❌ Indexing all documents in a single namespace without ACL metadata

**Available solutions:**
- AWS Bedrock Knowledge Bases: supports metadata filtering
- Atolio: permission-aware enterprise RAG
- Pinecone: namespace-based access control

**Facilitator Notes:**
- This connects to Module 14 (AI Security). For regulated industries, this is non-negotiable.
- Common question: "Can't we just have separate vector stores per team?" — Yes, but it doesn't scale. Metadata-based ACLs are the production pattern.
- Time: 3 minutes

---

### [NEW 2026] Slide 19: Hands-On Lab Extension — Build an Agentic RAG Pipeline

**Insert after:** Existing hands-on activity  
**Format:** Lab activity

**Content:**

**Lab Extension: Agentic RAG with LangGraph**
**Duration:** 20 minutes (extended lab) or homework  
**Prerequisite:** Completed the basic RAG pipeline lab

**Objective:** Convert a naive RAG pipeline into an agentic system with retrieval evaluation and query rewriting.

**Architecture:**
```python
# LangGraph state machine for Agentic RAG
from langgraph.graph import StateGraph

# Define state
class RAGState(TypedDict):
    question: str
    retrieved_docs: list
    relevance_score: float
    rewrite_count: int
    answer: str

# Define nodes
graph = StateGraph(RAGState)
graph.add_node("retrieve", retrieve_documents)
graph.add_node("evaluate", evaluate_relevance)
graph.add_node("rewrite", rewrite_query)
graph.add_node("generate", generate_answer)
graph.add_node("verify", verify_faithfulness)

# Define edges (the control loop)
graph.add_edge("retrieve", "evaluate")
graph.add_conditional_edges("evaluate", 
    route_by_relevance,  # score > 0.7 → generate, else → rewrite
    {"good": "generate", "poor": "rewrite"})
graph.add_edge("rewrite", "retrieve")  # loop back
graph.add_edge("generate", "verify")
```

**Steps:**
1. Start with existing basic RAG pipeline
2. Add a relevance evaluator (LLM scores retrieved chunks 0-1)
3. Add a query rewriter (triggered when relevance < 0.7)
4. Add iteration cap (max 3 retrieval attempts)
5. Add faithfulness verification on the final answer
6. Measure: latency increase, quality improvement, cost delta

**Success criteria:**
- Faithfulness ≥ 0.9 on test set
- Answers previously-failing multi-hop questions correctly
- Iteration cap prevents infinite loops

**Facilitator Notes:**
- Students can use LangGraph, LlamaIndex Workflows, or even a simple while loop
- Provide a set of 10 multi-hop test questions that naive RAG fails on
- Expected time for motivated students: 20-30 minutes for basic version
- Time for explanation: 5 minutes (students do the work after class or in an extended session)

---

### [NEW 2026] Slide 20: The Future — Where RAG Is Heading

**Insert after:** Resources section  
**Format:** Forward-looking discussion

**Content:**

**Emerging trends to watch (2026-2027):**

1. **RAG is merging with agents** — The boundary between "RAG system" and "agent with retrieval tools" is dissolving. MCP makes retrieval just another tool. Expect "RAG pipeline" to become an outdated term within 2 years.

2. **Long-context models challenge RAG** — 1M+ token windows (Gemini, Claude) reduce the need for retrieval in some cases. But cost, latency, and "lost in the middle" effects mean RAG remains essential for large corpora.

3. **Multimodal retrieval is becoming standard** — ColPali showed the way. Expect embedding models that natively handle text + images + tables within 12 months.

4. **Evaluation is becoming continuous** — Not just pre-deployment testing. Production RAG systems now run continuous faithfulness monitoring, with alerts when metrics drift.

5. **Structured retrieval is rising** — Text-to-SQL + vector search + graph traversal as composable retrieval tools, orchestrated by an agent that picks the right one per query.

6. **Provider-managed RAG** — Anthropic Citations, OpenAI File Search, Bedrock Knowledge Bases are making basic RAG a commodity. The value moves to orchestration, evaluation, and domain-specific tuning.

**Discussion question:** "If long-context models keep scaling (2M, 10M tokens), will RAG become obsolete? Why or why not?"

**Facilitator Notes:**
- End on this discussion question. It's provocative and helps students think critically.
- The consensus answer: RAG won't die because (1) cost scales with context length, (2) "lost in the middle" doesn't fully resolve, (3) freshness requires external retrieval, (4) permission control needs document-level filtering.
- Time: 4 minutes

---

## FACILITATOR UPDATE BRIEF

### Top 3 Most Important Additions

1. **Contextual Retrieval + Late Chunking (Slides 3-4)** — These are the highest-impact, most immediately actionable additions. Students can implement contextual retrieval in existing pipelines within a day. Late chunking provides a cost-effective alternative.

2. **Agentic RAG architecture (Slides 7-10)** — The Self-RAG / CRAG / Adaptive RAG taxonomy is now standard practitioner knowledge. Students will encounter these patterns in job interviews and architecture reviews. The control-loop framing (vs. pipeline) is the key mental model shift.

3. **The 2026 Evaluation Stack (Slide 11)** — RAGAS metrics with specific production targets (faithfulness ≥0.9, context precision ≥0.8) are now table stakes. This transforms evaluation from "vague quality check" to measurable engineering.

### What's Now Outdated in the Original Module

| Original Content | Issue | How to Address |
|---|---|---|
| "Naive vs Advanced vs Agentic RAG" as a simple taxonomy | The taxonomy is now richer (Self-RAG, CRAG, Adaptive, GraphRAG) | Replace with the full decision matrix (Slide 14) |
| Chunking section focused on fixed-size + overlap | Overlap may not help (NAACL 2025). Contextual retrieval and late chunking are now standard | Update with Slide 15 data; note overlap finding |
| Evaluation section mentions "faithfulness, relevance, recall" generically | RAGAS is now the named tool with specific metric definitions and targets | Replace with Slide 11 specifics |
| Re-ranking mentioned without specific tool recommendations | Voyage AI rerank-2.5 now leads (10-12% over Cohere) | Update recommendation in Slide 16 |
| No mention of MCP or provider-managed retrieval | These are now production defaults (2025-2026) | Add Slide 12 |

### Fitting New Content into 60 Minutes

**Recommended approach:** This module now has too much content for 60 minutes. Options:

1. **60-minute version (standard delivery):** Keep original structure. Add Slides 1 (landscape shift), 3 (contextual retrieval), 7 (agentic RAG), 11 (eval stack), and 14 (decision matrix). Mention others briefly as "further reading." Remove some existing detail on basic chunking.

2. **90-minute extended version (recommended for technical audiences):** Deliver all 20 new slides. Skip the basics for experienced students. Add the hands-on lab extension (Slide 19).

3. **Split into two sessions:** 
   - 8A: Foundations of RAG (original + Slides 1-6, 15-16) — chunking, retrieval, evaluation
   - 8B: Advanced & Agentic RAG (Slides 7-14, 17-20) — agentic patterns, GraphRAG, production

### New Tools/Accounts/Demos to Set Up

| Tool | What For | Setup Time |
|---|---|---|
| **RAGAS** (pip install ragas) | Live evaluation demo | 5 min |
| **Langfuse** (free tier) | Observability demo — show traces of agentic RAG | 15 min |
| **LangGraph** (pip install langgraph) | Agentic RAG control loop lab | 5 min |
| **AWS Bedrock Knowledge Bases** | Demo contextual retrieval config | Access required |
| **Voyage AI** | Reranking demo (API key needed) | 5 min |
| **A test corpus** | 50+ documents with known Q&A pairs for live demo | 30 min prep |

---

*Module 08 Update — July 2026*
