import numpy as np  # operaciones matematicas
import time  # eventos relacionados a tiempo
import cmath  # en el caso de las raices cuadradas, nos permite regresar valores imaginarios
# Pillow, nos permite trabajar con imagenes
from PIL import Image, ImageFont, ImageDraw
import cv2  # nos permite trabajar con imagenes y modificarlas

# from tkinter import *
# from tkinter import filedialog
# import tkinter as tk
# ^ Todavia no se usan


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


def imgRatio():
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
            cv2.imwrite('new.jpg', img)
            # mostramos el resultado al finalizar cada instancia
            cv2.imshow('image', img)

    # img ahora vale la imagen original
    # abrimos la imagen
    img = cv2.imread('medidor objetos\images\minecraft 3.png')
    # img = cv2.resize(im, (960, 540))  # hacemos resize
    # mostramos la imagen original, con el nombre image
    cv2.imshow('image', img)
    # llamamos al la funcion de cv2 setMouseCallback con image y mousePoints
    cv2.setMouseCallback("image", mousePoints)

    cv2.waitKey(0)  # espera al input del usuario para terminar

    # encontrar el centro
    # usamosla libreria Image, parte de Pillow, y la funcion Image.open para abrir la imagen original
    image = Image.open('new.jpg')
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

    if np.isnan((v/u).real) or (v/u).real == 0.00:
        success = False
        font = cv2.FONT_HERSHEY_TRIPLEX
        img = cv2.rectangle(img, (8, 470), (813, 508), (0, 0, 0), -1)
        cv2.putText(img, 'Error, por favor presiona esc para reiniciar ',
                    (10, 500), font, 1, (0, 0, 255), 2)

        cv2.imshow('image', img)
        cv2.waitKey(0)\

    else:
        ratio = ("%.2f" % (v/u).real)
        font = cv2.FONT_HERSHEY_TRIPLEX
        print("Ratio: ", ratio)  # para que imprima el numero real
        img = cv2.rectangle(img, (8, 470), (199, 511), (0, 0, 0), -1)
        cv2.putText(img, 'Ratio: '+str(ratio),
                    (10, 500), font, 1, (0, 0, 255), 2)

        cv2.imshow('image', img)
        cv2.waitKey(0)

        success = True

    return success


# ==============MAIN==============
repetir = True
while repetir == True:
    if imgRatio():
        print("-"*100)
        print("Exito")
        repetir = False
    else:
        print("Hubo un error, intenta otra vez por favor")
        repetir = True


# ====== Codigo viejo que probablemente ya no se necesite ======

# xc = []  # lista de coordenadas x, se asignaban antes de la funcion antes

# yc = []  # lista de coordenadas en y

# coord = {}

# funcion para cuando hacemos clic
# def mousePoints(event, x, y, flags, params):

#     font = cv2.FONT_HERSHEY_SIMPLEX
#     if event == cv2.EVENT_LBUTTONDOWN:  # funcion de cv2 para detectar input de mouse
#         print(x, y)  # imprimimos las coordenadas obtenidas
#         xc.append(x)  # agregamos la coordenada a la lista de xc y yc
#         yc.append(y)
#         if len(xc) == 1:  # se despliega el nombre de la coordenada dependiendo de que tantos elementos esten en la lista xc, una vez que supera 4, ya no se toma en cuenta
#             cv2.putText(img, 'A', (x, y), font, 1, (255, 249, 0), 2)

#         elif len(xc) == 2:
#             cv2.putText(img, 'B', (x, y), font, 1, (255, 249, 0), 2)

#         elif len(xc) == 3:
#             cv2.putText(img, 'C', (x, y), font, 1, (255, 249, 0), 2)

#         elif len(xc) == 4:
#             cv2.putText(img, 'D', (x, y), font, 1, (255, 249, 0), 2)

#         else:
#             cv2.putText(img, '.', (x, y), font, 1, (255, 249, 0), 3)
#         # creamos una nueva imagen con la tag de img
#         cv2.imwrite('new.jpg', img)
#         # mostramos el resultado al finalizar cada instancia
#         cv2.imshow('image', img)

# Todo el proceso en una sola funcion por el momento


# if np.isnan((v/u)):
#     print("Hubo un error, intenta otra vez por favor")
# else:
#     ratio = ("%.2f" % (v/u).real)
#     font = cv2.FONT_HERSHEY_TRIPLEX
#     print("Ratio: ", ratio)  # para que imprima el numero real
#     img = cv2.rectangle(img, (8, 470), (199, 511), (0, 0, 0), -1)
#     cv2.putText(img, 'Ratio: '+str(ratio), (10, 500), font, 1, (0, 0, 255), 2)

#     cv2.imshow('image', img)
#     cv2.waitKey(0)

# Version anterior del for
# for i in range(len(xc)):  # el valor de las coordenadas ahora se basa en el centro
#         if xc[i] >= centroX:
#             xc[i] = -(centroX - xc[i])
#         else:
#             xc[i] = xc[i] - centroX

#     for i in range(len(yc)):
#         if yc[i] >= centroY:
#             yc[i] = -(centroY - yc[i])
#         else:
#             yc[i] = yc[i] - centroY
