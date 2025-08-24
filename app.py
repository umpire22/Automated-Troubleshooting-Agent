import re
import streamlit as st
import pandas as pd
import PyPDF2

st.subheader("📂 Bulk Troubleshooting")

# --- Option 1: File Upload ---
uploaded_file = st.file_uploader(
    "Upload a file with problems (CSV, Excel, TXT, or PDF)", 
    type=["csv", "xlsx", "txt", "pdf"]
)

# --- Option 2: Copy-Paste ---
pasted_text = st.text_area(
    "Or just paste your problems here (one per line):",
    placeholder="Example:\nWiFi not connecting\nLaptop overheating\nComputer very slow"
)

df = None

# --- If file is uploaded ---
if uploaded_file is not None:
    file_type = uploaded_file.name.split(".")[-1].lower()

    if file_type == "csv":
        df = pd.read_csv(uploaded_file)
    elif file_type == "xlsx":
        df = pd.read_excel(uploaded_file)
    elif file_type == "txt":
        text = uploaded_file.read().decode("utf-8").splitlines()
        clean_lines = [line.strip() for line in text if len(line.strip()) > 3]
        df = pd.DataFrame({"Problem": clean_lines})
    elif file_type == "pdf":
        reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        lines = text.splitlines()
        clean_lines = [
            line.strip() for line in lines
            if len(line.strip()) > 3 and not re.match(r"^\d+$", line.strip())
        ]
        df = pd.DataFrame({"Problem": clean_lines})

# --- If text is pasted ---
elif pasted_text.strip() != "":
    lines = pasted_text.splitlines()
    clean_lines = [line.strip() for line in lines if len(line.strip()) > 3]
    df = pd.DataFrame({"Problem": clean_lines})

# --- Process problems ---
if df is not None and "Problem" in df.columns:
    st.write("📌 Problems to Analyze:", df)

    results = []
    for issue in df["Problem"]:
        issue_lower = issue.lower()
        if "wifi" in issue_lower:
            results.append("Check router, verify password, update drivers")
        elif "slow" in issue_lower:
            results.append("Close apps, upgrade RAM, scan for malware")
        elif "overheat" in issue_lower or "hot" in issue_lower:
            results.append("Clean fans, check CPU usage, use cooling pad")
        else:
            results.append("Unknown issue — please provide more details")

    df["Suggested Solution"] = results
    st.write("🔎 Troubleshooting Results:", df)

    # Download button
    st.download_button(
        "⬇️ Download Results",
        data=df.to_csv(index=False),
        file_name="troubleshooting_results.csv",
        mime="text/csv"
    )
else:
    st.info("Upload a file or paste problems above to begin.")
