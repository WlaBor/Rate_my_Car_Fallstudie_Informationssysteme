import tkinter as tk
from frontend.custom_widgets.CanvasLogo import LogoCanvas
from frontend.custom_widgets.ButtonLogo import ButtonCanvas
from frontend.custom_widgets.ToggleButton import ToggleButton
from frontend.EingabeMaske import EingabeMaskeFrame
from frontend.MeineSuchen import MeineSuchenFrame

PROFIL_BUTTONS_DESIGN = {
    'bg': '#92D050',
    'highlightthickness': 0,
    'bd': 0,
    'font': ('Arial', 12),
    'cursor': 'hand2',
    'anchor': 'w'
}

PROFIL_LABEL_DESIGN = {
    'bg': '#92D050',
    'highlightthickness': 0,
    'bd': 0,
    'font': ('Arial', 12),
    'anchor': 'w'
}

PROFIL_BUTTONS_DESIGN_ON = {
    'bg': '#F6FBF1',
    'highlightthickness': 0,
    'bd': 0,
    'font': ('Arial', 12),
    'cursor': 'hand2',
    'anchor': 'w'
}


class HomeFrame(tk.Frame):

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent)
        self.parent = parent

        self.layout()

        self.parent.command_home = self.command_home

    def layout(self):
        # Navigationsbar
        navbar = tk.Frame(self, bg='#92D050', height=100)
        navbar.pack(side=tk.TOP, fill=tk.X)
        self.navbar = navbar
        self.layout_navbar()

        # Working area
        workingarea = tk.Frame(self)
        workingarea.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.workingarea = workingarea
        self.parent.workingarea = workingarea
        self.layout_workingarea()

        global closed
        closed = True

    # ////////////////////////////////////////////
    # Layout Navigationsleiste
    def layout_navbar(self):
        # ////////////////////////////////////////////
        # Logo
        # self.parent.pictures['logo']
        logo = LogoCanvas(parent=self.navbar, controller=self.parent, image_name='logo', size=(200, 60))
        logo.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        icon_size = (45, 45)
        # ////////////////////////////////////////////
        # Mein Profil
        mein_profil = ButtonCanvas(parent=self.navbar, controller=self.parent,
                                   off_pic='profil_btn_off',
                                   on_pic='profil_btn_on',
                                   click_pic='profil_btn_click',
                                   size=icon_size,
                                   command=self.command_click_profil)
        mein_profil.pack(side=tk.RIGHT,  padx=(0, 10), pady=10)
        self.btn_meinprofil = mein_profil

        # ////////////////////////////////////////////
        # SETTINGS
        settings_btn = ButtonCanvas(parent=self.navbar, controller=self.parent,
                                    off_pic='settings_btn_off',
                                    on_pic='settings_btn_on',
                                    click_pic='settings_btn_click',
                                    size=icon_size,
                                    command=None)
        settings_btn.pack(side=tk.RIGHT, padx=0, pady=10)
        self.btn_settings = settings_btn

        # ////////////////////////////////////////////
        # notifications
        notifications_btn = ButtonCanvas(parent=self.navbar, controller=self.parent,
                                         off_pic='notifications_btn_off',
                                         on_pic='notifications_btn_on',
                                         click_pic='notifications_btn_click',
                                         size=icon_size,
                                         command=None)
        notifications_btn.pack(side=tk.RIGHT, padx=0, pady=10)
        self.btn_notifications = notifications_btn

        # ////////////////////////////////////////////
        # home
        home_btn = ButtonCanvas(parent=self.navbar, controller=self.parent,
                                off_pic='home_btn_off',
                                on_pic='home_btn_on',
                                click_pic='home_btn_click',
                                size=icon_size,
                                command=self.command_home)
        home_btn.pack(side=tk.RIGHT, padx=0, pady=10)
        self.btn_home = home_btn

        self.navbar.bind('<ButtonPress-1>', self.bind_destroy_profilframe)

    # ////////////////////////////////////////////
    # Command und Bindings für Mein Profil
    def bind_destroy_profilframe(self, *args):
        try:
            self.profil_frame.destroy()
        except:
            pass
        global closed
        closed = True

    def command_click_profil(self):
        global closed

        if closed == False:
            self.bind_destroy_profilframe()
            self.btn_meinprofil.canvas.config(bg='#92D050')
        else:
            background = tk.Frame(self, bg=PROFIL_BUTTONS_DESIGN_ON['bg'])
            background.place(relx=1, rely=0, x=-10, y=70, anchor=tk.NE)
            self.profil_frame = background

            frame = tk.Frame(background, bg='#92D050')
            frame.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)

            # Abmelden
            def abmelden():
                self.parent.active_user = None
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

            # Premium Account
            is_premium = self.parent.backend.User.check_UserPremium(str(self.parent.active_user))
            # print(is_premium)
            if is_premium == 0:
                is_premium = 'off'
            elif is_premium == 1:
                is_premium = 'on'
            else:
                is_premium = 'off'

            # print(is_premium)

            frame_premium = tk.Frame(frame, bg='#92D050')
            frame_premium.pack(side=tk.TOP, fill=tk.X, padx=1, pady=0)
            tk.Label(frame_premium, text='Premium?', **PROFIL_LABEL_DESIGN).pack(side=tk.LEFT)
            toggle_button = ToggleButton(frame_premium, self.parent, (45, 15), state=is_premium,
                                         on_command=lambda *args: self.parent.backend.User.activate_premium(
                                             str(self.parent.active_user)),
                                         off_command=lambda *args: self.parent.backend.User.deactivate_premium(str(self.parent.active_user)))
            toggle_button.pack(side=tk.RIGHT, expand=True)

            closed = False
            self.btn_meinprofil.canvas.config(bg='white')

    # ////////////////////////////////////////////
    # Layout Arbeitsframe
    def layout_workingarea(self):
        self.workingarea.config(bg='#E2E2E2')
        self.workingarea.bind('<ButtonPress-1>', self.bind_destroy_profilframe)

        # Meine letzte Suche
        letzte_suche_frame = tk.Frame(self.workingarea, bg='#C1C1C1', width=600)
        letzte_suche_frame.pack(side=tk.LEFT, fill=tk.Y,  padx=30, pady=30)
        letzte_suche_frame.bind('<ButtonPress-1>', self.bind_destroy_profilframe)

        # ////////////////////////////////////////////

        # Button Frame
        button_frame = tk.Frame(self.workingarea, bg='#E2E2E2', height=150)
        button_frame.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=30, pady=30, anchor=tk.N)
        button_frame.grid_columnconfigure(0, weight=1, uniform='col')
        button_frame.grid_columnconfigure(1, weight=1, uniform='col')
        button_frame.grid_rowconfigure(0, weight=1, uniform='row')
        button_frame.bind('<ButtonPress-1>', self.bind_destroy_profilframe)

        # ////////////////////////////////////////////
        button_size = (int(600*0.6), int(180*0.6))
        # home
        suche_btn = ButtonCanvas(parent=button_frame, controller=self.parent,
                                 off_pic='neue_suche_home_btn_off',
                                 on_pic='neue_suche_home_btn_on',
                                 click_pic='neue_suche_home_btn_click',
                                 size=button_size,
                                 command=self.command_eingabemaske_oeffnen)
        suche_btn.grid(row=0, column=0, padx=(10, 5), pady=10, sticky=tk.S)

        meine_suchen_btn = ButtonCanvas(parent=button_frame, controller=self.parent,
                                        off_pic='meine_suchen_home_btn_off',
                                        on_pic='meine_suchen_home_btn_on',
                                        click_pic='meine_suchen_home_btn_click',
                                        size=button_size,
                                        command=self.command_meinesuchen_oeffnen)
        meine_suchen_btn.grid(row=0, column=1, padx=(5, 10), pady=10, sticky=tk.N)

    # ////////////////////////////////////////////
    # Eingabemaske
    def command_eingabemaske_oeffnen(self, *args):
        for widget in self.workingarea.winfo_children():
            widget.forget()
        eingabemaske = EingabeMaskeFrame(self.workingarea, self.parent)
        eingabemaske.pack(fill=tk.BOTH, expand=True)

    # ////////////////////////////////////////////
    # Eingabemaske
    def command_meinesuchen_oeffnen(self, *args):
        for widget in self.workingarea.winfo_children():
            widget.forget()
        meinesuchen = MeineSuchenFrame(self.workingarea, self.parent)
        meinesuchen.pack(fill=tk.BOTH, expand=True)

    # ////////////////////////////////////////////
    # Home Taste
    def command_home(self, *args):
        for widget in self.workingarea.winfo_children():
            widget.destroy()
        self.layout_workingarea()
