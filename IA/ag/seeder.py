from paquete import Paquete
import pandas as pd
import random
import string

cant = 1000

def generar_paquete():
    id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    
    tamaño = random.choices(["pequeño", "mediano", "grande"], weights=[4, 3, 3])[0]
    
    if tamaño == "pequeño":
        peso = round(random.uniform(0.5, 5), 2)
        longitud = round(random.uniform(10, 40), 0)  # Rango de 10 cm a 40 cm
        anchura = round(random.uniform(10, 30), 0)  # Rango de 10 cm a 30 cm
        altura = round(random.uniform(1, 20), 0)    # Rango de 1 cm a 20 cm
    elif tamaño == "mediano":
        peso = round(random.uniform(5, 20), 2)
        longitud = round(random.uniform(30, 100), 0)  # Rango de 30 cm a 100 cm
        anchura = round(random.uniform(20, 60), 0)    # Rango de 20 cm a 60 cm
        altura = round(random.uniform(10, 50), 0)     # Rango de 10 cm a 50 cm
    elif tamaño == "grande":
        peso = round(random.uniform(20, 50), 2)
        longitud = round(random.uniform(80, 200), 0)  # Rango de 80 cm a 200 cm
        anchura = round(random.uniform(50, 100), 0)  # Rango de 50 cm a 150 cm
        altura = round(random.uniform(30, 100), 0)   # Rango de 30 cm a 100 cm
    volumen = round(longitud * anchura * altura, 0)
    
    return Paquete(id, tamaño, peso, volumen, longitud, anchura, altura)

paquetes = [generar_paquete() for _ in range(cant)]

data = {
    'ID': [paquete.id for paquete in paquetes],
    'Tamaño': [paquete.tamaño for paquete in paquetes],
    'Peso': [paquete.peso for paquete in paquetes],
    'Volumen': [paquete.volumen for paquete in paquetes],
    'Longitud': [paquete.longitud for paquete in paquetes],
    'Anchura': [paquete.anchura for paquete in paquetes],
    'Altura': [paquete.altura for paquete in paquetes]
}

df = pd.DataFrame(data)

df.to_csv('./ag/dataset.csv', index=False)
print("todo piola")
