# -*- coding: utf-8 -*-
"""
Created on Mon Jun  6 14:06:44 2022

@author: wladi
"""

import tkinter as tk
import os
from PIL import ImageTk, Image


class LogoCanvas(tk.Frame):

    def __init__(self, parent, controller, image_name, size, bg='#92D050'):

        super().__init__(master=parent, bg=bg, width=size[0], height=size[1])

        self.image_name = image_name
        self.parent = parent
        self.size = size
        self.bg = bg
        self.controller = controller

        self.create_canvas()

    def create_canvas(self):

        # Canvas
        canvas = tk.Canvas(self, width=self.size[0], height=self.size[1],
                           bg='#92D050', bd=0, highlightthickness=0, relief='ridge')

        image = self.controller.pictures[self.image_name].resize(self.size)

        image = ImageTk.PhotoImage(image, master=self.parent)
        self.image = image

        self.image_on_canvas = canvas.create_image(0, 0, anchor=tk.NW, image=image)
        canvas.image = self.image

        canvas.pack(fill=tk.BOTH, expand=True)

        self.canvas = canvas

    def change_pic(self, pic_name, size=None):
        if size != None:
            self.size = size
        image = self.controller.pictures[pic_name].resize(self.size)

        image = ImageTk.PhotoImage(image, master=self.parent)
        self.image = image
        self.canvas.image = self.image

        self.canvas.itemconfig(self.image_on_canvas, image=image)
