"""Chronological Streamlit view for the bounded learning-check state machine."""

from __future__ import annotations

import streamlit as st

from components.course_materials import CoursePage
from components.learning_agent import AgentState, run_learning_check
from components.quiz_panel import render_quiz_messages


def _consume_submission(submission: dict[str, object] | None, page: CoursePage | None) -> None:
    if not submission:
        return
    event_id = str(submission.get("event_id", ""))
    selected_text = str(submission.get("selected_text", "")).strip()
    question = str(submission.get("question", "")).strip()
    if not event_id or not selected_text or not question:
        return
    if event_id == st.session_state.last_submission_id:
        return

    st.session_state.last_submission_id = event_id
    with st.spinner("Đang kiểm tra nguồn và tạo một câu hỏi hiểu bài…"):
        run = run_learning_check(question=question, selected_text=selected_text, page=page)
    st.session_state.chat_turns.append(
        {
            "id": event_id,
            "selected_text": selected_text,
            "question": question,
            "run": run,
            "quiz_answer_index": None,
            "retry_answer_index": None,
            "skipped": False,
        }
    )


def _render_empty_thread() -> None:
    with st.chat_message("assistant", avatar="🧭"):
        st.markdown("**Chọn một đoạn có khái niệm, rồi hỏi tutor.**")
        st.write(
            "Mình chỉ dùng trang đang mở, xác minh nguồn trước khi tạo đúng một quiz "
            "bốn lựa chọn, và sẽ từ chối nếu ngữ cảnh không đủ."
        )


def _render_trace(run: object) -> None:
    with st.expander("Developer/demo trace", expanded=False):
        summary = run.trace_summary()
        st.json(
            {
                "current_state": summary["state"],
                "reason_code": summary["reason_code"],
                "source_id": summary["source_id"],
                "model": summary["model"],
                "latency_ms": summary["latency_ms"],
                "generation_attempts": summary["generation_attempts"],
                "schema_valid": summary["schema_valid"],
                "grounding_valid": summary["grounding_valid"],
                "prompt_version": summary["prompt_version"],
                "prompt_hash": summary["prompt_hash"],
                "artifact_version": summary["artifact_version"],
                "transitions": summary["transitions"],
            }
        )
        st.caption("Trace không chứa learner text, secret, raw error hay chain-of-thought.")


def _render_turn(turn: dict[str, object]) -> None:
    run = turn["run"]
    with st.chat_message("user", avatar="🙂"):
        st.write(str(turn["question"]))
        st.caption(f"Đoạn đã chọn: {str(turn['selected_text'])[:180]}")

    if run.state == AgentState.PRESENTED and run.artifact:
        with st.chat_message("assistant", avatar="🧭"):
            st.write(run.artifact.tutor_answer)
            st.markdown(f"> **Nguồn:** `{run.source_id}`")
        render_quiz_messages(turn)
    else:
        with st.chat_message("assistant", avatar="🧭"):
            if run.state == AgentState.ERROR_FALLBACK:
                st.warning(run.public_message)
            else:
                st.info(run.public_message)
            st.caption(f"Trạng thái: {run.state} · lý do: {run.reason_code}")
    _render_trace(run)


def render_chatbot_panel(submission: dict[str, object] | None, page: CoursePage | None) -> None:
    _consume_submission(submission, page)
    with st.container(height=656, border=True):
        st.markdown(
            "<div class='chat-heading'><span>Learning Check</span>"
            "<small>Grounded · bounded · deterministic scoring</small></div>",
            unsafe_allow_html=True,
        )
        if not st.session_state.chat_turns:
            _render_empty_thread()
        else:
            for turn in st.session_state.chat_turns:
                _render_turn(turn)