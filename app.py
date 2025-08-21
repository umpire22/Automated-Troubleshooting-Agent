import streamlit as st
import pandas as pd

# ---------- Custom Styling ----------
st.markdown(
    """
    <style>
        /* App background */
        .stApp {
            background: linear-gradient(135deg, #e0f7fa, #fce4ec);
            color: #333333;
            font-family: 'Segoe UI', sans-serif;
        }

        /* Titles */
        h1 {
            color: #1565c0;
            text-align: center;
            font-weight: bold;
            text-shadow: 1px 1px #90caf9;
        }
        h2, h3 {
            color: #ad1457;
            font-weight: 600;
        }

        /* Buttons */
        div.stButton > button {
            background: linear-gradient(90deg, #42a5f5, #7e57c2);
            color: white;
            border: none;
            border-radius: 12px;
            padding: 10px 20px;
            font-size: 16px;
            font-weight: bold;
            box-shadow: 2px 2px 5px rgba(0,0,0,0.2);
        }
        div.stButton > button:hover {
            background: linear-gradient(90deg, #1e88e5, #5e35b1);
            transform: scale(1.05);
        }

        /* Text area */
        textarea {
            border-radius: 10px !important;
            border: 2px solid #42a5f5 !important;
        }

        /* History table */
        table {
            border: 2px solid #ab47bc;
            border-radius: 10px;
            overflow: hidden;
        }
        th {
            background-color: #7e57c2 !important;
            color: white !important;
        }
        td {
            background-color: #f3e5f5 !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------- App Title ----------
st.title("🛠 Automated Troubleshooting Agent")
st.write("This agent helps diagnose and resolve common IT/software problems.")

# ---------- Initialize session state ----------
if "history" not in st.session_state:
    st.session_state.history = []
if "last_solution" not in st.session_state:
    st.session_state.last_solution = ""

# -------- Manual Troubleshooting --------
st.subheader("🔍 Describe Your Problem")

problem = st.text_area("Enter your issue here (e.g., 'WiFi not working', 'Laptop overheating').")

if st.button("🔎 Troubleshoot"):
    if "wifi" in problem.lower():
        solution = (
            "📡 **Possible Causes:**\n"
            "- Router not connected to internet\n"
            "- Wrong WiFi password\n"
            "- Network driver issue\n\n"
            "🛠 **Suggested Fixes:**\n"
            "1. Restart your router and check the cables.\n"
            "2. Verify that the password is correct.\n"
            "3. Update/reinstall your network adapter driver."
        )
        st.success(solution)

    elif "slow" in problem.lower():
        solution = (
            "🐢 **Possible Causes:**\n"
            "- Too many background apps\n"
            "- Low RAM\n"
            "- Malware infection\n\n"
            "🛠 **Suggested Fixes:**\n"
            "1. Close unused programs.\n"
            "2. Upgrade RAM if possible.\n"
            "3. Run a full antivirus scan."
        )
        st.warning(solution)

    elif "overheat" in problem.lower() or "hot" in problem.lower():
        solution = (
            "🔥 **Possible Causes:**\n"
            "- Dust buildup in cooling fan\n"
            "- High CPU usage\n"
            "- Poor ventilation\n\n"
            "🛠 **Suggested Fixes:**\n"
            "1. Clean cooling vents and fans.\n"
            "2. Monitor CPU usage in Task Manager.\n"
            "3. Place laptop on a cooling pad for better airflow."
        )
        st.error(solution)

    else:
        solution = "🤔 Sorry, I don’t recognize that problem yet. Try describing it differently."
        st.info(solution)

    # Save to history
    st.session_state.history.append({"Problem": problem, "Solution": solution})
    st.session_state.last_solution = f"Problem: {problem}\n\nSolution:\n{solution}"

# -------- Extra Buttons --------
if st.session_state.last_solution:
    st.download_button(
        label="⬇️ Download Last Solution",
        data=st.session_state.last_solution,
        file_name="solution.txt",
        mime="text/plain"
    )

if st.button("🧹 Clear All"):
    st.session_state.history = []
    st.session_state.last_solution = ""
    st.experimental_rerun()

# -------- History Log --------
if st.session_state.history:
    st.subheader("📜 Troubleshooting History")

    # Add search bar
    search_term = st.text_input("🔍 Search history by keyword")
    hist_df = pd.DataFrame(st.session_state.history)

    if search_term:
        filtered = hist_df[hist_df.apply(lambda row: search_term.lower() in row.to_string().lower(), axis=1)]
        st.table(filtered)
    else:
        st.table(hist_df)

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
    st.download_button(
        "⬇️ Download Results",
        data=df.to_csv(index=False),
        file_name="troubleshooting_results.csv",
        mime="text/csv"
    )

