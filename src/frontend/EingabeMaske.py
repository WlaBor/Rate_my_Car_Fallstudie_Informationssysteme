import tkinter as tk
from tkinter import ttk
from frontend.custom_widgets.CanvasLogo import LogoCanvas
from frontend.custom_widgets.EingabemaskeCombobox import EingabemaskeCombobox
from frontend.ErgebnisFrame import ErgebnisFrame
from datetime import date

UEBERSCHRIFT_DESIGN = {
    'bg': '#E2E2E2',
    'font': ('Arial', 24, 'bold')
}

FRAGE_LABEL_DESIGN = {
    'bg': '#E2E2E2',
    'font': ('Arial', 22)
}

BUTTON_DESIGN = {
    'font': ('Arial', 22),
    'bg': '#92D050',
    'width': 20,
    'cursor': 'hand2'
}

BACKGROUND = '#E2E2E2'


class EingabeMaskeFrame(tk.Frame):

    def __init__(self, parent, controller, *args, **kwargs):
        super().__init__(parent)
        self.parent = parent
        self.controller = controller

        self.auto_marken = self.controller.backend.Automodel.get_unqiue_marken()
        print(self.auto_marken)

        self.betrachtungs_raum = {
            'marke': None,
            'model': None,
            'typ': None
        }

        self.regression_eingaben = {
            'erstzulassung': 2016,
            'leistung': 0,
            'kilometerstand': 0,
            'getriebe': None,
            'antrieb': None,
            'autoschaden': 0
        }

        self.layout()

    @property
    def betrachtungs_raum(self):
        return self._betrachtungs_raum

    @betrachtungs_raum.setter
    def betrachtungs_raum(self, value_dic):
        self._betrachtungs_raum = value_dic
        # print(value_dic)
        if None not in list(value_dic.values()):
            try:
                self.btn_weiter.pack(side=tk.LEFT, fill=tk.Y, pady=10, padx=10)
            except:
                pass
        else:
            try:
                self.btn_weiter.forget()
            except:
                pass

    def layout(self):
        self.config(bg='#E2E2E2')

        # Arbeitsbereich
        frame_left = tk.Frame(self, bg=BACKGROUND)
        frame_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Frame auf der rechten Seite, evtl. für Werbung
        frame_right = tk.Frame(self, bg=BACKGROUND, width=400)
        frame_right.pack(side=tk.LEFT, fill=tk.Y, padx=20, pady=20)

        # Logo und Überschrift oben links
        logo_frame = tk.Frame(frame_left, bg=BACKGROUND)
        logo_frame.pack(side=tk.TOP, anchor=tk.W, pady=20, padx=20)
        logo = LogoCanvas(logo_frame, self.controller, size=(50, 50), image_name='lupe_logo', bg='#E2E2E2')
        logo.pack(side=tk.LEFT)
        self.logo = logo
        tk.Label(logo_frame, text='Neue Suche', **UEBERSCHRIFT_DESIGN).pack(side=tk.LEFT, padx=0)

        #  Überschrift 2: Fragestellung
        frage_frame = tk.Frame(frame_left, bg=BACKGROUND)
        frage_frame.pack(side=tk.TOP, anchor=tk.W, pady=30, padx=(150, 20))
        trichter_logo = LogoCanvas(frage_frame, self.controller, size=(40, 40),
                                   image_name='trichter_logo', bg=BACKGROUND)
        trichter_logo.pack(side=tk.LEFT)
        self.trichter_logo = trichter_logo
        frage_label = tk.Label(frage_frame, text='Wonach suchst du?', **FRAGE_LABEL_DESIGN)
        frage_label.pack(side=tk.LEFT, padx=0)
        self.frage_label = frage_label

        # Eingabebereich
        eingabe_frame = tk.Frame(frame_left, bg=BACKGROUND)
        eingabe_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=(160, 20))
        self.eingabe_frame = eingabe_frame
        self.design_eingabe_frame()

        # Button Bereich
        button_frame = tk.Frame(frame_left, bg=BACKGROUND, height=100)
        button_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=(150, 20), pady=20)
        self.button_frame = button_frame
        self.design_button_frame()

    # ////////////////////////////////////////////
    # Eingabebereich 1
    def design_eingabe_frame(self):
        # Automarke
        self.cb_marke = EingabemaskeCombobox(parent=self.eingabe_frame, controller=self.controller,
                                             text='Welche Marke sollen wir betrachten?', bg=BACKGROUND, values=self.auto_marken)
        self.cb_marke.pack(side=tk.TOP, fill=tk.X)
        self.cb_marke.combobox.bind("<<ComboboxSelected>>", self.select_marke)

        # Automodell
        self.cb_model = EingabemaskeCombobox(parent=self.eingabe_frame, controller=self.controller,
                                             text='Und was für ein Modell?', bg=BACKGROUND, values=[])

        self.cb_model.combobox.bind("<<ComboboxSelected>>", self.select_model)

        # Autotyp
        self.cb_typ = EingabemaskeCombobox(parent=self.eingabe_frame, controller=self.controller,
                                           text='Was für eine Form hat das Auto?', bg=BACKGROUND, values=[])
        self.cb_typ.combobox.bind("<<ComboboxSelected>>", self.select_type)

    # Automarke
    def select_marke(self, *args):
        marke = self.cb_marke.value

        modelle = self.controller.backend.Automodel.get_unique_models_from_brand(marke)

        self.cb_model.values = modelle

        self.cb_model.forget()
        self.cb_typ.forget()
        self.cb_model.combobox.set('')
        self.cb_model.pack(side=tk.TOP, fill=tk.X, pady=5)

        self.betrachtungs_raum = {
            'marke': marke,
            'model': None,
            'typ': None
        }

        print(modelle)

    def select_model(self, *args):
        marke = self.cb_marke.value
        model = self.cb_model.value

        types = self.controller.backend.Automodel.get_unique_cartype_from_brand_model(marke, model)
        print(types)

        self.cb_typ.values = types

        self.cb_typ.forget()
        self.cb_typ.combobox.set('')
        self.cb_typ.pack(side=tk.TOP, fill=tk.X, pady=5)
        self.betrachtungs_raum = {
            'marke': marke,
            'model': model,
            'typ': None
        }

    def select_type(self, *args):
        marke = self.cb_marke.value
        model = self.cb_model.value
        typ = self.cb_typ.value

        self.betrachtungs_raum = {
            'marke': marke,
            'model': model,
            'typ': typ
        }

    # ////////////////////////////////////////////
    # BUTTON
    def design_button_frame(self):
        def command_weiter(*args):
            for widget in self.eingabe_frame.winfo_children():
                widget.forget()
            self.eingabemaske_regression()

            for widget in self.button_frame.winfo_children():
                widget.forget()
            self.button_frame_regression()

            self.frage_label.config(text='Nenn uns nähere Daten zu dem Auto:')

            self.trichter_logo.change_pic('näher_betrachten_logo')

        self.btn_weiter = tk.Button(self.button_frame, text='Weiter', command=command_weiter, ** BUTTON_DESIGN)
        self.btn_weiter.bind('<Enter>', lambda *args: self.btn_weiter.config(bg='#C7E7A6'))
        self.btn_weiter.bind('<Leave>', lambda *args: self.btn_weiter.config(bg='#92D050'))

        # Abbrechen Button
        self.btn_abbrechen = tk.Button(self.button_frame, text='Abbrechen', command=self.controller.command_home,
                                       **BUTTON_DESIGN)
        self.btn_abbrechen.pack(pady=10, padx=10, side=tk.LEFT)

        self.btn_abbrechen.bind('<Enter>', lambda *args: self.btn_abbrechen.config(bg='#C7E7A6'))
        self.btn_abbrechen.bind('<Leave>', lambda *args: self.btn_abbrechen.config(bg='#92D050'))

    # ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # Eingabemaske 2 -> Eingaben für die Regression

    def validate(self, val):
        return val.isdigit() or str(val) == ''

    def eingabemaske_regression(self):
        font = ('Arial', 18)
        PADY = 10

        eingabeframe_regression = tk.Frame(self.eingabe_frame, bg=BACKGROUND)
        eingabeframe_regression.pack(fill=tk.BOTH, expand=True)

        # Erstzulassung
        tk.Label(eingabeframe_regression, text='Erstzulassung:',
                 bg=BACKGROUND, font=font).grid(row=0, column=0, sticky=tk.W, pady=(5, PADY))
        if not hasattr(self, 'var_erstzulassung'):
            self.var_erstzulassung = tk.StringVar(value=2016)
            self.var_erstzulassung.trace_add(
                'write', lambda *args: self.command_set_regression_eingaben('erstzulassung', self.var_erstzulassung.get()))

        tk.Spinbox(eingabeframe_regression,  from_=0,
                   to=2016, validate='key', validatecommand=(self.controller.register(self.validate), '%P'), textvariable=self.var_erstzulassung, font=font, width=15).grid(row=0, column=1, sticky=tk.W, padx=40)

        # Leistung
        tk.Label(eingabeframe_regression, text='Leistung [PS]:',
                 bg=BACKGROUND, font=font).grid(row=1, column=0, sticky=tk.W, pady=PADY)
        if not hasattr(self, 'var_leistung'):
            self.var_leistung = tk.StringVar()
            self.var_leistung.trace_add(
                'write', lambda *args: self.command_set_regression_eingaben('leistung', self.var_leistung.get()))

        tk.Spinbox(eingabeframe_regression,  from_=0,
                   to=10000, textvariable=self.var_leistung, validate='key', validatecommand=(self.controller.register(self.validate), '%P'), font=font, width=15).grid(row=1, column=1, sticky=tk.W, padx=40)

        # Kilometerstand
        tk.Label(eingabeframe_regression, text='Kilometerstand:',
                 bg=BACKGROUND, font=font).grid(row=2, column=0, sticky=tk.W, pady=PADY)
        if not hasattr(self, 'var_kilometer'):
            self.var_kilometer = tk.StringVar()
            self.var_kilometer.trace_add(
                'write', lambda *args: self.command_set_regression_eingaben('kilometerstand', self.var_kilometer.get()))

        tk.Spinbox(eingabeframe_regression,  from_=0,
                   to=10000000, textvariable=self.var_kilometer, validate='key', validatecommand=(self.controller.register(self.validate), '%P'), font=font, width=15).grid(row=2, column=1, sticky=tk.W, padx=40)

        # Getriebe
        tk.Label(eingabeframe_regression, text='Getriebe:', bg=BACKGROUND,
                 font=font).grid(row=3, column=0, sticky=tk.W, pady=PADY)

        if not hasattr(self, 'var_getriebe'):
            self.var_getriebe = tk.StringVar()
            self.var_getriebe.trace_add(
                'write', lambda *args: self.command_set_regression_eingaben('getriebe', self.var_getriebe.get()))
        ttk.Combobox(eingabeframe_regression, textvariable=self.var_getriebe, font=font,
                     state="readonly", values=['Manuell', 'Automatik'], width=15).grid(row=3, column=1, sticky=tk.W, padx=40)

        # Antrieb
        tk.Label(eingabeframe_regression, text='Antrieb:', bg=BACKGROUND,
                 font=font).grid(row=4, column=0, sticky=tk.W, pady=PADY)

        if not hasattr(self, 'var_antrieb'):
            self.var_antrieb = tk.StringVar()
            self.var_antrieb.trace_add(
                'write', lambda *args: self.command_set_regression_eingaben('antrieb', self.var_antrieb.get()))
        ttk.Combobox(eingabeframe_regression, textvariable=self.var_antrieb, font=font,
                     state="readonly", values=['Benzin', 'Diesel', 'LPG', 'CNG', 'Hybrid', 'Elektro'], width=15).grid(row=4, column=1, sticky=tk.W, padx=40)

        # Autoschaden
        tk.Label(eingabeframe_regression, text='Autoschaden vorhanden?:',
                 bg=BACKGROUND, font=font).grid(row=5, column=0, sticky=tk.W, pady=PADY)

        if not hasattr(self, 'var_schaden'):
            self.var_schaden = tk.IntVar()
            self.var_schaden.trace_add(
                'write', lambda *args: self.command_set_regression_eingaben('autoschaden', self.var_schaden.get()))
        c1 = tk.Checkbutton(eingabeframe_regression, text='Ja', variable=self.var_schaden, onvalue=1, offvalue=0, bg=BACKGROUND,
                            font=font)
        c1.grid(row=5, column=1, sticky=tk.W, padx=(40, 5))
        c2 = tk.Checkbutton(eingabeframe_regression, text='Nein', variable=self.var_schaden, onvalue=0, offvalue=1, bg=BACKGROUND,
                            font=font)
        c2.grid(row=5, column=1, sticky=tk.E, padx=20)

    # ////////////////////////////////////////////
    def button_frame_regression(self):
        # Abbrechen Button
        self.btn_abbrechen.pack(pady=10, padx=10, side=tk.LEFT)

        self.btn_abbrechen.bind('<Enter>', lambda *args: self.btn_abbrechen.config(bg='#C7E7A6'))
        self.btn_abbrechen.bind('<Leave>', lambda *args: self.btn_abbrechen.config(bg='#92D050'))

        # Zurück Button
        def command_zurueck(*args):
            for widget in self.eingabe_frame.winfo_children():
                widget.forget()
            self.cb_marke.pack(side=tk.TOP, fill=tk.X)
            self.cb_model.pack(side=tk.TOP, fill=tk.X)
            self.cb_typ.pack(side=tk.TOP, fill=tk.X)

            for widget in self.button_frame.winfo_children():
                widget.forget()
            self.btn_abbrechen.pack(pady=10, padx=10, side=tk.LEFT)
            self.btn_weiter.pack(pady=10, padx=10, side=tk.LEFT)

            self.frage_label.config(text='Wonach suchst du?')

            self.trichter_logo.change_pic('trichter_logo')

        if not hasattr(self, 'btn_back'):
            self.btn_back = tk.Button(self.button_frame, text='Zurück', command=command_zurueck,
                                      **BUTTON_DESIGN)
        self.btn_back.pack(pady=10, padx=10, side=tk.LEFT)
        self.btn_back.bind('<Enter>', lambda *args: self.btn_back.config(bg='#C7E7A6'))
        self.btn_back.bind('<Leave>', lambda *args: self.btn_back.config(bg='#92D050'))

        # Weiter Button in Regression
        if not hasattr(self, 'btn_weiter_regression'):
            self.btn_weiter_regression = tk.Button(self.button_frame, text='Ergebnis', command=None, ** BUTTON_DESIGN)

        def command_ergebnis(*args):
            for widgets in self.winfo_children():
                widgets.forget()
            ErgebnisFrame(self, self.controller, regression_daten_dic={
                'brand': self.betrachtungs_raum['marke'],
                'model': self.betrachtungs_raum['model'],
                'vehicletype': self.betrachtungs_raum['typ'],
                'auto_alter': 2016 - int(self.regression_eingaben['erstzulassung']),
                'auto_leistung_ps': self.regression_eingaben['leistung'],
                'auto_kilometerstand': self.regression_eingaben['kilometerstand'],
                'getriebe': self.regression_eingaben['getriebe'],
                'antriebsart': self.regression_eingaben['antrieb'],
                'schaden_vorhanden': self.regression_eingaben['autoschaden'],
                'erstzulassung': int(self.regression_eingaben['erstzulassung'])
            }).pack(fill=tk.BOTH, expand=True)

        self.btn_weiter_regression.config(command=command_ergebnis)
        self.btn_weiter_regression.bind('<Enter>', lambda *args: self.btn_weiter_regression.config(bg='#C7E7A6'))
        self.btn_weiter_regression.bind('<Leave>', lambda *args: self.btn_weiter_regression.config(bg='#92D050'))

        if None not in list(self.regression_eingaben.values()):
            # Zeige Button
            self.btn_weiter_regression.pack(pady=10, padx=10, side=tk.LEFT)
        #self.btn_weiter_regression.pack(pady=10, padx=10, side=tk.LEFT)

    # ////////////////////////////////////////////
    def command_set_regression_eingaben(self, key, value):
        if not hasattr(self, 'btn_weiter_regression'):
            return
        self.regression_eingaben[key] = value

        if None not in list(self.regression_eingaben.values()):
            # Zeige Button
            self.btn_weiter_regression.pack(pady=10, padx=10, side=tk.LEFT)
        else:
            self.btn_weiter_regression.forget()
