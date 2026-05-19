#Fecha de creación: 17/05/2026
#Ultima actualización: 17/05/2026
#Documento de funciones

from datetime import date
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
    except FileNotFoundError: #Si no existe el archivo significa que es la primera ejecución. Se retornan las estructuras iniciales vacías o con datos por defecto.
        return [], lugaresDonacion, False

def reporteDonantesProvinciaHTML(codigoProvincia):
    """
    Genera un reporte HTML con los donantes activos de una provincia dada.
    Ordenados por nombre completo.
    """
    nombresProvincia = {
        1: "San José",
        2: "Alajuela",
        3: "Cartago",
        4: "Heredia",
        5: "Guanacaste",
        6: "Puntarenas",
        7: "Limón"
    }
    #Filtrar donantes activos de la provincia indicada
    donantesFiltrados = []
    for donador in baseDatos:
        cedulaProvincia = int(donador[1][0])  #Primer dígito de la cédula = código de provincia
        if cedulaProvincia == codigoProvincia and donador[8] == 1:  # activo
            donantesFiltrados.append(donador)
    #Ordenar por apellido1, apellido2, nombre
    donantesFiltrados.sort(key=lambda d: (d[0][1], d[0][2], d[0][0]))
    fechaHora = date.today().strftime("%d/%m/%Y")
    provincia = nombresProvincia.get(codigoProvincia, "Desconocida")
    titulo = f"Donantes Activos de la Provincia de {provincia}"
    #Construcción de las filas
    filas = ""
    for donador in donantesFiltrados:
        nombre = f"{donador[0][0]} {donador[0][1]} {donador[0][2]}"
        cedula = donador[1]
        fechaNac = f"{donador[4][0]:02d}/{donador[4][1]:02d}/{donador[4][2]}"
        telefono = donador[7]
        correo = donador[6]
        #f""" inicia un f-string multilínea, permite escribir el HTML en múltiples líneas y usar variables de Python con {variable} directamente en el string.
        filas += f"""
        <tr>
            <td>{cedula}</td>
            <td>{nombre}</td>
            <td>{fechaNac}</td>
            <td>{telefono}</td>
            <td>{correo}</td>
        </tr>"""

    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="utf-8" />
    <title>{titulo}</title>
    <style>
        body {{font-family: Arial, sans-serif; margin: 40px; background-color: #f9f9f9; color: #222;}}
        h1 {{color: #b30000; text-align: center;}}
        p {{text-align: center; color: #555;}}
        table {{width: 100%; border-collapse: collapse; margin-top: 20px; background-color: #fff;}}
        th {{background-color: #b30000; color: white; padding: 10px; text-align: left;}}
        td {{padding: 8px 10px; border-bottom: 1px solid #ddd;}}
        tr:hover {{background-color: #f1f1f1;}}
        .sinDatos {{text-align: center; color: #888; padding: 20px;}}
    </style>
</head>
<body>
    <h1>{titulo}</h1>
    <p>Fecha y hora de generación: {fechaHora}</p>
    <table>
        <thead>
            <tr>
                <th>Cédula</th>
                <th>Nombre Completo</th>
                <th>Fecha de Nacimiento</th>
                <th>Teléfono</th>
                <th>Correo</th>
            </tr>
        </thead>
        <tbody>
            {"".join(filas) if donantesFiltrados else '<tr><td colspan="5" class="sinDatos">No hay donantes activos registrados para esta provincia.</td></tr>'}
        </tbody>
    </table>
</body>
</html>"""
    try:
        nombreArchivo = f"reporte_donantes_{provincia.lower().replace(' ', '_')}.html"
        with open(nombreArchivo, "w", encoding="utf-8") as archivo: #Guardar el archivo en la carpeta actual con codificación UTF-8.
            archivo.write(html)
        return True
    except Exception:
        return False