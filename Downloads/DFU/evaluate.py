import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# =========================
# LOAD MODEL
# =========================
model = tf.keras.models.load_model("models/dfu_2class_model.keras")

# =========================
# DATASET PATH
# =========================
dataset_path = "dataset"

# =========================
# PREPROCESSING
# =========================
datagen = ImageDataGenerator(
    rescale=1./255,
    validation_split=0.2
)

# =========================
# VALIDATION DATA
# =========================
val_data = datagen.flow_from_directory(
    dataset_path,
    target_size=(224, 224),
    batch_size=32,
    class_mode='categorical',
    subset='validation',
    shuffle=False,
    seed=42
)

# =========================
# CLASS LABELS
# =========================
classes = list(val_data.class_indices.keys())
print("\nClass Mapping:", val_data.class_indices)

# =========================
# PREDICTIONS
# =========================
y_pred = model.predict(val_data)
y_pred_classes = np.argmax(y_pred, axis=1)
y_true = val_data.classes

# =========================
# ACCURACY
# =========================
accuracy = accuracy_score(y_true, y_pred_classes)
print(f"\n✅ Accuracy: {accuracy * 100:.2f}%")

# =========================
# CLASSIFICATION REPORT
# =========================
print("\n🔥 Classification Report:\n")
print(classification_report(y_true, y_pred_classes, target_names=classes))

# =========================
# CONFUSION MATRIX
# =========================
cm = confusion_matrix(y_true, y_pred_classes)

print("\n🔥 Confusion Matrix:\n")
print(cm)

# =========================
# VISUALIZATION
# =========================
plt.figure(figsize=(6, 5))

sns.heatmap(cm,
            annot=True,
            fmt='d',
            cmap='Blues',
            xticklabels=classes,
            yticklabels=classes)

plt.xlabel("Predicted Label")
plt.ylabel("True Label")
plt.title("DFU Confusion Matrix")

plt.show()