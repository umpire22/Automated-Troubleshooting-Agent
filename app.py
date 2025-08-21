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
        st.write("3. Place laptop on a cooling pad for better airflow.")

    else:
        st.write("🤔 Sorry, I don’t recognize that problem yet. Try describing it differently.")

# -------- Bulk Troubleshooting --------
st.subheader("📂 Bulk Troubleshooting via CSV")

uploaded_file = st.file_uploader("Upload a CSV file with a column named 'Problem'", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write("Uploaded Problems:", df)

    results = []
    for issue in df["Problem"]:
        if "wifi" in issue.lower():
            results.append("Check router, verify password, update drivers")
        elif "slow" in issue.lower():
            results.append("Close apps, upgrade RAM, scan for malware")
        elif "overheat" in issue.lower() or "hot" in issue.lower():
            results.append("Clean fans, check CPU usage, use cooling pad")
        else:
            results.append("Unknown issue — please provide more details")

    df["Suggested Solution"] = results
    st.write("🔎 Troubleshooting Results:", df)

    # Option to download results
    df.to_csv("troubleshooting_results.csv", index=False)
    st.download_button("⬇️ Download Results", data=df.to_csv(index=False), file_name="troubleshooting_results.csv", mime="text/csv")
# Download button
if st.session_state.solution:
    st.download_button(
        label="📥 Download Solution",
        data=f"Problem: {problem}\n\nSuggested Solution: {st.session_state.solution}",
        file_name="solution.txt",
        mime="text/plain"
    )

# Clear button
if st.button("🧹 Clear All"):
    st.session_state.problem = ""
    st.session_state.solution = ""
    st.session_state.email = ""
    st.experimental_rerun()
