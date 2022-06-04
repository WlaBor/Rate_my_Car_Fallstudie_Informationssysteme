import tkinter as tk

from frontend.custom_widgets.InteractiveEntryLogin import InteractiveEntryLogin
from frontend.custom_widgets.LoginButton import LoginButton
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


class RegistrierFrame(tk.Frame):

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent)
        self.parent = parent

        self.layout()

    def layout(self):
        # Hintergrund
        self.config(bg='#92D050')

        # Eingabebereich
        eingabe_frame = tk.Frame(self, bg='white', width=800, height=600)
        eingabe_frame.pack_propagate(False)
        eingabe_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Registrieren Überschrift
        tk.Label(eingabe_frame, text='Registrieren', **DESIGN_LOGIN_LABEL).pack(side=tk.TOP, fill=tk.X, pady=(20, 20))

        # ////////////////////////////////////////////
        # Binding
        def focusin(lbl, entry, *args):
            color = '#92D050'
            lbl.config(fg=color)
            entry.config(bg=color)

        def focusout(lbl, entry, *args):
            color = '#394240'
            lbl.config(fg=color)
            entry.config(bg=color)

        # ////////////////////////////////////////////
        # Label Benutzername
        lbl_Benutzername = tk.Label(eingabe_frame, text='Benutzername:', **
                                    DESIGN_LOGIN_SMALL_LABEL)
        lbl_Benutzername.pack(side=tk.TOP, anchor=tk.W, pady=3, padx=50)

        # Entry Benutzername
        entry_benutzername = InteractiveEntryLogin(parent=eingabe_frame)
        entry_benutzername.pack(side=tk.TOP, fill=tk.X, padx=50)
        entry_benutzername.entry.bind('<FocusIn>', lambda *args: focusin(lbl_Benutzername, entry_benutzername))
        entry_benutzername.entry.bind('<FocusOut>', lambda *args: focusout(lbl_Benutzername, entry_benutzername))

        # ////////////////////////////////////////////
        # Label Passwort
        lbl_Passwort = tk.Label(eingabe_frame, text='Passwort:', **
                                DESIGN_LOGIN_SMALL_LABEL)
        lbl_Passwort.pack(side=tk.TOP, anchor=tk.W, pady=3, padx=50)

        # Entry Passwort
        entry_Passwort = InteractiveEntryLogin(parent=eingabe_frame)
        entry_Passwort.pack(side=tk.TOP, fill=tk.X, padx=50)
        entry_Passwort.entry.config(show="*")
        entry_Passwort.entry.bind('<FocusIn>', lambda *args: focusin(lbl_Passwort, entry_Passwort))
        entry_Passwort.entry.bind('<FocusOut>', lambda *args: focusout(lbl_Passwort, entry_Passwort))

        # ////////////////////////////////////////////
        # Label Passwort bestätigen
        lbl_pw_bestaetigen = tk.Label(eingabe_frame, text='Passwort bestätigen:', **
                                      DESIGN_LOGIN_SMALL_LABEL)
        lbl_pw_bestaetigen.pack(side=tk.TOP, anchor=tk.W, pady=3, padx=50)

        # Entry Passwort bestätigen
        entry_pw_bestaetigen = InteractiveEntryLogin(parent=eingabe_frame)
        entry_pw_bestaetigen.pack(side=tk.TOP, fill=tk.X, padx=50)
        entry_pw_bestaetigen.entry.config(show="*")
        entry_pw_bestaetigen.entry.bind('<FocusIn>', lambda *args: focusin(lbl_pw_bestaetigen, entry_pw_bestaetigen))
        entry_pw_bestaetigen.entry.bind('<FocusOut>', lambda *args: focusout(lbl_pw_bestaetigen, entry_pw_bestaetigen))

        # ////////////////////////////////////////////
        # Label Straße
        lbl_strasse = tk.Label(eingabe_frame, text='Straße:', **
                               DESIGN_LOGIN_SMALL_LABEL)
        lbl_strasse.pack(side=tk.TOP, anchor=tk.W, pady=3, padx=50)

        # Entry Straße
        entry_strasse = InteractiveEntryLogin(parent=eingabe_frame)
        entry_strasse.pack(side=tk.TOP, fill=tk.X, padx=50)
        entry_strasse.entry.bind('<FocusIn>', lambda *args: focusin(lbl_strasse, entry_strasse))
        entry_strasse.entry.bind('<FocusOut>', lambda *args: focusout(lbl_strasse, entry_strasse))

        # ////////////////////////////////////////////
        # Label Postleitzahl
        lbl_plz = tk.Label(eingabe_frame, text='Postleitzahl:', **
                           DESIGN_LOGIN_SMALL_LABEL)
        lbl_plz.pack(side=tk.TOP, anchor=tk.W, pady=3, padx=50)

        # Entry Postleitzahl
        entry_plz = InteractiveEntryLogin(parent=eingabe_frame)
        entry_plz.pack(side=tk.TOP, fill=tk.X, padx=50)
        entry_plz.entry.bind('<FocusIn>', lambda *args: focusin(lbl_plz, entry_plz))
        entry_plz.entry.bind('<FocusOut>', lambda *args: focusout(lbl_plz, entry_plz))

        # Eingabekontrolle PLZ
        def callback(val):
            if str.isdigit(val) or val == "":
                return True
            else:
                return False
        vcmd = (self.parent.register(callback))

        entry_plz.entry.config(validate='all', validatecommand=(vcmd, '%P'))

        # ////////////////////////////////////////////
        # Buttons
        frame_buttons = tk.Frame(eingabe_frame, bg='white')
        frame_buttons.pack(side=tk.BOTTOM, fill=tk.X, padx=50)
        frame_buttons.grid_columnconfigure(0, weight=1)
        frame_buttons.grid_columnconfigure(1, weight=1)
        frame_buttons.grid_rowconfigure(0, weight=1)

        # Abbrechen - Button
        def abbrechen(*args):
            self.parent.switch_frames('LogIn')
            self.destroy()

        btn_abbrechen = LoginButton(parent=frame_buttons, text='Abbrechen',
                                    command=abbrechen)
        btn_abbrechen.grid(row=0, column=0, sticky='nsew', padx=(0, 5), pady=(10, 30))

        def save_user():
            username = entry_benutzername.value.strip()
            passwort = entry_Passwort.value.strip()
            passwort_best = entry_pw_bestaetigen.value.strip()
            strasse = entry_strasse.value.strip()
            if strasse == '':
                strasse = None
            plz = entry_plz.value.strip()
            if plz == '':
                plz = None

            def entry_rot_faerben(lbl, entry):
                color = 'red'
                lbl.config(fg=color)
                entry.config(bg=color)

            # Eingabekontrollen
            # Benutzername leer
            if username == '':
                entry_rot_faerben(lbl_Benutzername, entry_benutzername)
                tk.messagebox.showwarning('Achtung', 'Kein Benutzername eingegeben.')
                return

            # Passwort leer
            if passwort == '':
                entry_rot_faerben(lbl_Passwort, entry_Passwort)
                entry_rot_faerben(lbl_pw_bestaetigen, entry_pw_bestaetigen)
                tk.messagebox.showwarning('Achtung', 'Kein Passwort eingegeben.')
                return

            # Passwort mindestens 4 Zeichen
            if len(passwort) < 4:
                entry_rot_faerben(lbl_Passwort, entry_Passwort)
                entry_rot_faerben(lbl_pw_bestaetigen, entry_pw_bestaetigen)
                tk.messagebox.showwarning('Achtung', 'Passwort muss mindestens 4 Zeichen lang sein.')
                return

            # Check ob Username bereits vergeben ist
            if self.parent.backend.User.check_User(username) == True:
                entry_rot_faerben(lbl_Benutzername, entry_benutzername)
                tk.messagebox.showwarning('Achtung', 'Benutzername ist bereits vergeben.')
                return

            # Passwort und Passwort bestätigt müssen gleich sein
            if passwort != passwort_best:
                entry_rot_faerben(lbl_pw_bestaetigen, entry_pw_bestaetigen)
                tk.messagebox.showwarning('Achtung', 'Passwort und Passwort bestätigt stimmen nicht über ein.')
                return

            # User speichern
            self.parent.backend.User.save_User(username, passwort, strasse=strasse, plz=plz)
            tk.messagebox.showinfo('Erfolg', 'Benutzer erfolgreich erstellt!')

            # Zurück zum Login Bildschirm
            self.parent.switch_frames('LogIn')
            self.destroy()

        # Bestätigen - Button
        btn_bestaetigen = LoginButton(parent=frame_buttons, text='Bestätigen', command=save_user)
        btn_bestaetigen.grid(row=0, column=1, sticky='nsew', padx=(5, 0), pady=(10, 30))
