# -*- coding: utf-8 -*-
"""
Created on Thu Jun 30 21:42:25 2022

@author: wladi
"""


import tkinter as tk


class ErgebnisSubFrameGrey(tk.Frame):

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.border_color = '#212122'
        self.frame_color = '#618A35'

        self.config(bg=self.border_color, *args, **kwargs)

        self.inner_frame = tk.Frame(self, bg=self.frame_color)
        self.inner_frame.pack(fill=tk.BOTH, expand=True, padx=3, pady=3)
