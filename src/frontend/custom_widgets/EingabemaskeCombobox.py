# -*- coding: utf-8 -*-
"""
Created on Mon Jun 20 14:21:43 2022

@author: wladi
"""
import tkinter as tk
from tkinter import ttk

font = ('Arial', 18)


class EingabemaskeCombobox(tk.Frame):

    def __init__(self, parent, controller, *args, **kwargs):

        self.label_text = kwargs.pop('text', None)
        self.values = kwargs.pop('values', [])

        super().__init__(master=parent, *args, **kwargs)

        self.parent = parent
        self.controller = controller

        self.bg = kwargs.pop('bg', None)

        self.layout()

    @property
    def values(self):
        return self._values

    @values.setter
    def values(self, values):
        if isinstance(values, list):
            self._values = values
            try:
                self.combobox.config(values=values)
            except:
                pass

    @property
    def value(self):
        print(self.combobox.get())
        return self.combobox.get()

    def layout(self):
        # Label
        if self.label_text != None:
            label = tk.Label(self, text=self.label_text, bg=self.bg, font=font)
            label.pack(side=tk.TOP, anchor=tk.W)
            self.label = label

        str_var = tk.StringVar()
        self.variable = str_var

        combobox = ttk.Combobox(self, textvariable=str_var, font=font,
                                state="readonly", values=self.values)
        combobox.pack(side=tk.TOP, fill=tk.X, padx=20)
        self.combobox = combobox
