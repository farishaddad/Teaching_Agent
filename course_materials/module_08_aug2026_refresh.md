# Module 08 — RAG: Retrieval-Augmented Generation
## [NEW AUG-2026] Content Refresh Addendum
### Engineering Track | August 2026

---

## A) EXECUTIVE SUMMARY — What Changed Since July 2026

1. **BM25 beats dense retrieval by ~20 points at scale** — A landmark arxiv study (July 30, 2026) across 28 nested corpus tiers showed BM25 overtakes agents and dense retrieval at ~10M tokens and dominates at scale. Agentic retrieval wins only on small corpora at 39× the token cost. This challenges the "replace BM25" narrative.

2. **Amazon Bedrock Managed Knowledge Base went GA** (June 17, 2026) — Fully managed RAG with Agentic Retriever (multi-hop query decomposition), smart parsing, 6 native connectors (S3, SharePoint, Confluence, Web Crawler, Google Drive, OneDrive). No vector DB to manage.

3. **Amazon Kendra enters maintenance mode** (June 30, 2026) — Closed to new customers July 30. AWS consolidates enterprise retrieval onto Bedrock Knowledge Bases. Bedrock Agents Classic also deprecated.

4. **AWS publishes "Beyond RAG: Task-Aware Knowledge Compression" (TAKC)** (July 27, 2026) — A new paradigm where entire knowledge bases are pre-compressed into task-specific representations (8×–64× compression), outperforming RAG by 8 F1 points on QA tasks at 20× compression. Shifts the question from "which chunks to retrieve?" to "how to compress the whole corpus task-specifically?"

5. **Google ships Agentic RAG in Gemini Enterprise Agent Platform** (June 5, 2026) — Multi-agent RAG with a "Sufficient Context Agent" that evaluates whether enough information has been retrieved before answering. Claims +34% accuracy over standard RAG on factuality datasets.

6. **OpenAI Assistants API deprecated** — Shutting down August 26, 2026. File Search moves to the Responses API, which is "agentic by default" (multi-tool, multi-turn in a single request). Migration required.

7. **Ops-ColQwen3-4B released** — Alibaba Cloud OpenSearch-AI team open-sources a ColPali-style multimodal embedding model based on Qwen3-VL-4B, advancing visual document retrieval into production-grade OpenSearch integration.

8. **Jina Embeddings v5 launched** (February 2026) — Supports 32K token context with late chunking native support, binary quantization robustness, and task-targeted embedding distillation. Sub-1B parameter models achieving 4B-quality.

9. **Anthropic releases Claude Sonnet 5** (June 2026) and **Claude Opus 4.8** — Both models feature enhanced agentic capabilities. Claude Opus 4.6 introduced 1M token context window (February 2026), challenging the "always retrieve" assumption for moderate-sized corpora.

10. **OpenAI launches GPT-5.6 with "ultra" setting** (August 11, 2026) — Coordinates multiple agents across parallel workstreams. The Agents SDK replaces the deprecated Agent Builder product.

---

## B) NEW SLIDES

---

### [NEW AUG-2026] Slide 1: The Scaling Bombshell — BM25 Wins at Scale

**Insert after:** "Hybrid Search 2026" section (existing Slide 16)
**Source:** arxiv.org/abs/2607.26497 (July 30, 2026) + AI Weekly analysis (August 10, 2026)

**Content:**

A controlled RAG scaling study (July 2026) tested lexical, dense, graph-based, and agentic retrieval across 28 nested corpus tiers spanning ~450× in size. The headline finding:

```
                         RETRIEVAL ACCURACY vs. CORPUS SCALE
    
    100%│  🤖 Agent wins here
        │  ╲
     80%│    ╲         ┌── BM25 overtakes at ~10M tokens
        │     ╲       ╱
     60%│      ╲─────╱────────────────── BM25 ──────────── (+20pt lead)
        │       ╲  ╱
     40%│        ╳         Dense retrieval
        │       ╱ ╲
     20%│      ╱    ╲────── Agentic (fades)
        │     ╱        
      0%│────┼──────┼──────┼──────┼──────┼──────┼
        │  100K   1M    10M   50M  100M  500M+
        │              Corpus tokens →
```

**Key findings:**
- **File-System Agent** wins at small corpora (<10M tokens) but costs **39× more query tokens**
- **BM25 overtakes at ~10M tokens** and leads every tier above that by up to 20 points
- **Dense retrieval** stays efficient but less accurate at all tiers
- **GraphRAG hits construction walls** before reaching deployment scale
- BM25 anchors the low-cost end of the Pareto frontier — no LLM-based construction needed

**Practical implication:**
> *"Keep a boring BM25 baseline in production. Spend saved tokens on the reader and re-ranker rather than replacing the retriever."* — AI Weekly summary

**The new architecture mental model:**
```
BM25 (retriever) → Dense reranker (precision) → Agent (reasoning)
                    ↑ This is where to invest
```

NOT: Agent (retriever) → Agent (reader) → Agent (verifier)

**Facilitator Notes:**
- This is controversial and counter-narrative. Present the data, acknowledge limitations (one study, one reader model, one judging protocol), but emphasise the scaling insight.
- Key message: "Don't throw away BM25. Use agents for re-ranking and reasoning AFTER lexical retrieval, not in place of it."
- Common question: "Does this mean vector search is dead?" — No. Hybrid (BM25 + dense + reranker) is still the gold standard. The point is BM25 alone scales better than agents alone.
- Time: 5 minutes
- 🔥 HIGH IMPACT — This directly challenges assumptions from the July 2026 module

---

### [NEW AUG-2026] Slide 2: Amazon Bedrock Managed Knowledge Base — Fully Managed RAG (GA June 2026)

**Insert after:** "MCP as Retrieval Surface" section (existing Slide 12)
**Source:** aws.amazon.com/about-aws/whats-new/2026/06/amazon-bedrock-managed-knowledge-base/ + AWS blog

**Content:**

AWS made **Amazon Bedrock Managed Knowledge Base** generally available on June 17, 2026 at AWS Summit New York. It's a zero-infrastructure RAG service:

**What it includes:**
| Component | Capability |
|---|---|
| **Data connectors** | 6 native: S3, SharePoint, Confluence, Web Crawler, Google Drive, OneDrive |
| **Smart Parsing** | Auto-detects document type, preserves HTML structure, extracts tables/images |
| **Vector storage** | Managed by AWS (not selectable) — auto-scaling, on-demand pricing |
| **Retrieval** | Agentic Retriever with multi-hop query decomposition |
| **Embeddings** | Auto-selected (overridable) |
| **Re-ranking** | Built-in (overridable) |

**The Agentic Retriever in action:**
```
Query: "What is the ML platform team's cloud budget, and does 
        the expense policy allow prepaying annual commitments?"

Standard RAG: Finds budget doc → Misses policy link → Partial answer

Agentic Retriever:
  Step 1: Decompose → 2 sub-queries identified
  Step 2: Retrieve budget document → ✓ Found
  Step 3: Identify "expense policy" reference → Follow link
  Step 4: Retrieve policy document → ✓ Found
  Step 5: Evaluate sufficiency → Sufficient → Return
```

**Managed vs Self-Managed comparison:**
| Dimension | Managed KB | Self-Managed KB |
|---|---|---|
| Vector store | AWS-managed (no selection) | Aurora, OpenSearch, Neptune, MongoDB, Pinecone, Redis |
| Chunking | Smart Parsing defaults | Custom Lambda (LangChain/LlamaIndex) |
| GraphRAG | Not available | Available via Neptune Analytics |
| Pricing | On-demand, no upfront | OpenSearch minimum ~$350/month |
| Control | Low (opinionated defaults) | Full |

**Critical context: Amazon Kendra deprecated**
- Kendra entered maintenance mode June 30, 2026
- Closed to new customers July 30, 2026
- Migration path: Bedrock Managed Knowledge Base
- Also deprecated: Amazon Bedrock Agents Classic, Amazon Q Business

**Facilitator Notes:**
- This is the "AWS RAG consolidation" slide. AWS is betting everything on Bedrock Knowledge Bases.
- Demo suggestion: Walk through the Bedrock console setup — show how fast you can stand up a RAG pipeline with zero infrastructure.
- Common question: "Should I migrate from Kendra?" — Yes, if you're an existing customer, plan migration now. No new features coming.
- Time: 5 minutes

---

### [NEW AUG-2026] Slide 3: Beyond RAG — Task-Aware Knowledge Compression (TAKC)

**Insert after:** "The Future — Where RAG Is Heading" section (existing Slide 20)
**Source:** aws.amazon.com/blogs/machine-learning/beyond-rag-task-aware-knowledge-compression-for-enterprise-ai-on-aws/ (July 27, 2026)

**Content:**

**The limitation of RAG that no one talks about:** RAG retrieves the top-K most *similar* chunks. But for complex analytical tasks spanning hundreds of documents, the answer isn't in any single chunk — it's in the *connections between* documents.

**Task-Aware Knowledge Compression (TAKC) — A post-RAG paradigm:**

Instead of retrieving fragments at query time, TAKC **pre-compresses entire knowledge bases** into task-specific representations:

```
TRADITIONAL RAG:
  Query → Embed → Retrieve top-K → Generate
  Problem: Misses cross-document connections
  
TAKC:
  [Offline] Documents → Compress with task-specific lens → Cache
  [Query time] Query → Retrieve compressed corpus → Generate
  Advantage: Sees ALL documents, preserves connections
```

**Multi-rate compression tiers:**
| Tier | Compression | Context Reduction | Use Case |
|---|---|---|---|
| Light (8×) | ~87.5% reduced | Multi-step reasoning, cross-doc synthesis |
| Medium (16×) | ~93.8% reduced | Analytical queries, moderate complexity |
| High (32×) | ~96.9% reduced | Factual lookups, well-defined questions |
| Ultra (64×) | ~98.4% reduced | Classification, keyword lookups |

**Benchmark results (EACL 2026):**
- At 20× compression: TAKC outperforms RAG by **8 F1 points** on QA tasks
- Latency reduction: **4× faster** than RAG (no retrieval step at query time)

**When TAKC beats RAG:**
- ✅ Due diligence across hundreds of documents
- ✅ Regulatory compliance reviews (cross-reference requirements)
- ✅ Multi-subsidiary financial analysis
- ❌ Real-time document updates (requires recompression)
- ❌ Simple factual lookups (RAG is simpler and cheaper)

**AWS implementation:** Serverless architecture using Lambda + Bedrock + ElastiCache. Open-source on GitHub (aws-samples/sample-bedrock-takc-compression).

**Facilitator Notes:**
- This is a "paradigm expansion" slide. TAKC doesn't replace RAG — it addresses a specific failure mode (cross-document reasoning) that RAG structurally cannot solve.
- Key message: "RAG finds needles in haystacks. TAKC understands the whole haystack."
- Common question: "Isn't this just summarisation?" — No. It's task-specific compression that preserves different information for different tasks from the same document. The financial compression of a 10-K looks nothing like the legal risk compression.
- Time: 5 minutes
- ⚡ ADVANCED — This is cutting-edge; position as "where the field is heading"

---

### [NEW AUG-2026] Slide 4: Google's Sufficient Context Agent — Know When You Don't Know

**Insert after:** "Corrective RAG (CRAG)" section (existing Slide 9)
**Source:** research.google/blog/unlocking-dependable-responses-with-gemini-enterprise-agent-platforms-agentic-rag/ (June 5, 2026)

**Content:**

Google Research introduced a key innovation in their Agentic RAG framework (June 2026): the **Sufficient Context Agent** — a quality-control inspector that evaluates whether enough information has been retrieved before allowing generation.

**The Multi-Agent RAG Architecture:**
```
Query
  │
  ├── Orchestrator (Root Agent)
  │     └── "This isn't a one-step job"
  │
  ├── Planner Agent
  │     └── Maps information pathways across sources
  │
  ├── Query Rewriter
  │     └── Turns vague queries into multiple precise searches
  │
  ├── Search Fanout Agent
  │     └── Parallel retrieval across data sources
  │
  ├── Sufficient Context Agent ← KEY INNOVATION
  │     └── Evaluates: Do we have enough? If NO → iterate
  │
  └── Generator (final response)
```

**What makes the Sufficient Context Agent different:**

Standard agentic RAG:
- Retrieve → Score relevance → If low, rewrite query → Try again
- **Problem:** Doesn't know if it has *enough* information, only if what it found is relevant

Google's approach:
- Retrieve → Evaluate **sufficiency** → If incomplete, continue searching different sources
- **Advantage:** Prevents the AI from "guessing" when the first search comes up empty

**Result:** +34% accuracy over standard RAG on factuality datasets.

**Example (medical records):**
```
Query: "Discharge medications, dietary restrictions, and allergic 
        reactions for John Doe after knee surgery"

Phase 1 (Orchestration): Parse → 3 sub-tasks (Pharmacy, Nutrition, Clinical Notes)
Phase 2 (Search): Find medications ✓, diet ✓, allergies ✗ (not in obvious files)
Phase 3 (Sufficient Context): "Allergy info missing. Continue searching."
Phase 4 (Iterative): Search nursing notes → Find allergy record ✓
Phase 5 (Generate): Complete answer with all three elements
```

**Available in:** Google Cloud Gemini Enterprise Agent Platform (GA)

**Facilitator Notes:**
- This is a great complement to the CRAG slide. CRAG evaluates relevance; Google's agent evaluates sufficiency.
- Key message: "The innovation isn't better retrieval — it's knowing when you have enough."
- Common question: "How is this different from just doing more retrieval iterations?" — The Sufficient Context Agent has an explicit model of what "enough" means for the query. It doesn't just iterate blindly.
- Time: 4 minutes

---

### [NEW AUG-2026] Slide 5: The AWS RAG Consolidation — What Got Deprecated

**Insert after:** Amazon Bedrock Managed KB slide
**Source:** Forbes (July 24, 2026) + AWS documentation

**Content:**

On June 30, 2026, AWS moved ~20 AI services into maintenance mode. For RAG practitioners, the key casualties:

| Service | Status | Replacement | Impact |
|---|---|---|---|
| **Amazon Kendra** | Maintenance mode June 30; closed to new customers July 30 | Bedrock Managed Knowledge Base | Enterprise search customers must migrate |
| **Amazon Q Business** | Maintenance mode | Bedrock AgentCore + Knowledge Bases | Business Q&A use cases migrate |
| **Bedrock Agents Classic** | Renamed; closed to new customers July 30 | Amazon Bedrock AgentCore | All new agent work goes through AgentCore |

**The new AWS stack for RAG in August 2026:**
```
┌─────────────────────────────────────────────────┐
│  Amazon Bedrock AgentCore                        │
│  (Agent orchestration, MCP gateway, memory)      │
├─────────────────────────────────────────────────┤
│  Amazon Bedrock Knowledge Bases                  │
│  ├── Managed KB (fully managed, agentic retrieval)│
│  └── Self-managed (custom vector store, GraphRAG) │
├─────────────────────────────────────────────────┤
│  Three Knowledge Layers (June 25, 2026):         │
│  ├── Organizational Knowledge (your data)        │
│  ├── World Knowledge (web/public data)           │
│  └── Paid Knowledge (licensed data sources)      │
└─────────────────────────────────────────────────┘
```

**What AgentCore adds for RAG:**
- MCP-native: Knowledge Base exposed as an MCP connector target — agents discover and query via standard MCP calls
- Agentic Retrieval: Multi-hop decomposition, iterative retrieval, sufficiency evaluation
- Native observability: Built-in retrieval traces, agentic traces, per-KB metrics
- Three new knowledge layers: Organizational, World, and Paid knowledge sources

**Migration reality check:**
- Kendra had advanced features (FAQ extraction, document ranking, access control) that Bedrock Managed KB doesn't fully replicate yet
- Self-managed KB is the closer feature match (supports custom vector stores, GraphRAG via Neptune)
- If you need GraphRAG → Self-managed KB with Neptune Analytics
- If you want zero-ops → Managed KB (but less control)

**Facilitator Notes:**
- This is critical operational context for students on AWS. Many may have Kendra in production.
- Key message: "AWS has bet everything on Bedrock. If you're on Kendra or Agents Classic, start planning migration now."
- Time: 4 minutes

---

### [NEW AUG-2026] Slide 6: ColQwen3 and Multimodal RAG Goes Production

**Insert after:** "ColPali — Multimodal RAG Without OCR" (existing Slide 5)
**Source:** huggingface.co/OpenSearch-AI/Ops-Colqwen3-4B + arxiv.org/abs/2605.05185

**Content:**

The ColPali paradigm (visual document retrieval without OCR) has matured significantly since we last covered it:

**Evolution of visual document retrieval models:**
| Model | Base | Released | Key Advance |
|---|---|---|---|
| ColPali | PaliGemma-3B | 2024 | Original visual doc retrieval |
| ColQwen2 | Qwen2-VL | 2025 | Better multilingual, higher accuracy |
| **Ops-ColQwen3-4B** | Qwen3-VL-4B | 2026 | Production-grade, OpenSearch native |
| Jina Embeddings v4 | Qwen2.5-VL-3B | 2025 | Unified text + image, multi-vector + single-vector |

**Ops-ColQwen3-4B (Alibaba Cloud OpenSearch-AI):**
- Maps text queries AND visual documents into a unified multi-vector embedding space
- Native integration with OpenSearch for production deployment
- Handles PDFs, slides, screenshots, scanned documents natively
- **Production ready** — not just a research model

**Patch-level memory optimization (2026 research):**
- Original ColPali/ColQwen2: ~1,024 patch embeddings per page (memory-intensive)
- New research shows methods to reduce patch embeddings per page with minimal performance degradation
- Spatially-grounded retrieval: reduces context tokens by 28.8% vs returning all OCR regions

**OpenSearch multimodal search (April 2026 benchmark):**
Three approaches compared:
1. Caption-and-index (traditional): Generate text captions, index those
2. Unified vision embeddings (Cohere Embed 4, Voyage multimodal-3): Single-vector
3. Page-as-image (ColPali/ColQwen): Multi-vector late interaction

Result: Page-as-image with ColQwen models consistently outperforms on visual-heavy documents.

**When to use each approach:**
| Document Type | Best Approach |
|---|---|
| Text-heavy (contracts, emails) | Traditional text embedding |
| Mixed text + tables | Hybrid: text embedding + ColQwen for visual elements |
| Scanned/handwritten | ColQwen3 (visual only) |
| Slides, diagrams, engineering drawings | ColQwen3 |
| Production at scale (cost-sensitive) | Cohere Embed 4 multimodal (single-vector, cheaper) |

**Facilitator Notes:**
- Update from July: ColPali is no longer "emerging" — it's production-grade with OpenSearch integration.
- Demo idea: Show Ops-ColQwen3 retrieving from a complex PDF with tables and charts vs text-only retrieval.
- Time: 4 minutes
- ⚡ ADVANCED but increasingly mainstream

---

### [NEW AUG-2026] Slide 7: OpenAI's Responses API — RAG as a Built-in Tool

**Insert after:** "MCP as Retrieval Surface" section
**Source:** platform.openai.com/docs + openai.com/index/new-tools-and-features-in-the-responses-api/

**Content:**

OpenAI deprecated the Assistants API (shutting down August 26, 2026) and consolidated on the **Responses API** — which makes RAG a native, agentic capability:

**What changed:**
```
BEFORE (Assistants API, deprecated):
  Create assistant → Attach files → Create thread → Run → Poll for result
  (Multi-step, complex lifecycle management)

AFTER (Responses API):
  Single API call with tools: [file_search, web_search, code_interpreter, MCP servers]
  Model decides which tools to use, iterates within one request
  (Agentic by default)
```

**File Search in Responses API:**
- Semantic AND keyword search over uploaded files
- Model autonomously decides when to search
- Retrieves, evaluates, and can search again if needed
- Supports remote MCP servers alongside built-in tools

**The "agentic by default" principle:**
> *"With a single Responses API call, developers can solve increasingly complex tasks using multiple tools and model turns."* — OpenAI

**Implications for RAG architecture:**
1. Provider-managed RAG (OpenAI File Search, Bedrock KB, Gemini RAG Engine) is now the baseline for simple use cases
2. Custom RAG only justified when you need: custom chunking, specialized embeddings, permission control, or GraphRAG
3. The line between "RAG system" and "agent with retrieval tool" is now fully erased

**Facilitator Notes:**
- If students use OpenAI: emphasise the August 26 deadline for Assistants API migration
- Key message: "RAG is now a built-in model capability, not something you build from scratch — unless you have specific requirements that justify custom infrastructure"
- Time: 3 minutes

---

### [NEW AUG-2026] Slide 8: Jina Embeddings v5 and the Embedding Landscape Refresh

**Insert after:** "Hybrid Search 2026" section
**Source:** jina.ai/news/jina-embeddings-v5-text + arxiv.org/abs/2602.15547

**Content:**

The embedding landscape shifted significantly in early-mid 2026:

**Jina Embeddings v5 (February 2026):**
- **32K token context** (small model) / 8K (nano model)
- Late chunking natively supported
- Robust under truncation and binary quantization
- Task-targeted embedding distillation: sub-1B parameter models achieve 4B-quality
- Multilingual (100+ languages)

**Current embedding model landscape (August 2026):**
| Model | Params | Context | Multi-vector | Multimodal | Best For |
|---|---|---|---|---|---|
| jina-embeddings-v5 | <1B | 32K | No | No | Cost-effective text |
| jina-embeddings-v4 | 3.8B | 32K | Yes (late interaction) | Yes (text + image) | Unified multimodal |
| Cohere Embed v4 | Proprietary | 128K | No | Yes | Enterprise, easy API |
| text-embedding-3-large (OpenAI) | Proprietary | 8K | No | No | General purpose |
| Ops-ColQwen3-4B | 4B | Visual | Yes (patches) | Yes (visual docs) | Document image retrieval |
| Voyage AI multimodal-3 | Proprietary | 32K | No | Yes | Multimodal search |

**Key trend: Embedding models are splitting into two paradigms:**
1. **Single-vector** (traditional): One embedding per chunk. Fast, cheap, good for most use cases.
2. **Multi-vector / Late Interaction**: Multiple embeddings per document (patch-level for images, token-level for text). Higher quality, much higher storage cost.

**Production choice framework:**
- Budget-constrained, text-only → jina-embeddings-v5 nano
- Enterprise, easy integration → Cohere Embed v4
- Visual documents → Ops-ColQwen3-4B or jina-embeddings-v4
- Maximum quality, text → jina-embeddings-v5 small + reranker

**Facilitator Notes:**
- Update the July slide's recommendation: Jina v5 is now the cost-performance leader for text embedding
- The distillation approach (4B-quality from <1B params) is a major cost breakthrough
- Time: 3 minutes

---

### [NEW AUG-2026] Slide 9: The Agentic RAG Cost-Benefit Reality (August 2026 Data)

**Insert after:** "Agentic RAG" section (existing Slide 7)
**Source:** arxiv.org/abs/2601.07711 + lyzr.ai + marsdevs.com production data

**Content:**

The paper "Is Agentic RAG Worth It?" (January 2026, updated April) plus the BM25 scaling study (July 2026) give us hard numbers:

**When Agentic RAG is worth the cost:**

| Query Complexity | Agentic RAG Benefit | Cost Multiplier | Verdict |
|---|---|---|---|
| Simple factual (1 doc) | None to negative | 3-5× | ❌ Skip — use naive RAG or parametric |
| Multi-doc correlation | +15-25% accuracy | 4-8× | ⚠️ Maybe — depends on stakes |
| Multi-hop reasoning | +30-40% accuracy | 5-10× | ✅ Yes — can't solve otherwise |
| Cross-corpus synthesis | +20-34% accuracy | 6-12× | ✅ Yes — Google reports +34% |
| Small corpus (<10M tokens) | Agent wins | 39× tokens | ⚠️ Only if budget allows |
| Large corpus (>10M tokens) | BM25 + reranker wins | 1-2× | ❌ Use BM25 + reranker instead |

**The production stack emerging in August 2026:**
```
                    ┌── Simple queries (60-70% of traffic)
                    │   BM25 + reranker → Generate
Query Router ──────┤
                    │   Complex queries (20-30%)
                    ├── Dense hybrid + reranker → Generate
                    │
                    │   Multi-hop queries (5-10%)
                    └── Agentic RAG loop → Generate
```

**Key insight from production teams:**
> *"Route complexity appropriately. 70% of production queries don't need agentic RAG. The 5-10% that do absolutely cannot be solved without it."* — MarsDevs production data, 2026

**Facilitator Notes:**
- This replaces the "cost reality" table from July with harder numbers from the BM25 scaling study
- Key message: "Agentic RAG is justified only for the queries that literally cannot be answered any other way. For everything else, it's burning money."
- Connect to Adaptive RAG slide (Slide 10 from July): the router is the highest-ROI component
- Time: 4 minutes

---

### [NEW AUG-2026] Slide 10: Claude's 1M Token Window — Does RAG Still Matter?

**Insert after:** "The Future — Where RAG Is Heading" section
**Source:** anthropic.com/news/claude-opus-4-6 (February 2026) + Claude model release notes

**Content:**

Claude Opus 4.6 shipped with a **1M token context window** in February 2026 — the first Opus-class model with this capacity. Claude Sonnet 5 followed in June 2026. Combined with GPT-5.x's large context and Gemini's 2M+ tokens:

**The "stuff everything in context" temptation:**

1M tokens ≈ 750,000 words ≈ 3,000 pages of text

Can't we just... put everything in context and skip retrieval?

**Why RAG still matters (even with 1M+ token windows):**

| Factor | Long-Context Only | RAG |
|---|---|---|
| **Cost per query** | $2-15 per query (1M tokens in) | $0.01-0.10 per query |
| **Latency** | 15-60 seconds for 1M context | 1-5 seconds |
| **"Lost in the middle"** | Still happens — accuracy degrades for info in positions 30-70% | Focused context, no middle problem |
| **Freshness** | Entire corpus re-loaded per query | Index updated incrementally |
| **Permission control** | All or nothing | Document-level filtering |
| **Corpus size** | Capped at context window | Unlimited |
| **Quality at position** | Degrades with distance from edges | Consistent (top-K is all "top") |

**The hybrid emerging pattern:**
```
Small corpus (<500 pages): Stuff in context (cheaper per-query at low volume)
Medium corpus (500-5000 pages): RAG with reranking
Large corpus (>5000 pages): RAG mandatory (exceeds any context window)
Any corpus with access control: RAG mandatory (permission filtering)
```

**New research finding (2026):**
> Task-Aware Knowledge Compression (TAKC) offers a middle path: compress 5000 pages into 100 pages task-specifically, then stuff the compressed version into long context. Gets the "full corpus awareness" benefit without the cost.

**Facilitator Notes:**
- This updates the "Future" slide with concrete data from 2026 model releases
- Key message: "Long context doesn't kill RAG — it changes the threshold. RAG is now for large corpora and access-controlled scenarios, not for small document sets."
- Common question: "So when should I just stuff everything in?" — When corpus < 500 pages, no access control needed, and you can absorb the per-query cost.
- Time: 4 minutes

---

### [NEW AUG-2026] Slide 11: Bedrock AgentCore + Knowledge Bases — The Full Agentic RAG Stack on AWS

**Insert after:** AWS Bedrock Managed KB slide
**Source:** docs.aws.amazon.com + hidekazu-konishi.com (June 29, 2026)

**Content:**

The complete AWS Agentic RAG architecture as of August 2026 integrates AgentCore Runtime, Knowledge Bases, Rerank API, Guardrails, and Evaluations into a coherent loop:

```
┌─────────────────────────────────────────────────────────────────┐
│                    BEDROCK AGENTCORE RUNTIME                      │
│                                                                   │
│  ┌────────┐    ┌──────────┐    ┌──────────┐    ┌────────────┐   │
│  │  Plan  │───▶│ Retrieve │───▶│ Rerank   │───▶│   Grade    │   │
│  └────────┘    └──────────┘    └──────────┘    └────────────┘   │
│       ▲              │                               │           │
│       │              │                          ┌────┴─────┐     │
│       │              ▼                          │ Sufficient│     │
│       │     Knowledge Bases                     │   YES/NO  │     │
│       │     ├── Managed KB                      └────┬─────┘     │
│       │     ├── Self-managed KB                      │           │
│       │     └── MCP Connectors                  ┌────┴─────┐     │
│       │                                         │  NO → Re  │     │
│       └─────────────────────────────────────────┤  query    │     │
│                                                  └──────────┘     │
│                                                       │           │
│                                                  ┌────┴─────┐     │
│                                                  │ Generate  │     │
│                                                  │ + Cite    │     │
│                                                  └────┬─────┘     │
│                                                       │           │
│                                                  ┌────┴─────┐     │
│                                                  │ Guardrails│     │
│                                                  │ + Verify  │     │
│                                                  └──────────┘     │
└─────────────────────────────────────────────────────────────────┘
                              │
                    ┌─────────┴─────────┐
                    │  AgentCore        │
                    │  Observability    │
                    │  (traces, metrics)│
                    └───────────────────┘
```

**Key capabilities (June 2026):**
- **Multi-hop decomposition**: Complex queries broken into sub-queries automatically
- **Cross-KB retrieval**: Query spans multiple knowledge bases in one request
- **MCP native**: KBs exposed as MCP connector targets — standard tool interface
- **Built-in observability**: Retrieval traces, agentic traces, per-KB metrics
- **Three knowledge layers**: Organizational (your data), World (web), Paid (licensed)

**Facilitator Notes:**
- This is the AWS reference architecture for agentic RAG. Students building on AWS should understand this as the target state.
- Demo: Set up a simple AgentCore agent with a Knowledge Base and show the observability traces
- Time: 4 minutes

---

### [NEW AUG-2026] Slide 12: RAG Evaluation in Practice — 10 Common Mistakes (2026)

**Insert after:** "The 2026 RAG Evaluation Stack" (existing Slide 11)
**Source:** towardsdatascience.com (June 29, 2026) + premai.io (July 27, 2026)

**Content:**

Based on production RAG deployments through mid-2026, these are the 10 most common evaluation mistakes:

**The mistakes that kill production RAG:**

| # | Mistake | Why It's Deadly | Fix |
|---|---|---|---|
| 1 | No golden test set | Can't detect regressions | Build 50-200 curated Q&A pairs |
| 2 | Evaluating generation without retrieval | Wrong diagnosis (blaming LLM for retrieval failure) | Measure context_precision + faithfulness separately |
| 3 | Using BLEU/ROUGE for RAG | These measure text overlap, not factual accuracy | Use RAGAS faithfulness + answer_relevancy |
| 4 | One-time eval only | Quality drifts as data updates | Continuous monitoring + alerts |
| 5 | No latency tracking | p95 spikes kill UX | Track retrieval + generation latency separately |
| 6 | Ignoring cost per query | Agentic RAG can 10× your bill silently | Attribute cost per retrieval iteration |
| 7 | Testing on synthetic data only | Doesn't represent real user queries | Collect and test on actual user queries |
| 8 | High faithfulness + low relevancy | "Correctly answering the wrong question" | Add answer_relevancy as primary metric |
| 9 | No permission testing | ACL bypass in retrieval | Test with multiple user roles |
| 10 | Evaluating on fresh data only | Stale embedding problem hidden | Test with old docs that should still be findable |

**The minimum viable eval pipeline (2026):**
```python
# Three things you need before going to production:
1. Golden dataset: 100-500 examples with expected answers + source docs
2. Automated RAGAS metrics: faithfulness ≥0.9, context_precision ≥0.8
3. CI/CD gate: Block deployment if metrics regress >5%
```

**Facilitator Notes:**
- Make this actionable: "If you do nothing else, build the golden test set. Everything follows from that."
- Students can start with 50 Q&A pairs and grow to 500 over time
- Common question: "How do I know my golden set is good?" — Each item should have: question, expected answer, AND the specific source documents that contain the answer.
- Time: 4 minutes

---

### [NEW AUG-2026] Slide 13: The "Agentic Search" Challenge to RAG

**Insert after:** BM25 at Scale slide
**Source:** medium.com/@buzzgrewal (May 2026) + Amazon Science AAAI 2026

**Content:**

A provocative counter-narrative is gaining traction in mid-2026: **AI agents don't need vector search.**

**The argument:**
- Amazon Science paper at AAAI 2026: Agentic keyword search achieved **94.5% of RAG faithfulness** with zero vector store
- **Search-R1**: Trained retrieval policy with reinforcement learning, beat RAG by 24% relative
- Agents that learn *how* to search (via RL) outperform agents given pre-built retrieval pipelines

**The "agentic search stack" replacing traditional RAG (for some use cases):**
```
TRADITIONAL RAG:                    AGENTIC SEARCH:
Documents → Embed → Vector DB       Documents → Index (BM25/full-text)
Query → Embed → Vector search       Query → Agent decides search strategy
Top-K → Rerank → Generate           Agent searches → Evaluates → Searches more
                                     Agent generates from found docs
```

**Key differences:**
| Aspect | Traditional RAG | Agentic Search |
|---|---|---|
| Search strategy | Fixed (embed → nearest neighbor) | Learned/adaptive |
| Index required | Vector DB (expensive) | Full-text index (cheap) |
| Query formulation | One embedding | Multiple reformulations |
| When to stop | Fixed top-K | Learned sufficiency |

**The nuanced reality:**
> *"The vector database hasn't died. It's been demoted from the default to the fallback."*

**When traditional RAG still wins:**
- High-throughput, low-latency requirements
- Simple factual lookups
- Cost-sensitive at scale (agent iterations are expensive)

**When agentic search wins:**
- Complex, multi-step information needs
- Small-to-medium corpora where agent exploration is feasible
- Tasks where query reformulation is the key to finding the answer

**Facilitator Notes:**
- Present as an emerging counter-narrative, not a settled conclusion
- Key message: "The field is questioning whether vector search should be the default retriever. Watch this space."
- Connects to the BM25 scaling study: at large scale, even agents can't beat lexical search
- Time: 3 minutes
- ⚡ ADVANCED — provocative discussion prompt

---

### [NEW AUG-2026] Slide 14: Model Releases Impacting RAG (June-August 2026)

**Insert after:** "The RAG Landscape Has Shifted" section (existing Slide 1)
**Source:** Anthropic, OpenAI, AWS announcements

**Content:**

**Model releases that directly impact RAG architecture decisions (June-August 2026):**

| Model | Release | RAG Impact |
|---|---|---|
| **Claude Sonnet 5** | June 2026 | "Most agentic Sonnet" — better at multi-tool orchestration for agentic RAG |
| **Claude Opus 4.8** | July 2026 | Dynamic workflows, 2.5× fast mode — cheaper agentic RAG iterations |
| **GPT-5.6** | August 11, 2026 | "Ultra" setting coordinates multiple agents across parallel workstreams |
| **GPT-5.2** | June 2026 | Best at long contexts, understanding complex instructions |
| **OpenAI Agents SDK** | August 2026 | Replaces deprecated Agent Builder; new AgentKit framework |

**What "more agentic models" means for RAG:**
1. Models are better at deciding *when* to retrieve (fewer unnecessary retrievals)
2. Models can evaluate retrieval quality more accurately (better self-correction)
3. Models handle multi-tool orchestration natively (MCP + file_search + web_search in one call)
4. The "structured prompting approximation" of Self-RAG now works better (capturing ~90% of fine-tuned benefit)

**Platform shifts:**
- OpenAI Assistants API → Responses API (deadline: August 26, 2026)
- OpenAI Agent Builder → Deprecated (wind-down November 30, 2026)
- AWS Bedrock Agents Classic → AgentCore (closed to new customers July 30)
- Google Vertex AI → Gemini Enterprise Agent Platform (rename + major update)

**Facilitator Notes:**
- Keep this as a reference slide — update monthly as models change
- Key message: "The models themselves are getting better at RAG. The gap between naive and agentic RAG is narrowing because models are more capable at self-directed retrieval."
- Time: 3 minutes

---

### [NEW AUG-2026] Slide 15: Hands-On Lab Update — TAKC + BM25 Baseline Experiment

**Insert after:** Existing hands-on lab extension (Slide 19)
**Source:** AWS samples GitHub + arxiv scaling study

**Content:**

**New Lab Option: Compare RAG vs TAKC vs BM25 Baseline**
**Duration:** 25 minutes (or homework)
**Prerequisite:** Completed basic RAG pipeline lab

**Objective:** Empirically validate the August 2026 findings on your own test corpus.

**Setup:**
```python
# Three retrieval approaches on the same 50-question test set:

# Approach 1: BM25 baseline (the "boring" approach)
from rank_bm25 import BM25Okapi
bm25 = BM25Okapi(tokenized_corpus)
results_bm25 = bm25.get_top_n(query, corpus, n=5)

# Approach 2: Your existing RAG pipeline (hybrid search + reranker)
results_rag = rag_pipeline.retrieve(query, top_k=5)

# Approach 3: Agentic RAG (with query rewriting + iteration)
results_agentic = agentic_rag.retrieve(query, max_iterations=3)
```

**Measurement:**
```python
from ragas import evaluate
from ragas.metrics import context_precision, faithfulness, answer_relevancy

# Compare across all three approaches:
# - Accuracy (RAGAS faithfulness)
# - Context quality (context_precision)
# - Cost (total tokens used)
# - Latency (wall-clock time)
```

**Expected findings:**
- For simple factual questions: BM25 ≈ RAG >> Agentic (at much lower cost)
- For multi-hop questions: Agentic >> RAG > BM25
- Total cost: BM25 (1×) < RAG (1.5×) < Agentic (5-10×)

**Discussion prompt:** "Based on your results, which approach would you deploy for your use case, and at what query volume does the cost difference matter?"

**Facilitator Notes:**
- This lab validates the scaling study findings on a small corpus (students will see agents win on small data)
- The key learning: "Measure before you commit to an architecture. The simplest approach that meets your quality bar is the right one."
- Time for explanation: 3 minutes; lab execution: 25 minutes

---

## C) UPDATED CASE STUDIES

### Case Study 1: Google's Agentic RAG in Healthcare (June 2026)
**Source:** research.google/blog (June 5, 2026)

Google deployed their multi-agent RAG with Sufficient Context Agent for medical record retrieval. The system handles complex queries spanning pharmacy, nutrition, and clinical notes — decomposing a single doctor query into multiple sub-searches, evaluating sufficiency, and iterating until complete. Result: +34% accuracy over standard RAG on factuality benchmarks.

**Relevance to module:** Validates the CRAG/agentic RAG patterns taught in Slides 7-10. Shows the "Sufficient Context" evaluation step is the key differentiator in production.

### Case Study 2: AWS Task-Aware Knowledge Compression for PE Due Diligence (July 2026)
**Source:** AWS ML Blog (July 27, 2026)

A private equity firm analyzing $500M acquisitions across 200+ supplier contracts, 12 subsidiaries' financials, and 50+ legal cases. Standard RAG couldn't surface cross-document connections. TAKC pre-compressed the entire corpus into task-specific representations (financial analysis, legal risk, compliance). At 20× compression, outperformed RAG by 8 F1 points with 4× lower latency.

**Relevance to module:** Expands the "when RAG isn't enough" discussion. Shows a concrete production alternative for broad-knowledge tasks.

### Case Study 3: The BM25 Scaling Revelation (July 2026)
**Source:** arxiv.org/abs/2607.26497

A 28-tier controlled study varying corpus size from ~100K to 500K+ documents. The "File-System Agent" (agentic retrieval) won at small corpora but at 39× token cost. At 10M+ corpus tokens, BM25 overtook and led by 20 points at full scale. Dense retrieval was consistent but never the leader. GraphRAG hit construction limits before reaching deployment scale.

**Relevance to module:** Directly challenges the "always use dense + agentic" assumption. Validates the hybrid approach (BM25 + reranker) as the scalable default.

### Case Study 4: Enterprise Agentic RAG Adoption Reality (August 2026)
**Source:** TheStreet / Gartner (August 12, 2026)

Gartner's 2026 Hype Cycle for Agentic AI: Only 17% of organizations have deployed AI agents. Over 40% of agentic AI projects expected to be canceled by 2027 due to costs, unclear value, or inadequate risk controls. The infrastructure gap (fragmented data, legacy systems) is the primary barrier — not model capability.

**Relevance to module:** Reality check for students excited about agentic RAG. Emphasise that most enterprises are still at the "add a reranker" stage, not "deploy multi-agent RAG."

---

## D) UPDATED TOOLS & RESOURCES

### New Tools (June-August 2026)

| Tool | What's New | URL |
|---|---|---|
| **Amazon Bedrock Managed Knowledge Base** | GA June 17, 2026 — zero-ops RAG | aws.amazon.com/bedrock/knowledge-bases/ |
| **Amazon Bedrock AgentCore** | Replaces Bedrock Agents Classic — MCP native | docs.aws.amazon.com/bedrock-agentcore/ |
| **Ops-ColQwen3-4B** | Production-grade multimodal retrieval | huggingface.co/OpenSearch-AI/Ops-Colqwen3-4B |
| **Jina Embeddings v5** | 32K context, sub-1B params, late chunking native | jina.ai/models/ |
| **OpenAI Responses API (File Search)** | Replaces Assistants API — agentic by default | platform.openai.com/docs/guides/tools-file-search |
| **OpenAI Agents SDK (updated)** | Replaces Agent Builder — sandbox environments | openai.com/index/the-next-evolution-of-the-agents-sdk/ |
| **Google RAG Engine** | Part of Gemini Enterprise Agent Platform | docs.cloud.google.com/gemini-enterprise-agent-platform |
| **AWS TAKC sample** | Task-Aware Knowledge Compression reference impl | github.com/aws-samples/sample-bedrock-takc-compression |
| **Cohere Embed v4** | 128K context, multimodal (text + image) | cohere.com |

### Key Papers (June-August 2026)

| Paper | Finding | Link |
|---|---|---|
| "BM25 Wins at Scale" | BM25 beats dense & agents by ~20 pts at scale | arxiv.org/abs/2607.26497 |
| "CacheNotes: Task-Aware KV Cache Compression" | TAKC outperforms RAG by 8 F1 at 20× compression | EACL 2026 |
| Google Agentic RAG | Sufficient Context Agent yields +34% accuracy | research.google/blog (June 2026) |
| "Is Agentic RAG Worth It?" | Experimental comparison of RAG paradigms | arxiv.org/abs/2601.07711 |
| Jina Embeddings v5 | Task-targeted distillation, 4B→<1B quality | arxiv.org/abs/2602.15547 |

### Deprecated/Sunset (Action Required)

| Service | Deadline | Migration Path |
|---|---|---|
| OpenAI Assistants API | August 26, 2026 | Responses API |
| Amazon Kendra | July 30, 2026 (closed to new customers) | Bedrock Managed KB |
| Amazon Bedrock Agents Classic | July 30, 2026 | Bedrock AgentCore |
| Amazon Q Business | Maintenance mode | AgentCore + Knowledge Bases |
| OpenAI Agent Builder | November 30, 2026 | Agents SDK |

---

## E) FARIS HADDAD CONTENT INTEGRATION

**Search results:** No directly attributable LinkedIn posts, blog articles, or Medium posts by "Faris Haddad" were found in public search results specific to RAG or agentic AI topics for the June-August 2026 period.

**Recommendation:** If Faris has published content on LinkedIn or other platforms related to:
- Agentic RAG production experiences
- AWS Bedrock Knowledge Bases usage
- RAG evaluation practices
- Context engineering approaches

These could be integrated with framing like:
- *"As I discussed in my recent post on [topic], the key challenge we see in production is..."*
- *"Building on something I shared recently about [observation]..."*

**Course platform note:** The course is listed on elvtr.com (UK) as "AI Solutions Architecture" — this could be referenced for credibility context.

**Action item:** Check Faris's LinkedIn activity for June-August 2026 posts that could be woven into facilitator delivery. Particularly relevant sections: Agentic RAG patterns, AWS Bedrock updates, or RAG evaluation insights.

---

## F) FACILITATOR REFRESH BRIEF

### Top 3 Things That Changed Since July 2026

1. **BM25 scaling study upends the "always embed" assumption** (July 30, 2026)
   - At scale (>10M tokens), BM25 beats dense retrieval AND agents by ~20 points
   - Practical implication: Keep BM25 in your stack; spend agent tokens on reasoning, not retrieval
   - This is the single most important finding to update from July's module

2. **AWS consolidates on Bedrock — Kendra, Q Business, Agents Classic all deprecated** (June-July 2026)
   - Students on AWS need to know: Bedrock Managed KB is the future, everything else is sunsetting
   - AgentCore is the new orchestration layer with native MCP support
   - Three new knowledge layers: Organizational, World, Paid

3. **Task-Aware Knowledge Compression emerges as a "Beyond RAG" paradigm** (July 27, 2026)
   - For broad-knowledge tasks spanning hundreds of documents, TAKC outperforms RAG
   - AWS published an open-source reference implementation
   - This is the first serious alternative to "retrieve fragments" for complex analytical work

### What to Emphasise as 'Breaking News'

- 🔥 **"BM25 wins at scale"** — Counter-intuitive, backed by rigorous study. Present as a provocation: "Everything you just learned about dense retrieval? It's the right approach... for corpora under 10M tokens."
- 🔥 **"AWS killed Kendra"** — If anyone in the room uses Kendra, they need to migrate. Urgency is real.
- 🔥 **"TAKC: The post-RAG paradigm"** — For the advanced students: what comes after RAG for cross-document reasoning?
- 📢 **"OpenAI Assistants API shuts down August 26"** — If anyone built RAG on Assistants, they have days (not weeks) to migrate.

### Demos and Tools to Set Up Fresh

| Demo | What to Show | Setup Required |
|---|---|---|
| **Bedrock Managed KB** | End-to-end: upload docs → agentic retrieval → traced response | AWS account with Bedrock access; 15 min setup |
| **BM25 vs Dense vs Agentic comparison** | Same 20 questions, three approaches, measure quality + cost | rank_bm25 + existing RAG pipeline + LangGraph; 20 min |
| **TAKC on AWS** | Deploy the aws-samples reference, compress a doc set, query | Clone repo, configure Lambda/Bedrock; 30 min |
| **OpenAI Responses API with File Search** | Show the new "agentic by default" paradigm | OpenAI API key; 5 min |
| **RAGAS continuous eval** | Golden set → metrics → CI/CD gate that blocks regressions | pip install ragas; 10 min |
| **AgentCore observability traces** | Show retrieval traces for agentic RAG queries | Existing Bedrock setup with AgentCore; 15 min |

### Timing Adjustment for August Delivery

The July module had 20 slides. This addendum adds 15 more priority slides. Recommended integration:

**For 60-minute delivery (standard):**
- Add: BM25 at Scale (Slide 1), Bedrock Managed KB (Slide 2), Cost-Benefit Reality (Slide 9), Model Releases (Slide 14)
- Mention: TAKC, Google Sufficient Context, Deprecations as "further reading"
- Remove: Some of the more detailed July slides on Self-RAG internals

**For 90-minute delivery (extended, recommended):**
- Deliver all 15 new slides
- Group into three blocks: "What broke" (deprecations, BM25 finding), "What's new" (Bedrock, TAKC, Google), "What it means" (cost-benefit, architecture decisions)

**For 120-minute workshop:**
- Full delivery + hands-on lab comparing BM25 vs RAG vs Agentic on a test corpus

---

*Module 08 August 2026 Refresh — Prepared August 12, 2026*
*Next refresh due: September 2026*
