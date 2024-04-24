import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder

# Cargar los datos
data = pd.read_csv('dataset comida.csv')

# Obtener las columnas de los ingredientes
ingredientes = ['Maíz', 'Frijoles', 'Especias', 'Tomates', 'Cebollas', 'Chile', 'Aguacate', 'Carne de res', 'Pollo', 'Cerdo',    'Pescado y mariscos', 'Arroz', 'Limones', 'Cilantro', 'Queso', 'Crema', 'Masa', 'Tortillas de harina',    'Tortillas de maíz', 'Quesillo', 'Ajo', 'Piña', 'Aceite de oliva', 'Albahaca',    'Queso (mozzarella, parmesano, ricotta, etc.)', 'Pasta (spaghetti, fettuccine, lasagna, etc.)',    'Champiñones', 'Vino tinto o blanco (usado en salsas y en algunos platos)', 'Pan', 'Lechuga', 'Salsa de tomate',    'Pepinillos', 'Mayonesa', 'Ketchup', 'Mostaza', 'Papas', 'Tocino', 'Huevos', 'Salsa picante', 'Legumbres',    'Tofu', 'Frutas (manzanas, peras, fresas, etc.)',    'Verduras (zanahorias, brócoli, calabacín, champiñones, etc.)', 'Frutos secos', 'Salsa de soja', 'Chocolate']


# Codificar las columnas de los ingredientes como variables dummy
data_encoded = pd.get_dummies(data, columns=ingredientes)

# Separar los datos en características (X) y etiquetas (y)
X = data_encoded.drop('Platillo', axis=1)
y = data_encoded['Platillo']

# Convertir las etiquetas categóricas en valores numéricos
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(y)

# Crear el modelo de regresión logística
model = LogisticRegression()

# Entrenar el modelo
model.fit(X, y)

# Predecir las etiquetas de los datos de entrenamiento
y_pred = model.predict(X)

# Graficar la regresión logística
plt.scatter(X.iloc[:, 0], X.iloc[:, 1], c=y_pred, cmap='viridis')
plt.xlabel('Característica 1')
plt.ylabel('Característica 2')
plt.title('Regresión Logística')
plt.show()
