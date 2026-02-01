import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Try to load environment variables if available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

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
# Session state initialization
# ----------------------
if "responses" not in st.session_state:
    st.session_state.responses = {}
    st.session_state.score = 0
    st.session_state.submitted = False
    st.session_state.student_name = ""

# ----------------------
# Student info
# ----------------------
student_name = st.text_input("Student name", key="student_input")

# ----------------------
# Email sending function
# ----------------------
def send_quiz_results_email(student_name, score, total_questions, responses, questions):
    """Send quiz results to teacher's email"""
    try:
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        
        # Email configuration
        sender_email = os.getenv("EMAIL_ADDRESS")
        sender_password = os.getenv("EMAIL_PASSWORD")
        teacher_email = os.getenv("TEACHER_EMAIL", sender_email)
        
        # If email is not configured, just show success message
        if not sender_email or not sender_password:
            st.info("📧 Email configuration not found. Results will not be emailed to teacher.")
            return True
        
        # Build detailed response table
        response_details = ""
        for i, q in enumerate(questions):
            is_correct = responses.get(i) == q["answer"]
            response_details += f"\nQuestion {i+1}: {q['question']}\n"
            response_details += f"Student's Answer: {responses.get(i, 'Not answered')}\n"
            response_details += f"Correct Answer: {q['answer']}\n"
            response_details += f"Status: {'✓ Correct' if is_correct else '✗ Incorrect'}\n"
            response_details += "-" * 50
        
        # Create message
        message = MIMEMultipart("alternative")
        message["Subject"] = f"Quiz Submission: {student_name}"
        message["From"] = sender_email
        message["To"] = teacher_email
        
        # Email body
        text = f"""
        New Quiz Submission
        
        Student Name: {student_name}
        Score: {score} / {total_questions}
        Percentage: {(score/total_questions)*100:.1f}%
        Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        
        Detailed Responses:
        {response_details}
        """
        
        html = f"""
        <html>
          <body>
            <h2>New Quiz Submission</h2>
            <ul>
              <li><strong>Student Name:</strong> {student_name}</li>
              <li><strong>Score:</strong> {score} / {total_questions}</li>
              <li><strong>Percentage:</strong> {(score/total_questions)*100:.1f}%</li>
              <li><strong>Timestamp:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</li>
            </ul>
            <h3>Detailed Responses:</h3>
            <pre>{response_details}</pre>
          </body>
        </html>
        """
        
        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")
        message.attach(part1)
        message.attach(part2)
        
        # Send email
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, teacher_email, message.as_string())
        
        return True
    except Exception as e:
        st.error(f"Failed to send email: {str(e)}")
        return False

# ----------------------
# Quiz
# ----------------------
if student_name:
    st.session_state.student_name = student_name
    
    if not st.session_state.submitted:
        st.subheader("Please answer all questions:")
        
        for i, q in enumerate(questions):
            st.markdown(f"### Question {i+1}: {q['question']}")
            
            answer = st.radio(
                "Select an answer:",
                q["options"],
                key=f"q{i}",
                label_visibility="collapsed"
            )
            st.session_state.responses[i] = answer
            st.divider()
        
        # Submit button
        col1, col2 = st.columns([1, 3])
        with col1:
            submit = st.button("Submit Quiz", type="primary")
        
        if submit:
            # Check if all questions are answered
            if len(st.session_state.responses) == len(questions):
                st.session_state.score = sum(
                    1 for i, q in enumerate(questions)
                    if st.session_state.responses.get(i) == q["answer"]
                )
                st.session_state.submitted = True
                
                # Send email with results to teacher
                with st.spinner("Sending submission to teacher..."):
                    if send_quiz_results_email(student_name, st.session_state.score, len(questions), st.session_state.responses, questions):
                        st.success("Quiz submitted! Your results have been sent to your teacher.")
                        st.rerun()
            else:
                st.error("Please answer all questions before submitting.")

# ----------------------
# Results + CSV export
# ----------------------
if st.session_state.submitted and st.session_state.student_name:
    st.divider()
    st.subheader("Quiz Results")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Score", f"{st.session_state.score}/{len(questions)}")
    with col2:
        percentage = (st.session_state.score / len(questions)) * 100
        st.metric("Percentage", f"{percentage:.1f}%")
    with col3:
        status = "✓ Passed" if percentage >= 70 else "✗ Review Needed"
        st.metric("Status", status)
    
    st.divider()
    
    # Show detailed answers
    st.subheader("Your Answers:")
    for i, q in enumerate(questions):
        is_correct = st.session_state.responses.get(i) == q["answer"]
        status_icon = "✓" if is_correct else "✗"
        
        with st.container(border=True):
            st.write(f"{status_icon} **Question {i+1}:** {q['question']}")
            st.write(f"Your answer: **{st.session_state.responses.get(i)}**")
            if not is_correct:
                st.write(f"Correct answer: **{q['answer']}**")
    
    st.divider()
    
    # Build results table
    results_data = {
        "Student Name": [st.session_state.student_name],
        "Score": [st.session_state.score],
        "Total Questions": [len(questions)],
        "Percentage": [f"{(st.session_state.score/len(questions))*100:.1f}%"],
        "Timestamp": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
    }
    
    # Add individual question results
    for i, q in enumerate(questions):
        results_data[f"Q{i+1}"] = [st.session_state.responses.get(i)]
    
    df = pd.DataFrame(results_data)
    
    st.dataframe(df, use_container_width=True)
    
    # Export CSV
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download results as CSV",
        data=csv,
        file_name=f"quiz_results_{st.session_state.student_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv"
    )
    
    # Reset quiz option
    if st.button("Take Quiz Again"):
        st.session_state.responses = {}
        st.session_state.score = 0
        st.session_state.submitted = False
        st.session_state.student_name = ""
        st.rerun()