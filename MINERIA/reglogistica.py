import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression

# Datos de ejemplo
X = np.array([[2, 4], [1, 3], [4, 2], [3, 5], [5, 1], [6, 4]])
y = np.array([0, 0, 1, 1, 1, 0])

# Inicialización y entrenamiento del modelo de regresión logística
model = LogisticRegression()
model.fit(X, y)

# Generar una malla de puntos para la gráfica
x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.01), np.arange(y_min, y_max, 0.01))
Z = model.predict(np.c_[xx.ravel(), yy.ravel()])
Z = Z.reshape(xx.shape)

# Obtener los coeficientes e intercepto de la regresión logística
coef = model.coef_
intercept = model.intercept_

# Calcular los valores correspondientes a la línea de decisión
line = (-coef[0, 0] * xx - intercept) / coef[0, 1]

# Graficar la región de decisión, los puntos de datos y la línea de decisión
plt.contourf(xx, yy, Z, alpha=0.8, cmap='bwr')
plt.scatter(X[:, 0], X[:, 1], c=y, cmap='bwr')
# plt.plot(xx, line, c='k', label='Línea de Decisión',color='blue', linewidth=2)

# Etiquetas y título del gráfico
plt.xlabel('Característica 1')
plt.ylabel('Característica 2')
plt.title('Gráfico de Regresión Logística')

# Mostrar la leyenda
plt.legend()

# Mostrar la gráfica
plt.show()
