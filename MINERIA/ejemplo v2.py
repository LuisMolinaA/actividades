import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# Datos de ejemplo
X = np.array([[2, 4], [1, 3], [4, 2], [3, 5], [5, 1], [6, 4]])
Y = np.array([0, 0, 1, 1, 1, 0])

# Inicialización y entrenamiento del modelo de regresión logística
model = LogisticRegression()
model.fit(X, Y)

# Obtener las predicciones para los datos de entrenamiento
y_pred = model.predict(X)

# Calcular la precisión de las predicciones
accuracy = accuracy_score(Y, y_pred)
print("Precisión de la regresión logística: {:.2f}%".format(accuracy * 100))

# Graficar los resultados y la línea de decisión
plt.scatter(X[:, 0], X[:, 1], c=Y, cmap='bwr')
plt.xlabel('Característica 1')
plt.ylabel('Característica 2')
plt.title('Regresión Logística')

# Obtener los coeficientes e intercepto de la regresión logística
coef = model.coef_
intercept = model.intercept_

# Calcular los valores correspondientes a la línea de decisión
x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
xx = np.arange(x_min, x_max, 0.01)
yy = (-intercept - coef[0, 0] * xx) / coef[0, 1]

# Graficar la línea de decisión
plt.plot(xx, yy, label='Línea de Decisión', color='blue', linewidth=2)

plt.legend()
plt.show()
