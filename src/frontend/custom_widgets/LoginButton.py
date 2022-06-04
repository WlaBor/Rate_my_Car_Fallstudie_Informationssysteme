# -*- coding: utf-8 -*-
"""
Created on Fri Jun  3 16:08:23 2022

@author: wladi
"""
import tkinter as tk

font = ('Arial', 16, 'bold')


class LoginButton(tk.Button):

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.layout()

    def layout(self):
        # Hintergrund
        self.config(bg='#92D050', font=font, fg='white', cursor='hand2')

        # Bindings
        self.bind('<Enter>', lambda *args: self.config(bg='#C7E7A6', fg='#394240'))
        self.bind('<Leave>', lambda *args: self.config(bg='#92D050', fg='white'))
