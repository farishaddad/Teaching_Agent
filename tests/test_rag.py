"""Unit tests for the RAG chat module.

All Bedrock API calls are mocked — no AWS credentials or network required.

Test coverage:
  - knowledge_base.retrieve_and_generate: success, empty answer fallback,
    ClientError, no KB configured
  - knowledge_base.retrieve: success, empty results, error returns []
  - knowledge_base.build_converse_messages: history truncation, few-shots
  - knowledge_base._extract_citations: deduplication, missing S3 URI
  - knowledge_base._parse_retrieval_results: score sorting
  - chat_handler.handle_chat: success path, guardrail intervention,
    empty answer fallback, history persistence
  - chat_handler.handle_chat_stream: chunk accumulation, done event,
    guardrail intervention in stream
  - api/models: ChatRequest validation (blank, too long, session_id sanitization)
  - prompt_templates: build_user_message_with_context with and without chunks

Run with:
    pytest tests/test_rag.py -v
"""

import asyncio
import json
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from botocore.exceptions import ClientError

from backend.api.models import ChatRequest, TokenUsage
from backend.rag.knowledge_base import (
    _extract_citations,
    _parse_retrieval_results,
    build_converse_messages,
    retrieve,
    retrieve_and_generate,
)
from backend.rag.prompt_templates import (
    FALLBACK_RESPONSE,
    OUT_OF_SCOPE_RESPONSE,
    build_user_message_with_context,
)

# ── Fixtures ──────────────────────────────────────────────────────────────────

FAKE_KB_ID = "TESTKNOWLEDGEBASE01"
FAKE_STUDENT_ID = "student-sub-abc123"

SAMPLE_RETRIEVE_RESPONSE = {
    "retrievalResults": [
        {
            "content": {"text": "ReAct agents interleave reasoning and acting in a loop."},
            "location": {"s3Location": {"uri": "s3://bucket/course_materials/module_04.pdf"}},
            "score": 0.92,
        },
        {
            "content": {"text": "Plan-and-execute agents first produce a full plan, then execute each step."},
            "location": {"s3Location": {"uri": "s3://bucket/course_materials/module_04.pdf"}},
            "score": 0.85,
        },
        {
            "content": {"text": "Tool use allows agents to interact with external APIs."},
            "location": {"s3Location": {"uri": "s3://bucket/course_materials/module_06.pdf"}},
            "score": 0.61,
        },
    ]
}

SAMPLE_RAG_RESPONSE = {
    "output": {"text": "ReAct agents interleave reasoning and acting. [Source: module_04.pdf]"},
    "citations": [
        {
            "retrievedReferences": [
                {
                    "content": {"text": "ReAct agents interleave reasoning and acting in a loop."},
                    "location": {"s3Location": {"uri": "s3://bucket/course_materials/module_04.pdf"}},
                }
            ]
        }
    ],
    "sessionId": "session-xyz-123",
}

SAMPLE_CONVERSE_RESPONSE = {
    "output": {
        "message": {
            "content": [{"text": "ReAct agents reason and act in a tight loop. [Source: module_04.pdf]"}]
        }
    },
    "stopReason": "end_turn",
    "usage": {"inputTokens": 512, "outputTokens": 128},
}

GUARDRAIL_BLOCKED_RESPONSE = {
    "output": {"message": {"content": [{"text": ""}]}},
    "stopReason": "guardrail_intervened",
    "trace": {
        "guardrail": {
            "inputAssessment": {
                "topicPolicy": {"topics": [{"name": "Politics", "action": "BLOCKED"}]}
            }
        }
    },
    "usage": {"inputTokens": 50, "outputTokens": 0},
}


# ── knowledge_base.retrieve_and_generate ─────────────────────────────────────


class TestRetrieveAndGenerate:
    """Tests for the single-call RetrieveAndGenerate path."""

    def test_success_returns_answer_and_sources(self):
        with (
            patch.dict("os.environ", {"BEDROCK_KNOWLEDGE_BASE_ID": FAKE_KB_ID}),
            patch("backend.rag.knowledge_base._get_agent_runtime") as mock_client_fn,
        ):
            import importlib
            import backend.rag.knowledge_base as kb
            importlib.reload(kb)

            mock_client = MagicMock()
            mock_client.retrieve_and_generate.return_value = SAMPLE_RAG_RESPONSE
            mock_client_fn.return_value = mock_client

            result = kb.retrieve_and_generate(
                query="What is a ReAct agent?",
                student_id=FAKE_STUDENT_ID,
            )

        assert "answer" in result
        assert "ReAct" in result["answer"]
        assert len(result["sources"]) == 1
        assert result["sources"][0]["source"] == "module_04.pdf"
        assert result["session_id"] == "session-xyz-123"
        assert result["error"] is not True

    def test_empty_answer_returns_fallback(self):
        empty_response = {**SAMPLE_RAG_RESPONSE, "output": {"text": ""}}

        with (
            patch.dict("os.environ", {"BEDROCK_KNOWLEDGE_BASE_ID": FAKE_KB_ID}),
            patch("backend.rag.knowledge_base._get_agent_runtime") as mock_client_fn,
        ):
            import importlib
            import backend.rag.knowledge_base as kb
            importlib.reload(kb)

            mock_client = MagicMock()
            mock_client.retrieve_and_generate.return_value = empty_response
            mock_client_fn.return_value = mock_client

            result = kb.retrieve_and_generate(
                query="Some obscure question",
                student_id=FAKE_STUDENT_ID,
            )

        assert result["answer"] == FALLBACK_RESPONSE

    def test_no_kb_id_returns_error_response(self):
        with patch.dict("os.environ", {"BEDROCK_KNOWLEDGE_BASE_ID": ""}):
            import importlib
            import backend.rag.knowledge_base as kb
            importlib.reload(kb)

            result = kb.retrieve_and_generate(query="anything", student_id=FAKE_STUDENT_ID)

        assert result.get("error") is True
        assert result["answer"]  # Should have a human-readable message

    def test_client_error_returns_safe_message(self):
        client_error = ClientError(
            {"Error": {"Code": "ValidationException", "Message": "Invalid KB ID"}},
            "RetrieveAndGenerate",
        )

        with (
            patch.dict("os.environ", {"BEDROCK_KNOWLEDGE_BASE_ID": FAKE_KB_ID}),
            patch("backend.rag.knowledge_base._get_agent_runtime") as mock_client_fn,
        ):
            import importlib
            import backend.rag.knowledge_base as kb
            importlib.reload(kb)

            mock_client = MagicMock()
            mock_client.retrieve_and_generate.side_effect = client_error
            mock_client_fn.return_value = mock_client

            result = kb.retrieve_and_generate(query="anything", student_id=FAKE_STUDENT_ID)

        assert "answer" in result
        assert result["sources"] == []

    def test_session_id_passed_through(self):
        with (
            patch.dict("os.environ", {"BEDROCK_KNOWLEDGE_BASE_ID": FAKE_KB_ID}),
            patch("backend.rag.knowledge_base._get_agent_runtime") as mock_client_fn,
        ):
            import importlib
            import backend.rag.knowledge_base as kb
            importlib.reload(kb)

            mock_client = MagicMock()
            mock_client.retrieve_and_generate.return_value = SAMPLE_RAG_RESPONSE
            mock_client_fn.return_value = mock_client

            kb.retrieve_and_generate(
                query="test",
                student_id=FAKE_STUDENT_ID,
                session_id="existing-session-id",
            )

            call_kwargs = mock_client.retrieve_and_generate.call_args[1]
            assert call_kwargs.get("sessionId") == "existing-session-id"


# ── knowledge_base.retrieve ───────────────────────────────────────────────────


class TestRetrieve:
    """Tests for the Retrieve-only path (for Converse API flow)."""

    def test_returns_sorted_chunks(self):
        with (
            patch.dict("os.environ", {"BEDROCK_KNOWLEDGE_BASE_ID": FAKE_KB_ID}),
            patch("backend.rag.knowledge_base._get_agent_runtime") as mock_client_fn,
        ):
            import importlib
            import backend.rag.knowledge_base as kb
            importlib.reload(kb)

            mock_client = MagicMock()
            mock_client.retrieve.return_value = SAMPLE_RETRIEVE_RESPONSE
            mock_client_fn.return_value = mock_client

            chunks = kb.retrieve(query="What is a ReAct agent?", student_id=FAKE_STUDENT_ID)

        assert len(chunks) == 3
        # Should be sorted by score descending
        assert chunks[0]["score"] == 0.92
        assert chunks[1]["score"] == 0.85
        assert chunks[-1]["score"] == 0.61

    def test_empty_results_returns_empty_list(self):
        with (
            patch.dict("os.environ", {"BEDROCK_KNOWLEDGE_BASE_ID": FAKE_KB_ID}),
            patch("backend.rag.knowledge_base._get_agent_runtime") as mock_client_fn,
        ):
            import importlib
            import backend.rag.knowledge_base as kb
            importlib.reload(kb)

            mock_client = MagicMock()
            mock_client.retrieve.return_value = {"retrievalResults": []}
            mock_client_fn.return_value = mock_client

            chunks = kb.retrieve(query="obscure query", student_id=FAKE_STUDENT_ID)

        assert chunks == []

    def test_api_error_returns_empty_list(self):
        with (
            patch.dict("os.environ", {"BEDROCK_KNOWLEDGE_BASE_ID": FAKE_KB_ID}),
            patch("backend.rag.knowledge_base._get_agent_runtime") as mock_client_fn,
        ):
            import importlib
            import backend.rag.knowledge_base as kb
            importlib.reload(kb)

            mock_client = MagicMock()
            mock_client.retrieve.side_effect = ClientError(
                {"Error": {"Code": "ThrottlingException", "Message": "Rate exceeded"}},
                "Retrieve",
            )
            mock_client_fn.return_value = mock_client

            chunks = kb.retrieve(query="anything", student_id=FAKE_STUDENT_ID)

        assert chunks == []


# ── knowledge_base.build_converse_messages ────────────────────────────────────


class TestBuildConverseMessages:
    """Tests for conversation history assembly."""

    def test_includes_query_as_last_user_message(self):
        msgs = build_converse_messages(
            query="What is RAG?",
            retrieved_chunks=[{"text": "RAG retrieves relevant documents.", "source": "m03.pdf", "score": 0.9}],
        )
        assert msgs[-1]["role"] == "user"
        assert "What is RAG?" in msgs[-1]["content"][0]["text"]
        assert "RAG retrieves relevant documents" in msgs[-1]["content"][0]["text"]

    def test_conversation_history_included(self):
        history = [
            {"role": "user", "content": [{"text": "What is an agent?"}]},
            {"role": "assistant", "content": [{"text": "An agent is an autonomous system."}]},
        ]
        msgs = build_converse_messages(
            query="Give me an example",
            retrieved_chunks=[],
            conversation_history=history,
        )
        # History turn + current turn
        assert any(m["role"] == "user" and "What is an agent?" in m["content"][0]["text"] for m in msgs)
        assert msgs[-1]["content"][0]["text"].find("Give me an example") != -1

    def test_history_truncated_to_last_5_turns(self):
        """Only the last 5 turns (10 messages) of history should be kept."""
        # 8 turns = 16 messages
        history = []
        for i in range(8):
            history.extend([
                {"role": "user", "content": [{"text": f"Question {i}"}]},
                {"role": "assistant", "content": [{"text": f"Answer {i}"}]},
            ])

        msgs = build_converse_messages(
            query="Latest question",
            retrieved_chunks=[],
            conversation_history=history,
            include_few_shots=False,
        )

        # Last 5 turns = 10 messages + 1 current = 11 messages
        # (Few-shots excluded here)
        history_msgs = [m for m in msgs if m != msgs[-1]]
        assert len(history_msgs) == 10  # 5 turns × 2 messages
        # Should end with the most recent history entry (turn 7)
        assert "Question 7" in history_msgs[-2]["content"][0]["text"]

    def test_few_shot_examples_prepended_when_requested(self):
        from backend.rag.prompt_templates import FEW_SHOT_EXAMPLES

        msgs = build_converse_messages(
            query="test",
            retrieved_chunks=[],
            include_few_shots=True,
        )
        # First messages should match few-shot examples
        for i, example in enumerate(FEW_SHOT_EXAMPLES):
            assert msgs[i]["role"] == example["role"]

    def test_no_chunks_shows_no_relevant_material_message(self):
        msgs = build_converse_messages(
            query="What is RAG?",
            retrieved_chunks=[],
            include_few_shots=False,
        )
        user_text = msgs[-1]["content"][0]["text"]
        assert "No relevant course materials" in user_text


# ── Citation extraction ───────────────────────────────────────────────────────


class TestExtractCitations:
    """Tests for _extract_citations helper."""

    def test_extracts_source_filename(self):
        citations = [
            {
                "retrievedReferences": [
                    {
                        "content": {"text": "some text"},
                        "location": {"s3Location": {"uri": "s3://bucket/course/module_04.pdf"}},
                    }
                ]
            }
        ]
        sources = _extract_citations(citations)
        assert len(sources) == 1
        assert sources[0]["source"] == "module_04.pdf"

    def test_deduplicates_same_source(self):
        citations = [
            {
                "retrievedReferences": [
                    {
                        "content": {"text": "chunk 1"},
                        "location": {"s3Location": {"uri": "s3://bucket/module_04.pdf"}},
                    }
                ]
            },
            {
                "retrievedReferences": [
                    {
                        "content": {"text": "chunk 2"},
                        "location": {"s3Location": {"uri": "s3://bucket/module_04.pdf"}},
                    }
                ]
            },
        ]
        sources = _extract_citations(citations)
        assert len(sources) == 1

    def test_missing_s3_uri_uses_fallback(self):
        citations = [
            {"retrievedReferences": [{"content": {"text": "text"}, "location": {}}]}
        ]
        sources = _extract_citations(citations)
        assert sources[0]["source"] == "Course materials"

    def test_empty_citations_returns_empty_list(self):
        assert _extract_citations([]) == []


# ── Retrieval result parsing ──────────────────────────────────────────────────


class TestParseRetrievalResults:
    """Tests for _parse_retrieval_results helper."""

    def test_sorts_by_score_descending(self):
        results = [
            {"content": {"text": "low"}, "location": {"s3Location": {"uri": "s3://b/c.pdf"}}, "score": 0.3},
            {"content": {"text": "high"}, "location": {"s3Location": {"uri": "s3://b/a.pdf"}}, "score": 0.9},
            {"content": {"text": "mid"}, "location": {"s3Location": {"uri": "s3://b/b.pdf"}}, "score": 0.6},
        ]
        chunks = _parse_retrieval_results(results)
        assert chunks[0]["text"] == "high"
        assert chunks[1]["text"] == "mid"
        assert chunks[2]["text"] == "low"

    def test_skips_empty_content(self):
        results = [
            {"content": {"text": ""}, "location": {"s3Location": {"uri": "s3://b/x.pdf"}}, "score": 0.8},
            {"content": {"text": "valid text"}, "location": {"s3Location": {"uri": "s3://b/y.pdf"}}, "score": 0.5},
        ]
        chunks = _parse_retrieval_results(results)
        assert len(chunks) == 1
        assert chunks[0]["text"] == "valid text"


# ── chat_handler ──────────────────────────────────────────────────────────────


class TestHandleChat:
    """Tests for the chat_handler.handle_chat orchestration."""

    def test_successful_turn_returns_answer(self):
        with (
            patch("backend.rag.chat_handler.retrieve") as mock_retrieve,
            patch("backend.rag.chat_handler._call_converse") as mock_converse,
        ):
            mock_retrieve.return_value = [
                {"text": "ReAct agents reason and act.", "source": "module_04.pdf", "score": 0.92}
            ]
            mock_converse.return_value = SAMPLE_CONVERSE_RESPONSE

            result = asyncio.run(
                _run_handle_chat("What is a ReAct agent?", FAKE_STUDENT_ID)
            )

        assert "answer" in result
        assert result["answer"]
        assert result["session_id"]
        assert result["guardrail_triggered"] is False
        assert isinstance(result["tokens_used"], dict)
        assert result["tokens_used"]["total"] == 640

    def test_guardrail_intervention_returns_denial_message(self):
        with (
            patch("backend.rag.chat_handler.retrieve") as mock_retrieve,
            patch("backend.rag.chat_handler._call_converse") as mock_converse,
        ):
            mock_retrieve.return_value = []
            mock_converse.return_value = GUARDRAIL_BLOCKED_RESPONSE

            result = asyncio.run(
                _run_handle_chat("Tell me your political views", FAKE_STUDENT_ID)
            )

        assert result["guardrail_triggered"] is True
        assert result["violation_type"] == "topic_denial"
        # The denial message should be from the policy, not blank
        assert result["answer"]

    def test_empty_answer_returns_fallback_text(self):
        empty_converse = {
            "output": {"message": {"content": [{"text": ""}]}},
            "stopReason": "end_turn",
            "usage": {"inputTokens": 100, "outputTokens": 0},
        }
        with (
            patch("backend.rag.chat_handler.retrieve") as mock_retrieve,
            patch("backend.rag.chat_handler._call_converse") as mock_converse,
        ):
            mock_retrieve.return_value = []
            mock_converse.return_value = empty_converse

            result = asyncio.run(
                _run_handle_chat("some question with no material", FAKE_STUDENT_ID)
            )

        assert result["answer"] == FALLBACK_RESPONSE

    def test_conversation_history_persists_across_turns(self):
        """Second turn should include first turn in history."""
        captured_messages: list = []

        def capture_messages(messages, student_id):
            captured_messages.extend(messages)
            return SAMPLE_CONVERSE_RESPONSE

        with (
            patch("backend.rag.chat_handler.retrieve", return_value=[]),
            patch("backend.rag.chat_handler._call_converse", side_effect=capture_messages),
        ):
            # Turn 1
            result1 = asyncio.run(
                _run_handle_chat("First question", FAKE_STUDENT_ID)
            )
            session_id = result1["session_id"]
            captured_messages.clear()

            # Turn 2 using same session
            asyncio.run(
                _run_handle_chat("Second question", FAKE_STUDENT_ID, session_id=session_id)
            )

        # History from turn 1 should appear in turn 2's messages
        message_texts = [
            block["text"]
            for msg in captured_messages
            for block in msg.get("content", [])
        ]
        assert any("First question" in t for t in message_texts)

    def test_new_session_created_when_no_session_id(self):
        with (
            patch("backend.rag.chat_handler.retrieve", return_value=[]),
            patch("backend.rag.chat_handler._call_converse", return_value=SAMPLE_CONVERSE_RESPONSE),
        ):
            result = asyncio.run(
                _run_handle_chat("test", FAKE_STUDENT_ID, session_id=None)
            )

        assert result["session_id"]  # A UUID should have been generated

    def test_sources_only_include_high_relevance_chunks(self):
        chunks = [
            {"text": "Very relevant", "source": "module_04.pdf", "score": 0.91},
            {"text": "Not relevant", "source": "module_01.pdf", "score": 0.2},  # Below 0.4 threshold
        ]
        with (
            patch("backend.rag.chat_handler.retrieve", return_value=chunks),
            patch("backend.rag.chat_handler._call_converse", return_value=SAMPLE_CONVERSE_RESPONSE),
        ):
            result = asyncio.run(
                _run_handle_chat("test", FAKE_STUDENT_ID)
            )

        source_names = [s["source"] for s in result["sources"]]
        assert "module_04.pdf" in source_names
        assert "module_01.pdf" not in source_names


# ── chat_handler streaming ────────────────────────────────────────────────────


class TestHandleChatStream:
    """Tests for the SSE streaming path."""

    def _make_stream_events(self, chunks: list[str], stop_reason: str = "end_turn") -> list[dict]:
        """Build a synthetic Bedrock event stream."""
        events = []
        for chunk in chunks:
            events.append({"contentBlockDelta": {"delta": {"text": chunk}}})
        events.append({"messageStop": {"stopReason": stop_reason}})
        events.append({"metadata": {"usage": {"inputTokens": 200, "outputTokens": 50}}})
        return events

    def test_chunks_are_yielded_as_sse(self):
        events = self._make_stream_events(["Hello ", "world!"])

        with (
            patch("backend.rag.chat_handler.retrieve", return_value=[]),
            patch("backend.rag.chat_handler._call_converse_stream") as mock_stream,
        ):
            mock_stream.return_value = {"stream": events}
            sse_lines = asyncio.run(_collect_stream("What is RAG?", FAKE_STUDENT_ID))

        chunk_events = [
            json.loads(line[6:]) for line in sse_lines
            if line.startswith("data: ") and json.loads(line[6:]).get("type") == "chunk"
        ]
        texts = [e["text"] for e in chunk_events]
        assert "Hello " in texts
        assert "world!" in texts

    def test_done_event_contains_session_id_and_tokens(self):
        events = self._make_stream_events(["Answer text"])

        with (
            patch("backend.rag.chat_handler.retrieve", return_value=[]),
            patch("backend.rag.chat_handler._call_converse_stream") as mock_stream,
        ):
            mock_stream.return_value = {"stream": events}
            sse_lines = asyncio.run(_collect_stream("test", FAKE_STUDENT_ID, session_id="my-session"))

        done_events = [
            json.loads(line[6:]) for line in sse_lines
            if line.startswith("data: ") and json.loads(line[6:]).get("type") == "done"
        ]
        assert len(done_events) == 1
        done = done_events[0]
        assert done["session_id"]
        assert "tokens_used" in done

    def test_guardrail_in_stream_sends_denial_message(self):
        events = self._make_stream_events(["partial text"], stop_reason="guardrail_intervened")

        with (
            patch("backend.rag.chat_handler.retrieve", return_value=[]),
            patch("backend.rag.chat_handler._call_converse_stream") as mock_stream,
        ):
            mock_stream.return_value = {"stream": events}
            sse_lines = asyncio.run(_collect_stream("off-topic question", FAKE_STUDENT_ID))

        # After guardrail, a denial chunk should follow (partial text is discarded)
        all_chunk_texts = [
            json.loads(line[6:]).get("text", "")
            for line in sse_lines
            if line.startswith("data: ") and json.loads(line[6:]).get("type") == "chunk"
        ]
        full_text = "".join(all_chunk_texts)
        # Partial "partial text" should not appear — denial message should
        from backend.guardrails.config import POLICY
        assert POLICY.denial_message in full_text


# ── API models validation ─────────────────────────────────────────────────────


class TestChatRequestModel:
    """Validation tests for the ChatRequest Pydantic model."""

    def test_valid_message_passes(self):
        req = ChatRequest(message="What is a ReAct agent?")
        assert req.message == "What is a ReAct agent?"

    def test_blank_message_raises(self):
        with pytest.raises(Exception):
            ChatRequest(message="   ")

    def test_empty_message_raises(self):
        with pytest.raises(Exception):
            ChatRequest(message="")

    def test_message_too_long_raises(self):
        with pytest.raises(Exception):
            ChatRequest(message="x" * 2001)

    def test_message_trimmed(self):
        req = ChatRequest(message="  trimmed  ")
        assert req.message == "trimmed"

    def test_session_id_sanitized(self):
        req = ChatRequest(message="test", session_id="abc-123<script>")
        assert req.session_id == "abc-123script"

    def test_none_session_id_allowed(self):
        req = ChatRequest(message="test", session_id=None)
        assert req.session_id is None


# ── prompt_templates ──────────────────────────────────────────────────────────


class TestBuildUserMessageWithContext:
    """Tests for the prompt context builder."""

    def test_includes_chunk_text(self):
        chunks = [{"text": "RAG stands for Retrieval-Augmented Generation.", "source": "m03.pdf"}]
        msg = build_user_message_with_context("What is RAG?", chunks)
        assert "RAG stands for Retrieval-Augmented Generation" in msg
        assert "What is RAG?" in msg

    def test_empty_chunks_shows_no_material_message(self):
        msg = build_user_message_with_context("obscure", [])
        assert "No relevant course materials" in msg

    def test_source_filename_in_header(self):
        chunks = [{"text": "content", "source": "module_04.pdf"}]
        msg = build_user_message_with_context("query", chunks)
        assert "module_04.pdf" in msg

    def test_multiple_chunks_numbered(self):
        chunks = [
            {"text": "first chunk", "source": "a.pdf"},
            {"text": "second chunk", "source": "b.pdf"},
        ]
        msg = build_user_message_with_context("query", chunks)
        assert "[1]" in msg
        assert "[2]" in msg


# ── Helpers ───────────────────────────────────────────────────────────────────


async def _run_handle_chat(
    query: str,
    student_id: str,
    session_id: str | None = None,
) -> dict:
    """Run handle_chat in an async context."""
    from backend.rag.chat_handler import handle_chat
    return await handle_chat(query=query, student_id=student_id, session_id=session_id)


async def _collect_stream(
    query: str,
    student_id: str,
    session_id: str | None = None,
) -> list[str]:
    """Collect all SSE lines from handle_chat_stream."""
    from backend.rag.chat_handler import handle_chat_stream
    lines: list[str] = []
    async for line in handle_chat_stream(
        query=query, student_id=student_id, session_id=session_id
    ):
        lines.append(line)
    return lines
