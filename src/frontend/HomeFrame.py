import tkinter as tk
from frontend.custom_widgets.CanvasLogo import LogoCanvas
from frontend.custom_widgets.ButtonLogo import ButtonCanvas
from frontend.custom_widgets.ToggleButton import ToggleButton
from frontend.EingabeMaske import EingabeMaskeFrame
from frontend.MeineSuchen import MeineSuchenFrame
from frontend.ErgebnisFrame import ErgebnisFrame

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

UEBERSCHRIFT_DESIGN = {
    'bg': '#E2E2E2',
    'font': ('Arial', 24, 'bold'),
    # 'fg': '#618A35'
}

UEBERSCHRIFT_DESIGN_2 = {
    'bg': '#E2E2E2',
    'font': ('Arial', 20),
    # 'fg': '#618A35'
}


class HomeFrame(tk.Frame):

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent)
        self.parent = parent
        self.controller = parent

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
        letzte_suche_frame = tk.Frame(self.workingarea, bg='#E2E2E2', width=600)
        letzte_suche_frame.pack(side=tk.LEFT, fill=tk.Y,  padx=30, pady=30)
        letzte_suche_frame.bind('<ButtonPress-1>', self.bind_destroy_profilframe)
        letzte_suche_frame.pack_propagate(False)

        tk.Label(letzte_suche_frame, text='Willkommen, {}'.format(
            self.controller.active_user), **UEBERSCHRIFT_DESIGN).pack(side=tk.TOP, anchor=tk.NW)

        tk.Label(letzte_suche_frame, text='Deine letzte Suche:', **
                 UEBERSCHRIFT_DESIGN_2).pack(side=tk.TOP, anchor=tk.NW, pady=(40, 5))

        ##############################
        meine_suchen_df = self.meine_suchen_df = self.controller.backend.Suche.load_data_from_user_as_df(
            self.controller.active_user)

        suche_frame_bg = tk.Frame(letzte_suche_frame, bg='#92D050',
                                  width=600, height=500)
        suche_frame_bg.pack(side=tk.TOP, padx=20, pady=(5, 20))
        suche_frame_bg.pack_propagate(False)
        suche_frame_ = tk.Frame(suche_frame_bg, bg='#ECF7E1')
        suche_frame_.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=3, pady=3)
        suche_frame_.pack_propagate(False)

        # Abfrage ob Suchanfragen vorhanden sind
        if len(meine_suchen_df) > 0:
            dictionary = meine_suchen_df[meine_suchen_df['zeitpunkt']
                                         == meine_suchen_df['zeitpunkt'].max()].iloc[0].to_dict()

            print(dictionary)

            # Header
            header_frame = tk.Frame(suche_frame_, bg='#92D050', height=50)
            header_frame.pack(side=tk.TOP, fill=tk.X)
            tk.Label(header_frame, text=str(str(dictionary['eingaben_brand']) + ' - ' + str(dictionary['eingaben_model']) + ' - ' + str(
                dictionary['eingaben_vehicletype'])).upper().replace('_', ' '), bg='#92D050', fg='white', font=('Arial', 15)).pack(side=tk.LEFT, expand=True)

            TEXT = {
                'bg': '#ECF7E1',
                'font': ('Arial', 15)
            }
            TEXT_GREEN = {
                'bg': '#92D050',
                'font': ('Arial', 15),
                'fg': 'white'
            }

            # Erstzulassung
            erstzulassung_frame = tk.Frame(suche_frame_, bg='#ECF7E1')
            erstzulassung_frame.pack(side=tk.TOP, fill=tk.X)
            tk.Label(erstzulassung_frame, text='Erstzulassung', **
                     TEXT).pack(side=tk.LEFT, expand=False, anchor=tk.W, padx=(50, 10), pady=10)
            ez_green_frame = tk.Frame(erstzulassung_frame, bg=TEXT_GREEN['bg'], height=30, width=250)
            ez_green_frame.pack_propagate(False)
            ez_green_frame.pack(side=tk.LEFT, expand=True, anchor=tk.E, padx=(0, 50), pady=10)
            tk.Label(ez_green_frame, text=str(
                int(dictionary['eingaben_erstzulassung'])), **TEXT_GREEN).pack(expand=True)

            # kilometerstand
            kilometerstand_frame = tk.Frame(suche_frame_, bg='#ECF7E1')
            kilometerstand_frame.pack(side=tk.TOP, fill=tk.X)
            tk.Label(kilometerstand_frame, text='Kilometerstand', **
                     TEXT).pack(side=tk.LEFT, expand=False, anchor=tk.W, padx=(50, 10), pady=10)
            kilometerstand_green_frame = tk.Frame(kilometerstand_frame, bg=TEXT_GREEN['bg'], height=30, width=250)
            kilometerstand_green_frame.pack_propagate(False)
            kilometerstand_green_frame.pack(side=tk.LEFT, expand=True, anchor=tk.E, padx=(0, 50), pady=10)
            tk.Label(kilometerstand_green_frame, text=str(
                int(dictionary['eingaben_kilometerstand'])) + ' km', **TEXT_GREEN).pack(expand=True)

            # leistung
            leistung_frame = tk.Frame(suche_frame_, bg='#ECF7E1')
            leistung_frame.pack(side=tk.TOP, fill=tk.X)
            tk.Label(leistung_frame, text='Leistung', **
                     TEXT).pack(side=tk.LEFT, expand=False, anchor=tk.W, padx=(50, 10), pady=10)
            leistung_green_frame = tk.Frame(leistung_frame, bg=TEXT_GREEN['bg'], height=30, width=250)
            leistung_green_frame.pack_propagate(False)
            leistung_green_frame.pack(side=tk.LEFT, expand=True, anchor=tk.E, padx=(0, 50), pady=10)
            tk.Label(leistung_green_frame, text=str(
                int(dictionary['eingaben_leistung_ps'])) + ' PS', **TEXT_GREEN).pack(expand=True)

            # getriebe
            getriebe_frame = tk.Frame(suche_frame_, bg='#ECF7E1')
            getriebe_frame.pack(side=tk.TOP, fill=tk.X)
            tk.Label(getriebe_frame, text='Getriebe', **
                     TEXT).pack(side=tk.LEFT, expand=False, anchor=tk.W, padx=(50, 10), pady=10)
            getriebe_green_frame = tk.Frame(getriebe_frame, bg=TEXT_GREEN['bg'], height=30, width=250)
            getriebe_green_frame.pack_propagate(False)
            getriebe_green_frame.pack(side=tk.LEFT, expand=True, anchor=tk.E, padx=(0, 50), pady=10)
            tk.Label(getriebe_green_frame, text=str(
                dictionary['eingaben_getriebe']), **TEXT_GREEN).pack(expand=True)

            # kraftstoff
            kraftstoff_frame = tk.Frame(suche_frame_, bg='#ECF7E1')
            kraftstoff_frame.pack(side=tk.TOP, fill=tk.X)
            tk.Label(kraftstoff_frame, text='Kraftstoff', **
                     TEXT).pack(side=tk.LEFT, expand=False, anchor=tk.W, padx=(50, 10), pady=10)
            kraftstoff_green_frame = tk.Frame(kraftstoff_frame, bg=TEXT_GREEN['bg'], height=30, width=250)
            kraftstoff_green_frame.pack_propagate(False)
            kraftstoff_green_frame.pack(side=tk.LEFT, expand=True, anchor=tk.E, padx=(0, 50), pady=10)
            tk.Label(kraftstoff_green_frame, text=str(
                dictionary['eingaben_fueltype']), **TEXT_GREEN).pack(expand=True)

            # preis
            preis_frame = tk.Frame(suche_frame_, bg='#ECF7E1')
            preis_frame.pack(side=tk.TOP, fill=tk.X)
            tk.Label(preis_frame, text='Prognostizierter\nPreis', **
                     TEXT, justify=tk.LEFT).pack(side=tk.LEFT, expand=False, anchor=tk.W, padx=(50, 10), pady=10)
            preis_green_frame = tk.Frame(preis_frame, bg=TEXT_GREEN['bg'], height=30, width=250)
            preis_green_frame.pack_propagate(False)
            preis_green_frame.pack(side=tk.LEFT, expand=True, anchor=tk.E, padx=(0, 50), pady=10)
            tk.Label(preis_green_frame, text=str(int(
                dictionary['prognose_preis'])) + ' €', anchor=tk.W, **TEXT_GREEN).pack(expand=True)

            #####
            # Button
            def command_ergebnis(*args):

                dic = dictionary

                for widgets in self.workingarea.winfo_children():
                    widgets.forget()
                ErgebnisFrame(self.workingarea, self.controller, regression_daten_dic={
                    'brand': dic['eingaben_brand'],
                    'model': dic['eingaben_model'],
                    'vehicletype': dic['eingaben_vehicletype'],
                    'auto_alter': 2016 - int(dic['eingaben_erstzulassung']),
                    'auto_leistung_ps': int(dic['eingaben_leistung_ps']),
                    'auto_kilometerstand': int(dic['eingaben_kilometerstand']),
                    'getriebe': dic['eingaben_getriebe'],
                    'antriebsart': dic['eingaben_fueltype'],
                    'schaden_vorhanden': dic['eingaben_schaden_vorhanden'],
                    'erstzulassung': int(dic['eingaben_erstzulassung'])
                }, save=False).pack(fill=tk.BOTH, expand=True)

            btn = tk.Button(suche_frame_, text='Letzte Suche öffnen', command=command_ergebnis,
                            bg='#92D050', font=('Arial', 18, 'bold'), cursor='hand2', fg='white')
            btn.pack(side=tk.BOTTOM, anchor=tk.E, padx=10, pady=10)
            btn.bind('<Enter>', lambda *args: btn.config(bg='#C7E7A6', fg='white'))
            btn.bind('<Leave>', lambda *args: btn.config(bg='#92D050', fg='white'))

        ###############################################
        ###############################################
        else:
            tk.Label(suche_frame_, text='Du hast noch keine Suchen durchgeführt.',
                     font=('Arial', 17), bg='#ECF7E1').pack(
                side=tk.TOP, expand=True, anchor=tk.S)

            label_suche_starten = tk.Label(suche_frame_, text='Starte deine erste Suche',
                                           font=('Arial', 17, 'bold'), bg='#ECF7E1', fg='#618A35', cursor='hand2')
            label_suche_starten.pack(
                side=tk.TOP, expand=True, pady=20, anchor=tk.N)
            label_suche_starten.bind('<Enter>', lambda *args: label_suche_starten.config(fg='#92D050'))
            label_suche_starten.bind('<Leave>', lambda *args: label_suche_starten.config(fg='#618A35'))
            label_suche_starten.bind('<Button-1>', self.command_eingabemaske_oeffnen)

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
