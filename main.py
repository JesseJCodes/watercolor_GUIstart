import tkinter.font
from tkinter import *
from tkinter import filedialog
import os
import shutil
import colorlist
import PIL.Image
from PIL import ImageTk, Image, ImageDraw, ImageFont



def open_directorys(func):
    def wrapper(*args, **kwargs):
        global img_name

        window.filename = filedialog.askopenfilename(initialdir="/", title="Select file",
                                                     filetypes=(
                                                     ("jpeg files", "*.jpg *.png *.svg"), ("all files", "*.*")))
        img_name = window.filename.split("/")[-1]
        old_path = window.filename
        new_path = os.getcwd()
        shutil.copyfile(old_path,new_path+f"/app_img/{img_name}")
        func(*args, *kwargs)
    return wrapper


def add_to_canvas():
    global img_name
    global canvas
    img_name = os.getcwd()+f"/app_img/{img_name}"
    display = PIL.Image.open(img_name, mode='r').resize((800,800))
    img = ImageTk.PhotoImage(display)
    canvas.destroy()
    canvas = Canvas(window, height=599, width=699)
    canvas.image = img # keep a reference
    canvas.pack()
    canvas.create_image(0, 0, image=img, anchor=NW)


add_to_canvas = open_directorys(add_to_canvas)


def add_watermark(func):
    def wrapper(*args, **kwargs):
        global img_name
        display = PIL.Image.open(img_name, mode='r').resize((800, 800))
        text = watermark_text.get()
        font = ImageFont.load_default(75)
        wm = ImageDraw.Draw(display)
        wm.text((10, 10), text, font=font, fill=(255, 255, 255))
        display.save(f"{img_name}")

        func(*args, **kwargs)

    return wrapper


def update_canvas():
    display = PIL.Image.open(img_name, mode='r').resize((800, 800))
    img = ImageTk.PhotoImage(display)
    canvas.image = img
    canvas.update()
    canvas.create_image(0, 0, image=img, anchor=NW)


wm = add_watermark(update_canvas)


def begin():
    global canvas
    start_button.destroy()
    canvas.destroy()
    window.title("WaterMark App")
    canvas = Canvas(window, height=599, width=699)
    canvas.pack(side=TOP, fill=BOTH, expand=True)
    label = Label(window, text="You need to add a photo to WaterMark", font=("Arial", 20))
    label.place(x=180, y=0)
    browse_but = Button(text="Browse", command=add_to_canvas)
    browse_but.place(x=90, y=0)


window = Tk()
window.title("WaterMark App")
window.minsize(850, 700)
window.configure(padx=10, pady=10, bg="gray")
canvas = Canvas(window, height=599, width=699)
canvas.pack()
welcome_img = ImageTk.PhotoImage(Image.open('fitwelcome.png'))
canvas.create_image(0, 0, image=welcome_img, anchor=NW)
start_button = Button(window, height=5, width=5, text='Get Started!', command=begin)
start_button.place(x=350, y=320)
watermark_text = StringVar()
entry1 = Entry(window,bg="white",textvariable=watermark_text,width=28,fg='black', insertbackground='black')
entry1.place(y=630,x=220)
entry_label = Label(window,text="Write your watermark text below",bg="gray",fg="white",font=('Helvetica',18))
entry_label.place(y=607,x=220)
submit_button = Button(text="Save", command=wm,bg='gray',bd=0,padx=0,pady=0)
submit_button.place(y=627,x=520)


window.mainloop()
