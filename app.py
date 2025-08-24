import io
import streamlit as st
import pandas as pd

st.title("⚡ Automated Troubleshooting Agent")

# --- Upload Method ---
st.subheader("📂 Upload a File")
uploaded_file = st.file_uploader("Upload a text file with issues", type=["txt"])

# --- Manual Input Method ---
st.subheader("📝 Manual Input Troubleshooting")
manual_input = st.text_area("Enter your problem(s) here (one per line):")

problems, results = [], []

if uploaded_file:
    problems = uploaded_file.read().decode("utf-8").splitlines()

elif manual_input:
    problems = manual_input.split("\n")

if problems:
    for issue in problems:
        if "wifi" in issue.lower():
            results.append("Check router, verify password, update drivers")
        elif "slow" in issue.lower():
            results.append("Close apps, upgrade RAM, scan for malware")
        elif "overheat" in issue.lower() or "hot" in issue.lower():
            results.append("Clean fans, check CPU usage, use cooling pad")
        else:
            results.append("Unknown issue — please provide more details")

    df = pd.DataFrame({"Problem": problems, "Suggested Solution": results})
    st.write("🔎 Troubleshooting Results:", df)

    # --- CSV download ---
    st.download_button(
        "⬇️ Download as CSV",
        df.to_csv(index=False),
        "results.csv",
        "text/csv",
        key="download-csv"
    )

    # --- Excel download ---
    excel_buffer = io.BytesIO()
    with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Results")
    excel_buffer.seek(0)

    st.download_button(
        "⬇️ Download as Excel",
        excel_buffer,
        "results.xlsx",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        key="download-excel"
    )

# --- Custom CSS for button colors ---
st.markdown("""
    <style>
    div[data-testid="stDownloadButton"] > button,
    div[data-testid="stFileUploader"] button,
    div[data-testid="stTextArea"] textarea {
        border-radius: 8px;
        font-weight: 600;
        padding: 0.6em 1.2em;
    }

    /* Upload button (purple) */
    div[data-testid="stFileUploader"] button {
        background-color: #9C27B0;
        color: white;
    }

    /* CSV button (green) */
    div[data-testid="stDownloadButton"][key="download-csv"] > button {
        background-color: #4CAF50;
        color: white;
    }

    /* Excel button (blue) */
    div[data-testid="stDownloadButton"][key="download-excel"] > button {
        background-color: #2196F3;
        color: white;
    }

    /* Text area (manual input box highlight) */
    div[data-testid="stTextArea"] textarea {
        border: 2px solid #FF9800; /* Orange border */
        font-weight: 500;
    }
    </style>
""", unsafe_allow_html=True)
