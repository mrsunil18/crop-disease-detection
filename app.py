"""Web app:  streamlit run app.py
CLI:        python app.py path\\to\\leaf.jpg
"""
import sys
import json
import numpy as np
from PIL import Image
import tensorflow as tf
from disease_tips import get_tips, pretty

IMG_SIZE = (224, 224)


def load():
    model = tf.keras.models.load_model("C:\Users\RATHVA SUNIL\Downloads\mili02\archive (6)")
    with open("class_names.json") as f:
        names = json.load(f)
    return model, names


def predict(model, names, img, top=3):
    img = img.convert("RGB").resize(IMG_SIZE)
    arr = np.expand_dims(np.array(img, dtype="float32"), 0)
    probs = model.predict(arr, verbose=0)[0]
    idx = probs.argsort()[::-1][:top]
    return [(names[i], float(probs[i])) for i in idx]


if len(sys.argv) > 1:                       # ---- command-line mode
    model, names = load()
    results = predict(model, names, Image.open(sys.argv[1]))
    best, conf = results[0]
    crop, disease = pretty(best)
    info = get_tips(best)
    print(f"\nCrop: {crop}\nResult: {disease}  ({conf:.1%})")
    print("Cause:", info["cause"])
    print("Tips:")
    for t in info["tips"]:
        print(" -", t)
else:                                       # ---- Streamlit mode
    import streamlit as st

    st.set_page_config(page_title="Crop Disease Detector", page_icon="🌿")
    st.title("🌿 Crop Disease Detection")
    st.write("Upload a clear photo of a single leaf.")

    @st.cache_resource
    def cached():
        return load()

    file = st.file_uploader("Leaf image", type=["jpg", "jpeg", "png"])
    if file:
        img = Image.open(file)
        st.image(img, use_container_width=True)
        model, names = cached()
        results = predict(model, names, img)
        best, conf = results[0]
        crop, disease = pretty(best)
        info = get_tips(best)

        if "healthy" in best.lower():
            st.success(f"{crop}: Healthy ({conf:.1%})")
        else:
            st.error(f"{crop}: {disease} ({conf:.1%})")
        if conf < 0.60:
            st.warning("Low confidence. Retake the photo in good light, close to the leaf.")

        st.subheader("About")
        st.write(info["cause"])
        st.subheader("Solution tips")
        for t in info["tips"]:
            st.markdown(f"- {t}")
        st.caption("Other possibilities: " +
                   ", ".join(f"{pretty(n)[1]} ({p:.0%})" for n, p in results[1:]))
        st.caption("Advice is general. Confirm with a local agriculture expert before spraying.")
