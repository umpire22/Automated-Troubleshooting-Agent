import io
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Troubleshooting Agent", page_icon="⚡", layout="centered")

# --- Header with custom color ---
st.markdown("""
    <h1 style='text-align: center; color: #FF5722; font-size: 2.5em;'>
        ⚡ Automated Troubleshooting Agent
    </h1>
""", unsafe_allow_html=True)

# --- Upload Method ---
st.subheader("📂 Upload a File")
uploaded_file = st.file_uploader("Upload a text file with issues", type=["txt"])

# --- Manual Input Method ---
st.subheader("📝 Manual Input (copy & paste supported)")
manual_input = st.text_area("Paste your problem(s) here (one per line):", key="text_area")

col1, col2, col3 = st.columns([1,1,2])
with col1:
    analyze_clicked = st.button("🔍 Analyze Problems")
with col2:
    clear_clicked = st.button("🧹 Clear All")
with col3:
    paste_clicked = st.button("📋 Paste from Clipboard")

if clear_clicked:
    st.session_state["text_area"] = ""  # clears text area

if paste_clicked:
    st.session_state["text_area"] = st.experimental_get_query_params().get("clipboard", [""])[0]

problems, results = [], []

if analyze_clicked:
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
        st.success("✅ Analysis complete! See results below.")

        # --- Centered Results Table ---
        st.markdown("<div class='centered'>", unsafe_allow_html=True)
        st.write("🔎 Troubleshooting Results:")
        st.dataframe(df, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

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

# --- Custom CSS for styling ---
st.markdown("""
    <style>
    /* Center elements */
    .centered {
        display: flex;
        justify-content: center;
        margin: 20px 0;
    }

    /* Upload + buttons styling */
    div[data-testid="stDownloadButton"] > button,
    div[data-testid="stFileUploader"] button,
    div[data-testid="stTextArea"] textarea,
    div[data-testid="stButton"] > button {
        border-radius: 10px;
        font-weight: 600;
        padding: 0.6em 1.4em;
        transition: 0.3s;
    }

    /* Upload button (purple) */
    div[data-testid="stFileUploader"] button {
        background-color: #9C27B0;
        color: white;
    }
    div[data-testid="stFileUploader"] button:hover {
        background-color: #7B1FA2;
    }

    /* Analyze button (orange gradient) */
    div[data-testid="stButton"] > button:has(span:contains("Analyze")) {
        background: linear-gradient(45deg, #FF5722, #FFC107);
        color: white;
        font-size: 1.1em;
        border: none;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.2);
    }

    /* Clear button (grey) */
    div[data-testid="stButton"] > button:has(span:contains("Clear")) {
        background-color: #9E9E9E;
        color: white;
    }

    /* Paste button (teal) */
    div[data-testid="stButton"] > button:has(span:contains("Paste")) {
        background-color: #009688;
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

    /* Text area */
    div[data-testid="stTextArea"] textarea {
        border: 2px solid #1E88E5; 
        font-weight: 500;
        background: #FFFFFF;   /* plain white */
        color: #000000;        /* black text */
    }

    /* Results table */
    .stDataFrame {
        border: 2px solid #4CAF50;
        border-radius: 10px;
    }

    /* Make dataframe header row bold & colorful */
    .stDataFrame thead tr th {
        background-color: #FF5722 !important;
        color: white !important;
        font-weight: bold;
        text-align: center !important;
    }
    </style>
""", unsafe_allow_html=True)
