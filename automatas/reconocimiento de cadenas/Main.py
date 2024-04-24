import locale
import io
import textwrap
import tkinter as tk
from tkinter import messagebox as mb
from tkinter import filedialog
from tkinter.ttk import Treeview
from tkinter import ttk
from tkinter import *
import numpy as np
from Automata import *

sentenciasValidas = []

def openfile():
    fileopen = filedialog.askopenfilename(
        initialdir="/",
        title="Seleccione su archivo de texto",
        filetypes=(("Text files", "*.txt"), ("All files", "*.*")),
    )
    print(fileopen)
    create_query_string(fileopen)

def guess_encoding(fileopen):
    with io.open(fileopen, "rb") as f:
        data = f.read(5)
    if data.startswith(b"\xEF\xBB\xBF"):
        return "utf-8-sig"
    elif data.startswith(b"\xFF\xFE") or data.startswith(b"\xFE\xFF"):
        return "utf-16"
    else:  
        try:
            with io.open(fileopen, encoding="utf-8") as f:
                return "utf-8"
        except UnicodeDecodeError:
            return locale.getdefaultlocale()[1]

def create_query_string(sql_file):
    with open(sql_file, 'r', encoding=guess_encoding(sql_file)) as f_in:
        lines = f_in.read()
        query_string = textwrap.dedent("""{}""".format(lines))
    try:
        with open('data.txt', 'w') as f:
            f.write(query_string)
            f.close()

    except:
        verdad = False

    with open('data.txt') as archivo:
        for linea in archivo:
            lin = linea.replace("\n", "")
            print(lin)
            automata.Automata(lin)
            if automata.Automata(lin):
                print(automata.Automata(lin))
                sentenciasValidas.append(lin)
                print(sentenciasValidas)
    cont = str(sentenciasValidas)
    cal = cont.replace("[", "")
    lista = cal.replace("]", "")
    limp = lista.replace("'", "")
    limpio = limp.replace(",", "\n")
    with open('sentenciasValidas.txt', 'w') as f:
        f.write(limpio)
        f.close()
    sentenciasValidas.clear()
    with open('sentenciasValidas.txt') as f:
        vacio = f.readlines()
        print(vacio)
        if vacio == []:
            mb.showerror("Mensaje", "Sentencias no validas")
        else:
            showData()

def inicio():
    scene = tk.Tk()
    scene.title("Seleccion de archivo txt")
    scene['bg'] = '#2C0D8E'
    scene.geometry('400x300')
    scene.resizable(width=False, height=False)
    canvas = Canvas(scene, width=320, height=320, bg="#CEAB00")
    canvas.create_text(160, 100, text="Busque su archivo txt", fill="black", font=('Helvetica 15'))
    Button(scene, text="Agregar archivo", command=openfile).place(relx=0.5, rely=0.5, width=100, anchor='c')
    canvas.pack()
    scene.mainloop()

def showData():
    scene = Tk()
    scene.title('Sentencias validas')
    scene.geometry('500x150')
    scene['bg'] = '#2C0D8E'

    td = ttk.Treeview(scene, columns=1, height=50)
    td.pack(pady=15, padx=10)
    td.column("#0", width=500, minwidth=100)
    td.heading("#0", text="Sentencias", anchor=CENTER)

    with open('sentenciasValidas.txt') as archivo:
        for linea in archivo:
            if linea == " ":
                print("no hay valores")
            else:
                td.insert('', 0, text=linea)
    td.pack()

    scene.mainloop()

if __name__ == '__main__':
    inicio()
