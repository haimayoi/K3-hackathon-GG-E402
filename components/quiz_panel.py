"""Quiz messages embedded in the learning chat thread.

The comprehension quiz (question, options, misconceptions) comes from a real
Gemini call made in chatbot_panel.py via components/ai_client.py — this module
only renders whatever result landed on the turn (ok / insufficient / error).
The retry follow-up question is the one piece that stays static mock data.
"""

import streamlit as st

from components.mock_data import CORRECT_RETRY_OPTION, RETRY_OPTIONS, RETRY_QUESTION


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
    """Render the AI-generated quiz (or its refusal/error state), then feedback."""
    turn_id = str(turn["id"])
    quiz_status = turn.get("quiz_status")

    if quiz_status == "error":
        with st.chat_message("assistant", avatar="🧭"):
            st.warning(
                "Mình chưa tạo được câu kiểm tra hiểu lúc này — lỗi khi gọi mô hình "
                f"({turn.get('quiz_reason', 'không rõ nguyên nhân')}). Bạn cứ tiếp tục đọc, "
                "mình sẽ thử lại ở lượt hỏi tiếp theo."
            )
        return

    if quiz_status == "insufficient":
        with st.chat_message("assistant", avatar="🧭"):
            st.info(
                "Đoạn này chưa đủ nội dung cụ thể để mình ra một câu kiểm tra hiểu có ý nghĩa "
                f"({turn.get('quiz_reason', 'thiếu ngữ cảnh')}). Bạn thử bôi đen một đoạn nói rõ "
                "hơn về khái niệm nhé."
            )
        return

    quiz_data = turn.get("quiz_data") or {}
    options = quiz_data.get("options") or []
    correct_index = quiz_data.get("correct_index")
    misconceptions = {
        item["option_index"]: item["explanation"]
        for item in quiz_data.get("misconceptions") or []
    }
    quiz_answer_index = turn.get("quiz_answer_index")

    if not options or correct_index is None:
        with st.chat_message("assistant", avatar="🧭"):
            st.warning("Câu kiểm tra hiểu trả về không hợp lệ, bỏ qua bước này.")
        return

    with st.chat_message("assistant", avatar="🧭"):
        st.markdown("**Kiểm tra nhanh**")
        st.write(quiz_data.get("question", ""))

        if quiz_answer_index is None:
            with st.form(f"quiz-form-{turn_id}", border=False):
                selection = st.radio(
                    "Chọn một đáp án",
                    options,
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
                    turn["quiz_answer_index"] = options.index(selection)
                    turn["quiz_is_correct"] = turn["quiz_answer_index"] == correct_index
                    st.rerun()
        else:
            _render_option_list(options)

    if quiz_answer_index is None:
        return

    with st.chat_message("user", avatar="🙂"):
        st.markdown(f"**Đáp án của mình:** {options[quiz_answer_index]}")

    with st.chat_message("assistant", avatar="🧭"):
        if turn.get("quiz_is_correct", False):
            st.markdown("**✅ Chính xác!**")
            st.write(f"Đúng — {options[correct_index]}")
        else:
            st.markdown("**❌ Chưa đúng — cùng gỡ điểm dễ nhầm này nhé.**")
            st.write(
                misconceptions.get(
                    quiz_answer_index,
                    f"Đáp án đúng là: {options[correct_index]}.",
                )
            )

    if not turn.get("quiz_is_correct", False):
        _render_retry_quiz(turn)
