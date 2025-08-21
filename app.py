import streamlit as st
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

st.title("🛠 Automated Troubleshooting Agent with Email Alerts")

# --------- Email Sending Function ----------
def send_email(receiver, subject, message):
    sender_email = "your_email@gmail.com"        # change this
    sender_password = "your_app_password"        # use Gmail App Password
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

# -------- Manual Troubleshooting --------
st.subheader("🔍 Describe Your Problem")

problem = st.text_area("Enter your issue here (e.g., 'WiFi not working', 'Laptop overheating').")
user_email = st.text_input("Enter your email to receive the troubleshooting steps:")

if st.button("Troubleshoot"):
    solution = ""
    if "wifi" in problem.lower():
        solution = """📡 Possible Causes:
- Router not connected
- Wrong WiFi password
- Driver issue

🛠 Fixes:
1. Restart router
2. Verify password
3. Update drivers"""
    elif "slow" in problem.lower():
        solution = """🐢 Possible Causes:
- Too many apps
- Low RAM
- Malware

🛠 Fixes:
1. Close unused apps
2. Upgrade RAM
3. Run antivirus"""
    elif "overheat" in problem.lower() or "hot" in problem.lower():
        solution = """🔥 Possible Causes:
- Dust in fan
- High CPU usage
- Poor ventilation

🛠 Fixes:
1. Clean fans
2. Check Task Manager
3. Use cooling pad"""
    else:
        solution = "🤔 Sorry, I don’t recognize that problem yet."

    st.write(solution)import streamlit as st
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Load secrets from Streamlit Cloud
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

    
    
    

    
