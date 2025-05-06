import os
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tkinter import Tk, filedialog

# 📥 Modell betöltése
model = load_model("model_final.keras")

# 📁 Kategóriák (ezeket te adtad meg a mappanevekkel)
class_names = ['Apple', 'Banana', 'Cherry', 'Limes', 'Orange', 'Peach']

# 📂 Kép kiválasztása felugró ablakból
root = Tk()
root.withdraw()  # Elrejti a főablakot
img_path = filedialog.askopenfilename(
    title="Válassz egy képet",
    filetypes=[("Képek", "*.jpg *.jpeg *.png")]
)

if not img_path:
    print("❌ Nem választottál ki képet.")
    exit()

# 📐 Kép betöltése és előfeldolgozása
img = image.load_img(img_path, target_size=(100, 100))
img_array = image.img_to_array(img)
img_array = np.expand_dims(img_array, axis=0)
img_array /= 255.0  # Normalizálás

# 🤖 Predikció
predictions = model.predict(img_array)
predicted_class = class_names[np.argmax(predictions[0])]
confidence = np.max(predictions[0]) * 100

# 📢 Eredmény kiírása
print(f"🔍 Felismert osztály: {predicted_class} ({confidence:.2f}% biztonsággal)")
