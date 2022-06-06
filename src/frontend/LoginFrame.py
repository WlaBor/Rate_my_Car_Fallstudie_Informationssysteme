import tkinter as tk

from frontend.custom_widgets.InteractiveEntryLogin import InteractiveEntryLogin
from frontend.custom_widgets.LoginButton import LoginButton
from frontend.custom_widgets.CanvasLogo import LogoCanvas

import os
from PIL import ImageTk, Image

DESIGN_LOGIN_LABEL = {
    'bg': 'white',
    'font': ('Arial', 25, 'bold'),
    'fg': '#394240'
}

DESIGN_LOGIN_SMALL_LABEL = {
    'bg': 'white',
    'font': ('Arial', 12, 'bold'),
    'fg': '#394240'
}

DESIGN_REGISTRIER_LABEL = {
    'bg': 'white',
    'font': ('Arial', 11, 'bold'),
    'fg': '#394240',
    'cursor': 'hand2'
}


class LoginFrame(tk.Frame):

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent)
        self.parent = parent

        self.layout()

    def layout(self):
        # Hintergrund
        self.config(bg='#92D050')

        # Logo
        # self.parent.pictures['logo']
        logo = LogoCanvas(parent=self, controller=self.parent, image_name='logo', size=(600, 150))
        logo.place(relx=0.5, rely=0.15, anchor=tk.CENTER)

        #logo_label = tk.Label(self, image=logo_pic)
        #logo_label.image = logo_pic
        # logo_label.place(relx=0.5, rely=0.15, anchor=tk.CENTER)

        # Eingabebereich
        eingabe_frame = tk.Frame(self, bg='white', width=800, height=400)
        eingabe_frame.pack_propagate(False)
        eingabe_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Login Überschrift
        tk.Label(eingabe_frame, text='Log In', **DESIGN_LOGIN_LABEL).pack(side=tk.TOP, fill=tk.X, pady=(20, 20))

        # ////////////////////////////////////////////
        # Label Benutzername
        lbl_Benutzername = tk.Label(eingabe_frame, text='Benutzername:', **
                                    DESIGN_LOGIN_SMALL_LABEL)
        lbl_Benutzername.pack(side=tk.TOP, anchor=tk.W, pady=3, padx=50)

        # Entry Benutzername
        entry_benutzername = InteractiveEntryLogin(parent=eingabe_frame)
        entry_benutzername.pack(side=tk.TOP, fill=tk.X, padx=50)

        # ////////////////////////////////////////////
        # Label Passwort
        lbl_passwort = tk.Label(eingabe_frame, text='Passwort:', **
                                DESIGN_LOGIN_SMALL_LABEL)
        lbl_passwort.pack(side=tk.TOP, anchor=tk.W, pady=(20, 3), padx=50)

        # Entry Passwort
        entry_passwort = InteractiveEntryLogin(parent=eingabe_frame)
        entry_passwort.entry.config(show="*")
        entry_passwort.pack(side=tk.TOP, fill=tk.X, padx=50)

        # ////////////////////////////////////////////
        # BINDINGS
        # Binding für visuelle Effekte - Benutzername

        def focusin_benutzername(*args):
            color = '#92D050'
            lbl_Benutzername.config(fg=color)
            entry_benutzername.config(bg=color)

        def focusout_benutzername(*args):
            color = '#394240'
            lbl_Benutzername.config(fg=color)
            entry_benutzername.config(bg=color)

        entry_benutzername.entry.bind('<FocusIn>', focusin_benutzername)
        entry_benutzername.entry.bind('<FocusOut>', focusout_benutzername)

        # ////////////////////////////////////////////
        # BINDINGS
        # Binding für visuelle Effekte - Passwort
        def focusin_passwort(*args):
            color = '#92D050'
            lbl_passwort.config(fg=color)
            entry_passwort.config(bg=color)

        def focusout_passwort(*args):
            color = '#394240'
            lbl_passwort.config(fg=color)
            entry_passwort.config(bg=color)

        entry_passwort.entry.bind('<FocusIn>', focusin_passwort)
        entry_passwort.entry.bind('<FocusOut>', focusout_passwort)

        # ////////////////////////////////////////////
        # Registriert Button
        lbl_registriert = tk.Label(eingabe_frame, text='Noch nicht registriert?', **
                                   DESIGN_REGISTRIER_LABEL)
        lbl_registriert.pack(side=tk.BOTTOM, padx=50, pady=(0, 15), anchor=tk.E)
        lbl_registriert.bind('<Enter>', lambda *args: lbl_registriert.config(fg='#92D050'))
        lbl_registriert.bind('<Leave>', lambda *args: lbl_registriert.config(fg='#394240'))
        lbl_registriert.bind('<Button-1>', lambda *args: self.parent.switch_frames(frame_name='Registrieren'))

        # ////////////////////////////////////////////
        # Login funktion
        def login(*args):
            self.parent.focus()
            # Eingabekontrollen
            # Username
            if self.parent.backend.User.check_User(entry_benutzername.value) == False:
                lbl_Benutzername.config(fg='red')
                entry_benutzername.config(bg='red')
                tk.messagebox.showerror('Achtung', 'Benutzername nicht vorhanden.')
                return

            # Passwort
            if self.parent.backend.User.give_Password_from_User(entry_benutzername.value, entry_passwort.value) == False:
                lbl_passwort.config(fg='red')
                entry_passwort.config(bg='red')
                tk.messagebox.showerror('Achtung', 'Benutzername und Passwort stimmen nicht über ein.')
                return

            # Login erfolgreich -> Home
            self.parent.switch_frames('Home')
            self.destroy()

        entry_benutzername.entry.bind('<Return>', login)
        entry_passwort.entry.bind('<Return>', login)

        # Log In - Button
        btn_login = LoginButton(parent=eingabe_frame, text='Log In', command=login)
        btn_login.pack(side=tk.BOTTOM, fill=tk.X, padx=50, pady=(0, 10))
