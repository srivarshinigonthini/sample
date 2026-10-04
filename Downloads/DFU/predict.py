import tensorflow as tf
import numpy as np
import cv2

# ==========================
# Load Model
# ==========================
model = tf.keras.models.load_model("dfu_2class_model.keras")

classes = ["healthy", "ulcer"]

# ==========================
# Image Input
# ==========================
img_path = input("Enter image path: ")

img = cv2.imread(img_path)

if img is None:
    print("❌ Error: Image not found. Check path.")
    exit()

# Resize image
img = cv2.resize(img, (224, 224))

# Convert BGR → RGB
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# Normalize
img = img / 255.0

# Expand dimensions
img = np.expand_dims(img, axis=0)

# ==========================
# Prediction
# ==========================
pred = model.predict(img)[0]

predicted_class = classes[np.argmax(pred)]
confidence = np.max(pred) * 100

print("\n==========================")
print("Prediction:", predicted_class.upper())
print(f"Confidence: {confidence:.2f}%")
print("==========================")

# ==========================
# Smart Medical Logic
# ==========================
if predicted_class == "ulcer":
    print("\n⚠ Recommendation:")
    print("✔ Consult a doctor immediately")
    print("✔ Clean and dress wound daily")
    print("✔ Monitor blood glucose")
    print("✔ Avoid walking barefoot")

elif predicted_class == "healthy":
    print("\n✅ Status: Healthy foot detected")
    print("✔ Maintain hygiene")
    print("✔ Regular foot inspection advised")