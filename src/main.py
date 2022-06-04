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
        self.pictures['logo'] = ImageTk.PhotoImage(Image.open(
            str(os.path.join(self.pic_path, 'logo.png'))).resize((600, 150)), master=self)

    def switch_frames(self, frame_name, *args, **kwargs):
        if self.aktueller_frame != None:
            #print('Alter Frame: ' + str(self.aktueller_frame))
            self.aktueller_frame.forget()
        frame = self.frame_container[frame_name](self, *args, **kwargs)
        frame.pack(fill=tk.BOTH, expand=True)
        #print('Neuer Frame: ' + frame_name)
        self.aktueller_frame = frame


if __name__ == '__main__':
    app = Application()
    app.mainloop()
