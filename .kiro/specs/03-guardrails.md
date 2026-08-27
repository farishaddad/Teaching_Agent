# Spec: Guardrails Module

## Goal
Implement comprehensive safety guardrails using Amazon Bedrock Guardrails to ensure the agent stays on-topic, blocks harmful content, and protects student privacy.

## Inputs
- Student messages (input filtering)
- LLM responses (output filtering)
- Guardrail configuration (policies)

## Outputs
- Filtered/blocked content with appropriate user messaging
- Guardrail violation logs for admin review
- Configuration that can be demonstrated in the tutorial

## Guardrail Policies to Implement

### 1. Topic Denial
- ALLOW: Agentic AI, AI agents, LLMs, prompt engineering, RAG, tool use, multi-agent systems, AI safety, AI ethics, course logistics
- DENY: Everything else (politics, religion, personal advice, coding homework unrelated to agents, general chat)
- Denial message: "I'm focused on Agentic AI topics from your course. Could you rephrase your question to relate to the course material?"

### 2. Content Filtering
- Block: Hate speech, sexual content, violence, self-harm (HIGH threshold)
- Block: Insults, profanity (MEDIUM threshold)

### 3. PII Protection
- REDACT (in logs): Email addresses, phone numbers, physical addresses
- BLOCK (in responses): Never output student personal data

### 4. Word/Phrase Filters
- Block: Competitor product promotions, jailbreak attempts
- Managed word list: Common prompt injection phrases

### 5. Contextual Grounding
- Enable grounding check: Responses must be supported by retrieved context
- Hallucination threshold: 0.7 (block if <70% grounded)

## Files to Create
- `backend/guardrails/__init__.py`
- `backend/guardrails/config.py` — Guardrail ID/version config, policy definitions
- `backend/guardrails/middleware.py` — Pre/post processing middleware
- `backend/guardrails/violation_handler.py` — User-friendly violation messages + logging
- `infrastructure/guardrails_stack.py` — CDK: Bedrock Guardrail resource
- `tests/test_guardrails.py` — Tests with known violating inputs

## Acceptance Criteria
- [ ] Off-topic questions are politely declined with redirect to course topics
- [ ] Toxic/harmful content is blocked before reaching the LLM
- [ ] PII is never stored in plain text in interaction logs
- [ ] Guardrail violations are logged separately for admin monitoring
- [ ] Students see friendly messages (not raw error codes) when guardrails activate
- [ ] Guardrail config is version-controlled and deployed via CDK
- [ ] Contextual grounding prevents hallucinated answers

## Do Not Do
- Do NOT implement custom content filtering — use Bedrock Guardrails exclusively
- Do NOT reveal guardrail internals to students (don't say "blocked by guardrail policy X")
- Do NOT log the full PII that was redacted — only log that redaction occurred
