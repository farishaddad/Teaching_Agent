# Module 03 — AI for Technical Audiences: How It Actually Works
## 🔄 2026 Update: New Slides & Facilitator Delivery Notes

---

## Gap Analysis

The original Module 03 covered the foundational mechanics of LLMs well for a 2024 audience. In mid-2026, the following gaps are significant:

1. **Reasoning models are completely absent.** OpenAI o3, Claude extended thinking, DeepSeek R1, and Gemini Deep Think are production-grade reasoning models that students will encounter daily. The original module doesn't mention them or explain how they differ architecturally from standard LLMs.

2. **Mixture of Experts (MoE) is now the dominant frontier architecture.** By April 2026, every frontier model except Anthropic's Claude line uses MoE. DeepSeek V3/V4, GPT-5.5, Qwen 3 — all ship sparsity. The original module treats all models as dense transformers.

3. **Test-time compute scaling (inference-time reasoning budgets)** is a new paradigm not covered at all. The shift from "scale training compute" to "scale inference compute" is arguably the biggest conceptual shift in the field.

4. **Context windows have standardised at 1M tokens** (up from 128K–200K). Llama 4 Scout claims 10M. The practical implications — including "context rot" and effective attention limits — are not addressed.

5. **Speculative decoding** is now the highest-ROI inference optimization (2–4× speedup with identical output quality). The original module mentions "inference considerations" generically but doesn't cover this technique.

6. **Multi-Head Latent Attention (MLA)** — DeepSeek's innovation that reduces KV cache by 75–93% — is reshaping how production inference is done. Not covered.

7. **Multimodal architectures have matured** from "vision bolted on" to natively multimodal models (GPT-4o, Gemini, etc.). The original only briefly mentions multimodality as a milestone.

8. **The pricing/performance landscape has inverted.** DeepSeek V4 Flash: $0.14/M input tokens. GPT-5.5: $30/M output tokens. The 200× price spread with narrowing performance gaps is a critical architectural decision factor not covered.

9. **Distillation and model merging** have moved from research to production tooling. Open-weight models trained via distillation from frontier models now rival closed-source on specific tasks.

10. **Post-training alignment has evolved beyond RLHF.** GRPO (Group Relative Policy Optimization), DPO, Constitutional AI, and other methods are now standard. The original module only covers RLHF.

---

## New Slides

---

### [NEW 2026] Slide: The Two Scaling Laws — Training vs. Inference Compute
**Insert after:** "How LLMs are trained" section
**Format:** Concept explanation with diagram

**Content:**

Until 2024, the dominant belief was that AI capability scales with **training compute** — more GPUs, more data, more time → smarter model. This is Chinchilla/Kaplan scaling.

In 2025–2026, a second scaling axis emerged: **test-time compute** (inference-time reasoning).

```
┌────────────────────────────────────────────────────────────┐
│              TWO SCALING AXES                               │
│                                                            │
│  TRAINING-TIME SCALING (Chinchilla/Kaplan)                 │
│  ─────────────────────────────────────────                 │
│  More compute at training → smarter model                  │
│  Diminishing returns beyond ~10^26 FLOPs                   │
│  Fixed capability at deployment                            │
│                                                            │
│  TEST-TIME SCALING (2025+)                                 │
│  ─────────────────────────────────────────                 │
│  More compute at inference → better answer on THIS query   │
│  Adaptive: easy questions = cheap, hard questions = think  │
│  Same model, different intelligence per problem            │
│                                                            │
│  KEY INSIGHT: A $0.01 query to o3 and a $2.00 query to    │
│  o3 can produce vastly different quality answers from the  │
│  same weights.                                             │
└────────────────────────────────────────────────────────────┘
```

**Why this matters:** Choosing the right compute budget per query is now an engineering decision as important as choosing the right model. "More thinking" isn't free — Claude extended thinking can cost $0.26/request at max budget vs. $0.013 without.

**Facilitator Notes:**
- Open with: "Until 2024, making AI smarter meant training a bigger model. In 2025, we learned you can also make AI smarter by letting it think longer at inference time. This is the single biggest conceptual shift in the field."
- Common student question: "Is this just chain-of-thought prompting?" Answer: No — CoT prompting is a user technique. Reasoning models have architectural training to do internal deliberation before output.
- For beginners: Focus on the economic implication — same model, different cost/quality per query.
- For advanced: Discuss the Plan-and-Budget framework — decomposing queries into sub-questions and allocating token budgets adaptively.
- Time: 5 minutes

---

### [NEW 2026] Slide: Reasoning Models — A New Architecture Category
**Insert after:** The Two Scaling Laws slide
**Format:** Concept explanation + comparison table

**Content:**

Reasoning models (o3, Claude Extended Thinking, DeepSeek R1, Gemini Deep Think) are NOT just LLMs with better prompts. They are architecturally distinct:

| Property | Standard LLM | Reasoning Model |
|---|---|---|
| Output generation | Token-by-token, no deliberation | Internal chain-of-thought BEFORE visible output |
| Hidden computation | None — every token is visible | Thinking tokens (hidden or in a separate block) |
| Cost profile | Predictable per-token | Variable — "thinking" adds 2,000–10,000+ tokens |
| Latency | Proportional to output length | 5–60× slower due to deliberation phase |
| Best for | Creative writing, translation, chat | Math, coding, logic, scientific analysis, planning |
| Prompting style | Detailed instructions, CoT helpful | Minimal prompting — model reasons internally |
| Training method | RLHF / DPO | Process reward models + RL on reasoning traces |

**Key insight:** Reasoning models perform an internal search — exploring and pruning solution paths before committing to an answer. Think of standard LLMs as System 1 (fast, intuitive) and reasoning models as System 2 (slow, deliberate).

**The reasoning model family (mid-2026):**
- OpenAI o3 / o3-mini / o4-mini
- Anthropic Claude with Extended Thinking
- Google Gemini Deep Think
- DeepSeek R1 / R1-Lite
- Qwen QwQ

**Facilitator Notes:**
- Key point: "When someone asks 'should I use a reasoning model?', the answer is about the problem, not the user. Math, logic, multi-step planning = yes. Creative writing, summarisation = no, you're paying for thinking you don't need."
- Common question: "Can I see the thinking tokens?" — Depends on provider. Anthropic shows them in a `<thinking>` block. OpenAI hides them (you pay but don't see). DeepSeek R1 exposes them.
- Demo opportunity: Show the same coding problem solved by Claude Sonnet (fast) vs. Claude with extended thinking — visibly different quality + cost.
- Time: 5 minutes

---

### [NEW 2026] Slide: Prompting Reasoning Models Differently
**Insert after:** Reasoning Models slide
**Format:** Practical guidance with examples

**Content:**

⚠️ **Existing prompt engineering patterns BREAK on reasoning models.**

What changes:
1. **Less instruction = better results.** Detailed step-by-step instructions actually harm performance — they interfere with the model's own reasoning process.
2. **No chain-of-thought prompting needed.** The model already chains internally. Adding "think step by step" is redundant and may confuse it.
3. **System prompts are shorter.** Role prompting and persona design are less effective — the model is trained to reason, not roleplay.
4. **Temperature and sampling change.** Reasoning models often perform best at temperature 0 (deterministic reasoning).
5. **Budget control is the new lever.** Instead of tuning prompts, you control how much reasoning budget the model gets.

```
❌ WRONG (standard LLM prompt on reasoning model):
"You are an expert mathematician. Think step by step.
First identify the variables. Then set up equations.
Then solve systematically. Show all work."

✅ RIGHT (reasoning model prompt):
"Solve this optimization problem: [problem statement]"
```

**The new hierarchy of prompting:**
- Standard LLMs: detailed prompts → better output
- Reasoning models: clear problem statement → let the model reason → better output

**Facilitator Notes:**
- This slide often surprises students who've invested heavily in prompt engineering. Emphasise: "Your prompt skills still apply to standard LLMs. But reasoning models want you to get out of the way."
- Live demo: Show same problem with verbose vs. minimal prompt on o3. Minimal often wins.
- Time: 3 minutes
- ⚡ ADVANCED: Discuss "thinking budget" as an API parameter (Anthropic's `max_tokens_thinking`)

---

### [NEW 2026] Slide: Mixture of Experts (MoE) — The Dominant Architecture
**Insert after:** "Model families and their trade-offs" section
**Format:** Architecture explanation with diagram

**Content:**

**By mid-2026, every frontier model except Claude uses Mixture of Experts.**

MoE lets models grow much larger (more knowledge, more capability) without proportionally increasing inference cost. Only a subset of parameters ("experts") activate for each token.

```
┌─────────────────────────────────────────────┐
│           HOW MoE WORKS                      │
│                                              │
│  Input Token                                 │
│      ↓                                       │
│  [Router / Gate Network]                     │
│      ↓ selects top-K experts                 │
│  ┌───┐ ┌───┐ ┌───┐ ┌───┐ ... ┌───┐         │
│  │E1 │ │E2 │ │E3 │ │E4 │     │EN │         │
│  └─┬─┘ └───┘ └─┬─┘ └───┘     └───┘         │
│    │  ACTIVE   │   INACTIVE (not computed)   │
│    ↓           ↓                             │
│  [Weighted Combination]                      │
│      ↓                                       │
│  Output                                      │
│                                              │
│  Total params: 671B  |  Active per token: 37B│
│  (DeepSeek V3 example)                       │
└─────────────────────────────────────────────┘
```

**Key MoE models in 2026:**

| Model | Total Params | Active Params | Sparsity | Experts |
|---|---|---|---|---|
| DeepSeek V3 | 671B | 37B | ~94% | 256 fine-grained |
| GPT-5.5 | ~1.8T (est.) | Unknown | High | Estimated 16 |
| Mixtral 8x22B | 176B | 44B | 75% | 8, top-2 routing |
| Qwen 3 MoE | ~400B | ~40B | ~90% | 128 |
| Llama 4 Maverick | 400B | 17B | ~96% | 128, routed |

**Why this matters for practitioners:**
- You get "big model" intelligence at "small model" inference cost
- Hosting requires more RAM (full model loaded) even though compute is lower
- Expert routing quality determines output quality — not all tokens get equal treatment

**Facilitator Notes:**
- Open with: "If someone asks 'how can DeepSeek be as good as GPT at 1/200th the price?' — this slide is the answer."
- Common question: "Why doesn't Anthropic use MoE?" — They prioritise dense models for reliability and consistency. Trade-off: more expensive but every parameter engaged.
- For beginners: Focus on the economic insight (big brain, small bill). For advanced: discuss routing strategies (top-k, expert-choice, fine-grained shared).
- Time: 5 minutes

---

### [NEW 2026] Slide: DeepSeek V3 — The Architecture That Changed the Economics
**Insert after:** MoE slide
**Format:** Case study / architecture deep-dive

**Content:**

DeepSeek V3 (Dec 2024 → production 2025) is the most influential open model architecture of the last 18 months. It introduced two innovations that are now industry-standard:

**1. Multi-Head Latent Attention (MLA)**
Traditional attention stores full Key and Value matrices per layer → enormous memory (KV cache). MLA projects Q, K, V into a compact latent space first:
- KV cache reduced by **75–93%** compared to standard attention
- Enables serving long contexts affordably
- Shifts attention from memory-bound to compute-bound

**2. Auxiliary-Loss-Free Load Balancing**
Traditional MoE suffers from "expert collapse" (some experts used too much, others starved). Previous fix: add a loss term that penalises imbalance. DeepSeek eliminated this auxiliary loss entirely using a dynamic bias mechanism — simpler, better training stability.

**3. Multi-Token Prediction (MTP)**
Instead of predicting only the next token, DeepSeek V3 predicts multiple future tokens simultaneously during training. This:
- Improves training sample efficiency
- Can be used at inference for speculative self-verification
- Teaches the model to "plan ahead"

**The cost headline:** Trained on 2,048 H800 GPUs for ~$5.5M total — a fraction of comparable closed-source models ($100M+).

**Facilitator Notes:**
- This is the "how did they do it so cheaply?" slide. Students will have heard about DeepSeek. Give them the actual technical answer.
- Common question: "Can I use MLA in my own models?" — It's open-sourced. Hugging Face transformers supports it. But it requires custom kernels for full performance.
- ⚡ ADVANCED slide — beginners can be told "DeepSeek innovated on attention and expert routing to achieve frontier quality at 1/20th the cost" without the mechanics.
- Time: 5 minutes

---

### [NEW 2026] Slide: Context Windows — From 128K to 10M (And What Actually Works)
**Insert after:** "Tokens, embeddings, context windows, and temperature" section
**Format:** Data-driven comparison + practical guidance

**Content:**

**The headline:** Context windows standardised at 1M tokens in H1 2026. Llama 4 Scout claims 10M.

| Model | Max Context | Effective Reliable Range | Price per 1M Input Tokens |
|---|---|---|---|
| GPT-5.5 | 1M | ~500K–800K | $7.50 |
| Claude Opus 4 | 1M | ~600K–900K | $15.00 |
| Gemini 3.1 Pro | 2M | ~1M–1.5M | $3.50 |
| DeepSeek V4 | 128K | ~100K | $0.14 |
| Llama 4 Scout | 10M | ~2M (early reports) | Open-weight |

**The critical distinction:** "Technically accepts 1M tokens" ≠ "reliably reasons over 1M tokens."

**Context Rot (Lost in the Middle problem):**
- Model performance degrades **30%+** when key content falls in mid-window positions
- Benchmarks distinguishing acceptance from reliability arrived in early 2026 (RULER, BABILong)
- Practical implication: Position critical information at the **beginning or end** of context

**The RAG vs. Long Context decision in 2026:**

| Scenario | Winner |
|---|---|
| Corpus < 5M tokens, static | Long context (stuff it all in) |
| Corpus > 5M tokens | RAG still wins |
| Content changes daily | RAG wins (freshness) |
| Need attribution/citations | RAG wins (source tracking) |
| Latency-critical | RAG wins (faster than processing 1M tokens) |
| Simplicity-critical | Long context wins (no vector DB stack) |

**Facilitator Notes:**
- Lead with: "Every vendor says '1M tokens'. Here's the dirty secret — there's a difference between accepting tokens and actually using them."
- This connects to Module 8 (RAG): "Long context is NOT killing RAG. It's changing when you need it."
- Demo: Show a needle-in-a-haystack test at different positions in a 200K-token context — hit rate drops in the middle.
- Time: 5 minutes

---

### [NEW 2026] Slide: Speculative Decoding — The Highest-ROI Inference Trick
**Insert after:** "Inference, latency, and deployment considerations" section
**Format:** Technical explanation with diagram

**Content:**

**The problem:** LLM inference is memory-bandwidth-bound. The GPU is mostly idle waiting for model weights to transfer from memory — generating one token per forward pass wastes most of its compute capability.

**The solution:** Speculative decoding uses a small, fast "draft" model to propose K tokens, then the large model verifies all K in a single forward pass. Accepted tokens are free — you only pay for the one verification pass.

```
WITHOUT Speculative Decoding:
  Large model → token 1 → token 2 → token 3 → ... (slow, one at a time)

WITH Speculative Decoding:
  Draft model → proposes tokens [1,2,3,4,5] (fast, cheap)
  Large model → verifies all 5 at once (single forward pass)
  Result: tokens [1,2,3] accepted ✓, token 4 rejected ✗
  Net gain: 3 tokens for the cost of ~1 large-model forward pass
```

**Performance (2026 production data):**
- Typical speedup: **2–4×** with mathematically identical output
- No quality degradation — output is provably identical to greedy/sampled decoding
- Works best for: code generation, structured output, predictable continuations
- Works worst for: highly creative/divergent text (draft model can't predict well)

**Modern variants:**
| Method | Draft Approach | Speedup | Overhead |
|---|---|---|---|
| Standard SD | Separate small model | 2–3× | Must host 2 models |
| EAGLE-2 | Lightweight head on same model | 2–4× | Minimal extra params |
| Medusa | Multi-head parallel prediction | 2–3× | Same model, extra heads |
| Self-speculative | Use model's own early layers | 1.5–2× | No extra model needed |
| n-gram matching | Token n-gram lookup (no model) | 1.5–2× | Zero GPU cost for drafting |

**Facilitator Notes:**
- Analogy: "It's like having an intern draft an email and you just approve/reject each sentence in bulk — faster than writing from scratch."
- Common question: "Why isn't this always used?" — It IS now standard in most serving frameworks (vLLM, TGI). But it helps most at batch size 1; at high batch sizes the large model's GPU is already saturated.
- For beginners: Focus on the "free speedup, no quality loss" message.
- ⚡ ADVANCED: Discuss EAGLE's feature-level drafting vs. token-level drafting.
- Time: 5 minutes

---

### [NEW 2026] Slide: KV Cache — The Hidden Bottleneck
**Insert after:** Speculative Decoding slide
**Format:** Technical concept explanation

**Content:**

**What is the KV cache?**
During autoregressive generation, the model re-uses computed Key and Value matrices from all previous tokens. Storing these avoids recomputing attention from scratch at each step — but the memory cost is enormous.

**Why it matters in 2026:**
- A 70B model at 128K context: KV cache alone = **40+ GB of GPU memory**
- At 1M context: KV cache dominates total memory (more than model weights)
- It's the #1 constraint on how many concurrent users a single GPU can serve

**The KV cache problem → solutions spectrum:**

| Technique | How It Works | Memory Saving | Quality Impact |
|---|---|---|---|
| KV quantization (AQUA-KV) | Compress K/V to 2–4 bits | 60–75% | Near-lossless at 4-bit |
| Grouped-Query Attention (GQA) | Share K/V heads across query groups | 50–80% | Minimal |
| Multi-Head Latent Attention (MLA) | Project into low-dim latent space | 75–93% | None (architectural) |
| Token eviction | Drop "unimportant" tokens from cache | 40–60% | Task-dependent |
| PagedAttention (vLLM) | Non-contiguous memory allocation | Reduces waste | Zero |
| CPU offloading (MIRAGE) | Remap parameter memory for KV | ~80% GPU saving | Adds latency |

**The practical takeaway:** When you're told "this model supports 1M context," ask: "how much does the KV cache cost at that length?" The answer determines whether it's economically viable for your use case.

**Facilitator Notes:**
- This is the "why can't I just give it all my documents?" answer. Students hitting memory limits in production will immediately connect.
- Common question: "Which technique should I use?" — PagedAttention (vLLM) is free and automatic. GQA is baked into model architecture. KV quantization is the biggest lever for existing models.
- ⚡ ADVANCED — beginners can skip this slide. For advanced: draw the memory waterfall chart showing model weights vs. KV cache vs. activations at different sequence lengths.
- Time: 4 minutes

---

### [NEW 2026] Slide: Native Multimodal Architecture (Not "Vision Bolted On")
**Insert after:** MoE architecture section or existing multimodality mention
**Format:** Architecture comparison

**Content:**

**2023 approach:** Separate vision encoder (ViT) → adapter → feed into LLM text model. Images are "translated" into text-space tokens. Modalities are loosely connected.

**2025–2026 approach:** Natively multimodal — all modalities share the same transformer backbone from pre-training. No adapter needed. The model "thinks" in a unified space across text, image, audio, and video.

```
OLD: "Bolt-on" Architecture
  [Image] → ViT Encoder → Adapter → [LLM (text-native)]
  (Image information "translated" to text space)

NEW: Native Multimodal Architecture
  [Image + Text + Audio] → Unified Tokeniser → [Shared Transformer]
  (All modalities in same latent space from pre-training)
```

**Frontier multimodal capabilities (mid-2026):**

| Model | Input Modalities | Output Modalities | Native? |
|---|---|---|---|
| GPT-5.5 / GPT-4o | Text, Image, Audio, Video | Text, Image, Audio | Yes |
| Gemini 3.1 | Text, Image, Audio, Video | Text, Image | Yes |
| Claude Opus 4 | Text, Image, PDF | Text | Vision via encoder |
| Llama 4 | Text, Image | Text | Yes |
| Qwen 2.5-VL | Text, Image, Video | Text | Yes |

**Why native matters:**
- Better cross-modal reasoning (model can "see" and "read" simultaneously)
- Lower latency (no encoder hop)
- Emergent capabilities (diagram understanding, visual counting, spatial reasoning)
- Enables: UI agent navigation, document understanding, video analysis

**Facilitator Notes:**
- Demo opportunity: Show a model analysing a complex architecture diagram and explaining it — something bolt-on models couldn't do reliably.
- Common question: "Can Claude really not generate images?" — Correct. Anthropic focused on text output. They accept images as input (via a vision encoder) but don't generate them.
- Time: 4 minutes

---

### [NEW 2026] Slide: The Model Landscape in Mid-2026 — A Practitioner's Map
**Insert after:** Model families section
**Format:** Comparison table (updated)

**Content:**

The landscape has stratified into clear tiers with distinct use cases:

| Tier | Models | Active Params | Context | Price (input/M) | Best For |
|---|---|---|---|---|---|
| **Frontier Reasoning** | o3, Claude Extended, Gemini Deep Think | Full (dense/MoE) | 128K–1M | $5–30 | Math, code, complex analysis |
| **Frontier General** | GPT-5.5, Claude Opus 4, Gemini 3.1 | Full | 1M–2M | $3–15 | General high-quality tasks |
| **Mid-tier Workhorse** | Claude Sonnet 4, GPT-4.1, Gemini Flash | Moderate | 200K–1M | $0.40–3 | Day-to-day production work |
| **Fast/Cheap** | GPT-4o-mini, Claude Haiku 4, DeepSeek V4 Flash | Small/efficient | 128K | $0.04–0.30 | High-volume, latency-critical |
| **Open-weight Frontier** | Llama 4, DeepSeek V4, Qwen 3, MiniMax M3 | 17B–37B active | 128K–10M | Self-hosted | Full control, on-prem, customisation |
| **Small/Edge** | Phi-4, Gemma 3, Llama 3.2 3B | 2–14B | 4K–128K | Self-hosted | On-device, embedded, offline |

**The 2026 pricing reality:**
- Most expensive: o3 at max reasoning budget → ~$60/M output tokens
- Cheapest frontier: DeepSeek V4 Flash → $0.14/M input tokens
- That's a **428× price spread** with narrowing quality gap
- "Which model?" is now an economic question as much as a capability question

**Facilitator Notes:**
- Update this table before each delivery — the landscape changes monthly.
- Key message: "There is no single best model. There is only the best model for your task at your budget."
- Activity tie-in: Students should map their use cases to tiers as an exercise.
- Time: 5 minutes

---

### [NEW 2026] Slide: Beyond RLHF — Modern Alignment Techniques
**Insert after:** "How LLMs are trained: pre-training, fine-tuning, RLHF" section
**Format:** Technical comparison

**Content:**

RLHF (2022–2023) was the breakout alignment technique. But training a separate reward model is expensive and unstable. The field has moved to simpler, more efficient methods:

| Method | How It Works | Advantages | Used By |
|---|---|---|---|
| **RLHF** | Reward model + PPO optimisation | Well-understood, strong results | OpenAI (still, partially) |
| **DPO** (Direct Preference Optimization) | Train directly on preference pairs, no reward model | Simpler, cheaper, more stable | Llama, many open models |
| **GRPO** (Group Relative Policy Optimization) | Group responses, rank relatively, no critic model | DeepSeek's secret weapon — very efficient | DeepSeek R1, V3 |
| **Constitutional AI (CAI)** | Model critiques its own outputs against principles | Self-improving, scalable | Anthropic Claude |
| **Process Reward Models** | Reward each reasoning STEP, not just final answer | Critical for reasoning models | o3, R1 |
| **RLAIF** (RL from AI Feedback) | AI generates the preference data | Scales without human labelers | Google, various |

**The key shift:** From rewarding final answers to rewarding **reasoning processes**. Process Reward Models (PRMs) are what make reasoning models possible — they evaluate whether each thinking step is valid, not just whether the final answer is correct.

**Facilitator Notes:**
- Lead with: "RLHF was the original magic that turned GPT-3 into ChatGPT. But the field has moved on — here's what actually trains the models you use today."
- For beginners: "The key insight is that we've found cheaper, simpler ways to align models. RLHF was expensive and finicky. DPO and GRPO are more practical."
- For advanced: Discuss the implications of process reward — it enables reasoning models to self-correct mid-chain because each step is independently evaluable.
- Common question: "Which should I use if I'm fine-tuning?" — DPO for most use cases. It's well-supported in Hugging Face TRL, requires only preference pairs, no reward model training.
- Time: 4 minutes

---

### [NEW 2026] Slide: Structured Outputs — Guaranteed Machine-Readable Responses
**Insert after:** Temperature/inference section or Prompt Engineering connection
**Format:** Technical + practical

**Content:**

**The problem (2023–2024):** You ask an LLM for JSON. Sometimes you get JSON. Sometimes you get JSON wrapped in markdown. Sometimes you get a conversational response with JSON buried inside.

**The solution (2025+):** Constrained decoding / structured output guarantees.

Major providers now offer **native structured output** that guarantees valid JSON/schema conformance:

```python
# OpenAI Structured Outputs
response = client.chat.completions.create(
    model="gpt-4o",
    response_format={
        "type": "json_schema",
        "json_schema": {
            "name": "extraction",
            "schema": {
                "type": "object",
                "properties": {
                    "entities": {"type": "array", "items": {"type": "string"}},
                    "sentiment": {"type": "string", "enum": ["positive", "negative", "neutral"]}
                },
                "required": ["entities", "sentiment"]
            }
        }
    },
    messages=[{"role": "user", "content": "Extract entities and sentiment from: ..."}]
)
# Guaranteed to return valid JSON matching this schema — no parsing errors, ever
```

**How it works (constrained decoding):**
- At each token position, the model's logits are masked to only allow tokens that are valid continuations of the target schema
- It's like putting guardrails on the generation highway — the model can only produce valid output
- Zero quality loss for well-designed schemas

**Provider support (mid-2026):**
| Provider | Feature | Schema Support |
|---|---|---|
| OpenAI | `response_format: json_schema` | Full JSON Schema |
| Anthropic | Tool use with schemas | JSON Schema via tools |
| Google | Controlled generation | JSON Schema |
| vLLM/Outlines | Constrained decoding | Regex, JSON, CFG |

**Facilitator Notes:**
- This is immediately practical for every student. "Never write another JSON parser for LLM output again."
- Demo: Show code that uses structured outputs vs. code that parses unstructured output + handles errors. The difference in reliability and code simplicity is dramatic.
- Connection to agents: Structured outputs are what make reliable tool calling possible. An agent that can't produce valid function call arguments is useless.
- Time: 4 minutes

---

### [NEW 2026] Slide: Inference Economics — The New Decision Framework
**Insert after:** Deployment considerations
**Format:** Decision framework

**Content:**

In 2026, choosing how to serve an LLM is as important as choosing which LLM to serve. The decision space:

**Cost Levers in LLM Inference:**

| Lever | Effect | Trade-off |
|---|---|---|
| **Model size** (smaller = cheaper) | 10–100× cost reduction | Capability loss |
| **Quantization** (4-bit, 8-bit) | 2–4× memory saving | Minimal quality loss |
| **Speculative decoding** | 2–4× latency reduction | No quality loss |
| **Batching** (continuous batching) | 3–10× throughput | Increased latency |
| **KV cache optimization** | 50–93% memory saving | Architecture-dependent |
| **Reasoning budget** | Control thinking cost | Quality on hard problems |
| **Caching/semantic cache** | 100× on repeat queries | Only helps repeated patterns |
| **Model routing** | Send easy → cheap, hard → expensive | Routing accuracy matters |

**The Model Router Pattern (2026 production standard):**
```
User Query → [Complexity Classifier] → Easy?  → Haiku/Flash ($0.04/M)
                                      → Medium? → Sonnet/4o ($1/M)
                                      → Hard?   → Opus/o3 ($15–60/M)
```

**Real-world economics:**
- A 1M daily query workload routed well: **$200–500/day**
- Same workload, all to frontier: **$15,000–40,000/day**
- Model routing can reduce costs 30–50× without meaningful quality loss on the aggregate

**Facilitator Notes:**
- This connects Module 3 (technical) to Module 16 (FinOps for AI). "Understanding the mechanics is how you make smart economic decisions."
- Common question: "How do I build a router?" — Start simple: input length + keyword classification. Graduate to a small classifier trained on your own traffic.
- Activity: Give students 5 use cases and ask them to assign each to a tier with cost estimate.
- Time: 5 minutes

---

### [NEW 2026] Slide: Multi-Token Prediction (MTP) and Next-Generation Training Objectives
**Insert after:** Beyond RLHF slide or training section
**Format:** Technical concept
**⚡ ADVANCED**

**Content:**

Traditional LLM training: predict the next single token given all previous tokens. Simple, effective, but potentially myopic — the model never learns to "plan ahead."

**Multi-Token Prediction (MTP):**
- Model simultaneously predicts the next 2–4 tokens at each position
- Shared trunk → multiple prediction heads (one per future position)
- Forces the model to develop longer-range planning in its internal representations

**Results (DeepSeek V3 / Meta research):**
- Improves code generation significantly (requires planning structure)
- Improves factual consistency (model "sees" where it's going)
- Can be used at inference: model's own future predictions become speculative decode candidates ("self-speculative decoding")

```
Standard training:         Predict token[t+1]
MTP training:              Predict token[t+1], token[t+2], token[t+3], token[t+4]
                           (separate heads, shared backbone)
```

**Why it matters:** Models trained with MTP show better coherence on long outputs because they've learned to consider future context during generation. This is one reason DeepSeek V3 writes better long-form code than some larger models.

**Facilitator Notes:**
- ⚡ ADVANCED — Skip for non-engineering audiences. For ML engineers: this is conceptually important because it breaks the "next-token prediction is all you need" assumption.
- Connection: This enables self-speculative decoding (the model can verify its own draft predictions).
- Time: 3 minutes

---

### [NEW 2026] Slide: The Frontier Convergence — What Actually Differentiates Models Now?
**Insert after:** Model landscape table
**Format:** Discussion / analysis

**Content:**

**An uncomfortable truth for mid-2026:** On standard benchmarks (MMLU, HumanEval, MATH), frontier models have nearly converged. GPT-5.5, Claude Opus 4, Gemini 3.1, and DeepSeek V4 all score within 2–5% of each other on most tasks.

**So what actually differentiates them now?**

| Differentiation Factor | Who Leads | Why It Matters |
|---|---|---|
| **Reasoning depth** | o3, Claude Extended Thinking | Complex multi-step problems |
| **Instruction following precision** | Claude | Enterprise reliability, agentic tool calling |
| **Code generation** | Claude, DeepSeek | Agent coding, software engineering |
| **Long-context reliability** | Gemini | Document processing, large codebases |
| **Speed / cost** | DeepSeek, GPT-4o-mini | High-volume production workloads |
| **Multimodal depth** | GPT-4o, Gemini | Vision, audio, video understanding |
| **Safety / steerability** | Claude | Enterprise compliance, sensitive domains |
| **Openness / customisability** | DeepSeek, Llama, Qwen | On-prem, fine-tuning, modification |

**The practical implication:** "Which model is best?" is no longer answerable without the context of "for what task, at what scale, under what constraints?"

**The new selection criteria:**
1. What modalities do I need?
2. What's my latency tolerance?
3. What's my cost ceiling per query?
4. Do I need reasoning or speed?
5. Do I need on-prem / data sovereignty?
6. Do I need fine-tuning / modification rights?

**Facilitator Notes:**
- This reframes the conversation from "which model is best" to "which model is right for my context" — a much more mature question.
- Discussion prompt: "If all models are similarly capable, what becomes the competitive advantage?" (Answer: how you use them — harness engineering, agent design, data quality)
- Time: 4 minutes

---

### [NEW 2026] Slide: Open-Weight Models — The Viability Inflection Point
**Insert after:** Frontier convergence slide
**Format:** Market landscape + decision guide

**Content:**

**The open-weight revolution (2025–2026):**

Open-weight models went from "interesting but weaker" to "frontier-competitive for most tasks":

| Model | Release | Quality vs. GPT-4 | Key Feature |
|---|---|---|---|
| Llama 4 Maverick | 2025 | ~98% on MMLU | 400B MoE, 17B active, 10M context |
| DeepSeek V3/V4 | 2025–2026 | ~99% on coding | 671B MoE, $5.5M training cost |
| Qwen 3 | 2025 | ~97% multi-lingual | Best non-English open model |
| MiniMax M3 | May 2026 | ~96% general | First open 1M-context + multimodal + coding |
| Mistral Large 3 | 2025 | ~95% enterprise | Strong EU/enterprise governance |

**When to choose open-weight:**
- ✅ Data sovereignty / on-premise requirements
- ✅ Need to fine-tune or customise deeply
- ✅ High-volume workloads where API costs are prohibitive
- ✅ Reproducibility and auditability requirements
- ✅ Edge / embedded / offline deployment

**When to stay with closed-source:**
- ✅ Need the absolute frontier (reasoning models)
- ✅ Don't want to manage infrastructure
- ✅ Need the latest capabilities immediately (APIs update faster)
- ✅ Small-scale usage where API costs are trivial

**Facilitator Notes:**
- Key message: "The gap has closed. For most enterprise use cases, open-weight models are now a genuine strategic choice, not a compromise."
- Connect to Module 9 (fine-tuning): "And because they're open, you can fine-tune them for your domain — something you can't do with GPT-5.5."
- Common question: "Open-weight vs open-source?" — Most are open-weight (weights available, restrictive license). Truly open-source (Apache 2.0, MIT) is rarer. License matters for commercial use.
- Time: 4 minutes

---

### [NEW 2026] Slide: Tokenisers — Why They Still Matter (And What Changed)
**Insert after:** "Tokens, embeddings, context windows" section
**Format:** Practical concept update

**Content:**

**Why students still need to understand tokenisation in 2026:**
- Pricing is per-token (and tokeniser efficiency varies 30%+ across models)
- Context window limits are in tokens (not words, not characters)
- Non-English languages are tokenised less efficiently (same content = more tokens)
- Code tokens ≠ prose tokens ≠ JSON tokens

**What changed (2025–2026):**
- **Tiktoken updates:** GPT-4o uses a more efficient tokeniser than GPT-4 (same text = fewer tokens = cheaper)
- **Byte-level tokenisers:** Some models (Gemma, T5) tokenise at byte level — eliminates unknown token problems entirely
- **Multimodal tokenisers:** Images are now tokenised into fixed-size patches (e.g., 1 image ≈ 1,170 tokens in GPT-4o)
- **Audio tokenisers:** 1 minute of audio ≈ 1,500–3,000 tokens depending on model

**Practical cost implication:**
```
Same 1000-word document:
  GPT-4:       ~1,500 tokens
  GPT-4o:      ~1,200 tokens (20% more efficient tokeniser)
  Claude 3:    ~1,300 tokens
  DeepSeek V3: ~1,100 tokens

Same document with GPT-4o + 1 image:
  Text: 1,200 tokens + Image: 1,170 tokens = 2,370 total
```

**Facilitator Notes:**
- Quick practical exercise: Use tiktoken (Python) or the OpenAI tokeniser playground to tokenise the same text across different models. Show the cost difference.
- Key insight: "Choosing a model with a better tokeniser can save you 20% on every API call — for free."
- Time: 3 minutes

---

### [NEW 2026] Slide: Understanding Attention Patterns — Why Models Fail on Certain Tasks
**Insert after:** KV Cache slide or Transformer architecture section
**Format:** Conceptual + failure analysis
**⚡ ADVANCED**

**Content:**

**The core mechanism that enables and limits LLMs: self-attention**

Every token can "attend to" every other token. But in practice, attention is not uniform:
- **Attention sinks:** First few tokens receive disproportionate attention regardless of content
- **Recency bias:** Recent tokens get more attention weight than older ones
- **Middle neglect:** Tokens in the middle of long contexts receive less attention (the "Lost in the Middle" phenomenon — 30%+ performance drop)

**Practical implications:**
1. Put important instructions at the START and END of your prompt
2. In RAG: put the most relevant chunk FIRST, not in order of retrieval score
3. In agents: periodically "re-inject" critical information to avoid it being lost

**New attention variants (2025–2026):**
| Variant | What It Changes | Benefit |
|---|---|---|
| Sliding Window Attention | Only attend to last N tokens | Faster, handles very long sequences |
| Ring Attention | Distribute long-context across multiple devices | Enables 10M+ context |
| Multi-Head Latent Attention (MLA) | Compress KV into latent space | 75–93% memory reduction |
| Sparse Attention (MiniMax) | Only attend to selected tokens | Faster at very long lengths |

**Facilitator Notes:**
- ⚡ ADVANCED — This slide explains WHY models fail in specific ways. For beginners, summarise as: "Models pay more attention to the beginning and end of what you give them. Put important stuff there."
- Connect to Module 7 (Prompt Engineering): This is the technical reason behind many prompt engineering best practices.
- Connect to Module 8 (RAG): This explains why retrieval order matters and why re-ranking helps.
- Time: 4 minutes

---

### [NEW 2026] Slide: Production Serving Stacks — What's Actually Running in 2026
**Insert after:** Inference economics or deployment section
**Format:** Landscape table + architecture

**Content:**

**The standard production inference stack (2026):**

```
┌────────────────────────────────────────────┐
│  Application Layer (your code)             │
├────────────────────────────────────────────┤
│  Load Balancer / Model Router              │
│  (routes by complexity/cost/latency)       │
├────────────────────────────────────────────┤
│  Inference Server                          │
│  vLLM │ TGI │ TensorRT-LLM │ SGLang       │
│  (PagedAttention, continuous batching,     │
│   speculative decoding, KV cache mgmt)     │
├────────────────────────────────────────────┤
│  Hardware                                  │
│  NVIDIA H100/H200 │ AMD MI300X │ AWS       │
│  Trainium2 │ Inferentia3 │ Gaudi 3        │
├────────────────────────────────────────────┤
│  Managed alternatives: AWS Bedrock,        │
│  Azure OpenAI, Google Vertex AI            │
└────────────────────────────────────────────┘
```

**Inference framework comparison (mid-2026):**

| Framework | Strengths | Used By |
|---|---|---|
| **vLLM** | PagedAttention, highest throughput, broad model support | Industry standard |
| **SGLang** | RadixAttention, structured output, best for agentic | Growing fast |
| **TensorRT-LLM** | NVIDIA-optimized, lowest latency on NVIDIA GPUs | Enterprise |
| **TGI** | Hugging Face native, easiest to deploy | Quick prototyping |

**Facilitator Notes:**
- "You don't need to build this yourself — but you need to know it exists so you can have an intelligent conversation with your platform team."
- For AWS-focused audiences: "Module 10 will cover Bedrock and SageMaker in depth. This slide shows you what's under the hood."
- Time: 3 minutes

---

### [NEW 2026] Slide: The Model Development Pipeline in 2026
**Insert after:** Training section (pre-training/fine-tuning/RLHF)
**Format:** Updated process flow

**Content:**

The full pipeline from raw compute to deployed model has evolved:

```
STAGE 1: PRE-TRAINING (months, $1M–$100M+)
  Web crawl + books + code + multilingual data
  → Standard next-token prediction (+ MTP)
  → Produces: base model (no alignment, no safety)

STAGE 2: POST-TRAINING ALIGNMENT (weeks, $100K–$1M)
  ├── Supervised Fine-Tuning (SFT) on instruction data
  ├── Preference optimization (DPO/GRPO/RLHF)
  ├── Process Reward Model training (for reasoning)
  ├── Safety training (Constitutional AI / red-teaming)
  └── Produces: aligned chat model

STAGE 3: SPECIALISATION (days–weeks, $1K–$100K)
  ├── Domain fine-tuning (LoRA/QLoRA on your data)
  ├── Distillation from larger model
  ├── Continued pre-training on domain corpus
  └── Produces: your custom model

STAGE 4: DEPLOYMENT OPTIMIZATION (hours–days)
  ├── Quantization (GPTQ, AWQ, GGUF for 4/8-bit)
  ├── Speculative decoding setup
  ├── KV cache configuration
  ├── Serving framework deployment
  └── Produces: production endpoint
```

**What's new vs. the original module:**
- MTP as a training objective (Stage 1)
- DPO/GRPO replacing RLHF as default (Stage 2)
- Process Reward Models for reasoning (Stage 2)
- Distillation as a mainstream technique (Stage 3)
- Quantization + speculative decoding as standard deployment (Stage 4)

**Facilitator Notes:**
- This slide replaces/extends the original "How LLMs are trained" content. Walk through each stage and note what's new with [NEW 2026].
- Key insight: "Most practitioners will work in Stages 3 and 4. You rarely pre-train from scratch. But understanding Stages 1 and 2 helps you choose models intelligently."
- Time: 5 minutes

---

### [NEW 2026] Slide: Key Numbers Every Practitioner Should Know (2026 Edition)
**Insert after:** Final section or before Knowledge Check
**Format:** Quick reference / cheat sheet

**Content:**

| Metric | Value (mid-2026) | Why It Matters |
|---|---|---|
| Frontier model MMLU score | 91–93% | Near-human, models converging |
| Context window standard | 1M tokens | But effective attention < full window |
| Context rot degradation | 30%+ in mid-window | Position matters for prompt design |
| Cheapest frontier API | $0.14/M input (DeepSeek Flash) | 200× cheaper than 2023 GPT-4 |
| Speculative decoding speedup | 2–4× | Free lunch for single-stream serving |
| MoE active ratio | 3–35% of total params | Why big models run cheaply |
| KV cache at 1M context (70B model) | 40+ GB | The real scaling bottleneck |
| Reasoning model cost premium | 4–17× vs. standard | Budget reasoning carefully |
| Reasoning model latency premium | 5–60× vs. standard | Not suitable for real-time chat |
| Open-weight quality gap to frontier | <3% on most benchmarks | Open is now a viable default |
| Training cost, frontier model | $50M–$500M+ | Still exclusive to major labs |
| Fine-tuning cost, LoRA on 70B | $100–$5,000 | Accessible to any team |
| Image tokens (1 image, GPT-4o) | ~1,170 tokens | Factor into multimodal costs |

**Facilitator Notes:**
- "Pin this slide. These are the numbers that let you sanity-check vendor claims and estimate costs without a calculator."
- Update these numbers every delivery — they shift quarterly.
- Great as a printed handout students can take away.
- Time: 2 minutes (quick reference, not deep discussion)

---

### [NEW 2026] Slide: Hands-On Activity Extension — Model Comparison Lab (Updated)
**Insert after:** Existing hands-on activity
**Format:** Lab activity

**Content:**

**Updated Lab: "Compare the Generations" (2026 Edition)**

**Objective:** Students directly experience the trade-offs between model tiers, reasoning modes, and cost.

**Setup required:**
- Access to: OpenAI API (GPT-4o-mini + GPT-4o + o3-mini), Anthropic API (Haiku + Sonnet + Sonnet with extended thinking), and one open-weight model via API (DeepSeek or Groq-hosted Llama)

**Instructions:**

1. **Task 1: Simple extraction** — Send the same invoice image to GPT-4o-mini, Claude Haiku, and DeepSeek. Compare: quality, speed, cost. (Expected: all perform similarly, huge cost difference)

2. **Task 2: Complex reasoning** — Send a multi-step logic puzzle to GPT-4o, o3-mini, and Claude Sonnet with/without extended thinking. Compare: answer quality, thinking process visibility, cost. (Expected: reasoning models dramatically better, but 10–20× more expensive)

3. **Task 3: Long-context** — Load a 50-page PDF and ask a specific question whose answer is on page 37. Compare: Gemini (2M context), GPT-4o (128K, may need RAG), DeepSeek (128K). (Expected: long-context model finds it directly; shorter models may miss it)

4. **Task 4: Structured output** — Ask for JSON extraction with a specific schema. Compare: with structured output mode ON vs. OFF. (Expected: structured mode never fails; free-form occasionally produces invalid JSON)

5. **Debrief:** Students fill in a decision matrix — which model for which use case, and why?

**Facilitator Notes:**
- Allow 15 minutes for the lab in a 75-min extended version, or assign as homework for the 60-min version.
- Pre-provision API keys. Estimated cost per student: ~$2–5 for the full lab.
- The "aha moment" is Task 2: students see a reasoning model genuinely solve something a standard model gets wrong.
- Time: 15 minutes (in extended version) or assign as post-module exercise

---

## Facilitator Update Brief

### 🎤 Top 3 Most Important Additions

1. **Reasoning Models & Test-Time Compute** (Slides 1–3) — This is the single biggest conceptual shift since transformers. Students WILL encounter reasoning models in their work. Without this content, they can't make informed model selection decisions or understand why some API calls cost 17× more than others.

2. **Mixture of Experts (MoE) & DeepSeek Architecture** (Slides 4–5) — Explains the economics that dominate the 2026 landscape. "How can open models compete with trillion-dollar companies?" is answered here. Without it, students can't evaluate open-weight options.

3. **Context Windows & Attention Patterns** (Slides 6, 14) — The "1M context" headline hides critical practical limitations (context rot, Lost in the Middle). Students building RAG or agent systems need to understand effective vs. advertised context capacity.

### 📝 What's Now Outdated in the Original Module

| Original Content | Status | How to Handle |
|---|---|---|
| "RLHF is how models are aligned" | Outdated as sole method | Keep RLHF as historical context, add "Beyond RLHF" slide showing DPO/GRPO/CAI as current standard |
| Model families table (if listing GPT-4, Claude 3, etc.) | Outdated names/specs | Replace entirely with the 2026 landscape table |
| Context windows described as "up to 200K" | Outdated | Update to 1M standard, add effective-vs-advertised distinction |
| Inference described generically | Insufficient | Add speculative decoding, KV cache, and model routing slides |
| "Multimodality" as a future trend | Now standard | Reframe as "native multimodal architecture" — describe how it works |

### ⏱️ Fitting Into 60 Minutes

**The honest answer:** With all new content, this module warrants **75–90 minutes**. 

**Option A — 60-minute standard delivery:**
- Keep original Transformer/Training content (15 min) but compress
- Add: Reasoning Models + Two Scaling Laws (8 min)
- Add: MoE + DeepSeek case study (7 min)  
- Add: Context windows update + context rot (5 min)
- Add: Updated model landscape table (5 min)
- Add: Speculative decoding + inference economics (5 min)
- Keep: Hands-on activity (10 min)
- Keep: Knowledge check (5 min)
- **Mark as SKIP FOR BEGINNERS:** MTP, KV Cache deep-dive, Attention patterns, Production serving stacks

**Option B — 90-minute extended delivery:**
- Full original content + ALL new slides
- Extended hands-on lab (15 min instead of 10)
- Discussion: "The Frontier Convergence" slide with group activity

### 🛠️ New Tools/Accounts/Demos to Set Up

1. **OpenAI API account** with access to o3-mini (for reasoning model demo)
2. **Anthropic API** with extended thinking enabled (for visible thinking demo)
3. **DeepSeek API** (free tier available — for cost comparison demo)
4. **tiktoken Python library** (for tokeniser comparison exercise)
5. **OpenAI Tokenizer Playground** (https://platform.openai.com/tokenizer) — browser-based
6. **A long PDF (50+ pages)** for the context window comparison demo
7. **A needle-in-a-haystack test script** for demonstrating context rot at different positions

---

*Module 03 Update — Version 2026.07 — AI & Agentic AI Training Programme*
