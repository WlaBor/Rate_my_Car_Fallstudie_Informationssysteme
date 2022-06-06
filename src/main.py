# Bibliotheke importieren
import tkinter as tk
import os
import sys
from PIL import ImageTk, Image

# Backend
from backend.backend import Backend

# Frames
from frontend.LoginFrame import LoginFrame
from frontend.RegistFrame import RegistrierFrame
from frontend.HomeFrame import HomeFrame

# Konstanten
TITLE = 'Rate My Car Value'
GEOMETRY = '1550x850'


class Application(tk.Tk):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.configurations()

        self.backend = Backend(db_path=self.db_path)

        self.pictures = {}
        self.load_pics()

        self.frame_container = {
            'LogIn': LoginFrame,
            'Registrieren': RegistrierFrame,
            'Home': HomeFrame
        }
        self.aktueller_frame = None

        self.switch_frames('LogIn')

    def configurations(self):
        # Titel der Applikation
        self.title = TITLE
        self.wm_title(TITLE)

        # Größe des Fensters
        self.geometry(GEOMETRY)
        self.minsize(1500, 800)

        # Arbeitsordner
        self.folder_path = os.path.abspath(os.path.dirname(sys.argv[0]))
        print('Arbeitsordner: ' + str(self.folder_path))

        # Datenbank Pfad
        self.db_path = os.path.join(self.folder_path, 'sqlite_db.db')
        print('Datenbank: ' + str(self.db_path))

        # Pfad zu Bildern
        self.pic_path = os.path.join(self.folder_path, 'pics')

    def load_pics(self):
        # Logo
        self.pictures['logo'] = Image.open(str(os.path.join(self.pic_path, 'logo.png')))

        # Profil Button
        self.pictures['profil_btn_off'] = Image.open(str(os.path.join(self.pic_path, 'profil_btn_off.png')))
        self.pictures['profil_btn_on'] = Image.open(str(os.path.join(self.pic_path, 'profil_btn_on.png')))
        self.pictures['profil_btn_click'] = Image.open(str(os.path.join(self.pic_path, 'profil_btn_click.png')))

    def switch_frames(self, frame_name, *args, **kwargs):
        if self.aktueller_frame != None:
            #print('Alter Frame: ' + str(self.aktueller_frame))
            self.aktueller_frame.forget()
        frame = self.frame_container[frame_name](self, *args, **kwargs)
        frame.pack(fill=tk.BOTH, expand=True)
        #print('Neuer Frame: ' + frame_name)
        self.aktueller_frame = frame

    def get_mouse_position(self):
        print((self.winfo_pointerx() - self.winfo_vrootx(), self.winfo_pointery() - self.winfo_vrooty()))
        return self.winfo_pointerx() - self.winfo_vrootx(), self.winfo_pointery() - self.winfo_vrooty()


if __name__ == '__main__':
    app = Application()
    app.mainloop()
