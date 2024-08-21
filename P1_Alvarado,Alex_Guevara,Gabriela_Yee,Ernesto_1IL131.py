import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox as mb
import matplotlib.pyplot as plt

#Texto de los botones de la ventana
botones = ['           Algoritmo DDA para dibujar líneas           ','       Algoritmo de Bresenham para dibujar líneas      ',
           '    Algoritmo de punto medio para la circunferencia    ','        Algoritmo de punto medio para la elipse        ',
           '                 Presentación formal                   ', '                        Salir                         ', 
           '                     Regresar                          ']
#Creación de la ventana principal
root = tk.Tk()
root.title("Proyecto N1 - HCG - AGY")
root.geometry('800x300+200+200')

#Algoritmos de funcionamiento
def dda_linea (xi, yi, xf, yf, valor):
  #obtencion de los diferenciales
  dx = xf - xi
  dy = yf - yi
  #si delta de x es distinto de 0 entoces dy/dx sino 0
  m = dy/dx if dx != 0 else 0.0
  pointx = [xi]
  pointy = [yi]
  #los pasos para controlara el for
  steps = abs(dx) if dx >= dy else abs(dy)
  #pendient de x o y, mejora el rendiemiento para el dda - izq a der y dda - der a izq
  slope = 1 if valor==True else -1
  for n in range(steps):
    if m <= 1.0:
      xi = xi + slope
      yi = yi + slope * m
    else:
      xi = xi + slope / m
      yi = yi + slope
    pointx.append(round(xi))
    pointy.append(round(yi))
  return pointx, pointy

def bresenham_linea(xi, yi, xf, yf):
    #valor absoluto de dx y dy
    dx = abs(xf - xi)
    dy = abs(yf - yi)
    #si x inicial es mayor que x final entonces se reduce en 1, de igual forma se aplica en y
    slope_dx = 1 if xi < xf else -1
    slope_dy = 1 if yi < yf else -1
    #Se realiza un control de los datos cuando la pendiende sea menor a 1 y mayor que -1
    p  = 2 * dy - dx if dx > dy else 2 * dx - dy
    inc1 = 2 * dy if dx > dy else 2 * dx
    inc2 = 2 * (dy - dx) if dx > dy else 2 * (dx - dy)
    pointx = [xi]
    pointy = [yi]
    #cuando la pendiende sea menor a 1 y sea mayor a -1
    if dx > dy:
        while xi != xf:
            xi += slope_dx
            if p < 0:
                p += inc1
            else:
                yi += slope_dy
                p += inc2
            pointx.append(xi)
            pointy.append(yi)
    #la pendiente es mayor que 1 o menor a -1
    else:
        while yi != yf:
            yi += slope_dy
            if p < 0:
                p += inc1
            else:
                xi += slope_dx
                p += inc2
            pointx.append(xi)
            pointy.append(yi)
    return pointx, pointy

def circunferencia (xc, yc, r):
  x = 0
  y = r
  p = 1 - r
  puntosx = []
  puntosy = []
  while x <= y:
    #q1
    puntosx.append(xc + x); puntosy.append(yc + y)
    #q2
    puntosx.append(xc - x); puntosy.append(yc + y)
    #q3
    puntosx.append(xc + y); puntosy.append(yc + x)
    #q4
    puntosx.append(xc - y); puntosy.append(yc + x)
    #q5
    puntosx.append(xc + y); puntosy.append(yc - x)
    #q6
    puntosx.append(xc - y); puntosy.append(yc - x)
    #q7
    puntosx.append(xc + x); puntosy.append(yc - y)
    #q8
    puntosx.append(xc - x); puntosy.append(yc - y)
    #Optencion de pk y valores x, y
    if p < 0:
      p += 2 * x + 3
    else:
      p += 2 * (x - y) + 5
      y -= 1
    x += 1
  return puntosx, puntosy

def elipse(rx, ry, xc, yc):
  x0 = 0
  y0 = ry
  r2y = ry**2
  r2x = rx**2
  p = r2y - r2x * ry + 0.25 * r2x
  puntosx = []
  puntosy = []
  #bucle que controla el primer sub cuadrante de la elipse
  while 2 * r2y * x0 < 2 * r2x * y0:
    #q1
    puntosx.append(xc + x0); puntosy.append(yc + y0)
    #q2
    puntosx.append(xc - x0); puntosy.append(yc + y0)
    #q3
    puntosx.append(xc + x0); puntosy.append(yc - y0)
    #q4
    puntosx.append(xc - x0); puntosy.append(yc - y0)
    #Optencion de pk y valores x, y
    if p < 0:
      p += 2 * r2y * (x0 + 1) + r2y
    else:
      p += 2 * r2y * (x0 + 1) + r2y - 2 * r2x * (y0 - 1)
      y0 -= 1
    x0 += 1
  #segundo pk para el sub cuadrante de la elipse
  p2 = r2y * (x0 + 0.5)**2 + r2x * (y0 - 1)**2 - r2x * r2y
  #bucle que controla el segundo sub cuadrante de la elipse y se maneja hasta que y sea igual a 0
  while y0 >= 0:
    p#q10
    puntosx.append(xc + x0); puntosy.append(yc + y0)
    #q2
    puntosx.append(xc - x0); puntosy.append(yc + y0)
    #q3
    puntosx.append(xc + x0); puntosy.append(yc - y0)
    #q4
    puntosx.append(xc - x0); puntosy.append(yc - y0)
    #Optencion de pk2 y valores x, y
    if p2 < 0:
      p2 += 2 * r2y * (x0 + 1) - 2 * r2x * (y0 - 1) + r2x
      x0 += 1
    else:
      p2 += -2 * r2x * (y0 - 1) + r2x
    y0 -= 1
  return puntosx, puntosy

#Funcion para la creación automatica de botones del menu principal
def crearboton(titulo,i,j, ejecucion):
    boton_practica = tk.Button(root, text=titulo, command = ejecucion)
    boton_practica.pack()
    boton_practica.place(x=i, y=j)
#Funcion para la creacion de texto dentro de la ventana
def etiqueta(titulo,ventana):
    etiquetas = tk.Label(ventana, text=titulo, font=('Times New Roman', 12))
    etiquetas.pack()
#Creación de la ventana para obtencion de los parametros de cada uno de los algoritmos de trazado de líneas, circulos y elipses
def ventana(apli,titulo,x,y,titulo2,xff,control,yff,pos):
    vn = tk.Toplevel()
    vn.geometry("700x320")
    vn.title(apli)
    etiqueta("Ingrese los parametros requeridos para el correcto funcionamiento del algoritmo.\n\nSolo se permiten números ENTEROS",vn)
    etiqueta("\n"+titulo,vn)
    cajax = tk.Entry(vn); cajax.place(x=100, y=80); cajax.pack()
    xi = tk.Label(vn, text=x); xi.place(x=200, y=80); xi.pack()

    cajay = tk.Entry(vn); cajay.place(x=100, y=95); cajay.pack()
    yi = tk.Label(vn, text=y); yi.place(x=380, y=95); yi.pack()

    final = tk.Label(vn, text=titulo2,font=('Times New Roman', 12)); final.place(x=200, y=100); final.pack();
    cajaxf = tk.Entry(vn); cajaxf.place(x=100, y=120); cajaxf.pack()
    xf = tk.Label(vn, text=xff); xf.place(x=380, y=120); xf.pack()

    if control == True:
        cajayf = tk.Entry(vn); cajayf.place(x=100, y=140); cajayf.pack()
        yf = tk.Label(vn, text=yff); yf.place(x=380, y=140); yf.pack()
        subir = tk.Button(vn, text='Aceptar', command=lambda: verificar(pos,vn,cajax.get(),cajay.get(),cajaxf.get(),cajayf.get()))
        subir.pack()
    else: 
        subir = tk.Button(vn, text='Aceptar', command=lambda: verificar(pos,vn,cajax.get(),cajay.get(),cajaxf.get(),'0'))
        subir.pack()
#Funcion para validar los datos ingresados sean numeros enteros
def verificar(pos,cerrar,xi,yi,xf_rx,yf_ry):
    control = True
    datos = [xi.strip(),yi.strip(),xf_rx.strip(),yf_ry.strip()]
    for dat in datos:
        try:
            int(dat)
        except:
            mb.showerror("Error",(dat+" no es un valor entero"))
            control = False
            break
    if control == True:
        mb.showinfo("Información","Se han verificado todos los datos correctamente")
        cerrar.destroy()
        #Una vez verificados los datos, se pasa al envío de otra función para que se evalueen los algoritmos
        enviar(pos,datos)
        return True
    else:
        return False
#Función para obtener los resultados respectivos de cada algoritmo
def enviar(pos,datos):
    valor = True
    x = int(datos[0]);y = int(datos[1]);xf = int(datos[2]);yf = int(datos[3]);
    s = 4000
    datosx = []
    datosy = []

    if pos == 0:
        #ejecucion del programa
        #VERDADERO SI ES DE IZQUIERDA A DERECHA, FALSO DE DERECHA A IZQUIERDA
        respuesta = mb.askquestion("Algoritmo DDA", "DETERMINE:\nIzquierda a Derecha (SI) \nDerecha a Izquierda(NO)")
        #SI EL USUARIO NO INGRESA SU RESPUESTA, SE ASUME COMO TRUE
        if respuesta == 'yes':
            valor = True
        elif respuesta == 'no':
            valor = False
        datosx, datosy = dda_linea(x, y, xf, yf, valor)
    elif pos == 1:
        datosx, datosy = bresenham_linea(x, y, xf, yf)
    elif pos == 2:
        datosx, datosy = circunferencia(x, y, xf)
        s=2000
        datosx.append(x)
        datosy.append(y)
    else:
        datosx, datosy = elipse(xf, yf, x, y)
        s=2000
        datosx.append(x)
        datosy.append(y)
    #Enviar los resultados obtenidos para la creación de la gráfica
    resul(pos,datosx,datosy,s)
#Funcion para la impresión de la gráfica resultante de los algoritmos
def resul(pos,x,y,s):
    plt.figure("Resultados", figsize=(9,7))
    plt.style.use('ggplot')
    plt.title(botones[pos])
    plt.xlabel('Valores en X')
    plt.ylabel('Valores en Y')
    plt.scatter(x=x, y=y, s=s,marker='s', color='#0DC18D', label='Cuadrados')
    #Coordenadas
    for i in range(len(x)):
        plt.text(x[i], y[i], f'({x[i]},{y[i]})', fontsize=9, verticalalignment='bottom')
    plt.show()
#Impresión de la portada en una ventana distinta de la principal
def presentacion():
    vn = tk.Toplevel()
    vn.geometry("700x400")
    vn.title("Presentación Formal")
    etiqueta("UNIVERSIDAD TECNOLÓGICA DE PANAMÁ\nFACULTAD DE INGENIERÍA DE SISTEMAS COMPUTACIONALES"+
             "\nDEPARTAMENTO DE COMPUTACIÓN Y SIMULACIÓN DE SISTEMAS\nASIGNATURA: HERRAMIENTAS DE COMPUTACIÓN GRÁFICA"+
             "\n\nTEMA:\nPROYECTO N1\n\nINTEGRANTES: \nALVARADO ALEX, 8-998-934\nGUEVARA GABRIELA, 8-1005-662\nYEE ERNESTO, 8-963-608"+
             "\n\nFACILITADOR:\nING. MARK TACK\n\nFECHA: \n06/05/2024", vn)
#Funcion para salir del programa
def salir():
   root.destroy()
   mb.showinfo("Información","Ha salido del programa\nHasta pronto \\'o'/")
#Creación de los botones para el menu principal
crearboton(botones[0],120,100, lambda:ventana(botones[0],'Puntos iniciales','Xi','Yi','Puntos finales','Xf',True,'Yf',0))
crearboton(botones[1],420,100, lambda:ventana(botones[1],'Puntos iniciales','Xi','Yi','Puntos finales','Xf',True,'Yf',1))
crearboton(botones[2],100,140, lambda:ventana(botones[2],'Centros','Xc','Yc','Radio','R',False,'',2))
crearboton(botones[3],420,140, lambda:ventana(botones[3],'Centros','Xc','Yc','Radio','Rx',True,'Ry',3))
crearboton(botones[4],130,180, lambda:presentacion())
crearboton(botones[5],460,180, lambda:salir())
etiqueta("BIENVENIDO \\'o'/\nPROYECTO N1 - HCG - AGY\n\n\nSELECCIONE UNA DE LAS OPCIONES DEL MENU --->", root)
#Este es el bucle para que se muestre la pantalla
root.mainloop()