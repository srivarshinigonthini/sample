import streamlit as st

st.set_page_config(page_title="About DFU", page_icon="📖", layout="wide")

st.title("📖 About Diabetic Foot Ulcer")

st.markdown("---")

# -----------------------------
# What is DFU?
# -----------------------------
st.header("🦶 What is a Diabetic Foot Ulcer?")

st.write("""
A **Diabetic Foot Ulcer (DFU)** is an open wound or sore that develops
on the feet of people with diabetes. It usually occurs due to poor blood
circulation, nerve damage (neuropathy), and prolonged high blood sugar levels.

If not treated early, a diabetic foot ulcer can become infected and may
lead to severe complications, including amputation.
""")

st.markdown("---")

# -----------------------------
# Symptoms
# -----------------------------
st.header("⚠ Symptoms")

col1, col2 = st.columns(2)

with col1:
    st.success("✔ Swelling")
    st.success("✔ Redness")
    st.success("✔ Open wound")
    st.success("✔ Bad odor")

with col2:
    st.success("✔ Drainage")
    st.success("✔ Pain or numbness")
    st.success("✔ Skin discoloration")
    st.success("✔ Slow healing")

st.markdown("---")

# -----------------------------
# Causes
# -----------------------------
st.header("🩺 Causes")

st.write("""
• Poor blood circulation

• Peripheral neuropathy

• High blood sugar

• Foot injuries

• Infection

• Improper footwear

• Delayed treatment
""")

st.markdown("---")

# -----------------------------
# Risk Factors
# -----------------------------
st.header("📈 Risk Factors")

st.write("""
People are at higher risk if they have:

- Diabetes for many years
- Smoking habit
- High blood pressure
- Poor foot hygiene
- Kidney disease
- Previous foot ulcers
""")

st.markdown("---")

# -----------------------------
# Prevention
# -----------------------------
st.header("🛡 Prevention")

st.info("""
✔ Check feet daily

✔ Maintain blood sugar levels

✔ Wear comfortable footwear

✔ Keep feet clean and dry

✔ Visit a doctor regularly

✔ Avoid walking barefoot
""")

st.markdown("---")

# -----------------------------
# About the AI Project
# -----------------------------
st.header("🤖 About This Project")

st.write("""
This project uses a **Hybrid Deep Learning Model**
(EfficientNet + Inception-ResNet-V2)
to detect diabetic foot ulcers from medical images.

### Main Features

- Healthy vs Ulcer Detection
- Severity Estimation
- Confidence Score
- Medical Recommendations
- PDF Report Generation
- Explainable AI (Grad-CAM)
""")

st.markdown("---")

st.success("Early detection of diabetic foot ulcers can significantly reduce complications and improve patient care.")