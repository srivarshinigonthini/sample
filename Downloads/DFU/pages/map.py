import streamlit as st

# -------------------------------------------------------
# PAGE CONFIGURATION
# -------------------------------------------------------
st.set_page_config(
    page_title="Nearby Hospital Finder",
    page_icon="🏥",
    layout="wide"
)

# -------------------------------------------------------
# CUSTOM CSS (matches rest of app — dark theme)
# -------------------------------------------------------
st.markdown("""
<style>

#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

.stApp{
    background: radial-gradient(circle at 20% 0%, #16213E 0%, #0D1321 60%, #060911 100%);
}

.block-container{
    padding-top:3rem;
    max-width:850px;
    margin:auto;
}

h1{
    text-align:center;
    background:linear-gradient(90deg,#FFFFFF,#8FD3FF);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
    font-size:38px;
    font-weight:800;
}

/* Section card (replaces old white header-card) */
.section-card{
    background:rgba(255,255,255,0.04);
    border:1px solid rgba(255,255,255,0.08);
    backdrop-filter:blur(8px);
    border-radius:20px;
    padding:30px 32px;
    text-align:center;
    margin-bottom:22px;
}

.section-card p{
    color:#A9B4C4 !important;
    font-size:16px;
    margin:0;
}

.section-card b{
    color:#7FC4FF;
}

h3{
    color:#FFFFFF !important;
    text-align:center;
}

/* Input Box */
.stTextInput input{
    border-radius:12px;
    border:1px solid rgba(255,255,255,0.15);
    background:rgba(255,255,255,0.03);
    color:#FFFFFF;
    padding:12px;
    font-size:16px;
}

/* Buttons */
.stButton>button{
    background:linear-gradient(135deg,#223A5E,#2E4F7C);
    color:#E8EEF6;
    border:1px solid rgba(255,255,255,0.08);
    border-radius:12px;
    font-size:16px;
    font-weight:600;
    padding:12px 26px;
    box-shadow:0 2px 8px rgba(0,0,0,0.3);
    transition:0.25s;
}
.stButton>button:hover{
    background:linear-gradient(135deg,#2A4670,#355A8C);
    transform:translateY(-1px);
    box-shadow:0 4px 12px rgba(0,0,0,0.4);
}

/* Result Card */
.result-card{
    background:rgba(34,163,102,0.10);
    border:1px solid rgba(34,163,102,0.4);
    border-radius:16px;
    padding:22px;
    text-align:center;
    margin-bottom:18px;
}

.result-card h2{
    color:#5FE3A0 !important;
    margin-bottom:8px;
}

.result-card p{
    color:#B7C0CD !important;
    font-size:15px;
    margin:0;
}

/* Map frame wrapper */
.map-frame-wrapper{
    border-radius:16px;
    overflow:hidden;
    border:1px solid rgba(255,255,255,0.08);
    margin-bottom:18px;
}

.footer-note{
    text-align:center;
    color:#5C6577;
    font-size:13px;
    margin-top:30px;
}

</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------
# HEADER
# -------------------------------------------------------

st.markdown("<h1>🏥 Nearby Hospital Finder</h1>", unsafe_allow_html=True)

st.markdown("""
<div class="section-card">
<p>Find nearby <b>Diabetic Foot Ulcer</b> treatment hospitals using your PIN Code.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("<h3>📍 Enter Your 6-Digit PIN Code</h3>", unsafe_allow_html=True)

pin = st.text_input(
    "PIN Code",
    placeholder="Example: 520001",
    max_chars=6,
    label_visibility="collapsed"
)

st.write("")

if st.button("🔍 Search Nearby Hospitals", use_container_width=True):

    if len(pin) != 6 or not pin.isdigit():

        st.error("Please enter a valid 6-digit PIN Code.")

    else:

        search_query = f"diabetic foot ulcer hospital near {pin}"
        google_map_link = f"https://www.google.com/maps/search/?api=1&query={search_query.replace(' ', '+')}"
        embed_src = f"https://www.google.com/maps?q={search_query.replace(' ', '+')}&output=embed"

        st.markdown("""
        <div class="result-card">
            <h2>✅ Hospitals Found</h2>
            <p>Showing results near PIN code below. Use the map to explore, or open it in full screen.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="map-frame-wrapper">
            <iframe
                src="{embed_src}"
                width="100%"
                height="420"
                style="border:0;"
                loading="lazy">
            </iframe>
        </div>
        """, unsafe_allow_html=True)

        st.link_button(
            "📍 Open Full Map in Google Maps",
            google_map_link,
            use_container_width=True
        )

st.write("")
st.write("")

st.button(
    "⬅ Back to Dashboard",
    use_container_width=True,
    on_click=lambda: st.switch_page("app.py")
)

st.markdown("""
<div class="footer-note">
🏥 Diabetic Foot Ulcer Detection & Monitoring System
</div>
""", unsafe_allow_html=True)