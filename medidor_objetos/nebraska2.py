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
contador = 0


def imgRatio(img_path):
    print("-"*100)
    print("\nWorld At Scale 1.0\n")
    print("-"*100)

    xc = []  # lista de coordenadas x
    yc = []  # lista de coordenadas en y
    circles = None
    circles = np.zeros((4, 2), np.int)

    print("Coordenadas originales: ")

    def mousePoints(event, x, y, flags, params):
        global contador
        font = cv2.FONT_HERSHEY_SIMPLEX
        if event == cv2.EVENT_LBUTTONDOWN:  # funcion de cv2 para detectar input de mouse
            print(x, y)  # imprimimos las coordenadas obtenidas
            xc.append(x)  # agregamos la coordenada a la lista de xc y yc
            yc.append(y)
            circles[contador] = x, y
            contador += 1

            if len(xc) == 1:  # se despliega el nombre de la coordenada dependiendo de que tantos elementos esten en la lista xc, una vez que supera 4, ya no se toma en cuenta
                cv2.putText(img, 'A', (x, y), font, 1, (255, 249, 0), 2)

            elif len(xc) == 2:
                cv2.putText(img, 'B', (x, y), font, 1, (255, 249, 0), 2)

            elif len(xc) == 3:
                cv2.putText(img, 'C', (x, y), font, 1, (255, 249, 0), 2)

            elif len(xc) == 4:
                cv2.putText(img, 'D', (x, y), font, 1, (255, 249, 0), 2)

            else:
                cv2.putText(img, '', (x, y), font, 1, (255, 249, 0), 3)
            # creamos una nueva imagen con la tag de img
            # AQUI SE GUARDA LA NUEVA IMAGEN
            cv2.imwrite('medidor_objetos/recursos/new.jpg', img)
            # mostramos el resultado al finalizar cada instancia
            cv2.imshow('image', img)

    # img ahora vale la imagen original
    # abrimos la imagen

    img = cv2.imread(img_path)
    copy = cv2.imread(img_path)

    # img = cv2.resize(im, (960, 540))  # hacemos resize leer arriba !!!!!!!!!
    font = cv2.FONT_HERSHEY_SIMPLEX
    img = cv2.rectangle(img, (8, 20), (550, 60), (0, 0, 0), -1)
    cv2.putText(img, 'Selecciona los puntos A B C y D ',
                (10, 50), font, 1, (255, 249, 0), 2)
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
    for i in range(len(xc)):  # El valor de las coordenadas con respecto al centro de la imagen
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

    # en casos donde el resultado del ratio sea nan o 0, regresamos false al usuario para que se pueda repetir el ciclo
    if np.isnan((v/u).real) or (v/u).real == 0.00:
        success = False
        font = cv2.FONT_HERSHEY_TRIPLEX
        img = cv2.rectangle(img, (8, 470), (813, 508), (0, 0, 0), -1)
        cv2.putText(img, 'Error, por favor presiona esc para reiniciar ',
                    (10, 500), font, 1, (0, 0, 255), 2)

        global contador
        contador = 0
        cv2.imshow('image', img)

        cv2.waitKey(0)

    else:
        ratio = ("%.3f" % (v/u).real)  # si no hay errores, mostamos el ratio
        font = cv2.FONT_HERSHEY_TRIPLEX
        print("Ratio: ", ratio)  # para que imprima el numero real
        img = cv2.rectangle(img, (8, 470), (230, 511), (0, 0, 0), -1)
        cv2.putText(img, 'Ratio: '+str(ratio),
                    (10, 500), font, 1, (0, 0, 255), 2)

        cv2.imshow('image', img)  # mostramos el resultado
        warp(copy, circles, float(ratio))
        cv2.waitKey(0)
        infosize = CrossRatio(xc, yc, centroX, centroY, (v/u).real)
        Realsize(infosize[0], infosize[1], infosize[2], (v/u).real)
        success = True  # regresamos true

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
            px.append(x)  # agregamos la coordenada a la lista de px y py
            py.append(y)
            if len(px) == 1:  # se despliega el nombre de la coordenada dependiendo de que tantos elementos esten en la lista xc, una vez que supera 4, ya no se toma en cuenta
                cv2.putText(img, 'a', (x, y), font, 1, (255, 0, 255), 2)

            elif len(px) == 2:
                cv2.putText(img, 'b', (x, y), font, 1, (255, 0, 255), 2)

            elif len(px) == 3:
                cv2.putText(img, 'c', (x, y), font, 1, (255, 0, 255), 2)

            elif len(px) == 4:
                cv2.putText(img, 'd', (x, y), font, 1, (255, 0, 255), 2)

            else:
                cv2.putText(img, '.', (x, y), font, 1, (255, 0, 255), 3)
            # creamos una nueva imagen con la tag de img
            cv2.imwrite('medidor_objetos/recursos/new.jpg', img)
            # mostramos el resultado al finalizar cada instancia
            cv2.imshow('image', img)

    # img ahora vale la imagen original
    # abrimos la imagen
    font = cv2.FONT_HERSHEY_SIMPLEX
    img = cv2.imread('medidor_objetos/recursos/new.jpg')
    img = cv2.rectangle(img, (8, 20), (640, 60), (0, 0, 0), -1)
    cv2.putText(img, 'Ahora selecciona los puntos del objeto ',
                (10, 50), font, 1, (255, 0, 255), 2)
    # img = cv2.resize(im, (750, 1333))  # hacemos resize
    # mostramos la imagen original, con el nombre image
    cv2.imshow('image', img)
    # llamamos al la funcion de cv2 setMouseCallback con image y mousePoints
    cv2.setMouseCallback("image", mousePoints2)
    cv2.waitKey(0)
    # # Estos son los cuatro vértices de la estructura principal, se añade una tercera dimensión en "z" = 1
    vphband = 'None'
    vpvband = 'None'
    dist = []
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
        vphband = 'right'
        BC = np.linalg.norm(C1-P4)
        AD = np.linalg.norm(vph-P3)
    else:  # Si el punto de horizonte se encuentra a la izquierda
        vphband = 'left'
        BC = np.linalg.norm(P3-C1)
        AD = np.linalg.norm(P3-vph)

    CR = (AC*BD) / (BC*AD)  # Cross ratio

    # Posteriormente se debe multiplicar este valor por el tamaño horizontal
    dist.append(1 / CR)
    print(dist[0])

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

    # Posteriormente se debe multiplicar este valor por el tamaño horizontal
    dist.append(1 / CR)
    print(dist[1])

    # Intersecciones y

    # De igual forma la interpretación de las distancias dependerá de la localización del punto de horizonte
    print("\nDistancia Vertical 1\n")
    C3 = np.cross(L1, l3)  # Punto de intersección
    C3 = C3 / C3[2]

    BD = np.linalg.norm(P1-P3)
    AC = np.linalg.norm(vpv-C3)
    # Si el punto de horizonte se encuentra abajo
    if np.linalg.norm(vpv-P1) < np.linalg.norm(vpv-P3):
        vpvband = 'down'
        BC = np.linalg.norm(C3-P1)
        AD = np.linalg.norm(vpv-P3)
    else:  # Si el punto de horizonte se encuentra arriba
        vpvband = 'up'
        BC = np.linalg.norm(P3-C3)
        AD = np.linalg.norm(P1-vpv)

    CR = (AC*BD) / (BC*AD)  # Cross ratio

    # Como está en función del tamaño horizontal, reemplazamos con el aspect ratio de la estructura original
    dist.append(ratio / CR)
    print(dist[2])
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

    # Como está en función del tamaño horizontal, reemplazamos con el aspect ratio de la estructura original
    dist.append(ratio / CR)
    print(dist[3])
    return [dist, vphband, vpvband]


def Realsize(dist, vph, vpv, ratio):
    side = int(input("\n ¿Qué medida conoce?, vertical(0) u horizontal(1): "))
    length = float(input("Introduzca el tamaño: "))
    if side == 0:  # Si es vertical
        length = length / ratio
        print("La distancia horizontal es: ", length)
    else:
        print("La distancia vertical es: ", length*ratio)
    for i in range(0, len(dist)):
        dist[i] = np.around(dist[i]*length, decimals=2)

    if vph == 'left':
        print("Las distancias hacia el rectángulo desde el borde AC son: ",
              dist[0], "y", dist[1])
    else:
        print("Las distancias hacia el rectángulo desde el borde BD son: ",
              dist[0], "y", dist[1])
    if vpv == 'up':
        print("Las distancias hacia el rectángulo desde el borde CD son: ",
              dist[2], "y", dist[3])
    else:
        print("Las distancias hacia el rectángulo desde el borde AB son: ",
              dist[2], "y", dist[3])


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


def warp(img, circles, a_ratio):
    # img = imagen delimitada por los 4 puntos seleccionados por el usuario
    # circles = arreglo que guarda las coordenadas de los 4 puntos seleccionados por el usuario en la image noriginal
    # a_ratio = aspect ratio calculado

    # temp se usa para guardar los datos de circles de una manera particular
    temp = [circles[0], circles[2], circles[3], circles[1]]
    # pues así lo solicita el método de Area
    # se calcula el ancho que tendrá la imagen warpeada
    width = cmath.sqrt(Area(temp)/a_ratio).real
    # con base en una fórmula que relaciona el a_ratio con la altura y el ancho
    height = width*a_ratio  # se calcula la altura que tendrá la imagen warpeada

    # pts1 es para crear un arreglo con las coordenadas acomodadas de una manera específica,
    # la cual tiene como primeros dos elementos los puntos superiores del rectángulo, mientras
    # que los últimos dos elementos representan los puntos inferiores
    pts1 = np.float32([circles[2], circles[3], circles[0], circles[1]])

    # pts2 representa la manera en que queremos que nos acomode en la nueva imagen los datos que le demos-
    # el primer elemento representa el punto superior izquierdo, el segundo el punto superior derecho, el
    # tercero el punto inferior izquierdo y el cuarto punto es el inferior derecho
    pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])

    # las variables anteriores son necesarias para obtener una matriz
    matrix = cv2.getPerspectiveTransform(pts1, pts2)  # matriz

    # teniendo todos los datos necesarios, ya podemos llamar al método de warpPerspective.
    # width y height los hacemos int porque deben de serlo para pasarlos como parámetro, y como
    # al ser calculados al incio no quedan como números enterros, debemos transformarlos
    imgw = cv2.warpPerspective(img, matrix, (int(width), int(height)))

    # mostramos la imagen warpeada
    cv2.imshow("WARP", imgw)
    cv2.imwrite('area.jpg', imgw)


def Area(corners):
    n = 4  # of corners
    area = 0.0
    for i in range(n):
        j = (i + 1) % n
        area += corners[i][0] * corners[j][1]
        area -= corners[j][0] * corners[i][1]
    area = abs(area) / 2.0
    return area


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
