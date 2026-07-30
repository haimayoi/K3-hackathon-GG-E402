'''Quiz and targeted misconception feedback inside the chat thread.'''

import streamlit as st


def _retry(turn: dict[str, object]) -> None:
    turn_id = str(turn['id'])
    answer = turn.get('retry_answer')
    options = list(turn['retry_options'])
    with st.chat_message('assistant', avatar='🧭'):
        st.markdown('**Thử lại với một tình huống ngắn hơn**')
        st.write(str(turn['retry_question']))
        if answer is None:
            with st.form(f'retry-form-{turn_id}', border=False):
                selected = st.radio(
                    'Chọn đáp án', options, index=None,
                    key=f'retry-option-{turn_id}', label_visibility='collapsed'
                )
                submitted = st.form_submit_button(
                    'Gửi đáp án', use_container_width=True
                )
                if submitted and selected is None:
                    st.warning('Hãy chọn một đáp án trước khi gửi.')
                elif submitted:
                    turn['retry_answer'] = selected
                    turn['retry_is_correct'] = (
                        selected == turn['correct_retry_option']
                    )
                    st.rerun()
        else:
            for option in options:
                st.markdown(f'- {option}')
    if answer is None:
        return
    with st.chat_message('user', avatar='🙂'):
        st.markdown(f'**Đáp án thử lại:** {answer}')
    with st.chat_message('assistant', avatar='🧭'):
        if turn.get('retry_is_correct', False):
            st.markdown('**✅ Đúng rồi!**')
            st.write(str(turn['retry_correct_explanation']))
        else:
            st.markdown('**❌ Chưa đúng.**')
            st.write(str(turn['retry_wrong_explanation']))


def render_quiz_messages(turn: dict[str, object]) -> None:
    '''Render quiz, answer and targeted repair as chronological messages.'''
    turn_id = str(turn['id'])
    answer = turn.get('quiz_answer')
    options = list(turn['quiz_options'])
    with st.chat_message('assistant', avatar='🧭'):
        st.markdown('**Kiểm tra nhanh**')
        st.write(str(turn['quiz_question']))
        if answer is None:
            with st.form(f'quiz-form-{turn_id}', border=False):
                selected = st.radio(
                    'Chọn một đáp án', options, index=None,
                    key=f'quiz-option-{turn_id}', label_visibility='collapsed'
                )
                submitted = st.form_submit_button(
                    'Gửi đáp án', type='primary', use_container_width=True
                )
                if submitted and selected is None:
                    st.warning('Hãy chọn một đáp án trước khi gửi.')
                elif submitted:
                    turn['quiz_answer'] = selected
                    turn['quiz_is_correct'] = (
                        selected == turn['correct_quiz_option']
                    )
                    st.rerun()
        else:
            for option in options:
                st.markdown(f'- {option}')
    if answer is None:
        return
    with st.chat_message('user', avatar='🙂'):
        st.markdown(f'**Đáp án của mình:** {answer}')
    with st.chat_message('assistant', avatar='🧭'):
        if turn.get('quiz_is_correct', False):
            st.markdown('**✅ Chính xác!**')
            st.write(str(turn['correct_explanation']))
        else:
            st.markdown('**❌ Chưa đúng — cùng gỡ điểm dễ nhầm này nhé.**')
            selected_index = options.index(str(answer))
            feedback = dict(turn['misconception_feedback_map'])
            st.write(feedback.get(str(selected_index), 'Hãy xem lại giải thích.'))
    if not turn.get('quiz_is_correct', False):
        _retry(turn)
