#Fecha de creación: 17/05/2026
#Ultima actualización: 31/05/2026
#Documento de funciones

from datetime import datetime, date
from faker import Faker
import random
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

fake = Faker()

justificaciones = { #Razones de rechazo.
    1: "Portador de enfermedad infecciosa o crónica grave (VIH, Hepatitis, Tuberculosis, Diabetes insulinodependiente, etc.)",
    2: "Conducta de riesgo (nuevas parejas o relaciones sexuales por dinero/drogas en los últimos 3 meses)",
    3: "Factores de salud física (hemoglobina baja/alta, presión inestable, fiebre o infección reciente)",
    4: "Procedimiento médico reciente (transfusión, trasplante, cirugía mayor, tatuaje, piercing o endoscopía)",
    5: "Uso de medicamentos inyectables sin receta o fármacos restringidos",
    6: "Estilo de vida o viajes (drogas recreativas, alcohol en últimas 24h, viaje a zona endémica de malaria/dengue)",
    7: "Situación especial (embarazo, lactancia o menstruación activa)"
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
    except Exception: #Captura cualquier error.
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

def generarDonadores(cantidadDonadores, listaDonadores):
    """
    Genera donadores de forma aleatoria y los agrega a listaDonadores.
    """
    if cantidadDonadores <= 0:
        print("La cantidad de donadores debe ser mayor a 0.")
        return
    fechaHoy = date.today()

    for persona in range(cantidadDonadores):
        #Faker genera el nombre completo.
        nombre = fake.first_name()
        primerApellido = fake.last_name()
        segundoApellido = fake.last_name()
        nombreCompleto = [nombre, primerApellido, segundoApellido]
        #Se utiliza Random para generar el numero de cedula.
        codigoProvincia = random.randint(1, 7)
        numeroTomo = random.randint(1, 999)
        numeroAsiento = random.randint(1, 9999)
        cedula = f"{codigoProvincia}-{numeroTomo:04d}-{numeroAsiento:04d}"
        #Random elige el índice de tiposSangre
        indiceTipoSangre = random.randint(0, len(tiposSangre) - 1)
        #Random elige entre True (Masculino) y False (Femenino)
        esMasculino = random.choice([True, False])
        #Faker genera la fecha de nacimiento directamente respetando los rangos de edad indicados
        fechaNacimientoObj = fake.date_of_birth(minimum_age=10, maximum_age=80)  #Fecha entre 10 y 80 años
        fechaNacimiento = (fechaNacimientoObj.day, fechaNacimientoObj.month, fechaNacimientoObj.year) #Convertir a tupla (DD, MM, AAAA)
        #Faker genera un float con rango y decimales específicos.
        pesoKg = fake.pyfloat(min_value=30, max_value=150, right_digits=1) #Peso entre 30.0 y 150.0 kg
        #Random genera un número de telefono
        digitosPermitidosInicio = [2, 4, 6, 7, 8, 9]
        primerDigitoTelefono = random.choice(digitosPermitidosInicio)
        digitosRestantes = random.randint(0, 9999999)
        telefonoRaw = f"{primerDigitoTelefono}{digitosRestantes:07d}" 
        telefono = f"{telefonoRaw[:4]}-{telefonoRaw[4:]}"
        #Faker genera el correo
        dominiosValidos = ["gmail.com", "costarricense.cr", "racsa.go.cr", "ccss.sa.cr"]
        nombreUsuario = fake.user_name()
        dominioElegido = random.choice(dominiosValidos)
        correo = f"{nombreUsuario}@{dominioElegido}"
        #Calcular edad exacta considerando si ya pasó el cumpleaños este año.
        yaCumplioAnios = (fechaHoy.month, fechaHoy.day) >= (fechaNacimientoObj.month, fechaNacimientoObj.day)
        edadActual = fechaHoy.year - fechaNacimientoObj.year - (0 if yaCumplioAnios else 1)
        estadoDonador = 1 
        justificacionDonador = 0
        if edadActual < 18 or edadActual > 70:
            #Edad fuera del rango permitido para donar
            estadoDonador = 0
            justificacionDonador = 3 #Justificación 3: factor de salud física
        elif pesoKg < 50:
            #Peso insuficiente para donar
            estadoDonador = 0
            justificacionDonador = 3 #Justificación 3: factor de salud física
        elif pesoKg > 120:
            #Sobrepeso que impide la donación
            estadoDonador = 0
            justificacionDonador = 3 #Justificación 3: factor de salud física
        else:
            #Apto físicamente, pero 30% de probabilidad de otra restricción.
            if random.random() < 0.30: #random genera probabilidad de ser no apto por otras razones.
                estadoDonador = 0
                justificacionDonador = random.randint(1, 7)
        nuevoDonador = [ #Construcción del donador.
            nombreCompleto,
            cedula,
            indiceTipoSangre,
            esMasculino,
            fechaNacimiento,
            pesoKg,
            correo,
            telefono,
            estadoDonador,
            justificacionDonador
        ]
        listaDonadores.append(nuevoDonador)
    return True

def actualizarDonador(cedula, nuevosDatos, listaDonadores):
    """
    Busca un donador por cédula en listaDonadores y actualiza sus datos.
    Si no existe, retorna False con un mensaje de error.
    Si existe, actualiza todos los campos excepto la cédula y retorna True.
    nuevosDatos es una lista con el mismo formato del donador, sin incluir la cédula.
    """
    #Buscar el donador recorriendo la lista completa.
    indiceEncontrado = -1
    for indice in range(len(listaDonadores)):
        if listaDonadores[indice][1] == cedula:#Comparar cédula en posición 1.
            indiceEncontrado = indice
            break #Detener búsqueda al encontrar el primer coincidente.
    if indiceEncontrado == -1:
        return False, f"La persona con el número de cédula: {cedula} no está registrado en la base de datos del Banco de Sangre aún."
    donadorActual = listaDonadores[indiceEncontrado]
    donadorActualizado = [
        nuevosDatos[0],
        donadorActual[1],
        nuevosDatos[1],
        nuevosDatos[2],
        nuevosDatos[3],
        nuevosDatos[4],
        nuevosDatos[5],
        nuevosDatos[6],
        donadorActual[8],
        donadorActual[9]
    ]
    listaDonadores[indiceEncontrado] = donadorActualizado
    return True, "Datos actualizados correctamente."

def reporteDonantesProvinciaHTML(codigoProvincia, listaDonadores):
    """
    Genera un reporte HTML con los donantes activos de una provincia dada.
    Ordenados por nombre completo.
    """
    #Diccionario con los nombres de las provincias según su código numérico
    nombresProvincia = {
        1: "San José",
        2: "Alajuela",
        3: "Cartago",
        4: "Heredia",
        5: "Guanacaste",
        6: "Puntarenas",
        7: "Limón"
    }
    #Filtrar donantes activos cuyo primer dígito de cédula coincida con la provincia
    donantesFiltrados = []
    for donador in listaDonadores:
        cedulaProvincia = int(donador[1][0]) 
        esActivo        = donador[8] == 1 

        if cedulaProvincia == codigoProvincia and esActivo:
            donantesFiltrados.append(donador)
    #Ordenar por nombre completo
    donantesFiltrados.sort(key=lambda d: f"{d[0][0]} {d[0][1]} {d[0][2]}")
    #Fecha y hora del sistema en formato legible
    fechaHora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    provincia = nombresProvincia.get(codigoProvincia, "Desconocida")
    titulo    = f"Donantes Activos de la Provincia de {provincia}"
    #Construir las filas de la tabla HTML recorriendo los donantes filtrados
    filas = ""
    for donador in donantesFiltrados:
        nombreCompleto = f"{donador[0][0]} {donador[0][1]} {donador[0][2]}"
        cedula = donador[1]
        fechaNac = f"{donador[4][0]:02d}/{donador[4][1]:02d}/{donador[4][2]}"
        telefono = donador[7]
        correo = donador[6]
        filas += f"""
        <tr>
            <td>{cedula}</td>
            <td>{nombreCompleto}</td>
            <td>{fechaNac}</td>
            <td>{telefono}</td>
            <td>{correo}</td>
        </tr>"""
    #Si no hay donantes se muestra un mensaje en lugar de una tabla vacía
    filasFinales = filas if donantesFiltrados else '<tr><td colspan="5" class="sinDatos">No hay donantes activos registrados para esta provincia.</td></tr>'
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
            {filasFinales}
        </tbody>
    </table>
</body>
</html>"""
    try:
        nombreArchivo = f"reporte_donantes_{provincia.lower().replace(' ', '_')}.html"
        with open(nombreArchivo, "w", encoding="utf-8") as archivo:
            archivo.write(html)
        return True
    except Exception:
        return False
    
def reporteTipoSangreProvinciaHTML(indiceTipoSangre, codigoProvincia, listaDonadores):
    """
    Genera un reporte HTML con los donantes activos de un tipo de sangre
    y provincia específicos. Pensado para emergencias donde se necesita
    localizar donadores que puedan donar de inmediato.
    """
    #Diccionario con los nombres de las provincias según su código numérico.
    nombresProvincia = {
        1: "San José",
        2: "Alajuela",
        3: "Cartago",
        4: "Heredia",
        5: "Guanacaste",
        6: "Puntarenas",
        7: "Limón"
    }
    #Obtener el nombre legible del tipo de sangre usando el índice en la tupla global.
    nombreTipoSangre = tiposSangre[indiceTipoSangre]
    #Obtener el nombre de la provincia, "Desconocida" si el código no existe.
    provincia = nombresProvincia.get(codigoProvincia, "Desconocida")
    #Filtrar donantes que cumplan las tres condiciones: provincia, tipo de sangre y activo.
    donantesFiltrados = []
    for donador in listaDonadores:
        cedulaProvincia = int(donador[1][0]) 
        esMismaProvincia = cedulaProvincia == codigoProvincia
        esMismoTipoSangre = donador[2] == indiceTipoSangre 
        esActivo = donador[8] == 1
        if esMismaProvincia and esMismoTipoSangre and esActivo:
            donantesFiltrados.append(donador)
    #Obtener fecha y hora actual del sistema para el encabezado del reporte.
    fechaHora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    #Título que incluye tipo de sangre y provincia.
    titulo = f"Donantes Activos con Sangre {nombreTipoSangre} en {provincia}"
    #Construir las filas de la tabla HTML recorriendo los donantes filtrados.
    filas = ""
    for donador in donantesFiltrados:
        nombreCompleto = f"{donador[0][0]} {donador[0][1]} {donador[0][2]}"
        cedula = donador[1]
        fechaNacimiento = f"{donador[4][0]:02d}/{donador[4][1]:02d}/{donador[4][2]}"
        telefono = donador[7]
        correo = donador[6]
        filas += f"""
        <tr>
            <td>{cedula}</td>
            <td>{nombreCompleto}</td>
            <td>{fechaNacimiento}</td>
            <td>{telefono}</td>
            <td>{correo}</td>
        </tr>"""
    #Si la lista está vacía se muestra un mensaje en lugar de una tabla vacía.
    filasFinales = filas if donantesFiltrados else f'<tr><td colspan="5" class="sinDatos">No hay donantes activos con sangre {nombreTipoSangre} en {provincia}.</td></tr>'
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
            {filasFinales}
        </tbody>
    </table>
</body>
</html>"""
    try:
        nombreArchivo = f"reporte_sangre_{nombreTipoSangre.replace('+', 'pos').replace('-', 'neg')}_{provincia.lower().replace(' ', '_')}.html"
        with open(nombreArchivo, "w", encoding="utf-8") as archivo:
            archivo.write(html)
        return True
    except Exception:
        return False
    
def reporteMujeresDonanteONegativoHTML(listaDonadores):
    """
    Genera un reporte HTML con las mujeres donantes activas de tipo O-,
    menores de 45 años, ordenadas por edad.
    """
    #Indice de O- en la tupla global tiposSangre = 1
    indiceONegativo = tiposSangre.index("O-")
    #Fecha actual para calcular edades
    fechaHoy = datetime.now()
    #Filtrar mujeres activas con sangre O- y menores de 45 años.
    donantesFiltradas = []
    for donador in listaDonadores:
        esMujer = donador[3] == False
        esONegativo = donador[2] == indiceONegativo
        esActiva = donador[8] == 1
        if esMujer and esONegativo and esActiva:
            #Calcular edad exacta considerando si ya pasó el cumpleaños este año.
            yaCumplioAnios = (fechaHoy.month, fechaHoy.day) >= (donador[4][1], donador[4][0])
            edadActual = fechaHoy.year - donador[4][2] - (0 if yaCumplioAnios else 1)
            if edadActual < 45: #Solo menores de 45 años
                donantesFiltradas.append((donador, edadActual))#Guardar tupla (donador, edad) para ordenar.
    #Ordenar por edad de menor a mayor.
    donantesFiltradas.sort(key=lambda d: d[1])
    #Fecha y hora del sistema para el encabezado del reporte.
    fechaHora = fechaHoy.strftime("%d/%m/%Y %H:%M:%S")
    titulo = "Mujeres Donantes con Sangre O- Menores de 45 Años"
    #Construir las filas de la tabla HTML recorriendo las donantes filtradas.
    filas = ""
    for donador, edad in donantesFiltradas:
        nombreCompleto = f"{donador[0][0]} {donador[0][1]} {donador[0][2]}"
        cedula = donador[1]
        fechaNacimiento = f"{donador[4][0]:02d}/{donador[4][1]:02d}/{donador[4][2]}"
        telefono = donador[7]
        correo = donador[6]
        filas += f"""
        <tr>
            <td>{cedula}</td>
            <td>{nombreCompleto}</td>
            <td>{fechaNacimiento}</td>
            <td>{telefono}</td>
            <td>{correo}</td>
        </tr>"""
    #Si la lista está vacía se muestra un mensaje en lugar de una tabla vacía.
    filasFinales = filas if donantesFiltradas else '<tr><td colspan="5" class="sinDatos">No hay mujeres donantes O- menores de 45 años registradas.</td></tr>'
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
            {filasFinales}
        </tbody>
    </table>
</body>
</html>"""
    try:
        with open("reporte_mujeres_o_negativo.html", "w", encoding="utf-8") as archivo:
            archivo.write(html)
        return True
    except Exception:
        return False
    
def reporteDeQuienPuedeRecibirHTML(indiceTipoSangre, listaDonadores):
    """
    Genera un reporte HTML con los donantes activos que pueden donar
    al tipo de sangre indicado, agrupados por provincia descendentemente.
    """
    #Diccionario con los nombres de las provincias según su código numérico
    nombresProvincia = {
        1: "San José",
        2: "Alajuela",
        3: "Cartago",
        4: "Heredia",
        5: "Guanacaste",
        6: "Puntarenas",
        7: "Limón"
    }
    #Tabla de compatibilidad: clave = índice del receptor, valor = lista de índices de donantes compatibles
    compatibilidad = {
        0: [0, 1], #O+  recibe de: O+, O-
        1: [1], #O-  recibe de: O-
        2: [0, 1, 2, 3], #A+  recibe de: O+, O-, A+, A-
        3: [1, 3], #A-  recibe de: O-, A-
        4: [0, 1, 4, 5], #B+  recibe de: O+, O-, B+, B-
        5: [1, 5], #B-  recibe de: O-, B-
        6: [0, 1, 2, 3, 4, 5, 6, 7],  # AB+ recibe de: todos
        7: [1, 3, 5, 7] #AB- recibe de: O-, A-, B-, AB-
    }
    #Obtener el nombre legible del tipo de sangre receptor
    nombreTipoSangreReceptor = tiposSangre[indiceTipoSangre]
    #Obtener los índices de los tipos de sangre que pueden donar al receptor
    indicesCompatibles = compatibilidad[indiceTipoSangre]
    #Filtrar donantes activos cuyo tipo de sangre sea compatible con el receptor
    donantesFiltrados = []
    for donador in listaDonadores:
        esCompatible = donador[2] in indicesCompatibles
        esActivo     = donador[8] == 1
        if esCompatible and esActivo:
            donantesFiltrados.append(donador)
    #Agrupar donantes por código de provincia
    donantesPorProvincia = {}
    for donador in donantesFiltrados:
        codigoProvincia = int(donador[1][0])
        if codigoProvincia not in donantesPorProvincia:
            donantesPorProvincia[codigoProvincia] = []
        donantesPorProvincia[codigoProvincia].append(donador)
    #Ordenar las provincias descendentemente
    provinciaOrdenadas = sorted(donantesPorProvincia.keys(), reverse=True)
    #Fecha y hora del sistema para el encabezado del reporte
    fechaHora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    titulo = f"Donantes que Pueden Donar a Sangre {nombreTipoSangreReceptor}"
    #Construir las filas agrupadas por provincia en orden descendente
    filas = ""
    for codigoProvincia in provinciaOrdenadas:
        nombreProv = nombresProvincia.get(codigoProvincia, "Desconocida")
        #Fila de encabezado de provincia dentro de la tabla
        filas += f"""
        <tr class="filaProvincia">
            <td colspan="5">{nombreProv}</td>
        </tr>"""
        for donador in donantesPorProvincia[codigoProvincia]:
            nombreCompleto = f"{donador[0][0]} {donador[0][1]} {donador[0][2]}"
            cedula = donador[1] 
            nombreTipoSangre = tiposSangre[donador[2]]
            telefono = donador[7]
            correo = donador[6]
            filas += f"""
        <tr>
            <td>{cedula}</td>
            <td>{nombreCompleto}</td>
            <td>{nombreTipoSangre}</td>
            <td>{telefono}</td>
            <td>{correo}</td>
        </tr>"""
    #Si no hay donantes compatibles se muestra un mensaje
    filasFinales = filas if donantesFiltrados else f'<tr><td colspan="5" class="sinDatos">No hay donantes compatibles con sangre {nombreTipoSangreReceptor}.</td></tr>'
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
        .filaProvincia {{background-color: #e0e0e0; font-weight: bold;}}
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
                <th>Tipo de Sangre</th>
                <th>Teléfono</th>
                <th>Correo</th>
            </tr>
        </thead>
        <tbody>
            {filasFinales}
        </tbody>
    </table>
</body>
</html>"""
    try:
        nombreArchivo = f"reporte_puede_recibir_{nombreTipoSangreReceptor.replace('+', 'pos').replace('-', 'neg')}.html"
        with open(nombreArchivo, "w", encoding="utf-8") as archivo:
            archivo.write(html)
        return True
    except Exception:
        return False
    
def reporteLugaresDonacionHTML(listaDonadores, diccionarioLugares):
    """
    Genera un reporte HTML con las provincias ordenadas ascendentemente
    según el Registro Civil del Tribunal Supremo de Elecciones, mostrando
    la cantidad de donadores registrados (activos e inactivos) y los
    recintos posibles de recaudación por provincia.
    """
    #Provincias ordenadas ascendentemente según el Registro Civil del TSE (1 al 7)
    nombresProvincia = {
        1: "San José",
        2: "Alajuela",
        3: "Cartago",
        4: "Heredia",
        5: "Guanacaste",
        6: "Puntarenas",
        7: "Limón"
    }
    #Contar donadores (activos e inactivos) por provincia usando el primer dígito de la cédula
    contadorPorProvincia = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0}
    for donador in listaDonadores:
        codigoProvincia = int(donador[1][0]) #Primer dígito de cédula = código de provincia
        if codigoProvincia in contadorPorProvincia:
            contadorPorProvincia[codigoProvincia] += 1 #Contar sin importar el estado
    #Fecha y hora del sistema para el encabezado del reporte
    fechaHora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    titulo = "Lugares de Donación por Provincia"
    #Construir filas ordenadas ascendentemente por código de provincia (1 → 7)
    filas = ""
    for codigoProvincia in sorted(nombresProvincia.keys()):
        nombreProv = nombresProvincia[codigoProvincia]
        cantidadDonadores = contadorPorProvincia.get(codigoProvincia, 0)
        lugares = diccionarioLugares.get(codigoProvincia, [])
        recintos = "<br>".join(lugares) if lugares else "Sin recintos registrados"
        filas += f"""
        <tr>
            <td>{nombreProv}</td>
            <td>{cantidadDonadores}</td>
            <td>{recintos}</td>
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
        td {{padding: 8px 10px; border-bottom: 1px solid #ddd; vertical-align: top;}}
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
                <th>Provincia</th>
                <th>Cantidad de Donadores Registrados (Activos e Inactivos)</th>
                <th>Recintos Posibles de Recaudación</th>
            </tr>
        </thead>
        <tbody>
            {filas}
        </tbody>
    </table>
</body>
</html>"""
    try:
        with open("reporte_lugares_donacion.html", "w", encoding="utf-8") as archivo:
            archivo.write(html)
        return True
    except Exception:
        return False
