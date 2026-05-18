#Fecha de creación: 17/05/2026
#Ultima actualización: 17/05/2026
#Documento de funciones

import pickle

tiposSangre = ("O+", "O-", "A+", "A-", "B+", "B-", "AB+", "AB-") #Tupla de tipos de sangre.

#Diccionario con los códigos de las provincias y las listas con los hospitales.
lugaresDonacion = {
    1: ["El Banco Nacional de sangre","Hospital México","Hospital San Juan de Dios"], #San José
    2: ["Hospital San Rafael de Alajuela","Hospital de San Ramón","Hospital del Cantón Norteño"], #Alajuela
    3: ["Hospital Max Peralta"], #Cartago
    4: ["Hospital San Vicente de Paúl"], #Heredia
    5: ["Hospital La Anexión en Nicoya","Hospital Enrique Baltodano de Liberia"], #Guanacaste
    6: ["Hospital Monseñor Sanabria"], #Puntarenas
    7: ["Hospital Tony Facio","Hospital de Guápiles"] #Limón
}

baseDatos = []

def guardarDatos(nombreArchivo):
    """
    Guarda la baseDatos y lugaresDonacion en disco
    usando Pickle para mantener las estructuras exactas.
    """
    try:
        with open(nombreArchivo, "wb") as archivoBinario: #Abre el archivo en modo escritura binaria, "wb" es requerido por Pickle para escribir estructuras.
            pickle.dump({"baseDatos": baseDatos, "lugaresDonacion": lugaresDonacion}, archivoBinario)  #Empaqueta ambas estructuras en un diccionario.
        return True
    except FileNotFoundError:
        return False
    
def cargarDatos(nombreArchivo):
    """
     Carga los datos del archivo .pkl a las estructuras en RAM.
    """
    try:
        with open(nombreArchivo, "rb") as archivoBinario: #Abre el archivo en modo lectura binaria, "rb" es requerido por Pickle para leer estructuras.
            datosGuardados = pickle.load(archivoBinario) #Desempaqueta el diccionario guardado previamente.
            #Extrae cada estructura por su llave.
            return datosGuardados["baseDatos"], datosGuardados["lugaresDonacion"], True
    except FileNotFoundError:# Si no existe el archivo significa que es la primera ejecución. Se retornan las estructuras iniciales vacías o con datos por defecto.
        return [], lugaresDonacion, False
    
