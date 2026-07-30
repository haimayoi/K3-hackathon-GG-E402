"""Render validated quizzes and deterministically evaluate learner answers."""

from __future__ import annotations

import streamlit as st

from components.learning_agent import evaluate_answer, generate_followup_quiz


def render_quiz_messages(turn: dict[str, object]) -> None:
    if turn.get("skipped"):
        with st.chat_message("assistant", avatar="🧭"):
            st.info("Đã bỏ qua câu kiểm tra. Bạn có thể chọn đoạn khác để tiếp tục.")
        return

    run = turn["run"]
    if not run or not run.artifact:
        return

    # Migration for legacy turns created prior to 3-attempt state machine
    if "attempts" not in turn:
        attempts = []
        if turn.get("quiz_answer_index") is not None:
            q1 = run.artifact.quiz
            idx1 = int(turn["quiz_answer_index"])
            res1 = evaluate_answer(run, idx1, retry=False)
            attempts.append({
                "attempt_num": 1,
                "quiz": q1,
                "selected_index": idx1,
                "correct": res1["correct"],
                "feedback": res1["feedback"],
            })
            if res1["correct"]:
                turn["completed"] = True

        if not turn.get("completed") and turn.get("retry_answer_index") is not None:
            q2 = run.artifact.retry_quiz
            idx2 = int(turn["retry_answer_index"])
            res2 = evaluate_answer(run, idx2, retry=True)
            attempts.append({
                "attempt_num": 2,
                "quiz": q2,
                "selected_index": idx2,
                "correct": res2["correct"],
                "feedback": res2["feedback"],
            })
            if res2["correct"]:
                turn["completed"] = True
        turn["attempts"] = attempts

    attempts = turn["attempts"]
    completed = turn.get("completed", False)
    user_won = any(att.get("correct", False) for att in attempts)

    # 1. Render all past completed attempts chronologically
    for idx, att in enumerate(attempts, start=1):
        q = att["quiz"]
        sel = att["selected_index"]
        correct = att["correct"]
        feedback = att["feedback"]

        with st.chat_message("assistant", avatar="🧭"):
            st.markdown(f"**Lần {idx} — {q.question}**")
            for o_idx, opt in enumerate(q.options):
                if o_idx == sel and not correct:
                    st.markdown(f"- ❌ **{opt}** *(Lựa chọn của bạn)*")
                elif o_idx == q.correct_index and (correct or completed or len(attempts) >= 3):
                    st.markdown(f"- ✅ **{opt}** *(Đáp án đúng)*")
                elif o_idx == sel and correct:
                    st.markdown(f"- ✅ **{opt}** *(Lựa chọn của bạn)*")
                else:
                    st.markdown(f"- {opt}")

        if correct:
            with st.chat_message("assistant", avatar="🧭"):
                st.success(f"🎉 **Chính xác ở Lần {idx}!** Bạn đã nắm vững khái niệm này.")
        else:
            with st.chat_message("assistant", avatar="🧭"):
                st.warning(f"⚠️ **Chưa đúng ở Lần {idx}:** {feedback}")

    # If user answered correctly in any attempt, stop here
    if user_won:
        turn["completed"] = True
        return

    # 2. If 3 attempts completed and all 3 were incorrect:
    if len(attempts) >= 3:
        turn["completed"] = True
        with st.chat_message("assistant", avatar="🎓"):
            st.error("### 📝 Tổng hợp luồng câu hỏi & Giải thích chi tiết")
            st.markdown("---")
            st.markdown("#### 1. Tổng hợp chi tiết các lần trả lời:")
            for idx, att in enumerate(attempts, start=1):
                q = att["quiz"]
                sel = att["selected_index"]
                wrong_opt = q.options[sel]
                right_opt = q.options[q.correct_index]
                st.markdown(
                    f"**Lần {idx}:** {q.question}\n\n"
                    f"- ❌ **Bạn chọn:** `{wrong_opt}`\n"
                    f"- 💡 **Giải thích điểm chưa đúng:** {att['feedback']}\n"
                    f"- ✅ **Đáp án đúng:** `{right_opt}`\n"
                )
            st.markdown("---")
            st.markdown("#### 2. Kiến thức cốt lõi cần nhớ từ nguồn:")
            st.info(run.artifact.tutor_answer)
            st.markdown("---")
            st.markdown("#### 3. 🌟 Lời động viên:")
            st.success(
                "**Đừng nản lòng nhé!** Việc chưa chọn đúng qua các lần thử là cơ hội rất tốt để nhận ra "
                "những điểm tinh tế dễ nhầm lẫn trong tài liệu. Bạn đã học thêm được nhiều góc nhìn quan trọng "
                "qua các giải thích trên.\n\n"
                "Hãy đọc kỹ lại phần kiến thức cốt lõi ở trên và tiếp tục chọn một đoạn khác để rèn luyện nhé! 💪🎓"
            )
        return

    # Determine current attempt number (1, 2, or 3)
    current_attempt_num = len(attempts) + 1

    # 3. Determine current quiz for active attempt
    if current_attempt_num == 1:
        current_quiz = run.artifact.quiz
    else:
        quiz_key = f"quiz_attempt_{current_attempt_num}"
        if quiz_key in turn:
            current_quiz = turn[quiz_key]
        else:
            prev_att = attempts[-1]
            prev_quiz = prev_att["quiz"]
            wrong_opt = prev_quiz.options[prev_att["selected_index"]]
            with st.spinner("Đang tạo câu hỏi củng cố…"):
                current_quiz = generate_followup_quiz(
                    source_context=str(turn.get("source_context", "")),
                    previous_question=prev_quiz.question,
                    wrong_answer=wrong_opt,
                    misconception_feedback=prev_att["feedback"],
                    attempt_num=current_attempt_num,
                )
            turn[quiz_key] = current_quiz

    # 4. Render form for current attempt
    with st.chat_message("assistant", avatar="🧭"):
        header_text = (
            "**Kiểm tra bài**"
            if current_attempt_num == 1
            else "**Câu hỏi củng cố**"
        )
        st.markdown(header_text)
        st.write(current_quiz.question)
        st.caption(f"Nguồn: `{run.source_id}`")

        form_key = f"quiz-form-{turn['id']}-attempt-{current_attempt_num}"
        with st.form(form_key, border=False):
            selection = st.radio(
                "Chọn một đáp án",
                current_quiz.options,
                index=None,
                key=f"{form_key}-radio",
                label_visibility="collapsed",
            )
            submitted = st.form_submit_button(
                "Gửi đáp án", type="primary", use_container_width=True
            )
            if submitted and selection is None:
                st.warning("Hãy chọn một đáp án trước khi gửi.")
            elif submitted:
                selected_idx = current_quiz.options.index(selection)
                eval_res = evaluate_answer(run, selected_idx, quiz_override=current_quiz)
                attempts.append({
                    "attempt_num": current_attempt_num,
                    "quiz": current_quiz,
                    "selected_index": selected_idx,
                    "correct": eval_res["correct"],
                    "feedback": eval_res["feedback"],
                })
                if eval_res["correct"] or len(attempts) >= 3:
                    turn["completed"] = True
                st.rerun()

    if current_attempt_num == 1 and not attempts:
        if st.button("Bỏ qua / tiếp tục", key=f"skip-{turn['id']}"):
            turn["skipped"] = True
            st.rerun()