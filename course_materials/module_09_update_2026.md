# Module 09 — Fine-Tuning, Distillation & Model Customisation
## [2026 UPDATE] New Content, Gap Analysis & Facilitator Delivery Notes

---

## STEP 2: GAP ANALYSIS

The original module was written from a mid-2024 perspective. Here's what's now outdated or missing:

1. **GRPO and RL-based training entirely missing** — Group Relative Policy Optimization (DeepSeek-R1, published Nature Sep 2025) is now the standard post-training technique for reasoning. The module has no coverage of RL-based fine-tuning.

2. **Preference optimisation landscape is incomplete** — Original covered only RLHF and basic fine-tuning. DPO, ORPO, SimPO, KTO, and their trade-offs are now standard production tools that students will encounter immediately.

3. **The "Four-Stage Pipeline" is the new production standard** — The 2026 consensus is: Continued Pre-Training → LoRA SFT → Preference Alignment (DPO/GRPO) → Rejection-Sampled SFT. The original module has no multi-stage pipeline concept.

4. **Continued Pre-Training (CPT/DACPT) not covered** — Domain-adaptive continued pre-training is distinct from fine-tuning and is the first step most production teams take. The module jumps straight to SFT.

5. **Model merging is entirely absent** — TIES, DARE, SLERP, and evolutionary merging allow combining fine-tuned capabilities without additional training. This is now a standard production technique.

6. **Speculative decoding not covered** — Now a production standard (vLLM, TensorRT-LLM native support), achieving 2–3× inference speedup. Students will encounter this in deployment.

7. **Small Language Models (SLMs) revolution is missing** — Phi-4, Gemma 3/4, Llama 3.2 1B/3B, Qwen 2.5/3, Ministral — the 2026 consensus is "a well-trained 7B handles 90% of production use cases at 1% the cost."

8. **Synthetic data generation for fine-tuning now has clear best practices** — Four distinct use cases (training data, eval sets, edge-case augmentation, privacy substitution) with different failure modes.

9. **Tooling has shifted dramatically** — Unsloth (2–5× faster, 80% less VRAM, no-code UI), Axolotl for multi-GPU, MLX-LoRA for Mac, TRL for control. Original module doesn't mention any 2025-2026 tools.

10. **The decision framework has evolved** — "Prompt first, retrieve for knowledge, fine-tune for behavior" with a new fourth option: fine-tune + agent. The original binary framing is outdated.

---

## STEP 3: NEW SLIDES

---

### [NEW 2026] Slide: The 2026 Model Customisation Landscape
**Insert after:** Section 1 (When to Fine-Tune vs. Prompt vs. RAG)
**Format:** Concept explanation with updated decision tree

The model customisation landscape in 2026 is no longer a binary choice. It's a layered stack:

```
┌────────────────────────────────────────────────┐
│  LAYER 5: Agentic (tools + memory + actions)   │ ← New option
├────────────────────────────────────────────────┤
│  LAYER 4: Preference Alignment (DPO/GRPO)      │ ← Was "RLHF"
├────────────────────────────────────────────────┤
│  LAYER 3: Supervised Fine-Tuning (LoRA SFT)    │ ← Behaviour
├────────────────────────────────────────────────┤
│  LAYER 2: Continued Pre-Training (CPT/DACPT)   │ ← Knowledge
├────────────────────────────────────────────────┤
│  LAYER 1: RAG + Prompt Engineering             │ ← Context
└────────────────────────────────────────────────┘
```

**The 2026 Rule:** "Prompt first, retrieve for knowledge, fine-tune for behaviour, align for quality, agent for action."

Most production implementations combine multiple layers. The question is not "which one?" but "which combination, for which failure mode?"

| Failure Mode | Layer to Apply |
|---|---|
| Model doesn't know X | RAG (Layer 1) or CPT (Layer 2) |
| Model knows X but answers wrong format | SFT (Layer 3) |
| Model answers correctly but tone/style is off | Preference alignment (Layer 4) |
| Model needs to take real-world actions | Agentic layer (Layer 5) |
| Model hallucinates on domain content | RAG + eval loops |

**Facilitator Notes:**
- 🎤 "The biggest shift since 2024 is that fine-tuning is no longer one thing — it's a 4-stage pipeline. Let me walk you through each stage."
- Common question: "When do I really need CPT vs just RAG?" Answer: "CPT for durable domain vocabulary and reasoning patterns. RAG for changing facts."
- Time: 5 minutes
- Emphasise for beginners: the decision tree. For advanced: the failure-mode mapping.

---

### [NEW 2026] Slide: The Four-Stage Production Pipeline
**Insert after:** The 2026 Model Customisation Landscape
**Format:** Process flow / architecture diagram

The production consensus for domain-specialised LLMs in 2026:

```
Stage 1          Stage 2        Stage 3           Stage 4
┌─────────┐    ┌─────────┐    ┌──────────┐    ┌──────────────┐
│  DACPT  │ →  │LoRA SFT │ →  │  DPO /   │ →  │ Rejection-   │
│         │    │         │    │  GRPO    │    │ Sampled SFT  │
└─────────┘    └─────────┘    └──────────┘    └──────────────┘
 Knowledge      Behaviour      Quality         Multi-turn
 (what it       (how it        (aligned to     coherence
 knows)         responds)      preferences)    (final polish)
```

**What each stage fixes:**

| Stage | Input | Fixes | Typical Compute |
|---|---|---|---|
| DACPT | Domain corpus (5B–50B tokens) | Model doesn't understand domain terminology/patterns | 2–4× H100, 24–72h |
| LoRA SFT | 1K–10K curated examples | Model knows domain but produces wrong format/structure | 1× H100, 1–3h |
| DPO/GRPO | Preference pairs or reward signal | Model produces correct format but quality/tone varies | 1–2× H100, 2–6h |
| Rejection-Sampled SFT | Synthetic multi-turn filtered outputs | Multi-turn coherence degrades; final polish | 1× H100, 1–2h |

**Key insight:** "Skip a stage and it shows up as a measurable regression on your eval suite."

**Facilitator Notes:**
- 🎤 "This pipeline comes from the convergent practice of teams at Meta (Llama), DeepSeek, Alibaba (Qwen), and dozens of production teams. It's not theoretical — it's what actually ships."
- Common question: "Do I always need all 4 stages?" Answer: "No — many teams need only stages 2–3. Stage 1 (CPT) is for deep domain specialisation. Stage 4 is polish."
- Time: 5 minutes

---

### [NEW 2026] Slide: Continued Pre-Training (DACPT) — Deep Dive
**Insert after:** The Four-Stage Production Pipeline
**Format:** Technical concept with hyperparameters

**What it is:** Same causal LM loss as original pre-training, run on a mixture of domain corpus + 5–15% general data replay to prevent catastrophic forgetting.

**When to use it:**
- Domain has specialised vocabulary (legal, medical, financial, scientific)
- Model needs deep reasoning patterns specific to your domain
- You have >5B tokens of high-quality domain text

**Hyperparameters that matter:**

| Parameter | Recommended Range | Why |
|---|---|---|
| Learning rate | 1e-5 to 3e-5 | 10–100× lower than original pre-training |
| Replay ratio | 5–15% general data | Below 5% → catastrophic forgetting; above 15% → dilution |
| Token budget | 5B–50B tokens | Below 1B is just extended SFT — call it what it is |
| Sequence length | Full model context (8K–32K) | Pack documents with boundary attention masking |
| Optimizer | AdamW, weight decay 0.1, grad clip 1.0 | Standard — don't get creative here |

**Success criteria:** In-domain validation perplexity drops 30–60% with ≤2% regression on general-capability benchmarks (MMLU, GSM8K). If >5% MMLU drop → replay ratio too low or LR too high.

**Data quality is the dominant predictor:**
- OCR with layout-aware extraction (Marker, Nougat) for scanned PDFs
- Near-duplicate removal (MinHash/SimHash)
- PII redaction (model-based, not regex alone)
- Quality filtering (fastText classifier on hand-labelled sample)

**Facilitator Notes:**
- 🎤 "Most teams under-invest in this stage. They jump to SFT and wonder why the model doesn't understand their domain."
- ⚡ ADVANCED — The hyperparameter table is for engineers. For PMs, focus on the "when to use" criteria.
- Common question: "How is this different from just giving the model more context?" Answer: "CPT changes what the model *knows at the weight level*. RAG shows it information at inference time."
- Time: 5 minutes

---

### [NEW 2026] Slide: GRPO — Group Relative Policy Optimization
**Insert after:** Fine-tuning methods section
**Format:** Technical concept with diagram

**The breakthrough:** DeepSeek-R1 (Nature, Sep 2025) proved you can train a model to match OpenAI o1-level reasoning using pure RL without labelled data, for ~$294K in compute.

**How GRPO works:**

```
Traditional PPO:                    GRPO:
┌────────────┐                     ┌────────────┐
│ Policy     │                     │ Policy     │
│ Model      │                     │ Model      │
└──────┬─────┘                     └──────┬─────┘
       │                                  │
       ▼                                  ▼
┌────────────┐                     Generate G responses
│ Value      │ ← expensive         per prompt (group)
│ Function   │   to train                 │
│ Model      │                            ▼
└────────────┘                     Rank within group
                                   (no value model needed!)
                                          │
                                          ▼
                                   Compute relative advantage
                                   from group scores
```

**Key innovation:** GRPO eliminates the value function model entirely. Instead, it generates a *group* of G responses for each prompt, ranks them using a reward signal (verifiable answer, judge model, or binary outcome), and computes relative advantages within the group.

**Why it matters for practitioners:**
- 50% less memory than PPO (no value model)
- Simpler to implement (no critic training instability)
- Works with verifiable rewards (math, code, structured tasks)
- Now a "standard component in many commercial LLM APIs" (2026)

**Available implementations:** TRL (Hugging Face), Unsloth GRPO, OpenRLHF, DeepSpeed-RLHF

**Facilitator Notes:**
- 🎤 "GRPO is what made DeepSeek-R1 possible. It's now the default RL algorithm for reasoning improvement. Published in Nature — that's how significant this is."
- ⚡ ADVANCED — The mechanics of group scoring are for engineers. For PMs: "There's a new way to make models reason better that doesn't require expensive labelling."
- Common question: "Can I use GRPO on my own model?" Answer: "Yes — Unsloth and TRL both support it. You need a verifiable reward signal."
- Time: 5 minutes

---

### [NEW 2026] Slide: The Preference Alignment Zoo
**Insert after:** GRPO slide
**Format:** Comparison table

The post-training alignment landscape has exploded since 2024. Here's what practitioners actually use:

| Algorithm | Key Idea | When to Use | Complexity |
|---|---|---|---|
| **DPO** (Direct Preference Optimization) | Train directly on preference pairs without RL | Default first choice; paired preference data available | Low |
| **GRPO** (Group Relative Policy Optimization) | RL with group-relative advantages, no value model | Reasoning tasks with verifiable rewards (math, code) | Medium |
| **SimPO** (Simple Preference Optimization) | Reference-free reward; no reference model needed | When you want simpler DPO with better AlpacaEval scores | Low |
| **KTO** (Kahneman-Tversky Optimization) | Works with unpaired feedback (just good/bad labels) | When you can't get paired comparisons easily | Low |
| **ORPO** (Odds Ratio Preference Optimization) | Unified SFT + preference alignment in single stage | When you want fewer training stages | Low |
| **Online DPO** | DPO with fresh on-policy samples during training | When static preference data isn't enough | Medium |
| **PPO** (Proximal Policy Optimization) | Full RL with value model | Maximum control; complex reward functions | High |

**The oxRL finding (March 2026, 240 training runs):**
> "Algorithm rankings are unstable across scale. At 1.5B, GRPO tops all methods. By 7B, SimPO becomes the best — a complete ranking inversion driven by model scale."

**Practical guidance:** Start with DPO. Move to GRPO for reasoning. Don't over-engineer your first alignment pass — vanilla DPO with good data beats 20 DPO variants.

**Facilitator Notes:**
- 🎤 "You'll see all of these in blog posts and papers. The honest answer is: DPO is still the best default starting point. GRPO when you need reasoning. The rest are useful in specific situations."
- Common question: "Which one should I use?" Answer: "DPO first. If you have verifiable rewards (math, code, structured extraction), try GRPO."
- Time: 4 minutes

---

### [NEW 2026] Slide: Model Merging — Combine Capabilities Without Training
**Insert after:** Model Distillation section
**Format:** Technical concept with methods comparison

**What is it?** Combining the weight tensors of 2+ fine-tuned models into a single checkpoint — no gradient descent, no new data, no GPU clusters.

**Why it works:** After fine-tuning, a model's weights encode adaptation as a perturbation on the base. If two fine-tunes start from the same base and their perturbations don't contradict, you can average them.

**The methods:**

| Method | How It Works | Best For |
|---|---|---|
| **Linear (Task Arithmetic)** | Average weight differences from base | Simple; first try |
| **SLERP** | Spherical linear interpolation between two models | Smoothest blending; 2 models only |
| **TIES** | Trim small changes, resolve sign conflicts, merge | Reducing interference between many models |
| **DARE** | Randomly drop most delta parameters, rescale survivors | Sparse specialisation; preserves generality |
| **Evolutionary** | Genetic algorithm optimises merge weights per layer | Maximum quality; highest compute |

**Production use cases:**
- Combine "coding expert" + "instruction follower" + "safety-aligned" into one deployment
- Merge multilingual adapters without quality degradation
- Combine task-specific LoRAs into a single model
- Bias mitigation: SLERP at moderate weights consistently reduces bias while maintaining performance

**Tools:** MergeKit (standard), Model Merge extension in Unsloth Studio

**Facilitator Notes:**
- 🎤 "Model merging is the 'lazy but effective' approach to multi-skill models. No training, no data, just math on weights."
- Common question: "How well does it actually work?" Answer: "Surprisingly well for 2 models. Quality degrades with 4+. Always eval after merging."
- ⚡ ADVANCED — The methods table is for engineers. For beginners: "You can combine two fine-tuned models into one without retraining."
- Time: 4 minutes

---

### [NEW 2026] Slide: Speculative Decoding — 2–3× Faster Inference
**Insert after:** Model Merging slide
**Format:** Technical concept with production guidance

**The problem:** LLM inference is bottlenecked by sequential token generation. Each token requires a full forward pass.

**The solution:** Use a small "draft" model to propose multiple tokens in parallel, then verify them with the larger "target" model in one batch forward pass.

```
Traditional:  T₁ → T₂ → T₃ → T₄ → T₅  (5 forward passes)

Speculative:  [Draft proposes T₁T₂T₃T₄T₅] → [Target verifies in 1 pass]
              Accept T₁T₂T₃, reject T₄T₅ → regenerate from T₄
              Net: 2 passes instead of 5
```

**Production status (2026):**
- Native support in vLLM and TensorRT-LLM
- NVIDIA demonstrated 3.6× throughput on H200 GPUs
- Achieves 2–3× speedup with zero quality loss (mathematically identical output)
- Now standard for production serving of 70B+ models

**When to use:**
- ✅ Latency-sensitive applications (chatbots, real-time)
- ✅ 70B+ models where inference cost dominates
- ✅ Tasks with high acceptance rates (structured/predictable outputs)
- ❌ Not helpful for very small models (draft overhead > benefit)
- ❌ Not helpful at high batch sizes (already GPU-saturated)

**Facilitator Notes:**
- 🎤 "This is free performance. Same outputs, faster inference. If you're serving a large model, you should be using speculative decoding."
- Common question: "Where do I get the draft model?" Answer: "Use a smaller model from the same family (e.g., Llama 3.2 1B drafts for Llama 3.1 70B), or distil your own."
- Time: 4 minutes

---

### [NEW 2026] Slide: Small Language Models (SLMs) — When Smaller Wins
**Insert after:** Speculative Decoding slide
**Format:** Comparison table with decision framework

**The 2026 consensus:** "A well-trained 7B model handles 90% of production use cases at 1% of the cost."

**The SLM lineup:**

| Model | Params | Strengths | Runs On |
|---|---|---|---|
| **Phi-4** | 14B | Reasoning, code, math — approaches GPT-4 level | Single GPU |
| **Gemma 3/4** | 2B–27B | Multilingual, instruction following, distillation target | Edge to cloud |
| **Llama 3.2** | 1B–3B | Fastest; edge deployment; mobile | Phone/laptop |
| **Qwen 2.5/3** | 0.5B–72B | Best multilingual; great for Asian languages | Flexible |
| **Ministral** | 3B–8B | Long context; efficient attention | Single GPU |

**SLMs for agentic AI:**
- Classification and routing: 2B model routes requests to specialist agents
- Tool selection: 3B model decides which tool to call
- Extraction: 7B model pulls structured data from documents
- Guard model: 1B model screens inputs for injection attacks

**The distillation path:**
1. Use frontier model (Claude/GPT-4/Gemini) as teacher
2. Generate high-quality outputs on your task
3. Fine-tune SLM on teacher outputs
4. Result: 90%+ of teacher quality at 1% of inference cost

**Facilitator Notes:**
- 🎤 "The most over-looked production pattern is distilling a big model into a small one for your specific use case. Most tasks don't need GPT-4."
- Common question: "Won't a small model hallucinate more?" Answer: "On your specific task, after distillation, usually not. It's been trained on correct outputs for exactly that task."
- Time: 4 minutes

---

### [NEW 2026] Slide: Synthetic Data for Fine-Tuning — The 2026 Playbook
**Insert after:** Dataset preparation section
**Format:** Framework with use cases

**Four distinct use cases (each with different failure modes):**

| Use Case | What You Generate | Quality Signal | Common Failure Mode |
|---|---|---|---|
| **Training data** | Full instruction/response pairs from teacher model | Human review of seed set; consistency checks | Model collapse from self-referential generation |
| **Eval sets** | Test cases with known correct answers | Ground truth validation | Eval set too easy; doesn't test edge cases |
| **Edge-case augmentation** | Rare scenario data to fill distribution gaps | Coverage metrics; failure analysis | Over-fitting to synthetic artefacts |
| **Privacy substitution** | Synthetic versions of PII-containing real data | Statistical fidelity; utility preservation | Losing the distributional properties that matter |

**The 2026 best practice stack:**
1. Seed set: 50–200 hand-curated, gold-standard examples
2. Teacher generation: Use strongest available model (Claude 3.7, GPT-4o) with structured prompts
3. Diversity injection: Vary persona, difficulty, format, edge cases
4. Quality filtering: LLM-as-judge + rule-based checks + human spot-check (10%)
5. Decontamination: Ensure no test set leakage into training data

**Critical finding (ACL 2026):** Diversity of synthetic data matters more than volume. 2K diverse examples > 20K repetitive ones.

**The anti-pattern:** Don't replace real data with synthetic — accumulate real data alongside it. Synthetic for bootstrapping; real for long-term quality.

**Facilitator Notes:**
- 🎤 "Everyone is using synthetic data in 2026. The question is not whether to use it, but how to use it without introducing model collapse or quality degradation."
- Common question: "Isn't training on AI outputs just model collapse?" Answer: "Only if you do it naively. With proper diversity, filtering, and real data mixing, it works."
- Time: 4 minutes

---

### [NEW 2026] Slide: The Unsloth Revolution — Fine-Tuning Democratised
**Insert after:** Tools and implementation section
**Format:** Tool overview with demo guidance

**What Unsloth does:** Drop-in replacement for HuggingFace Transformers with hand-optimised Triton kernels.

**The numbers:**
- 2–5× faster training
- 60–80% less VRAM
- Zero accuracy loss
- LoRA, QLoRA, full fine-tune, and now GRPO all supported
- No-code UI via Unsloth Studio (June 2026)

**What this means in practice:**

| Model Size | Standard | With Unsloth |
|---|---|---|
| 7B QLoRA | 1× A100 (80GB), 2h | 1× RTX 4090 (24GB), 40min |
| 13B QLoRA | 2× A100, 4h | 1× A100, 1.5h |
| 70B QLoRA | 8× A100, 12h | 2× H100, 3h |

**The 2026 fine-tuning toolkit:**

| Tool | Best For | Key Feature |
|---|---|---|
| **Unsloth** | Single-GPU LoRA/QLoRA; prototyping; GRPO | Speed + memory efficiency |
| **Axolotl** | Multi-GPU production training | Config-driven; reproducible |
| **TRL** (HuggingFace) | Maximum control; custom training loops | Most flexible; reference implementation |
| **MLX-LoRA** | Mac fine-tuning (M1/M2/M3/M4) | Apple Silicon native |
| **LLaMA-Factory** | GUI-based; non-engineers | Low code; 100+ model support |

**Facilitator Notes:**
- 🎤 "If you tried fine-tuning in 2023 and it was painful and expensive — try again. Unsloth has made it a one-command, one-GPU operation."
- Demo opportunity: Show a 7B fine-tune on a free Colab T4 GPU in real-time (~20 min)
- Time: 4 minutes

---

### [NEW 2026] Slide: Rejection-Sampled SFT — The Final Polish Stage
**Insert after:** Preference Alignment section
**Format:** Technical concept

**What it is:** Generate N outputs from your model, filter using a reward model or judge, keep only the best, and do a final SFT pass on those high-quality outputs.

**Why it exists:** Even after DPO/GRPO, multi-turn conversations can still degrade. Rejection sampling catches this:

```
For each prompt in your eval set:
  1. Generate N=8 responses from your aligned model
  2. Score each with reward model or LLM-as-judge
  3. Keep top-K (usually K=1 or K=2)
  4. Fine-tune on the curated (prompt, best_response) pairs
```

**When to use:**
- Multi-turn coherence issues after DPO
- Model performance varies wildly across runs (high variance)
- You want to "self-distil" — the model teaches itself from its own best outputs

**Key insight:** This is self-play for language models. The model generates, judges, and learns from its own best behaviour.

**Facilitator Notes:**
- 🎤 "Think of this as the 'quality assurance' pass. The model already knows how to do the task — we're just removing the bad luck outputs."
- ⚡ ADVANCED — This is typically Stage 4 and optional for most use cases. Essential for production chatbots.
- Time: 3 minutes

---

### [NEW 2026] Slide: When NOT to Fine-Tune — The Counter-Arguments
**Insert after:** Rejection-Sampled SFT
**Format:** Discussion / common mistakes

**The 2026 anti-patterns:**

| Anti-Pattern | Why It Fails | What to Do Instead |
|---|---|---|
| Fine-tuning for knowledge injection | Weights are bad at storing facts; catastrophic forgetting | Use RAG |
| Fine-tuning when you have <100 examples | Overfitting; no generalisation | Prompt engineer with few-shot |
| Fine-tuning to fix hallucinations | FT doesn't fix model's tendency to confabulate | RAG + eval loops + guardrails |
| Fine-tuning every week as data changes | Too expensive; weights go stale | RAG for changing data; FT for stable behaviour |
| Fine-tuning without an eval suite | "It feels better" isn't a signal | Build evals BEFORE fine-tuning |

**The updated decision tree:**

```
Does the problem require new KNOWLEDGE or new BEHAVIOUR?
├── Knowledge → RAG (or CPT if knowledge is stable and deep)
└── Behaviour → Fine-tune
    ├── Is the behaviour consistent (format, style, structure)?
    │   └── Yes → LoRA SFT on 1K–10K examples
    └── Does quality vary despite correct format?
        └── Yes → Add preference alignment (DPO/GRPO)
```

**The layering principle:** "Most production implementations combine multiple approaches. The question is which combination, for which failure mode."

**Facilitator Notes:**
- 🎤 "Before you fine-tune, make sure you're solving the right problem. Half of 'fine-tuning projects' should actually be RAG projects or better prompting."
- This slide often generates the most discussion. Allow 2–3 min for questions.
- Time: 4 minutes

---

### [NEW 2026] Slide: LoRA Adapters in Production — Multi-Tenant Serving
**Insert after:** PEFT section
**Format:** Architecture concept

**The production pattern:** Serve one base model with multiple LoRA adapters hot-swapped per request.

```
                    ┌─────────┐
Customer A ────→   │         │ ← LoRA Adapter A (legal domain)
                    │  Base   │
Customer B ────→   │  Model  │ ← LoRA Adapter B (medical domain)  
                    │  (70B)  │
Customer C ────→   │         │ ← LoRA Adapter C (finance domain)
                    └─────────┘
```

**Why this matters:**
- One GPU cluster serves many customers
- Each adapter is tiny (50–200MB vs 140GB base)
- Hot-swap in milliseconds (no model reload)
- Each customer gets customised behaviour without dedicated infrastructure

**Supported by:** vLLM (LoRAX), Predibase, Amazon SageMaker Multi-Adapter Endpoints, Anyscale

**Cost implications:** 10 fine-tuned models as a service costs the same as 1 base model + adapter storage.

**Facilitator Notes:**
- 🎤 "This is how AI-as-a-service companies actually deploy. One base, many adapters. It's the economics that make fine-tuning viable at scale."
- Common question: "Can adapters interfere with each other?" Answer: "No — each request uses exactly one adapter. They share the base but don't interact."
- Time: 3 minutes

---

### [NEW 2026] Slide: Evaluating Fine-Tuned Models — The 2026 Stack
**Insert after:** Evaluating custom models section
**Format:** Updated framework

**The eval hierarchy (most to least reliable):**

| Level | Method | What It Measures | Cost |
|---|---|---|---|
| 1 | **Task-specific automated metrics** | Exact match, F1, BLEU/ROUGE, pass@k for code | Free |
| 2 | **LLM-as-judge** (strong model grades weaker) | Quality, helpfulness, safety, instruction following | Low |
| 3 | **A/B testing in production** | Real user preference between old and new model | Medium |
| 4 | **Human expert evaluation** | Domain-specific correctness, nuance, trust | High |
| 5 | **Red team testing** | Safety, adversarial robustness, edge cases | High |

**The "eval before you train" principle:**
1. Build your eval suite FIRST (before any fine-tuning)
2. Measure baseline (prompt engineering or RAG)
3. Fine-tune and measure improvement on same evals
4. If improvement < 5%... you probably didn't need to fine-tune

**New tools (2026):**
- **RAGAS v2** — automated RAG and generation quality metrics
- **Inspect AI** (UK AISI) — framework for systematic model evaluations
- **OpenAI Evals** — structured eval framework, open source
- **Braintrust** — production eval platform with versioning

**Facilitator Notes:**
- 🎤 "The #1 mistake in fine-tuning projects: training first, evaluating after. Flip it. Evals first, then train."
- Time: 3 minutes

---

### [NEW 2026] Slide: RL for Reasoning — The DeepSeek R1 Breakthrough
**Insert after:** GRPO slide
**Format:** Case study

**The story:** In January 2025, DeepSeek released R1-Zero — a model trained with pure RL (GRPO) on math and code, with NO supervised fine-tuning or human labels. The result matched OpenAI o1 on reasoning benchmarks.

**What emerged (unprompted):**
- Chain-of-thought reasoning appeared naturally through RL
- Self-verification behaviour ("wait, let me check that")
- Step-by-step problem decomposition
- The model learned to allocate more "thinking" to harder problems

**Training cost:** ~$294,000 (2 months on ~2,000 H800 GPUs)

**The Nature paper (Sep 2025):** "DeepSeek-R1 incentivises reasoning in LLMs through reinforcement learning" — on the cover of Nature.

**Why this matters for your work:**
- Reasoning capability can be **trained in**, not just prompted
- Pure RL on verifiable tasks (where you can check if the answer is correct) is sufficient
- You don't always need expensive human preference labels
- Small teams can replicate this approach on domain-specific tasks (math, code, structured extraction)

**Replication recipe for practitioners:**
1. Define tasks with verifiable answers (code that compiles, math that checks out, structured outputs that validate)
2. Use GRPO with binary reward (correct/incorrect)
3. Train on 7B–13B model with Unsloth or TRL
4. Expect 10–30% improvement on reasoning tasks

**Facilitator Notes:**
- 🎤 "This paper changed the industry. It proved that you can train reasoning ability directly, without expensive human labellers. The implications are still unfolding."
- Common question: "Can I do this with my domain?" Answer: "If you can verify correctness automatically — yes."
- Time: 4 minutes

---

### [NEW 2026] Slide: Continued Pre-Training vs. Fine-Tuning vs. RAG — The Decision Matrix
**Insert after:** When NOT to Fine-Tune
**Format:** Decision table

| Criterion | CPT | SFT | RAG |
|---|---|---|---|
| **Changes model knows** | ✅ Deep | ❌ Shallow | ❌ None |
| **Changes model behaves** | ❌ Minimal | ✅ Primary purpose | ❌ None |
| **Changes model sees** | ❌ None | ❌ None | ✅ Primary purpose |
| **Data requirement** | 5B+ tokens | 1K–10K examples | Documents in any volume |
| **Handles changing data** | ❌ Static once trained | ❌ Static once trained | ✅ Live updates |
| **Compute cost** | $$$ (24–72h multi-GPU) | $ (1–3h single GPU) | $ (indexing only) |
| **Latency impact** | None (weights baked in) | None (weights baked in) | + retrieval latency |
| **Auditability** | Low (opaque weights) | Low (opaque weights) | High (can trace source) |
| **Best for** | Domain vocabulary/reasoning | Format, style, behaviour | Facts, citations, freshness |

**The layering pattern most teams arrive at:**
```
RAG (always-on for knowledge freshness)
  + SFT (trained once for format/behaviour)
    + DPO (trained once for quality alignment)
      = Production system
```

**Facilitator Notes:**
- 🎤 "This matrix is the cheat sheet. Print it. Most confusion in AI projects comes from people using the wrong technique for their problem."
- Time: 3 minutes

---

### [NEW 2026] Slide: Catastrophic Forgetting and How to Prevent It
**Insert after:** DACPT Deep Dive
**Format:** Problem-solution with techniques

**The problem:** When you fine-tune on domain data, the model can "forget" general capabilities.

**Detection:** Run general benchmarks (MMLU, GSM8K, HumanEval) before and after. >5% drop = forgetting.

**Prevention techniques:**

| Technique | How It Works | When to Use |
|---|---|---|
| **Replay mixing** | Include 5–15% general data in training mix | Always during CPT |
| **Elastic Weight Consolidation (EWC)** | Penalise changes to "important" weights | When fine-tuning on very narrow data |
| **LoRA rank limiting** | Keep rank 16–32; fewer parameters = less forgetting | Standard practice |
| **Progressive freezing** | Freeze early layers; only adapt later layers | When base capabilities must be preserved exactly |
| **Multi-task training** | Include general instruction-following in SFT mix | Always during SFT |

**The 2026 best practice:** "Use LoRA SFT (not full fine-tune) and always include 10% general-capability examples in your training mix."

**Facilitator Notes:**
- 🎤 "Every fine-tuning project should measure forgetting. It's the silent killer of model quality."
- Time: 3 minutes

---

### [NEW 2026] Slide: LoRA Hyperparameters That Actually Matter
**Insert after:** LoRA/QLoRA section (existing)
**Format:** Technical reference with practical guidance

**The 2026 defaults that work for 7B–70B:**

| Parameter | Recommended | Why |
|---|---|---|
| **Rank (r)** | 16–64 | Higher = more expressiveness but more memory. 32 is the sweet spot for most tasks |
| **Alpha (α)** | 2× rank | Scaling factor. α=64 for r=32 is the standard |
| **Target modules** | q_proj, k_proj, v_proj, o_proj, gate_proj, up_proj, down_proj | Hit all projections for full expressiveness |
| **Dropout** | 0.05 | Prevents adapter overfitting |
| **Learning rate** | 1e-4 to 3e-4 | 10× higher than full fine-tune (only adapter weights move) |
| **Epochs** | 2–3 | More = overfitting on small datasets |
| **Batch size** | Largest that fits memory | Use gradient accumulation if needed |
| **Quantisation** | 4-bit (QLoRA) | Standard for 70B on single GPU |

**Common mistakes:**
- ❌ Rank too high (128+) → memory waste, minimal quality gain
- ❌ Training for 10+ epochs → overfitting
- ❌ Only targeting attention layers → missing MLP adaptation
- ❌ LR too low (1e-5) → adapter barely changes

**Facilitator Notes:**
- ⚡ ADVANCED — This slide is for engineers who will actually train. PMs can skip.
- 🎤 "These are starting points, not sacred numbers. But they work for 90% of cases."
- Time: 2 minutes

---

### [NEW 2026] Slide: Hands-On Activity — The Decision Sprint (Updated)
**Insert after:** Existing hands-on activity section
**Format:** Activity update

**Updated activity: "Model Customisation Decision Sprint"**

**Scenario:** Your team has been asked to build a domain-specific AI assistant for [pick one]:
- A) Legal contract analysis (interprets clauses, identifies risks)
- B) Internal IT helpdesk (answers employee tech questions)
- C) Financial report generation (writes quarterly summaries from data)

**For your chosen scenario, decide:**

| Decision | Your Answer | Justification |
|---|---|---|
| 1. CPT needed? (Y/N) | | |
| 2. SFT data source and volume? | | |
| 3. Preference alignment method? (DPO/GRPO/Skip) | | |
| 4. Base model and size? | | |
| 5. RAG layer needed? (Y/N, for what?) | | |
| 6. Eval suite (3 key metrics)? | | |
| 7. Deploy as full model or LoRA adapter? | | |
| 8. Estimated training compute (GPU-hours)? | | |

**Groups present for 2 min, class votes on best approach.**

**Facilitator Notes:**
- 🎤 "This activity replaces the original single-axis decision. Students now must think across the full pipeline."
- Time: 12 minutes (5 min work, 6 min present + vote, 1 min debrief)
- Tip: Legal scenario is hardest (needs CPT). IT helpdesk is easiest (RAG + prompt may suffice).

---

### [NEW 2026] Slide: Knowledge Check Updates
**Insert after:** Existing quiz section
**Format:** Updated quiz questions

**New/replacement quiz questions:**

Q1. [NEW] What is the primary innovation of GRPO compared to PPO?
- A) It uses a larger learning rate
- B) It eliminates the need for a value function model ✅
- C) It requires more training data
- D) It only works with closed-source models

Q2. [NEW] In the four-stage pipeline (DACPT → SFT → DPO → Rejection-Sampled SFT), what does Stage 1 (DACPT) primarily teach the model?
- A) How to format responses correctly
- B) User preferences about quality
- C) Domain vocabulary and reasoning patterns ✅
- D) Which tools to call

Q3. [NEW] What is model merging?
- A) Training two models simultaneously
- B) Combining weight tensors of fine-tuned models without additional training ✅
- C) Running two models in parallel at inference
- D) Splitting a large model across GPUs

Q4. [NEW] Speculative decoding achieves faster inference by:
- A) Using a smaller model to draft tokens verified by the larger model in parallel ✅
- B) Reducing the model size
- C) Skipping attention computation
- D) Caching all possible outputs

Q5. [NEW] According to the 2026 consensus, when should you use RAG instead of fine-tuning?
- A) When you need the model to adopt a specific output format
- B) When your knowledge changes frequently or you need source citations ✅
- C) When you need faster inference
- D) When you have unlimited compute budget

---

### [NEW 2026] Slide: Case Study — Building a Domain LLM (2026 Real-World)
**Insert after:** Case studies section
**Format:** Case study

**Case: TensorOps "Talkie" Project — A 1930s-Only LLM**

**Challenge:** Build an AI assistant that only knows information from before 1931 — no modern knowledge leakage.

**Why they trained from scratch:** Hard knowledge cutoff requirement. No existing model could guarantee zero post-1930 information.

**Pipeline:** 13B parameters, 260B tokens of pre-1931 text, standard DACPT → SFT → DPO pipeline.

**Lesson for students:** This is the rare case where from-scratch makes sense. For 99% of use cases, continued pre-training on an existing 70B is strictly better. The three conditions for from-scratch:
1. Hard knowledge cutoff (contamination unacceptable)
2. Vocabulary the base model can't represent (protein sequences, novel scripts)
3. Trillions of in-distribution tokens + matching compute budget

**Contrast: Most domain projects in 2026** use Llama 3.1 70B or Qwen2.5-72B as base → DACPT with 5B–50B domain tokens → LoRA SFT on 2K–10K examples → DPO → deploy. Total compute: 2–4× H100 for 1–3 days. Total cost: $2K–$15K.

**Facilitator Notes:**
- 🎤 "This case study shows both the exception AND the rule. From-scratch is almost never the move — but knowing when it IS helps you avoid over-engineering."
- Time: 3 minutes

---

### [UPDATE 2026] Slide: Updated "When to Fine-Tune" Decision Tree
**Insert after:** Replacing/updating existing Section 1 content
**Format:** Updated decision flow (replaces original binary framework)

The original module presented fine-tuning as a binary: fine-tune vs. prompt. The 2026 reality is a 4-way decision with layering:

```
START: What is your primary problem?
│
├─→ "Model doesn't know domain content"
│    └─→ Is the content stable (doesn't change weekly)?
│         ├── Yes → Continued Pre-Training (DACPT)
│         └── No → RAG
│
├─→ "Model knows content but gives wrong format/style"
│    └─→ LoRA SFT on 1K–10K examples
│
├─→ "Model gives right format but quality is inconsistent"
│    └─→ Preference Alignment (DPO for general; GRPO for reasoning)
│
├─→ "Model needs to use tools and take actions"
│    └─→ Agentic layer (fine-tune for tool calling + agent framework)
│
└─→ "Not sure yet"
     └─→ Start with prompting + RAG. Measure. Fine-tune only where metrics show clear gaps.
```

**Facilitator Notes:**
- 🎤 [UPDATE] "This replaces the binary framing from the original module. The 2026 reality is more nuanced but actually clearer once you map it to failure modes."
- Time: 3 minutes (replaces existing content, does not add time)

---

## STEP 4: FACILITATOR UPDATE BRIEF

---

### 🎤 Facilitator Update Brief — Module 09

#### Top 3 Most Important Additions

1. **GRPO and the preference alignment zoo** — Students will encounter GRPO, DPO, SimPO, KTO within their first week of real-world fine-tuning work. The DeepSeek R1 story is both inspirational and technically grounding. This is the single biggest gap in the original module.

2. **The four-stage pipeline** — The production consensus (DACPT → SFT → DPO → Rejection-Sampled SFT) gives students a complete mental model instead of treating fine-tuning as a single step. This reframes the entire module.

3. **Model merging + speculative decoding + SLMs** — These are the "free lunch" techniques that students can use immediately. Merging combines capabilities without training; speculative decoding makes serving faster for free; SLMs reduce cost by 99% for most tasks.

#### What's Now Outdated in the Original

| Original Content | Issue | How to Address |
|---|---|---|
| Binary "fine-tune vs. prompt" decision | Oversimplified; missing RAG, CPT, and agents as options | Replace with the 4-way layered decision tree |
| RLHF as the alignment method | GRPO/DPO have largely replaced PPO-based RLHF in practice | Present PPO as history; DPO/GRPO as current practice |
| No mention of preference optimisation variants | DPO, GRPO, SimPO, KTO are daily tools | Add the preference alignment zoo slide |
| Fine-tuning presented as expensive and complex | Unsloth makes 7B fine-tuning a one-command operation on consumer GPU | Update with tooling slide; mention free Colab demos |
| No multi-stage pipeline concept | Students leave thinking FT is one-shot | The four-stage pipeline reframes everything |

#### Time Management (60 min → 75-90 min recommended)

The new content adds approximately 15–20 slides. For a **60-minute delivery**, recommended approach:
- Keep the updated decision framework (5 min)
- Four-stage pipeline overview (5 min)
- GRPO + preference alignment (7 min)
- Synthetic data best practices (4 min)
- Model merging + speculative decoding + SLMs (8 min combined)
- Updated hands-on activity (12 min)
- Skip: DACPT deep hyperparameters, rejection-sampled SFT, LoRA hyperparameters table (mark as reference handout)

For a **75-minute extended version:** Include everything except the LoRA hyperparameters table.
For a **90-minute deep-dive:** Full content including live Unsloth demo.

#### New Tools/Accounts/Demos to Set Up

| Tool | Purpose | Setup |
|---|---|---|
| **Unsloth** | Live fine-tuning demo on free Colab GPU | Pre-run notebook to verify GPU allocation; have backup recording |
| **MergeKit** | Model merging demonstration | Pre-download 2 small LoRA adapters to merge |
| **HuggingFace account** | Access to open models and LoRA hub | Create/verify account; ensure can push/pull models |
| **vLLM** | Speculative decoding demo | Optional — show benchmark results if live demo isn't feasible |

#### Recommended Pre-Reading for Advanced Students
- "How to Train a Custom LLM for Your Business in 2026" — TensorOps (the full pipeline)
- "DeepSeek-R1 incentivises reasoning in LLMs through reinforcement learning" — Nature (Sep 2025)
- "Do Post-Training Algorithms Actually Differ?" — oxRL paper (March 2026, 240 training runs)
- "The Anatomy of an Agent Harness" — Akshay Pachaar (context for why fine-tuning feeds into agents)

---

*Module 09 Update — AI & Agentic AI Training Programme*  
*Updated: July 2026 · Covers developments through June 2026*
