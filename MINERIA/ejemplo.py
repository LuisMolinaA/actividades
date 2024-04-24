import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression

# Datos de ejemplo
X = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20])
Y = np.array([[1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0],
              [0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1],
              [1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1]
              ])

# Asegurar que las dimensiones de los datos sean correctas
X = X.reshape(-1, 1)

# Inicialización y entrenamiento del modelo de regresión logística
model = LogisticRegression()
model.fit(X, np.argmax(Y, axis=0))

# Generar valores de predicción para la gráfica
x_min, x_max = X.min() - 1, X.max() + 1
xx = np.arange(x_min, x_max, 0.01).reshape(-1, 1)
Z = model.predict_proba(xx)

# Graficar la curva de decisión
plt.plot(xx, Z[:, 1], color='blue', linewidth=2)

# Graficar los puntos de datos
for i in range(Y.shape[0]):
    plt.scatter(X, Y[i], cmap='bwr', label='Condimento {}'.format(i+1))

# Etiquetas y título del gráfico
plt.xlabel('Característica')
plt.ylabel('Etiqueta')
plt.title('Gráfico de Regresión Logística')

# Mostrar la leyenda
plt.legend()

# Mostrar la gráfica
plt.show()
