import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.datasets import mnist
import matplotlib.pyplot as plt

# Cargar y preprocesar el conjunto de datos MNIST
(train_images, train_labels), (test_images, test_labels) = mnist.load_data()
train_images, test_images = train_images / 255.0, test_images / 255.0

# Construir el modelo
model = models.Sequential([
    layers.Flatten(input_shape=(28, 28)),     # Aplanar la imagen de 28x28 a un vector de 784 elementos
    layers.Dense(128, activation='relu'),      # Capa completamente conectada con 128 neuronas y función de activación ReLU
    layers.Dropout(0.2),                       # Dropout para evitar sobreajuste
    layers.Dense(10, activation='softmax')     # Capa de salida con 10 neuronas para las 10 clases y función de activación softmax
])

# Compilar el modelo
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# Entrenar el modelo
model.fit(train_images, train_labels, epochs=5)

# Evaluar el modelo en el conjunto de prueba
test_loss, test_acc = model.evaluate(test_images, test_labels)
print(f'\nPrecisión en el conjunto de prueba: {test_acc}')

# Hacer predicciones en algunas imágenes de prueba
predictions = model.predict(test_images[:5])

# Mostrar las imágenes de prueba y las predicciones
for i in range(5):
    plt.imshow(test_images[i], cmap='gray')
    plt.title(f'Etiqueta verdadera: {test_labels[i]}, Predicción: {tf.argmax(predictions[i])}')
    plt.show()
