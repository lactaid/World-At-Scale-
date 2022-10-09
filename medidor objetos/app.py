from tkinter import *
from tkinter import filedialog
import tkinter as tk
from PIL import Image, ImageTk
import os

img_path = ""

root = Tk()
root.title("World At Scale")
root.geometry("400x500")
root.configure(background='#3d3d3b')

lab1 = Label(root, text="Image Viewer", font=(
    "courier", 19, "bold"), fg='white', bg='#3d3d3b')
lab1.place(relx=0.5, rely=0.06, anchor=CENTER)


label_image = Label(root, text='', bg='#3d3d3b')

img_path = ""


def showimage():
    global img_path
    img_path = filedialog.askopenfilename(initialdir=os.getcwd(), title=" Open Text File", filetypes=[
                                          ("Image Files", "*.jpg *.gif *.jpg *.png *.jpeg")])
    print(img_path)
    img = Image.open(img_path)
    img = ImageTk.PhotoImage(img)
    label_image['image'] = img
    img.close()


btn = Button(text="Select Image", command=showimage)


btn = Button(root, text="Seleccionar Imagen", fg='white', bg='#A248DF', highlightthickness=5, borderwidth=5,
             relief=RIDGE, height=1, width=12, font=("normal", 13), padx=15, pady=1, command=showimage)
btn2 = Button(root, text="Rotate Image", fg='white', bg='#A248DF', highlightthickness=5, borderwidth=5,
              relief=RIDGE, height=1, width=12, font=("normal", 13), padx=15, pady=1, command=lambda: exit())

btn.pack(side='right', anchor='s', expand=True)
btn2.pack(side='right', anchor='s', expand=True)

btn3 = Button(text="Salir", fg='white', bg='#A248DF', highlightthickness=5,
              borderwidth=5, font=("normal", 13), command=lambda: exit())
btn3.pack(side='right', anchor='s', expand=True)

label_image.place(relx=0.5, rely=0.5, anchor=CENTER)
root.mainloop()
print('Path: ', img_path)
