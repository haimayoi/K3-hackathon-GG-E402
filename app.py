"""Entry point for the Streamlit Learning Assistant prototype."""

import streamlit as st

from components.chatbot_panel import render_chatbot_panel
from components.document_panel import render_document_panel
from components.mock_data import DEFAULT_DOCUMENT, DEFAULT_SELECTION, DOCUMENT_TITLE


st.set_page_config(
    page_title="Learning Assistant",
    page_icon="🎓",
    layout="wide",
)


SESSION_DEFAULTS = {
    "selected_text": DEFAULT_SELECTION,
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


def initialize_session_state() -> None:
    """Initialize the required state once per Streamlit session."""
    for key, value in SESSION_DEFAULTS.items():
        if key not in st.session_state:
            st.session_state[key] = value


def render_sidebar() -> float:
    """Render controls shared by the complete learning flow."""
    with st.sidebar:
        st.title("🎓 Learning Assistant")
        st.markdown("**Tài liệu mẫu**")
        st.caption(DOCUMENT_TITLE)

        confidence_threshold = st.slider(
            "Quiz confidence threshold",
            min_value=0.0,
            max_value=1.0,
            value=0.80,
            step=0.05,
            help="Quiz chỉ xuất hiện khi confidence bằng hoặc cao hơn ngưỡng này.",
        )

        if st.button("Reset session", use_container_width=True):
            st.session_state.clear()
            st.rerun()

        st.divider()
        st.info(
            "Prototype mô phỏng luồng đọc tài liệu, hỏi đáp và kiểm tra nhanh. "
            "Câu trả lời, confidence và quiz đều là dữ liệu tĩnh; không có API bên ngoài."
        )

    return confidence_threshold


def main() -> None:
    initialize_session_state()
    confidence_threshold = render_sidebar()

    st.title("Learning Assistant")
    st.caption("Đọc một đoạn kiến thức, đặt câu hỏi và kiểm tra lại mức độ hiểu bài.")

    left_col, right_col = st.columns([1.1, 1], gap="large")
    with left_col:
        selected_text = render_document_panel(DEFAULT_DOCUMENT, DEFAULT_SELECTION)
    with right_col:
        render_chatbot_panel(selected_text, confidence_threshold)


if __name__ == "__main__":
    main()

