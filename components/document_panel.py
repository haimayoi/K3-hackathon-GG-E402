"""Document viewer and selected-text input."""

import streamlit as st

from components.mock_data import DOCUMENT_TITLE


ANSWER_STATE_DEFAULTS = {
    "user_question": "",
    "answer_generated": False,
    "mock_answer": "",
    "confidence": 0.0,
    "quiz_visible": False,
    "quiz_submitted": False,
    "quiz_is_correct": False,
    "selected_option": None,
    "retry_quiz_visible": False,
}


def _clear_answer_state() -> None:
    """Remove results that no longer match a newly selected passage."""
    for key, value in ANSWER_STATE_DEFAULTS.items():
        st.session_state[key] = value

    st.session_state["question_input"] = ""
    for widget_key in ("quiz_option", "retry_option"):
        st.session_state.pop(widget_key, None)
    for retry_key in ("retry_quiz_submitted", "retry_quiz_is_correct"):
        st.session_state.pop(retry_key, None)


def render_document_panel(default_document: str, default_selection: str) -> str:
    """Render the source document and return the committed selected passage."""
    st.header("📄 Document Viewer")
    st.subheader(DOCUMENT_TITLE)

    with st.container(border=True):
        st.markdown(default_document)

    st.markdown("#### Selected text")
    st.caption(
        "Prototype chưa đọc được phần bôi đen trực tiếp. Hãy chỉnh đoạn văn bên dưới "
        "rồi xác nhận để sử dụng."
    )

    if "selected_text_input" not in st.session_state:
        st.session_state.selected_text_input = (
            st.session_state.get("selected_text") or default_selection
        )

    draft_selection = st.text_area(
        "Đoạn nội dung cần giải thích",
        key="selected_text_input",
        height=150,
        label_visibility="collapsed",
    )

    if st.button("Use selected text", type="primary", use_container_width=True):
        normalized_selection = draft_selection.strip()
        if not normalized_selection:
            st.warning("Vui lòng nhập một đoạn nội dung trước khi xác nhận.")
        else:
            selection_changed = normalized_selection != st.session_state.selected_text
            st.session_state.selected_text = normalized_selection
            if selection_changed:
                _clear_answer_state()
            st.success("Đã cập nhật đoạn nội dung dùng cho câu hỏi.")

    return st.session_state.selected_text

