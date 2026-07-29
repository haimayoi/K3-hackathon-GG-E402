"""Mock chatbot response, confidence, and quiz routing."""

import time

import streamlit as st

from components.mock_data import MOCK_ANSWER, MOCK_CONFIDENCE, MOCK_EVIDENCE
from components.quiz_panel import render_quiz_panel


def _reset_quiz_state() -> None:
    """Reset quiz results whenever a new question is submitted."""
    st.session_state.quiz_submitted = False
    st.session_state.quiz_is_correct = False
    st.session_state.selected_option = None
    st.session_state.retry_quiz_visible = False
    st.session_state.retry_quiz_submitted = False
    st.session_state.retry_quiz_is_correct = False
    for widget_key in ("quiz_option", "retry_option"):
        st.session_state.pop(widget_key, None)


def _confidence_label(score: float) -> str:
    if score >= 0.80:
        return "High confidence"
    if score >= 0.60:
        return "Medium confidence"
    return "Low confidence"


def render_chatbot_panel(selected_text: str, confidence_threshold: float) -> None:
    """Render the chatbot interaction and conditionally display its quiz."""
    st.header("💬 Learning Chatbot")
    st.markdown("#### Nội dung đang được sử dụng")
    if selected_text.strip():
        st.info(selected_text)
    else:
        st.warning("Chưa có đoạn nội dung nào được chọn.")

    question = st.text_input(
        "Câu hỏi của bạn",
        key="question_input",
        placeholder="Ví dụ: Vì sao overfitting làm mô hình dự đoán kém?",
        disabled=not selected_text.strip(),
    )

    can_ask = bool(selected_text.strip() and question.strip())
    ask_clicked = st.button(
        "Ask chatbot",
        type="primary",
        use_container_width=True,
        disabled=not can_ask,
    )
    if not can_ask:
        st.caption("Nhập đủ đoạn nội dung và câu hỏi để gửi cho chatbot.")

    if ask_clicked:
        with st.spinner("Đang phân tích đoạn văn và câu hỏi..."):
            time.sleep(0.6)

        st.session_state.user_question = question.strip()
        st.session_state.answer_generated = True
        st.session_state.mock_answer = MOCK_ANSWER
        st.session_state.confidence = MOCK_CONFIDENCE
        _reset_quiz_state()

    if not st.session_state.answer_generated:
        return

    st.divider()
    st.subheader("Câu trả lời")
    st.write(st.session_state.mock_answer)

    confidence = float(st.session_state.confidence)
    metric_col, status_col = st.columns([1, 1.4])
    with metric_col:
        st.metric("Answer confidence", f"{confidence:.0%}")
    with status_col:
        st.markdown("**Mức độ tin cậy**")
        st.write(_confidence_label(confidence))
    st.progress(confidence)

    with st.expander("Evidence đối chiếu", expanded=True):
        st.write(MOCK_EVIDENCE)

    # Re-evaluate on every rerun so the sidebar threshold takes effect immediately.
    st.session_state.quiz_visible = confidence >= confidence_threshold
    if st.session_state.quiz_visible:
        render_quiz_panel()
    else:
        st.warning(
            f"Confidence {confidence:.0%} chưa đạt ngưỡng {confidence_threshold:.0%}; "
            "hệ thống chưa tạo quiz."
        )

