import tensorflow as tf
from tensorflow.keras import layers, Model
from tensorflow.keras.applications.efficientnet import preprocess_input as effnet_preprocess
from tensorflow.keras.applications.inception_resnet_v2 import preprocess_input as inception_preprocess

# ==========================
# Dataset Path
# ==========================
# NOTE: update this to the actual path of the dataset on whichever
# machine runs this script.
dataset_path = r"Dataset"

img_size = (224, 224)
batch_size = 16

# ==========================
# Load Dataset (RAW pixel values 0-255, no manual rescaling here)
# ==========================
train_ds = tf.keras.utils.image_dataset_from_directory(
    dataset_path,
    validation_split=0.2,
    subset="training",
    seed=123,
    image_size=img_size,
    batch_size=batch_size
)

val_ds = tf.keras.utils.image_dataset_from_directory(
    dataset_path,
    validation_split=0.2,
    subset="validation",
    seed=123,
    image_size=img_size,
    batch_size=batch_size
)

class_names = train_ds.class_names
print("Classes:", class_names)

# IMPORTANT: no Rescaling(1./255) here anymore. Each backbone gets its
# own correct preprocessing applied INSIDE the model graph below, so the
# dataset should stay in raw 0-255 float form.

AUTOTUNE = tf.data.AUTOTUNE
train_ds = train_ds.prefetch(AUTOTUNE)
val_ds = val_ds.prefetch(AUTOTUNE)

# ==========================
# Input Layer
# ==========================
input_layer = layers.Input(shape=(224, 224, 3))

# ==========================
# EfficientNet Branch
# EfficientNetB0 has its own internal normalization and expects raw
# 0-255 pixel values directly, so effnet_preprocess_input is effectively
# a no-op here but is kept for clarity / future-proofing.
# ==========================
effnet_input = layers.Lambda(effnet_preprocess, name="effnet_preprocess")(input_layer)

effnet = tf.keras.applications.EfficientNetB0(
    include_top=False,
    weights="imagenet",
    input_tensor=effnet_input
)
effnet.trainable = False

x1 = layers.GlobalAveragePooling2D()(effnet.output)

# ==========================
# InceptionResNetV2 Branch
# InceptionResNetV2 expects pixel values scaled to [-1, 1], which is
# what inception_preprocess_input does. This is the branch that was
# getting the WRONG input range before (0-1 instead of -1 to 1).
# ==========================
inception_input = layers.Lambda(inception_preprocess, name="inception_preprocess")(input_layer)

inception = tf.keras.applications.InceptionResNetV2(
    include_top=False,
    weights="imagenet",
    input_tensor=inception_input
)
inception.trainable = False

x2 = layers.GlobalAveragePooling2D()(inception.output)

# ==========================
# Fusion Layer
# ==========================
combined = layers.concatenate([x1, x2])

x = layers.Dense(256, activation="relu")(combined)
x = layers.Dropout(0.3)(x)
x = layers.Dense(128, activation="relu")(x)
x = layers.Dropout(0.3)(x)

output = layers.Dense(2, activation="softmax")(x)

# ==========================
# Model
# ==========================
model = Model(inputs=input_layer, outputs=output)

model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.0001),
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

model.summary()

# ==========================
# Train Model
# ==========================
history = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=10
)

# ==========================
# Save Model
# ==========================
model.save("dfu_hybrid_model.keras")

print("✅ Hybrid Model Training Completed & Saved!")