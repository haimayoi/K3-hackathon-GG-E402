"""Entry point for the Streamlit Learning Assistant prototype."""

from dataclasses import replace
from pathlib import Path

import streamlit as st

from components.chatbot_panel import render_chatbot_panel
from components.document_panel import render_document_panel
from components.mock_data import DEFAULT_TEST_CASE_ID, TEST_CASES
from components.pdf_loader import DEFAULT_PDF_PATH, load_pdf_path
from services.ai_client import AIConfig


COURSE_PDF_PATHS = (
    Path(__file__).parent / 'data' / 'vlearn-pack' / 'slides' / 'd1-slide-hackathon.pdf',
    Path(__file__).parent / 'data' / 'vlearn-pack' / 'slides' / 'd2-slide-hackathon.pdf',
)


st.set_page_config(
    page_title="Learning Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed",
)


@st.cache_data(show_spinner=False)
def load_default_document() -> dict[str, object]:
    """Extract the bundled Day 1 PDF once for the complete app session."""
    return load_pdf_path(DEFAULT_PDF_PATH)


@st.cache_data(show_spinner=False)
def load_course_documents() -> list[dict[str, object]]:
    '''Load bundled course PDFs once, always ordered Day 1 then Day 2.'''
    documents: list[dict[str, object]] = []
    for day_number, path in enumerate(COURSE_PDF_PATHS, start=1):
        if not path.is_file():
            continue
        document = load_pdf_path(path)
        document['course_id'] = f'd{day_number}'
        document['day_label'] = f'Day {day_number}'
        documents.append(document)
    if not documents:
        document = load_pdf_path(DEFAULT_PDF_PATH)
        document['course_id'] = 'd1'
        document['day_label'] = 'Day 1'
        documents.append(document)
    return documents


def initialize_session_state() -> None:
    """Initialize the required state once per Streamlit session."""
    if "chat_turns" not in st.session_state:
        st.session_state.chat_turns = []
    if "last_submission_id" not in st.session_state:
        st.session_state.last_submission_id = None
    if "selector_generation" not in st.session_state:
        st.session_state.selector_generation = 0
    if "active_test_case" not in st.session_state:
        st.session_state.active_test_case = DEFAULT_TEST_CASE_ID
    if "viewer_test_case" not in st.session_state:
        st.session_state.viewer_test_case = st.session_state.active_test_case
    if "viewer_focus_page" not in st.session_state:
        st.session_state.viewer_focus_page = 1


    if 'active_document_id' not in st.session_state:
        st.session_state.active_document_id = 'd1'
    if 'viewer_document_id' not in st.session_state:
        st.session_state.viewer_document_id = st.session_state.active_document_id
    if 'runtime_api_key' not in st.session_state:
        st.session_state.runtime_api_key = ''
    if 'runtime_model' not in st.session_state:
        st.session_state.runtime_model = AIConfig.from_env().model


def reset_session() -> None:
    """Start a clean thread and remount the document selection component."""
    st.session_state.chat_turns = []
    st.session_state.last_submission_id = None
    st.session_state.selector_generation += 1


def render_test_case_control() -> str:
    """Keep the three deterministic mock routes without exposing file import UI."""
    label_col, picker_col = st.columns([2.2, 3], vertical_alignment="center")
    with label_col:
        st.markdown(
            "<div class='scenario-label'><strong>AI & LLM Foundation</strong>"
            "<span>Day 1 · 23 trang · chọn một kịch bản để kiểm thử</span></div>",
            unsafe_allow_html=True,
        )
    with picker_col:
        selected_test_case = st.selectbox(
            "Kịch bản mock",
            list(TEST_CASES),
            key="active_test_case",
            label_visibility="collapsed",
            format_func=lambda item: (
                f"{TEST_CASES[item]['title']} · {TEST_CASES[item]['slide_hint']}"
            ),
        )
    if selected_test_case != st.session_state.viewer_test_case:
        st.session_state.viewer_test_case = selected_test_case
        st.session_state.viewer_focus_page = int(
            TEST_CASES[selected_test_case]["focus_page"]
        )
    return selected_test_case


def render_scenario_control() -> str:
    '''Choose a deterministic prompt suggestion without mislabeling the PDF.'''
    st.caption('Câu hỏi gợi ý để kiểm thử luồng chọn đoạn → giải thích → quiz')
    selected_test_case = st.selectbox(
        'Kịch bản kiểm thử',
        list(TEST_CASES),
        key='active_test_case',
        label_visibility='collapsed',
        format_func=lambda item: '{} · {}'.format(
            TEST_CASES[item]['title'], TEST_CASES[item]['slide_hint']
        ),
    )
    if selected_test_case != st.session_state.viewer_test_case:
        st.session_state.viewer_test_case = selected_test_case
        st.session_state.viewer_focus_page = int(
            TEST_CASES[selected_test_case]['focus_page']
        )
    return selected_test_case


def render_document_control(
    documents: list[dict[str, object]],
) -> dict[str, object]:
    '''Render a stable D1 -> D2 selector and return the active document.'''
    by_id = {str(item['course_id']): item for item in documents}
    available_ids = list(by_id)
    if st.session_state.active_document_id not in by_id:
        st.session_state.active_document_id = available_ids[0]
    selected_id = st.selectbox(
        'Slide bài học',
        available_ids,
        key='active_document_id',
        format_func=lambda item_id: '{} · {} · {} trang'.format(
            by_id[item_id]['day_label'],
            by_id[item_id]['name'],
            by_id[item_id]['page_count'],
        ),
    )
    if selected_id != st.session_state.viewer_document_id:
        st.session_state.viewer_document_id = selected_id
        st.session_state.viewer_focus_page = 1
        st.session_state.selector_generation += 1
    return by_id[selected_id]


def render_ai_settings() -> AIConfig:
    '''Build an in-memory config; never persist or display the secret value.'''
    environment_config = AIConfig.from_env()
    has_environment_key = bool(environment_config.api_key)
    with st.expander('⚙ Cấu hình AI', expanded=not has_environment_key):
        key_col, model_col = st.columns([1.4, 1])
        with key_col:
            st.text_input(
                'Gemini API key (chỉ giữ trong session)',
                type='password',
                key='runtime_api_key',
                placeholder=(
                    'Đã nạp key từ .env' if has_environment_key
                    else 'Dán Gemini API key'
                ),
            )
        with model_col:
            st.text_input('Model Gemini', key='runtime_model')
        active_key = st.session_state.runtime_api_key.strip() or environment_config.api_key
        if environment_config.use_mock:
            st.info('Đang dùng Mock mode theo USE_MOCK_LLM=true.')
        elif active_key:
            st.success('API key đã sẵn sàng. Giá trị key không được ghi vào log.')
        else:
            st.warning('Chưa có API key. Có thể nhập tại đây hoặc cấu hình .env.')
    return replace(
        environment_config,
        api_key=active_key,
        model=st.session_state.runtime_model.strip() or environment_config.model,
    )


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

        .scenario-label {
            display: flex;
            flex-direction: column;
            gap: .12rem;
            padding: .25rem 0 .55rem;
            color: var(--app-ink);
        }

        .scenario-label strong { font-size: .88rem; }
        .scenario-label span { color: var(--app-muted); font-size: .76rem; }

        .scenario-label {
            display: flex;
            flex-direction: column;
            gap: .12rem;
            padding: .25rem 0 .55rem;
            color: var(--app-ink);
        }

        .scenario-label strong { font-size: .88rem; }
        .scenario-label span { color: var(--app-muted); font-size: .76rem; }

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
    apply_page_styles()

    title_col, action_col = st.columns([5, 1], vertical_alignment="center")
    with title_col:
        st.markdown(
            "<div class='app-brand'><span class='app-mark'>✦</span>"
            "<h1>Learning Assistant</h1></div>"
            "<p class='app-subtitle'>Đọc chủ động, hỏi ngay trong ngữ cảnh và kiểm tra mức độ hiểu bài.</p>",
            unsafe_allow_html=True,
        )
    with action_col:
        if st.button("↻ Bắt đầu lại", use_container_width=True):
            reset_session()
            st.rerun()

    documents = load_course_documents()
    active_document = render_document_control(documents)
    test_case_id = render_scenario_control()
    scenario = TEST_CASES[test_case_id]
    ai_config = render_ai_settings()

    left_col, right_col = st.columns([1.34, 0.66], gap="small")
    with left_col:
        submission = render_document_panel(
            str(active_document["text"]),
            component_key=(
                f"document-selector-{active_document['id']}-"
                f"{st.session_state.selector_generation}"
            ),
            document_title=str(active_document["name"]),
            question_placeholder=str(scenario["suggested_question"]),
            focus_page=int(st.session_state.viewer_focus_page),
            library_documents=[
                {
                    'course_id': item['course_id'],
                    'day_label': item['day_label'],
                    'name': item['name'],
                    'page_count': item['page_count'],
                }
                for item in documents
            ],
            active_document_id=str(active_document['course_id']),
            pages=list(active_document["pages"]),
        )
    with right_col:
        render_chatbot_panel(
            submission,
            test_case_id=test_case_id,
            ai_config=ai_config,
        )


if __name__ == "__main__":
    main()
