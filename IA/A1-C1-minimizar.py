import random
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from sympy import symbols, cos, solve
import sympy as sp
import os
import cv2
from natsort import natsorted
import numpy as np

labelArr = [
    "Poblacion Inicial",
    "Poblacion Maxima",
    "Max Generacion",
    "prob Cruza",
    "prob Muta",
    "a",
    "b",
    "resolucion inicial",
    "Tipo (max o min)",
    "Prob Gen"
]
z = 0

def binarioDecimal(binario):
    # Convierte los números binarios a enteros
    decimal = int("".join(map(str, binario)), 2)
    return decimal


def firstPov(poblacionSize, canBinario):
    pob = []
    for _ in range(poblacionSize):
        individuo = [random.randint(0, 1) for _ in range(canBinario)]
        pob.append(individuo)
    print(pob)
    return pob


def evolPoblacion(poblacion, poblacionSize, propCruza, propMuta, propMutaGen):
    new_poblacion = []
    for i in range(len(poblacion)):
        if random.random() < propCruza:
            first_padre = poblacion[i]
            ran = random.randint(0, len(poblacion) - 1)
            second_padre = poblacion[ran]
            sectores_totales = len(first_padre)
            sector = random.randint(0, sectores_totales - 1)
            descendiente1 = first_padre[:sector] + second_padre[sector:]
            new_poblacion.append(poblacion[i])
            new_poblacion.append(descendiente1)
        else:
            new_poblacion.append(poblacion[i])
            
    new_poblacion.append(poblacion[0])    
    for z in range(len(poblacion)):
        if random.random() < propMuta:
            for x in range(len(poblacion[z])):
                if random.random() < propMutaGen:
                    new_poblacion[i][x] = 1 if new_poblacion[i][x] == 0 else 0
    new_poblacion[0]=poblacion[0]
    return new_poblacion


def poda(poblacion, poblacionSize):
    iguales = set(map(tuple, poblacion))
    popClean = list(map(list, iguales))
    if len(popClean) > poblacionSize:
        popClean = popClean[:poblacionSize]
    print(f"se ha creado una nueva descendencia de {len(popClean)}")
    return popClean


def algoritmoGenetico(
    poblacionSize, generaciones, propCruza, propMuta, a, b, resolucion, popInicial, tipo,propMutaGen
):
    canBinario = calcularBin(resolucion, a, b)
    poblacion = firstPov(popInicial, canBinario)
    mejores_fitness = []
    peores_fitness = []
    promedio_fitness = []
    calculoX = []
    for generacion in range(generaciones):
        num = [binarioDecimal(individuo) for individuo in poblacion]
        print(num)
        x = [calcularX(a, b, i, canBinario) for i in num]
        fitness = [(x**2*np.cos(x)*np.sin(x)*np.log(np.abs(x)+2)) for x in x]
        poblacion_fitness = list(zip(poblacion, fitness))
        if tipo == "min":
            poblacion_fitness.sort(key=lambda x: x[1])
            mejores_fitness.append(min(fitness))
            peores_fitness.append(max(fitness))
        elif tipo == "max":
            poblacion_fitness.sort(key=lambda x: x[1], reverse=True)
            mejores_fitness.append(max(fitness))
            peores_fitness.append(min(fitness))
            
        poblacion_ordenada, fitness_ordenado = zip(*poblacion_fitness)
        poblacion_ordenada = poblacion_ordenada[:poblacionSize]
        promedio_fitness.append(sum(fitness) / len(fitness))
        
        poblacion = evolPoblacion(
            poblacion_ordenada, poblacionSize, propCruza, propMuta, propMutaGen
        )
        genImg(a,b,fitness,x, generaciones,tipo)
        poblacion = poda(poblacion, poblacionSize)
    
    folder_path = './Imagenes'
    video_path = './video.mp4'
    convertir_a_video(folder_path, video_path)
    print("mejores fitness por cada generacion")
    print(mejores_fitness)
    print(calculoX)
    if tipo == "min":
        minimo = min(mejores_fitness)
        maximo = max(peores_fitness)
    elif tipo == "max":
        maximo = max(mejores_fitness)
        minimo = min(peores_fitness)

    generaciones = range(1, generaciones + 1)
    plt.plot(
        generaciones, mejores_fitness, label="Mejor Fitness", marker="o", linestyle="-"
    )
    plt.plot(
        generaciones, peores_fitness, label="Peor Fitness", marker="o", linestyle="-"
    )
    plt.plot(
        generaciones,
        promedio_fitness,
        label="Fitness Promedio",
        marker="o",
        linestyle="-",
    )

    plt.xlabel("Generación")
    plt.ylabel("Fitness")
    plt.title("Desempeño del Algoritmo Genético por Generación")
    plt.legend()
    plt.ylim(bottom=int(minimo) - 5, top=int(maximo) + 5)

    plt.show()


def genImg(a,b,fitness,x, generaciones,tipo):
    generaciones = range(1, generaciones + 1)
    global z
    z = z+1
    
    def mi_funcion(x):
        return (x**2*np.cos(x)*np.sin(x)*np.log(np.abs(x)+2))
    coordenadas = [(x, fitness) for i in x]
    intervalo_x = np.linspace(b, a, 1000)
    valores_y = mi_funcion(intervalo_x)
    plt.plot(intervalo_x, valores_y, label='Funcion')
    
    indice_min = np.argmin(fitness)
    indice_max = np.argmax(fitness)
    print(indice_max)
    print(indice_min)
    
    if tipo=="max":
        for i, (x_punto, y_punto) in enumerate(coordenadas):
            if i == indice_min:
                plt.scatter(x_punto, y_punto, color='green', marker='o', label='peor individuo')
            elif i == indice_max:
                plt.scatter(x_punto, y_punto, color='blue', marker='o', label='mejor individuo')
    elif tipo=="min":
        for i, (x_punto, y_punto) in enumerate(coordenadas):
            if i == indice_min:
                plt.scatter(x_punto, y_punto, color='green', marker='o', label='mejor individuo')
            elif i == indice_max:
                plt.scatter(x_punto, y_punto, color='blue', marker='o', label='peor individuo')


    plt.title(f'Generacion')
    plt.xlabel('Eje X')
    plt.ylabel('Eje Y')
    plt.legend()
    plt.grid(True)
    folder_path = './Imagenes'
    os.makedirs(folder_path, exist_ok=True)
    image_path = os.path.join(folder_path, f'grafico_ejemplo{z}.png')
    plt.savefig(image_path)
    plt.close()

    
def convertir_a_video(folder_path, video_path):
    print("video")
    image_files = [f for f in os.listdir(folder_path) if f.endswith('.png')]
    image_files = natsorted(image_files)  
    first_image_path = os.path.join(folder_path, image_files[0])
    img = cv2.imread(first_image_path)
    height, width, _ = img.shape

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  
    video = cv2.VideoWriter(video_path, fourcc, 1, (width, height))
    for image_file in image_files:
        image_path = os.path.join(folder_path, image_file)
        img = cv2.imread(image_path)
        video.write(img)
    video.release()
    cv2.destroyAllWindows()
    global numero
    numero = 0
    global z
    z= 0
    
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f'Error al eliminar {file_path}: {e}')

def calcularBin(resolucion, a, b):
    rango = b - a
    if rango < 0:
        rango = rango * -1
    numPuntos = (rango / resolucion) + 1
    n = 1
    while not (2 ** (n - 1) <= numPuntos <= 2**n):
        n = n + 1
    return n


def calcularX(a, b, i, canBinario):
    delta_x = calcularDX(a, b, canBinario)
    x = a + (i * delta_x)
    return x


def calcularDX(a, b, canBinario):
    rango = b - a
    delta_x = abs(rango / (2**canBinario - 1))
    return delta_x


if __name__ == "__main__":

    def submit_data():
        # Obtener los datos ingresados
        poblacionSize = 12
        generaciones = 12
        propCruza = 0.33
        propMuta = 0.4
        popInicial = 0
        a = 0
        b = 0
        resolucion = 0
        tipo = ""

        i = 0
        for entry in entries:
            if i == 0:
                valor_ingresado = entry.get()
                popInicial = int(valor_ingresado)
            elif i == 1:
                valor_ingresado = entry.get()
                poblacionSize = int(valor_ingresado)
            elif i == 2:
                valor_ingresado = entry.get()
                generaciones = int(valor_ingresado)
            elif i == 3:
                valor_ingresado = entry.get()
                propCruza = float(valor_ingresado)
            elif i == 4:
                valor_ingresado = entry.get()
                propMuta = float(valor_ingresado)
            elif i == 5:
                valor_ingresado = entry.get()
                a = float(valor_ingresado)
            elif i == 6:
                valor_ingresado = entry.get()
                b = float(valor_ingresado)
            elif i == 7:
                valor_ingresado = entry.get()
                resolucion = float(valor_ingresado)
            elif i == 8:
                valor_ingresado = entry.get()
                tipo = valor_ingresado
            elif i == 9:
                valor_ingresado = entry.get()
                propMutaGen = float(valor_ingresado)

            i += 1

        algoritmoGenetico(
            poblacionSize,
            generaciones,
            propCruza,
            propMuta,
            a,
            b,
            resolucion,
            popInicial,
            tipo,
            propMutaGen
        )

        # Crear la ventana principal

    window = tk.Tk()
    window.title("Ingreso de Datos")

    header_label = tk.Label(window, text="Ingrese los datos:")
    header_label.grid(row=0, column=0, columnspan=2, padx=10, pady=5)

    # Crear las etiquetas y campos de entrada
    labels = []
    entries = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for i in range(len(labelArr)):
        label = tk.Label(window, text=f" {labelArr[i]}:")
        label.grid(row=i + 1, column=0, padx=10, pady=5)
        entry = tk.Entry(window)
        entry.grid(row=i + 1, column=1, padx=10, pady=5)
        labels.append(label)
        entries[i] = entry

    submit_button = tk.Button(window, text="Submit", command=submit_data)
    submit_button.grid(row=len(labelArr) + 1, column=0, columnspan=2, padx=10, pady=10)
    # Iniciar el bucle principal de la interfaz
    window.mainloop()
