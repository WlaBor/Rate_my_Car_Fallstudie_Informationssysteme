import tkinter as tk
import os
from PIL import ImageTk, Image


class ToggleButton(tk.Frame):

    def __init__(self, parent, controller, size, bg='#92D050', command=None, state='off',
                 on_command=None, off_command=None):
        super().__init__(master=parent, bg=bg, width=size[0], height=size[1])
        self.parent = parent
        self.controller = controller
        self.size = size
        self.state = state
        self.off_command = off_command
        self.on_command = on_command

        self.off_pic = ImageTk.PhotoImage(
            self.controller.pictures['toggle_off'].resize(self.size), master=self.controller)
        self.on_pic = ImageTk.PhotoImage(
            self.controller.pictures['toggle_on'].resize(self.size), master=self.controller)

        self.layout()

    def layout(self):
        current_pic = self.off_pic
        if self.state == 'on':
            current_pic = self.on_pic
        canvas = tk.Canvas(self, width=self.size[0], height=self.size[1],
                           bg='#92D050', bd=0, highlightthickness=0, relief='ridge', cursor='hand2')
        pic = canvas.create_image(0, 0, anchor=tk.NW, image=current_pic)
        canvas.image = current_pic

        canvas.pack(fill=tk.BOTH, expand=True)

        global on_p
        on_p = False

        def bind_canvas_click(*args):
            global on_p
            if on_p == False:
                return
            if self.state == 'off':
                canvas.itemconfig(pic, image=self.on_pic)
                canvas.image = self.on_pic
                self.state = 'on'
                try:
                    self.on_command()
                except Exception as ex:
                    print(ex)
                    pass

            else:
                canvas.itemconfig(pic, image=self.off_pic)
                canvas.image = self.off_pic
                self.state = 'off'
                try:
                    self.off_command()
                except Exception as ex:
                    print(ex)
                    pass

        def bind_enter(*args):
            global on_p
            on_p = True

        def bind_leave(*args):
            global on_p
            on_p = False
        canvas.bind('<ButtonRelease-1>', bind_canvas_click)
        canvas.bind('<Enter>', bind_enter)
        canvas.bind('<Leave>', bind_leave)
