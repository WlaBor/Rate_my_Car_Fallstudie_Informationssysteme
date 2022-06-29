
import tkinter as tk
import os
from PIL import ImageTk, Image


class ButtonCanvas(tk.Frame):

    def __init__(self, parent, controller, on_pic, off_pic, click_pic, size, bg='#92D050', command=None):

        super().__init__(master=parent, bg=bg, width=size[0], height=size[1])

        self.off_pic = off_pic
        self.on_pic = on_pic
        self.click_pic = click_pic
        self.parent = parent
        self.size = size
        self.bg = bg
        self.controller = controller
        self.command = command

        self.create_canvas()

    def create_canvas(self):
        image_off = ImageTk.PhotoImage(self.controller.pictures[self.off_pic].resize(self.size), master=self.controller)
        image_on = ImageTk.PhotoImage(self.controller.pictures[self.on_pic].resize(self.size), master=self.controller)
        image_click = ImageTk.PhotoImage(
            self.controller.pictures[self.click_pic].resize(self.size), master=self.controller)

        # Canvas
        canvas = tk.Canvas(self, width=self.size[0]+2, height=self.size[1]+2,
                           bg=self.bg, bd=0, highlightthickness=0, relief='ridge', cursor='hand2')

        self.canvas = canvas

        pic = canvas.create_image(int((self.size[0]+2)/2), int((self.size[1]+2)/2), anchor=tk.CENTER, image=image_off)
        canvas.image = image_off

        canvas.pack(fill=tk.BOTH, expand=True)

        global click
        click = False

        global on_pic
        on_pic = False

        # Enter bind

        def bind_enter(*args):
            global on_pic
            on_pic = True
            if click == False:
                canvas.itemconfig(pic, image=image_on)
                canvas.image = image_on

        canvas.bind('<Enter>', bind_enter)

        # Leave bind
        def bind_leave(*args):
            global on_pic
            on_pic = False
            if click == False:
                canvas.itemconfig(pic, image=image_off)
                canvas.image = image_off
        canvas.bind('<Leave>', bind_leave)

        # Button Click
        def bind_click(*args):
            global click
            click = True
            canvas.itemconfig(pic, image=image_click)
            canvas.image = image_click
        canvas.bind('<Button-1>', bind_click)

        # Button Release
        def bind_button_release(*args):
            global click
            click = False
            global on_pic
            if on_pic == True:
                if self.command != None:
                    try:
                        self.command()
                    except Exception as ex:
                        print('command fehlgeschlagen')
                        print(ex)
                canvas.itemconfig(pic, image=image_on)
                canvas.image = image_on
            else:
                canvas.itemconfig(pic, image=image_off)
                canvas.image = image_off
        canvas.bind('<ButtonRelease-1>', bind_button_release)
