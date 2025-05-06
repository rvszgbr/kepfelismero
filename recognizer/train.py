import os
import sys

from tensorflow.keras import Input
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

# Elérési utak
base_dir = r"C:\Users\rivas\kepfelismero\data\images"
train_dir = os.path.join(base_dir, "Training")
test_dir = os.path.join(base_dir, "Test")

# Modell paraméterek
img_height = 100
img_width = 100
batch_size = 32
epochs = 30  # Tanítási körök száma

# Adat augmentáció a tanításhoz
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    zoom_range=0.2,
    width_shift_range=0.2,
    height_shift_range=0.2,
    horizontal_flip=True
)

# Teszt adatok normalizálása
test_datagen = ImageDataGenerator(rescale=1./255)

# Adatok betöltése
train_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=(img_height, img_width),
    batch_size=batch_size,
    class_mode='categorical',
    shuffle=True
)

test_generator = test_datagen.flow_from_directory(
    test_dir,
    target_size=(img_height, img_width),
    batch_size=batch_size,
    class_mode='categorical',
    shuffle=False
)

# Osztály információk kiírása
print(f" {train_generator.num_classes} osztály betöltve.")
print(f" Osztályok: {train_generator.class_indices}")

# Modell felépítése
model = Sequential([
    Input(shape=(img_height, img_width, 3)),

    Conv2D(32, (3, 3), activation='relu'),
    MaxPooling2D(pool_size=(2, 2)),

    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D(pool_size=(2, 2)),

    Conv2D(128, (3, 3), activation='relu'),
    MaxPooling2D(pool_size=(2, 2)),

    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.5),
    Dense(train_generator.num_classes, activation='softmax')
])

# Modell fordítása
model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# Callbackek – korai megállítás és modell mentés
callbacks = [
    EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True),
    ModelCheckpoint('model_best.keras', monitor='val_accuracy', save_best_only=True)
]

# Modell tanítása
history = model.fit(
    train_generator,
    epochs=epochs,
    validation_data=test_generator,
    callbacks=callbacks,
)

# Modell mentése
model.save("model_final.keras")
print("Tanítás kész. Modell elmentve: model_final.keras")
