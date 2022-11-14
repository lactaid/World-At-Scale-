import numpy as np  # operaciones matematicas
import time  # eventos relacionados a tiempo
import cmath  # en el caso de las raices cuadradas, nos permite regresar valores imaginarios


import cv2  # nos permite trabajar con imagenes y modificarlas

from tkinter import *  # esto nos permite hacer aplicaciones
from tkinter import filedialog
import tkinter as tk
import os  # nos permite acceder al file explorer

# PIL SIEMPRE DEBE IR DESPUES DE TKINTER, YA QUE TIENE SU PROPIA FUNCION IMAGE QUE REEMPLAZA A LA DE PIL
# Pillow, nos permite trabajar con imagenes
from PIL import Image, ImageFont, ImageDraw, ImageTk


'''
Funcionamiento basico:
- Seleccionar los puntos A B C y D dentro de la imagen, haciendo clic para asignar cada uno, basarse en la posicion del cursor, no lo que muestra la pantalla, 
porque este ultimo no es 100% exacto.
- Una vez seleccionados los 4, presionar esc o cerra la ventana.
- Cuando esto suceda, el programa calculara las coordenadas junto con el ratio
-El programa volvera a abrir la imagen, esta vez con los resultados en pantalla.

'''

'''
Mejoras a futuro:
-Hacer que el programa funcione dentro de una app de tkinter
-Poder utilizar el ratio obtenido dentro de otras operaciones

'''

'''
Hacer que el resize dependa de la resolucion de la imagen
'''

img_path = ""  # aqui se guarda el path que donde el usuario elige su propia imagen, su funcionamiento se ve en la funcion de calcular


def imgRatio(img_path):
    print("-"*100)
    print("\nWorld At Scale 1.0\n")
    print("-"*100)
    xc = []  # lista de coordenadas x
    yc = []  # lista de coordenadas en y
    print("Coordenadas originales: ")

    def mousePoints(event, x, y, flags, params):
        font = cv2.FONT_HERSHEY_SIMPLEX
        if event == cv2.EVENT_LBUTTONDOWN:  # funcion de cv2 para detectar input de mouse
            print(x, y)  # imprimimos las coordenadas obtenidas
            xc.append(x)  # agregamos la coordenada a la lista de xc y yc
            yc.append(y)
            if len(xc) == 1:  # se despliega el nombre de la coordenada dependiendo de que tantos elementos esten en la lista xc, una vez que supera 4, ya no se toma en cuenta
                cv2.putText(img, 'A', (x, y), font, 1, (255, 249, 0), 2)

            elif len(xc) == 2:
                cv2.putText(img, 'B', (x, y), font, 1, (255, 249, 0), 2)

            elif len(xc) == 3:
                cv2.putText(img, 'C', (x, y), font, 1, (255, 249, 0), 2)

            elif len(xc) == 4:
                cv2.putText(img, 'D', (x, y), font, 1, (255, 249, 0), 2)

            else:
                cv2.putText(img, '.', (x, y), font, 1, (255, 249, 0), 3)
            # creamos una nueva imagen con la tag de img
            # AQUI SE GUARDA LA NUEVA IMAGEN
            cv2.imwrite('medidor_objetos/recursos/new.jpg', img)
            # mostramos el resultado al finalizar cada instancia
            cv2.imshow('image', img)

    # img ahora vale la imagen original
    # abrimos la imagen

    img = cv2.imread(img_path)

    # img = cv2.resize(im, (960, 540))  # hacemos resize leer arriba !!!!!!!!!

    # mostramos la imagen original, con el nombre image
    cv2.imshow('image', img)
    # llamamos al la funcion de cv2 setMouseCallback con image y mousePoints
    cv2.setMouseCallback("image", mousePoints)

    cv2.waitKey(0)  # espera al input del usuario para terminar

    # encontrar el centro
    # usamosla libreria Image, parte de Pillow, y la funcion Image.open para abrir la imagen original
    image = Image.open('medidor_objetos/recursos/new.jpg')
    # en image,size se alamacenan las medidas de la imagen en una lista, basta con dividir ambas /2 para encontrar el centro
    centroX = image.size[0]/2
    centroY = image.size[1]/2
    print('size: ', image.size)  # ver tamaño original
    print('coords: ', centroX, centroY)  # ver la posicion xy del centro
    print("-"*100)
    for i in range(len(xc)):  # el valor de las coordenadas ahora se basa en el centro
        xc[i] = xc[i] - centroX

    for i in range(len(yc)):
        yc[i] = yc[i] - centroY

    print(xc, yc)  # comprobamos los nuevos valores de xc y yc

    # Ratio
    ax = xc[0]
    ay = yc[0]
    bx = xc[1]
    by = yc[1]
    cx = xc[2]
    cy = yc[2]
    dx = xc[3]
    dy = yc[3]
    #C = np.array([[bx,cx,dx], [by,cy,dy], [1,1,1]])
    # print(np.linalg.det(C))
    A = np.array([[1.0, 0, -bx, 0, 0, 0], [0, 1, -by, 0, 0, 0], [0, 0, 0, 1, 0, -cx],
                  [0, 0, 0, 0, 1, -cy], [1, 0, -dx, 1, 0, -dx], [0, 1, -dy, 0, 1, -dy]])  # A
    b = np.array([[bx-ax], [by-ay], [cx-ax], [cy-ay], [dx-ax], [dy-ay]])  # B

    M = np.append(A, b, 1)  # M
    print("Matriz original\n", M)
    n = M.shape[0]

    for i in range(0, n-1):
        if M[i, i] == 0:
            for k in range(i+1, n):
                if M[k, i] != 0:
                    aux = np.copy(M[k, :])
                    M[k, :] = np.copy(M[i, :])
                    M[i, :] = np.copy(aux)
        Piv = M[i, i]  # Pivote
        RP = M[i, :]  # Vector Renglon
        CP = M[:, i]  # Vector columna

        for j in range(i+1, n):
            M[j, :] = M[j, :] - RP*CP[j] / Piv

    #print("\n Matriz gauss simple ")
    # print(M)

    xS = np.zeros((n, 1))  # Vector solución
    aux = n-1  # Auxiliar

    for i in range(n-1, -1, -1):
        x = 0
        for j in range(n-1, aux, -1):
            x += M[i, j]*xS[j]

        xS[i] = np.around((M[i, n] - x) / M[i, i],
                          decimals=2)  # [1,xS[i+1],xS[i]]
        aux -= 1

    #print("\nVector solución\n", np.around(xS, decimals = 10))

    l = cmath.sqrt((-xS[0]*xS[3]-xS[1]*xS[4]) / (xS[2]*xS[5]))
    print("l = ", l)
    ux = xS[0]
    print("ux: ", ux)
    uy = xS[1]
    print("uy: ", uy)
    uz = xS[2]*l
    print("uz: ", uz)
    vx = xS[3]
    print("vx: ", vx)
    vy = xS[4]
    print("vy: ", vy)
    vz = xS[5]*l
    print("vz: ", vz)

    u = cmath.sqrt(ux**2+uy**2+uz**2)
    v = cmath.sqrt(vx**2+vy**2+vz**2)

    # en casos donde el resultado del ratio sea nan o 0, regresamos false al usuario para que se pueda repetir el ciclo
    if np.isnan((v/u).real) or (v/u).real == 0.00:
        success = False
        font = cv2.FONT_HERSHEY_TRIPLEX
        img = cv2.rectangle(img, (8, 470), (813, 508), (0, 0, 0), -1)
        cv2.putText(img, 'Error, por favor presiona esc para reiniciar ',
                    (10, 500), font, 1, (0, 0, 255), 2)

        cv2.imshow('image', img)
        cv2.waitKey(0)\

    else:
        ratio = ("%.2f" % (v/u).real)  # si no hay errores, mostamos el ratio
        font = cv2.FONT_HERSHEY_TRIPLEX
        print("Ratio: ", ratio)  # para que imprima el numero real
        img = cv2.rectangle(img, (8, 470), (199, 511), (0, 0, 0), -1)
        cv2.putText(img, 'Ratio: '+str(ratio),
                    (10, 500), font, 1, (0, 0, 255), 2)

        cv2.imshow('image', img)  # mostramos el resultado
        cv2.waitKey(0)

        success = True  # regresamos true

    return success


def calcular():
    global img_path  # accedemos al poth
    img_path = filedialog.askopenfilename(initialdir=os.getcwd(), title=" Open Text File", filetypes=[
                                          ("Image Files", "*.jpg *.gif *.jpg *.png *.jpeg")])  # esto permite que el usuario utilice sus propias imagenes
    repetir = True
    while repetir == True:
        if imgRatio(img_path):  # accedemos a la funcion de imgRatio usando el path anterior
            print("-"*100)  # si regresa true, no hubo error y no se repite
            print("Exito")
            repetir = False
        else:  # si regresa false, hubo un error y se repite
            print("Hubo un error, intenta otra vez por favor")
            repetir = True

# ==============MAIN==============


root = Tk()  # app tkinter
root.title("World At Scale")  # titulo
root.geometry("500x750")  # tamaño
root.configure(background='#3d3d3b')  # Color de fondo

lab1 = Label(root, text="World At Scale", font=(
    "courier", 19, "bold"), fg='white', bg='#3d3d3b')
lab1.place(relx=0.5, rely=0.06, anchor=CENTER)  # Titulo

# imagen con las instrucciones
label_image = Label(root, text='', bg='#3d3d3b')

# abrimos la imagen con las instrucciones
inst = Image.open('medidor_objetos/recursos/Instrucciones_img.png')
inst = ImageTk.PhotoImage(inst)
label_image['image'] = inst  # mostramos la imagen
# inst.close()


btn = Button(root, text="Seleccionar Imagen", fg='white', bg='#5300A8', highlightthickness=5, borderwidth=5,
             relief=RIDGE, height=1, width=12, font=("normal", 13), padx=15, pady=1, command=calcular)  # creamos un boton que inicie la funcion de calcular

# placement del boton de calcular
btn.pack(side='left', anchor='s', expand=True)
label_image.place(relx=0.5, rely=0.5, anchor=CENTER)  # placement de la imagen

root.mainloop()  # esto es necesario para ejecutar el tkinter