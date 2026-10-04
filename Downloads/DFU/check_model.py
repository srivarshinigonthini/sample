import os
import sys

print("Script started...")
sys.stdout.flush()

filename = "dfu_hybrid_model.keras"

print(f"Looking for: {filename}")
print(f"Current folder: {os.getcwd()}")
print(f"File exists here: {os.path.exists(filename)}")
sys.stdout.flush()

try:
    import tensorflow as tf
    print("TensorFlow imported successfully.")
    sys.stdout.flush()

    model = tf.keras.models.load_model(filename)
    print("Model loaded successfully!")
    sys.stdout.flush()

    model.summary()

except Exception as e:
    print("ERROR occurred:")
    print(e)

print("Script finished.")