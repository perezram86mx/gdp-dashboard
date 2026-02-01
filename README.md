import streamlit as st
import pandas as pd
from datetime import datetime

st.title("Rhetorical Analysis Quiz")

# ----------------------
# Questions
# ----------------------
questions = [
    {
        "question": "Which rhetorical appeal focuses on credibility?",
        "options": ["Ethos", "Pathos", "Logos"],
        "answer": "Ethos"
    },
    {
        "question": "Which appeal is based on emotion?",
        "options": ["Logos", "Ethos", "Pathos"],
        "answer": "Pathos"
    },
    {
        "question": "Statistics and evidence mainly appeal to:",
        "options": ["Pathos", "Logos", "Ethos"],
        "answer": "Logos"
    }
]

# ----------------------
# Session state
# ----------------------
if "responses" not in st.session_state:
    st.session_state.responses = []
    st.session_state.score = 0
    st.session_state.submitted = False

# ----------------------
# Student info
# ----------------------
student_name = st.text_input("Student name")

# ----------------------
# Quiz
# ----------------------
if student_name and not st.session_state.submitted:
    for i, q in enumerate(questions):
        st.write(f"**Question {i+1}:** {q['question']}")
        answer = st.radio(
            "Select an answer:",
            q["options"],
            key=f"q{i}"
        )
        st.session_state.responses.append(answer)

    if st.button("Submit Quiz"):
        st.session_state.score = sum(
            1 for i, q in enumerate(questions)
            if st.session_state.responses[i] == q["answer"]
        )
        st.session_state.submitted = True

# ----------------------
# Results + CSV export
# ----------------------
if st.session_state.submitted:
    st.success(
        f"Quiz complete! Score: "
        f"{st.session_state.score} / {len(questions)}"
    )

    # Build results table
    data = {
        "Student": student_name,
        "Score": st.session_state.score,
        "Total Questions": len(questions),
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    df = pd.DataFrame([data])

    st.dataframe(df)

    # Export CSV
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download results as CSV",
        data=csv,
        file_name="quiz_results.csv",
        mime="text/csv"
    )