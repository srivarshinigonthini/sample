import streamlit as st

# ---------------------------------
# Page Configuration
# ---------------------------------
st.set_page_config(
    page_title="Diabetic Foot Ulcer Detection System",
    page_icon="🦶",
    layout="wide"
)

# ---------------------------------
# Custom CSS - Dark hero, glass cards
# ---------------------------------
st.markdown("""
<style>

#MainMenu{visibility:hidden;}
header{visibility:hidden;}
footer{visibility:hidden;}

.stApp{
    background: radial-gradient(circle at 20% 0%, #16213E 0%, #0D1321 60%, #060911 100%);
}

.hero{
    text-align:center;
    padding:50px 20px 30px 20px;
}

.hero-badge{
    display:inline-block;
    background:rgba(90,169,255,0.12);
    border:1px solid rgba(90,169,255,0.4);
    color:#7FC4FF;
    padding:6px 18px;
    border-radius:999px;
    font-size:13px;
    font-weight:700;
    letter-spacing:1px;
    text-transform:uppercase;
    margin-bottom:20px;
}

.hero h1{
    font-size:52px;
    font-weight:800;
    background:linear-gradient(90deg,#FFFFFF,#8FD3FF);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
    margin:0 0 14px 0;
    letter-spacing:-1px;
}

.hero p{
    color:#A9B4C4 !important;
    font-size:19px;
    max-width:640px;
    margin:0 auto;
}

.glass-panel{
    background:rgba(255,255,255,0.04);
    border:1px solid rgba(255,255,255,0.08);
    backdrop-filter:blur(8px);
    border-radius:22px;
    padding:32px 36px;
    margin:36px 0;
    display:flex;
    align-items:center;
    gap:26px;
}
.glass-panel .icon{
    font-size:52px;
}
.glass-panel h2{
    color:#FFFFFF !important;
    font-size:22px;
    margin:0 0 8px 0;
}
.glass-panel p{
    color:#B7C0CD !important;
    font-size:15.5px;
    line-height:1.6;
    margin:0;
    text-align:left !important;
}
.glass-panel b{
    color:#7FC4FF;
}

.section-label{
    text-align:center;
    color:#7C8798;
    font-size:13px;
    font-weight:700;
    text-transform:uppercase;
    letter-spacing:2px;
    margin:34px 0 20px 0;
}

.feature-card{
    background:linear-gradient(145deg, rgba(255,255,255,0.06), rgba(255,255,255,0.02));
    border:1px solid rgba(255,255,255,0.09);
    border-radius:20px;
    padding:34px 18px;
    text-align:center;
    height:230px;
    display:flex;
    flex-direction:column;
    justify-content:center;
    align-items:center;
    transition:0.25s;
}
.feature-card:hover{
    transform:translateY(-6px);
    border-color:#4EA8FF;
    box-shadow:0 16px 32px rgba(78,168,255,0.18);
}
.feature-icon{
    font-size:48px;
    margin-bottom:10px;
}
.feature-title{
    font-size:19px;
    font-weight:800;
    color:#FFFFFF;
}
.feature-text{
    color:#8B96A6;
    font-size:14px;
    margin-top:6px;
}

.footer-note{
    text-align:center;
    color:#5C6577;
    font-size:12.5px;
    margin-top:40px;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------
# Hero
# ---------------------------------

st.markdown("""
<div class="hero">
    <div class="hero-badge">🧠 Hybrid Deep Learning &nbsp;•&nbsp; Explainable AI</div>
    <h1>🦶 Diabetic Foot Ulcer Detection System</h1>
    <p>AI-powered early detection, Grad-CAM explainability, and instant medical reporting — built to help catch DFUs before they escalate.</p>
</div>
""", unsafe_allow_html=True)

# ---------------------------------
# Welcome (glass panel)
# ---------------------------------

st.markdown("""
""", unsafe_allow_html=True)

# ---------------------------------
# Features — exactly 4 cards
# ---------------------------------

st.markdown('<div class="section-label">What you can do</div>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <style>
    .st-key-detect button{
        width:100%; height:230px; margin-top:-230px;
        opacity:0; border:none; cursor:pointer;
    }
    </style>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">📷</div>
        <div class="feature-title">Detect Ulcer</div>
        <div class="feature-text">Upload a foot image for instant AI analysis.</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("", key="detect", use_container_width=True):
        st.switch_page("pages/detect_ulcer.py")

with col2:
    st.markdown("""
    <style>
    .st-key-assistant button{
        width:100%; height:230px; margin-top:-230px;
        opacity:0; border:none; cursor:pointer;
    }
    </style>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🤖</div>
        <div class="feature-title">AI Assistant</div>
        <div class="feature-text">Ask questions about diabetic foot ulcers.</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("", key="assistant", use_container_width=True):
        st.switch_page("pages/ai_health_assistant.py")

with col3:
    st.markdown("""
    <style>
    .st-key-hospital button{
        width:100%; height:230px; margin-top:-230px;
        opacity:0; border:none; cursor:pointer;
    }
    </style>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🏥</div>
        <div class="feature-title">Hospitals Near You</div>
        <div class="feature-text">Locate nearby diabetic foot care centers.</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("", key="hospital", use_container_width=True):
        st.switch_page("pages/map.py")

with col4:
    st.markdown("""
    <style>
    .st-key-records button{
        width:100%; height:230px; margin-top:-230px;
        opacity:0; border:none; cursor:pointer;
    }
    </style>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🗂️</div>
        <div class="feature-title">Medical Record</div>
        <div class="feature-text">Securely store and access your records.</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("", key="records", use_container_width=True):
        st.switch_page("pages/medical_record.py")

st.markdown("""
<div class="footer-note">
⚠ This system supports, not replaces, professional medical diagnosis.
</div>
""", unsafe_allow_html=True)