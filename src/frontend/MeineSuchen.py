import tkinter as tk


class MeineSuchenFrame(tk.Frame):

    def __init__(self, parent, controller, *args, **kwargs):
        super().__init__(parent)
        self.parent = parent
        self.controller = controller

        self.layout()

    def layout(self):
        self.config(bg='blue')
