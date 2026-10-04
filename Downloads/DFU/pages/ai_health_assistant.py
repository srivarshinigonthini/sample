import time
import streamlit as st
from google import genai
from google.genai import types

# =====================================
# Page Configuration
# =====================================

st.set_page_config(
    page_title="AI Health Assistant",
    page_icon="🤖",
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

.block-container{
    max-width:900px;
    margin:auto;
    padding-top:3rem;
}

h1{
    text-align:center;
    background:linear-gradient(90deg,#FFFFFF,#8FD3FF);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
    font-size:36px;
    font-weight:800;
}

.intro-text{
    text-align:center;
    color:#A9B4C4 !important;
    font-size:16px;
    margin-bottom:24px;
}

[data-testid="stChatMessage"]{
    background:rgba(255,255,255,0.04);
    border:1px solid rgba(255,255,255,0.08);
    border-radius:16px;
}

.stChatInputContainer, [data-testid="stChatInput"]{
    border-radius:14px;
}

section[data-testid="stSidebar"]{
    background:#0D1321;
}

</style>
""", unsafe_allow_html=True)

# =====================================
# Title
# =====================================

st.markdown("<h1>🤖 AI Health Assistant</h1>", unsafe_allow_html=True)
st.markdown(
    '<p class="intro-text">Ask anything about diabetic foot ulcers — symptoms, '
    'prevention, wound care, treatment, or general diabetes-related foot health.</p>',
    unsafe_allow_html=True
)

# =====================================
# API Client Setup
# =====================================
# API key is read from Streamlit secrets (.streamlit/secrets.toml):
#
#   GEMINI_API_KEY = "your-key-here"
#
# Never hardcode the key directly in this file.

try:
    api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    api_key = None

if not api_key:
    st.error(
        "⚠ No API key found. Add GEMINI_API_KEY to "
        ".streamlit/secrets.toml to enable the AI Health Assistant."
    )
    st.stop()

client = genai.Client(api_key=api_key)

# =====================================
# System Prompt — scopes the assistant to DFU-related topics
# and keeps it medically responsible
# =====================================

SYSTEM_PROMPT = """You are a health information assistant inside a Diabetic Foot Ulcer (DFU) \
detection application. You answer questions specifically about diabetic foot ulcers, \
diabetic foot care, wound healing, infection warning signs, and related diabetes \
management topics that affect foot health.

Guidelines:
- Give clear, accurate, and genuinely helpful general health information.
- Always encourage the user to consult a qualified healthcare professional for \
diagnosis, treatment decisions, medication, or anything urgent — you are not a \
substitute for medical care.
- If a question is completely unrelated to diabetic foot ulcers, diabetes, or general \
foot/wound health, politely redirect the user back to those topics.
- Keep answers concise and easy to read (a few short paragraphs or a short list), \
not overly long or clinical.
- Never provide specific drug dosages or prescribe treatment — describe general \
approaches only and point to a doctor for specifics.
"""

# Models are tried in order; if the first is busy/unavailable, the next is used.
# If a name gives a "not found" error, check aistudio.google.com for current flash models.
MODELS = ["gemini-3.8-flash", "gemini-3.7-flash", "gemini-3.5-flash-lite"]

# =====================================
# Chat State
# =====================================

if "messages" not in st.session_state:
    st.session_state.messages = []

# Render existing chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# =====================================
# Chat Input
# =====================================

user_input = st.chat_input("Ask about diabetic foot ulcers...")

if user_input:

    # Show user message immediately
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Convert chat history to Gemini format (Gemini uses "model" instead of "assistant")
    history = [
        types.Content(
            role="user" if m["role"] == "user" else "model",
            parts=[types.Part(text=m["content"])],
        )
        for m in st.session_state.messages
    ]

    # Get AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            answer = None
            last_error = None

            for model_name in MODELS:
                for attempt in range(4):
                    try:
                        response = client.models.generate_content(
                            model=model_name,
                            contents=history,
                            config=types.GenerateContentConfig(
                                system_instruction=SYSTEM_PROMPT,
                                max_output_tokens=2048,
                            ),
                        )
                        answer = response.text
                        break
                    except Exception as e:
                        last_error = e
                        if "503" in str(e) or "UNAVAILABLE" in str(e):
                            time.sleep(2 * (attempt + 1))  # wait 2s, 4s, 6s, 8s
                            continue
                        break  # other errors: don't retry this model
                if answer:
                    break

            if not answer:
                answer = (
                    "⚠ The AI service is very busy right now. "
                    "Please try again in a minute. "
                    f"({last_error})"
                )

            st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})

st.markdown("---")
st.info(
    "⚠ This AI Health Assistant provides educational information only and should not replace professional medical advice."
)