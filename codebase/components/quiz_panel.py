"""Render validated quizzes and deterministically evaluate learner answers."""

from __future__ import annotations

import streamlit as st

from components.learning_agent import evaluate_answer


def _answer_form(turn: dict[str, object], *, retry: bool) -> None:
    run = turn["run"]
    quiz = run.artifact.retry_quiz if retry else run.artifact.quiz
    answer_key = "retry_answer_index" if retry else "quiz_answer_index"
    answer_index = turn.get(answer_key)
    form_key = f"{'retry' if retry else 'quiz'}-form-{turn['id']}"

    with st.chat_message("assistant", avatar="🧭"):
        st.markdown("**Thử lại — câu dễ hơn**" if retry else "**Kiểm tra nhanh · 1 câu**")
        st.write(quiz.question)
        st.caption(f"Nguồn: {run.source_id}")
        if answer_index is None:
            with st.form(form_key, border=False):
                selection = st.radio(
                    "Chọn một đáp án",
                    quiz.options,
                    index=None,
                    key=f"{form_key}-option",
                    label_visibility="collapsed",
                )
                submitted = st.form_submit_button(
                    "Gửi đáp án", type="primary", use_container_width=True
                )
                if submitted and selection is None:
                    st.warning("Hãy chọn một đáp án trước khi gửi.")
                elif submitted:
                    turn[answer_key] = quiz.options.index(selection)
                    st.rerun()
        else:
            for option in quiz.options:
                st.markdown(f"- {option}")

    if answer_index is None:
        if not retry and st.button("Bỏ qua / tiếp tục", key=f"skip-{turn['id']}"):
            turn["skipped"] = True
            st.rerun()
        return

    result = evaluate_answer(run, int(answer_index), retry=retry)
    with st.chat_message("user", avatar="🙂"):
        st.markdown(f"**Đáp án:** {quiz.options[int(answer_index)]}")
    with st.chat_message("assistant", avatar="🧭"):
        if result["correct"]:
            st.success("Chính xác. Bạn có thể tiếp tục học.")
            st.write(f"Đáp án đúng: {quiz.options[result['correct_index']]}")
        elif retry:
            st.error("Chưa đúng. Hãy đối chiếu lại đoạn nguồn trước khi tiếp tục.")
            st.write(result["feedback"])
            st.write(f"Đáp án đúng: {quiz.options[result['correct_index']]}")
        else:
            st.warning("Chưa đúng — đây là điểm dễ nhầm trong lựa chọn của bạn.")
            st.write(result["feedback"])
            st.caption("Hệ thống chấm bằng correct_index đã xác minh, không gọi model để chấm.")

    if not result["correct"] and not retry:
        _answer_form(turn, retry=True)


def render_quiz_messages(turn: dict[str, object]) -> None:
    if turn.get("skipped"):
        with st.chat_message("assistant", avatar="🧭"):
            st.info("Đã bỏ qua câu kiểm tra. Bạn có thể chọn đoạn khác để tiếp tục.")
        return
    _answer_form(turn, retry=False)