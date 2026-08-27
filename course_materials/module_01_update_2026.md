# Module 01 Update — [NEW 2026]
## The AI Moment: Understanding Where We Are
### Track: Foundation | Updated: July 2026

---

## GAP ANALYSIS

The original Module 01 was built around the generative AI paradigm shift and the landscape as of early 2025. Here's what's now outdated or missing:

1. **Reasoning models are an entirely new paradigm not covered** — OpenAI o3/o4-mini, Claude 3.7 Sonnet extended thinking, Gemini 2.5 Pro with Deep Think. These represent a shift from "next token prediction" to "deliberate multi-step reasoning" (Large Reasoning Models / LRMs).

2. **The model landscape has exploded** — In early 2025, there were ~5 major model families. By mid-2026 there are 10+: GPT-5.5, Claude Opus 4.7/Sonnet 5, Gemini 3.1 Pro, DeepSeek V4, Llama 4, Qwen 3.5, Mistral Medium 3.5, Amazon Nova 2, Kimi K2.6, GLM-5. Students need an updated mental map.

3. **Open-weight models have closed the gap** — DeepSeek V4 Pro ties the closed frontier on SWE-Bench. The "open vs closed" dichotomy is now a spectrum with real production implications.

4. **"Context engineering" has replaced "prompt engineering" in practitioner discourse** — Coined by Andrej Karpathy and Tobi Lütke in mid-2025, now endorsed by Gartner. This shifts the framing from "how to write good prompts" to "how to design the information system around the model."

5. **Agentic AI is no longer theoretical** — 31% of enterprises have at least one agent in production (S&P Global/McKinsey). Gartner: 40% of enterprise apps will embed AI agents by end of 2026, up from <5% in 2025. This is the defining trend of this era.

6. **The AI Performance Paradox needs coverage** — McKinsey (April 2026): 89% of companies deployed AI, but 94% report NOT seeing "significant" value. Only ~6% are AI high performers. The gap is not a model problem — it's a value realisation problem. This directly motivates why this course exists.

7. **Enterprise adoption data is dramatically higher** — Overall US AI adoption: 50.6% (April 2026). 78% of orgs use AI in at least one function. Global AI spending: $407B in 2026 (+35% YoY). GenAI investment surged from $1.7B to $37B in two years.

8. **AI coding agents are now a $10B market** — Gartner predicts 65% of engineering teams will treat IDEs as optional by 2027. This changes how students should think about AI's role in software development.

9. **Multimodal has gone beyond text+image** — o3/o4-mini "think with images" (crop, zoom, rotate in chain-of-thought). Video understanding, audio processing, and tool-using multimodality are production-ready.

10. **The original "myths vs realities" section needs updating** — New myths: "AI will replace all developers," "bigger models are always better," "open-source can't compete with closed." New realities: the harness matters more than the model, most AI value goes uncaptured, test-time compute beats training compute for many tasks.

---

## NEW SLIDES

---

### [NEW 2026] Slide: The AI Performance Paradox
**Insert after:** "The generational shift from rule-based to generative AI" section
**Format:** Concept explanation with data visualisation

**Content:**

The single most important finding in enterprise AI for 2026:

| Metric | Value | Source |
|--------|-------|--------|
| Companies that have deployed AI | 89% | McKinsey, April 2026 |
| Companies reporting "significant" value | 6% | McKinsey, April 2026 |
| Global AI spending 2026 | $407 billion | IDC |
| YoY spending growth | +35% | IDC |

**The Paradox:** Almost everyone is deploying. Almost no one is capturing value. The gap is not about better models — high performers and laggards use the same models. The gap is about:
- Architecture (how you build around the model)
- Integration (how deeply AI is embedded in workflows)
- Measurement (whether you even know what "value" looks like)
- People (whether your teams can build and operate AI systems)

> *"They don't have a model problem. They have a value problem."* — McKinsey analysis, 2026

**Why this matters for THIS course:** This course exists in the gap. It teaches what separates the 6% from the 94%.

**Facilitator Notes:**
- 🎤 Open with: "Here's the dirty secret of enterprise AI in 2026..." — this statistic lands hard with experienced professionals
- Common student question: "Then why is everyone spending so much?" Answer: because the 6% who get it right see 5%+ EBIT impact — that's transformative
- For advanced students: connect to the AI-DLC (Module 6) — the gap is in operationalisation, not experimentation
- Time: 5 minutes
- This slide sets up the ENTIRE course rationale — spend time here

---

### [NEW 2026] Slide: The 2026 Model Landscape — A New Map
**Insert after:** "AI landscape map: models, platforms, tools, players"
**Format:** Comparison table / visual map

**Content:**

The model landscape has exploded from ~5 major families in early 2025 to 10+ in mid-2026:

**Closed Frontier (API-only):**
| Model Family | Provider | Key Strength |
|---|---|---|
| GPT-5.5 | OpenAI | General-purpose + reasoning |
| Claude Opus 4.7 / Sonnet 5 | Anthropic | Extended thinking, coding, safety |
| Gemini 3.1 Pro | Google | Multimodal, large context (2M tokens) |
| Grok 4.3 | xAI | Speed, uncensored |

**Open-Weight Frontier (self-hostable):**
| Model Family | Provider | Key Strength |
|---|---|---|
| DeepSeek V4 Pro/Flash | DeepSeek | Agentic coding, MoE efficiency |
| Llama 4 | Meta | General-purpose, permissive license |
| Qwen 3.5 / Qwen3-Coder | Alibaba | Code + multilingual |
| Mistral Medium 3.5 | Mistral AI | European, efficiency |
| Kimi K2.6 | Moonshot | Top neutral benchmark score |
| GLM-5.1 | Zhipu AI | MIT license, open |
| Amazon Nova 2 | AWS | Bedrock-native, cost-optimised |

**Key insight:** The quality gap between open and closed is now small enough that many use cases don't justify paying for closed models. DeepSeek V4 Pro ties closed frontier on SWE-Bench.

**Facilitator Notes:**
- 🎤 Say: "If you last looked at this landscape in 2024, you wouldn't recognise it. The number of competitive model families has tripled."
- Common question: "Which one should we use?" Answer: it depends on use case, but the answer is increasingly "multiple" — model routing is a production pattern now
- For beginners: focus on closed vs. open distinction and 3 big providers
- For advanced: discuss MoE architectures, model routing, cost/quality tradeoffs
- Time: 5 minutes

---

### [NEW 2026] Slide: Reasoning Models — The Second Paradigm Shift
**Insert after:** "Key milestones: LLMs, foundation models, multimodality"
**Format:** Concept explanation

**Content:**

**2022-2024: The Generative Shift** — Models that predict the next token  
**2025-2026: The Reasoning Shift** — Models that think before they answer

**What is a reasoning model?**
A Large Reasoning Model (LRM) inserts a deliberation phase before responding. It generates internal "thinking tokens" — planning, evaluating approaches, backtracking on dead ends — then produces a final answer.

**The key concept: Test-Time Compute**
Instead of making models smarter only through more training, reasoning models spend more compute at inference time. The model "thinks harder" when the problem is hard.

**Benchmarks that demonstrate the shift:**
- OpenAI o3 scored ~87.5% on ARC-AGI (3× its predecessor o1)
- Gemini Deep Think solved 5/6 International Mathematical Olympiad problems (July 2025) — first AI gold medal under standard conditions
- Andrew Ng's demo: GPT-3.5 in an iterative reasoning loop beat single-shot GPT-4 on HumanEval (95% vs 67%)

**Key insight for practitioners:**
> *"Stop polishing one perfect sentence and start designing the system the model works inside."* — Forbes on context engineering, June 2026

**Facilitator Notes:**
- 🎤 Say: "If generative AI was 'a machine that can write', reasoning AI is 'a machine that can think'. That's not hyperbole — it's what the benchmarks show."
- Common student question: "Is this real intelligence?" — Redirect: "The question that matters is: does it solve the problems you need solved?" Philosophically interesting, practically irrelevant.
- For beginners: use the analogy — "standard LLM = first-draft writer, reasoning model = writer who outlines, drafts, revises, then publishes"
- For advanced: discuss test-time compute scaling laws, the relationship between inference cost and quality
- Time: 5 minutes

---

### [NEW 2026] Slide: From Prompt Engineering to Context Engineering
**Insert after:** "Reasoning Models" slide
**Format:** Concept explanation with hierarchy diagram

**Content:**

**The terminology shift of 2025-2026:**

In mid-2025, Shopify CEO Tobi Lütke and former OpenAI researcher Andrej Karpathy both argued publicly that "prompt engineering" undersells the real work of building AI systems. The term **context engineering** caught fire.

```
┌─────────────────────────────────────────────┐
│         CONTEXT ENGINEERING                 │
│  Designing the entire information system    │
│  around the model: data, tools, memory,     │
│  retrieval, verification, orchestration     │
│  ┌─────────────────────────────────────┐    │
│  │     PROMPT ENGINEERING              │    │
│  │  Crafting the instructions          │    │
│  │  the model receives                 │    │
│  └─────────────────────────────────────┘    │
└─────────────────────────────────────────────┘
```

**The distinction:**
| Prompt Engineering | Context Engineering |
|---|---|
| How to word a single instruction | What information the model needs access to |
| Surface: the text of the prompt | System: data retrieval + tool selection + memory |
| "Write a better prompt" | "Design a better information environment" |
| Skill of a user | Skill of a systems architect |

**Why it matters:** Gartner now uses the term officially. Anthropic published a working definition. It's the framework that underpins Modules 7–13 of this course.

> *"Context engineering treats AI quality as a systems problem: it focuses on what the model has access to — the rules, documents, memories and tools driving its behavior — rather than just how a single user message is phrased."* — Gartner, April 2026

**Facilitator Notes:**
- 🎤 Say: "Every recruiter asking for 'prompt engineering' skills in 2024 will be asking for 'context engineering' skills by 2027. Same work, better name."
- Common student question: "So prompt engineering is dead?" Answer: No — it's a subset. You still need to write good instructions, but that's the easy part. The hard part is everything around it.
- For all levels: this reframing helps students understand why Modules 7-13 exist
- Time: 4 minutes

---

### [NEW 2026] Slide: The Agentic Era — From Answering to Doing
**Insert after:** "Context Engineering" slide
**Format:** Data + concept

**Content:**

**The defining shift of 2025-2026: AI systems that act, not just answer.**

| Metric | Value | Source |
|--------|-------|--------|
| Enterprises with at least one AI agent in production | 31% | S&P Global / McKinsey |
| Enterprise apps embedding AI agents by end 2026 | 40% (up from <5% in 2025) | Gartner |
| Enterprise apps shipped in Q1 2026 with ≥1 agent | 80% | Gartner |
| AI coding agent market size | ~$10 billion (annualised, April 2026) | Gartner |
| Engineering teams using agentic coding treating IDEs as optional by 2027 | 65% | Gartner |

**What "agentic" means in practice:**
- **Chatbot (2023-2024):** You ask → it answers → you act
- **Assistant (2024-2025):** You ask → it answers + suggests → you decide → it helps
- **Agent (2025-2026):** You set a goal → it plans → it acts → it verifies → it reports

Gartner released its **first-ever Hype Cycle dedicated to Agentic AI** in June 2026, mapping 30+ innovations — this is now a distinct technology category, not a feature.

**Where agents are deployed today:**
- Banking & insurance: 47% have agents in production
- Healthcare: 18%
- Government: 14%

**Facilitator Notes:**
- 🎤 Say: "This is the single biggest shift since we moved from on-premises to cloud. Modules 11-13 of this course are dedicated entirely to building these systems."
- Common student question: "Are these real agents or just fancy chatbots?" Answer: Both exist in the market. The difference is whether the system can use tools, manage state, and make decisions autonomously. Most "agents" today are closer to "automated workflows with an LLM brain" — and that's fine. Real value doesn't require AGI.
- For beginners: keep it concrete — "an agent books your meeting, researches your competitor, writes your report, and emails it to your boss"
- For advanced: mention Gartner's Hype Cycle positioning, MCP/A2A protocols, multi-agent orchestration
- Time: 5 minutes

---

### [NEW 2026] Slide: Enterprise AI Adoption — The Real Numbers
**Insert after:** "AI value creation" section
**Format:** Data dashboard / statistics slide

**Content:**

**Enterprise AI Adoption, mid-2026:**

| Metric | Value |
|--------|-------|
| US business AI adoption rate | 50.6% (April 2026) |
| Organisations using AI in ≥1 function | 78% |
| Fortune 500 companies — adoption tripled YoY | 3× (2025→2026) |
| Global AI market value | $305 billion (2026) |
| Enterprise AI spending | $407 billion (2026, +35% YoY) |
| GenAI investment (2-year growth) | $1.7B → $37B |
| GenAI share of global SaaS market | 6% |
| ChatGPT enterprise message volume growth | 8× YoY |
| API reasoning token consumption per org | 320× YoY |
| Claude API calls (monthly) | 25 billion (45% from enterprise) |
| Gemini Enterprise paid seats | 8 million across 2,800 companies |

**What this tells us:**
1. Adoption is no longer the question — it's universal in large enterprises
2. Intensity of use is exploding (320× reasoning token growth!)
3. The competition is now between Claude, GPT, and Gemini for enterprise contracts
4. The real question has moved to: **value capture, not adoption**

**Facilitator Notes:**
- 🎤 Say: "When I show these numbers, the question stops being 'should we use AI?' and starts being 'why aren't we capturing value from AI we already use?'"
- Common student question: "Which provider is winning?" — Answer: Anthropic (Claude) recently overtook OpenAI in enterprise adoption (70% of Fortune 100 use Claude tools). But multi-model strategies are now the norm — 62% of enterprises use 3+ model providers.
- For beginners: the key message is "this is already everywhere" — they're not early
- For advanced: discuss the implications of 320× reasoning token growth — enterprises are moving from simple completion to complex multi-step reasoning
- Time: 4 minutes

---

### [NEW 2026] Slide: The New AI Value Chain
**Insert after:** Enterprise adoption slide
**Format:** Framework / visual hierarchy

**Content:**

The AI value chain has matured. Here's how value flows in 2026:

```
INFRASTRUCTURE     Compute (GPUs, Trainium, Inferentia) → Commodity
       │
    MODELS         Foundation models → Converging in capability
       │                               (open ≈ closed for many tasks)
       │
   HARNESS         Context engineering + agents → Where differentiation lives
       │           (memory, tools, orchestration, verification)
       │
  APPLICATION      Domain-specific AI products → Where value is captured
       │           (what the user actually experiences)
       │
    VALUE          Business outcome → What actually matters
                   (revenue, cost, speed, quality, risk)
```

**Key insight from 2026:** The model is becoming a commodity. The harness is where competitive advantage lives. This is why LangChain jumped from outside top-30 to rank 5 on TerminalBench by changing only the infrastructure wrapping the same model.

**Implications for careers:**
- "I know how to use ChatGPT" → Table stakes
- "I can design the context engineering around a model" → Valuable
- "I can architect and govern production AI systems" → Premium

**Facilitator Notes:**
- 🎤 Say: "This is the value stack. Notice where 'the model' sits — it's important but it's not where differentiation happens anymore. The harness and the application layer are where careers and companies are built."
- This directly motivates why Modules 7-16 exist
- For all levels: use this as a roadmap for the rest of the course
- Time: 4 minutes

---

### [NEW 2026] Slide: Open vs. Closed — The Spectrum Has Changed
**Insert after:** Model landscape slide
**Format:** Comparison table with nuance

**Content:**

**2024 framing:** "Open-source AI is always worse than closed — you pay for quality"  
**2026 reality:** "Open-weight models match or beat closed models on many tasks"

| Dimension | Closed Frontier (GPT-5.5, Claude Opus) | Open-Weight Frontier (DeepSeek V4, Llama 4, Qwen 3.5) |
|---|---|---|
| **Quality (general)** | Highest overall | 90-95% of closed on most benchmarks |
| **Quality (coding/agentic)** | Very high | DeepSeek V4 **ties** closed frontier on SWE-Bench |
| **Cost** | API pricing ($3-60/M tokens) | Self-host or cheap API providers |
| **Data control** | Data leaves your environment | Full control, air-gapped possible |
| **Customisability** | Limited (fine-tuning APIs) | Full (train, merge, distil, quantise) |
| **Speed to deploy** | Minutes (API key) | Hours to days (infra setup) |
| **Lock-in risk** | High (API changes, pricing) | Low (weights are yours) |
| **Reasoning capability** | Full (o3, extended thinking) | Growing (DeepSeek R1, Qwen-reasoning) |

**The new reality:**
- 50%+ of LLM deployments now use open-weight models (on-premises)
- Model routing (using different models for different tasks) is standard practice
- "Model-agnostic" architecture is no longer aspirational — it's required

**Facilitator Notes:**
- 🎤 Say: "If you're still assuming closed = better, you're leaving money and control on the table. The 2026 answer is: use both, route intelligently."
- Common student question: "Should we host our own?" Answer: Depends on data sensitivity, volume, and customisation needs. Many enterprises run open models for high-volume/sensitive tasks and API models for complex/low-volume tasks.
- ⚡ ADVANCED: discuss MoE (Mixture of Experts) architectures that enable large model capability at small model inference costs
- Time: 4 minutes

---

### [NEW 2026] Slide: AI Coding Agents — The Canary in the Mine
**Insert after:** "Agentic Era" slide
**Format:** Case study / emerging trend

**Content:**

AI coding agents are the **first category of agentic AI to achieve mainstream enterprise deployment** — and they show us where every other domain is headed.

**The numbers:**
- AI coding tool adoption: 84-91% across all major surveys (2025-2026)
- Enterprise AI coding agent market: ~$10 billion annualised (April 2026)
- Gartner predicts: 65% of engineering teams will treat IDEs as optional by 2027
- Trust in AI coding accuracy: dropped to 29% (down from 40%) despite higher adoption

**What happened:** Code completion → code generation → agentic coding
- **2023-2024:** Autocomplete suggestions (GitHub Copilot tab-complete)
- **2025:** Multi-file generation from natural language (Cursor, Windsurf)
- **2026:** Autonomous agents that plan, write, test, and fix code across entire repos (Claude Code, OpenAI Codex, Devin)

**The trust paradox:** Adoption up ↑ but trust down ↓ — because people are using agents for harder tasks where failures are more visible.

**Why this matters beyond coding:**
Every other enterprise function (sales, HR, finance, ops) will follow this same pattern with a 12-24 month lag. Coding agents are the template for how agentic AI enters the enterprise.

**Facilitator Notes:**
- 🎤 Say: "Coding agents are the first wave. Every function in your org will have its own version of this within 2 years. Watch what happens here — it's your preview."
- Common student question: "Will AI replace developers?" Answer: No, but it will replace developers who refuse to work with AI. The role shifts from "writing all the code" to "directing, reviewing, and governing AI-generated code."
- For all levels: concrete and relatable — most students have used Copilot/Cursor
- Time: 4 minutes

---

### [NEW 2026] Slide: Updated Myths vs. Realities (2026 Edition)
**Insert after:** Original "Common myths vs. realities" section
**Format:** [UPDATE 2026] — replaces/extends original content

**Content:**

| ❌ Myth (2026) | ✅ Reality (2026) |
|---|---|
| "Bigger models are always better" | Reasoning loops with smaller models often outperform single-shot larger models (Andrew Ng's HumanEval demo: GPT-3.5 in a loop beat GPT-4) |
| "AI will replace all developers" | 84-91% of developers use AI tools, but trust in accuracy dropped to 29%. AI augments; the role shifts. |
| "Open-source AI can't compete with closed" | DeepSeek V4 Pro ties closed frontier on SWE-Bench. 50%+ of deployments use open-weight models. |
| "We need better models to get value" | 89% deploy AI, 94% report no significant value. The gap is architecture, integration, and people — not models. |
| "Prompt engineering is the key skill" | Context engineering (designing what the model sees) matters more than how you word a single prompt. |
| "AI agents are future tech" | 31% of enterprises have agents in production. 80% of apps shipped in Q1 2026 include at least one agent. |
| "You need massive data to use AI" | Pre-trained foundation models + RAG + a few examples often outperform custom-trained models on enterprise tasks. |
| "AI adoption means AI value" | Only 6% of companies see >5% EBIT from AI. Adoption ≠ value. |

**Facilitator Notes:**
- 🎤 Use this as an interactive exercise: show the myth column, ask students to guess the reality before revealing it
- This replaces/extends the original myths section — it's 2026-specific and evidence-backed
- Common student reaction: shock at the 94% / 6% split. Use this to motivate the rest of the course.
- Time: 5 minutes (interactive)

---

### [NEW 2026] Slide: The "Three Eras" Framework
**Insert after:** "The generational shift" section
**Format:** Concept explanation / timeline

**Content:**

A clearer framing of where we've come and where we are:

**Era 1: Rules & Statistics (1960s–2018)**
- Hand-coded rules → machine learning → deep learning
- Required: domain experts, labelled data, training pipelines
- Output: predictions, classifications, recommendations

**Era 2: Generation (2018–2024)**
- Foundation models → transformers → LLMs
- Required: prompts, API access, some fine-tuning
- Output: text, images, code, audio — content creation

**Era 3: Reasoning & Agency (2025–present)**
- Reasoning models + agentic systems + context engineering
- Required: systems architecture, tool orchestration, governance
- Output: decisions, actions, workflows — task completion

**The shift that matters:** Each era changes what the AI produces AND what the human needs to bring.
- Era 1: humans bring data → AI gives predictions
- Era 2: humans bring instructions → AI gives content
- Era 3: humans bring goals → AI gives outcomes

**Where this course sits:** Primarily Era 3, with foundational coverage of Era 2 technologies.

**Facilitator Notes:**
- 🎤 Say: "Most AI training out there is still teaching Era 2. This course teaches Era 3 — because that's where the market is moving and where careers will be made."
- For all levels: simple, memorable framework students can use in their own presentations
- Time: 3 minutes

---

### [NEW 2026] Slide: What "AI-Native" Means for Organisations
**Insert after:** "How to think about AI value creation"
**Format:** Framework / levels

**Content:**

McKinsey's research reveals a stark hierarchy:

| Level | Description | % of Enterprises | AI Impact on EBIT |
|---|---|---|---|
| **AI Mature** | AI embedded in core workflows, measured, governed | ~1% | Transformative (>10%) |
| **AI High Performers** | Multiple AI systems in production, clear ROI | ~6% | Significant (>5%) |
| **AI Deployers** | At least one AI in production, limited measurement | ~82% | Minimal / unclear |
| **AI Experimenters** | POCs and pilots, no production deployment | ~11% | None |

**What separates the 6% from the 82%:**
1. **Architecture** — They build around the model, not just call the model
2. **Integration** — AI is in the workflow, not beside it
3. **Measurement** — They know what "good" looks like (evals, metrics)
4. **Governance** — They can trust the system to act autonomously
5. **People** — They have trained teams, not just licensed tools

**This course is designed to move people from the 82% to the 6%.**

**Facilitator Notes:**
- 🎤 Ask the class: "Where does your organisation sit on this ladder?" — guaranteed to provoke honest discussion
- This directly sets up Modules 5 (Roadmap) and 6 (AI-DLC) as the path from Deployer to High Performer
- Time: 4 minutes

---

### [NEW 2026] Slide: Multimodal AI — Beyond Text + Image
**Insert after:** Model landscape section
**Format:** Concept overview with examples

**Content:**

**2024:** Multimodal = text + image generation/understanding  
**2026:** Multimodal = text + image + video + audio + tool use + code execution + physical world interaction

**What's new in multimodal (2025-2026):**

| Capability | What It Means | Example |
|---|---|---|
| **Thinking with images** | Reasoning models can crop, zoom, rotate, annotate images in their chain-of-thought | o3/o4-mini visual reasoning |
| **Video understanding** | Process and reason about video content natively | Gemini 3.1 Pro, GPT-5.5 |
| **Computer use** | AI can see and interact with a computer screen | Claude computer use, OpenAI operator |
| **Audio native** | Real-time voice conversation with reasoning | GPT-4o voice, Gemini Live |
| **Multimodal RAG** | Retrieve and reason over documents including charts, tables, diagrams | ColPali, multimodal embeddings |

**The trajectory:** Every 6 months, another modality becomes production-ready. By 2027, most enterprise AI systems will be multimodal by default.

**Facilitator Notes:**
- 🎤 Say: "When we say 'multimodal' now, we don't just mean 'it can look at a picture'. We mean it can use a computer, watch a video, and talk to you — all while reasoning about what it's doing."
- For beginners: focus on computer use and voice as the most relatable examples
- For advanced: discuss ColPali and multimodal RAG implications for enterprise document processing
- Time: 3 minutes

---

### [NEW 2026] Slide: The Speed of Change — What to Expect Next
**Insert after:** Final content section (before activity/quiz)
**Format:** Future-looking / discussion

**Content:**

**What's on the 6-12 month horizon (mid-2026 forward):**

| Trend | Timeframe | Impact |
|---|---|---|
| **Agent-to-agent economies** | Now → 12 months | Agents from different vendors negotiate and transact autonomously |
| **Autonomous coding teams** | Now → 6 months | Full feature development without human intervention for standard work |
| **Model routing as default** | Now | Multiple models per application, chosen dynamically based on task |
| **AI governance regulation enforcement** | Now → 18 months | EU AI Act penalties begin. Non-compliance = material business risk |
| **Personal AI agents** | 6-12 months | Everyone has a persistent AI agent that knows their context and acts on their behalf |
| **Reasoning-first architectures** | Now | Systems designed around test-time compute, not just model selection |

**What this means for students:**
- The landscape in Module 1 will be outdated within 6 months of taking this course
- The **frameworks and principles** (context engineering, agentic architecture, governance) will remain valid
- Build mental models, not memorised facts

**Facilitator Notes:**
- 🎤 Say: "I want to be honest with you: specific model names and benchmarks I've shared today will be outdated within months. What WON'T be outdated are the patterns, the architecture principles, and the mental models. That's what this course teaches."
- Good closing slide for the module — motivates continued learning
- Time: 3 minutes

---

### [NEW 2026] Slide: Module 1 Knowledge Check — Updated Questions
**Insert after:** Original knowledge check (replaces or extends)
**Format:** [UPDATE 2026] Quiz update

**Content:**

Q1. What is "context engineering"?
- A) Writing better prompts for ChatGPT
- B) Designing the entire information system around a model — what it sees, when, and from where ✅
- C) Training a model on more context data
- D) Increasing the context window size

Q2. According to McKinsey (2026), what percentage of companies deploying AI report seeing "significant" value?
- A) 78%
- B) 50%
- C) 6% ✅
- D) 31%

Q3. What distinguishes a reasoning model (LRM) from a standard LLM?
- A) It uses more training data
- B) It spends extra compute at inference time generating internal thinking tokens before responding ✅
- C) It has a larger parameter count
- D) It can only do mathematics

Q4. By end of 2026, what percentage of enterprise applications will embed AI agents according to Gartner?
- A) 5%
- B) 15%
- C) 40% ✅
- D) 80%

Q5. In the 2026 AI value chain, where does competitive differentiation primarily live?
- A) In the GPU infrastructure layer
- B) In the foundation model itself
- C) In the harness / context engineering layer ✅
- D) In the user interface

**Facilitator Notes:**
- These replace the original quiz — they test 2026-current knowledge
- Q2 is the "shock" question — most students guess much higher
- Q5 connects directly to the value chain framework earlier in the module

---

### [NEW 2026] Slide: Discussion Questions — Updated 2026
**Insert after:** Quiz section
**Format:** Discussion / interactive

**Content:**

1. **The Performance Paradox:** 89% of companies deploy AI but only 6% see significant value. What do you think the 6% are doing differently? (Preview of Modules 5 & 6)

2. **Open vs. Closed:** If open-weight models now match closed models on many benchmarks, what's the business case for continuing to pay for API access to closed models? When does self-hosting make sense?

3. **Context Engineering Careers:** Andrej Karpathy and Gartner both say "context engineering" is the new skill. What does this mean for your current role? How would you explain it to your manager?

4. **The Trust Paradox:** AI coding adoption is at 84-91%, but trust in AI accuracy dropped from 40% to 29%. Why? What does this tell us about how AI adoption actually works?

5. **6-Month Obsolescence:** If the specific model landscape in this module will be outdated within 6 months, what's the point of learning it at all? What should you actually memorise vs. what should you develop as a skill?

**Facilitator Notes:**
- These are designed for 8-10 minutes of small-group discussion
- Q1 directly motivates the rest of the course
- Q5 is metacognitive — helps students develop a learning strategy, not just memorise facts

---

### [NEW 2026] Slide: Recommended Resources — 2026 Update
**Insert after:** Original resources section
**Format:** [UPDATE 2026] Resource list

**Content:**

**Reports & Data:**
- McKinsey: "AI Productivity Gains and the Performance Paradox" (April 2026)
- Gartner: "Hype Cycle for Agentic AI" (June 2026) — first dedicated agentic AI hype cycle
- OpenAI: "The State of Enterprise AI 2025 Report"
- Digital Applied: "AI Agent Adoption 2026: 120+ Enterprise Data Points"

**Key Articles:**
- Forbes: "Prompt Engineering Is Not Dead" (June 2026) — the context engineering vs. prompt engineering debate
- InfoWorld: "What is Context Engineering? And Why It's the New AI Architecture" (July 2026)
- Gartner: "Context Engineering — Why It's Replacing Prompt Engineering" (April 2026)

**Model Landscape:**
- Codersera: "Open Source LLMs Landscape 2026" — comprehensive comparison
- Artificial Analysis (artificialanalysis.ai) — real-time model benchmarking

**AWS:**
- Amazon Nova Model Release Timeline (from re:Invent 2024 through Nova 2 at re:Invent 2025)
- Amazon Bedrock documentation — current model availability

**Facilitator Notes:**
- Share the McKinsey "Performance Paradox" article as pre-reading — it sets up the course beautifully
- The Gartner Hype Cycle for Agentic AI is behind a paywall but the summary is widely available

---

## FACILITATOR UPDATE BRIEF

### Top 3 Most Important Additions

1. **The AI Performance Paradox** (McKinsey: 89% deploy, 6% capture value) — This single data point justifies the entire course. Lead with it. Make it the emotional hook that carries students through 16 modules.

2. **Reasoning Models as a paradigm shift** — Students will encounter o3, Claude extended thinking, and Gemini Deep Think in the wild immediately. They need to understand test-time compute and why iterative reasoning loops beat single-shot prompting. This sets up Modules 7 and 11.

3. **Context Engineering as the new framing** — Endorsed by Karpathy, Lütke, and Gartner. This is the organising principle that connects prompting (Module 7), RAG (Module 8), and agents (Modules 11-13). Introduce it in Module 1 as a preview.

### What's Now Outdated in the Original

| Original Content | Issue | How to Address |
|---|---|---|
| "Common myths vs realities" | Myths were 2024-era | Replace with 2026 myths table (provided above) |
| AI landscape map | Only ~5 model families | Update with the 10+ family table |
| Enterprise adoption data | Was 2024 data | Replace with 2026 statistics (50.6% adoption, $407B spending) |
| "The generational shift" framing | Only covers Era 1→2 | Extend to the Three Eras framework (Era 3 = reasoning + agency) |
| Multimodal coverage | Text + image only | Extend to video, audio, computer use, visual reasoning |

### How to Fit in 60 Minutes

The original 60-minute module + 12 new slides would need ~90 minutes. Recommended approach:

**Option A — 60 minutes (tight, skip some original content):**
- Cut original "history of AI" section to 2 minutes (students can read this)
- Replace original myths with new myths table (saves 3 min)
- Replace original stats with new stats (saves 2 min)
- Add: Performance Paradox (5 min), Reasoning Models (5 min), Context Engineering (4 min), Agentic Era (5 min), Value Chain (4 min)
- Keep one original activity but shorten to 8 minutes
- Total: ~60 minutes

**Option B — 75 minutes (recommended for in-person delivery):**
- Deliver all original content (abbreviated)
- Add all [NEW 2026] slides
- Full discussion time
- Extended Q&A

**Option C — 90 minutes (deep-dive version):**
- Full original + all new slides + extended discussion + live demo of reasoning model vs standard model comparison

### New Tools/Accounts/Demos to Set Up

1. **Claude.ai account** — to demo extended thinking (visible chain-of-thought)
2. **Artificial Analysis** (artificialanalysis.ai) — live model comparison dashboard (free, no account needed)
3. **Chatbot Arena** (lmarena.ai) — live model comparison leaderboard
4. **Access to at least 2 different model APIs** — to show the "model routing" concept in action (e.g., call Claude for reasoning, GPT for generation, open model for classification)

---

*Module 01 Update Complete — AI & Agentic AI Training Programme — July 2026*
