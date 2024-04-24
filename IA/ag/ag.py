import numpy as np
import math as m
import matplotlib.pyplot as plt
import pandas as pd
from paquete import Paquete
import random

espacios = 3000000

def algoritmo_gen(poblacionSize, poblacionMaxima, probCruza, probMuta, estanterias, repisas, iteraciones, ruta_archivo):
    class ReadData:
        def __init__(self, archivo):
            self.archivo = archivo

        def readCsv(self):
            df = pd.read_csv(self.archivo)
            paquetes = []
            for index, row in df.iterrows():
                id = row["ID"]
                tamaño = row["Tamaño"]
                peso = row["Peso"]
                volumen = row["Volumen"]
                longitud = row["Longitud"]
                anchura = row["Anchura"]
                altura = row["Altura"]
                paquete = Paquete(
                    id, tamaño, peso, volumen, longitud, anchura, altura
                )
                paquetes.append(paquete)
            print("Datos leídos desde el archivo CSV:")
            return paquetes


    def cruza(poblacion, csv, probCruza):
        newPoblacion = []
        poblacion.sort(
            key=lambda individuo: evaluarIndividuo(individuo, csv), reverse=True
        )
        for estanteria in poblacion:
            if random.uniform(0, 1) < probCruza:
                padre2 = random.sample(poblacion, 1)
                padre1 = estanteria
                puntoCruza = random.randint(0, len(padre1))
                hijo = padre1[:puntoCruza] + padre2[0][puntoCruza:]
                newPoblacion.append(padre1)
                newPoblacion.append(hijo)
                hijo = eliminarPaquetesRepetidos(hijo, csv)

            else:
                newPoblacion.append(estanteria)
        newPoblacion = poblacion + newPoblacion
        return newPoblacion


    def mutacion(poblacion, probMutacion, csv):
        for individuo in poblacion:
            if random.random() < probMutacion:
                repisa1 = random.randint(0, len(individuo) - 1)
                repisa2 = random.randint(0, len(individuo) - 1)
                paquete1 = random.randint(0, len(individuo[repisa1]) - 1)
                paquete2 = random.randint(0, len(individuo[repisa2]) - 1)
                individuo[repisa1][paquete1], individuo[repisa2][paquete2] = individuo[repisa2][paquete2], individuo[repisa1][paquete1]
                individuo = eliminarPaquetesRepetidos(individuo, csv)
        return poblacion


    def evaluarIndividuo(individuo, csv):
        espacioTotal = estanterias * repisas * espacios
        volumenTotal = sum(paquete.volumen for paquete in csv)
        volumenOcupado = sum(
            sum(sum(paquete.volumen for paquete in repisa) for repisa in estanteria)
            for estanteria in individuo
        )
        espacioDisponible = espacioTotal - volumenOcupado
        puntaje = espacioDisponible / volumenTotal
        paquetesDentro = contarPaquetes(individuo)
        paquetesFuera = len(csv) - paquetesDentro
        puntaje += 0.3 * paquetesFuera

        return puntaje


    def seleccionarMejoresIndividuos(poblacion, csv, numMejores):
        evaluaciones = [
            (individuo, evaluarIndividuo(individuo, csv)) for individuo in poblacion
        ]
        evaluaciones.sort(key=lambda x: x[1], reverse=True)
        mejoresIndividuos = [evaluacion[0] for evaluacion in evaluaciones[:numMejores]]
        return mejoresIndividuos


    def contarPaquetes(estanterias):
        paquetesVistos = []
        for estanteria in estanterias:
            for repisa in estanteria:
                volumenEstante = espacios
                for paquete in repisa:
                    if (
                        paquete.id not in paquetesVistos
                        and volumenEstante >= paquete.volumen
                    ):
                        volumenEstante -= paquete.volumen
                        paquetesVistos.append(paquete.id)

        return len(paquetesVistos)


    def eliminarPaquetesRepetidos(hijo, csv):
        hijoLimpio = []

        for estanteria in hijo:
            paquetesVistos = set()
            cleanEstanteria = []
            for repisa in estanteria:
                volumenEstante = espacios
                cleanRepisa = []
                for paquete in repisa:
                    if (
                        paquete.id not in paquetesVistos
                        and volumenEstante >= paquete.volumen
                    ):
                        volumenEstante -= paquete.volumen
                        paquetesVistos.add(paquete.id)
                        cleanRepisa.append(paquete)
                    else:
                        for paquete in csv:
                            if (
                                paquete.id not in paquetesVistos
                                and volumenEstante >= paquete.volumen
                            ):
                                cleanRepisa.append(paquete)
                                volumenEstante -= paquete.volumen
                                paquetesVistos.add(paquete.id)
                        continue

            hijoLimpio.append(cleanEstanteria)
        return hijoLimpio


    def createIndividuo(csv):
        individuo = []
        paquetesSinGuardar = []
        paquetesColocados = set()
        for _ in range(estanterias):
            estanteria = []
            for _ in range(repisas):
                c = 0

                repisa = []
                espacioEstanteria = espacios
                while espacioEstanteria >= 0:
                    indice = random.randint(0, len(csv) - 1)
                    paquete = csv[indice]
                    volumePaquete = paquete.volumen
                    if (
                        paquete.id not in paquetesColocados
                        and espacioEstanteria >= volumePaquete
                    ):
                        repisa.append(paquete)
                        espacioEstanteria -= volumePaquete
                        paquetesColocados.add(paquete.id)
                    elif paquete.id in paquetesColocados and c != len(csv):
                        c += 1
                        continue
                    else:
                        for paquete in csv:
                            if (
                                paquete.id not in paquetesColocados
                                and espacioEstanteria >= paquete.volumen
                            ):
                                repisa.append(paquete)
                                espacioEstanteria -= paquete.volumen
                                paquetesColocados.add(paquete.id)
                        break

                estanteria.append(repisa)
            individuo.append(estanteria)

        paquetesGuardados = set(
            paquete.id
            for estanteria in individuo
            for repisa in estanteria
            for paquete in repisa
        )
        for paquete in csv:
            if paquete.id not in paquetesGuardados:
                paquetesSinGuardar.append(paquete)
        return individuo


    def visualizarPoblacion(population):
        for _, individuo in enumerate(population):
            print(f"Individuo {_ + 1}:")
            visualizarIndividuos(individuo[0])
            print("-----------------------")


    def visualizarIndividuos(individuo):
        # Creamos una paleta de colores única para cada paquete
        num_colores = len(individuo) * len(individuo[0])  # Calculamos el número total de colores necesarios
        colores = plt.cm.viridis(np.linspace(0, 1, num_colores))  # Generamos la paleta de colores

        idx_color = 0  # Índice para iterar sobre la paleta de colores

        # Desplazamiento para separar las cajas
        desplazamiento = 0.1
        
        for j, repisa in enumerate(individuo):
            fig = plt.figure(figsize=(10, 6))
            ax = fig.add_subplot(111, projection='3d')

            posiciones_ocupadas = set()  # Conjunto para registrar las posiciones ocupadas en la repisa

            for k, paquete in enumerate(repisa):
                # Intentamos colocar el paquete en una posición que no esté ocupada
                intentos = 0
                while True:
                    # Calculamos las coordenadas del paquete dentro de la repisa con desplazamiento
                    x = 0  # La posición X de todas las cajas en una repisa es la misma
                    y = k * 2 + desplazamiento * k  # Espacio entre paquetes + desplazamiento
                    z = j * 2 + desplazamiento * j  # Espacio entre repisas + desplazamiento
                    dx = paquete.longitud
                    dy = paquete.anchura
                    dz = paquete.altura

                    # Verificamos si la posición está ocupada
                    if (y, z) not in posiciones_ocupadas:
                        # Si la posición no está ocupada, agregamos el paquete y registramos la posición
                        ax.bar3d(x, y, z, dx, dy, dz, color=colores[idx_color % num_colores], edgecolor='k')
                        posiciones_ocupadas.add((y, z))
                        break  # Salimos del bucle while ya que hemos colocado el paquete
                    else:
                        # Si la posición está ocupada, incrementamos el número de intentos
                        intentos += 1
                        # Si hemos intentado demasiadas veces sin éxito, aumentamos el desplazamiento
                        if intentos >= len(repisa):
                            desplazamiento += 0.1  # Aumentamos el desplazamiento para evitar la superposición
                            break

                idx_color += 1

            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_zlabel('Z')
            ax.set_title(f'Repisa {j+1}')

            # Creamos la leyenda de los colores de los paquetes
            handles = [plt.Rectangle((0,0),1,1, color=colores[i % num_colores]) for i in range(num_colores)]
            ax.legend(handles, [f'Box {i+1}' for i in range(num_colores)], loc='upper left')

            plt.show()

    for _ in range(iteraciones):
        csv = ReadData(ruta_archivo).readCsv()
        poblacion = [createIndividuo(csv) for _ in range(poblacionSize)]
        poblacion = cruza(poblacion, csv, probCruza)
        poblacion = mutacion(poblacion, probMuta, csv)
        poblacion = seleccionarMejoresIndividuos(poblacion, csv, poblacionMaxima)

    poblacion.sort(key=lambda individuo: evaluarIndividuo(individuo, csv))
    visualizarIndividuos(poblacion[0][0])
    paquetes = contarPaquetes(poblacion[0])
    print(paquetes - len(csv), "paquetes")
    