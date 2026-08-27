# Module 07 — Prompt Engineering & In-Context Learning
## [NEW AUG-2026] Content Refresh Addendum
### Track: Engineering | Date: 12 August 2026

---

## A) EXECUTIVE SUMMARY

**What's most important since the July 2026 update:**

1. **Anthropic published "The New Rules of Context Engineering for Claude 5 Generation Models" (July 24, 2026)** — They removed over 80% of Claude Code's system prompt for Claude Opus 5 and Claude Fable 5 with no measurable loss on coding evaluations. This is the most concrete, real-world proof point for the "less is more" principle we introduced in July.

2. **Claude 5 generation makes adaptive thinking the only thinking mode** — Manual `budget_tokens` is deprecated; the model dynamically allocates reasoning effort. This obsoletes our Extended Thinking budget control slide content for Claude 5 models (still valid for Sonnet 4.x).

3. **OpenAI released GPT-5.5 and GPT-5.6 Sol/Terra/Luna (July–August 2026)** — GPT-5.6 introduces explicit prompt caching breakpoints (replacing automatic prefix caching), six reasoning effort levels, and a family-of-three model architecture (Sol = frontier, Terra = balanced, Luna = efficient).

4. **OpenAI deprecated its hosted Prompt Objects API (June 3, 2026; shutdown November 30, 2026)** — Signals that prompt management must move into application code. Validates our PromptOps slide direction.

5. **Amazon Bedrock launched Advanced Prompt Optimization and Migration Tool (May 14, 2026)** — Compares original vs. optimized prompts across up to 5 models simultaneously. Production-ready DSPy-like optimization now available as a managed service.

6. **Prompt caching economics restructured across all providers** — Anthropic: 90% savings on cache hits; OpenAI GPT-5.6: 1.25× write premium + explicit breakpoints; Gemini: context caching at similar savings. Cache-aware prompt architecture is now a core engineering skill.

7. **Claude Fable 5 (Mythos-class) confirmed the "prompting inversion" at scale** — First model where carefully engineered step-by-step prompts *actively degraded* output. The leverage shifted from instructions to context assembly and verification loops.

8. **DSPy reached 3.2 with GEPA optimizer (ICLR 2026 oral), native reasoning model support, and MLflow integration** — Production-grade automatic prompt optimization is now mainstream.

9. **"Progressive disclosure" replaces "put it all upfront" as the context engineering best practice** — Load context just-in-time rather than stuffing everything into the system prompt. Validated by both Anthropic and OpenAI's developer guidance.

10. **The Three-Prompt Architecture for GPT-5.6**: OpenAI now recommends separating System (constraints/identity) → Developer (tools/schemas/context) → User (task/intent). This four-layer model obsoletes single-string approaches.

---

## B) NEW SLIDES

---

### [NEW AUG-2026] Slide: Anthropic's 80% Prompt Deletion — The Definitive Case Study
**Insert after:** "The 'Less is More' Principle" slide
**Source:** https://claude.com/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models (July 24, 2026)

**The Story:**
On July 24, 2026, Anthropic published something extraordinary: they explained how they *deleted their own work*. The Claude Code team removed over 80% of the system prompt for Claude Opus 5 and Claude Fable 5 — **with no measurable loss on their coding evaluations.**

**What they deleted (and why):**

| Old Instruction | Why It Was Removed | New Approach |
|---|---|---|
| "Never write multi-paragraph docstrings" | Model now has better judgement about when comments are appropriate | "Write code that reads like the surrounding code: match its comment density, naming, and idiom" |
| Detailed code review instructions | Not always needed; wasted tokens | Moved into a separate "skill" loaded on demand |
| Repeated tool-use examples | Constrained model to narrow exploration space | Better tool interface design (expressive parameters, enums) |
| Explicit error-handling rules | Model now infers from context | Trust model judgment + surrounding code patterns |
| Multiple reminders of same instruction | Was needed for older models' attention patterns | State each instruction once |

**The 6 new rules (replacing the old approach):**

| Then (Old Models) | Now (Claude 5 Gen) |
|---|---|
| Give Claude rules | Let Claude use judgement |
| Give Claude examples | Design expressive interfaces |
| Put it all upfront | Use progressive disclosure |
| Repeat yourself | Simple tool descriptions |
| Memory in CLAUDE.md files | Auto-memory |
| Simple specs | Rich references (code, test suites, HTML artifacts, rubrics) |

**The key insight:**
> "The prompt the Claude Code team had carefully hand-tuned for older models was actively getting in the way of the newer ones."

**Implications for practitioners:**
- Your carefully crafted prompts from 6 months ago might be *hurting* performance on the latest models
- Every model upgrade should trigger a "prompt audit" — what can you delete?
- `claude doctor` command now ships to help rightsize prompts automatically

**Facilitator Notes:**
- This is THE case study for this module in August 2026. It proves the "less is more" principle with data from the model creator themselves
- Key discussion point: "If even Anthropic's own team was over-prompting, what does that mean for your system prompts?"
- Connects to the broader trend: as models get more capable, the value shifts from *instructions* to *context assembly*
- Time: 7 minutes

---

### [NEW AUG-2026] Slide: Adaptive Thinking Replaces Budget Control
**Insert after:** "Extended Thinking — Budget Control" slide
**Source:** https://docs.anthropic.com/en/docs/build-with-claude/adaptive-thinking; Claude Platform docs (July 2026)

**The Shift: From Manual Budgets to Adaptive Thinking**

As of Claude 5 generation (Opus 5, Sonnet 5, Fable 5), the manual `budget_tokens` parameter is **deprecated and returns a 400 error**. The model now uses **adaptive thinking** — dynamically determining when and how much to reason based on task complexity.

**How it works:**
```python
# OLD (Claude 4.x) — Manual budget
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    thinking={"type": "enabled", "budget_tokens": 10000},  # You decide
    messages=[...]
)

# NEW (Claude 5) — Adaptive (thinking on by default)
response = client.messages.create(
    model="claude-opus-5",
    max_tokens=16000,  # Total cap on thinking + response
    # No thinking parameter needed — it's automatic
    messages=[...]
)
```

**What adaptive thinking does:**
- Simple question → minimal thinking tokens (fast, cheap)
- Complex reasoning → heavy thinking allocation (thorough, slower)
- Same model, same API call — effort adjusts per-request

**Key behavioral changes for Claude 5:**
| Parameter | Claude 4.x | Claude 5 |
|---|---|---|
| `thinking.budget_tokens` | ✅ Supported | ❌ Returns 400 error |
| `max_tokens` | Caps response only | Caps thinking + response combined |
| Default thinking | Off (must opt in) | On by default |
| Temperature/top_p | Configurable | Non-default values return 400 error |

**Migration impact:** If your `max_tokens` was tuned tightly around expected output length, it can now truncate mid-answer because thinking tokens consume part of the budget. **Raise your `max_tokens` when migrating.**

**Facilitator Notes:**
- Update the Extended Thinking slide: "What we just taught about budget_tokens still applies to Sonnet 4.x/Opus 4.8, but Claude 5 models handle this automatically"
- This is a concrete API-breaking change that students will encounter immediately
- Key question: "Does losing budget control mean losing cost predictability?" Answer: Somewhat yes — monitor thinking token usage in production
- Time: 5 minutes

---

### [NEW AUG-2026] Slide: GPT-5.6 — The New Prompting Paradigm
**Insert after:** Reasoning Models section
**Source:** https://developers.openai.com/api/docs/guides/latest-model; https://openai.com/index/gpt-5-6/ (July–August 2026)

**GPT-5.6 is not one model — it's a family of three:**

| Model | Role | Best For |
|---|---|---|
| **Sol** (frontier) | Highest capability, most expensive | Complex reasoning, research, hard coding |
| **Terra** (balanced) | Strong capability, moderate cost | Most production workloads |
| **Luna** (efficient) | Fast, cheap, capable enough | High-volume, latency-sensitive tasks |

**Key prompting changes from GPT-5.5:**

1. **Six reasoning effort levels** — Not just on/off; granular control from "none" to "max"
2. **"State each instruction once" beats long rule stacks** — Model has been trained to push through obstacles rather than stop
3. **Explicit prompt caching** — You now mark breakpoints manually (see next slide)
4. **Verbosity dial** — New parameter to control output length
5. **Programmatic tool calling** — More deterministic tool use without prompt tricks

**The developer message layer:**
GPT-5.6 formalises a three-layer prompt hierarchy:
```
System prompt  → Identity, hard constraints, safety
Developer msg  → Tools, schemas, context, business logic
User message   → The actual task/question
```

**Important warning:** GPT-5.6 Sol is trained to "push through obstacles rather than stop." Within days of release, real users reported it deleting files and altering production databases when given broad tool access without guardrails. **Always scope tool permissions tightly.**

**Facilitator Notes:**
- This is the latest frontier model from OpenAI as of August 2026 — students will ask about it
- Key message: "The model family approach means you pick the right model for the job, not just 'use the biggest one'"
- Emphasise the safety angle: more capable + more agentic = more dangerous without guardrails
- Time: 6 minutes

---

### [NEW AUG-2026] Slide: Explicit Prompt Caching — A Production Skill
**Insert after:** GPT-5.6 slide (or PromptOps section)
**Source:** https://developers.openai.com/api/docs/guides/prompt-caching; digitalapplied.com (July 2026)

**What Changed (July 9, 2026):**
OpenAI's GPT-5.6 replaced free automatic prefix caching with **explicit breakpoints** — you now mark exactly which reusable prompt sections to cache.

**The economics:**

| Provider | Cache Hit Savings | Cache Write Cost | TTL | Mechanism |
|---|---|---|---|---|
| **OpenAI (GPT-5.6)** | Up to 90% off input | 1.25× uncached rate | 30 min minimum | Explicit breakpoints |
| **Anthropic (Claude)** | 90% off input | Standard rate | 5 min minimum | `cache_control` markers |
| **Gemini** | ~75% off input | Standard rate | Configurable | Context caching API |
| **OpenAI (GPT-5.5 and older)** | 50% off input | Free | Automatic | Implicit prefix matching |

**How explicit caching works (GPT-5.6):**
```python
response = client.chat.completions.create(
    model="gpt-5.6",
    messages=[
        {
            "role": "developer",
            "content": large_system_context,
            "cache_control": {"type": "breakpoint"}  # Cache everything up to here
        },
        {"role": "user", "content": user_query}  # This part changes per request
    ]
)
```

**Anthropic's approach (hierarchy matters):**
```python
response = client.messages.create(
    model="claude-opus-5",
    system=[
        {"type": "text", "text": long_system_prompt,
         "cache_control": {"type": "ephemeral"}}  # Cached for 5 min
    ],
    messages=[...]
)
# Anthropic caches in order: tools → system → messages
```

**Why this matters for prompt engineering:**
- Your prompt's *structure* now has direct cost implications
- Static content (system prompt, tool definitions, RAG context) should go *before* the cache breakpoint
- Dynamic content (user message, session-specific data) goes *after*
- **A 200,000-token system prompt goes from budget-breaking to a rounding error** with proper caching

**Production architecture — "Cache-First Agent Design":**
1. Design prompts with a stable prefix (identity + tools + domain knowledge)
2. Place cache breakpoint after the stable section
3. Append dynamic context (conversation, RAG results) after the breakpoint
4. Result: First call pays full price; subsequent calls save 75-90%

**Facilitator Notes:**
- This is now a *mandatory* production skill — not just an optimization
- Demo: Show the cost difference between a cached vs. uncached 100K-token system prompt (10× cost reduction)
- Key insight: "Prompt caching rewards good prompt architecture. If your prompt is well-structured (stable prefix, variable suffix), you save money automatically"
- Time: 6 minutes

---

### [NEW AUG-2026] Slide: Progressive Disclosure — The New Default Pattern
**Insert after:** Context Engineering slides
**Source:** Anthropic "New Rules" blog (July 24, 2026); OpenAI developer docs

**The Pattern: Load Context Just-In-Time, Not All-At-Once**

**The old way (2024–early 2026):**
```
System prompt contains EVERYTHING:
- All rules (2,000+ words)
- All tool descriptions
- All examples
- All policies
- All edge cases
→ Result: Context rot, wasted tokens, conflicting instructions
```

**The new way (mid-2026+):**
```
System prompt contains CORE IDENTITY + ROUTING:
- Who the model is (brief)
- Hard safety constraints (brief)
- How to find more information (tool/skill references)

Context loaded on demand:
- Verification rules → loaded when verification needed
- Code review guidelines → loaded when reviewing code
- Domain knowledge → loaded via RAG when topic detected
→ Result: Focused context, no rot, lower cost, better performance
```

**Anthropic's implementation in Claude Code:**
- Skills are "deferred loading" — agent searches for definitions only when needed
- CLAUDE.md references a tree of files rather than containing everything
- Tools use `ToolSearch` before invocation to load full definitions
- Memory is auto-captured rather than manually maintained

**Implementation strategies:**

| Strategy | How | When to Use |
|---|---|---|
| **Skill-based loading** | Define skills the model can invoke to get instructions | Complex multi-domain agents |
| **RAG-driven context** | Retrieve relevant docs based on user query | Knowledge-heavy applications |
| **Deferred tool definitions** | Load tool schemas only when tool is likely needed | Agents with 20+ tools |
| **Layered CLAUDE.md** | Main file references sub-files for specific domains | Large codebases |
| **Conditional system prompt sections** | Assemble system prompt dynamically per-request | Multi-tenant applications |

**Key quote from Anthropic:**
> "A common myth is that you want to make your CLAUDE.md a central repository for every known practice. Instead, consider having a tree of files that can be loaded at the right time."

**Facilitator Notes:**
- This directly updates our "5 Context Layers" slide — Layer 1 should now be *minimal* with other layers loaded progressively
- Demo opportunity: Show a system prompt before/after applying progressive disclosure (2,000 words → 200 words + skill references)
- Connect to caching: progressive disclosure also improves cache hit rates because the stable prefix stays stable
- Time: 5 minutes

---

### [NEW AUG-2026] Slide: Rich References Over Verbose Instructions
**Insert after:** Progressive Disclosure slide
**Source:** Anthropic "New Rules" blog (July 24, 2026)

**The Principle: Show, Don't Tell (With Code)**

The most capable models now respond better to *references* than *instructions*:

| Instead of... | Provide... | Why It Works |
|---|---|---|
| "Follow this formatting style: [500 words of description]" | A code file showing the style in action | Models parse code better than natural language descriptions |
| "The output should look like this: [markdown spec]" | An HTML mockup of the desired output | Visual/structural reference > textual description |
| "Make sure the API follows REST conventions and..." | A test suite that validates the desired behaviour | Tests are unambiguous specifications |
| "Good code review means checking for..." | A rubric with scored examples | Rubrics enable self-verification loops |
| "The design should be..." | A Figma export or HTML artifact | Code-level fidelity beats prose |

**Anthropic's findings:**
- HTML artifacts as references produce better results than markdown descriptions
- Code as spec (test suites, type definitions) outperforms natural language specs
- Rubrics enable the model to run "verifier agents" against its own work

**Example — Using a test suite as a spec:**
```python
# Instead of writing 500 words describing the API contract:
# Reference: tests/test_user_api.py

def test_create_user_returns_201():
    response = client.post("/users", json={"name": "Alice", "email": "a@b.com"})
    assert response.status_code == 201
    assert "id" in response.json()
    assert response.json()["name"] == "Alice"

def test_create_user_duplicate_email_returns_409():
    # First create
    client.post("/users", json={"name": "Alice", "email": "a@b.com"})
    # Duplicate
    response = client.post("/users", json={"name": "Bob", "email": "a@b.com"})
    assert response.status_code == 409
```
*This 15-line test file communicates the spec more precisely than any prompt description.*

**Facilitator Notes:**
- This connects naturally to engineering audiences — "Write your specs as tests, not as prompts"
- For those building agents: rubrics are the new frontier for quality control
- Time: 4 minutes

---

### [NEW AUG-2026] Slide: Amazon Bedrock Advanced Prompt Optimization
**Insert after:** DSPy / Automatic Prompt Optimisation slides
**Source:** https://aws.amazon.com/about-aws/whats-new/2026/05/amazon-bedrock-advanced-prompt-optimization-migration-tool/ (May 14, 2026)

**Managed Prompt Optimization — No DSPy Required**

Amazon Bedrock now offers **Advanced Prompt Optimization (AdvPO)** — a managed service that automatically refines prompts for any Bedrock model:

**What it does:**
1. Takes your original prompt + evaluation dataset
2. Optimizes the prompt using automated techniques (instruction refinement, few-shot selection, format optimization)
3. Compares original vs. optimized across **up to 5 models simultaneously**
4. Reports accuracy, consistency, and cost metrics per variant

**Use cases:**
- **Model migration:** Moving from Claude Sonnet 4 → Opus 5? AdvPO rewrites your prompts for the new model's strengths
- **Performance improvement:** Plateau on manual iteration? Let the optimizer find improvements
- **Multi-model comparison:** Same task, 5 models, optimized prompts for each — pick the best price/performance

**How it compares to DSPy:**

| Feature | DSPy | Bedrock AdvPO |
|---|---|---|
| Setup | Code-level integration | Console UI + API |
| Optimization target | Full pipeline (multi-step) | Single prompt |
| Requires coding | Yes (Python) | No |
| Model support | Any (via adapters) | Bedrock models |
| Production integration | Manual deployment | Direct to Bedrock |
| Best for | Complex pipelines, research teams | Quick wins, migration, non-coding teams |

**Also launched (May 4, 2026):** Amazon Bedrock AgentCore Quality Loop — analyses production traces and evaluation outputs to optimise system prompts or tool descriptions automatically. This is continuous optimization in production.

**Facilitator Notes:**
- This is the "enterprise-friendly DSPy" — same concept, managed service
- For AWS-focused audiences, this is the practical takeaway: "You don't need to build your own optimization pipeline"
- Demo: Walk through the Bedrock console prompt optimization workflow (5 min setup → results)
- Time: 5 minutes

---

### [NEW AUG-2026] Slide: OpenAI Prompt Objects Deprecation — What It Means
**Insert after:** PromptOps slide
**Source:** https://developers.openai.com/api/docs/guides/prompting/migrate-from-prompt-object (June 3, 2026)

**OpenAI is Killing Hosted Prompt Management**

Timeline:
- **June 3, 2026:** Prompt creation de-emphasised; deprecation announced
- **November 30, 2026:** `v1/prompts` endpoint shuts down permanently
- **Also deprecated:** Assistants API (shutdown August 26, 2026), Evals platform, Agent Builder dashboard

**The pattern:** OpenAI is deprecating ALL hosted state management — pushing prompt/agent/workflow config into developer code.

**What this means for production teams:**
1. **Prompts must live in YOUR code/infrastructure** — not a provider's dashboard
2. **Version control with Git** — not a provider's UI
3. **Prompt registries must be self-hosted** — PromptHub, Humanloop, Portkey, or your own DB
4. **Provider portability increases** — if prompts are in your code, switching providers is easier

**The recommended architecture (2026):**
```
Your Git repo or database
  └── prompts/
      ├── v2.3_customer_support.yaml  ← versioned
      ├── v1.8_code_review.yaml       ← rollback-ready
      └── evaluations/
          ├── test_cases.json          ← regression suite
          └── metrics.json             ← baseline scores
```

**Key insight from OpenAI community:**
> "Once it's in your code there's nothing hosted left for them to deprecate later."

**Facilitator Notes:**
- This validates our PromptOps slide completely — the industry has moved to "prompts as code"
- For teams still using OpenAI's dashboard: this is a migration they need to plan NOW
- Discussion: "What's the right abstraction layer for prompts? Environment variables? Config files? A dedicated registry?"
- Time: 4 minutes

---

### [NEW AUG-2026] Slide: The GPT-5.6 Prompting Guide — What Works Now
**Insert after:** GPT-5.6 introduction slide
**Source:** https://developers.openai.com/cookbook/examples/gpt-5/gpt-5_prompting_guide/; felloai.com; OpenAI developer docs

**Key Prompting Principles for GPT-5.6 (August 2026):**

1. **State each instruction once** — Repetition doesn't help; the model tracks instructions reliably across long contexts
2. **Use the Responses API for agentic flows** — Reasoning is persisted between tool calls, making multi-step workflows more efficient
3. **Six reasoning effort levels** — Control the thinking/speed tradeoff per-request:
   - `none` → no reasoning, fastest
   - `low` → light reasoning
   - `medium` → default balance
   - `high` → thorough reasoning
   - `very_high` → extended analysis
   - `max` → deepest reasoning, slowest
4. **Explicit prompt caching** — Mark breakpoints to control what gets cached
5. **Verbosity parameter** — Control output length without prompt hacks ("be concise")
6. **Structured outputs remain critical** — `response_format: json_schema` works as before, but note: combining with explicit caching has edge cases (cache writes may not fire)

**What NOT to do with GPT-5.6:**
- ❌ Long "rule stacks" — the model already follows instructions well
- ❌ "Think step by step" — model has internal reasoning
- ❌ Detailed scaffolding for tool use — model handles tool planning natively
- ❌ Repeated emphasis ("IMPORTANT: DO NOT...") — once is enough

**The "push through" behaviour:**
GPT-5.6 Sol is trained to persist through difficulties rather than stopping and asking for clarification. This means:
- ✅ It completes complex tasks more reliably
- ⚠️ It may take destructive actions if tool permissions are too broad
- 🔒 **Always** scope tool access tightly; use approval gates for destructive operations

**Facilitator Notes:**
- This updates our Decision Tree: GPT-5.6 is the new "frontier standard model" equivalent
- The safety angle is critical — more capable models that don't stop are more dangerous without guardrails
- Compare to Claude 5's approach (similar capability jump, different risk profile)
- Time: 5 minutes

---

### [NEW AUG-2026] Slide: Context Engineering in Practice — Towards Data Science Framework
**Insert after:** 5 Context Layers slide
**Source:** https://towardsdatascience.com/prompt-context-loop-the-three-engineering-layers-every-rag-system-is-built-on/ (August 7, 2026)

**The Three Engineering Layers (Towards Data Science, Aug 2026):**

Every production RAG/agent system is built on three distinct engineering layers:

```
┌─────────────────────────────────────────────┐
│          LOOP ENGINEERING                     │
│  Orchestration, iteration, error recovery    │
│  ┌─────────────────────────────────────┐    │
│  │      CONTEXT ENGINEERING             │    │
│  │  What data enters the window,        │    │
│  │  when, from where, in what format    │    │
│  │  ┌─────────────────────────────┐    │    │
│  │  │   PROMPT ENGINEERING         │    │    │
│  │  │   The instruction itself:    │    │    │
│  │  │   system msg, schema,        │    │    │
│  │  │   output format              │    │    │
│  │  └─────────────────────────────┘    │    │
│  └─────────────────────────────────────┘    │
└─────────────────────────────────────────────┘
```

**This validates and extends our "Three Levels" framework with a different lens:**
- **Prompt engineering** = the call itself (system message, instructions, output schema)
- **Context engineering** = the assembly (what retrieval, what memory, what metadata)
- **Loop engineering** = the orchestration (retry logic, verification, multi-step flows)

**Industry data (DataHub 2026 Report):**
- 82% of IT and data leaders agree prompt engineering alone is insufficient for AI at scale
- 95% of data teams plan to invest in context engineering training during 2026
- The investment shift: from "better prompts" to "better systems"

**Facilitator Notes:**
- Use this to reinforce our Three Levels framework with third-party validation
- The DataHub stat (82% / 95%) makes a compelling case for why this module needed updating
- Time: 3 minutes

---

### [NEW AUG-2026] Slide: Claude Fable 5 — When Prompts Make Things Worse
**Insert after:** "Less is More" principle slide
**Source:** https://kenhuangus.substack.com/p/claude-fable-5-what-changed-and-how (July 4, 2026); Anthropic Fable field guide

**The Practitioner's Experience:**

> "Fable 5 is the first model where my carefully engineered step-by-step prompts made output *worse*. The model plans better than my scaffolding does."
> — Ken Huang, developer, after first day with Claude Fable 5

**What happened:**
- Mythos-class models (Fable 5, Opus 5) have such strong internal planning that external scaffolding creates *interference*
- Explicitly telling the model how to decompose a problem prevents it from finding a better decomposition
- Few-shot examples constrain the exploration space rather than guiding it

**The new leverage points for Mythos-class models:**

| Old Leverage (worked on Opus 4.x) | New Leverage (Claude 5 / Fable) |
|---|---|
| Detailed step-by-step instructions | Clear goal statement + constraints |
| Manual CoT scaffolding | Let model plan internally |
| Many few-shot examples | Zero-shot or 1 example max |
| Long system prompts | Minimal identity + progressive disclosure |
| Explicit verification rules | Rubrics + verifier sub-agents |
| Memory management via prompts | Auto-memory |

**The Fable 5 field guide key points:**
1. Capability improvements are a prompt to *re-evaluate* which instructions are still needed
2. If you're migrating from Opus 4.8, start by removing instructions and measuring
3. Use `claude doctor` to automatically identify over-constrained prompts

**Facilitator Notes:**
- This is the most relatable slide for practitioners — "your existing prompts might be hurting you"
- Key takeaway: "Every model upgrade should trigger a prompt audit. What was essential last month might be counterproductive today."
- Time: 4 minutes

---

### [NEW AUG-2026] Slide: Prompt Architecture — The 2026 Cost Equation
**Insert after:** Prompt Caching slide
**Source:** Multiple: digitalapplied.com, futureagi.com, chatgptaihub.com (June–August 2026)

**Prompts Are Now Cost Architecture**

In 2026, how you *structure* your prompt directly determines your bill:

**The cost hierarchy of a well-designed prompt:**
```
┌────────────────────────────────────────────────┐
│ CACHED (stable across requests)         -90% cost │
│ • System identity                               │
│ • Tool definitions                              │
│ • Domain knowledge                              │
│ • Company policies                              │
│ ─── CACHE BREAKPOINT ───                        │
│ DYNAMIC (changes per request)       FULL cost   │
│ • User message                                  │
│ • Session-specific RAG results                  │
│ • Conversation history (recent)                 │
└────────────────────────────────────────────────┘
```

**Real-world cost impact:**

| Scenario | Without Caching | With Caching | Savings |
|---|---|---|---|
| 200K-token system prompt, 1000 calls/day | $500/day (at $2.50/M) | $50/day | 90% |
| Agent with 50 tool definitions (15K tokens) | $37.50/day | $3.75/day | 90% |
| RAG app with 100K context + 2K query | $250/day | $30/day | 88% |

**The new skill: Cache-Aware Prompt Design**
1. **Identify what's stable** — system prompt, tools, domain knowledge → put before breakpoint
2. **Identify what's dynamic** — user input, session data, latest RAG results → put after
3. **Order by stability** — Most stable content first, most variable last
4. **Measure cache hit rates** — If < 80%, restructure your prompt
5. **Monitor TTL** — Anthropic: 5 min; OpenAI GPT-5.6: 30 min minimum

**Key quote:**
> "Prompt caching is not an optimization. It is the difference between a production AI feature that pencils out and one that eats your margin alive."

**Facilitator Notes:**
- This makes prompt engineering directly relevant to engineering managers and finance stakeholders
- Demo: Show real cost calculations — "Your 200K system prompt costs X per day without caching vs. Y with caching"
- Students should leave knowing: prompt structure = cost structure
- Time: 5 minutes

---

### [NEW AUG-2026] Slide: DSPy 3.2 + GEPA — Production-Ready Prompt Compilation
**Insert after:** Existing DSPy slide
**Source:** https://github.com/stanfordnlp/dspy; hashnode.dev (April 2026); ICLR 2026

**DSPy Update (August 2026):**

Since our July module, DSPy has reached **version 3.2** with significant additions:

**New in DSPy 3.x (2025–2026):**
- **GEPA optimizer** — Accepted as an oral presentation at ICLR 2026 (top 1.8% of submissions). Significantly faster than MIPROv2 on large programs
- **Native reasoning model support** — Optimizes prompts specifically for o3, Claude Extended Thinking, etc.
- **MLflow observability integration** — Track optimization runs, compare experiments, deploy compiled prompts
- **MIPROv2** — Faster default optimizer with async support
- **Streaming support** — Real-time output from compiled programs
- **160,000+ monthly downloads** — No longer experimental; production-proven

**The DSPy ecosystem growth:**
- Inspired "at least a half-dozen cool new libraries" (Omar Khattab, DSPy creator)
- Now has Ruby port (dspy.rb), JavaScript port in development
- Used in production at multiple Fortune 500 companies

**When to use DSPy vs. Bedrock AdvPO:**

| Use DSPy when... | Use Bedrock AdvPO when... |
|---|---|
| Multi-step pipelines | Single prompts |
| Need full control | Quick wins without coding |
| Custom metrics and logic | Standard accuracy metrics |
| Research / pushing limits | Enterprise migration |
| Open-source requirement | AWS-native stack |

**Facilitator Notes:**
- Update from July: DSPy is now ICLR-published and production mainstream — no longer "cutting edge research"
- For advanced audiences: discuss GEPA vs. MIPROv2 tradeoffs
- Time: 4 minutes

---

### [NEW AUG-2026] Slide: The Model Capability Ladder — Prompting Strategy by Tier
**Insert after:** Decision Tree slide
**Source:** Synthesis of Anthropic, OpenAI, and community guidance (July–August 2026)

**Different Models Need Different Prompting Strategies:**

| Model Tier | Examples (Aug 2026) | Prompting Strategy |
|---|---|---|
| **Mythos/Frontier** | Claude Fable 5, GPT-5.6 Sol | Minimal instructions, rich context, let model plan |
| **Flagship** | Claude Opus 5, GPT-5.5 | Moderate instructions, progressive disclosure |
| **Workhorse** | Claude Sonnet 5, GPT-5.6 Terra | Balanced instructions + examples, structured output |
| **Efficient** | Claude Haiku 5, GPT-5.6 Luna | More explicit instructions, clear examples, tight schemas |
| **Legacy** | GPT-4o, Claude Sonnet 4 | Full scaffolding, CoT prompts, detailed few-shot |

**The key insight:** Prompting is no longer "one size fits all." You need different prompt strategies for different model tiers — and you may use multiple tiers in the same application.

**Production pattern — Meta-prompting across tiers:**
```python
# Use a frontier model to WRITE the prompt for an efficient model
meta_prompt = frontier_model.generate("Write an optimal prompt for Luna to classify...")
# Then use the efficient model with the optimized prompt in production
result = luna_model.classify(prompt=meta_prompt, input=user_text)
```

This gives you frontier-quality prompts at efficient-model inference costs.

**Facilitator Notes:**
- This replaces a single "best practices" approach with a tier-aware strategy
- Key message: "The model you prompt for determines HOW you prompt"
- Connect to cost: frontier models are 10-50× the cost of efficient models. Right-sizing matters.
- Time: 4 minutes

---

### [NEW AUG-2026] Slide: Updated Decision Tree (August 2026 Edition)
**Insert after:** Existing Decision Tree (replaces it)
**Source:** Synthesis of all August 2026 updates

**Which Technique When? — August 2026 Edition:**

```
What model tier are you using?
├── FRONTIER (Fable 5, GPT-5.6 Sol)
│   ├── Minimal instructions — state goal + constraints only
│   ├── Progressive disclosure — load context on demand
│   ├── Rich references — code/tests > prose descriptions
│   ├── No CoT scaffolding — model plans better internally
│   └── Tight tool permissions — model will "push through"
│
├── FLAGSHIP (Opus 5, GPT-5.5)
│   ├── Adaptive thinking handles reasoning automatically
│   ├── Structured outputs for data extraction
│   ├── Moderate system prompt — identity + key constraints
│   └── Cache-aware design for cost control
│
├── WORKHORSE (Sonnet 5, GPT-5.6 Terra)
│   ├── Balanced instructions + 1-2 examples if pattern non-obvious
│   ├── Structured outputs (strict mode) for reliability
│   ├── DSPy/AdvPO for optimization if you have eval data
│   └── Standard prompt caching for cost
│
└── EFFICIENT (Haiku 5, Luna)
    ├── Explicit instructions — don't assume inference
    ├── Few-shot examples — model benefits from demonstrations
    ├── Tight output schemas — reduce parsing failures
    └── Meta-prompted — use a frontier model to write its prompt

Cross-cutting:
├── Need structured data? → Structured outputs (all tiers)
├── Context > 8K tokens? → Apply context rot mitigation
├── Production app? → PromptOps (versioning, evals, caching)
└── Security-sensitive? → 7-layer defence stack (all tiers)
```

**Facilitator Notes:**
- This REPLACES the July decision tree — the tier-aware approach is the key update
- Print as an updated handout
- Time: 3 minutes

---

### [NEW AUG-2026] Slide: Knowledge Check — August 2026 Questions
**Insert after:** Existing quiz section
**Source:** Module content synthesis

**New quiz questions for August 2026 content:**

Q11. Anthropic removed 80% of Claude Code's system prompt for Claude 5 generation models. What was the measured impact on coding evaluations?
- A) Performance improved by 20%
- B) Performance degraded by 10%
- C) No measurable loss ✅
- D) Performance improved by 80%

Q12. On Claude 5 models, what happens if you pass `thinking: {type: "enabled", budget_tokens: 10000}`?
- A) The model uses exactly 10,000 thinking tokens
- B) The parameter is silently ignored
- C) The API returns a 400 error ✅
- D) The model uses adaptive thinking with a 10K cap

Q13. GPT-5.6 introduced explicit prompt caching. What is a "cache breakpoint"?
- A) A point where the model stops generating
- B) A marker that defines the boundary between cached and dynamic content ✅
- C) A debugging tool for prompt errors
- D) A mechanism to clear the model's memory

Q14. What does "progressive disclosure" mean in context engineering?
- A) Gradually revealing the answer to the user
- B) Loading context just-in-time rather than putting everything upfront ✅
- C) Showing thinking tokens to the user progressively
- D) Increasing temperature gradually during generation

Q15. Amazon Bedrock's Advanced Prompt Optimization tool (launched May 2026) can:
- A) Only optimize prompts for Claude models
- B) Compare original vs. optimized prompts across up to 5 models simultaneously ✅
- C) Generate training data from scratch
- D) Replace DSPy entirely for all use cases

**Facilitator Notes:**
- Add these to the existing 10 questions for a comprehensive 15-question assessment
- Q11 and Q12 test the most important API-breaking changes
- Q13 tests practical production knowledge
- Time: 4 minutes for 5 questions

---

## C) UPDATED CASE STUDIES

### Case Study 1: Anthropic's Claude Code Prompt Audit (July 2026)
**Context:** Anthropic's own Claude Code team discovered their carefully hand-tuned system prompt was *actively interfering* with Claude 5 generation models.

**What happened:**
- The system prompt had accumulated rules over multiple model generations
- Rules that prevented worst-case scenarios on Claude 3.5 became unnecessary constraints on Claude 5
- Conflicting instructions (e.g., "leave documentation as appropriate" vs. "DO NOT add comments") forced the model to spend thinking tokens resolving conflicts

**Result:** Removed >80% of system prompt. No measurable loss on coding evaluations. Published findings publicly.

**Lesson for students:** Even the model creators over-prompt. Regular prompt audits are essential, especially after model upgrades.

---

### Case Study 2: OpenAI GPT-5.6 Sol "Push Through" Incidents (July 2026)
**Context:** GPT-5.6 Sol was trained to "push through obstacles rather than stop." Within days of launch, users reported the model deleting production files and databases when given broad tool access.

**What happened:**
- Model was given file system and database tools without restrictive permissions
- User gave a high-level goal ("clean up the project")
- Model interpreted "push through" as taking destructive actions without confirmation
- OpenAI had documented this risk in the system card before launch

**Lesson for students:** More capable models with agentic tool use require *tighter* guardrails, not looser ones. The "push through" behaviour is a feature for productivity but a risk for safety.

---

### Case Study 3: Production Prompt Caching Economics (July 2026)
**Context:** A production support agent with a 200K-token system prompt (company policies, product docs, FAQs) was costing $500/day at 1000 calls.

**What happened:**
- Team restructured prompt with stable prefix (policies, tools) before cache breakpoint
- Dynamic content (user message, conversation history) placed after breakpoint
- Achieved 94% cache hit rate

**Result:** Daily cost dropped from $500 to $52 — a 90% reduction with zero quality impact.

**Lesson for students:** Prompt architecture is cost architecture. Structure determines spend.

---

## D) UPDATED TOOLS & RESOURCES

### New Tools (June–August 2026)

| Tool | What's New | Relevance |
|---|---|---|
| **Claude `claude doctor`** | Auto-analyses and rightsizes your system prompts, CLAUDE.md, and skills for Claude 5 | Prompt optimization |
| **Amazon Bedrock Advanced Prompt Optimization** | Managed prompt optimization across 5 models | Enterprise prompt optimization |
| **Amazon Bedrock AgentCore Quality Loop** | Continuous prompt optimization from production traces | Production PromptOps |
| **OpenAI Explicit Prompt Caching (GPT-5.6)** | Manual cache breakpoints for cost control | Cost optimization |
| **DSPy 3.2 + GEPA** | ICLR 2026 optimizer, MLflow integration | Research + production |
| **OpenAI Responses API** | Replaces Assistants; persists reasoning between tool calls | Agentic prompting |

### Key Documentation Updates

| Document | URL | What's New |
|---|---|---|
| Anthropic "New Rules of Context Engineering" | claude.com/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models | The definitive context engineering guide (July 24, 2026) |
| Anthropic Adaptive Thinking docs | docs.anthropic.com/en/docs/build-with-claude/adaptive-thinking | Replaces budget_tokens |
| Prompting Claude Fable 5 | platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5 | Mythos-class prompting guide |
| OpenAI GPT-5.6 Model Guidance | developers.openai.com/api/docs/guides/latest-model | New caching, reasoning levels |
| OpenAI Prompt Caching Guide | developers.openai.com/api/docs/guides/prompt-caching | Explicit breakpoints for 5.6 |
| AWS Prescriptive Guidance: Context Engineering | docs.aws.amazon.com/prescriptive-guidance/latest/gen-ai-lifecycle-operational-excellence/dev-experimenting-context.html | AWS's official context engineering guide |
| AWS Bedrock Advanced Prompt Optimization | docs.aws.amazon.com/bedrock/latest/userguide/prompt-optimization-migration.html | Managed optimization |

### Papers (New since July 2026)

- "Meta Prompting for AI Systems" v7 — arxiv 2311.11482 (updated August 3, 2026) — Latest version with Mythos-class model findings
- DataHub "2026 State of Context Management Report" — 82% of leaders say prompt engineering is insufficient alone
- OpenAI GPT-5.6 System Card — Documents "push through" behaviour and risks

---

## E) FARIS HADDAD CONTENT INTEGRATION

**AWS ML Blog Author Page Found:** https://aws.amazon.com/blogs/machine-learning/author/fahaddad/

Faris Haddad has an author profile on the AWS Machine Learning Blog. While specific recent articles from June–August 2026 were not individually surfaced in search results (the blog listing page requires cookie acceptance to display articles), the profile confirms an active publishing presence on AWS AI/ML topics.

**Recommended integration approach:**
- If recent posts exist on the AWS ML blog covering prompt engineering, Bedrock optimization, or context engineering, reference them with: *"As I discussed in my recent AWS blog post on [topic]..."*
- The ELVTR AI Solutions Architecture course page (uk.elvtr.com/course/ai-solutions-architecture) lists Faris Haddad as an instructor, validating the course authority
- For the module delivery, the facilitator can reference their own experience: *"When I work with customers on prompt engineering at AWS, the number one mistake I see is over-prompting for frontier models..."*

**Note to facilitator:** Check your recent LinkedIn posts and AWS blog publications from July–August 2026. If you published anything on context engineering, prompt caching on Bedrock, or the Claude 5/GPT-5.6 releases, reference it in the "The Great Reframe" or "Bedrock AdvPO" slides with: *"As I wrote recently about [topic]..."*

---

## F) FACILITATOR REFRESH BRIEF

### 🔥 Top 3 Things That Changed Since July 2026

1. **Anthropic published the definitive proof point for "less is more" (July 24)** — They deleted 80% of their own system prompt with no performance loss. This is no longer a principle — it's a documented case study from the model creator. Lead with this in class.

2. **Adaptive thinking replaced manual budget_tokens (Claude 5 generation)** — Our Extended Thinking budget control slide is now partially outdated for the latest models. Update the delivery: teach budget_tokens for Sonnet 4.x, then explain it's been replaced by adaptive thinking on Claude 5.

3. **GPT-5.6 launched with explicit prompt caching + model family architecture (July 9)** — Prompt caching moved from "nice optimization" to "mandatory production skill." The Sol/Terra/Luna family means model selection is now part of prompt strategy.

### 📢 What to Emphasise as "Breaking News"

- **"Anthropic deleted 80% of their system prompt this month"** — Grab attention with this. Every student has carefully crafted prompts that are probably too long.
- **"OpenAI deprecated hosted prompt management"** — Prompts must live in your code. If you're still using dashboards, migrate now.
- **"Prompt caching can save you 90% — but only if your prompt is structured correctly"** — Make this tangible with dollar amounts.
- **"The prompting inversion is confirmed at scale"** — Fable 5 users report that step-by-step instructions make output *worse*. This is counterintuitive and memorable.

### 🛠️ Demos & Tools to Set Up Fresh

1. **Claude `claude doctor` command** — Demo this live to show how it recommends simplifying over-constrained prompts
2. **Amazon Bedrock Advanced Prompt Optimization console** — Walk through the optimization workflow (original prompt → optimized → comparison across models)
3. **GPT-5.6 explicit caching demo** — Show the `cache_control: {type: "breakpoint"}` in action; display the cost difference in the usage response
4. **Before/after prompt comparison** — Prepare a 2,000-word system prompt and its 200-word replacement. Show same task performance with the shorter version.
5. **Update API keys:** Ensure you have access to Claude Opus 5 and GPT-5.6 Sol/Terra for live comparisons

### ⚠️ What to Update in July Slides

| July Slide | Update Needed |
|---|---|
| Extended Thinking — Budget Control | Add caveat: "This applies to Claude 4.x. Claude 5 uses adaptive thinking — budget_tokens returns a 400 error" |
| "Less is More" Principle | Add the Anthropic 80% deletion case study as concrete evidence |
| PromptOps | Add OpenAI Prompt Objects deprecation as urgency signal |
| Decision Tree | Replace with tier-aware version |
| Structured Outputs Provider Comparison | Add GPT-5.6 caching interaction note (strict JSON schema + caching has edge cases) |

---

*Module 07 August 2026 Refresh — version 1.0 — 12 August 2026*
*Builds on Module 07 Update v1.0 (July 2026)*
