import re
import networkx as nx
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk

def validar_curp(expresion, cadena):
    regex = re.compile(expresion)
    if regex.fullmatch(cadena):
        return True
    else:
        return False

def graficar_automata(expresion):
    expresion = re.sub(r'[^a-zA-Z]', '', expresion)
    G = nx.DiGraph()
    estados = set()
    transiciones = set()

    for i in range(len(expresion) + 1):
        estados.add(i)

    for i in range(len(expresion)):
        transiciones.add((i, i+1, expresion[i]))

    for estado, siguiente, simbolo in transiciones:
        G.add_edge(estado, siguiente, label=simbolo)

    pos = nx.circular_layout(G)
    labels = {i: f'q{i}' for i in estados}
    
    nx.draw_networkx_nodes(G, pos)
    nx.draw_networkx_edges(G, pos)
    nx.draw_networkx_labels(G, pos, labels)
    
    for estado, _, _ in transiciones:
        if G.has_edge(estado, estado):
            x, y = pos[estado]
            plt.text(x, y, "", bbox=dict(facecolor='white', edgecolor='white', boxstyle='circle'))

    nx.draw_networkx_edge_labels(G, pos, edge_labels={(estado, siguiente): simbolo for estado, siguiente, simbolo in transiciones})

    plt.show()

def validar_y_graficar():
    cadena = cadena_entry.get()
    expresion_seleccionada = expresion_combobox.get()

    if expresion_seleccionada == "MO*A*L*" :
        expresion = r'^[Mm]([Oo]{0,}[Aa]{0,}[Ll]{0,})$'
    elif expresion_seleccionada == "M(OAL)*":
        expresion = r'^[Mm](O|o|A|a|L|l){0,}$'

    resultado = validar_curp(expresion, cadena)
    mensaje_var.set(f'{cadena} - {"Cadena Valida" if resultado else "Cadena no valida"}')
    if resultado:
        graficar_automata(expresion)

app = tk.Tk()
app.title("Validador y Graficador de Expresiones Regulares")

frame_principal = ttk.Frame(app, padding="15")
frame_principal.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

cadena_label = ttk.Label(frame_principal, text="Ingrese la cadena:")
cadena_label.grid(column=0, row=0, sticky=tk.W)

cadena_var = tk.StringVar()
cadena_entry = ttk.Entry(frame_principal, textvariable=cadena_var)
cadena_entry.grid(column=1, row=0, sticky=tk.W)

expresion_label = ttk.Label(frame_principal, text="Seleccione la expresion:")
expresion_label.grid(column=0, row=1, sticky=tk.W)

expresion_var = tk.StringVar()
expresion_combobox = ttk.Combobox(frame_principal, textvariable=expresion_var, values=["MO*A*L*", "M(OAL)*"])
expresion_combobox.grid(column=1, row=1, sticky=tk.W)
expresion_combobox.set("MO*A*L*")

validar_button = ttk.Button(frame_principal, text="Validar y Graficar", command=validar_y_graficar)
validar_button.grid(column=0, row=2, columnspan=2, pady=10)

mensaje_var = tk.StringVar()
resultado_label = ttk.Label(frame_principal, textvariable=mensaje_var, foreground="blue")
resultado_label.grid(column=0, row=3, columnspan=2, pady=10)

app.mainloop()
