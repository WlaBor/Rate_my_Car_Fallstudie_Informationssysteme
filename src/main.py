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
        self.workingarea = None
        self.active_user = None

        self.switch_frames('LogIn')

    @property
    def active_user(self):
        return self._active_user

    @active_user.setter
    def active_user(self, username):
        self._active_user = username
        print('Aktiver User: ' + str(self._active_user))

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

        # Settings Button
        self.pictures['settings_btn_off'] = Image.open(str(os.path.join(self.pic_path, 'settings_btn_off.png')))
        self.pictures['settings_btn_on'] = Image.open(str(os.path.join(self.pic_path, 'settings_btn_on.png')))
        self.pictures['settings_btn_click'] = Image.open(str(os.path.join(self.pic_path, 'settings_btn_click.png')))

        # notifications Button
        self.pictures['notifications_btn_off'] = Image.open(
            str(os.path.join(self.pic_path, 'notifications_btn_off.png')))
        self.pictures['notifications_btn_on'] = Image.open(str(os.path.join(self.pic_path, 'notifications_btn_on.png')))
        self.pictures['notifications_btn_click'] = Image.open(
            str(os.path.join(self.pic_path, 'notifications_btn_click.png')))

        # home Button
        self.pictures['home_btn_off'] = Image.open(str(os.path.join(self.pic_path, 'home_btn_off.png')))
        self.pictures['home_btn_on'] = Image.open(str(os.path.join(self.pic_path, 'home_btn_on.png')))
        self.pictures['home_btn_click'] = Image.open(str(os.path.join(self.pic_path, 'home_btn_click.png')))

        # home neue suche Button
        self.pictures['neue_suche_home_btn_off'] = Image.open(
            str(os.path.join(self.pic_path, 'neue_suche_home_btn_off.png')))
        self.pictures['neue_suche_home_btn_on'] = Image.open(
            str(os.path.join(self.pic_path, 'neue_suche_home_btn_on.png')))
        self.pictures['neue_suche_home_btn_click'] = Image.open(
            str(os.path.join(self.pic_path, 'neue_suche_home_btn_click.png')))

        # home neue suche Button
        self.pictures['meine_suchen_home_btn_off'] = Image.open(
            str(os.path.join(self.pic_path, 'meine_suchen_home_btn_off.png')))
        self.pictures['meine_suchen_home_btn_on'] = Image.open(
            str(os.path.join(self.pic_path, 'meine_suchen_home_btn_on.png')))
        self.pictures['meine_suchen_home_btn_click'] = Image.open(
            str(os.path.join(self.pic_path, 'meine_suchen_home_btn_click.png')))

        # toggle Button
        self.pictures['toggle_off'] = Image.open(str(os.path.join(self.pic_path, 'toggle_off.png')))
        self.pictures['toggle_on'] = Image.open(str(os.path.join(self.pic_path, 'toggle_on.png')))

        # Lupe Logo
        self.pictures['lupe_logo'] = Image.open(str(os.path.join(self.pic_path, 'lupe_logo.png')))

        # trichter Logo
        self.pictures['trichter_logo'] = Image.open(str(os.path.join(self.pic_path, 'trichter_logo.png')))

        # näher betrachten Logo
        self.pictures['näher_betrachten_logo'] = Image.open(
            str(os.path.join(self.pic_path, 'näher_betrachten_logo.png')))

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
