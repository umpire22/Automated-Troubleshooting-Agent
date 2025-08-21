import streamlit as st
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Load secrets (stored safely in Streamlit Cloud settings)
EMAIL_USER = st.secrets["EMAIL_USER"]
EMAIL_PASS = st.secrets["EMAIL_PASS"]

def send_email(receiver, subject, message):
    sender_email = EMAIL_USER
    sender_password = EMAIL_PASS
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    try:
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = receiver
        msg["Subject"] = subject
        msg.attach(MIMEText(message, "plain"))

        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        return str(e)


# Streamlit UI
st.title("🔧 Automated Troubleshooting Agent")
st.write("This agent suggests fixes for common technical problems and can send them to your email.")

# Input area
problem = st.text_area("Describe your issue:")
email = st.text_input("Enter your email (to get the solution):")

if st.button("Analyze Problem"):
    if problem.strip() == "":
        st.warning("⚠️ Please describe your issue first.")
    else:
        # Simple troubleshooting suggestions
        if "wifi" in problem.lower():
            solution = "Check your router, restart it, or try reconnecting to the network."
        elif "slow" in problem.lower():
            solution = "Close unused programs, clear cache, and restart your device."
        elif "error" in problem.lower():
            solution = "Search the error code online, reinstall the app, or check for updates."
        else:
            solution = "Try basic troubleshooting: restart device, check connections, and update software."

        st.success(f"✅ Suggested Solution: {solution}")

        if email:
            status = send_email(
                email,
                "Troubleshooting Suggestion",
                f"Problem: {problem}\n\nSuggested Solution: {solution}"
            )
            if status is True:
                st.info(f"📧 Solution also sent to {email}")
            else:
                st.error(f"❌ Failed to send email: {status}")
