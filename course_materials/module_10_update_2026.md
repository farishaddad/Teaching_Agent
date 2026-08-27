# Module 10 Update — AI on AWS: The Bedrock-to-SageMaker Stack
## [NEW 2026] Additions & Facilitator Notes

---

## GAP ANALYSIS

Based on web research into AWS AI developments from 2025–2026, the following gaps exist in the original module:

1. **Amazon Bedrock AgentCore is missing entirely** — This is now the primary platform for building, deploying, and operating AI agents on AWS, replacing "Bedrock Agents" (now in maintenance mode as "Agents Classic"). AgentCore has 12 components: Runtime, Harness, Memory, Gateway, Identity, Code Interpreter, Browser, Observability, Payments, Evaluations, Policy, and Registry.

2. **Amazon Nova model family not covered** — Nova (Dec 2024) and Nova 2 (Dec 2025) are Amazon's first-party foundation models with extended thinking capabilities, multimodal input (text, image, video), and purpose-built variants (Nova Act for browser automation, Nova Canvas for image generation, Nova Reel for video).

3. **OpenAI models on Bedrock not mentioned** — As of June 2026, GPT-5.5, GPT-5.4, and Codex are available on Amazon Bedrock through an expanded OpenAI partnership. Bedrock now supports OpenAI-compatible APIs (Responses API and Chat Completions API).

4. **Strands Agents SDK missing** — AWS's open-source (Apache 2.0) agent SDK for Python and TypeScript, released May 2025, is the model-driven framework powering AgentCore's managed harness. It's the recommended starting point for building agents on AWS.

5. **Kiro IDE not covered** — AWS's next-generation AI IDE (replacing Q Developer IDE plugins by April 2027) uses spec-driven development where AI agents generate requirements, designs, and implementation plans before code.

6. **Nova Forge missing** — Amazon's "open training" service allowing enterprises to build custom model variants using Nova as a starting point.

7. **Trainium3 and AI silicon advances not covered** — Trainium3 (3nm, 2.52 PFLOPS/chip, 144GB HBM3e) launched at re:Invent 2025. UltraServers with 144 chips deliver 362 PFLOPS. Project Rainier: 500,000 Trainium2 chips training Anthropic's Claude.

8. **Bedrock Managed Knowledge Base missing** — A fully managed RAG service (GA June 2026) that eliminates the need to manage vector databases, data pipelines, or retrieval infrastructure separately.

9. **SageMaker rebranding not reflected** — SageMaker is now "Amazon SageMaker AI" (the ML platform) integrated within "Amazon SageMaker Unified Studio" (data + analytics + AI in one).

10. **Bedrock Guardrails multimodal support** — Now supports image content filtering (88% harmful multimodal content blocking), InvokeGuardrailChecks API for agentic applications, and integration with AgentCore.

---

## NEW SLIDES

---

### [NEW 2026] Slide 1: The 2025–2026 AWS AI Platform Shift
**Insert after:** Module title slide (Slide 1)
**Format:** Concept explanation / landscape overview

**Content:**

The AWS AI platform underwent a fundamental restructuring in 2025–2026. Understanding where things moved is critical before diving into individual services.

**Key shifts:**
- **Bedrock Agents → Bedrock AgentCore** (Agents Classic now in maintenance mode)
- **SageMaker → SageMaker AI** (ML platform) + **SageMaker Unified Studio** (data/analytics/AI combined)
- **CodeWhisperer → Q Developer → Kiro** (AI-assisted development evolution)
- **Nova family** became Amazon's first-party model line (competing with Claude, GPT on their own platform)
- **OpenAI models** arrived on Bedrock (GPT-5.5, GPT-5.4, Codex — June 2026)
- **Strands Agents SDK** — open-source agent framework powering AgentCore

**The mental model:**
```
┌──────────────────────────────────────────────────────────────┐
│  Amazon Bedrock = Model Access + Agent Orchestration + RAG    │
│  ├── Foundation Models (Nova, Claude, GPT, Llama, Gemma...)  │
│  ├── AgentCore (build, deploy, operate agents)               │
│  ├── Knowledge Bases (managed RAG)                           │
│  ├── Guardrails (safety and governance)                      │
│  └── Model Evaluation & Fine-tuning                          │
├──────────────────────────────────────────────────────────────┤
│  Amazon SageMaker AI = Custom Model Training + Hosting        │
│  ├── HyperPod (distributed training at scale)                │
│  ├── Pipelines, Experiments, Model Registry                  │
│  └── Inference endpoints                                     │
├──────────────────────────────────────────────────────────────┤
│  Developer Tools = Building WITH AI                           │
│  ├── Kiro (spec-driven AI IDE)                               │
│  ├── Q Developer (CLI + console assistant)                   │
│  └── Strands Agents SDK (open-source agent building)         │
├──────────────────────────────────────────────────────────────┤
│  AI Silicon = Custom Chips                                    │
│  ├── Trainium3 (training)                                    │
│  └── Inferentia2 (inference)                                 │
└──────────────────────────────────────────────────────────────┘
```

**Facilitator Notes:**
- 🎤 Open with: "If you learned AWS AI services 18 months ago, about 40% of what you learned has been reorganised or replaced. Let's reorient."
- Common student question: "Do I need to migrate from Bedrock Agents?" — Answer: Yes, eventually. Agents Classic is in maintenance mode. AgentCore is the future.
- For beginners: Focus on the mental model diagram. The key insight is that Bedrock is now both a model marketplace AND an agent platform.
- Time: 5 minutes
- Tip: Show this slide at the start and return to it at the end as a "now you know where everything fits" recap.

---

### [NEW 2026] Slide 2: Amazon Nova Model Family — First-Party Intelligence
**Insert after:** Foundation models overview section
**Format:** Comparison table

**Content:**

Amazon Nova is AWS's first-party model family, launched Dec 2024 (Gen 1) and expanded Dec 2025 (Gen 2). It sits alongside third-party models on Bedrock but offers the deepest AWS integration and cost advantages.

**Nova 2 Family (December 2025):**

| Model | Size | Modality | Extended Thinking | Key Use Case |
|-------|------|----------|-------------------|--------------|
| Nova 2 Premier | Largest | Text + Image + Video → Text | ✅ High/Med/Low | Complex reasoning, analysis, coding |
| Nova 2 Pro | Medium | Text + Image + Video → Text | ✅ High/Med/Low | Balanced workloads, RAG, agentic |
| Nova 2 Lite | Smallest | Text + Image + Video → Text | ✅ Low | Cost-efficient automation, document processing |
| Nova Canvas | — | Text → Image | — | Studio-quality image generation |
| Nova Reel | — | Text/Image → Video | — | Video generation |
| Nova Act | Custom | Browser UI automation | — | Reliable web workflow agents |

**Nova 2 differentiators:**
- **Extended thinking** with 3 intensity levels (low/medium/high) — developer controls the speed/intelligence/cost balance
- **128K–300K token context windows** with prompt caching (up to 20K tokens)
- **Multimodal native** — understands documents, charts, images, video in a single model call
- **Agentic-optimised** — designed for multi-turn tool calling and orchestration loops

**Facilitator Notes:**
- 🎤 "Nova is Amazon's answer to the question: should we build our own models or just host everyone else's? The answer is both."
- Common question: "How does Nova 2 compare to Claude 4 or GPT-5.5?" — Answer: Nova 2 Premier competes on reasoning; Nova 2 Lite wins on cost. The right choice depends on the task.
- For advanced students: Discuss extended thinking intensity as a knob between speed and accuracy — this is unique to Nova.
- Time: 5 minutes

---

### [NEW 2026] Slide 3: OpenAI on Bedrock — The Multi-Provider Reality
**Insert after:** Amazon Nova slide
**Format:** Concept explanation + practical implications

**Content:**

As of June 2026, Amazon Bedrock hosts models from OpenAI alongside Anthropic, Meta, Mistral, Cohere, Stability AI, Google (Gemma 4), and Amazon Nova. This makes Bedrock a true model marketplace.

**OpenAI models on Bedrock:**
- **GPT-5.5** — Most advanced frontier model (coding, research, long-running agentic tasks)
- **GPT-5.4** — Frontier reasoning, computer use, tool use, multi-step verification
- **Codex** — Code-specific model for development workflows
- **GPT OSS 20B** — Open-weight model available for fine-tuning

**OpenAI-Compatible APIs on Bedrock:**
```python
from openai import OpenAI

# Simply change the base URL — same SDK, same code
client = OpenAI(
    base_url="https://bedrock.us-east-1.amazonaws.com/openai/v1",
    api_key="your-bedrock-api-key"  # NOT your OpenAI API key
)

response = client.chat.completions.create(
    model="openai.gpt-5.5",
    messages=[{"role": "user", "content": "Explain quantum computing"}]
)
```

**What this means for architecture decisions:**
- You can migrate existing OpenAI code to Bedrock with a base URL change
- Bedrock's Responses API supports stateful conversations without manual history
- All Bedrock governance (Guardrails, logging, IAM) applies to OpenAI models
- Bedrock pricing model (on-demand, batch at 50% off, provisioned throughput) applies

**Facilitator Notes:**
- 🎤 "The 'which cloud for AI' question just got simpler — you can now use OpenAI models with AWS governance."
- Common question: "Why use Bedrock instead of OpenAI directly?" — Answer: IAM integration, VPC endpoints, Guardrails, unified billing, data residency, and the ability to switch models without code changes.
- Time: 4 minutes
- ⚡ ADVANCED: Discuss the Responses API and how it enables async inference for long-running agentic tasks.

---

### [NEW 2026] Slide 4: Bedrock AgentCore — The Agent Operating System
**Insert after:** Bedrock API section
**Format:** Concept explanation with architecture diagram

**Content:**

Amazon Bedrock AgentCore (launched fully in 2025, GA harness June 2026) is the platform for building, connecting, and operating AI agents. It replaces "Bedrock Agents" (now in maintenance mode as "Agents Classic").

**AgentCore philosophy:**
> "The loop was never the hard part. The hard part was everything around it." — AWS AgentCore launch blog

**AgentCore's 12 Components:**

| Component | What It Provides |
|-----------|-----------------|
| **Runtime** | Managed compute for agent sessions (isolated microVMs) |
| **Harness** | Managed orchestration loop (powered by Strands Agents) |
| **Memory** | Cross-session persistence and context management |
| **Gateway** | API management, authentication, rate limiting for agents |
| **Identity** | Agent-level IAM, credential passthrough, OAuth |
| **Code Interpreter** | Sandboxed code execution (Python, shell) |
| **Browser** | Web browsing capability via Nova Act integration |
| **Observability** | Traces, metrics, logs for agent sessions |
| **Payments** | Monetisation of agent capabilities |
| **Evaluations** | Automated quality assessment for agent responses |
| **Policy** | Guardrails integration, content filtering |
| **Registry** | Agent discovery and versioning |

**Two modes:**
1. **Managed Harness** — declare agent config (model, tools, instructions); AgentCore runs the loop
2. **Custom Runtime** — bring your own loop (any framework); AgentCore provides compute + infrastructure

```
AgentCore Harness (config-driven):
  Model: claude-sonnet-4  
  Tools: [knowledge_base, code_interpreter, web_search]
  Memory: enabled (cross-session)
  Guardrails: content-filter-v2
  → AgentCore handles the rest
```

**Facilitator Notes:**
- 🎤 "AgentCore is to AI agents what Lambda was to serverless functions — you define WHAT the agent does, AWS manages HOW it runs."
- Common question: "When should I use AgentCore Harness vs. Custom Runtime?" — Harness for fast iteration and standard patterns; Custom Runtime when you need full control (custom frameworks, complex orchestration).
- For beginners: Focus on the Harness mode — it's the fastest path from idea to deployed agent.
- For advanced: Discuss the Custom Runtime path and how it integrates with Strands Agents.
- Time: 7 minutes

---

### [NEW 2026] Slide 5: Strands Agents SDK — Open Source Agent Building
**Insert after:** AgentCore slide
**Format:** Code walkthrough + concept

**Content:**

Strands Agents is AWS's open-source (Apache 2.0) agent SDK for Python and TypeScript. Released May 2025, it powers AgentCore's managed harness internally and is the recommended framework for building agents on AWS.

**Core philosophy:** Model-driven — the LLM plans its own reasoning loop and tool use. You provide the model, the system prompt, and the tools. The agent loop is emergent.

**Three components:**
1. **Model** — any LLM (Bedrock, OpenAI-compatible, local)
2. **System Prompt** — natural language instructions
3. **Tools** — Python functions decorated with @tool

```python
from strands import Agent
from strands.tools import tool

@tool
def get_weather(city: str) -> str:
    """Get current weather for a city"""
    # Implementation here
    return f"Weather in {city}: 22°C, partly cloudy"

@tool  
def search_flights(origin: str, destination: str, date: str) -> str:
    """Search available flights"""
    return f"Found 3 flights from {origin} to {destination} on {date}"

# Create agent — that's it
agent = Agent(
    model="us.anthropic.claude-sonnet-4-20250514-v1:0",
    system_prompt="You are a travel assistant. Help users plan trips.",
    tools=[get_weather, search_flights]
)

# Run
response = agent("Plan a trip from London to Tokyo next week")
```

**Key features:**
- Works locally (laptop) and in production (AgentCore) with zero code changes
- Model-agnostic — switch models by changing one parameter
- Built-in observability (OpenTelemetry traces)
- Advanced orchestration: graph workflows, parallel agents, multi-agent coordination
- MCP server support for tool connections

**Facilitator Notes:**
- 🎤 "If you've used LangChain or CrewAI, Strands will feel simpler. It's intentionally minimal — just model + prompt + tools."
- Common question: "Why Strands vs. LangChain?" — Strands is lighter, model-driven (less scaffolding), and deeply integrated with AWS. LangChain gives more explicit workflow control.
- Demo opportunity: Show a live 5-line agent creation if time permits.
- Time: 6 minutes
- ⚡ ADVANCED: Show the graph workflow pattern and how to create supervisor/worker architectures.

---

### [NEW 2026] Slide 6: Nova Act — Browser Automation Agents
**Insert after:** Strands Agents slide
**Format:** Demo walkthrough + use case

**Content:**

Amazon Nova Act is purpose-built for reliable browser-based UI automation. Powered by a custom Nova 2 Lite model, it achieves **90% reliability** for production UI workflows (vs. ~40-50% for general-purpose LLMs on the same tasks).

**What Nova Act does:**
- Navigates websites, fills forms, clicks buttons, extracts data
- Executes repetitive UI workflows at enterprise scale
- Escalates to human supervisors when confidence is low
- Integrates as an AgentCore Browser capability

**Key differentiator:** Nova Act is NOT a general-purpose model doing browser tasks. It's a **specialist model trained specifically for UI understanding and interaction** — which is why reliability is dramatically higher.

```python
from nova_act import NovaAct

# Define a workflow
async with NovaAct(starting_page="https://travel-site.com") as agent:
    result = await agent.act(
        "Search for round-trip flights from London to Tokyo, "
        "departing next Monday, returning Friday. "
        "Select the cheapest economy option."
    )
    print(result.response)  # Structured result with flight details
```

**Production use cases:**
- Automated vendor onboarding (fill forms across multiple portals)
- Price monitoring and competitive intelligence
- Legacy system integration (UI-based data entry where no API exists)
- QA/testing automation for web applications
- Multi-agent collaboration: Nova Act handles browsers while orchestrator handles planning

**Facilitator Notes:**
- 🎤 "This solves a real production problem: 'the system we need to integrate with has no API, only a web interface.' Nova Act is the answer."
- Common question: "How is this different from Selenium/Playwright?" — Those are scripted; Nova Act is intelligent. It adapts to UI changes, handles dynamic content, and escalates when unsure.
- Time: 4 minutes
- Demo opportunity: If internet available, show a live Nova Act demo via the SDK preview.

---

### [NEW 2026] Slide 7: Bedrock Managed Knowledge Base — Fully Managed RAG
**Insert after:** Knowledge Bases section
**Format:** Comparison + architecture

**Content:**

Amazon Bedrock Managed Knowledge Base (GA June 2026) is a **fully managed RAG service** that eliminates the need to manage vector databases, embedding pipelines, or retrieval infrastructure.

**Before (Customer-Managed Knowledge Base):**
```
You manage: Data source → Chunking → Embedding → Vector DB → Retrieval → Reranking
AWS manages: API endpoint
```

**After (Bedrock Managed Knowledge Base):**
```
You manage: Connect data source
AWS manages: Everything else (ingestion, chunking, embedding, storage, retrieval, reranking)
```

**Comparison:**

| Feature | Bedrock Managed | Customer-Managed |
|---------|----------------|-----------------|
| Agentic retrieval | ✅ Supported | ❌ Not supported |
| Data store | Auto-scaling (managed) | You provision (OpenSearch, Pinecone, etc.) |
| Ingestion | Automatic | You configure |
| Embedding model | Auto-selected (or choose) | You configure |
| Reranking | Built-in | You add separately |
| Supported sources | S3, SharePoint, Confluence, Google Drive, OneDrive, Web Crawler | S3 + custom connectors |
| Cost model | Per-query + storage | Infrastructure + per-query |

**When to use Managed vs. Customer-Managed:**
- **Managed:** Standard RAG, quick setup, enterprise data sources, AgentCore integration
- **Customer-Managed:** Custom chunking logic, specific vector DB requirements, existing infrastructure, advanced hybrid search tuning

**Facilitator Notes:**
- 🎤 "This is the 'just make RAG work' option. For 80% of enterprise RAG use cases, you no longer need to think about vector databases."
- Common question: "What about chunking control?" — Managed KB handles this automatically. If you need custom chunking, use Customer-Managed.
- Connects to Module 8 (RAG): In that module we covered the pipeline in detail. Here we show how AWS abstracts most of it away.
- Time: 5 minutes

---

### [NEW 2026] Slide 8: Bedrock Guardrails — Multimodal & Agentic Safety
**Insert after:** Guardrails section
**Format:** Concept + practical application

**Content:**

Bedrock Guardrails expanded significantly in 2025–2026 with two major additions:

**1. Multimodal Content Filtering (GA March 2025)**
- Image content filters block up to **88% of harmful multimodal content**
- Filters: hate speech, insults, sexual content, violence, misconduct in BOTH text and images
- Configurable thresholds per content category
- Applied to inputs AND outputs

**2. InvokeGuardrailChecks API for Agentic Applications (June 2026)**
- Guardrails can now be called as a standalone API — not just within Bedrock inference
- This means ANY framework (Strands, LangChain, custom) can use Bedrock Guardrails
- Integrated directly with AgentCore for automatic safety checks

**3. AgentCore Integration**
- Guardrails are a first-class AgentCore component (Policy layer)
- Applied at three points: input to agent, output from agent, and per-tool-call
- Configuration-based — add guardrails with a single config field

```python
# Standalone guardrail check (any framework)
import boto3

bedrock_runtime = boto3.client("bedrock-runtime")

response = bedrock_runtime.invoke_guardrail_checks(
    guardrailIdentifier="my-guardrail-id",
    guardrailVersion="1",
    content=[{
        "text": {"text": user_input}
    }],
    source="INPUT"
)

if response["action"] == "BLOCKED":
    handle_blocked_content(response["outputs"])
```

**Facilitator Notes:**
- 🎤 "Guardrails used to be Bedrock-only. Now they work with any framework — this is how you add safety to your Strands agents, your LangChain apps, or anything else."
- Connects to Module 14 (AI Security): Guardrails are one layer of the defence-in-depth approach covered there.
- Time: 4 minutes

---

### [NEW 2026] Slide 9: AWS AI Silicon — Trainium3 and the Cost Advantage
**Insert after:** Deployment considerations section
**Format:** Concept + data points

**Content:**

AWS builds custom AI chips that power Bedrock's inference and enable customers to train/host models at significantly lower cost than NVIDIA GPUs.

**Trainium3 (launched re:Invent 2025):**
- Fabricated on **TSMC 3nm** process
- **2.52 PFLOPS** FP8 compute per chip
- **144 GB HBM3e** memory (1.5× Trainium2)
- **4.9 TB/s** memory bandwidth (1.7× Trainium2)

**Trainium3 UltraServers:**
- 144 Trainium3 chips per UltraServer
- **362 PFLOPS** per server
- **4.4×** more compute than Trainium2 UltraServers
- **4×** greater energy efficiency
- Customers reporting **50% cost reduction** vs. GPU alternatives

**Project Rainier:**
- **500,000 Trainium2 chips** in a single cluster
- Training Anthropic's Claude models
- World's largest non-NVIDIA AI cluster

**Roadmap announced:**
- **Trainium4** — will support NVIDIA NVLink Fusion for hybrid GPU/Trainium clusters

**Why this matters for the course:**
- Models served on Trainium/Inferentia cost less → lower inference costs on Bedrock
- Custom training on HyperPod with Trainium is significantly cheaper than GPU alternatives
- Not all models support all chips — architecture awareness helps with service selection

**Facilitator Notes:**
- 🎤 "You don't need to understand chip architecture. But you do need to know that AWS has its own silicon, and that's why some Bedrock models are cheaper than the same model on other clouds."
- Common question: "Do I need to know about this for my agent work?" — Not directly, but it affects pricing and availability. Nova models are optimised for Trainium, which is why they're cheaper.
- Time: 3 minutes
- SKIP FOR BEGINNERS who don't care about infrastructure.

---

### [NEW 2026] Slide 10: Kiro — Spec-Driven Development (The Post-Q-Developer Era)
**Insert after:** AWS AI services section
**Format:** Concept + workflow

**Content:**

AWS's AI development tooling has evolved rapidly:
- **CodeWhisperer** (2022) → **Q Developer** (2024) → **Kiro** (2026)

As of May 2026, Q Developer IDE plugins reach end-of-support April 2027. **Kiro is the future of AI-assisted development on AWS.**

**Kiro's core idea: Spec-Driven Development**

Traditional AI coding: "prompt → code → hope it works"
Kiro approach: "prompt → requirements spec → design doc → task plan → code → tests"

```
User Prompt: "Build a flight booking system"
     ↓
Kiro generates:
  1. Requirements document (scenarios, edge cases, success criteria)
  2. Technical design (architecture, data models, APIs)
  3. Implementation tasks (sequenced, with dependencies)
     ↓
Kiro implements with parallel agents
     ↓
Property-based tests catch edge cases
     ↓
Deployable, documented, maintainable code
```

**Key differentiators:**
- **Spec is the primary artifact** — code is a "build artifact" of the spec
- **Agent hooks** — automated actions triggered by code changes (run tests, update docs)
- **Parallel agents** — multiple coding agents work on separate tasks simultaneously
- **Context continuity** — project understanding persists across sessions

**For this course:** Kiro represents the emerging pattern of "AI that builds AI systems" — relevant to how students will actually construct the agentic applications covered in Modules 11–13.

**Facilitator Notes:**
- 🎤 "This is a preview of how you'll actually build the agents we cover in the next 3 modules. The tooling is moving from 'AI writes code' to 'AI architects systems'."
- Common question: "Should I learn Q Developer or Kiro?" — Kiro. Q Developer IDE is end-of-life 2027. Q Developer CLI/console agent role continues but the IDE experience is Kiro.
- Time: 4 minutes
- Demo opportunity: Show kiro.dev and the spec-driven workflow.

---

### [NEW 2026] Slide 11: Nova Forge — Custom Model Building
**Insert after:** Fine-tuning/customisation section
**Format:** Concept explanation

**Content:**

Amazon Nova Forge (announced re:Invent 2025) is an "open training" service that allows enterprises to build **custom model variants** using Nova as a starting point.

**What Nova Forge offers:**
- Start with any Nova model as a base
- Train on your proprietary data
- Customise model behaviour for your specific domain
- Full ownership of the resulting model weights
- Deploy on Bedrock or download for self-hosting

**Comparison with other customisation options:**

| Approach | What You Control | Data Needed | Compute Needed | Result |
|----------|-----------------|-------------|----------------|--------|
| Prompt engineering | Instructions only | Examples in prompt | None | Same base model |
| RAG | External knowledge | Documents | Embedding infra | Base model + retrieved context |
| Fine-tuning (LoRA) | Weight adjustments | 100s–1000s examples | Moderate | Adapted model |
| **Nova Forge** | Full model variant | Large proprietary corpus | Significant | Custom model |
| SageMaker training | Everything | Research-scale | Massive | Fully custom model |

**When to use Nova Forge vs. alternatives:**
- Use **Nova Forge** when: you have significant proprietary data, need a domain-specific model (legal, medical, financial), want model ownership, and don't want to manage training infrastructure
- Use **fine-tuning** when: you need lighter adaptation, smaller datasets, faster iteration
- Use **SageMaker HyperPod** when: you're training from scratch or using non-Nova architectures

**Facilitator Notes:**
- 🎤 "Nova Forge fills the gap between 'fine-tune someone else's model' and 'train your own from scratch.' It's AWS's answer to enterprise customers who want model ownership without PhD-level ML infrastructure."
- This connects to Module 9 (Fine-Tuning): Nova Forge is the 'heaviest' end of the customisation spectrum.
- Time: 3 minutes
- ⚡ ADVANCED: Discuss the economics of build vs. buy for foundation models.

---

### [NEW 2026] Slide 12: SageMaker AI + HyperPod — The Training Powerhouse
**Insert after:** SageMaker section
**Format:** Updated architecture overview

**Content:**

**Naming update (important):**
- **Amazon SageMaker AI** = the ML platform (training, hosting, pipelines) — formerly just "SageMaker"
- **Amazon SageMaker Unified Studio** = the combined data, analytics, and AI IDE
- SageMaker AI is integrated within Unified Studio but also available standalone

**SageMaker HyperPod (2025–2026 updates):**

Purpose-built infrastructure for training and fine-tuning at scale:
- Reduces training time by **up to 40%** through built-in resiliency
- Automatic node replacement on hardware failure (no manual intervention)
- Supports Trainium and NVIDIA GPU clusters
- Kubernetes-native (EKS integration) or Slurm-based orchestration
- **New: Troubleshooting skills for AI coding assistants** (June 2026) — HyperPod can diagnose its own training failures

**HyperPod Training Operator (Oct 2025):**
- Kubernetes-native interface for submitting training jobs
- Declarative training — define what you want, HyperPod manages how
- Automatic checkpointing and resume on failure

**When to use HyperPod:**
- Pre-training or continued pre-training of foundation models
- Fine-tuning at scale (thousands of examples, multi-GPU)
- Training with Trainium chips for cost efficiency
- Research workloads requiring custom training loops

**When NOT to use HyperPod:**
- Simple LoRA fine-tuning (use Bedrock fine-tuning instead)
- Inference-only workloads (use Bedrock or SageMaker endpoints)
- Small-scale experimentation (use SageMaker notebooks)

**Real result:** TGS (seismic analysis company) cut training time from **6 months to 5 days** using HyperPod for their Vision Transformer-based model.

**Facilitator Notes:**
- 🎤 "HyperPod is for when you're doing serious training — not a quick LoRA adaptation but real multi-GPU, multi-day jobs. Most students won't use it directly, but knowing it exists and when it's appropriate is key."
- Common question: "When do I use Bedrock fine-tuning vs. HyperPod?" — Bedrock: simple instruction tuning, small datasets, no infrastructure management. HyperPod: large-scale, custom training loops, Trainium cost savings.
- Time: 4 minutes
- ⚡ ADVANCED: Discuss the economics of Trainium vs. NVIDIA for training jobs.

---

### [NEW 2026] Slide 13: The AgentCore Harness — Configuration vs. Code
**Insert after:** AgentCore overview slide
**Format:** Code comparison + demo walkthrough

**Content:**

The AgentCore Managed Harness lets you create a production agent by **declaring what it does** rather than coding how it works.

**Harness = Managed orchestration loop:**
- Reasoning, tool selection, action execution, response streaming
- Each session gets its own **isolated microVM** with filesystem and shell
- **Model-agnostic** — switch models mid-session
- Powered by **Strands Agents** internally

**Configuration-driven agent definition:**
```json
{
  "harness": {
    "model": "us.anthropic.claude-sonnet-4-20250514-v1:0",
    "system_prompt": "You are a data analyst. Help users explore datasets.",
    "tools": ["code_interpreter", "knowledge_base:my-kb-id", "web_search"],
    "memory": { "enabled": true, "ttl_hours": 24 },
    "guardrails": "content-filter-enterprise-v2",
    "limits": { "max_turns": 50, "max_tokens_per_turn": 8192 }
  }
}
```

**What this gives you automatically:**
- ✅ Compute isolation (microVM per session)
- ✅ Filesystem access (agent can read/write files in its sandbox)
- ✅ Shell access (run commands, install packages)
- ✅ Memory (cross-session persistence)
- ✅ Identity (IAM integration, credential passthrough)
- ✅ Observability (traces, metrics, CloudWatch)
- ✅ Guardrails (content filtering on all inputs/outputs)
- ✅ Auto-scaling

**Harness vs. Runtime (custom):**
- Use **Harness** when: standard agent patterns work, you want fast iteration, you trust the managed loop
- Use **Runtime** when: you need custom orchestration (e.g., graph-based, multi-model routing), specific framework requirements, or the managed loop doesn't fit your use case

**Facilitator Notes:**
- 🎤 "This is the 'serverless for agents' moment. You define the what; AWS handles the how. Most students should start here."
- Demo: Show the AWS console AgentCore Harness creation flow if possible.
- Common question: "Can I see what the harness is doing?" — Yes, full traces in CloudWatch. AgentCore Observability gives you turn-by-turn visibility.
- Time: 5 minutes

---

### [NEW 2026] Slide 14: Bedrock Model Evaluation — Updated Capabilities
**Insert after:** Model Evaluation section
**Format:** Update + comparison

**Content:**

Bedrock Model Evaluation has expanded from simple benchmark comparison to a comprehensive evaluation platform:

**Current capabilities (2026):**
- **Automatic evaluation** — built-in metrics (accuracy, robustness, toxicity, latency)
- **Human evaluation** — managed workforce for subjective quality assessment
- **LLM-as-judge** — use a stronger model to evaluate a weaker model's outputs
- **Custom metrics** — define your own evaluation criteria
- **AgentCore Evaluations** — evaluate entire agent workflows, not just single model calls

**AgentCore Evaluations (new):**
- Turn production traces into evaluation datasets automatically
- Compare agent versions A vs. B on real user interactions
- Track regression across deployments
- Measure: task completion rate, tool call accuracy, hallucination incidents, cost per session

**What changed from the original module content:**
- Evaluation is no longer just "before deployment" — it's continuous in production
- The unit of evaluation shifted from "model response" to "agent session"
- AgentCore's optimization capabilities turn traces into continuous improvement signals

**Facilitator Notes:**
- 🎤 "Evaluation has moved from 'did the model get the right answer?' to 'did the agent complete the task correctly, safely, and cost-effectively?' That's a much harder question."
- Connects to Module 15 (Observability): The evaluation pipeline feeds the monitoring pipeline.
- Time: 3 minutes

---

### [NEW 2026] Slide 15: Updated Service Selection Decision Tree
**Insert after:** Choosing the right service section
**Format:** Decision framework / flowchart

**Content:**

The original module's service selection content needs updating. Here's the 2026 decision tree:

```
START: What do you need to do?
│
├── "I need to BUILD an AI agent"
│   └── Amazon Bedrock AgentCore
│       ├── Fast path → Managed Harness (config-driven)
│       └── Custom path → Runtime + Strands Agents SDK
│
├── "I need a model to call via API"
│   └── Amazon Bedrock (model access)
│       ├── Cost priority → Nova 2 Lite / Nova 2 Pro
│       ├── Best reasoning → Claude 4 / GPT-5.5
│       ├── Open weights → Llama, Gemma, Mistral
│       └── Image/Video → Nova Canvas / Nova Reel
│
├── "I need RAG (grounding in my data)"
│   ├── Quick setup → Bedrock Managed Knowledge Base
│   └── Custom control → Customer-Managed Knowledge Base
│
├── "I need to TRAIN or FINE-TUNE a model"
│   ├── Light adaptation → Bedrock Fine-Tuning (LoRA)
│   ├── Heavy customisation → Nova Forge
│   └── Full custom training → SageMaker AI + HyperPod
│
├── "I need browser automation"
│   └── Amazon Nova Act
│
├── "I need AI-assisted development"
│   └── Kiro (spec-driven IDE)
│
├── "I need to process documents/images/speech"
│   └── AWS AI Services (Textract, Rekognition, Transcribe, Comprehend)
│
└── "I need guardrails and safety"
    └── Bedrock Guardrails (works with any framework via InvokeGuardrailChecks API)
```

**Key insight:** The "right service" question has gotten simpler in some ways (AgentCore consolidates agent building) but more complex in others (model choice explosion).

**Facilitator Notes:**
- 🎤 "This tree is your cheat sheet. Print it. The students will reference it constantly after the course."
- Consider providing this as a handout/PDF.
- Time: 5 minutes
- Discussion prompt: "Given a real project you're working on, where would you start on this tree?"

---

### [NEW 2026] Slide 16: Reference Architecture — Production Agent on AWS
**Insert after:** Reference architectures section
**Format:** Architecture diagram + explanation

**Content:**

A modern production agent architecture on AWS (2026):

```
┌─────────────────────────────────────────────────────────────┐
│                        CLIENT LAYER                          │
│  Web App  |  Mobile App  |  Slack Bot  |  CLI  |  API       │
└─────────────────────┬───────────────────────────────────────┘
                      │ HTTPS / WebSocket
┌─────────────────────▼───────────────────────────────────────┐
│                 AgentCore GATEWAY                             │
│  Auth (Cognito/IAM) | Rate Limiting | API Management         │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│                 AgentCore HARNESS                             │
│  Orchestration Loop | Model Selection | Tool Dispatch        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                  │
│  │  Memory  │  │  Policy  │  │ Guardrails│                  │
│  └──────────┘  └──────────┘  └──────────┘                  │
└───────┬──────────────┬──────────────┬───────────────────────┘
        │              │              │
┌───────▼──────┐ ┌─────▼─────┐ ┌─────▼─────┐
│   TOOLS      │ │  KNOWLEDGE │ │  BROWSER  │
│ Code Interp. │ │  Managed   │ │  Nova Act │
│ Custom APIs  │ │  KB (RAG)  │ │           │
│ MCP Servers  │ │            │ │           │
└──────────────┘ └────────────┘ └───────────┘
        │
┌───────▼─────────────────────────────────────────────────────┐
│              OBSERVABILITY & EVALUATION                       │
│  CloudWatch | X-Ray Traces | AgentCore Metrics | Evals       │
└─────────────────────────────────────────────────────────────┘
```

**Key architectural decisions:**
1. **Agent per user session** (not shared) — microVM isolation
2. **Memory across sessions** — user context persists
3. **Guardrails at gateway AND per-tool** — defence in depth
4. **Managed Knowledge Base** for enterprise data grounding
5. **Nova Act** for tasks requiring web interaction
6. **Observability from day one** — never deploy an agent without traces

**Facilitator Notes:**
- 🎤 "This is the architecture you'd whiteboard for a solutions architect review. Every component maps to a managed AWS service."
- Common question: "What about cost?" — Provide rough estimate: microVM compute + model tokens + KB queries + storage. AgentCore pricing is per-session-second + per-model-token.
- Time: 5 minutes
- ⚡ ADVANCED: Discuss multi-agent architectures where multiple AgentCore agents collaborate via A2A protocol.

---

### [NEW 2026] Slide 17: Web Search on AgentCore — Grounding in Real-Time Information
**Insert after:** Managed Knowledge Base slide
**Format:** Feature overview

**Content:**

Web Search on Amazon Bedrock AgentCore (announced June 2026) adds real-time web knowledge as a built-in agent capability.

**What it does:**
- Agents can search the live web during their reasoning loop
- Results are automatically cited in agent responses
- No separate search API integration needed — it's a built-in tool

**Use cases:**
- Agents answering questions about current events
- Research agents that need real-time information
- Customer support agents that check product availability/pricing
- Competitive intelligence agents

**Comparison with Knowledge Base:**
| Source | Best For | Freshness | Control |
|--------|----------|-----------|---------|
| Managed Knowledge Base | Enterprise proprietary data | As fresh as sync schedule | Full (your data) |
| Web Search | Public internet information | Real-time | Limited (web results) |
| Both together | Complete grounding | Best of both | Enterprise data + web |

**Configuration (within harness):**
```json
{
  "tools": ["web_search", "knowledge_base:my-kb-id"]
}
```
The agent decides when to use web search vs. knowledge base based on the query.

**Facilitator Notes:**
- 🎤 "This solves the 'my agent is stuck in a knowledge cutoff' problem. Now agents can check the live web when their training data or knowledge base doesn't have the answer."
- Time: 3 minutes

---

### [NEW 2026] Slide 18: AWS AI Productivity Data Points — The Business Case
**Insert after:** Course outcomes / wrap-up area
**Format:** Data points for executives / case study

**Content:**

From AWS internal and customer deployments (2025–2026):

**AWS internal results:**
- A **6-engineer team** rebuilt the Amazon Bedrock inference engine in 76 days — a project originally scoped for **30 developers over 12–18 months** (using AI-assisted development)
- Median productivity gain across Amazon Stores pilots: **4.5× normalized deployment velocity**
- Some teams exceeded **10× productivity gains**
- 79% of Amazon development teams using generative AI tools as of early 2026

**Customer results on AWS AI platform:**
- **TGS (seismic analysis):** Training time reduced from 6 months to 5 days using HyperPod
- **Nova Act early customers:** 90% workflow reliability for browser automation
- **Trainium customers:** 50% cost reduction vs. GPU alternatives for training
- **AgentCore early adopters:** Time from idea to production agent reduced from weeks to hours

**What these numbers mean for students:**
- AI-assisted development is not theoretical — it's production-proven at Amazon scale
- The "build vs. buy" calculus is shifting rapidly — managed services are winning
- Cost advantages of AWS-native silicon are significant and growing

**Facilitator Notes:**
- 🎤 "These aren't projections — they're actuals from production deployments. The 4.5× productivity number is median, not cherry-picked."
- Use these data points to motivate the "why learn this now" argument for students who are on the fence.
- Time: 3 minutes
- Useful for: closing the module with business justification for the entire course

---

### [NEW 2026] Slide 19: Hands-On Lab (Updated) — Build an Agent with AgentCore
**Insert after:** Existing hands-on activity
**Format:** Activity instructions

**Content:**

**Updated Lab: Build a Research Agent on AgentCore**

**Objective:** Create a working agent that uses multiple tools (Knowledge Base + Web Search + Code Interpreter) to answer research questions.

**Prerequisites:**
- AWS account with Bedrock access
- AgentCore enabled
- A sample knowledge base (pre-provisioned or created in class)

**Instructions:**

**Step 1: Create a Managed Knowledge Base (5 min)**
- Go to Bedrock Console → AgentCore → Built-in Tools → Knowledge Base
- Connect an S3 bucket with sample documents (provided)
- Wait for sync to complete

**Step 2: Create an AgentCore Harness Agent (5 min)**
- Go to AgentCore → Create Agent → Managed Harness
- Configure:
  - Model: Claude Sonnet 4
  - Tools: knowledge_base, web_search, code_interpreter
  - System prompt: "You are a research analyst. Use your knowledge base for internal data, web search for current information, and code interpreter for calculations and charts."

**Step 3: Test the Agent (5 min)**
- Ask: "What does our internal data say about Q1 revenue, and how does that compare to the latest industry benchmarks from the web?"
- Observe: The agent uses KB for internal data, web search for benchmarks, and code interpreter to create a comparison chart

**Step 4: Add Guardrails (3 min)**
- Create a guardrail blocking PII in outputs
- Test with a query that would expose employee names

**Step 5: Review Traces (2 min)**
- Open AgentCore Observability → Session traces
- Walk through the reasoning steps, tool calls, and model interactions

**Expected Outcome:** A working multi-tool agent with safety controls and full observability, deployed in under 20 minutes.

**Facilitator Notes:**
- 🎤 "This replaces the original lab which focused on individual service calls. The modern approach is agent-first."
- Tip: Have the S3 bucket with sample docs pre-provisioned to save time.
- Fallback: If console access is limited, demo live and have students follow along.
- Time: 20 minutes (if included as the module's primary lab)

---

### [NEW 2026] Slide 20: AWS AI Services — What's Still Relevant, What's Absorbed
**Insert after:** AWS AI services section
**Format:** Update table

**Content:**

The original module covered Rekognition, Textract, Transcribe, and Comprehend as standalone services. Here's the 2026 reality:

**Still standalone and relevant:**
| Service | Status | When to Use |
|---------|--------|-------------|
| **Textract** | Active, enhanced with Generative AI queries | Document extraction at scale, form processing |
| **Transcribe** | Active, enhanced with speech-to-speech in Bedrock | Meeting transcription, call centre analytics |
| **Rekognition** | Active | Face detection, image moderation, object detection |
| **Comprehend** | Active | NLP at scale (sentiment, entities, PII detection) |

**What changed:**
- These services are increasingly **wrapped by agents** rather than called directly
- Bedrock Guardrails now handles much of what Comprehend was used for (PII detection, content moderation)
- AgentCore's Code Interpreter can call any of these via SDK within an agent session
- Nova 2 models understand documents/images natively — reducing the need for separate Textract/Rekognition calls for many use cases

**New pattern: Agent as orchestrator of AI services**
```
User: "Summarise the key findings from this 50-page PDF"
     ↓
Agent (AgentCore):
  1. Uses Textract to extract text + tables
  2. Uses Nova 2 Pro to summarise
  3. Uses Code Interpreter to create charts
  4. Returns structured summary with visualisations
```

**Facilitator Notes:**
- 🎤 "These services aren't dead — they're becoming agent tools rather than standalone APIs. The pattern is shifting from 'call Textract directly' to 'give the agent access to Textract and let it decide when to use it.'"
- Time: 3 minutes

---

## FACILITATOR UPDATE BRIEF

### 🎤 Top 3 Most Important Additions

1. **Amazon Bedrock AgentCore** (Slides 4, 5, 13, 16) — This is the single biggest change. AgentCore is now THE platform for building agents on AWS. Any student leaving this module without understanding AgentCore's 12 components and the Managed Harness concept will be immediately outdated. This should consume ~15 minutes of class time.

2. **Amazon Nova model family + OpenAI on Bedrock** (Slides 2, 3) — The model marketplace has exploded. Students need to understand the multi-provider reality (Nova, Claude, GPT, Llama, Gemma all on one platform) and how to make selection decisions. ~8 minutes.

3. **Strands Agents SDK + Kiro** (Slides 5, 10) — These are the developer tools students will actually use. Strands is how you build agents; Kiro is how you build software with AI assistance. Both represent the "how" of putting this module into practice. ~10 minutes.

### ⚠️ What in the Original is Now Outdated

| Original Content | Status | How to Address |
|---|---|---|
| "Bedrock Agents" as the agent platform | **Replaced** by AgentCore (Agents Classic in maintenance mode) | Mention Agents Classic exists but teach AgentCore |
| SageMaker as just "training and hosting" | **Expanded** — now SageMaker AI within Unified Studio | Update naming; mention the unified data+AI platform vision |
| Limited model selection (Claude, Llama) | **Massively expanded** — Nova, GPT-5.x, Gemma 4, dozens more | Show the full marketplace; teach selection criteria |
| Knowledge Bases as BYO-vector-DB | **Supplemented** by Managed Knowledge Base | Show both options; recommend Managed for most use cases |
| No agent developer tools covered | **New category** — Strands, Kiro, Q Developer | Add developer tooling as a track |
| Guardrails as text-only | **Expanded** — multimodal + standalone API | Update to show multimodal and framework-agnostic use |

### ⏱️ Fitting New Content in 60 Minutes

**Honest assessment:** The original module content + all 20 new slides = ~90–100 minutes. For a 60-minute delivery:

**Recommended 60-min schedule:**
| Time | Content | Slides |
|------|---------|--------|
| 0–5 min | Platform shift overview (the map) | NEW Slide 1 |
| 5–15 min | Bedrock models: Nova + OpenAI + selection | NEW Slides 2, 3 |
| 15–30 min | AgentCore deep-dive (harness, config, architecture) | NEW Slides 4, 5, 13 |
| 30–37 min | Knowledge Base (managed vs custom) + Guardrails | NEW Slides 7, 8 |
| 37–42 min | SageMaker AI + HyperPod + Silicon overview | NEW Slides 12, 9 |
| 42–47 min | Developer tools (Strands, Kiro) | NEW Slides 5, 10 |
| 47–50 min | Service selection decision tree | NEW Slide 15 |
| 50–55 min | Reference architecture walkthrough | NEW Slide 16 |
| 55–60 min | Wrap-up + Q&A |  |

**For 90-min extended version:** Add the hands-on lab (Slide 19, 20 min), Nova Act demo (Slide 6, 5 min), and business case data points (Slide 18, 5 min).

### 🛠️ New Tools/Accounts/Demos to Set Up

1. **AWS account with AgentCore access** — ensure Bedrock AgentCore is enabled in the target region
2. **Pre-provisioned S3 bucket** with sample documents for the Knowledge Base lab
3. **Strands Agents SDK** installed locally for live coding demo: `pip install strands-agents`
4. **Kiro account** (free tier available at kiro.dev) for spec-driven development demo
5. **Bedrock model access** — ensure Claude Sonnet 4, Nova 2 Pro, and at least one OpenAI model are enabled in the account
6. **AgentCore Harness** — have a pre-built agent ready as fallback if live creation fails during demo

---

*Module 10 Update — AI on AWS: The Bedrock-to-SageMaker Stack*  
*Updated: July 2026*  
*Research sources: AWS official announcements, re:Invent 2025, AWS Summit NYC 2026, AWS documentation*
