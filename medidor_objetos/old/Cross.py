import numpy as np  # operaciones matematicas
import time  # eventos relacionados a tiempo
import cmath  # en el caso de las raices cuadradas, nos permite regresar valores imaginarios
# Pillow, nos permite trabajar con imagenes
from PIL import Image, ImageFont, ImageDraw
import cv2  # nos permite trabajar con imagenes y modificarlas

# from tkinter import *
# from tkinter import filedialog
# import tkinter as tk
# Todavia no se usan


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
    img = cv2.imread('medidor_objetos\images\minecraft.jpg')

    # img = cv2.resize(im, (750, 1333))  # hacemos resize
    # mostramos la imagen original, con el nombre image
    cv2.imshow('image', img)
    # llamamos al la funcion de cv2 setMouseCallback con image y mousePoints
    cv2.setMouseCallback("image", mousePoints)

    cv2.waitKey(0)  # espera al input del usuario para terminar

    # encontrar el centro
    # usamosla libreria Image, parte de Pillow, y la funcion Image.open para abrir la imagen original
    image = Image.open('medidor_objetos\images\minecraft.jpg')
    # en image,size se alamacenan las medidas de la imagen en una lista, basta con dividir ambas /2 para encontrar el centro
    centroX = image.size[0]/2
    centroY = image.size[1]/2
    print('size: ', image.size)  # ver tamaño original
    print('coords: ', centroX, centroY)  # ver la posicion xy del centro
    print("-"*100)
    for i in range(len(xc)):  # el valor de las coordenadas ahora se basa en el centro
        if xc[i] >= centroX:
            xc[i] = np.abs(xc[i] - centroX)
        else:
            xc[i] = -np.abs(xc[i] - centroX)

    for i in range(len(yc)):
        if yc[i] >= centroY:
            yc[i] = -np.abs(yc[i] - centroY)
        else:
            yc[i] = np.abs(yc[i] - centroY)

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
    CrossRatio(xc, yc, centroX, centroY, (v/u).real)
    return success


# Calcula la distancia a una ventana con respecto a los bordes de la estructura principal
def CrossRatio(xc, yc, centroX, centroY, ratio):
    # Para seleccionar los 4 puntos de la ventana
    print("-"*100)
    print("\nDistancia a objeto\n")
    print("-"*100)
    px = []
    py = []

    def mousePoints2(event, x, y, flags, params):
        font = cv2.FONT_HERSHEY_SIMPLEX
        if event == cv2.EVENT_LBUTTONDOWN:  # funcion de cv2 para detectar input de mouse
            print(x, y)  # imprimimos las coordenadas obtenidas
            px.append(x)  # agregamos la coordenada a la lista de xc y yc
            py.append(y)
    cv2.setMouseCallback("image", mousePoints2)
    cv2.waitKey(0)  # espera al input del usuario para terminar
    # Estos son los cuatro vértices de la estructura principal, se añade una tercera dimensión en "z" = 1
    P1 = np.array([xc[0], yc[0], 1])  # Bottom left
    P2 = np.array([xc[1], yc[1], 1])  # Bottom right
    P3 = np.array([xc[2], yc[2], 1])  # Upper left
    P4 = np.array([xc[3], yc[3], 1])  # Upper right
    print(P1, P2, P3, P4)
    # Se calculan cuatro rectas de la estructura principal, el formato es [ax, by, c] = 0
    L1 = np.cross(P1, P3)  # Linea vertical izquierda
    L2 = np.cross(P2, P4)  # Linea vertical derecha
    L3 = np.cross(P3, P4)  # Linea horizontal superior
    L4 = np.cross(P1, P2)  # Linea horizontal inferior

    for i in range(len(px)):  # El valor de las coordenadas con respecto al centro de la imagen
        if px[i] >= centroX:
            px[i] = np.abs(px[i] - centroX)
        else:
            px[i] = -np.abs(px[i] - centroX)

    for i in range(len(py)):
        if py[i] >= centroY:
            py[i] = -np.abs(py[i] - centroY)
        else:
            py[i] = np.abs(py[i] - centroY)
    # Estos son los cuatro vértices de la ventana, cartel, etc.
    p1 = np.array([px[0], py[0], 1])  # Bottom left
    p2 = np.array([px[1], py[1], 1])  # Bottom right
    p3 = np.array([px[2], py[2], 1])  # Upper left
    p4 = np.array([px[3], py[3], 1])  # Upper right
    # Se calculan cuatro rectas de la segunda estructura, el formato es [ax, by, c] = 0
    l1 = np.cross(p1, p3)  # Linea vertical izquierda
    l2 = np.cross(p2, p4)  # Linea vertical derecha
    l3 = np.cross(p3, p4)  # Linea horizontal superior
    l4 = np.cross(p1, p2)  # Linea horizontal inferior

    # Punto de horizonte, el formato del punto debe quedar [ax, by, 1]
    vph = np.cross(L3, L4)  # Horizontal
    vph = vph / vph[2]
    vpv = np.cross(L1, L2)  # Vertical
    vpv = vpv / vpv[2]

    # Intersecciones x
    # Nota: Todas las distancias se encuentran en función del tamaño horizontal
    # De igual forma la interpretación de las distancias dependerá de la localización del punto de horizonte
    print("\nDistancia Horizontal 1\n")
    C1 = np.cross(L3, l1)  # Punto de intersección
    C1 = C1 / C1[2]
    # Para calcular distancia entre dos puntos se usa esta función
    BD = np.linalg.norm(P3-P4)
    AC = np.linalg.norm(vph-C1)
    # Si el punto de horizonte se encuentra a la derecha
    if np.linalg.norm(vph-P4) < np.linalg.norm(vph-P3):
        BC = np.linalg.norm(C1-P4)
        AD = np.linalg.norm(vph-P3)
    else:  # Si el punto de horizonte se encuentra a la izquierda
        BC = np.linalg.norm(P3-C1)
        AD = np.linalg.norm(P3-vph)

    CR = (AC*BD) / (BC*AD)  # Cross ratio

    dist = 1 / CR  # Posteriormente se debe multiplicar este valor por el tamaño horizontal
    print(dist)

    print("\nDistancia Horizontal 2\n")
    C2 = np.cross(L3, l2)  # Punto de intersección
    C2 = C2 / C2[2]
    AC = np.linalg.norm(vph-C2)
    if np.linalg.norm(vph-P4) < np.linalg.norm(vph-P3):  # Punto de horizonte a la derecha
        BC = np.linalg.norm(C2-P4)
        AD = np.linalg.norm(vph-P3)
    else:  # Punto de horizonte a la izquierda
        BC = np.linalg.norm(P3-C2)
        AD = np.linalg.norm(P3-vph)

    CR = (AC*BD) / (BC*AD)  # Cross ratio

    dist = 1 / CR  # Posteriormente se debe multiplicar este valor por el tamaño horizontal
    print(dist)

    # Intersecciones y

    # De igual forma la interpretación de las distancias dependerá de la localización del punto de horizonte
    print("\nDistancia Vertical 1\n")
    C3 = np.cross(L1, l3)  # Punto de intersección
    C3 = C3 / C3[2]

    BD = np.linalg.norm(P1-P3)
    AC = np.linalg.norm(vpv-C3)
    # Si el punto de horizonte se encuentra abajo
    if np.linalg.norm(vpv-P1) < np.linalg.norm(vpv-P3):
        BC = np.linalg.norm(C3-P1)
        AD = np.linalg.norm(vpv-P3)
    else:  # Si el punto de horizonte se encuentra arriba
        BC = np.linalg.norm(P3-C3)
        AD = np.linalg.norm(P1-vpv)

    CR = (AC*BD) / (BC*AD)  # Cross ratio

    dist = ratio / CR  # Como está en función del tamaño horizontal, reemplazamos con el aspect ratio de la estructura original
    print(dist)
    print("\nDistancia Vertical 2\n")
    C4 = np.cross(L1, l4)  # Punto de intersección
    C4 = C4 / C4[2]
    AC = np.linalg.norm(vpv-C4)
    # Si el punto de horizonte se encuentra abajo
    if np.linalg.norm(vpv-P1) < np.linalg.norm(vpv-P3):
        BC = np.linalg.norm(C4-P1)
        AD = np.linalg.norm(vpv-P3)
    else:  # Si el punto de horizonte se encuentra arriba
        BC = np.linalg.norm(P3-C4)
        AD = np.linalg.norm(P1-vpv)

    CR = (AC*BD) / (BC*AD)  # Cross ratio

    dist = ratio / CR  # Como está en función del tamaño horizontal, reemplazamos con el aspect ratio de la estructura original
    print(dist)


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


# Codigo viejo que probablemente ya no se necesite

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
