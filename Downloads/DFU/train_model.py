import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import os

# ==========================
# Dataset Path
# ==========================
dataset_path = r"C:\Users\vemul\OneDrive\Desktop\DFU_Project\dataset"

# ==========================
# Image Preprocessing
# ==========================
img_size = (224, 224)
batch_size = 16

datagen = ImageDataGenerator(
    rescale=1./255,
    validation_split=0.2
)

train_data = datagen.flow_from_directory(
    dataset_path,
    target_size=img_size,
    batch_size=batch_size,
    class_mode='categorical',
    subset='training',
    shuffle=True
)

val_data = datagen.flow_from_directory(
    dataset_path,
    target_size=img_size,
    batch_size=batch_size,
    class_mode='categorical',
    subset='validation',
    shuffle=True
)

# ==========================
# Model (Transfer Learning - MobileNetV2)
# ==========================
base_model = tf.keras.applications.MobileNetV2(
    input_shape=(224, 224, 3),
    include_top=False,
    weights='imagenet'
)

base_model.trainable = False  # freeze base model

model = models.Sequential([
    base_model,
    layers.GlobalAveragePooling2D(),
    layers.Dense(128, activation='relu'),
    layers.Dropout(0.3),
    layers.Dense(2, activation='softmax')  # ✅ 2 classes
])

# ==========================
# Compile Model
# ==========================
model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# ==========================
# Train Model
# ==========================
epochs = 10

history = model.fit(
    train_data,
    validation_data=val_data,
    epochs=epochs
)

# ==========================
# Save Model
# ==========================
model.save("dfu_2class_model.keras")

print("Model training completed and saved successfully!")