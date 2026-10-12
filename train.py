"""Train a crop disease classifier (MobileNetV2 transfer learning).
Run:  python train.py
"""
import os
import json
from pathlib import Path
import tensorflow as tf
from tensorflow.keras import layers, models

# ---- CONFIG -----------------------------------------------------------
DATA_DIR = r"C:\Users\RATHVA SUNIL\Downloads\MILESTONE02\archive (5)"
IMG_SIZE = (224, 224)
BATCH = 32
EPOCHS_HEAD = 5     # train only the new top layers
EPOCHS_FINE = 5     # then fine-tune the backbone
SEED = 42
# -----------------------------------------------------------------------

IMG_EXT = {".jpg", ".jpeg", ".png", ".bmp"}


def has_images(d):
    return any(f.suffix.lower() in IMG_EXT for f in Path(d).iterdir() if f.is_file())


def find_class_root(root):
    """Walk down until we reach a folder whose sub-folders are the classes."""
    for dirpath, dirnames, _ in os.walk(root):
        subs = [Path(dirpath) / d for d in sorted(dirnames)]
        if len(subs) >= 2 and all(has_images(s) for s in subs):
            return Path(dirpath)
    raise SystemExit("No class folders with images found under: " + root)


def find_val_sibling(train_root):
    for name in ("valid", "val", "validation", "test"):
        cand = train_root.parent / name
        if cand.is_dir():
            try:
                return find_class_root(cand)
            except SystemExit:
                pass
    return None


train_root = find_class_root(DATA_DIR)
val_root = find_val_sibling(train_root) if train_root.name.lower() in ("train", "training") else None
print("Train folder:", train_root)
print("Validation folder:", val_root or "(auto 80/20 split)")

common = dict(image_size=IMG_SIZE, batch_size=BATCH, seed=SEED, label_mode="categorical")
if val_root:
    train_ds = tf.keras.utils.image_dataset_from_directory(train_root, **common)
    val_ds = tf.keras.utils.image_dataset_from_directory(val_root, shuffle=False, **common)
else:
    train_ds = tf.keras.utils.image_dataset_from_directory(
        train_root, validation_split=0.2, subset="training", **common)
    val_ds = tf.keras.utils.image_dataset_from_directory(
        train_root, validation_split=0.2, subset="validation", **common)

class_names = train_ds.class_names
print(f"{len(class_names)} classes:", class_names)
with open("class_names.json", "w") as f:
    json.dump(class_names, f, indent=2)

AUTOTUNE = tf.data.AUTOTUNE
train_ds = train_ds.prefetch(AUTOTUNE)
val_ds = val_ds.prefetch(AUTOTUNE)

augment = tf.keras.Sequential([
    layers.RandomFlip("horizontal_and_vertical"),
    layers.RandomRotation(0.15),
    layers.RandomZoom(0.15),
    layers.RandomContrast(0.15),
])

base = tf.keras.applications.MobileNetV2(
    input_shape=IMG_SIZE + (3,), include_top=False, weights="imagenet")
base.trainable = False

inputs = layers.Input(shape=IMG_SIZE + (3,))
x = augment(inputs)
x = tf.keras.applications.mobilenet_v2.preprocess_input(x)
x = base(x, training=False)
x = layers.GlobalAveragePooling2D()(x)
x = layers.Dropout(0.3)(x)
outputs = layers.Dense(len(class_names), activation="softmax")(x)
model = models.Model(inputs, outputs)

callbacks = [
    tf.keras.callbacks.ModelCheckpoint("crop_disease_model.keras",
                                       save_best_only=True, monitor="val_accuracy"),
    tf.keras.callbacks.EarlyStopping(patience=3, restore_best_weights=True,
                                     monitor="val_accuracy"),
]

# Stage 1: train the head
model.compile(optimizer=tf.keras.optimizers.Adam(1e-3),
              loss="categorical_crossentropy", metrics=["accuracy"])
model.fit(train_ds, validation_data=val_ds, epochs=EPOCHS_HEAD, callbacks=callbacks)

# Stage 2: fine-tune top of the backbone
base.trainable = True
for layer in base.layers[:-30]:
    layer.trainable = False
model.compile(optimizer=tf.keras.optimizers.Adam(1e-5),
              loss="categorical_crossentropy", metrics=["accuracy"])
model.fit(train_ds, validation_data=val_ds, epochs=EPOCHS_FINE, callbacks=callbacks)

loss, acc = model.evaluate(val_ds)
print(f"Final validation accuracy: {acc:.2%}")
model.save("crop_disease_model.keras")
print("Saved crop_disease_model.keras and class_names.json")
