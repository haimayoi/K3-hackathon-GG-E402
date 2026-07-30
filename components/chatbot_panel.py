'''Conversation thread powered by the shared learning engine.'''

from __future__ import annotations

import streamlit as st

from components.quiz_panel import render_quiz_messages
from services.ai_client import AIConfig
from services.learning_engine import LearningTurn, run_learning_turn


def _to_ui_turn(
    result: LearningTurn,
    event_id: str,
    selected_text: str,
    page_number: int,
    question: str,
) -> dict[str, object]:
    response = result.response
    turn: dict[str, object] = {
        'id': event_id, 'selected_text': selected_text,
        'page_number': page_number, 'question': question,
        'status': response.status,
        'answer': response.answer, 'reason': response.reason,
        'citations': [citation.__dict__ for citation in response.citations],
        'provider': result.provider, 'model': result.model,
        'trace_path': result.trace_path, 'quiz_answer': None,
        'quiz_is_correct': False, 'retry_answer': None,
        'retry_is_correct': False,
    }
    if response.quiz is None:
        turn['quiz_visible'] = False
        return turn
    quiz = response.quiz
    turn.update({
        'quiz_question': quiz.question, 'quiz_options': quiz.options,
        'correct_quiz_option': quiz.options[quiz.correct_option_index],
        'correct_explanation': quiz.correct_explanation,
        'misconception_feedback_map': quiz.misconception_feedback,
        'quiz_visible': True, 'retry_question': quiz.retry_question,
        'retry_options': quiz.retry_options,
        'correct_retry_option': quiz.retry_options[
            quiz.correct_retry_option_index
        ],
        'retry_correct_explanation': quiz.retry_correct_explanation,
        'retry_wrong_explanation': quiz.retry_wrong_explanation,
    })
    return turn


def _consume_submission(
    submission: dict[str, object] | None,
    ai_config: AIConfig | None,
) -> None:
    if not submission:
        return
    event_id = str(submission.get('event_id', ''))
    selected_text = str(submission.get('selected_text', '')).strip()
    question = str(submission.get('question', '')).strip()
    try:
        page_number = int(submission.get('page_number', 0))
    except (TypeError, ValueError):
        page_number = 0
    if not event_id or not selected_text or not question:
        return
    if event_id == st.session_state.last_submission_id:
        return
    st.session_state.last_submission_id = event_id
    with st.spinner('Đang kiểm tra căn cứ và chuẩn bị phản hồi…'):
        result = run_learning_turn(
            selected_text, page_number, question, case_id=event_id,
            config=ai_config,
        )
    st.session_state.chat_turns.append(
        _to_ui_turn(result, event_id, selected_text, page_number, question)
    )


def _render_empty_thread() -> None:
    with st.chat_message('assistant', avatar='🧭'):
        st.markdown('**Hỏi trong phạm vi đoạn bạn bôi đen.**')
        st.write(
            'Mình chỉ trả lời và tạo quiz khi đoạn trên đúng trang có đủ căn cứ. '
            'Nếu thiếu hoặc mơ hồ, mình sẽ hỏi lại thay vì đoán.'
        )


def _retry_turn(turn: dict[str, object], ai_config: AIConfig | None) -> None:
    with st.spinner('Đang thử lại…'):
        result = run_learning_turn(
            str(turn['selected_text']), int(turn['page_number']),
            str(turn['question']), case_id=str(turn['id']), config=ai_config,
        )
    replacement = _to_ui_turn(
        result, str(turn['id']), str(turn['selected_text']),
        int(turn['page_number']), str(turn['question'])
    )
    turn.clear()
    turn.update(replacement)


def _render_turn(turn: dict[str, object], ai_config: AIConfig | None) -> None:
    with st.chat_message('user', avatar='🙂'):
        st.write(str(turn['question']))
        st.caption(
            'Trang {} · đoạn đã bôi đen'.format(turn.get('page_number'))
        )
    with st.chat_message('assistant', avatar='🧭'):
        status = str(turn.get('status', 'error'))
        st.write(str(turn['answer']))
        for citation in list(turn.get('citations', [])):
            st.markdown(
                '> **Trang {}:** {}'.format(
                    citation['page'], citation['quote']
                )
            )
        if status in {'insufficient_context', 'ambiguous', 'out_of_scope'}:
            st.caption('Lý do: {}'.format(turn.get('reason', '')))
        if status == 'error':
            retry_key = 'retry-turn-{}'.format(turn['id'])
            if st.button('Thử lại', key=retry_key):
                _retry_turn(turn, ai_config)
                st.rerun()
    if turn.get('quiz_visible', False):
        render_quiz_messages(turn)


def render_chatbot_panel(
    submission: dict[str, object] | None,
    ai_config: AIConfig | None = None,
) -> None:
    '''Render a chronological thread without a confidence threshold.'''
    _consume_submission(submission, ai_config)
    with st.container(height=736, border=True):
        st.markdown(
            '<div class=chat-heading><span>Chat Thread</span>'
            '<small>grounding theo trang và đoạn chọn</small></div>',
            unsafe_allow_html=True,
        )
        if not st.session_state.chat_turns:
            _render_empty_thread()
        else:
            for turn in st.session_state.chat_turns:
                _render_turn(turn, ai_config)
