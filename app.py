import json
import numpy as np
import streamlit as st
import tensorflow as tf

from pathlib import Path
from PIL import Image
from disease_tips import get_tips, pretty

# =====================================================
# 1. CONFIGURATION
# =====================================================

BASE_DIR = Path(r"C:\Users\RATHVA SUNIL\Downloads\mili02")

MODEL_PATH = BASE_DIR / "archive (6)"
CLASS_NAMES_PATH = BASE_DIR / "class_names.json"

IMG_SIZE = (224, 224)
LOW_CONFIDENCE_THRESHOLD = 0.60


# =====================================================
# 2. FIND AND LOAD MODEL
# =====================================================

def find_model_path(path):
    """
    Accept a model file or search a directory for
    .keras, .h5, or .hdf5 model files.
    """

    if path.is_file():
        if path.suffix.lower() in (".keras", ".h5", ".hdf5"):
            return path

        raise ValueError(
            f"Unsupported model file extension: {path.suffix}"
        )

    if path.is_dir():
        candidates = []

        for extension in ("*.keras", "*.h5", "*.hdf5"):
            candidates.extend(path.rglob(extension))

        if len(candidates) == 1:
            return candidates[0]

        if len(candidates) > 1:
            raise ValueError(
                "Multiple model files found:\n"
                + "\n".join(str(p) for p in candidates)
                + "\nSet MODEL_PATH to the exact model filename."
            )

        if (path / "saved_model.pb").is_file():
            raise ValueError(
                "A TensorFlow SavedModel directory was found. "
                "Keras 3 does not load it using load_model(). "
                "Export the model to .keras format or adapt "
                "the inference code for the SavedModel signature."
            )

        raise FileNotFoundError(
            f"No trained .keras or .h5 model found inside:\n{path}\n\n"
            "If this folder contains only plant images, train a "
            "CNN model first."
        )

    raise FileNotFoundError(f"Path does not exist:\n{path}")


@st.cache_resource
def load_model_and_classes():

    actual_model_path = find_model_path(MODEL_PATH)

    if not CLASS_NAMES_PATH.is_file():
        raise FileNotFoundError(
            f"Class names file not found:\n{CLASS_NAMES_PATH}"
        )

    model = tf.keras.models.load_model(str(actual_model_path))

    with open(CLASS_NAMES_PATH, "r", encoding="utf-8") as file:
        class_names = json.load(file)

    if not isinstance(class_names, list):
        raise ValueError(
            "class_names.json must contain a JSON list."
        )

    if model.output_shape[-1] != len(class_names):
        raise ValueError(
            f"Model output classes: {model.output_shape[-1]}\n"
            f"Class names count: {len(class_names)}\n"
            "Ensure class_names.json matches the model's "
            "training class order."
        )

    return model, class_names


# =====================================================
# 3. PREDICT PLANT DISEASE
# =====================================================

def predict(model, class_names, image, top=3):

    image = image.convert("RGB").resize(IMG_SIZE)

    image_array = np.asarray(image, dtype=np.float32)

    # IMPORTANT:
    # This assumes the model was trained on raw RGB values
    # in the range 0-255. Change this if your training code
    # used MobileNetV2 preprocess_input or another method.

    image_array = np.expand_dims(image_array, axis=0)

    predictions = np.asarray(
        model.predict(image_array, verbose=0)[0]
    )

    if not np.all(np.isfinite(predictions)):
        raise ValueError("Model returned invalid predictions.")

    # Convert logits to probabilities if needed.
    if (
        np.any(predictions < 0)
        or not np.isclose(predictions.sum(), 1.0, atol=0.01)
    ):
        predictions = tf.nn.softmax(predictions).numpy()

    top = min(top, len(class_names))
    indices = np.argsort(predictions)[::-1][:top]

    return [
        (class_names[i], float(predictions[i]))
        for i in indices
    ]


# =====================================================
# 4. STREAMLIT APPLICATION
# =====================================================

def main():

    st.set_page_config(
        page_title="Crop Disease Detector",
        page_icon="🌿",
        layout="wide"
    )

    st.title("🌿 Crop Disease Detection")
    st.write(
        "Upload a clear plant leaf photo to predict a possible "
        "disease and view general treatment tips."
    )

    try:
        model, class_names = load_model_and_classes()

    except Exception as error:
        st.error("Unable to load the trained model.")
        st.code(str(error))

        st.info(
            "Check your model path, class_names.json, "
            "and trained model file."
        )
        st.stop()

    uploaded_file = st.file_uploader(
        "Upload a plant leaf image",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_file is None:
        st.info("Upload a leaf image to start.")
        return

    try:
        image = Image.open(uploaded_file).convert("RGB")

        st.image(
            image,
            caption="Uploaded leaf image",
            use_container_width=True
        )

        with st.spinner("Analyzing the plant leaf..."):
            results = predict(
                model,
                class_names,
                image,
                top=3
            )

        best_class, confidence = results[0]

        crop, disease = pretty(best_class)
        info = get_tips(best_class)

        st.divider()

        if "healthy" in best_class.lower():
            st.success(
                f"🌱 {crop}: Healthy ({confidence:.1%})"
            )
        else:
            st.warning(
                f"🦠 {crop}: {disease} ({confidence:.1%})"
            )

        if confidence < LOW_CONFIDENCE_THRESHOLD:
            st.warning(
                "Low confidence. Try a clearer photo in good lighting "
                "or consult an agricultural expert."
            )

        st.subheader("About")
        st.write(
            info.get("cause", "Information unavailable.")
        )

        st.subheader("Solution Tips")

        tips = info.get("tips", [])

        if tips:
            for tip in tips:
                st.markdown(f"- {tip}")
        else:
            st.write("No treatment tips are available.")

        st.subheader("Other Possible Predictions")

        for class_name, probability in results[1:]:
            _, disease_name = pretty(class_name)
            st.write(f"- {disease_name}: {probability:.1%}")

        st.caption(
            "This application provides general guidance, not a "
            "confirmed diagnosis. Consult an agricultural expert "
            "before applying treatments."
        )

    except Exception as error:
        st.error(f"Prediction failed: {error}")


# =====================================================
# 5. RUN APPLICATION
# =====================================================

if __name__ == "__main__":
    main()