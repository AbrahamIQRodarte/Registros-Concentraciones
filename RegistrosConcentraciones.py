from tkinter import *
from tkinter import ttk, messagebox
from sqlite3 import *
import tkinter.scrolledtext as scrolledtext
import pyautogui
import numpy as np
from datetime import date, datetime
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from matplotlib import pyplot as plt

#Funciones de la ventana home
def coneccion_bd(sql, parametros=()):
	global cursor, coneccion
	coneccion=connect("database/database.db")
	cursor=coneccion.cursor()
	cursor.execute(sql, parametros)
	coneccion.commit()
def R():
    temp=float(TEMP.get())
    pe=float(PE.get())

    #tabla de datos
    T_Lista=[20,40,60,80,100]
    Conc_list=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33]
    PE_20=[1.0072,1.0163,1.0254,1.0345,1.0437,1.0529,1.0622,1.0715,1.0809,1.0903,1.0999,1.1096,1.1194,1.1292,1.139,1.149,1.159,1.1594,1.1796,1.1898,1.2003,1.2108,1.2214,1.232,1.2429,1.2538,1.2647,1.2756,1.2869,1.2979,1.3092,1.3206,1.3319]
    PE_40=[1.001,1.0098,1.0187,1.0276,1.0367,1.0458,1.0549,1.064,1.0733,1.0826,1.0819,1.1013,1.1109,1.1205,1.1302,1.1399,1.1499,1.1599,1.17,1.1801,1.1905,1.2009,1.2114,1.2219,1.2327,1.2435,1.2543,1.2652,1.2762,1.2873,1.2986,1.3099,1.3212]
    PE_60=[0.9919,1.0005,1.0092,1.018,1.0269,1.0358,1.0448,1.0538,1.063,1.0722,1.0814,1.0906,1.1002,1.1098,1.1194,1.129,1.139,1.149,1.159,1.169,1.1794,1.1898,1.2002,1.2106,1.2214,1.2322,1.243,1.2538,1.2648,1.2759,1.2872,1.2985,1.3098]
    PE_80=[0.9803,0.9899,0.9981,1.0063,1.0151,1.024,1.0329,1.0418,1.051,1.0602,1.0694,1.0786,1.0882,1.0978,1.1074,1.117,1.127,1.137,1.147,1.157,1.1674,1.1778,1.1882,1.1986,1.2104,1.2202,1.231,1.2418,1.2529,1.264,1.2753,1.2866,1.2979]
    PE_100=[0.967,0.9756,0.9843,0.9931,1.0021,1.0111,1.0201,1.0291,1.0384,1.0477,1.057,1.0663,1.0759,1.0855,1.0952,1.1049,1.1149,1.1249,1.135,1.145,1.1555,1.1659,1.1764,1.1869,1.1977,1.2085,1.2193,1.2301,1.2411,1.2522,1.2635,1.2748,1.2861]
    T=temp
    P=pe
    PEi_Lista=[]
    for p in range(33):
        PEV_Lista=[PE_20[p],PE_40[p],PE_60[p],PE_80[p],PE_100[p]]
        j = InterNewton(T_Lista, PEV_Lista, T)   
        PEi_Lista.append(j)    
    VPE, VC= Vectores(PEi_Lista, Conc_list, P)
    Rei= VC[1]+(P-VPE[1])*((VC[2]-VC[1])/(VPE[2]-VPE[1]))
    Re= "{:.2f}".format(Rei)
    Ye.delete(0, END)
    Ye.insert(0,Re)
def guardar_datos():
    today=date.today()
    now = datetime.now()

    dia = str(today.day)
    mes = str(today.month)
    año = str(today.year)
    hora= str(now.hour)
    minuto = str(now.minute)
    Fecha = dia + " / " + mes + " / " + año + " --> " + hora + ":" + minuto	
    if len(TEMP.get())==0 or len(PE.get())==0:
        messagebox.showwarning(message="No puede dejar campos en blanco", title="Error")
    else:

        sql="INSERT INTO algoritmos VALUES(NULL,?,?,?,?)"
        Resultados = "Temperatura = "+ TEMP.get()+ " °C" + '\n' + "Peso específico = " + PE.get() + '\n' + "Concentración de Carbonato = " +var.get()+ " %"  + '\n' + "Observación: " + observacion.get()
        conc= var.get()
        fechadia=today
        parametros=(Fecha, Resultados, conc, fechadia)
        coneccion_bd(sql, parametros)
        messagebox.showinfo(message="Datos guardados correctamente", title="Exito")
        llenar_lista()

#Funciones Ventana lista
def llenar_lista():
	elementos_tabla= titulos.get_children()
	for elemento in elementos_tabla:
		titulos.delete(elemento)

	sql="SELECT id, titulo, Concentracion, Fecha FROM algoritmos"		
	parametros=()
	coneccion_bd(sql, parametros)
	datos=cursor.fetchall()
	cont=0			
	for fila in datos:
		titulos.insert("", END, text=datos[cont][0], values=(datos[cont][1],))
		cont+=1
def mostrar_contenido(event):
	try:
		text_titulos.delete(1.0, END)
		titulos.selection()[0]
		id_algoritmo=titulos.item(titulos.selection())['text']
		sql = "SELECT texto FROM algoritmos WHERE id = ?"
		parametros= (id_algoritmo,)
		coneccion_bd(sql,parametros)
		datos=cursor.fetchall()	
		text_titulos.insert(1.0, datos[0][0])	
	except IndexError as e:
		messagebox.showwarning(message="No ha seleccionado ningún item", title="Error")



def eliminar_texto():
	try:
		titulos.selection()[0]
		id_algoritmo=titulos.item(titulos.selection())['text']
		desicion=messagebox.askyesno(message="Si elimina un item, no hay forma de recuperar la información.\n ¿Desea Continuar?")
		if desicion:
			sql = "DELETE FROM algoritmos WHERE id = ?"
			parametros= (id_algoritmo)
			coneccion_bd(sql,parametros)
			llenar_lista()
		else:
			pass		
	except IndexError as e:
		messagebox.showwarning(message="No ha seleccionado ningún item", title="Error")

#Graficar datos
def Graficar(event):
    sql = "SELECT Concentracion, Fecha FROM algoritmos WHERE id = ?"
    

        
root=Tk()
#Imágenes

#Ventanas
root.geometry("700x600")
root.title("Libro de concentraciones K2CO3")
pestañas=ttk.Notebook(root, height=800, width=700)
pestañas.pack()
home = Frame(pestañas, bg="#003f6f")
lista = Frame(pestañas)
acerca= Frame(pestañas)
tabla= Frame(pestañas)
grafica= Frame(pestañas)
pestañas.add(home, text="Cálculo de concentración")
pestañas.add(lista, text="Registros")
pestañas.add(tabla, text="  Tabla  ")
pestañas.add(grafica, text="  Gráfica  ")
pestañas.add(acerca, text="Acerca de")

#ventana home
def Vectores(xData,yData,x_int):
    i=0
    Lon = len(xData)
    for x in xData:
        if x_int <= x:
            if i==1 or x <= xData[0]:
                xint=[xData[0],xData[1],xData[2], xData[3]]
                yint=[yData[0],yData[1],yData[2], yData[3]]
                break
            if i==Lon-1:
                xint=[xData[Lon-4],xData[Lon-3],xData[Lon-2],xData[Lon-1]]
                yint=[yData[Lon-4],yData[Lon-3],yData[Lon-2], yData[Lon-1]]
                break
            xint=[xData[i-2], xData[i-1],xData[i], xData[i+1]]
            yint=[yData[i-2], yData[i-1],yData[i], yData[i+1]]
            break
        i=i+1
    if x_int >= xData[-1]:
        xint=[xData[Lon-4],xData[Lon-3],xData[Lon-2],xData[Lon-1]]
        yint=[yData[Lon-4],yData[Lon-3],yData[Lon-2], yData[Lon-1]]
    return xint, yint

        #Interpolación de Newton
def InterNewton(x,y,xint):
    n = len(x)
    a = np.zeros(n)
    difDiv = np.zeros((n-1,n-1))

    a[0] = y[0]
    #Comienza la tabla de diferencias divididas
    for i in range(0,n-1):
        try:
            difDiv[i,0] = (y[i+1]-y[i])/(x[i+1]-x[i])
        except ZeroDivisionError:
            difDiv[i,0] = (y[i+1]-y[i])/0.000000001
            print("Varios valores en el eje x son iguales")
    for j in range(1,n-1):
        for i in range(0,n-j-1):
            difDiv[i,j] = (difDiv[i+1, j-1]- difDiv[i,j-1])/(x[j+i+1]-x[i])
    for i in range(1, n):
        a[i] = difDiv[0,i-1]
    #Evaluar el Polinomio
    yint = a[0]
    prodx = 1
    for l in range(1,n):
        prodx = prodx*(xint-x[l-1])
        yint = yint + a[l]*prodx
    return yint




temp=StringVar()
pe=StringVar()
var=StringVar()
observacion=StringVar() 
def clr():
    try:
        temp.set("")
        pe.set("")
        var.set("")
    except ValueError:
        pass



miFrame=Frame(home, height=80, width=400, bg="white")
miFrame.place( x=190 ,y=50)
a=3
titulo=Label(miFrame, text="Ejemplo")
titulo.grid(row=0, column=1, padx=a, pady=a)
datos=Label(miFrame, text="Datos")
datos.grid(row=0, column=2, padx=a, pady=a)
ejemplot=Label(miFrame, text="80 ")
ejemplot.grid(row=1, column=1, padx=a, pady=a)
ejemplope=Label(miFrame, text="1.1370")
ejemplope.grid(row=2, column=1, padx=a, pady=a)
ejemploc=Label(miFrame, text="18.00")
ejemploc.grid(row=4, column=1, padx=a, pady=a)
temperatura=Label(miFrame, text="Temperatura: ")
temperatura.grid(row=1, column=0, padx=a, pady=a, sticky="e")
unidad1=Label(miFrame, text="  °C  ")
unidad1.grid(row=1, column=3, padx=a, pady=a)
unidad2=Label(miFrame, text="  %  ")
unidad2.grid(row=4, column=3, padx=a, pady=a)
unidad3=Label(miFrame, text="  %  ")
unidad3.grid(row=4, column=3, padx=a, pady=a)



peso=Label(miFrame, text="Peso específico: ")
peso.grid(row=2, column=0, padx=a, pady=a)

TEMP=Entry(miFrame, textvariable=temp, width=6)
TEMP.grid(row=1, column=2)
TEMP.config(justify="right")

PE=Entry(miFrame, textvariable=pe, width=6)
PE.grid(row=2, column=2)
PE.config(justify="right")
 
resultado=Label(miFrame, text="Resultado:")
resultado.grid(row=3, column=2, padx=a, pady=a)

conc=Label(miFrame, text="Concentración: ")
conc.grid(row=4, column=0, padx=a, pady=a)


Ye=Entry(miFrame, textvariable=var, borderwidth=5, width=6)
Ye.grid(row=4, column=2, sticky="e", padx=a, pady=a)
Ye.config(bg="Black", fg="White")

botonCalcular=Button(miFrame, text="Calcular", command=R)
botonCalcular.grid(row=5, column=1, sticky="e", padx=a, pady=a)

botonLimpiar=Button(miFrame, text="Limpiar", command=clr)
botonLimpiar.grid(row=5, column=2, sticky="e", padx=a, pady=a)



third_frame_inicio=Frame(home, height=20, width=400)
third_frame_inicio.place(x=150, y=300)

tipo=Label(third_frame_inicio, text="Observación: ")
tipo.pack()
obs=Entry(third_frame_inicio, textvariable=observacion, width=40)
obs.pack()
boton_guardar=Button(third_frame_inicio, text="Guardar", bg="green", fg="black", command=guardar_datos, width=50, borderwidth=5)
boton_guardar.pack()

#Ventana lista


princ_frame_lista=LabelFrame(lista, height=500)
princ_frame_lista.place(x=10, y=30)
label_lista_titulos=Label(princ_frame_lista, text="Fecha  -->   Hora", bg="#003f6f", fg="white")
label_lista_titulos.pack()
scroll_y=ttk.Scrollbar(princ_frame_lista)
scroll_y.pack(side=LEFT, fill=Y)
scroll_x=ttk.Scrollbar(princ_frame_lista, orient=HORIZONTAL)
scroll_x.pack(side=BOTTOM, fill=X)
titulos= ttk.Treeview(princ_frame_lista, yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set, height=21)
titulos["columns"]=("one")
titulos.heading('#0', text = '', anchor = CENTER)
titulos.column("#0",stretch=YES, width=0)
titulos.heading('#1', text = '', anchor = "w")
titulos.column("#1",stretch=YES, minwidth=400)
titulos.pack()
titulos.bind("<<TreeviewSelect>>", mostrar_contenido)
scroll_y.config(command=titulos.yview)
scroll_x.config(command=titulos.xview)
second_frame_lista=Frame(lista, bg="#003f6f")
second_frame_lista.place(x=241, y=30)
label_texto_lista=Label(second_frame_lista, text="Datos de la muestra", bg="#003f6f", fg="white")
label_texto_lista.pack()
text_titulos=scrolledtext.ScrolledText(second_frame_lista, height=29, width=60)
text_titulos['font'] = ('Arial', '10')
text_titulos.pack()
boton_eliminar=Button(lista, text="Eliminar Entrada", fg="black", command=eliminar_texto)
boton_eliminar.place(x=75, y=530)
llenar_lista()
# ventana Tabla

imagen=PhotoImage(file="images/Fondo.png")
fondotabla=Label(tabla,image=imagen).place(x=0, y=0)

#Ventana Gráfica


fig = Figure(figsize=(5,4), dpi=100)

canvas = FigureCanvasTkAgg(fig, master=grafica)
canvas.draw()
canvas.get_tk_widget().pack()
boton_graficar=Button(grafica, text="Graficar", fg="black", command= Graficar)
boton_graficar.pack()
toolbar = NavigationToolbar2Tk(canvas, grafica)
toolbar.update()
canvas.get_tk_widget().pack()




#Ventana Acerca de
princ_frame_acerca=LabelFrame(acerca, height=500)
princ_frame_acerca.place(x=10, y=50)
i1 = "Programa terminado el  Sábado 10 de Julio del 2020" + "\n"
i2 = "Autor: Abraham Rodarte de la Fuente"+ "\n"
i3 = "El programa interpola el valor de la concentración de carbonato de potasio" + "\n" 
i4 = "a partir de los datos obtenidos de temperatura y peso específico." + "\n" 
i5 = "Para realizar el tratamiento matemático se realiza una serie de Interpolaciones" + "\n"
i6 = "de Newton tomando los pesos especificos y las temperaturas como referencias" + "\n"
i7 = "para después realizar una interpolación lineal entre la concentración y el " + "\n"
i8 = "peso específico. Los datos son tomados de la tabla que se le proporcionó a la planta."
informacion = i1 + i2 + i3 + i4 + i5 + i6 + i7 + i8 + "\n" "Correo electrónico: abraham_luffy36@outlook.es"+ "\n" + "Télefono: 464 117 0091"
label_texto_acerca=Label(princ_frame_acerca, text=informacion, bg="white", fg="Black", font=("Arial", 11))
label_texto_acerca.config(justify="left", relief="sunken")
label_texto_acerca.pack()

root.mainloop()
