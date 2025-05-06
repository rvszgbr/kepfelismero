from recognizer.predict import predict_image
from data.nutrition_lookup import get_nutritional_info
from PyQt5.QtWidgets import QFileDialog, QMessageBox


def recognize_image(self):
    if not self.image_path:
        QMessageBox.warning(self, "Figyelmeztetés", "Először válassz ki egy képet.")
        return

    predicted_class, confidence = predict_image(self.image_path)

    self.label_result.setText(
        f"Eredmény: {predicted_class} ({confidence:.2f}%)"
    )

    # 🔎 Lekérdezzük a tápértéket
    nutrition = get_nutritional_info(predicted_class)
    if nutrition:
        nutrition_text = "\n".join(
            f"{key}: {value}" for key, value in nutrition.items()
        )
        self.label_nutrition.setText("Tápérték 100g-ra:\n" + nutrition_text)
    else:
        self.label_nutrition.setText("Tápérték nem elérhető.")

