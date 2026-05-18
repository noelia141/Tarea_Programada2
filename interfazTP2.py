#Fecha de creación: 17/05/2026
#Ultima actualización: 17/05/2026
#Interfaz gráfica con la utilización de tkinter

#Importación de librerías
import tkinter as tk
from tkinter import messagebox

nombreArchivo = "" #Variable global que almacenará el nombre del archivo.

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

donadores = {} #Diccionario donde se guardarán los donadores registrados.

def verificarArchivoExistente(nombreArchivo):
    """
    Función auxiliar para verificar la existencia del archivo.
    Intenta abrir el archivo especificado por el usuario en modo lectura.
    """
    try:
        with open(nombreArchivo, "r") as archivo:
            return True
    except FileNotFoundError:
        return False
    
class InterfazBancoSangre:
    def __init__(self, root):
        """
        Recibe la ventana raíz de Tkinter y 
        configura el inicio de la interfaz.
        """
        self.root = root 
        self.root.title("Sistema de Banco de Sangre") #Define el título de la ventana.
        self.root.geometry("450x550") #Define las dimensiones de la ventana principal.
        self.crearInterfaz()
        self.solicitarArchivo()

        def solicitarArchivo(self):
            """
            Crea una ventana flotante que le pide al usuario
            ingresar el nombre del archivo.
            """
            self.ventanaArchivo = tk.Toplevel(self.root) #Crea la ventana secundaria vinculada a la principal.
            self.ventanaArchivo.title("Cargar Base de Datos")
            self.ventanaArchivo.geometry("380x180")
            self.ventanaArchivo.grab_set() #Bloquea los clics en la ventana principal, por lo que fuerza el enfoque en esta ventana.
            #Etiqueta de bienvenida e instrucciones.
            tk.Label(self.ventanaArchivo, text = "Bienvenido al Sistema de Banco de Sangre", font = ("Arial", 11, "bold")).pack(pady = 10)
            tk.Label(self.ventanaArchivo, text = "Ingrese el nombre del archivo de datos:").pack(pady=2)
            #Componente de entrada de texto donde el usuario digita el nombre del archivo
            self.nombreArchivo = tk.Entry(self.ventanaArchivo, width = 35)
            self.nombreArchivo.pack(pady = 5)
            #Botón que al darle click ejecutar la función encargada de procesar el texto ingresado.
            botonAceptar = tk.Button(self.ventanaArchivo, text = "Cargar", width = 20, command = self.procesarArchivo)
            botonAceptar.pack(pady = 15)

        """
        Sin terminar.
        Sigue la creación de la función para procesar el archivo.
        """