__author__ = 'MaiteFelipe'
import os
from os import listdir, rename, chmod, remove, rmdir
from os.path import isdir, isfile, join, splitext, getsize
import shutil
import random
import re


def print_tree(dir_path):
    for nombre in listdir(dir_path):
        full_path = join(dir_path, nombre) # concatena los path pasados por pramentros
        if isfile(full_path):
            cadena = random.randint(1000, 2000)

            extension = splitext(nombre) # separa el nombre del file de la extension
            extension = extension[1]
            cadena = join(dir_path, 'programacion' + str(cadena) + extension + '.ext')

            if extension != '.py' and extension != '.ext':
                shutil.move(full_path, cadena) #cambia el nombre
        if isdir(full_path):
            print_tree(full_path)


# Eliminar directorio aunque tenga archivos dentro
def eliminar_dir(dir_path):
    for nombre in listdir(dir_path):
        full_path = join(dir_path, nombre) #concatena los path pasados por pramentros
        if isfile(full_path):
            remove(full_path)
        if isdir(full_path):
            eliminar_dir(full_path)
    rmdir(dir_path)


def del_caracteres_especiales (dir_path):
    # Eliminar los caracteres especiales del nombre de los archivos y dir
    for dir1 in listdir(dir_path):
        full_path = join(dir_path, dir1)
        new_Dir1 = re.sub(r"[^ ().a-zá-úÁ-ÚA-Z0-9_Ññ\-\[\]]", "", dir1)
        new_full_path = join(dir_path, new_Dir1)

        try:
            rename(full_path, new_full_path)
        except FileExistsError:
            print("El directorio o archivo ya existe : " + "Nombre actual: " + str(full_path) + " -> " +
                  "Nuevo nombre: " + str(new_full_path))

        if isdir(full_path):
            del_caracteres_especiales(full_path)


# Agrega en el nombre del dir el tamanno [_tamanno]
def property_size(dir_path):
    del_caracteres_especiales(dir_path)

    for dir1 in listdir(dir_path):
        full_path = join(dir_path, dir1)

        size = 0

        size_KB = 0
        size_MB = 0
        size_Gb = 0
        if isdir(full_path):
            # Calcula el tamanno de la carpeta
            for root, dirs, files in os.walk(full_path):
                #calcula el tamano de los ficheros(no dir) en el dir
                # (file es una lista de todos los ficheros en el dir raiz (root))
                size += sum(getsize(join(root, name)) for name in files)
                size_KB = size/1024
                size_MB = (size/1024)/1024
                size_Gb = ((size/1024)/1024)/1024

            # Quitando el tamanno del nombre del
            # dir en caso que ya estuviera renombrado con el tamanno
            parte_string1 = dir1.partition("[_")
            parte_string2 = dir1.partition("_]")
            dir1 = parte_string1[0] + parte_string2[2]

            #cambiar el nombre de la carpeta
            if size_Gb >= 1:

                cadena_actual = dir1 + "[_" + str("{:.2f}".format(size_Gb)) + " GB_]"
                cadena = join(dir_path, cadena_actual)
                shutil.move(full_path, cadena)
                full_path = cadena
            if 1024 > size_MB >= 1:
                cadena_actual = dir1 + "[_" + str("{:.2f}".format(size_MB)) + " MB_]"
                cadena = join(dir_path, cadena_actual)
                shutil.move(full_path, cadena)
                full_path = cadena
            if 1024 > size_KB >= 1:
                cadena_actual = dir1 + "[_" + str("{:.2f}".format(size_KB)) + " KB_]"
                cadena = join(dir_path, cadena_actual)
                shutil.move(full_path, cadena)
                full_path = cadena
            if size_KB < 1:
                cadena_actual = dir1 + "[_" + str("{:.2f}".format(size)) + " B_]"
                cadena = join(dir_path, cadena_actual)
                shutil.move(full_path, cadena)
                full_path = cadena
            # Haciendo la llamada recursiva
            property_size(full_path)


# pase = None
while True:
    print("Entre la dir a modificar")
    dir_user = input()
    dir_true = isdir(dir_user)
    file_true = isfile(dir_user)

    #comprobando error de la cadena entrada
    while dir_true is not True and file_true is not True:
        print("Entre una direccion correcta")
        dir_user = input()
        dir_true = isdir(dir_user)
        file_true = isfile(dir_user)

    print("Entre C para cambiar el nombre de los ficheros")
    print("Entre B para borrar el directorio")
    print("Entre T para poner tamanno en el nombre")
    select = input()

    #comprobando error del caracter seleccionado
    while select.lower() != "c" and select.lower() != "b" and select.lower() != "t":
        print("Entre un caracter correcto")
        print("Entre C para cambiar el nombre de los ficheros")
        print("Entre B para borrar el directorio")
        print("Entre T para borrar el directorio")
        select = input()

    if select == "C" or select == "c":
        print_tree(dir_user)
        print("Se cambio el nombre de todos los archivos")

    if select == "B" or select == "b":
        eliminar_dir(dir_user)
        print("Se elimino el dir")
    if select == "T" or select == "t":
        property_size(dir_user)
        print("Se modifico el nombre del DIR con el tamanno ")

    print("Si desea salir presione la tecla ESPACIO y ENTER")
    pase = input()
    if pase == " ":
        break
    else:
        continue

# input()
