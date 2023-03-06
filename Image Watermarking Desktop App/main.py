from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from PIL import Image, ImageTk, ImageDraw
from os import listdir


def update_img(event):
    WM = value_selcted.get()

    if WM == "Water Mark 1":
        img = WM1
    else:
        img = WM2

    canvas.itemconfig(wm_container, image=img)


def on_select(event):
    image_name = file_list.get(event.widget.curselection())
    image_path = folder_name["text"] + "/" + image_name

    img = Image.open(image_path)
    resized = img.resize((500, 500), Image.ANTIALIAS)

    img_resized = ImageTk.PhotoImage(resized)

    canvas.itemconfig(image_container, image=img_resized)
    image_container.image = img_resized


def load_folder():
    folder = filedialog.askdirectory(title="Select image folder")
    folder_name.config(text=folder)
    images = [file for file in listdir(folder) if file.endswith('.png')]
    for image in images:
        file_list.insert("end", image)


def set_wm():
    selected_file = folder_name["text"] + "/" + file_list.get(ACTIVE)
    img = Image.open(selected_file)

    WM = value_selcted.get()

    if WM == "Water Mark 1":
        wm = Image.open("WM1.png")
    else:
        wm = Image.open("WM2.png")

    width_img, heigth_img = img.size
    width_wm, height_wm = wm.size
    print(width_img, heigth_img, width_wm, height_wm)

    img.paste(wm, (width_img-width_wm,heigth_img-height_wm))

    new_filename = folder_name["text"] + "/WM_" + file_list.get(ACTIVE)
    img.save(new_filename)

    file_list.delete(0, END)

    images = [file for file in listdir(folder_name["text"]) if file.endswith('.png')]
    for image in images:
        file_list.insert("end", image)


window = Tk()
window.title("Water Marker")
window.geometry('1050x720')
window.config(padx=20, pady=20, bg="#FFFFFF")

# Images
WM1 = PhotoImage(file="WM1.png")
WM2 = PhotoImage(file="WM2.png")


# Option List
option_list = ["Water Mark 1", "Water Mark 2"]
value_selcted = StringVar(window)
value_selcted.set("select WM")

wm_opt = OptionMenu(window, value_selcted, *option_list, command=update_img)
wm_opt.grid(row=0, column=0)

# Buttons
load_btn = Button(height=3, width=20, text="Load Image", command=load_folder)
load_btn.grid(row=1, column=0)

set_btn = Button(height=3, width=20, text="Set WaterMark", command=set_wm)
set_btn.grid(row=1, column=1)

# Lisbox
file_list = Listbox(window, height=30)
file_list.grid(row=3, column=0)

file_list.bind('<<ListboxSelect>>', on_select)

scrollbar= ttk.Scrollbar(window, orient='vertical')
scrollbar.grid(row=3, column=1)

file_list.config(yscrollcommand= scrollbar.set)
#Configure the scrollbar
scrollbar.config(command= file_list.yview)

# Label
folder_name = Label(window, text="")
folder_name.grid(row=2, column=0)

# WM image
canvas = Canvas(window, width=200, height=120)
canvas.grid(row=0, column=1)
wm_container = canvas.create_image(20, 0, image=WM1, anchor="nw")

# Image
canvas = Canvas(window,width=500, height=500)
canvas.grid(row=1, column=2, rowspan=3)
image_container = canvas.create_image(0, 0, anchor='nw', image="")


window.mainloop()
