import streamlit as st
import sqlite3
import os
import shutil
from datetime import datetime
from auth import create_user, verify_user, init_db

# =====================================
# Page Configuration
# =====================================

st.set_page_config(
    page_title="Medical Record",
    page_icon="🗂️",
    layout="wide"
)

# =====================================
# Custom Theme (matches rest of app)
# =====================================

st.markdown("""
<style>

#MainMenu{visibility:hidden;}
header{visibility:hidden;}
footer{visibility:hidden;}

.stApp{
    background: radial-gradient(circle at 20% 0%, #16213E 0%, #0D1321 60%, #060911 100%);
}

h1{
    text-align:center;
    background:linear-gradient(90deg,#FFFFFF,#8FD3FF);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
    font-size:36px;
    font-weight:800;
}

.section-card{
    background:rgba(255,255,255,0.04);
    border:1px solid rgba(255,255,255,0.08);
    backdrop-filter:blur(8px);
    border-radius:20px;
    padding:26px 28px;
    margin-bottom:22px;
}

.section-card h3{
    color:#FFFFFF !important;
    text-align:center;
}

.stTextInput input{
    border-radius:12px;
    border:1px solid rgba(255,255,255,0.15);
    background:rgba(255,255,255,0.03);
    color:#FFFFFF;
    padding:10px;
}

[data-testid="stFileUploader"]{
    border-radius:14px;
    border:1px dashed rgba(78,168,255,0.5);
    background:rgba(255,255,255,0.02);
    padding:20px;
}

.stButton>button{
    background:linear-gradient(135deg,#223A5E,#2E4F7C);
    color:#E8EEF6;
    border:1px solid rgba(255,255,255,0.08);
    border-radius:12px;
    font-size:16px;
    font-weight:600;
    padding:10px 24px;
    box-shadow:0 2px 8px rgba(0,0,0,0.3);
    transition:0.25s;
}
.stButton>button:hover{
    background:linear-gradient(135deg,#2A4670,#355A8C);
    transform:translateY(-1px);
}

.stDownloadButton>button{
    background:linear-gradient(135deg,#22A366,#1B7F4F);
    color:white;
    border-radius:12px;
    font-weight:700;
    border:none;
}

.record-row{
    background:rgba(255,255,255,0.03);
    border:1px solid rgba(255,255,255,0.08);
    border-radius:12px;
    padding:14px 18px;
    margin-bottom:10px;
    display:flex;
    justify-content:space-between;
    align-items:center;
}

.block-container{
    max-width:850px;
    margin:auto;
    padding-top:3rem;
}

</style>
""", unsafe_allow_html=True)

RECORDS_DB = "medical_records.db"
RECORDS_DIR = "stored_records"
os.makedirs(RECORDS_DIR, exist_ok=True)


def init_records_db():
    conn = sqlite3.connect(RECORDS_DB)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            patient_name TEXT NOT NULL,
            file_name TEXT NOT NULL,
            stored_path TEXT NOT NULL,
            uploaded_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def save_record(username, patient_name, uploaded_file):
    init_records_db()

    safe_patient = "".join(c for c in patient_name if c.isalnum() or c in (" ", "_", "-")).strip()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    stored_filename = f"{username}_{safe_patient}_{timestamp}_{uploaded_file.name}"
    stored_path = os.path.join(RECORDS_DIR, stored_filename)

    with open(stored_path, "wb") as f:
        shutil.copyfileobj(uploaded_file, f)

    conn = sqlite3.connect(RECORDS_DB)
    c = conn.cursor()
    c.execute(
        """INSERT INTO records (username, patient_name, file_name, stored_path, uploaded_at)
           VALUES (?, ?, ?, ?, ?)""",
        (username, patient_name, uploaded_file.name, stored_path, datetime.now().strftime("%d-%m-%Y %H:%M"))
    )
    conn.commit()
    conn.close()


def get_records(username):
    init_records_db()
    conn = sqlite3.connect(RECORDS_DB)
    c = conn.cursor()
    c.execute(
        "SELECT patient_name, file_name, stored_path, uploaded_at FROM records WHERE username = ? ORDER BY id DESC",
        (username,)
    )
    rows = c.fetchall()
    conn.close()
    return rows


# =====================================
# Session State
# =====================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = None

st.markdown("<h1>🗂️ Medical Record</h1>", unsafe_allow_html=True)

# =====================================
# Not logged in -> Show Login / Sign Up
# =====================================

if not st.session_state.logged_in:

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("<h3>🔐 Login or Sign Up to manage medical records</h3>", unsafe_allow_html=True)

    tab_login, tab_signup = st.tabs(["Login", "Sign Up"])

    with tab_login:
        login_user = st.text_input("Username", key="login_user")
        login_pass = st.text_input("Password", type="password", key="login_pass")

        if st.button("Login", key="login_btn"):
            if not login_user or not login_pass:
                st.error("Please enter both username and password.")
            else:
                success, msg = verify_user(login_user, login_pass)
                if success:
                    st.session_state.logged_in = True
                    st.session_state.username = login_user
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)

    with tab_signup:
        signup_user = st.text_input("Choose a Username", key="signup_user")
        signup_pass = st.text_input("Choose a Password", type="password", key="signup_pass")
        signup_pass_confirm = st.text_input("Confirm Password", type="password", key="signup_pass_confirm")

        if st.button("Create Account", key="signup_btn"):
            if not signup_user or not signup_pass:
                st.error("Please fill in all fields.")
            elif signup_pass != signup_pass_confirm:
                st.error("Passwords do not match.")
            else:
                success, msg = create_user(signup_user, signup_pass)
                if success:
                    st.success(msg + " Please log in from the Login tab.")
                else:
                    st.error(msg)

    st.markdown('</div>', unsafe_allow_html=True)

# =====================================
# Logged in -> Upload + View Records
# =====================================

else:

    st.markdown(
        f'<p style="text-align:center;color:#A9B4C4;">Logged in as <b>{st.session_state.username}</b></p>',
        unsafe_allow_html=True
    )

    col_a, col_b = st.columns([1, 5])
    with col_a:
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.rerun()

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("<h3>📤 Upload Medical Record</h3>", unsafe_allow_html=True)

    patient_name = st.text_input("Patient Name", placeholder="Enter Patient Name")
    record_file = st.file_uploader(
        "Upload a medical record (PDF, image, or document)",
        type=["pdf", "png", "jpg", "jpeg", "docx"]
    )

    if st.button("Save Record"):
        if not patient_name:
            st.error("Please enter the patient name.")
        elif not record_file:
            st.error("Please choose a file to upload.")
        else:
            save_record(st.session_state.username, patient_name, record_file)
            st.success("✅ Medical record saved successfully.")
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("<h3>📁 Your Stored Records</h3>", unsafe_allow_html=True)

    records = get_records(st.session_state.username)

    if not records:
        st.markdown(
            '<p style="text-align:center;color:#5C6577;">No records uploaded yet.</p>',
            unsafe_allow_html=True
        )
    else:
        for patient, fname, path, uploaded_at in records:
            c1, c2 = st.columns([4, 1])
            with c1:
                st.markdown(
                    f'<div class="record-row"><div><b>{patient}</b><br>'
                    f'<span style="color:#8B96A6;font-size:13px;">{fname} — {uploaded_at}</span></div></div>',
                    unsafe_allow_html=True
                )
            with c2:
                if os.path.exists(path):
                    with open(path, "rb") as f:
                        st.download_button(
                            "⬇ Download",
                            data=f,
                            file_name=fname,
                            key=f"dl_{path}"
                        )

    st.markdown('</div>', unsafe_allow_html=True)