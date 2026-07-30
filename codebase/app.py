"""Canonical Streamlit entry point for the bounded Learning Assistant."""

from __future__ import annotations

import streamlit as st

from components.chatbot_panel import render_chatbot_panel
from components.course_materials import DOCUMENTS, normalize_submission
from components.document_panel import render_document_panel
from components.pdf_loader import document_id_for_bytes, extract_pdf_document, load_pdf_path


st.set_page_config(
    page_title="Learning Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def initialize_session_state() -> None:
    """Initialize stable keys once per Streamlit session."""
    defaults: dict[str, object] = {
        "chat_turns": [],
        "last_submission_id": None,
        "selector_generation": 0,
        "active_document_id": "d1",
        "uploaded_documents": {},
        "selected_page": 1,
        "pending_slide_page": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def reset_session() -> None:
    """Reset the learning thread while retaining session-uploaded documents."""
    st.session_state.chat_turns = []
    st.session_state.last_submission_id = None
    st.session_state.selector_generation += 1
    st.session_state.pending_slide_page = None


@st.cache_data(show_spinner=False)
def load_course_documents() -> dict[str, dict[str, object]]:
    """Load Day 1 and Day 2 through the normalized rendered-PDF contract."""
    documents: dict[str, dict[str, object]] = {}
    for document_id, (title, path) in DOCUMENTS.items():
        if not path.is_file():
            continue
        document = load_pdf_path(path)
        document.update(
            {
                "id": document_id,
                "name": title,
                "source": "bundled",
                "day_label": f"Day {document_id[1:]}",
            }
        )
        documents[document_id] = document
    return documents


def document_registry() -> dict[str, dict[str, object]]:
    """Combine bundled course decks with uploads owned by this session."""
    return {**load_course_documents(), **dict(st.session_state.uploaded_documents)}


def ingest_upload(uploaded_file: object) -> bool:
    """Extract one new in-memory upload and add it to the session library."""
    if not uploaded_file:
        return False
    data = uploaded_file.getvalue()
    document_id = document_id_for_bytes(data)
    already_in_library = document_id in st.session_state.uploaded_documents

    if not already_in_library:
        document = extract_pdf_document(data, uploaded_file.name, "upload")
        document["day_label"] = "PDF tải lên"
        st.session_state.uploaded_documents[document_id] = document

    if st.session_state.active_document_id != document_id:
        st.session_state.active_document_id = document_id
        st.session_state.selected_page = 1
        st.session_state.pending_slide_page = None
        st.session_state.selector_generation += 1
        return True

    return not already_in_library


def handle_document_switch(
    submission: dict[str, object] | None,
    documents: dict[str, dict[str, object]],
) -> dict[str, object] | None:
    """Switch the active document and discard selection state from the old one."""
    if not submission or submission.get("action") != "switch_document":
        return submission
    requested_id = str(submission.get("document_id", ""))
    if requested_id in documents and requested_id != st.session_state.active_document_id:
        st.session_state.active_document_id = requested_id
        st.session_state.selected_page = 1
        st.session_state.pending_slide_page = None
        st.session_state.selector_generation += 1
        st.rerun()
    return None


def apply_page_styles() -> None:
    """Apply the reading-focused visual system ported from the reference UI."""
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
        [data-testid="stMainBlockContainer"] {
            max-width: 1540px;
            padding: 1.6rem 2.2rem 2rem;
        }
        [data-testid="stHeader"], [data-testid="stToolbar"] { background: transparent; }
        [data-testid="stSidebar"] { display: none; }
        button, input, textarea, select {
            font-family: "Segoe UI", Tahoma, Arial, sans-serif !important;
        }
        .app-brand { display: flex; align-items: center; gap: .72rem; margin-bottom: .2rem; }
        .app-mark {
            display: grid; width: 2.35rem; height: 2.35rem; place-items: center;
            border-radius: .75rem; background: var(--app-accent); color: white;
            box-shadow: 0 8px 20px rgba(99,91,255,.24); font-size: 1.15rem;
        }
        .app-brand h1 {
            margin: 0; color: var(--app-ink); font-size: 1.55rem; letter-spacing: -.025em;
        }
        .app-subtitle { margin: 0 0 1.05rem 3.08rem; color: var(--app-muted); font-size: .91rem; }
        .chat-heading {
            position: sticky; z-index: 5; top: 0; display: flex;
            align-items: flex-start; justify-content: space-between; gap: 1rem;
            margin: -.45rem -.2rem .9rem; padding: .45rem .2rem .85rem;
            border-bottom: 1px solid var(--app-line); background: white;
        }
        .chat-heading span { color: var(--app-ink); font-size: 1rem; font-weight: 750; }
        .chat-heading small { color: var(--app-muted); font-size: .73rem; }
        [data-testid="stVerticalBlockBorderWrapper"] {
            border-color: var(--app-line); border-radius: 18px;
            box-shadow: 0 12px 36px rgba(28,38,58,.07);
        }
        [data-testid="stChatMessage"] {
            padding: .78rem .82rem; border: 1px solid #e4e8ef;
            border-radius: 14px; background: #f7f8fc; color: var(--app-ink) !important;
        }
        [data-testid="stChatMessage"] p,
        [data-testid="stChatMessage"] li,
        [data-testid="stChatMessage"] label,
        [data-testid="stChatMessage"] blockquote,
        [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] {
            color: var(--app-ink) !important;
        }
        [data-testid="stChatMessage"] [data-testid="stCaptionContainer"],
        [data-testid="stChatMessage"] [data-testid="stCaptionContainer"] p {
            color: var(--app-muted) !important;
        }
        [data-testid="stFormSubmitButton"] > button {
            border-color: var(--app-accent) !important;
            background: var(--app-accent) !important;
            color: #fff !important;
        }
        .stButton > button, [data-testid="stFormSubmitButton"] > button {
            border-radius: 10px; font-weight: 650;
        }
        @media (max-width: 900px) {
            [data-testid="stMainBlockContainer"] { padding: 1rem .8rem 1.5rem; }
            .app-subtitle { margin-left: 0; }
            .chat-heading small { display: none; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def main() -> None:
    initialize_session_state()
    if st.session_state.pending_slide_page is not None:
        st.session_state.selected_page = st.session_state.pending_slide_page
        st.session_state.pending_slide_page = None
    apply_page_styles()

    title_col, action_col = st.columns(
        [6.2, 1.2], vertical_alignment="center"
    )
    with title_col:
        st.markdown(
            "<div class='app-brand'><span class='app-mark'>✦</span>"
            "<h1>Learning Assistant</h1></div>"
            "<p class='app-subtitle'>Đọc chủ động, hỏi theo ngữ cảnh và kiểm tra mức độ hiểu bài.</p>",
            unsafe_allow_html=True,
        )
    with action_col:
        if st.button("↻ Bắt đầu lại", use_container_width=True):
            reset_session()
            st.rerun()

    documents = document_registry()
    if not documents:
        st.error(
            "Không tìm thấy tài liệu Day 1/Day 2. "
            "Hãy bổ sung data pack hoặc tải một PDF lên."
        )
        return
    if st.session_state.active_document_id not in documents:
        st.session_state.active_document_id = next(iter(documents))
    active_document = documents[st.session_state.active_document_id]
    page_count = int(active_document["page_count"])
    st.session_state.selected_page = max(
        1, min(int(st.session_state.selected_page), page_count)
    )

    left_col, right_col = st.columns([1.34, 0.66], gap="small")
    with left_col:
        if int(active_document.get("text_page_count", 0)) == 0:
            st.warning(
                "Không tìm thấy text có thể chọn trong PDF. File có thể chỉ chứa ảnh "
                "và hiện chưa hỗ trợ OCR."
            )
        submission = render_document_panel(
            str(active_document["name"]),
            component_key=(
                f"document-selector-{active_document['id']}-"
                f"{st.session_state.selector_generation}"
            ),
            pages=list(active_document["pages"]),
            page_count=page_count,
            focus_page=int(st.session_state.selected_page),
            active_document_id=str(active_document["id"]),
            library_documents=[
                {
                    "document_id": item["id"],
                    "course_id": item["id"],
                    "day_label": item.get("day_label", "PDF tải lên"),
                    "name": item["name"],
                    "page_count": item["page_count"],
                }
                for item in documents.values()
            ],
        )
        submission = handle_document_switch(submission, documents)
        normalized_submission, page = normalize_submission(
            submission,
            documents,
            active_document_id=str(active_document["id"]),
            fallback_page=int(st.session_state.selected_page),
        )
        if page is not None:
            st.session_state.selected_page = page.page
    with right_col:
        render_chatbot_panel(normalized_submission, page, active_document)


if __name__ == "__main__":
    main()
