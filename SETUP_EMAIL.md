# Rhetorical Analysis Quiz with Email Results

A Streamlit application for conducting rhetorical analysis quizzes with automatic email delivery of results.

## Features

- Interactive quiz interface
- Automatic email notifications with quiz results
- Results summary with score and timestamp
- CSV export option

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Email Settings

This app uses Gmail SMTP to send results via email. Follow these steps:

1. **Enable 2-Factor Authentication** on your Google account at https://myaccount.google.com/security

2. **Generate an App Password**:
   - Go to https://myaccount.google.com/apppasswords
   - Select "Mail" and "Windows Computer" (or your device)
   - Google will generate a 16-character password
   - Copy this password

3. **Create a `.env` file** in the project root:
   ```
   EMAIL_ADDRESS=your-email@gmail.com
   EMAIL_PASSWORD=your-16-character-app-password
   ```

   You can copy from `.env.example` and fill in your credentials:
   ```bash
   cp .env.example .env
   ```

### 3. Run the Application

```bash
streamlit run streamlit_app.py
```

The app will open in your browser at `http://localhost:8501`

## How It Works

1. Student enters their name and email address
2. Student completes the quiz
3. Upon submission, quiz results are automatically emailed to the student
4. Results are displayed on screen with option to download as CSV

## Email Template

The email includes:
- Student name personalization
- Final score and total questions
- Percentage score
- Timestamp of submission
- HTML formatted email for better presentation

## Security Notes

- **Never commit `.env` file** - it's already in `.gitignore`
- Use App Passwords (not your actual Google password)
- Keep your email credentials confidential
- The `.env` file is only read on application startup

## Troubleshooting

**"Email configuration not found" error:**
- Ensure `.env` file exists in the project root
- Verify `EMAIL_ADDRESS` and `EMAIL_PASSWORD` are set correctly
- Make sure the app password is exactly 16 characters (spaces included)

**"Failed to send email" error:**
- Check that 2-Factor Authentication is enabled on your Google account
- Verify the app password is correct (copy-paste again from myaccount.google.com)
- Ensure the recipient email address is valid
- Check your internet connection
