from __future__ import annotations

import html
from dataclasses import dataclass

import streamlit as st


st.set_page_config(
    page_title="VLearn · Check-for-Understanding",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed",
)


@dataclass(frozen=True)
class Evaluation:
    status: str
    title: str
    feedback: str
    hint: str | None
    tone: str


LESSON = {
    "title": "Context trong mô hình ngôn ngữ",
    "page": 31,
    "source_id": "T03-031",
    "selected_text": (
        "Context có thể hình dung như một “bàn làm việc” có giới hạn: "
        "nó chứa những thông tin mô hình có thể nhìn thấy và sử dụng "
        "tại thời điểm xử lý."
    ),
    "tutor_answer": (
        "“Context” (ngữ cảnh) giống như một **bàn làm việc có giới hạn** "
        "của mô hình ngôn ngữ.\n\n"
        "Nó chứa các chỉ dẫn, tài liệu và lịch sử hội thoại mà mô hình có "
        "thể sử dụng trong lượt xử lý hiện tại. Nếu lượng thông tin vượt quá "
        "giới hạn, một phần nội dung có thể bị bỏ sót hoặc không còn nằm trong "
        "vùng mô hình nhìn thấy."
    ),
    "question": (
        "Vì sao context được ví như một “bàn làm việc có giới hạn”? "
        "Hãy trả lời bằng 1–2 câu."
    ),
}

QUICK_QUIZ = (
    {
        "question": "1. Vì sao context được ví như một ‘bàn làm việc có giới hạn’?",
        "options": (
            "Vì context lưu mọi kiến thức của mô hình vĩnh viễn",
            "Vì context chỉ chứa một lượng thông tin hữu hạn cho lượt xử lý hiện tại",
            "Vì context chỉ chứa được hình ảnh, không chứa văn bản",
        ),
        "correct": "Vì context chỉ chứa một lượng thông tin hữu hạn cho lượt xử lý hiện tại",
        "explanation": "Context là vùng thông tin hữu hạn mà mô hình có thể nhìn thấy và sử dụng trong lượt hiện tại.",
    },
    {
        "question": "2. Điều gì có thể xảy ra khi lượng thông tin vượt giới hạn context?",
        "options": (
            "Mô hình tự động tăng giới hạn mà không có chi phí",
            "Một phần thông tin có thể bị bỏ sót hoặc không còn được nhìn thấy",
            "Mô hình sẽ ghi nhớ toàn bộ thông tin sang mọi cuộc hội thoại",
        ),
        "correct": "Một phần thông tin có thể bị bỏ sót hoặc không còn được nhìn thấy",
        "explanation": "Thông tin vượt quá cửa sổ context có thể không còn nằm trong vùng mô hình xử lý.",
    },
    {
        "question": "3. Nhận định nào đúng về context và bộ nhớ dài hạn?",
        "options": (
            "Context chính là bộ nhớ vĩnh viễn của mô hình",
            "Có trong context nghĩa là mô hình sẽ nhớ mãi",
            "Context chỉ phục vụ lượt xử lý hiện tại, không mặc định là bộ nhớ vĩnh viễn",
        ),
        "correct": "Context chỉ phục vụ lượt xử lý hiện tại, không mặc định là bộ nhớ vĩnh viễn",
        "explanation": "Context và bộ nhớ dài hạn là hai cơ chế khác nhau; context không đảm bảo lưu giữ vĩnh viễn.",
    },
)


def initialize_state() -> None:
    defaults = {
        "stage": "idle",
        "selection_active": False,
        "ask_mode": False,
        "chat_ready": False,
        "user_question": "",
        "note_mode": False,
        "note_saved": False,
        "confusion_reported": False,
        "quiz_submitted": False,
        "quiz_score": 0,
        "quiz_error": "",
        "quiz_index": 0,
        "quiz_attempts": 0,
        "quiz_last_wrong": None,
        "quiz_history": [],
        "attempt": 1,
        "answer": "",
        "evaluation": None,
        "feedback_sent": False,
        "check_skipped": False,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def reset_demo() -> None:
    keys = (
        "stage", "selection_active", "ask_mode", "chat_ready", "user_question",
        "note_mode", "note_saved", "confusion_reported", "quiz_submitted",
        "quiz_score", "quiz_error", "quick_q1", "quick_q2", "quick_q3",
        "quiz_index", "quiz_attempts", "quiz_last_wrong", "quiz_history", "quiz_answer",
        "attempt", "answer", "evaluation", "feedback_sent", "check_skipped",
        "ask_error", "form_error",
    )
    for key in keys:
        st.session_state.pop(key, None)
    initialize_state()


def select_passage() -> None:
    st.session_state.selection_active = True


def open_ask() -> None:
    st.session_state.ask_mode = True
    st.session_state.note_mode = False


def report_confusion() -> None:
    st.session_state.confusion_reported = True


def open_note() -> None:
    st.session_state.note_mode = True
    st.session_state.ask_mode = False


def evaluate_mock(answer: str) -> Evaluation:
    """CP2 mock evaluator. Replace this function with an LLM call at CP3."""
    normalized = " ".join(answer.lower().strip().split())

    misconception_signals = (
        "bộ nhớ vĩnh viễn",
        "ghi nhớ mãi",
        "nhớ tất cả",
        "không giới hạn",
        "lưu vĩnh viễn",
    )
    has_information = any(
        token in normalized
        for token in ("thông tin", "dữ liệu", "prompt", "lịch sử", "nội dung")
    )
    has_limit = any(
        token in normalized
        for token in ("giới hạn", "hữu hạn", "dung lượng", "không chứa hết", "bị bỏ")
    )
    has_current_use = any(
        token in normalized
        for token in ("hiện tại", "lượt xử lý", "mô hình nhìn", "mô hình sử dụng")
    )

    if any(signal in normalized for signal in misconception_signals):
        return Evaluation(
            status="misconception",
            title="Có một điểm cần xem lại",
            feedback=(
                "Context không phải bộ nhớ vĩnh viễn và cũng không giúp mô hình "
                "ghi nhớ mọi thứ mãi mãi."
            ),
            hint=(
                "Hãy phân biệt thông tin có trong lượt xử lý hiện tại với "
                "thông tin mô hình luôn ghi nhớ."
            ),
            tone="danger",
        )

    if has_information and has_limit and has_current_use:
        return Evaluation(
            status="correct",
            title="Bạn đã nắm đúng ý chính",
            feedback=(
                "Đúng: context chứa lượng thông tin hữu hạn mà mô hình có thể "
                "nhìn thấy và sử dụng trong lượt xử lý hiện tại."
            ),
            hint=None,
            tone="success",
        )

    if has_information or has_limit:
        return Evaluation(
            status="partial",
            title="Bạn đã đúng một phần",
            feedback=(
                "Bạn đã nhắc đến thông tin hoặc giới hạn, nhưng chưa nối đủ hai ý: "
                "context vừa chứa thông tin mô hình đang dùng, vừa có dung lượng hữu hạn."
            ),
            hint="Điều gì xảy ra khi lượng thông tin vượt quá giới hạn context?",
            tone="warning",
        )

    return Evaluation(
        status="partial",
        title="Mình cần bạn nói rõ hơn một chút",
        feedback=(
            "Câu trả lời hiện chưa cho thấy mối liên hệ giữa context, lượng "
            "thông tin và giới hạn xử lý."
        ),
        hint="“Bàn làm việc” chứa gì, và chuyện gì xảy ra khi bàn đã đầy?",
        tone="warning",
    )


def retry_quiz() -> None:
    for key in ("quick_q1", "quick_q2", "quick_q3", "quiz_answer"):
        st.session_state.pop(key, None)
    st.session_state.quiz_submitted = False
    st.session_state.quiz_score = 0
    st.session_state.quiz_error = ""
    st.session_state.quiz_index = 0
    st.session_state.quiz_attempts = 0
    st.session_state.quiz_last_wrong = None
    st.session_state.feedback_sent = False



def card(markup: str, css_class: str = "") -> None:
    st.markdown(f'<div class="card {css_class}">{markup}</div>', unsafe_allow_html=True)


initialize_state()

st.markdown(
    """
    <style>
    :root {
        --bg: #050a19;
        --panel: #0a1226;
        --panel-2: #0e1930;
        --line: #22324d;
        --muted: #8796b3;
        --text: #f5f7ff;
        --blue: #20a4f3;
        --cyan: #28d7f7;
        --green: #20d3a0;
        --amber: #f3b94f;
        --red: #ff6d84;
    }

    .stApp {
        background:
            radial-gradient(circle at 70% 0%, rgba(24, 73, 130, .18), transparent 30%),
            var(--bg);
        color: var(--text);
    }

    header[data-testid="stHeader"] { background: transparent; }
    [data-testid="stToolbar"] { display: none; }
    .block-container { padding: 1rem 1.4rem 2rem; max-width: 1900px; }

    .topbar {
        display: flex; align-items: center; justify-content: space-between;
        background: rgba(7, 13, 29, .96); border: 1px solid #182640;
        border-radius: 16px; padding: 12px 18px; margin-bottom: 14px;
        box-shadow: 0 14px 40px rgba(0,0,0,.24);
    }
    .brand { font-weight: 850; font-size: 21px; letter-spacing: -.4px; }
    .brand span { color: #ff758c; }
    .doc-title { color: #dce5f7; font-size: 14px; }
    .mock-badge {
        color: #ffcb64; border: 1px solid #6b5424; background: #241c0c;
        border-radius: 999px; padding: 5px 10px; font-size: 11px; font-weight: 800;
    }

    .section-title {
        color: #f7f9ff; font-size: 14px; font-weight: 800; margin: 4px 0 10px;
    }
    .eyebrow {
        color: var(--cyan); font-size: 10px; font-weight: 900;
        letter-spacing: 1.5px; text-transform: uppercase;
    }
    .muted { color: var(--muted); font-size: 12px; }

    .card {
        background: linear-gradient(145deg, rgba(15, 25, 48, .98), rgba(8, 16, 34, .98));
        border: 1px solid var(--line); border-radius: 15px; padding: 14px;
        box-shadow: 0 10px 26px rgba(0,0,0,.16);
    }
    .day {
        border: 1px solid #263853; border-radius: 12px; padding: 12px;
        margin-bottom: 9px; color: #c7d2e8; font-size: 13px;
    }
    .day.active { border-color: #1687c9; background: #092846; color: white; }
    .day small { display: block; color: #6f819f; margin-top: 5px; }

    .slide-shell {
        background: #0c152b; border: 1px solid #233959; border-radius: 18px;
        padding: 16px; min-height: 480px;
    }
    .slide-toolbar {
        display: flex; gap: 8px; align-items: center; color: #8fa2c1;
        font-size: 11px; margin-bottom: 12px;
    }
    .tool-pill {
        padding: 6px 10px; border: 1px solid #30445f; border-radius: 999px;
        background: #13213a;
    }
    .slide {
        background: #fff; color: #142039; min-height: 390px;
        border-radius: 5px; padding: 30px 38px; box-shadow: 0 16px 38px rgba(0,0,0,.35);
    }
    .slide h2 { color: #145da0; font-size: 24px; margin: 6px 0 18px; }
    .slide p, .slide li { font-size: 16px; line-height: 1.55; }
    .slide .highlight {
        background: #fff4a9; border-left: 4px solid #f0ad22;
        padding: 12px 14px; border-radius: 6px; margin: 18px 0;
    }
    .slide .selection-target {
        border: 1px dashed #7f90a8; padding: 12px 14px; border-radius: 6px;
        margin: 18px 0; background: #f5f7fb;
    }
    .slide .selected {
        outline: 3px solid rgba(32, 164, 243, .26);
        box-shadow: 0 0 0 6px rgba(32, 164, 243, .08);
    }
    .selection-status {
        color: #73dbf6; font-size: 11px; font-weight: 800; margin: 7px 0;
    }
    .empty-chat {
        min-height: 220px; display: flex; align-items: center; justify-content: center;
        text-align: center; color: #8494b1; line-height: 1.6;
    }
    .slide-footer {
        display: flex; justify-content: space-between; color: #738098;
        border-top: 1px solid #dbe2ec; padding-top: 13px; margin-top: 26px;
        font-size: 11px;
    }

    .chat-user {
        background: linear-gradient(135deg, #0e62a9, #087bc7);
        padding: 11px 13px; border-radius: 15px 15px 4px 15px;
        margin: 10px 0 10px 18%; font-size: 13px;
    }
    .chat-tutor {
        background: #0d172d; border: 1px solid #213550;
        padding: 13px; border-radius: 15px 15px 15px 4px;
        font-size: 13px; line-height: 1.55;
    }
    .source {
        display: inline-block; margin-top: 9px; padding: 4px 8px;
        border-radius: 7px; background: #102941; color: #65cafa;
        border: 1px solid #1c5274; font-size: 10px; font-weight: 800;
    }
    .check-card {
        margin-top: 12px; border-color: #1d6986;
        background: linear-gradient(145deg, #09233a, #0b172d);
    }
    .question {
        color: #f4f7ff; font-size: 15px; font-weight: 750; line-height: 1.45;
        margin: 7px 0;
    }
    .attempt { color: #77d8f5; font-size: 11px; font-weight: 850; }
    .result-success { border-color: #1d8b70; background: #09271f; }
    .result-warning { border-color: #a07725; background: #2a210c; }
    .result-danger { border-color: #a34c61; background: #2c1119; }
    .result-title { font-size: 16px; font-weight: 900; margin-bottom: 6px; }
    .result-success .result-title { color: #4be0b4; }
    .result-warning .result-title { color: #ffd06a; }
    .result-danger .result-title { color: #ff8ca0; }
    .hint {
        margin-top: 10px; padding: 9px 10px; border-radius: 9px;
        background: rgba(255,255,255,.06); color: #dce5f6; font-size: 12px;
    }
    .guardrail {
        color: #9aa9c2; font-size: 10px; margin-top: 9px;
        border-top: 1px solid rgba(255,255,255,.08); padding-top: 8px;
    }

    div.stButton > button {
        width: 100%; border-radius: 10px; font-weight: 800;
        min-height: 38px; border: 1px solid #285170;
    }
    div.stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #138ed3, #0673bd);
        border: none;
    }
    div[data-testid="stTextArea"] textarea {
        background: #081326; border: 1px solid #2a4463; color: white;
        border-radius: 11px; min-height: 95px;
    }
    div[data-testid="stAlert"] { border-radius: 10px; }

    @media (max-width: 1100px) {
        .slide { padding: 22px; min-height: 330px; }
        .slide-shell { min-height: 410px; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


st.markdown(
    """
    <div class="topbar">
      <div>
        <div class="brand"><span>V</span>Learn</div>
        <div class="doc-title">day03-tu-chatbot-den-agentic-agent-react.pdf · Trang 31/46</div>
      </div>
      <div class="mock-badge">CP2 · MOCK DATA</div>
    </div>
    """,
    unsafe_allow_html=True,
)

left, center, right = st.columns([0.78, 2.25, 1.22], gap="medium")

with left:
    st.markdown('<div class="section-title">📘 Học liệu môn học</div>', unsafe_allow_html=True)
    for day in range(1, 7):
        active = " active" if day == 3 else ""
        count = 2 if day in (1, 3, 4) else 1
        st.markdown(
            f'<div class="day{active}"><b>◉ Day {day}</b>'
            f'<small>{count} TÀI LIỆU · {"STUDYING" if day == 3 else "ACTIVE"}</small></div>',
            unsafe_allow_html=True,
        )
    card(
        '<div class="eyebrow">Đang học</div>'
        '<b>Context & Prompt Engineering</b>'
        '<div class="muted" style="margin-top:6px">46 trang · Trang 31 đang mở</div>'
    )
    st.button("↻ Reset demo", use_container_width=True, on_click=reset_demo)

with center:
    selected_class = "highlight selected" if st.session_state.selection_active else "selection-target"
    selection_label = "ĐOẠN ĐÃ BÔI ĐEN · NGỮ CẢNH GỬI TUTOR" if st.session_state.selection_active else "ĐOẠN CÓ THỂ CHỌN"
    st.markdown(
        f"""
        <div class="slide-shell">
          <div class="slide-toolbar">
            <span class="tool-pill">➤ Đọc</span>
            <span class="tool-pill">✎ Bút</span>
            <span class="tool-pill">⌁ Highlight</span>
            <span style="margin-left:auto">Trang 31 · 100% · − ＋</span>
          </div>
          <div class="slide">
            <div style="color:#67758e;font-size:12px;font-weight:700">NỘI DUNG BÀI HỌC</div>
            <h2>Context — “Bàn làm việc” của mô hình</h2>
            <p>Mô hình chỉ có thể sử dụng những thông tin đang nằm trong context của lượt xử lý hiện tại.</p>
            <div class="{selected_class}">
              <div style="font-size:10px;color:#397399;font-weight:800;margin-bottom:6px">{selection_label}</div>
              <b>Context có thể hình dung như một “bàn làm việc” có giới hạn:</b>
              nó chứa các chỉ dẫn, tài liệu và lịch sử hội thoại mà mô hình có thể nhìn thấy và sử dụng.
            </div>
            <ul>
              <li>Context có dung lượng hữu hạn.</li>
              <li>Thông tin vượt giới hạn có thể bị bỏ sót.</li>
              <li>Nhiều context hơn không đồng nghĩa với hiểu tốt hơn.</li>
            </ul>
            <div class="slide-footer">
              <span>AI Thực Chiến · Day 3</span><span>31 / 46</span>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not st.session_state.selection_active:
        st.caption("Mô phỏng thao tác bôi đen một đoạn trên slide.")
        st.button(
            "🖱️ Bôi đen đoạn ‘Context có thể hình dung…’",
            type="primary",
            use_container_width=True,
            on_click=select_passage,
        )
    else:
        st.markdown(
            '<div class="selection-status">✓ Đã chọn nội dung trên Trang 31</div>',
            unsafe_allow_html=True,
        )
        action_ask, action_confused, action_note = st.columns(3)
        with action_ask:
            st.button("🤖 Hỏi AI", type="primary", use_container_width=True, on_click=open_ask)
        with action_confused:
            st.button("⚠️ Báo bối rối", use_container_width=True, on_click=report_confusion)
        with action_note:
            st.button("📄 Ghi chú", use_container_width=True, on_click=open_note)

        if st.session_state.confusion_reported:
            st.info("Đã ghi nhận đoạn này gây bối rối. Tín hiệu được gửi cho giảng viên/TA ở dạng tổng hợp.")

        if st.session_state.ask_mode:
            card(
                '<div class="eyebrow">Hỏi theo đoạn đã chọn</div>'
                '<div class="muted" style="margin-top:6px">Tutor sẽ nhận câu hỏi cùng đoạn bôi đen và mã Trang 31.</div>',
                "check-card",
            )
            with st.form("ask_tutor_form", clear_on_submit=False):
                tutor_question = st.text_input(
                    "Câu hỏi cho AI Tutor",
                    placeholder="Ví dụ: Giải thích đoạn này bằng một ví dụ đơn giản",
                    label_visibility="collapsed",
                )
                ask_submitted = st.form_submit_button(
                    "Gửi cho AI Tutor ➤", type="primary", use_container_width=True
                )
            if ask_submitted:
                if not tutor_question.strip():
                    st.session_state.ask_error = "Hãy nhập câu hỏi trước khi gửi."
                else:
                    st.session_state.ask_error = ""
                    st.session_state.user_question = tutor_question.strip()
                    st.session_state.chat_ready = True
                    st.session_state.ask_mode = False
                    st.session_state.stage = "idle"
                    st.session_state.quiz_submitted = False
                    st.session_state.quiz_score = 0
                    st.session_state.quiz_error = ""
                    st.session_state.quiz_index = 0
                    st.session_state.quiz_attempts = 0
                    st.session_state.quiz_last_wrong = None
                    st.session_state.quiz_history = []
                    for quiz_key in ("quick_q1", "quick_q2", "quick_q3", "quiz_answer"):
                        st.session_state.pop(quiz_key, None)
                    st.rerun()
            if st.session_state.get("ask_error"):
                st.error(st.session_state.ask_error)

        if st.session_state.note_mode:
            with st.form("note_form"):
                note_text = st.text_area(
                    "Ghi chú cá nhân",
                    placeholder="Viết ghi chú cho đoạn đang chọn…",
                    label_visibility="collapsed",
                )
                note_submitted = st.form_submit_button("Lưu ghi chú", use_container_width=True)
            if note_submitted and note_text.strip():
                st.session_state.note_saved = True
                st.session_state.note_mode = False
                st.rerun()
        if st.session_state.note_saved:
            st.success("Đã lưu ghi chú cho Trang 31.")

with right:
    st.markdown(
        '<div class="section-title">🤖 VLearn Tutor '
        '<span style="color:#2ed8a3;font-size:10px">● TRỢ LÝ HỌC THEO NGỮ CẢNH</span></div>',
        unsafe_allow_html=True,
    )

    if not st.session_state.chat_ready:
        card(
            '<div><div style="font-size:28px;margin-bottom:10px">✦</div>'
            '<b>Hội thoại sẽ xuất hiện tại đây</b><br>'
            '<span class="muted">Bôi đen một đoạn trên slide, chọn <b>Hỏi AI</b> và gửi câu hỏi.</span></div>',
            "empty-chat",
        )
    else:
        st.markdown(
            f'<div class="chat-user">{html.escape(st.session_state.user_question)}</div>',
            unsafe_allow_html=True,
        )
        tutor_html = html.escape(LESSON["tutor_answer"]).replace("\n\n", "<br><br>")
        tutor_html = tutor_html.replace("**", "")
        card(
            f'<div class="eyebrow">Tutor trả lời · dựa trên đoạn đã chọn</div>'
            f'<div style="margin-top:7px">{tutor_html}</div>'
            f'<span class="source">Nguồn: {LESSON["source_id"]} · Trang {LESSON["page"]}</span>',
            "chat-tutor",
        )

        card(
            '<div class="eyebrow">Kiểm tra nhanh · từng câu một</div>'
            '<div class="question">Tutor sẽ hỏi tiếp về điểm chưa hiểu cho đến khi bạn trả lời đúng.</div>'
            '<div class="muted">Không tính điểm học tập · chọn một đáp án</div>',
            "check-card",
        )

        if not st.session_state.quiz_submitted:
            quiz_item = QUICK_QUIZ[st.session_state.quiz_index]

            if st.session_state.quiz_last_wrong is not None:
                previous_item = QUICK_QUIZ[st.session_state.quiz_last_wrong]
                card(
                    '<div class="result-title">Chưa chính xác — mình cùng làm rõ điểm này</div>'
                    f'<div>{previous_item["explanation"]}</div>'
                    '<div class="hint">Hãy dùng giải thích này để trả lời câu hỏi liên quan tiếp theo.</div>',
                    "result-warning",
                )

            with st.form(f"quick_quiz_form_{st.session_state.quiz_attempts}"):
                st.markdown(f"**{quiz_item['question']}**")
                quiz_answer = st.radio(
                    quiz_item["question"], quiz_item["options"], index=None,
                    key="quiz_answer", label_visibility="collapsed",
                )
                quiz_submit = st.form_submit_button(
                    "Kiểm tra câu trả lời", type="primary", use_container_width=True
                )

            if quiz_submit:
                if quiz_answer is None:
                    st.session_state.quiz_error = "Hãy chọn một đáp án trước khi nộp."
                else:
                    is_correct = quiz_answer == quiz_item["correct"]
                    st.session_state.quiz_history.append({
                        "question": quiz_item["question"],
                        "answer": quiz_answer,
                        "correct": is_correct,
                    })

                if quiz_answer is not None and is_correct:
                    st.session_state.quiz_error = ""
                    st.session_state.quiz_score = 1
                    st.session_state.quiz_submitted = True
                    st.session_state.quiz_attempts += 1
                    st.rerun()
                elif quiz_answer is not None:
                    st.session_state.quiz_error = ""
                    st.session_state.quiz_last_wrong = st.session_state.quiz_index
                    st.session_state.quiz_index = (st.session_state.quiz_index + 1) % len(QUICK_QUIZ)
                    st.session_state.quiz_attempts += 1
                    st.session_state.pop("quiz_answer", None)
                    st.rerun()

            if st.session_state.quiz_error:
                st.error(st.session_state.quiz_error)
        else:
            card(
                '<div class="result-title">Chúc mừng! Bạn đã hiểu kiến thức</div>'
                '<div>Bạn đã trả lời đúng. Tutor sẽ dừng hỏi tại đây.</div>'
                f'<span class="source">Căn cứ: {LESSON["source_id"]} · Trang {LESSON["page"]}</span>'
                '<div class="guardrail">Kết quả chỉ hỗ trợ tự học, không dùng để chấm điểm hoặc xếp hạng.</div>',
                "result-success",
            )
            st.button("Tiếp tục học", type="primary", use_container_width=True, on_click=reset_demo)

        if st.session_state.quiz_history:
            st.markdown("#### Lịch sử trả lời")
            for attempt_number, entry in enumerate(st.session_state.quiz_history, start=1):
                status_icon = "✅" if entry["correct"] else "❌"
                status_text = "Đúng" if entry["correct"] else "Sai"
                tone = "result-success" if entry["correct"] else "result-danger"
                card(
                    f'<div class="result-title">{status_icon} Lần {attempt_number}: {status_text}</div>'
                    f'<div class="muted">{html.escape(entry["question"])}</div>'
                    f'<div style="margin-top:6px"><b>Đã chọn:</b> {html.escape(entry["answer"])}</div>',
                    tone,
                )
st.markdown(
    """
    <div class="muted" style="text-align:center;margin-top:16px">
      CP2 prototype · Toàn bộ nội dung, câu hỏi và kết quả đánh giá đang được mock.
      Tại CP3, AI call thật sẽ sinh 3 câu hỏi, đáp án và giải thích từ đoạn đã chọn.
    </div>
    """,
    unsafe_allow_html=True,
)
