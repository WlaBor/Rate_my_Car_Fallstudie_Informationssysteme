import tkinter as tk
from frontend.custom_widgets.CanvasLogo import LogoCanvas
from frontend.custom_widgets.ButtonLogo import ButtonCanvas

PROFIL_BUTTONS_DESIGN = {
    'bg': '#92D050',
    'highlightthickness': 0,
    'bd': 0,
    'font': ('Arial', 12),
    'cursor': 'hand2'
}

PROFIL_BUTTONS_DESIGN_ON = {
    'bg': '#F6FBF1',
    'highlightthickness': 0,
    'bd': 0,
    'font': ('Arial', 12),
    'cursor': 'hand2'
}


class HomeFrame(tk.Frame):

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent)
        self.parent = parent

        self.layout()

    def layout(self):
        # Hintergrund
        self.config(bg='yellow')

        # Navigationsbar
        navbar = tk.Frame(self, bg='#92D050', height=100)
        navbar.pack(side=tk.TOP, fill=tk.X)
        self.navbar = navbar

        # Logo
        # self.parent.pictures['logo']
        logo = LogoCanvas(parent=navbar, controller=self.parent, image_name='logo', size=(200, 60))
        logo.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        mein_profil = ButtonCanvas(parent=navbar, controller=self.parent,
                                   off_pic='profil_btn_off',
                                   on_pic='profil_btn_on',
                                   click_pic='profil_btn_click',
                                   size=(60, 60),
                                   command=self.command_click_profil)
        mein_profil.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

        # Working area
        workingarea = tk.Frame(self, bg='gray')
        workingarea.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        workingarea.bind('<ButtonPress-1>', self.bind_destroy_profilframe)
        navbar.bind('<ButtonPress-1>', self.bind_destroy_profilframe)

    def bind_destroy_profilframe(self, *args):
        try:
            self.profil_frame.destroy()
        except:
            pass

    def command_click_profil(self):
        self.bind_destroy_profilframe()
        background = tk.Frame(self, bg=PROFIL_BUTTONS_DESIGN_ON['bg'])
        background.place(relx=1, rely=0, x=-10, y=70, anchor=tk.NE)
        self.profil_frame = background

        frame = tk.Frame(background, bg='#92D050')
        frame.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)

        # Abmelden
        def abmelden():
            self.parent.switch_frames('LogIn')
            self.destroy()

        btn_abmelden = tk.Button(frame, text='Abmelden', command=abmelden, **PROFIL_BUTTONS_DESIGN)
        btn_abmelden.pack(side=tk.TOP, fill=tk.X, padx=1, pady=0)
        btn_abmelden.bind('<Enter>', lambda *args: btn_abmelden.config(**PROFIL_BUTTONS_DESIGN_ON))
        btn_abmelden.bind('<Leave>', lambda *args: btn_abmelden.config(**PROFIL_BUTTONS_DESIGN))

        # Suchverlauf
        btn_suchen = tk.Button(frame, text='Meine Suchen', **PROFIL_BUTTONS_DESIGN)
        btn_suchen.pack(side=tk.TOP, fill=tk.X, padx=1, pady=0)
        btn_suchen.bind('<Enter>', lambda *args: btn_suchen.config(**PROFIL_BUTTONS_DESIGN_ON))
        btn_suchen.bind('<Leave>', lambda *args: btn_suchen.config(**PROFIL_BUTTONS_DESIGN))

        # Benutzerdaten ändern
        btn_benutzer = tk.Button(frame, text='Benutzerdaten', **PROFIL_BUTTONS_DESIGN)
        btn_benutzer.pack(side=tk.TOP, fill=tk.X, padx=1, pady=0)
        btn_benutzer.bind('<Enter>', lambda *args: btn_benutzer.config(**PROFIL_BUTTONS_DESIGN_ON))
        btn_benutzer.bind('<Leave>', lambda *args: btn_benutzer.config(**PROFIL_BUTTONS_DESIGN))

        # Passwort ändern
        btn_pw = tk.Button(frame, text='Passwort ändern', **PROFIL_BUTTONS_DESIGN)
        btn_pw.pack(side=tk.TOP, fill=tk.X, padx=1, pady=0)
        btn_pw.bind('<Enter>', lambda *args: btn_pw.config(**PROFIL_BUTTONS_DESIGN_ON))
        btn_pw.bind('<Leave>', lambda *args: btn_pw.config(**PROFIL_BUTTONS_DESIGN))
