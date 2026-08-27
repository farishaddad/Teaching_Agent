# 🎭 Animated Avatar Tutor — Architecture Spec

## Vision

Students interact with a video-chat interface where an animated version of you responds to their questions in your voice and likeness, powered by the same RAG knowledge base. It feels like asking you directly — but available 24/7.

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                    STUDENT BROWSER / APP                             │
│                                                                      │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────────────┐   │
│  │ 🎤 Mic Input │    │ 💬 Text Chat │    │ 🎥 Avatar Video      │   │
│  │ (optional)   │    │   (primary)  │    │   Stream (output)    │   │
│  └──────┬───────┘    └──────┬───────┘    └──────────▲───────────┘   │
│         │                   │                       │               │
└─────────┼───────────────────┼───────────────────────┼───────────────┘
          │                   │                       │
          ▼                   ▼                       │
┌─────────────────────────────────────────────────────┼───────────────┐
│                      ORCHESTRATION LAYER             │               │
│                                                      │               │
│  ┌──────────────┐    ┌──────────────────────────────┼────────────┐  │
│  │ STT (Speech  │    │        AI TUTOR BACKEND       │            │  │
│  │ to Text)     │    │                               │            │  │
│  │              │    │  ┌─────────┐  ┌───────────┐  │            │  │
│  │ Amazon       │    │  │ RAG     │  │  System   │  │            │  │
│  │ Transcribe   │    │  │ Pipeline│  │  Prompt   │  │            │  │
│  │ Streaming    │    │  │ (Bedrock│  │  (Tutor   │  │            │  │
│  └──────┬───────┘    │  │  KB)    │  │  persona) │  │            │  │
│         │            │  └────┬────┘  └─────┬─────┘  │            │  │
│         │            │       │             │         │            │  │
│         ▼            │       ▼             ▼         │            │  │
│  ┌──────────────┐    │  ┌────────────────────────┐   │            │  │
│  │ Query text   │───▶│  │   Bedrock Agent /      │   │            │  │
│  │              │    │  │   LLM + RAG retrieval   │   │            │  │
│  └──────────────┘    │  └───────────┬────────────┘   │            │  │
│                      │              │                 │            │  │
│                      └──────────────┼─────────────────┘            │  │
│                                     │                              │  │
│                                     ▼                              │  │
│                      ┌──────────────────────────────┐              │  │
│                      │      TEXT RESPONSE            │              │  │
│                      │  (tutor's answer as text)    │              │  │
│                      └──────────────┬───────────────┘              │  │
│                                     │                              │  │
│                      ┌──────────────▼───────────────┐              │  │
│                      │      TTS (Text to Speech)    │              │  │
│                      │      YOUR CLONED VOICE       │              │  │
│                      │                              │              │  │
│                      │  ElevenLabs / PlayHT API     │              │  │
│                      └──────────────┬───────────────┘              │  │
│                                     │ audio stream                 │  │
│                                     ▼                              │  │
│                      ┌──────────────────────────────┐              │  │
│                      │    AVATAR ANIMATION ENGINE   │──────────────┘  │
│                      │                              │                 │
│                      │  HeyGen Interactive Avatar   │                 │
│                      │  OR Synthesia Express API    │                 │
│                      │  OR D-ID Agents API          │                 │
│                      │                              │                 │
│                      │  Input: audio stream         │                 │
│                      │  Output: lip-synced video    │                 │
│                      └──────────────────────────────┘                 │
│                                                                       │
└───────────────────────────────────────────────────────────────────────┘
```

---

## Component Breakdown

### 1. Voice Clone — Your Voice

| Option | Quality | Setup Time | Cost | Notes |
|--------|---------|-----------|------|-------|
| **ElevenLabs Instant Clone** | Very good | 5 min | $5–22/mo | 30 sec audio sample needed. Best bang for buck. |
| **ElevenLabs Professional Clone** | Excellent | 2–3 days | $99 one-time | 3+ hours of audio. Near-perfect match. |
| **PlayHT 2.0** | Good | 10 min | $29/mo | 30 sec sample. Slightly less natural than ElevenLabs. |
| **Amazon Polly Custom Voice** | Enterprise | Weeks | Enterprise pricing | Requires working with AWS team. Best for scale. |

**Recommendation:** Start with **ElevenLabs Instant Clone** — record 30–60 seconds of you speaking naturally about AI (this way the clone inherits your cadence on technical topics). Upgrade to Professional if quality matters for a polished product.

#### Recording Requirements

```
VOICE CLONE RECORDING CHECKLIST:
─────────────────────────────────
□ Quiet room, no echo (closet with clothes works well)
□ Consistent distance from mic (30cm / 12 inches)
□ Speak naturally — the same way you'd teach
□ Content: explain an AI concept for 30-60 seconds
□ No background music or noise
□ Format: WAV or MP3, 44.1kHz
□ Do NOT read from a script robotically — be conversational
```

---

### 2. Avatar — Your Likeness

| Option | Type | Latency | Cost | Best For |
|--------|------|---------|------|----------|
| **HeyGen Interactive Avatar** | Real-time lip-sync | ~1–2 sec | $59/mo (Creator) | Live conversational avatar |
| **Synthesia Express** | Near-real-time | ~3–5 sec | $29/mo | Pre-recorded style, high quality |
| **D-ID Agents** | Real-time streaming | ~1–2 sec | $25/mo (Lite) | Budget option, good quality |
| **Tavus Conversational Video** | Real-time | <1 sec | Custom pricing | Lowest latency, enterprise |

**Recommendation:** **HeyGen Interactive Avatar** — best balance of quality, real-time interaction, and API maturity. Their Streaming Avatar API lets you pipe in audio and get back lip-synced video in real time.

#### Avatar Recording Requirements

```
AVATAR VIDEO RECORDING CHECKLIST:
──────────────────────────────────
□ 2–5 minutes of you speaking to camera
□ Well-lit (ring light or window light from front)
□ Neutral background (solid colour or clean office)
□ Business casual or however you'd dress to teach
□ Look directly at camera (eye contact with students)
□ Natural hand gestures and head movement
□ Multiple facial expressions (explaining, thinking, smiling)
□ Resolution: 1080p minimum, 4K preferred
□ Frame: head and shoulders (portrait orientation)
□ No other people visible
```

---

### 3. AI Backend — The Tutor Brain

This is the same RAG-powered agent we already built:

```python
# Architecture decision tree:

If you want ZERO code maintenance:
  → Amazon Bedrock Agent + Knowledge Base
  → API call: InvokeAgent(inputText=student_question)
  → Returns: text answer grounded in course materials

If you want MAXIMUM control:
  → Custom Python (LangChain/Strands + FAISS/OpenSearch)
  → Full control over chunking, retrieval, prompt
  → Self-hosted on ECS/Lambda

If you want FASTEST setup:
  → Amazon Quick Agent (already built!)
  → No public URL, but works for internal students
```

---

### 4. Orchestration — Gluing It Together

```python
# Pseudocode: Full pipeline for one student interaction

async def handle_student_message(text_or_audio):
    # 1. If audio, transcribe
    if is_audio(text_or_audio):
        text = await transcribe(text_or_audio)  # Amazon Transcribe
    else:
        text = text_or_audio

    # 2. Get tutor response (RAG + LLM)
    tutor_response = await bedrock_agent.invoke(text)

    # 3. Convert response to speech (your voice)
    audio_stream = await elevenlabs.text_to_speech(
        text=tutor_response,
        voice_id="YOUR_CLONED_VOICE_ID",
        model="eleven_turbo_v2_5",  # Low latency
        stream=True
    )

    # 4. Animate avatar with the audio
    video_stream = await heygen.streaming_avatar(
        avatar_id="YOUR_AVATAR_ID",
        audio_stream=audio_stream
    )

    # 5. Stream video back to student
    return video_stream, tutor_response  # Video + text fallback
```

---

## Deployment Architecture

```
┌──────────────────────────────────────────────────────────┐
│                   AWS DEPLOYMENT                          │
│                                                           │
│  ┌─────────────┐     ┌──────────────────────────────┐    │
│  │ CloudFront  │────▶│  S3 (static front-end)       │    │
│  │ (CDN)       │     │  React/Next.js chat UI       │    │
│  └─────────────┘     └──────────────────────────────┘    │
│                                                           │
│  ┌─────────────┐     ┌──────────────────────────────┐    │
│  │ API Gateway │────▶│  Lambda / ECS                 │    │
│  │ (WebSocket) │     │  Orchestration logic          │    │
│  └─────────────┘     │  - Calls Bedrock Agent        │    │
│                       │  - Calls ElevenLabs TTS       │    │
│                       │  - Calls HeyGen Avatar        │    │
│                       └──────────────────────────────┘    │
│                                                           │
│  ┌─────────────────────────────────────────────────────┐  │
│  │  Amazon Bedrock                                     │  │
│  │  - Agent (tutor persona + RAG)                      │  │
│  │  - Knowledge Base (course materials in S3)          │  │
│  │  - Guardrails (content safety)                      │  │
│  └─────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────┘

External APIs:
  → ElevenLabs (voice clone TTS)
  → HeyGen (avatar animation)
```

---

## Cost Estimate (Monthly)

| Component | Service | Est. Monthly Cost |
|-----------|---------|------------------|
| Voice clone | ElevenLabs Starter | $5–22 |
| Avatar generation | HeyGen Creator | $59 |
| AI backend | Bedrock (Claude Sonnet) | ~$50–150 (usage-based) |
| Knowledge Base | Bedrock KB + OpenSearch Serverless | ~$25–50 |
| Hosting | Lambda + S3 + CloudFront | ~$5–20 |
| **TOTAL** | | **~$150–300/mo** |

For a class of 30 students asking ~10 questions/day each, this is roughly **$5–10 per student per month**.

---

## Implementation Roadmap

| Week | Milestone | Deliverable |
|------|-----------|-------------|
| **Week 1** | Record materials + set up voice clone | 60-sec voice recording → ElevenLabs clone |
| **Week 1** | Record avatar video | 3-min video → HeyGen avatar created |
| **Week 2** | Deploy Bedrock Agent + KB | Working text-based tutor on Bedrock |
| **Week 2** | Integrate TTS pipeline | Tutor responds in your voice (audio only) |
| **Week 3** | Connect HeyGen streaming avatar | Full video response pipeline working |
| **Week 3** | Build front-end chat UI | React/Next.js with video player + text fallback |
| **Week 4** | Test with 5 students | Gather feedback on latency, quality, accuracy |
| **Week 4** | Polish + deploy to production URL | Public HTTPS URL students can access |

---

## Latency Budget

For a conversational experience, total response time needs to stay under **5 seconds**:

```
Student sends message          0 ms
  ↓
Bedrock Agent (RAG + LLM)  1500–3000 ms
  ↓
ElevenLabs TTS (streaming)   200–500 ms  (first chunk)
  ↓
HeyGen Avatar (streaming)    500–1000 ms (first frame)
  ↓
Student sees avatar speak   2200–4500 ms total
```

✅ Achievable with streaming at every step. The avatar starts moving before the full response is generated.

---

## Risk & Mitigations

| Risk | Impact | Mitigation |
|------|--------|-----------|
| Avatar looks uncanny | Students disengage | Offer text-only fallback; test with focus group first |
| Voice clone sounds slightly off | Breaks immersion | Use Professional Clone tier; record in same mic/room as teaching |
| High latency on complex questions | Frustrating UX | Show "thinking" animation; stream partial responses |
| Cost overrun with high usage | Budget exceeded | Set per-student daily query limits; cache common Q&A pairs |
| Hallucination despite RAG | Incorrect teaching | Bedrock Guardrails + verification prompt + "I'm not sure" fallback |
| Platform API changes/outages | Service disruption | Abstract vendor APIs behind interface; have text-only fallback |

---

## Alternative: Simpler "Talking Head" Version

If full real-time interaction is too complex for v1, consider a **pre-rendered approach**:

1. Student types question → gets text answer (existing agent)
2. System generates a 30-sec video of "you" reading the answer
3. Video appears in chat within 10–15 seconds

This is cheaper (~$30/mo with D-ID) and simpler to build, but less interactive. Good for a v0.5 pilot.

---

## Next Steps

1. **Record your voice sample** (30–60 seconds, quiet room, natural speech about AI)
2. **Record your avatar video** (3 minutes, good lighting, to camera)
3. **Decide: real-time or pre-rendered** for v1
4. I can help build the Bedrock Agent + KB deployment and the orchestration Lambda

---

*Architecture spec — AI & Agentic AI Course Avatar Tutor*  
*Last updated: July 2026*
