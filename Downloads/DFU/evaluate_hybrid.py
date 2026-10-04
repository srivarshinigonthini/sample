import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay

# ==========================
# Load Model
# ==========================
model = tf.keras.models.load_model("dfu_hybrid_model.keras")

# ==========================
# Dataset
# ==========================
dataset_path = "dataset_balanced"  # relative path

img_size = (224, 224)
batch_size = 16

val_ds = tf.keras.utils.image_dataset_from_directory(
    dataset_path,
    validation_split=0.2,
    subset="validation",
    seed=123,
    image_size=img_size,
    batch_size=batch_size,
    shuffle=False
)

class_names = val_ds.class_names
print("Classes:", class_names)

# NOTE: no manual rescaling here — model applies its own
# EfficientNet / InceptionResNetV2 preprocessing internally on raw [0,255] input

# ==========================
# Predictions
# ==========================
y_true = []
y_pred = []

for images, labels_batch in val_ds:
    preds = model.predict(images, verbose=0)

    preds = np.argmax(preds, axis=1)

    y_true.extend(labels_batch.numpy())
    y_pred.extend(preds)

y_true = np.array(y_true)
y_pred = np.array(y_pred)

# ==========================
# Force both labels always
# ==========================
labels = [0, 1]

# ==========================
# Classification Report
# ==========================
print("\n📊 Classification Report:\n")
print(classification_report(
    y_true,
    y_pred,
    labels=labels,
    target_names=class_names,
    zero_division=0
))

# ==========================
# Confusion Matrix
# ==========================
cm = confusion_matrix(y_true, y_pred, labels=labels)

print("\n📌 Confusion Matrix:\n")
print(cm)

disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=class_names)
disp.plot(cmap="Blues")
plt.title("Hybrid DFU Model - Confusion Matrix")
plt.show()

# ==========================
# Accuracy
# ==========================
accuracy = np.mean(y_true == y_pred)
print("\n🎯 Final Accuracy:", accuracy * 100, "%")