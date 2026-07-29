"""Quiz messages embedded in the learning chat thread."""

import streamlit as st

from components.mock_data import (
    CORRECT_EXPLANATION,
    CORRECT_QUIZ_OPTION,
    CORRECT_RETRY_OPTION,
    MISCONCEPTION_FEEDBACK,
    QUIZ_OPTIONS,
    QUIZ_QUESTION,
    RETRY_OPTIONS,
    RETRY_QUESTION,
)


def _render_option_list(options: list[str]) -> None:
    """Show answer choices as compact content inside an assistant message."""
    for option in options:
        st.markdown(f"- {option}")


def _render_retry_quiz(turn: dict[str, object]) -> None:
    """Append a simpler follow-up check after an incorrect answer."""
    turn_id = str(turn["id"])
    retry_answer = turn.get("retry_answer")

    with st.chat_message("assistant", avatar="🧭"):
        st.markdown("**Thử lại với một tình huống ngắn hơn**")
        st.write(RETRY_QUESTION)

        if retry_answer is None:
            with st.form(f"retry-form-{turn_id}", border=False):
                selection = st.radio(
                    "Chọn đáp án",
                    RETRY_OPTIONS,
                    index=None,
                    key=f"retry-option-{turn_id}",
                    label_visibility="collapsed",
                )
                submitted = st.form_submit_button(
                    "Gửi đáp án",
                    use_container_width=True,
                )
                if submitted and selection is None:
                    st.warning("Hãy chọn một đáp án trước khi gửi.")
                elif submitted:
                    turn["retry_answer"] = selection
                    turn["retry_is_correct"] = selection == CORRECT_RETRY_OPTION
                    st.rerun()
        else:
            _render_option_list(RETRY_OPTIONS)

    if retry_answer is None:
        return

    with st.chat_message("user", avatar="🙂"):
        st.markdown(f"**Đáp án thử lại:** {retry_answer}")

    with st.chat_message("assistant", avatar="🧭"):
        if turn.get("retry_is_correct", False):
            st.markdown("**✅ Đúng rồi!**")
            st.write(
                "Chênh lệch lớn giữa kết quả huấn luyện và kiểm thử là dấu hiệu "
                "điển hình của overfitting."
            )
        else:
            st.markdown("**❌ Chưa đúng. Đây là overfitting.**")
            st.write(
                "Mô hình đã học rất tốt tập huấn luyện (99%) nhưng không duy trì "
                "được kết quả trên dữ liệu chưa thấy (65%). Underfitting thường cho "
                "kết quả kém ngay cả trên tập huấn luyện."
            )


def render_quiz_messages(turn: dict[str, object]) -> None:
    """Render the quiz, learner answer, and feedback as consecutive messages."""
    turn_id = str(turn["id"])
    quiz_answer = turn.get("quiz_answer")

    with st.chat_message("assistant", avatar="🧭"):
        st.markdown("**Kiểm tra nhanh**")
        st.write(QUIZ_QUESTION)

        if quiz_answer is None:
            with st.form(f"quiz-form-{turn_id}", border=False):
                selection = st.radio(
                    "Chọn một đáp án",
                    QUIZ_OPTIONS,
                    index=None,
                    key=f"quiz-option-{turn_id}",
                    label_visibility="collapsed",
                )
                submitted = st.form_submit_button(
                    "Gửi đáp án",
                    type="primary",
                    use_container_width=True,
                )
                if submitted and selection is None:
                    st.warning("Hãy chọn một đáp án trước khi gửi.")
                elif submitted:
                    turn["quiz_answer"] = selection
                    turn["quiz_is_correct"] = selection == CORRECT_QUIZ_OPTION
                    st.rerun()
        else:
            _render_option_list(QUIZ_OPTIONS)

    if quiz_answer is None:
        return

    with st.chat_message("user", avatar="🙂"):
        st.markdown(f"**Đáp án của mình:** {quiz_answer}")

    with st.chat_message("assistant", avatar="🧭"):
        if turn.get("quiz_is_correct", False):
            st.markdown("**✅ Chính xác!**")
            st.write(CORRECT_EXPLANATION)
        else:
            st.markdown("**❌ Chưa đúng — cùng gỡ điểm dễ nhầm này nhé.**")
            st.write(
                MISCONCEPTION_FEEDBACK.get(
                    str(quiz_answer),
                    "Đáp án đúng là B: mô hình đã học cả nhiễu và các chi tiết "
                    "không mang tính tổng quát.",
                )
            )

    if not turn.get("quiz_is_correct", False):
        _render_retry_quiz(turn)
