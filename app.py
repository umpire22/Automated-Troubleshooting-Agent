import streamlit as st
import pandas as pd

st.title("🛠 Automated Troubleshooting Agent")

st.write("This agent helps diagnose and resolve common IT/software problems.")

# -------- Manual Troubleshooting --------
st.subheader("🔍 Describe Your Problem")

problem = st.text_area("Enter your issue here (e.g., 'WiFi not working', 'Laptop overheating').")

if st.button("Troubleshoot"):
    if "wifi" in problem.lower():
        st.write("📡 Possible Causes:")
        st.write("- Router not connected to internet")
        st.write("- Wrong WiFi password")
        st.write("- Network driver issue")

        st.write("🛠 Suggested Fixes:")
        st.write("1. Restart your router and check the cables.")
        st.write("2. Verify that the password is correct.")
        st.write("3. Update/reinstall your network adapter driver.")

    elif "slow" in problem.lower():
        st.write("🐢 Possible Causes:")
        st.write("- Too many background apps")
        st.write("- Low RAM")
        st.write("- Malware infection")

        st.write("🛠 Suggested Fixes:")
        st.write("1. Close unused programs.")
        st.write("2. Upgrade RAM if possible.")
        st.write("3. Run a full antivirus scan.")

    elif "overheat" in problem.lower() or "hot" in problem.lower():
        st.write("🔥 Possible Causes:")
        st.write("- Dust buildup in cooling fan")
        st.write("- High CPU usage")
        st.write("- Poor ventilation")

        st.write("🛠 Suggested Fixes:")
        st.write("1. Clean cooling vents and fans.")
        st.write("2. Monitor CPU usage in Task Manager.")
        st.write("
