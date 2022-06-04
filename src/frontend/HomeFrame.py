import tkinter as tk

from frontend.custom_widgets.InteractiveEntryLogin import InteractiveEntryLogin
from frontend.custom_widgets.LoginButton import LoginButton
import os
from PIL import ImageTk, Image


class HomeFrame(tk.Frame):

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent)
        self.parent = parent

        self.layout()

    def layout(self):
        # Hintergrund
        self.config(bg='yellow')
