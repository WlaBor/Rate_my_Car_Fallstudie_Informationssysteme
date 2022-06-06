# -*- coding: utf-8 -*-
"""
Created on Fri Jun  3 15:39:23 2022

@author: wladi
"""
import tkinter as tk

font = ('Arial', 16)


class InteractiveEntryLogin(tk.Frame):

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.trace = True

        self.layout()

    @property
    def value(self):
        self._value = self.str_var.get()
        return self._value

    def layout(self):
        # Hintergrund
        self.config(bg='#394240')

        # Weißer Hintergrund um Abstand im Entry größer zu machen
        entry_background = tk.Frame(self, bg='white')
        entry_background.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

        # Stringvariable, um Eingabewert zu lesen
        str_var = tk.StringVar(self)

        def trace_keine_leerzeile(*args):
            if self.trace == True:
                str_var.set(str_var.get().strip())

        str_var.trace('w', trace_keine_leerzeile)

        self.str_var = str_var

        # Eingabefeld
        entry = tk.Entry(entry_background, textvariable=str_var, font=font, relief=tk.FLAT)
        entry.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        self.entry = entry

        # Binding für visuelle Effekte
        entry.bind('<FocusIn>', lambda *args: self.config(bg='#92D050'))
        entry.bind('<FocusOut>', lambda *args: self.config(bg='#394240'))
