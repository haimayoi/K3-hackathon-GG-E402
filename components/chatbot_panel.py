"""Conversation thread for mock answers, quizzes, and learning feedback."""

import streamlit as st

from components.mock_data import MOCK_ANSWER, MOCK_CONFIDENCE, MOCK_EVIDENCE
from components.quiz_panel import render_quiz_messages


def _consume_submission(
    submission: dict[str, object] | None,
    confidence_threshold: float,
) -> None:
    """Convert a new document-popover event into a mock conversation turn."""
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
    st.session_state.chat_turns.append(
        {
            "id": event_id,
            "selected_text": selected_text,
            "question": question,
            "answer": MOCK_ANSWER,
            "evidence": MOCK_EVIDENCE,
            "confidence": MOCK_CONFIDENCE,
            "quiz_visible": MOCK_CONFIDENCE >= confidence_threshold,
            "quiz_answer": None,
            "quiz_is_correct": False,
            "retry_answer": None,
            "retry_is_correct": False,
        }
    )


def _render_empty_thread() -> None:
    with st.chat_message("assistant", avatar="🧭"):
        st.markdown("**Chào bạn! Mình sẵn sàng cùng bạn đọc tài liệu.**")
        st.write(
            "Bôi đen một đoạn ở khung bên trái, nhập câu hỏi vào popup rồi gửi. "
            "Câu trả lời và bài kiểm tra ngắn sẽ xuất hiện tại đây."
        )


def _render_turn(turn: dict[str, object]) -> None:
    with st.chat_message("user", avatar="🙂"):
        st.write(str(turn["question"]))
        st.caption("Đã gửi từ đoạn nội dung bạn bôi đen trong tài liệu")

    with st.chat_message("assistant", avatar="🧭"):
        st.write(str(turn["answer"]))
        st.markdown(f"> **Đối chiếu trong tài liệu:** {turn['evidence']}")

    if turn.get("quiz_visible", False):
        render_quiz_messages(turn)


def render_chatbot_panel(
    submission: dict[str, object] | None,
    confidence_threshold: float,
) -> None:
    """Render the full learning flow as one chronological chat thread."""
    _consume_submission(submission, confidence_threshold)

    with st.container(height=656, border=True):
        st.markdown(
            "<div class='chat-heading'><span>Chat Thread</span>"
            "<small>Trợ giảng mô phỏng · phản hồi tức thì</small></div>",
            unsafe_allow_html=True,
        )

        if not st.session_state.chat_turns:
            _render_empty_thread()
        else:
            for turn in st.session_state.chat_turns:
                _render_turn(turn)
