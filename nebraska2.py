import numpy as np
import time
import cmath
from PIL import Image

import cv2

xc = []
yc = []
coord = {}
print("hola")

# para cuando hacemos clic


def mousePoints(event, x, y, flags, params):

    font = cv2.FONT_HERSHEY_SIMPLEX
    if event == cv2.EVENT_LBUTTONDOWN:
        print(x, y)
        xc.append(x)
        yc.append(y)
        if len(xc) == 1:
            cv2.putText(img, 'A', (x, y), font, 1, (255, 249, 0), 3)

        elif len(xc) == 2:
            cv2.putText(img, 'B', (x, y), font, 1, (255, 249, 0), 3)

        elif len(xc) == 3:
            cv2.putText(img, 'C', (x, y), font, 1, (255, 249, 0), 3)

        elif len(xc) == 4:
            cv2.putText(img, 'D', (x, y), font, 1, (255, 249, 0), 3)

        else:
            cv2.putText(img, '.', (x, y), font, 1, (255, 249, 0), 3)
        cv2.imwrite('new.jpg', img)
        cv2.imshow('image', img)


img = cv2.imread('\\images\\2x2.jpg')
cv2.imshow('image', img)
cv2.setMouseCallback("image", mousePoints)

cv2.waitKey(0)

# encontrar el centro
image = Image.open('img\\2x2.jpg')
centroX = image.size[0]/2
centroY = image.size[1]/2
print('size: ', image.size)
print('coords: ', centroX, centroY)

for i in range(len(xc)):
    if xc[i] >= centroX:
        xc[i] = -(centroX - xc[i])
    else:
        xc[i] = xc[i] - centroX

for i in range(len(yc)):
    if yc[i] >= centroY:
        yc[i] = -(centroY - yc[i])
    else:
        yc[i] = yc[i] - centroY

print(xc, yc)
# Imagen tomada en cetys
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

    xS[i] = np.around((M[i, n] - x) / M[i, i], decimals=2)  # [1,xS[i+1],xS[i]]
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

print("Ratio", (v/u).real)  # para que imprima eln umero real
