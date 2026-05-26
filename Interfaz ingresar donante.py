import tkinter#Importar las librerias
import re
tipoSangre = ("O+","O-","A+","A-","B+","B-","AB+","AB-")
listaDonadores = []
#Funciones(si se puede ponerlos en un .py separado para no contaminar tanto visualmente el codigo.)
def verificarCedula(cedula):
    return re.match(r"^[1-9]-\d{4}-\d{4}$", cedula) != None

def registrarDonador():#Función que verifica los datos ingresados, en caso de que todo este bien, ingresa al donador a la lista.
    cedula = textoCedula.get()
    nombre = textoNombreCompleto.get()
    fecha = textoFechaNacimiento.get()
    tipoSangre = textoTipo.get()
    sexo = textoSexo.get()
    peso = textoPeso.get()
    telefono = textoTelefono.get()
    correo = textoCorreo.get()

    if not verificarCedula(cedula):#Concretar las demas condicionales y poner luego información de inserción
        print("Cédula no válida. Debe tener el formato X-XXXX-XXXX, donde X es un dígito.")
        return
    donadorRegistrar = [
        cedula,
        nombre,
        fecha,
        tipoSangre,
        sexo,
        peso,
        telefono,
        correo
    ]
    listaDonadores.append(donadorRegistrar)
    print(listaDonadores)
def limpiar():#Limpia las caracteristicas hasta que deja el espacio en 0 caracteristicas, y el .set es para que el selector del tipo de sangre vuelva a su estado incial.
    textoCedula.delete(0,tkinter.END)
    textoNombreCompleto.delete(0,tkinter.END)
    textoFechaNacimiento.delete(0,tkinter.END)
    textoPeso.delete(0,tkinter.END)
    textoTelefono.delete(0,tkinter.END)
    textoCorreo.delete(0,tkinter.END)
    textoTipo.set("Escoja su tipo de sangre.")
#Ventana emergente para registrar los datos
ventana=tkinter.Tk()
ventana.title("Donador")#Nombre y tamaño de la ventana
ventana.geometry("400x250")
#Cada texto y su respectivo espacio para escribirlo
tkinter.Label(ventana, text="Cédula: ").grid(row=0, column=0)
textoCedula = tkinter.Entry(ventana)
textoCedula.grid(row=0, column=1)
#Nombre del donador
tkinter.Label(ventana,text="Nombre Completo: ").grid(row=1, column=0)
textoNombreCompleto = tkinter.Entry(ventana)
textoNombreCompleto.grid(row=1, column=1)
#Fecha de nacimiento
tkinter.Label(ventana,text="Fecha de nacimiento: ").grid(row=2, column=0)
textoFechaNacimiento = tkinter.Entry(ventana)
textoFechaNacimiento.grid(row=2, column=1)
#Tipo de sangre
tkinter.Label(ventana,text="Tipo de sangre: ").grid(row=3, column=0)
textoTipo = tkinter.StringVar()
textoTipo.set("Escoja su tipo de sangre.")
menuTipo = tkinter.OptionMenu(ventana,textoTipo,*tipoSangre)
menuTipo.grid(row=3,column=1)
#Sexo del donador
tkinter.Label(ventana,text="Sexo: ").grid(row=4, column=0)
textoSexo = tkinter.Variable()
textoSexo.set(True)
tkinter.Radiobutton(ventana,text="Masculino",variable=textoSexo,value=True).grid(row=4, column=1)
tkinter.Radiobutton(ventana,text="Femenino",variable=textoSexo,value=False).grid(row=4, column=2)
#Peso del donador
tkinter.Label(ventana,text="Peso en KG: ").grid(row=5, column=0)
textoPeso = tkinter.Entry(ventana)
textoPeso.grid(row=5, column=1)
#Telefono
tkinter.Label(ventana,text="Teléfono: ").grid(row=6, column=0)
textoTelefono = tkinter.Entry(ventana)
textoTelefono.grid(row=6, column=1)
#Correo
tkinter.Label(ventana,text="Correo: ").grid(row=7, column=0)
textoCorreo = tkinter.Entry(ventana)
textoCorreo.grid(row=7, column=1)
#Botones
botonRegistrar = tkinter.Button(ventana, text="Registrar", command=registrarDonador)
botonRegistrar.grid(row=8, column=0)
botonRegistrar = tkinter.Button(ventana, text="Limpiar", command=limpiar)
botonRegistrar.grid(row=8, column=1)
botonRegistrar = tkinter.Button(ventana, text="Regresar")#Poner luego un command
botonRegistrar.grid(row=8, column=2)
ventana.mainloop()