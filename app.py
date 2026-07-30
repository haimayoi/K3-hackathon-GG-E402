"""Canonical Streamlit entry point for VLearn Learning Check Agent."""

import streamlit as st

from components.chatbot_panel import render_chatbot_panel
from components.course_materials import DOCUMENTS, get_page, load_document
from components.document_panel import render_document_panel


st.set_page_config(
    page_title="VLearn Learning Check Agent",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed",
)




def initialize_session_state() -> None:
    """Initialize the required state once per Streamlit session."""
    if "chat_turns" not in st.session_state:
        st.session_state.chat_turns = []
    if "last_submission_id" not in st.session_state:
        st.session_state.last_submission_id = None
    if "selector_generation" not in st.session_state:
        st.session_state.selector_generation = 0
    if "selected_document_id" not in st.session_state:
        st.session_state.selected_document_id = "d1"
    if "selected_page" not in st.session_state:
        st.session_state.selected_page = 29


def reset_session() -> None:
    """Start a clean thread and remount the document selection component."""
    st.session_state.chat_turns = []
    st.session_state.last_submission_id = None
    st.session_state.selector_generation += 1


def apply_page_styles() -> None:
    """Apply a compact, reading-focused visual system around native widgets."""
    st.markdown(
        """
        <style>
        :root {
            --app-ink: #172033;
            --app-muted: #687287;
            --app-accent: #635bff;
            --app-line: #e4e8ef;
        }

        [data-testid="stAppViewContainer"] {
            background:
                radial-gradient(circle at 12% 0%, rgba(99,91,255,.08), transparent 27rem),
                #f7f8fb;
            font-family: "Segoe UI", Tahoma, Arial, sans-serif;
        }

        button, input, textarea, select {
            font-family: "Segoe UI", Tahoma, Arial, sans-serif !important;
        }

        [data-testid="stMainBlockContainer"] {
            max-width: 1540px;
            padding: 1.8rem 2.6rem 2.2rem;
        }

        [data-testid="stHeader"], [data-testid="stToolbar"] { background: transparent; }
        [data-testid="stSidebar"] { display: none; }

        .app-brand {
            display: flex;
            align-items: center;
            gap: .72rem;
            margin-bottom: .2rem;
        }

        .app-mark {
            display: grid;
            width: 2.35rem;
            height: 2.35rem;
            place-items: center;
            border-radius: .75rem;
            background: var(--app-accent);
            box-shadow: 0 8px 20px rgba(99,91,255,.24);
            color: white;
            font-size: 1.15rem;
        }

        .app-brand h1 {
            margin: 0;
            color: var(--app-ink);
            font-size: 1.55rem;
            letter-spacing: -.025em;
        }

        .app-subtitle {
            margin: 0 0 1.15rem 3.08rem;
            color: var(--app-muted);
            font-size: .91rem;
        }

        .chat-heading {
            position: sticky;
            z-index: 5;
            top: 0;
            display: flex;
            align-items: flex-start;
            justify-content: space-between;
            gap: 1rem;
            margin: -.45rem -.2rem .9rem;
            padding: .45rem .2rem .85rem;
            border-bottom: 1px solid var(--app-line);
            background: white;
        }

        .chat-heading span {
            color: var(--app-ink);
            font-size: 1rem;
            font-weight: 750;
        }

        .chat-heading small {
            color: var(--app-muted);
            font-size: .73rem;
        }

        [data-testid="stVerticalBlockBorderWrapper"] {
            border-color: var(--app-line);
            border-radius: 18px;
            box-shadow: 0 12px 36px rgba(28,38,58,.07);
        }

        [data-testid="stChatMessage"] {
            padding: .78rem .82rem;
            border: 1px solid #e4e8ef;
            border-radius: 14px;
            background: #f7f8fc;
            color: var(--app-ink) !important;
        }

        [data-testid="stChatMessage"] p,
        [data-testid="stChatMessage"] li,
        [data-testid="stChatMessage"] label,
        [data-testid="stChatMessage"] blockquote,
        [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] {
            color: var(--app-ink) !important;
        }

        [data-testid="stChatMessage"] p { line-height: 1.55; }

        [data-testid="stChatMessage"] [data-testid="stCaptionContainer"],
        [data-testid="stChatMessage"] [data-testid="stCaptionContainer"] p {
            color: var(--app-muted) !important;
        }

        [data-testid="stChatMessage"] blockquote {
            border-left-color: #aaa5ff;
            background: #eeecff;
        }

        [data-testid="stRadio"] label,
        [data-testid="stRadio"] label p {
            color: var(--app-ink) !important;
        }

        [data-testid="stFormSubmitButton"] > button {
            border-color: var(--app-accent) !important;
            background: var(--app-accent) !important;
            color: #ffffff !important;
        }

        [data-testid="stFormSubmitButton"] > button:hover {
            border-color: #5148e5 !important;
            background: #5148e5 !important;
        }

        .stButton > button, [data-testid="stFormSubmitButton"] > button {
            border-radius: 10px;
            font-weight: 650;
        }

        @media (max-width: 900px) {
            [data-testid="stMainBlockContainer"] { padding: 1.2rem 1rem 2rem; }
            .app-subtitle { margin-left: 0; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def main() -> None:
    initialize_session_state()
    pending_page = st.session_state.pop("pending_slide_page", None)
    if pending_page is not None:
        st.session_state.selected_page = pending_page
    apply_page_styles()

    title_col, action_col = st.columns([5, 1], vertical_alignment="center")
    with title_col:
        st.markdown(
            "<div class='app-brand'><span class='app-mark'>✦</span>"
            "<h1>VLearn Learning Check Agent</h1></div>"
            "<p class='app-subtitle'>Một khái niệm · một quiz có căn cứ · phản hồi ngay tại điểm học.</p>",
            unsafe_allow_html=True,
        )
    with action_col:
        if st.button("↻ Bắt đầu lại", use_container_width=True):
            reset_session()
            st.rerun()

    chooser_col, page_col, source_col = st.columns([1.4, 1, 2.2], vertical_alignment="bottom")
    with chooser_col:
        document_id = st.selectbox(
            "Tài liệu khoá học",
            options=list(DOCUMENTS),
            format_func=lambda value: DOCUMENTS[value][0],
            key="selected_document_id",
        )
    pages = load_document(document_id)
    with page_col:
        page_number = st.selectbox(
            "Trang",
            options=list(range(1, len(pages) + 1)),
            key="selected_page",
        )
    page = get_page(document_id, page_number)
    with source_col:
        st.caption(
            f"Ngu\u1ed3n demo: `{page.source_id}` \u00b7 `{DOCUMENTS[document_id][1].name}` \u00b7 {page.source_label}"
            if page
            else "Không tìm thấy nguồn."
        )

    left_col, right_col = st.columns([1.08, 0.92], gap="medium")
    with left_col:
        submission = render_document_panel(
            page.source_label if page else "Tài liệu không khả dụng",
            page_number,
            len(pages),
            [item.text for item in pages],
            component_key=f"document-selector-{st.session_state.selector_generation}",
        )
        if submission:
            event_id = str(submission.get("event_id", ""))
            target_page = int(submission.get("page", page_number))
            is_new_question = event_id and event_id != st.session_state.last_submission_id
            if is_new_question and 1 <= target_page <= len(pages) and target_page != page_number:
                st.session_state.pending_slide_page = target_page
                st.rerun()
    with right_col:
        render_chatbot_panel(submission, page)


if __name__ == "__main__":
    main()
