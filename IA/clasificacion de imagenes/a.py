from keras.models import load_model
import cv2
import numpy as np

model = load_model("./clasificacion de imagenes/modelo.h5")
imagen_path = input("ingresar ruta de la imagen: ")
imagen_path = imagen_path.strip('"')

img = cv2.imread(imagen_path, cv2.IMREAD_GRAYSCALE)
img = cv2.resize(img, (64, 64))
img = np.array(img).reshape(-1, 64, 64, 1)

prediccion = model.predict(img)

classes = [
    "Echinopsis peruviana",
    "Embarazada",
    "Graptosedum Gosthy",
    "Haworthia cymbiformis",
    "Haworthiopsis fasciata",
    "Kalanchoe fedtschenkoi",
    "Mammillaria elongata",
    "Mammillaria polythele",
    "Opuntia monacantha",
    "Stapelia gigantea",
]
prediccion_clase = classes[np.argmax(prediccion)]
print(f"la clase predicha es: {prediccion_clase}")
