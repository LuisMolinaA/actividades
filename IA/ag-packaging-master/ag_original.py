import numpy as np
import math as m
import matplotlib.pyplot as plt
import pandas as pd
from paquete import Paquete
from contenedor import Repisa
import random

espacios = 2000000
repisa_size_x = 300
repisa_size_y = 100
repisa_size_z = 100


def algoritmo_gen(
    poblacionSize,
    poblacionMaxima,
    probMuta,
    estanterias,
    repisas,
    iteraciones,
    ruta_archivo,
):
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
                paquete = Paquete(id, tamaño, peso, volumen, longitud, anchura, altura)
                paquetes.append(paquete)
            print("Datos leídos desde el archivo CSV:")
            return paquetes

    def cruza(poblacion, csv, probMutacion):
        newPoblacion = []

        mejores_individuos = poblacion
        newPoblacion.extend(mejores_individuos)

        for individuo in poblacion:
            hijoLimpio = []
            for estanteria in individuo:
                estanteriaLimpia = []
                for repisa in estanteria:
                    repisaLimpia = Repisa(0, 0, 0) 
                    paquetesVistos = set()
                    cleanRepisa = []
                    for paquete in repisa.paquetes:
                        espacioRepisa = espacios - sum(
                            paquete.volumen for paquete in repisa.paquetes
                        )
                        paquetesVistos.add(paquete.id)
                        if random.random() < probMutacion:
                            c = 0
                            espacioRepisa += paquete.volumen
                            while espacioRepisa >= 0:
                                indice = random.randint(0, len(csv) - 1)
                                paqueteAcolocar = csv[indice]
                                volumenPaquete = paqueteAcolocar.volumen
                                if (
                                    paqueteAcolocar.id not in paquetesVistos
                                    and espacioRepisa >= volumenPaquete
                                ):
                                    cleanRepisa.append(paqueteAcolocar)
                                    paquetesVistos.add(paqueteAcolocar.id)
                                    espacioRepisa -= paqueteAcolocar.volumen
                                elif paqueteAcolocar.id in paquetesVistos and c != len(
                                    csv
                                ):
                                    c += 1
                                    continue
                                else:
                                    for paquete in csv:
                                        if (
                                            paqueteAcolocar.id not in paquetesVistos
                                            and espacioRepisa >= paqueteAcolocar.volumen
                                        ):
                                            cleanRepisa.append(paqueteAcolocar)
                                            espacioRepisa -= paqueteAcolocar.volumen
                                            paquetesVistos.add(paqueteAcolocar.id)
                                    break
                        else:
                            cleanRepisa.append(paquete)
                    repisaLimpia.paquetes = cleanRepisa
                    estanteriaLimpia.append(repisaLimpia)
                hijoLimpio.append(estanteriaLimpia)
            newPoblacion.append(hijoLimpio)

        return newPoblacion

    def evaluarIndividuo(individuo, csv):
        espacioTotal = estanterias * repisas * espacios
        volumenTotal = sum(paquete.volumen for paquete in csv)
        volumenOcupado = sum(
            sum(paquete.volumen for paquete in repisa.paquetes)
            for estanteria in individuo
            for repisa in estanteria
        )
        espacioDisponible = espacioTotal - volumenOcupado
        puntaje = espacioDisponible / volumenTotal

        return puntaje

    def seleccionarMejoresIndividuos(poblacion, csv, numMejores):
        evaluaciones = [
            (individuo, evaluarIndividuo(individuo, csv)) for individuo in poblacion
        ]
        evaluaciones.sort(key=lambda x: x[1], reverse=True)
        mejoresIndividuos = [evaluacion[0] for evaluacion in evaluaciones[:numMejores]]
        return mejoresIndividuos

    def contarPaquetes(estanterias):
        paquetesVistos = set()
        for estanteria in estanterias:
            for repisa in estanteria:
                for paquete in repisa.paquetes:
                    if paquete.id not in paquetesVistos:
                        paquetesVistos.add(paquete.id)

        return paquetesVistos

    def createIndividuo(csv):
        individuo = []
        paquetesSinGuardar = []
        paquetesColocados = set()
        for _ in range(estanterias):
            estanteria = []
            for _ in range(repisas):
                c = 0
                repisa = Repisa(0, 0, 0)
                espacioRepisa = espacios
                paquetes_repisa = []
                while espacioRepisa >= 0:
                    indice = random.randint(0, len(csv) - 1)
                    paquete = csv[indice]
                    volumenPaquete = paquete.volumen
                    if (
                        paquete.id not in paquetesColocados
                        and espacioRepisa >= volumenPaquete
                    ):
                        paquetes_repisa.append(paquete)
                        paquetesColocados.add(paquete.id)
                        espacioRepisa -= paquete.volumen
                    elif paquete.id in paquetesColocados and c != len(csv):
                        c += 1
                        continue
                    else:
                        for paquete in csv:
                            if (
                                paquete.id not in paquetesColocados
                                and espacioRepisa >= paquete.volumen
                            ):
                                paquetes_repisa.append(paquete)
                                espacioRepisa -= paquete.volumen
                                paquetesColocados.add(paquete.id)
                        break

                repisa.paquetes = paquetes_repisa
                estanteria.append(repisa)
            individuo.append(estanteria)
        paquetesGuardados = set(
            paquete.id
            for estanteria in individuo
            for repisa in estanteria
            for paquete in repisa.paquetes
        )

        for paquete in csv:
            if paquete.id not in paquetesGuardados:
                paquetesSinGuardar.append(paquete)
        return individuo

    def verificar_colision(posicion, longitud, anchura, altura, paquetes):
        for p in paquetes:
            # Verificar colisión basada en coordenadas y dimensiones
            if (
                # Punto frontal izquierdo
                posicion[0] < p.x + p.longitud
                and posicion[0] + longitud > p.x
                and posicion[1] < p.y + p.anchura
                and posicion[1] + anchura > p.y
                and posicion[2] < p.z + p.altura
                and posicion[2] + altura > p.z
                # Punto frontal derecho
                or posicion[0] + longitud > p.x
                and posicion[0] < p.x + p.longitud
                and posicion[1] < p.y + p.anchura
                and posicion[1] + anchura > p.y
                and posicion[2] < p.z + p.altura
                and posicion[2] + altura > p.z
                # Punto trasero izquierdo
                or posicion[0] < p.x + p.longitud
                and posicion[0] + longitud > p.x
                and posicion[1] + anchura > p.y
                and posicion[1] < p.y + p.anchura
                and posicion[2] < p.z + p.altura
                and posicion[2] + altura > p.z
                # Punto trasero derecho
                or posicion[0] + longitud > p.x
                and posicion[0] < p.x + p.longitud
                and posicion[1] + anchura > p.y
                and posicion[1] < p.y + p.anchura
                and posicion[2] < p.z + p.altura
                and posicion[2] + altura > p.z
                # Punto frontal superior izquierdo
                or posicion[0] < p.x + p.longitud
                and posicion[0] + longitud > p.x
                and posicion[1] < p.y + p.anchura
                and posicion[1] + anchura > p.y
                and posicion[2] + altura > p.z
                and posicion[2] < p.z + p.altura
                # Punto frontal superior derecho
                or posicion[0] + longitud > p.x
                and posicion[0] < p.x + p.longitud
                and posicion[1] < p.y + p.anchura
                and posicion[1] + anchura > p.y
                and posicion[2] + altura > p.z
                and posicion[2] < p.z + p.altura
                # Punto frontal inferior izquierdo
                or posicion[0] < p.x + p.longitud
                and posicion[0] + longitud > p.x
                and posicion[1] + anchura > p.y
                and posicion[1] < p.y + p.anchura
                and posicion[2] + altura > p.z
                and posicion[2] < p.z + p.altura
                # Punto frontal inferior derecho
                or posicion[0] + longitud > p.x
                and posicion[0] < p.x + p.longitud
                and posicion[1] + anchura > p.y
                and posicion[1] < p.y + p.anchura
                and posicion[2] + altura > p.z
                and posicion[2] < p.z + p.altura
            ):
                return True  # Hay colisión
            # Verificar si el nuevo paquete está completamente dentro de otro paquete

            if (
                posicion[0] >= p.x
                and posicion[0] <= p.x + p.longitud
                and posicion[1] >= p.y
                and posicion[1] <= p.y + p.anchura
                and posicion[2] >= p.z
                and posicion[2] <= p.z + p.altura
                and posicion[0] + longitud >= p.x
                and posicion[0] + longitud <= p.x + p.longitud
                and posicion[1] + anchura >= p.y
                and posicion[1] + anchura <= p.y + p.anchura
                and posicion[2] + altura >= p.z
                and posicion[2] + altura <= p.z + p.altura
                # Verificar los ocho puntos extremos del nuevo paquete
                and not any(
                    [
                        verificar_colision(
                            (posicion[0], posicion[1], posicion[2]),
                            0,
                            0,
                            0,
                            [p],
                        ),
                        verificar_colision(
                            (posicion[0] + longitud, posicion[1], posicion[2]),
                            0,
                            0,
                            0,
                            [p],
                        ),
                        verificar_colision(
                            (posicion[0], posicion[1] + anchura, posicion[2]),
                            0,
                            0,
                            0,
                            [p],
                        ),
                        verificar_colision(
                            (posicion[0], posicion[1], posicion[2] + altura),
                            0,
                            0,
                            0,
                            [p],
                        ),
                        verificar_colision(
                            (
                                posicion[0] + longitud,
                                posicion[1] + anchura,
                                posicion[2],
                            ),
                            0,
                            0,
                            0,
                            [p],
                        ),
                        verificar_colision(
                            (posicion[0], posicion[1] + anchura, posicion[2] + altura),
                            0,
                            0,
                            0,
                            [p],
                        ),
                        verificar_colision(
                            (posicion[0] + longitud, posicion[1], posicion[2] + altura),
                            0,
                            0,
                            0,
                            [p],
                        ),
                        verificar_colision(
                            (
                                posicion[0] + longitud,
                                posicion[1] + anchura,
                                posicion[2] + altura,
                            ),
                            0,
                            0,
                            0,
                            [p],
                        ),
                    ]
                )
            ):
                return True  # Hay colisión total

        return False  # No hay colisión

    def distribuir_paquetes(repisa_size_x, repisa_size_y, repisa_size_z, paquetes):

        paquetes.sort(key=lambda p: p.volumen, reverse=True)
        current_x = current_y = current_z = 0

        for paquete in paquetes:

            # Intentar colocar el paquete en la posición actual sin colisiones
            if (
                current_x + paquete.longitud <= repisa_size_x
                and current_y + paquete.anchura <= repisa_size_y
                and current_z + paquete.altura <= repisa_size_z
                and not verificar_colision(
                    (current_x, current_y, current_z),
                    paquete.longitud,
                    paquete.anchura,
                    paquete.altura,
                    paquetes[: paquetes.index(paquete)],
                )
            ):

                paquete.x, paquete.y, paquete.z = current_x, current_y, current_z

                current_x += paquete.longitud

            else:
                # Intentar rotar el paquete y colocarlo en una posición sin colisiones
                rotated = False
                for _ in range(3):  # Intentar rotar en cada eje (x, y, z)
                    paquete.longitud, paquete.anchura, paquete.altura = (
                        paquete.anchura,
                        paquete.altura,
                        paquete.longitud,
                    )
                    if (
                        current_x + paquete.longitud <= repisa_size_x
                        and current_y + paquete.anchura <= repisa_size_y
                        and current_z + paquete.altura <= repisa_size_z
                        and not verificar_colision(
                            (current_x, current_y, current_z),
                            paquete.longitud,
                            paquete.anchura,
                            paquete.altura,
                            paquetes[: paquetes.index(paquete)],
                        )
                    ):
                        paquete.x, paquete.y, paquete.z = (
                            current_x,
                            current_y,
                            current_z,
                        )
                        current_x += paquete.longitud
                        rotated = True
                        break
                if not rotated:
                    # Si no se pudo colocar el paquete sin colisiones ni rotaciones, colocarlo encima de otro paquete
                    for p in paquetes[: paquetes.index(paquete)]:
                        if p.z + p.altura <= repisa_size_z and not verificar_colision(
                            (p.x, p.y, p.z + p.altura),
                            paquete.longitud,
                            paquete.anchura,
                            paquete.altura,
                            paquetes[: paquetes.index(paquete)],
                        ):
                            paquete.x, paquete.y, paquete.z = p.x, p.y, p.z + p.altura
                            break
                    else:
                        # Si no se puede colocar encima de otro paquete, mover al siguiente nivel (eje y)
                        current_y += paquete.anchura
                        current_x = 0
                        current_z = 0

                        if current_y + paquete.anchura > repisa_size_y:
                            current_z += paquete.altura
                            current_y = 0

                            if current_z + paquete.altura > repisa_size_z:
                                print(
                                    "La repisa está llena. No se pueden colocar más paquetes."
                                )
                                break

    def visualizarPoblacion(population):
        best_individual = max(
            population, key=lambda individuo: evaluarIndividuo(individuo, csv)
        )

        for j, estanteria in enumerate(best_individual):
            fig = plt.figure()  # Crear una nueva figura para cada estantería
            fig.suptitle(f"Estantería {j+1}")  # Establecer un título para la figura
            for k, repisa in enumerate(estanteria):
                ax = fig.add_subplot(
                    1, len(estanteria), k + 1, projection="3d"
                )  # Añadir un subplot para cada repisa
                ax.set_title(f"Repisa {k+1}")  # Establecer el título
                visualizarRepisa3D(
                    ax, repisa, repisa_size_x, repisa_size_y, repisa_size_z
                )

            plt.show()

    def visualizarRepisa3D(
        ax, repisa, repisa_size_x, repisa_size_y, repisa_size_z, escala=1.0
    ):
        for paquete in repisa.paquetes:
            ax.bar3d(
                paquete.x,
                paquete.y,
                paquete.z,
                paquete.longitud,
                paquete.anchura,
                paquete.altura,
                color=paquete.color,
                alpha=0.8,
                linewidth=0.5,
                edgecolor="black",
            )

    csv = ReadData(ruta_archivo).readCsv()
    poblacion = [createIndividuo(csv) for _ in range(poblacionSize)]
    for _ in range(iteraciones):

        poblacion = cruza(poblacion, csv, probMuta)
        poblacion = seleccionarMejoresIndividuos(poblacion, csv, poblacionMaxima)

    for estanteria in poblacion[0]:
        for repisa in estanteria:
            distribuir_paquetes(
                repisa_size_x, repisa_size_y, repisa_size_z, repisa.paquetes
            )
    visualizarPoblacion(poblacion)
    paquetes = len(contarPaquetes(poblacion[0]))
    print(paquetes - len(csv), "paquetes")
