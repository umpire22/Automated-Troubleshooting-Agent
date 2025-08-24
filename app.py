import streamlit as st
import pandas as pd

st.set_page_config(page_title="Troubleshooting Agent", page_icon="🛠️", layout="centered")

# --- Styling ---
st.markdown(
    """
    <style>
        .stApp {
            background: linear-gradient(135deg, #89f7fe 0%, #66a6ff 100%);
            color: black;
        }
        .download-btn {
            background-color: #ff6f61;
            color: white;
            font-weight: bold;
            border-radius: 12px;
            padding: 8px 16px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🛠️ Automated Troubleshooting Agent")

# --- Function to analyze issues ---
def analyze_issues(issues):
    results = []
    for issue in issues:
        if "wifi" in issue.lower():
            results.append("Check router, verify password, update drivers")
        elif "slow" in issue.lower():
            results.append("Close apps, upgrade RAM, scan for malware")
        elif "overheat" in issue.lower() or "hot" in issue.lower():
            results.append("Clean fans, check CPU usage, use cooling pad")
        else:
            results.append("Unknown issue — please provide more details")
    return pd.DataFrame({"Problem": issues, "Suggested Solution": results})

# ---------------- Manual Input ----------------
st.subheader("📝 Manual Input")
manual_problem = st.text_input("Enter a problem (e.g., 'My laptop is slow'):")
manual_list = st.session_state.get("manual_list", [])

if st.button("Add Problem"):
    if manual_problem.strip():
        manual_list.append(manual_problem.strip())
        st.session_state["manual_list"] = manual_list

if manual_list:
    st.write("Problems Entered:", manual_list)
    df = analyze_issues(manual_list)
    st.write("🔎 Troubleshooting Results:", df)

    st.download_button("⬇️ Download as CSV", df.to_csv(index=False), "results.csv", "text/csv")
    st.download_button("⬇️ Download as Excel", df.to_excel("results.xlsx", index=False, engine="openpyxl"), "results.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

# ---------------- Copy & Paste ----------------
st.subheader("✍️ Paste Your Problems")
user_input = st.text_area("Paste problems here (one per line):")

if user_input:
    issues = [line.strip() for line in user_input.split("\n") if line.strip()]
    df = analyze_issues(issues)
    st.write("🔎 Troubleshooting Results:", df)

    st.download_button("⬇️ Download as CSV", df.to_csv(index=False), "results.csv", "text/csv")
    st.download_button("⬇️ Download as Excel", df.to_excel("results.xlsx", index=False, engine="openpyxl"), "results.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

# ---------------- File Upload ----------------
st.subheader("📂 Bulk Upload (CSV, Excel, TXT)")
uploaded_file = st.file_uploader("Upload file with a column named 'Problem'", type=["csv", "xlsx", "txt"])

if uploaded_file is not None:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith(".xlsx"):
        df = pd.read_excel(uploaded_file)
    elif uploaded_file.name.endswith(".txt"):
        with open(uploaded_file, "r") as f:
            lines = f.readlines()
        df = pd.DataFrame({"Problem": [line.strip() for line in lines if line.strip()]})

    st.write("Uploaded Problems:", df)
    df = analyze_issues(df["Problem"].tolist())
    st.write("🔎 Troubleshooting Results:", df)

    st.download_button("⬇️ Download as CSV", df.to_csv(index=False), "results.csv", "text/csv")
    st.download_button("⬇️ Download as Excel", df.to_excel("results.xlsx", index=False, engine="openpyxl"), "results.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
