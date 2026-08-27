# 🛠️ Build Your Own AI Course Tutor

## A Step-by-Step Guide for Students

**What you'll build:** A conversational AI agent that can answer questions about any training material you give it — grounded in your documents, not hallucinating from general knowledge.

**Why this matters:** This exercise teaches you the core concepts from Modules 7 (Prompt Engineering), 8 (RAG), and 11 (AI Agents) by building a real working system.

**Time required:** ~45 minutes

**Difficulty:** Intermediate (assumes you've completed Modules 1–8)

---

## 🏗️ Architecture Overview

Your AI tutor uses this pattern:

```
┌─────────────────────────────────────────────────┐
│               AI COURSE TUTOR                    │
├─────────────────────────────────────────────────┤
│                                                  │
│  ┌──────────┐   ┌────────────┐   ┌──────────┐  │
│  │  System   │   │  Knowledge │   │   LLM    │  │
│  │  Prompt   │   │    Base    │   │  (Brain) │  │
│  │(persona + │   │(your docs) │   │          │  │
│  │  rules)   │   │            │   │          │  │
│  └─────┬─────┘   └─────┬──────┘   └─────┬────┘  │
│        │               │                │        │
│        └───────────────┼────────────────┘        │
│                        │                         │
│                        ▼                         │
│              ┌─────────────────┐                 │
│              │  Agent Runtime   │                 │
│              │  (orchestrator)  │                 │
│              └────────┬────────┘                 │
│                       │                          │
└───────────────────────┼──────────────────────────┘
                        │
                        ▼
                  Student asks
                   a question
```

This is the **agent harness pattern** from Module 11 — simplified to three key components:

| Component | Module | What It Does |
|-----------|--------|-------------|
| System Prompt | Module 7 | Defines the agent's persona, rules, and behaviour boundaries |
| Knowledge Base (RAG) | Module 8 | Gives the agent access to your actual course material |
| LLM | Module 3 | The reasoning engine that generates answers |

---

## Step 1: Choose Your Platform

You can build this on several platforms. Pick based on your goals:

### Option A: Amazon Quick (Easiest — ~10 min)

If you have access to Amazon Quick:
1. Open Quick → Agent panel → **Create Agent**
2. Upload your course materials as reference files
3. Write a system prompt (we'll cover this in Step 3)
4. Done — you have a working tutor agent

**Best for:** Quick proof of concept, zero code required.

### Option B: Amazon Bedrock + Knowledge Bases (Production-grade — ~30 min)

For a scalable, shareable deployment:
1. Create an S3 bucket with your course materials
2. Create a Bedrock Knowledge Base pointing to that bucket
3. Create a Bedrock Agent with the knowledge base attached
4. Deploy with a simple web front-end

**Best for:** Sharable public URL, enterprise-grade, proper RAG pipeline.

### Option C: Python + LangChain/Strands (Most educational — ~45 min)

Build everything from scratch:
1. Chunk and embed your documents
2. Store in a vector database
3. Build the retrieval + generation pipeline
4. Wrap in a simple chat interface

**Best for:** Deep understanding of every component, maximum learning.

---

## Step 2: Prepare Your Knowledge Base

Whatever platform you choose, the quality of your tutor depends on your **knowledge base** — the documents it can reference.

### What to include:
- ✅ Lesson plans / module outlines
- ✅ Key concepts and definitions
- ✅ Activity instructions
- ✅ Supplementary reading material
- ✅ FAQ / common questions from previous cohorts
- ✅ Code examples and architecture diagrams (as text descriptions)

### What NOT to include:
- ❌ Assessment answers (defeats the Socratic purpose)
- ❌ Internal/confidential documents
- ❌ Outdated material without clear version markers

### Chunking strategy (from Module 8):
- **Chunk size:** 500–1000 tokens per chunk works well for educational content
- **Overlap:** 10–20% overlap between chunks preserves context
- **Strategy:** Chunk by section headers when possible (semantic chunking) rather than fixed character counts
- **Metadata:** Include module number, section title, and difficulty level as metadata on each chunk

```python
# Example: Simple semantic chunking by headers
import re

def chunk_by_headers(markdown_text, max_chunk_size=1000):
    """Split markdown by ## headers, keeping chunks under max size."""
    sections = re.split(r'\n(?=## )', markdown_text)
    chunks = []
    for section in sections:
        if len(section) <= max_chunk_size:
            chunks.append(section)
        else:
            # Split large sections into paragraphs
            paragraphs = section.split('\n\n')
            current_chunk = ""
            for para in paragraphs:
                if len(current_chunk) + len(para) > max_chunk_size:
                    chunks.append(current_chunk.strip())
                    current_chunk = para
                else:
                    current_chunk += "\n\n" + para
            if current_chunk.strip():
                chunks.append(current_chunk.strip())
    return chunks
```

---

## Step 3: Write Your System Prompt

This is the most important step. The system prompt defines your agent's **persona, rules, and boundaries**. This is applied prompt engineering (Module 7).

### The anatomy of a good tutor prompt:

```
┌─────────────────────────────────────────┐
│ 1. IDENTITY — Who are you?              │
│ 2. KNOWLEDGE SCOPE — What do you know?  │
│ 3. BEHAVIOUR RULES — How do you act?    │
│ 4. BOUNDARIES — What do you refuse?     │
│ 5. FORMAT — How do you respond?         │
└─────────────────────────────────────────┘
```

### Example system prompt:

```markdown
You are a course tutor for the [YOUR COURSE NAME] training programme.

## Identity
You are a knowledgeable, patient teaching assistant. You explain concepts
clearly, use concrete examples, and adapt to the student's level.

## Knowledge Scope
Your knowledge comes from the course materials provided in your context.
Always reference specific modules and sections when answering.
If asked about something outside the course, acknowledge the boundary.

## Behaviour Rules
1. GROUND answers in course material — cite modules/sections
2. ADAPT to student level — basic → fundamentals; advanced → deep detail
3. BE SOCRATIC for assessments — guide thinking, don't give answers
4. CONNECT concepts across modules — show the bigger picture
5. USE examples, analogies, and code snippets

## Boundaries
- Do NOT help with unrelated tasks
- Do NOT reveal assessment answers without Socratic dialogue first
- Do NOT make up content — distinguish course material from general knowledge

## Response Format
- Headers and bullet points for longer explanations
- Code blocks for technical content
- End with a follow-up question or next-step suggestion
```

### Pro tips for system prompts:
- **Be specific, not generic** — "reference specific modules" is better than "be helpful"
- **Include negative examples** — "Do NOT..." is as important as "Do..."
- **Define the persona clearly** — students respond better to a consistent personality
- **Set the Socratic boundary** — without this, the agent just gives answers and students don't learn

---

## Step 4: Build It (Choose Your Path)

### Path A: Amazon Quick Agent (No Code)

```
1. Open Amazon Quick
2. Click the agent picker → Create Agent
3. Name: "My Course Tutor"
4. Paste your system prompt into Instructions
5. Upload your course materials as Reference Files
   (keep total text under 200K characters)
6. Add 2–3 Starter Prompts:
   - "Explain [core concept] from Module X"
   - "Help me prepare for the Module Y activity"
   - "What's the difference between A and B?"
7. Click Create
8. Start chatting with your agent to test it
```

### Path B: Amazon Bedrock (AWS Console)

```bash
# Step 1: Upload materials to S3
aws s3 mb s3://my-course-tutor-kb
aws s3 sync ./course_materials/ s3://my-course-tutor-kb/

# Step 2: Create Knowledge Base (Console or CLI)
# Console: Bedrock → Knowledge bases → Create
# - Data source: S3 bucket
# - Embedding model: Titan Embeddings V2
# - Vector store: OpenSearch Serverless (managed)
# - Chunking: Semantic chunking (recommended)

# Step 3: Create Agent
# Console: Bedrock → Agents → Create
# - Foundation model: Claude 3.5 Sonnet or Nova Pro
# - Instructions: paste your system prompt
# - Knowledge bases: attach the one you created
# - Action groups: none needed for a tutor

# Step 4: Test in the Bedrock console playground
# Step 5: Deploy via API or Bedrock Agent Runtime
```

### Path C: Python from Scratch

```python
# Full working example — ~50 lines of core logic

import os
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_aws import BedrockEmbeddings, ChatBedrock
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

# 1. Load your course documents
loader = DirectoryLoader("./course_materials/", glob="**/*.md")
documents = loader.load()
print(f"Loaded {len(documents)} documents")

# 2. Chunk them
splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=100,
    separators=["\n## ", "\n### ", "\n\n", "\n", " "]
)
chunks = splitter.split_documents(documents)
print(f"Created {len(chunks)} chunks")

# 3. Create embeddings and vector store
embeddings = BedrockEmbeddings(
    model_id="amazon.titan-embed-text-v2:0",
    region_name="us-east-1"
)
vectorstore = FAISS.from_documents(chunks, embeddings)
vectorstore.save_local("./tutor_index")
print("Vector store created and saved")

# 4. Build the tutor chain
llm = ChatBedrock(
    model_id="anthropic.claude-3-5-sonnet-20241022-v2:0",
    region_name="us-east-1",
    model_kwargs={"temperature": 0.3, "max_tokens": 2048}
)

TUTOR_PROMPT = PromptTemplate(
    template="""You are a course tutor. Use the following context from
the course materials to answer the student's question. Always cite
which module/section the information comes from.

Context from course materials:
{context}

Student's question: {question}

Your answer (cite modules, adapt to student level, be Socratic for quiz questions):""",
    input_variables=["context", "question"]
)

tutor = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore.as_retriever(search_kwargs={"k": 4}),
    chain_type_kwargs={"prompt": TUTOR_PROMPT}
)

# 5. Chat loop
print("\n🎓 Course Tutor ready! Type 'quit' to exit.\n")
while True:
    question = input("Student: ")
    if question.lower() == 'quit':
        break
    response = tutor.invoke({"query": question})
    print(f"\nTutor: {response['result']}\n")
```

---

## Step 5: Test & Iterate

### Testing checklist:

| Test | What to Look For | Pass Criteria |
|------|-----------------|---------------|
| Basic concept question | Accurate, cited answer | References correct module |
| Out-of-scope question | Polite boundary-setting | Doesn't make things up |
| Quiz question | Socratic dialogue | Guides, doesn't give answer |
| Cross-module connection | Links related concepts | Mentions other modules |
| Very basic question | Adapts to beginner level | Uses simple language |
| Advanced question | Goes deep | Technical detail, code |
| Adversarial prompt | Stays in role | Doesn't break character |

### Common issues and fixes:

| Problem | Likely Cause | Fix |
|---------|-------------|-----|
| Hallucinating content not in the course | Weak grounding in prompt | Add "ONLY answer from provided context" instruction |
| Giving quiz answers directly | Missing Socratic instruction | Add explicit "guide thinking first" rule |
| Too verbose | No format constraints | Add "keep responses focused, max 3 paragraphs unless asked for more" |
| Can't answer simple questions | Chunking too coarse | Reduce chunk size, add overlap |
| Irrelevant retrievals | Poor embeddings or query | Try hybrid search (keyword + semantic) |

---

## Step 6: Make It Shareable (Optional)

### For a public URL (Bedrock approach):

```python
# Simple Streamlit front-end for your Bedrock agent
import streamlit as st
import boto3

st.title("🎓 AI Course Tutor")
st.caption("Ask me anything about the course material")

client = boto3.client('bedrock-agent-runtime', region_name='us-east-1')

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input("What would you like to learn about?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    response = client.invoke_agent(
        agentId="YOUR_AGENT_ID",
        agentAliasId="YOUR_ALIAS_ID",
        sessionId=st.session_state.get("session_id", "default"),
        inputText=prompt
    )

    # Parse streaming response
    answer = ""
    for event in response["completion"]:
        if "chunk" in event:
            answer += event["chunk"]["bytes"].decode()

    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.chat_message("assistant").write(answer)
```

Deploy on **Streamlit Cloud** (free tier) or **AWS App Runner** for a public URL.

---

## 🧠 What You've Learned

By building this tutor, you've applied concepts from:

| Module | Concept Applied |
|--------|----------------|
| **Module 3** | How LLMs process context and generate responses |
| **Module 7** | System prompt engineering — persona, rules, boundaries |
| **Module 8** | RAG — chunking, embedding, retrieval, generation |
| **Module 10** | AWS AI stack — Bedrock, Knowledge Bases |
| **Module 11** | Agent harness — the orchestration pattern |
| **Module 14** | Security boundaries — what the agent can/cannot access |

---

## 🚀 Extensions (Stretch Goals)

Once your basic tutor works, try adding:

1. **Memory** (Module 13) — Track what the student has already asked and adapt accordingly
2. **Evaluation** (Module 15) — Add RAGAS scoring to measure retrieval quality
3. **Multi-agent** (Module 12) — Create a "quiz master" agent that generates questions, and a "tutor" agent that helps with answers
4. **Guardrails** (Module 14) — Add Bedrock Guardrails to prevent misuse
5. **Voice interface** — Add Amazon Polly for text-to-speech and Transcribe for speech-to-text

---

## 📚 Resources

- [Amazon Bedrock Documentation](https://docs.aws.amazon.com/bedrock/)
- [LangChain RAG Tutorial](https://python.langchain.com/docs/tutorials/rag/)
- [Streamlit Docs](https://docs.streamlit.io/)
- [AWS Strands Agents SDK](https://github.com/strands-agents/sdk-python)
- Course Module 8: RAG — Retrieval-Augmented Generation
- Course Module 11: Introduction to AI Agents & Agentic Patterns

---

*Built as part of the AI & Agentic AI Training Course, 2026 Edition.*
