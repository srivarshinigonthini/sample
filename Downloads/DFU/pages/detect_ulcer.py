import streamlit as st
import tensorflow as tf
import numpy as np
import cv2
from report import generate_report
from gradcam import build_gradcam_feature_models, generate_gradcam_overlay

# =====================================
# Page Configuration
# =====================================

st.set_page_config(
    page_title="Detect Ulcer",
    page_icon="🦶",
    layout="wide"
)

# =====================================
# Custom Theme (matches homepage dark theme)
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
    font-size:40px;
    font-weight:800;
}

p{
    color:#A9B4C4;
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
    padding:12px 26px;
    box-shadow:0 2px 8px rgba(0,0,0,0.3);
    transition:0.25s;
}
.stButton>button:hover{
    background:linear-gradient(135deg,#2A4670,#355A8C);
    transform:translateY(-1px);
    box-shadow:0 4px 12px rgba(0,0,0,0.4);
}

.stDownloadButton>button{
    background:linear-gradient(135deg,#22A366,#1B7F4F);
    color:white;
    border-radius:12px;
    font-weight:700;
    border:none;
}

[data-testid="metric-container"]{
    background:rgba(255,255,255,0.04);
    border:1px solid rgba(255,255,255,0.08);
    border-radius:14px;
    padding:14px;
}
[data-testid="stMetricValue"]{
    color:#FFFFFF;
}
[data-testid="stMetricLabel"]{
    color:#8B96A6;
}

.result-badge{
    text-align:center;
    padding:16px;
    border-radius:14px;
    font-size:24px;
    font-weight:800;
    margin-bottom:14px;
}
.result-healthy{
    background:rgba(34,163,102,0.12);
    color:#5FE3A0;
    border:1px solid rgba(34,163,102,0.4);
}
.result-ulcer{
    background:rgba(255,82,82,0.10);
    color:#FF8A8A;
    border:1px solid rgba(255,82,82,0.4);
}

section[data-testid="stSidebar"]{
    background:#0D1321;
}

.block-container{
    padding-top:3rem;
    padding-bottom:2rem;
    max-width:1050px;
    margin:auto;
}

.gradcam-caption{
    text-align:center;
    color:#8B96A6;
    font-size:13px;
    margin-top:6px;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<h1>🦶 AI-Powered Diabetic Foot Ulcer Detection</h1>
<p style='text-align:center;font-size:18px;'>
Upload a diabetic foot image for AI-based ulcer detection with Grad-CAM explainability
</p>
""", unsafe_allow_html=True)

# =====================================
# Patient Information + Upload
# =====================================

st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown("<h3>👤 Patient Information</h3>", unsafe_allow_html=True)
patient_name = st.text_input(
    "Patient Name",
    placeholder="Enter Patient Name",
    label_visibility="collapsed"
)

st.markdown("<h3>📤 Upload Foot Image</h3>", unsafe_allow_html=True)
uploaded_file = st.file_uploader(
    "Upload Foot Image",
    type=["jpg", "jpeg", "png"],
    label_visibility="collapsed"
)
st.markdown('</div>', unsafe_allow_html=True)

# =====================================
# Load Model
# =====================================

MODEL_PATH = "dfu_hybrid_model.keras"


@st.cache_resource
def load_model():
    return tf.keras.models.load_model(MODEL_PATH)


model = load_model()
classes = ["Healthy", "Ulcer"]


@st.cache_resource
def load_gradcam_models(_model):
    # Built once per app session instead of rebuilding on every image,
    # which was the main cause of Grad-CAM feeling slow.
    return build_gradcam_feature_models(_model)


gradcam_feature_models = load_gradcam_models(model)

# =====================================
# Prediction (only runs when a file is uploaded)
# =====================================

if uploaded_file is not None:

    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    # Preprocessing
    img = cv2.resize(image, (224, 224))
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # NOTE: the retrained model applies its own per-backbone preprocessing
    # internally (EfficientNet + Inception-ResNet-V2 each need different
    # scaling), so we feed raw 0-255 pixel values here, not /255.
    img_raw = img_rgb.astype("float32")
    input_img = np.expand_dims(img_raw, axis=0)

    # Prediction
    prediction = model.predict(input_img, verbose=0)[0]
    class_index = np.argmax(prediction)
    confidence = float(np.max(prediction) * 100)
    label = classes[class_index]

    healthy_prob = float(prediction[0] * 100)
    ulcer_prob = float(prediction[1] * 100)

    # Grad-CAM overlay (true gradient-weighted, dual-backbone heatmap)
    try:
        overlay_rgb, heatmap_rgb = generate_gradcam_overlay(
            gradcam_feature_models, image, class_index=int(class_index)
        )
        gradcam_available = True
    except Exception as e:
        gradcam_available = False
        gradcam_error = str(e)

    # -----------------------------
    # Image + Grad-CAM row
    # -----------------------------
    st.markdown('<div class="section-card">', unsafe_allow_html=True)

    if gradcam_available:
        img_col, cam_col = st.columns(2)
        with img_col:
            st.image(cv2.cvtColor(image, cv2.COLOR_BGR2RGB), caption="Uploaded Image", use_container_width=True)
        with cam_col:
            st.image(overlay_rgb, caption="Grad-CAM: What the AI is focusing on", use_container_width=True)
    else:
        st.image(cv2.cvtColor(image, cv2.COLOR_BGR2RGB), caption="Uploaded Image", use_container_width=True)
        st.warning(f"⚠ Grad-CAM could not be generated: {gradcam_error}")

    st.markdown('</div>', unsafe_allow_html=True)

    # -----------------------------
    # Result
    # -----------------------------
    st.markdown('<div class="section-card">', unsafe_allow_html=True)

    if label == "Healthy":
        st.markdown(f'<div class="result-badge result-healthy">✅ {label}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="result-badge result-ulcer">⚠ {label}</div>', unsafe_allow_html=True)

    st.write(f"### Confidence : {confidence:.2f}%")
    st.progress(confidence / 100)

    st.markdown("##### 📊 Probability Breakdown")
    c1, c2 = st.columns(2)
    c1.metric("Healthy", f"{healthy_prob:.2f}%")
    c2.metric("Ulcer", f"{ulcer_prob:.2f}%")

    st.markdown('</div>', unsafe_allow_html=True)

    # =====================================
    # Healthy Case
    # =====================================

    if label == "Healthy":

        severity = "None"
        stage = "Healthy"
        wound_area = 0.0

        recommendations = [
            "Inspect your feet daily.",
            "Maintain normal blood sugar levels.",
            "Wear comfortable footwear.",
            "Keep feet clean and dry."
        ]

        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("🏥 Recommendations")
        for item in recommendations:
            st.success(f"✔ {item}")
        st.markdown('</div>', unsafe_allow_html=True)

    # =====================================
    # Ulcer Case
    # =====================================

    else:

        if confidence >= 95:
            severity = "Severe 🔴"
            stage = "Advanced Stage"
        elif confidence >= 80:
            severity = "Moderate 🟠"
            stage = "Progressive Stage"
        else:
            severity = "Mild 🟡"
            stage = "Early Stage"

        wound_area = round(min(confidence / 5, 25), 1)

        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("🩺 Clinical Assessment")

        col1, col2, col3 = st.columns(3)
        col1.metric("Severity", severity)
        col2.metric("Healing Stage", stage)
        col3.metric("Estimated Wound Area", f"{wound_area}%")

        recommendations = [
            "Clean the wound daily.",
            "Maintain blood glucose levels.",
            "Avoid walking barefoot.",
            "Wear diabetic footwear.",
            "Consult a healthcare professional."
        ]

        st.subheader("🏥 Medical Recommendations")
        for item in recommendations:
            st.success(f"✔ {item}")

        if severity == "Severe 🔴":
            st.warning("⚠ Immediate medical consultation is recommended.")

        st.markdown('</div>', unsafe_allow_html=True)

    st.info(
        "⚠ This AI system is intended to assist healthcare professionals and should not replace clinical diagnosis."
    )

    # =====================================
    # PDF Report Generation (inside upload check - fixed crash)
    # =====================================

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("📄 Download Medical Report")

    if st.button("📄 Generate PDF Report"):

        pdf_path = generate_report(
            patient_name=patient_name if patient_name else "Unknown",
            prediction=label,
            confidence=confidence,
            severity=severity,
            healing_stage=stage,
            wound_area=wound_area,
            recommendations=recommendations
        )

        st.success("✅ PDF Report Generated Successfully!")

        with open(pdf_path, "rb") as pdf_file:
            st.download_button(
                label="⬇ Download Medical Report",
                data=pdf_file,
                file_name="DFU_Report.pdf",
                mime="application/pdf"
            )

    st.markdown('</div>', unsafe_allow_html=True)

else:
    st.markdown(
        '<p style="text-align:center;color:#5C6577;">Upload an image above to run detection and view Grad-CAM insights.</p>',
        unsafe_allow_html=True
    )