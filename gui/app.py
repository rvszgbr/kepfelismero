import tkinter as tk
from tkinter import filedialog, Label
from PIL import Image, ImageTk
import numpy as np
import os

from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

# Modell betöltése
model = load_model(r"C:\Users\rivas\kepfelismero\recognizer\model_final.keras")


class_names = sorted(os.listdir(r"C:\Users\rivas\kepfelismero\data\images\Training"))

# GUI inicializálás
root = tk.Tk()
root.title("Képfelismerő")
root.geometry("500x500")

# Kép megjelenítő label
image_label = Label(root)
image_label.pack(pady=20)

# Eredmény label
result_label = Label(root, text="", font=("Arial", 16))
result_label.pack(pady=10)

def predict_image(img_path):
    # Kép betöltése és előkészítése
    img = image.load_img(img_path, target_size=(100, 100))
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    # Előrejelzés
    predictions = model.predict(img_array)
    predicted_class_index = np.argmax(predictions[0])
    predicted_class_name = class_names[predicted_class_index]
    confidence = predictions[0][predicted_class_index]

    return predicted_class_name, confidence

def upload_and_predict():
    file_path = filedialog.askopenfilename()
    if not file_path:
        return

    # Kép betöltése a GUI-hoz
    img = Image.open(file_path)
    img = img.resize((300, 300))
    img_tk = ImageTk.PhotoImage(img)
    image_label.configure(image=img_tk)
    image_label.image = img_tk

    # Predikció
    predicted_class, confidence = predict_image(file_path)
    result_label.config(text=f"Felismerés: {predicted_class} ({confidence * 100:.2f}%)")

# Feltöltés gomb
upload_button = tk.Button(root, text="Kép kiválasztása", command=upload_and_predict)
upload_button.pack(pady=10)

# GUI futtatása
root.mainloop()
