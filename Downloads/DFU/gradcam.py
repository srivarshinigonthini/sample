import tensorflow as tf
import numpy as np
import cv2

# Last conv layer of each backbone, confirmed from model.summary():
#   - "top_conv"  -> end of the EfficientNet branch
#   - "conv_7b"   -> end of the Inception-ResNet-V2 branch
CONV_LAYERS = ["top_conv", "conv_7b"]


def build_gradcam_feature_models(model):
    """
    Build the Grad-CAM feature-extraction models ONCE and reuse them for
    every prediction. Building a tf.keras.Model is expensive — doing it
    on every single image (as the earlier version did) is the main
    reason Grad-CAM felt slow. Call this once (wrap it in
    @st.cache_resource in the Streamlit page) and pass the result into
    generate_gradcam_overlay() every time.

    Returns:
        dict: { layer_name: tf.keras.Model(inputs=model.input,
                                             outputs=[conv_layer.output, model.output]) }
    """
    feature_models = {}

    for layer_name in CONV_LAYERS:
        try:
            layer = model.get_layer(layer_name)
        except ValueError:
            continue

        feature_models[layer_name] = tf.keras.Model(
            inputs=model.input,
            outputs=[layer.output, model.output]
        )

    return feature_models


def generate_gradcam_overlay(feature_models, img_bgr, class_index, target_size=(224, 224)):
    """
    Generate a TRUE gradient-weighted Grad-CAM overlay (not a simple
    channel average). Each conv channel is weighted by how much it
    actually influenced the predicted class score, which is what makes
    the heatmap point at the region the model used to make its decision
    instead of just lighting up generic activated areas.

    Args:
        feature_models: dict returned by build_gradcam_feature_models(model).
        img_bgr: original image as a BGR numpy array (e.g. from cv2.imread
                  or cv2.imdecode), NOT yet resized/normalized.
        class_index: the predicted class index (e.g. 0 = Healthy, 1 = Ulcer)
                      to compute gradients with respect to.
        target_size: size the model expects, default (224, 224).

    Returns:
        overlay_rgb: heatmap-over-original overlay, RGB numpy array, ready
                      for st.image().
        heatmap_rgb: the raw combined colored heatmap alone, RGB numpy array.
    """

    if not feature_models:
        raise ValueError(
            "No Grad-CAM feature models available. "
            "Check that 'top_conv' / 'conv_7b' still match model.summary()."
        )

    # -----------------------------
    # Preprocess
    # -----------------------------
    img_resized = cv2.resize(img_bgr, target_size)
    img_rgb = cv2.cvtColor(img_resized, cv2.COLOR_BGR2RGB)
    # Model applies its own per-backbone preprocessing internally now,
    # so feed raw 0-255 pixel values, not /255.
    input_img = np.expand_dims(img_rgb, axis=0).astype("float32")
    input_tensor = tf.convert_to_tensor(input_img)

    heatmaps = []

    for layer_name, feature_model in feature_models.items():

        with tf.GradientTape() as tape:
            conv_output, predictions = feature_model(input_tensor, training=False)
            class_score = predictions[:, class_index]

        # Gradient of the predicted class score w.r.t. the conv layer's output
        grads = tape.gradient(class_score, conv_output)

        if grads is None:
            # This backbone's conv layer doesn't influence the output
            # (shouldn't normally happen, but skip safely if it does)
            continue

        # Average gradient per channel = importance weight for that channel
        pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))

        conv_output = conv_output[0]  # drop batch dim
        heatmap = conv_output @ pooled_grads[..., tf.newaxis]
        heatmap = tf.squeeze(heatmap)

        # ReLU — only keep features that positively influenced the class
        heatmap = tf.maximum(heatmap, 0)

        heatmap = heatmap.numpy()
        if np.max(heatmap) != 0:
            heatmap = heatmap / np.max(heatmap)

        heatmap = cv2.resize(heatmap, target_size)
        heatmaps.append(heatmap)

    if not heatmaps:
        raise ValueError("Could not compute Grad-CAM for any backbone layer.")

    # -----------------------------
    # Combine both backbone heatmaps (simple average)
    # -----------------------------
    combined = np.mean(heatmaps, axis=0)

    if np.max(combined) != 0:
        combined = combined / np.max(combined)

    heatmap_uint8 = np.uint8(255 * combined)
    heatmap_color = cv2.applyColorMap(heatmap_uint8, cv2.COLORMAP_JET)

    # -----------------------------
    # Overlay on the resized original image
    # -----------------------------
    overlay = cv2.addWeighted(img_resized, 0.6, heatmap_color, 0.4, 0)

    overlay_rgb = cv2.cvtColor(overlay, cv2.COLOR_BGR2RGB)
    heatmap_rgb = cv2.cvtColor(heatmap_color, cv2.COLOR_BGR2RGB)

    return overlay_rgb, heatmap_rgb