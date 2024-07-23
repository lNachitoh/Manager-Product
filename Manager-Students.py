
#Importamos la librerias necesarias para el programa
import json
from colorama import init, Fore
from utils.modules import *
init()

#Definimos las variables que van a contener la lista y el nombre del archivo [Mas abajo se personaliza el nombre del archivo.]


def menu():
    while True:
        global archivo 
        archivo = input("Nombre del archivo (sin extension): ") + ".json"
        archivo = f"./{archivo}"
        try:
            cargar_archivo()
            break
        except FileNotFoundError:
            print(Fore.RED + f"[!] El archivo {archivo} no fue encontrado. Intente de nuevo.")
        except json.JSONDecodeError:
            print(Fore.RED + "[!] El archivo no contiene un JSON valido. Intente de nuevo.")
        except Exception as e:
            print(Fore.RED + f"[!] Ocurrio un error: {e}. Intente de nuevo.")

    while True:
            print(Fore.RESET +'''
                ------------- Menu interactivo -------------
                1- Agregar estudiante
                2- Buscar estudiante por matricula
                3- Listar todos los estudiantes
                4- Eliminar estudiante
                5- Listar todos los estudiantes aprobados
                6- Promedio de notas y edad de todos los estudiantes
                7- Guardar archivo
                8- Salir
                ---------------------------------------------''')
            opcion = int(input("¿Que opcion te gustaria elegir? -> "))
            if opcion == 1:
                cargar_estuadiante()
            if opcion == 2:
                matricula = input("Matricula que deseas buscar -> ")
                buscar_estudiante_matricula(matricula)
            if opcion == 3:
                listar_estudiantes()
            if opcion == 4:
                matricula = input("Matricula que deseas eliminar -> ")
                eliminar_estudiante(matricula)
            if opcion == 5:
                listar_estudiantes_aprobados()
            if opcion == 6:
                calcular_promedio()
            if opcion == 7:
                guardar_archivo()
            if opcion == 8:
                opcion = input("Sino guardaste el archivo se perdera todo lo que has cargado. ¿Seguro quieres salir del programa? [Si/No] -> ")
                opcion.lower()
                if opcion == "si":                 
                    print(Fore.RED + "[!] Saliendo del programa....")
                    break
                if opcion == "no":
                    continue
                    


if __name__ == "__main__":
    menu()