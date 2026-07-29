"""Knowledge-check quiz and misconception feedback."""

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


def _render_retry_quiz() -> None:
    """Render a simpler follow-up check after an incorrect answer."""
    st.markdown("#### Kiểm tra lại")
    st.write(RETRY_QUESTION)
    retry_selection = st.radio(
        "Chọn đáp án kiểm tra lại",
        RETRY_OPTIONS,
        index=None,
        key="retry_option",
        label_visibility="collapsed",
    )

    if st.button("Submit retry answer", use_container_width=True):
        if retry_selection is None:
            st.warning("Vui lòng chọn một đáp án cho câu kiểm tra lại.")
        else:
            st.session_state.retry_quiz_submitted = True
            st.session_state.retry_quiz_is_correct = (
                retry_selection == CORRECT_RETRY_OPTION
            )

    if st.session_state.get("retry_quiz_submitted", False):
        if st.session_state.get("retry_quiz_is_correct", False):
            st.success("Đúng rồi — chênh lệch lớn giữa kết quả huấn luyện và kiểm thử là dấu hiệu điển hình của overfitting.")
        else:
            st.error("Chưa đúng. Đây là overfitting, không phải underfitting.")
            st.info(
                "Mô hình đã học rất tốt tập huấn luyện (99%) nhưng không duy trì được "
                "kết quả trên dữ liệu chưa thấy (65%). Underfitting thường cho kết quả "
                "kém ngay cả trên tập huấn luyện."
            )


def render_quiz_panel() -> None:
    """Render the main quiz, grade it, and show targeted feedback."""
    st.divider()
    st.subheader("🧠 Quick knowledge check")
    st.write(QUIZ_QUESTION)

    selected_option = st.radio(
        "Chọn một đáp án",
        QUIZ_OPTIONS,
        index=None,
        key="quiz_option",
        label_visibility="collapsed",
    )

    if st.button("Submit answer", type="primary", use_container_width=True):
        if selected_option is None:
            st.warning("Vui lòng chọn một đáp án trước khi gửi.")
        else:
            st.session_state.selected_option = selected_option
            st.session_state.quiz_submitted = True
            st.session_state.quiz_is_correct = selected_option == CORRECT_QUIZ_OPTION
            st.session_state.retry_quiz_visible = not st.session_state.quiz_is_correct

            # A fresh main-quiz submission starts a fresh retry attempt.
            st.session_state.pop("retry_option", None)
            st.session_state.retry_quiz_submitted = False
            st.session_state.retry_quiz_is_correct = False

    if st.session_state.quiz_submitted:
        if st.session_state.quiz_is_correct:
            st.success("Chính xác!")
            st.info(CORRECT_EXPLANATION)
        else:
            st.error("Chưa đúng — hãy xem lại điểm kiến thức này.")
            feedback = MISCONCEPTION_FEEDBACK.get(
                st.session_state.selected_option,
                "Đáp án đúng là B: mô hình đã học cả nhiễu và các chi tiết không mang tính tổng quát.",
            )
            st.warning(feedback)

    if st.session_state.retry_quiz_visible:
        _render_retry_quiz()

