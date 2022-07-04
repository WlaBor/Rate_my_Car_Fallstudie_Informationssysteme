import tkinter as tk
from backend.prognose import Prognose
import string
from frontend.custom_widgets.CanvasLogo import LogoCanvas
from frontend.custom_widgets.ErgebnisSubFrames import ErgebnisSubFrame
from frontend.custom_widgets.ErgebnisSubFrameGrey import ErgebnisSubFrameGrey
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import pandas as pd
import numpy as np

SUBFRAME_DESIGN = {
    'bg': '#C7E7A6'
}


class ErgebnisFrame(tk.Frame):

    def __init__(self, parent, controller, regression_daten_dic, *args, **kwargs):
        super().__init__(parent)
        self.parent = parent
        self.controller = controller
        self.regression_daten_dic = regression_daten_dic

        try:
            self.prognosemodel = Prognose(controller=self.controller, **self.regression_daten_dic)
        except Exception as ex:
            print('Error')
            print(ex)
            tk.messagebox.showerror('Achtung', 'Zu wenig Daten für die Auswertung.')
            self.controller.command_home()

        self.raw_df = self.controller.backend.Anzeige.load_data_as_df(brand=self.regression_daten_dic['brand'],
                                                                      model=self.regression_daten_dic['model'],
                                                                      vehicletype=self.regression_daten_dic['vehicletype'])

        self.filter_df = self.controller.backend.Anzeige.load_data_with_filter(brand=self.regression_daten_dic['brand'],
                                                                               model=self.regression_daten_dic['model'],
                                                                               vehicletype=self.regression_daten_dic['vehicletype'])

        self.preisprognose = self.prognosemodel.make_prediction()
        print('Prognostizierter Preis: ' + str(round(self.preisprognose, 2)))

        # Check Premium
        if self.controller.backend.User.check_UserPremium(self.controller.active_user) == 1:
            self.layout_premium()
        else:
            self.layout_standard()

    ################
    # Layout für Premium User
    def layout_premium(self):
        self.config(bg='#E2E2E2')

        UEBERSCHRIFT1 = {
            'font': ('Arial', 22, 'bold'),
            'bg': '#E2E2E2'
        }

        UEBERSCHRIFT2 = {
            'font': ('Arial', 20),
            'bg': '#E2E2E2'
        }

        # Überschrift
        tk.Label(self, text='Preisanalyse', **UEBERSCHRIFT1).pack(side=tk.TOP, anchor=tk.W, padx=20, pady=(20, 2))
        tk.Label(self, text=str(str(self.regression_daten_dic['brand'])+' '+str(self.regression_daten_dic['model'])+' '+str(
            self.regression_daten_dic['vehicletype'])).upper(), **UEBERSCHRIFT2).pack(side=tk.TOP, anchor=tk.W, padx=20)

        # Unterer Berreich
        lower_frame = tk.Frame(self, bg='#E2E2E2')
        lower_frame.pack(side=tk.TOP, expand=True, fill=tk.BOTH)

        # daten frame
        daten_frame = tk.Frame(lower_frame, bg='#E2E2E2', width=800)
        daten_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(20, 0), pady=20)
        daten_frame.pack_propagate(False)
        self.layout_daten_frame(daten_frame)

        # grafik frame
        grafik_frame = tk.Frame(lower_frame, bg='#E2E2E2')
        grafik_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)
        self.show_plot(grafik_frame)

    ################
    # Layount für Standard User

    def layout_standard(self):
        self.config(bg='#E2E2E2')

        UEBERSCHRIFT1 = {
            'font': ('Arial', 22, 'bold'),
            'bg': '#E2E2E2'
        }

        UEBERSCHRIFT2 = {
            'font': ('Arial', 20),
            'bg': '#E2E2E2'
        }

        # Überschrift
        tk.Label(self, text='Preisanalyse', **UEBERSCHRIFT1).pack(side=tk.TOP, anchor=tk.W, padx=20, pady=(20, 2))
        tk.Label(self, text=str(str(self.regression_daten_dic['brand'])+' '+str(self.regression_daten_dic['model'])+' '+str(
            self.regression_daten_dic['vehicletype'])).upper(), **UEBERSCHRIFT2).pack(side=tk.TOP, anchor=tk.W, padx=20)

        # Unterer Berreich
        lower_frame = tk.Frame(self, bg='#E2E2E2')
        lower_frame.pack(side=tk.TOP, expand=True, fill=tk.BOTH)

        # daten frame
        daten_frame = tk.Frame(lower_frame, bg='#E2E2E2', width=800)
        daten_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(20, 0), pady=20)
        daten_frame.pack_propagate(False)
        self.layout_daten_frame_standard(daten_frame)

        # grafik frame
        grafik_frame = tk.Frame(lower_frame, bg='#E2E2E2')
        grafik_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)
        self.show_plot_standard(grafik_frame)

    def layout_daten_frame_standard(self, frame):
        LABEL_BOLD = {
            'font': ('Arial', 14, 'bold'),
            'bg': '#E6F4D7'
        }

        LABEL_BOLD_2 = {
            'font': ('Arial', 18, 'bold'),
            'bg': '#E6F4D7'
        }

        LABEL = {
            'font': ('Arial', 14),
            'bg': '#E6F4D7'
        }

        LABEL_GREY = {
            'font': ('Arial', 14, 'bold'),
            'bg': '#618A35',
            'fg': 'white'
        }

        # Oben
        upper_frame = tk.Frame(frame, bg='#E2E2E2', height=350)
        upper_frame.pack(side=tk.TOP, fill=tk.X)
        upper_frame.pack_propagate(False)

        logo = LogoCanvas(parent=upper_frame, controller=self.controller,
                          image_name='auto_dummy', size=(250, 250))
        logo.pack(side=tk.LEFT, padx=20, pady=20, anchor=tk.CENTER)

        oben_rechts_frame = tk.Frame(upper_frame, bg='#E2E2E2')
        oben_rechts_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 20), pady=20)

        # ////////////////////////////////////////////
        # Deine Angaben Frame
        deine_eingaben_frame = ErgebnisSubFrame(oben_rechts_frame)
        deine_eingaben_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        deine_eingaben_frame.pack_propagate(False)
        tk.Label(deine_eingaben_frame.inner_frame, text='Deine Angaben',
                 **LABEL_BOLD).grid(row=0, column=0, padx=5, pady=2, sticky=tk.W)
        tk.Label(deine_eingaben_frame.inner_frame, text='Erstzulassung:',
                 **LABEL_BOLD).grid(row=1, column=0, padx=5, pady=2, sticky=tk.W)
        tk.Label(deine_eingaben_frame.inner_frame, text='Leistung [PS]:',
                 **LABEL_BOLD).grid(row=2, column=0, padx=5, pady=2, sticky=tk.W)
        tk.Label(deine_eingaben_frame.inner_frame, text='Kilometerstand:',
                 **LABEL_BOLD).grid(row=3, column=0, padx=5, pady=2, sticky=tk.W)
        tk.Label(deine_eingaben_frame.inner_frame, text='Getriebe:',
                 **LABEL_BOLD).grid(row=4, column=0, padx=5, pady=2, sticky=tk.W)
        tk.Label(deine_eingaben_frame.inner_frame, text='Antrieb:',
                 **LABEL_BOLD).grid(row=5, column=0, padx=5, pady=2, sticky=tk.W)
        tk.Label(deine_eingaben_frame.inner_frame, text='Schaden?:',
                 **LABEL_BOLD).grid(row=6, column=0, padx=5, pady=2, sticky=tk.W)

        tk.Label(deine_eingaben_frame.inner_frame, text=str(self.regression_daten_dic['erstzulassung']),
                 **LABEL).grid(row=1, column=1, padx=10, pady=2, sticky=tk.W)
        tk.Label(deine_eingaben_frame.inner_frame, text=str(self.regression_daten_dic['auto_leistung_ps']),
                 **LABEL).grid(row=2, column=1, padx=10, pady=2, sticky=tk.W)
        tk.Label(deine_eingaben_frame.inner_frame, text=str(self.regression_daten_dic['auto_kilometerstand']),
                 **LABEL).grid(row=3, column=1, padx=10, pady=2, sticky=tk.W)
        tk.Label(deine_eingaben_frame.inner_frame, text=str(self.regression_daten_dic['getriebe']),
                 **LABEL).grid(row=4, column=1, padx=10, pady=2, sticky=tk.W)
        tk.Label(deine_eingaben_frame.inner_frame, text=str(self.regression_daten_dic['antriebsart']),
                 **LABEL).grid(row=5, column=1, padx=10, pady=2, sticky=tk.W)
        schaden = 'Nein'
        if self.regression_daten_dic['schaden_vorhanden'] == 1:
            schaden = 'Ja'
        tk.Label(deine_eingaben_frame.inner_frame, text=schaden,
                 **LABEL).grid(row=6, column=1, padx=10, pady=2, sticky=tk.W)

        # ////////////////////////////////////////////
        # Anzahl berücksichtigter Daten FRame
        anzahl_daten_frame = ErgebnisSubFrame(oben_rechts_frame, height=60)
        anzahl_daten_frame.pack(side=tk.TOP, fill=tk.X, pady=(10, 0))
        anzahl_daten_frame.pack_propagate(False)
        tk.Label(anzahl_daten_frame.inner_frame, text='Anzahl berücksichtigter Inserate:',
                 **LABEL_BOLD).pack(side=tk.LEFT, padx=5)
        tk.Label(anzahl_daten_frame.inner_frame, text=str(len(self.filter_df)),
                 **LABEL).pack(side=tk.LEFT, padx=10)

        # ////////////////////////////////////////////
        # Unten
        lower_frame = tk.Frame(frame, bg='#E2E2E2')
        lower_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        preis_anzahl_tage_frame = tk.Frame(lower_frame, bg='#E2E2E2')
        preis_anzahl_tage_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # ////////////////////////////////////////////
        preis_frame = ErgebnisSubFrame(preis_anzahl_tage_frame)
        preis_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        preis_frame.pack_propagate(False)
        tk.Label(preis_frame.inner_frame, text='Preis',
                 **LABEL_BOLD_2).pack(side=tk.TOP, fill=tk.X, padx=5, pady=5, expand=False)
        seperator = tk.Frame(preis_frame.inner_frame, bg=preis_frame.border_color, height=3)
        seperator.pack(side=tk.TOP, fill=tk.X, padx=5, expand=False)

        preis_daten_frame = tk.Frame(preis_frame.inner_frame, bg=preis_frame.frame_color)
        preis_daten_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Prognose
        preis_prognose = tk.Frame(preis_daten_frame, bg=preis_frame.frame_color)
        preis_prognose.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        preis_prognose.pack_propagate(0)
        tk.Label(preis_prognose, text='Prognose',
                 **LABEL_BOLD).pack(side=tk.TOP, fill=tk.BOTH, padx=5, expand=True)
        tk.Label(preis_prognose, text=str(int(self.preisprognose)) + ' €',
                 **LABEL).pack(side=tk.TOP, fill=tk.BOTH, padx=5, expand=True)

        tk.Frame(preis_daten_frame, bg=preis_frame.border_color, width=3).pack(
            side=tk.LEFT, fill=tk.Y, expand=False, pady=5)

        # Durchschnitt
        preis_durchschnitt = tk.Frame(preis_daten_frame, bg=preis_frame.frame_color)
        preis_durchschnitt.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        preis_durchschnitt.pack_propagate(0)

        tk.Label(preis_durchschnitt, text=u'⌀',
                 **LABEL_BOLD).pack(side=tk.TOP, fill=tk.BOTH, padx=5, expand=True)
        tk.Label(preis_durchschnitt, text=str(int(self.filter_df['preis'].mean())) + ' €',
                 **LABEL).pack(side=tk.TOP, fill=tk.BOTH, padx=5, expand=True)

        tk.Frame(preis_daten_frame, bg=preis_frame.border_color, width=3).pack(
            side=tk.LEFT, fill=tk.Y, expand=False, pady=5)

        # Standardabweichung
        preis_standardabweichung = tk.Frame(preis_daten_frame, bg=preis_frame.frame_color)
        preis_standardabweichung.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        preis_standardabweichung.pack_propagate(0)
        tk.Label(preis_standardabweichung, text=u'Std.',
                 **LABEL_BOLD).pack(side=tk.TOP, fill=tk.BOTH, padx=5, expand=True)
        tk.Label(preis_standardabweichung, text=str(int(self.filter_df['preis'].std())) + ' €',
                 **LABEL).pack(side=tk.TOP, fill=tk.BOTH, padx=5, expand=True)

        # ////////////////////////////////////////////
        anzahl_tage_frame = ErgebnisSubFrame(preis_anzahl_tage_frame)
        anzahl_tage_frame.pack_propagate(False)
        anzahl_tage_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        tk.Label(anzahl_tage_frame.inner_frame, text='Inseratsdauer',
                 **LABEL_BOLD_2).pack(side=tk.TOP, fill=tk.X, padx=5, pady=5, expand=False)
        seperator = tk.Frame(anzahl_tage_frame.inner_frame, bg=anzahl_tage_frame.border_color, height=3)
        seperator.pack(side=tk.TOP, fill=tk.X, padx=5, expand=False)

        anzahl_tage_daten_frame = tk.Frame(anzahl_tage_frame.inner_frame, bg=preis_frame.frame_color)
        anzahl_tage_daten_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Durchschnitt
        anzahl_tage_durchschnitt = tk.Frame(anzahl_tage_daten_frame, bg=preis_frame.frame_color)
        anzahl_tage_durchschnitt.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        anzahl_tage_durchschnitt.pack_propagate(0)

        tk.Label(anzahl_tage_durchschnitt, text=u'⌀',
                 **LABEL_BOLD).pack(side=tk.TOP, fill=tk.BOTH, padx=5, expand=True)
        tk.Label(anzahl_tage_durchschnitt, text=str(float(self.filter_df['anzahl_tage_online'].mean().round(1))).replace('.', ','),
                 **LABEL).pack(side=tk.TOP, fill=tk.BOTH, padx=5, expand=True)

        tk.Frame(anzahl_tage_daten_frame, bg=anzahl_tage_frame.border_color, width=3).pack(
            side=tk.LEFT, fill=tk.Y, expand=False, pady=5)

        # Standardabweichung
        anzahl_tage_standardabweichung = tk.Frame(anzahl_tage_daten_frame, bg=preis_frame.frame_color)
        anzahl_tage_standardabweichung.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        anzahl_tage_standardabweichung.pack_propagate(0)
        tk.Label(anzahl_tage_standardabweichung, text=u'Std.',
                 **LABEL_BOLD).pack(side=tk.TOP, fill=tk.BOTH, padx=5, expand=True)
        tk.Label(anzahl_tage_standardabweichung, text=str(float(self.filter_df['anzahl_tage_online'].std().round(1))).replace('.', ','),
                 **LABEL).pack(side=tk.TOP, fill=tk.BOTH, padx=5, expand=True)

        # ////////////////////////////////////////////
        kilometer_leistung_alter = tk.Frame(lower_frame, bg='#E2E2E2')
        kilometer_leistung_alter.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        kilometer_frame = ErgebnisSubFrameGrey(kilometer_leistung_alter)
        kilometer_frame.pack_propagate(False)
        kilometer_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        tk.Label(kilometer_frame.inner_frame, text='Premium-Feature',
                 **LABEL_GREY).pack(side=tk.TOP, fill=tk.X, padx=5, pady=5, expand=True)

        # ////////////////////////////////////////////
        leistung_frame = ErgebnisSubFrameGrey(kilometer_leistung_alter)
        leistung_frame.pack_propagate(False)
        leistung_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        tk.Label(leistung_frame.inner_frame, text='Premium-Feature',
                 **LABEL_GREY).pack(side=tk.TOP, fill=tk.X, padx=5, pady=5, expand=True)

        # ////////////////////////////////////////////
        alter_frame = ErgebnisSubFrameGrey(kilometer_leistung_alter)
        alter_frame.pack_propagate(False)
        alter_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        tk.Label(alter_frame.inner_frame, text='Premium-Feature',
                 **LABEL_GREY).pack(side=tk.TOP, fill=tk.X, padx=5, pady=5, expand=True)

    def show_plot_standard(self, frame):
        # Ampel mit Preisbereichen
        preis_prognose = int(self.preisprognose)
        preis_std = int(self.filter_df['preis'].std())

        #
        STD_STEP = 0.25 * preis_std
        print('Schrittweite: ' + str(STD_STEP))

        bereich_fair = (int(preis_prognose - 0.5 * STD_STEP), int(preis_prognose + 0.5 * STD_STEP))
        bereich_gut = (int(preis_prognose - 1.5 * STD_STEP), int(preis_prognose - 0.5 * STD_STEP))
        bereich_sehr_gut = (int(preis_prognose - 2.5 * STD_STEP), int(preis_prognose - 1.5 * STD_STEP))
        bereich_erhoeht = (int(preis_prognose + .5 * STD_STEP), int(preis_prognose + 1.5 * STD_STEP))
        bereich_schlecht = (int(preis_prognose + 1.5 * STD_STEP), int(preis_prognose + 2.5 * STD_STEP))

        grenze_0 = bereich_sehr_gut[0]
        grenze_1 = bereich_sehr_gut[1]
        grenze_2 = bereich_fair[0]
        grenze_3 = bereich_fair[1]
        grenze_4 = bereich_schlecht[0]
        grenze_5 = bereich_schlecht[1]

        print('Grenzen: ' + str(grenze_0) + ' __ ' +
              str(grenze_1) + ' __ ' +
              str(grenze_2) + ' __ ' +
              str(grenze_3) + ' __ ' +
              str(grenze_4) + ' __ ' +
              str(grenze_5))

        UEBERSCHRIFT2 = {
            'font': ('Arial', 20),
            'bg': '#E2E2E2'
        }
        tk.Label(frame, text='PREISKLASSEN', **UEBERSCHRIFT2).pack(side=tk.TOP, anchor=tk.NW)

        frame_preise_bg = tk.Frame(frame, bg='#C3E59E', height=120)
        frame_preise_bg.pack_propagate(False)
        frame_preise_bg.grid_propagate(False)
        frame_preise_bg.pack(side=tk.TOP, fill=tk.X)

        frame_preise = tk.Frame(frame_preise_bg, bg='#E6F4D7', height=120)
        frame_preise.pack_propagate(False)
        frame_preise.grid_propagate(False)
        frame_preise.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=3, pady=3)
        frame_preise.grid_rowconfigure(0, weight=1, uniform='row')
        frame_preise.grid_columnconfigure(0, weight=1, uniform='col')
        frame_preise.grid_columnconfigure(1, weight=3, uniform='col')
        frame_preise.grid_columnconfigure(2, weight=3, uniform='col')
        frame_preise.grid_columnconfigure(3, weight=3, uniform='col')
        frame_preise.grid_columnconfigure(4, weight=3, uniform='col')
        frame_preise.grid_columnconfigure(5, weight=3, uniform='col')
        frame_preise.grid_columnconfigure(6, weight=1, uniform='col')

        PAD = 3
        frame_unten = tk.Frame(frame_preise, bg='gray')
        frame_unten.grid(row=0, column=0, sticky='nsew', padx=(PAD, 1), pady=PAD)

        frame_sehrgut = tk.Frame(frame_preise, bg='#92D050')
        frame_sehrgut.grid(row=0, column=1, sticky='nsew', padx=1, pady=PAD)
        tk.Label(frame_sehrgut, text='Sehr\ngut', bg='#92D050', font=('Arial', 14, 'bold')).pack(
            fill=tk.BOTH, expand=True)

        frame_gut = tk.Frame(frame_preise, bg='#C7E7A6')
        frame_gut.grid(row=0, column=2, sticky='nsew', padx=1, pady=PAD)
        tk.Label(frame_gut, text='Gut', bg='#C7E7A6', font=('Arial', 14, 'bold')).pack(
            fill=tk.BOTH, expand=True)

        frame_fair = tk.Frame(frame_preise, bg='#F0CB41')
        frame_fair.grid(row=0, column=3, sticky='nsew', padx=1, pady=PAD)
        tk.Label(frame_fair, text='Fair', bg='#F0CB41', font=('Arial', 14, 'bold')).pack(
            fill=tk.BOTH, expand=True)

        frame_erhoeht = tk.Frame(frame_preise, bg='#D89A4C')
        frame_erhoeht.grid(row=0, column=4, sticky='nsew', padx=1, pady=PAD)
        tk.Label(frame_erhoeht, text='Erhöht', bg='#D89A4C', font=('Arial', 14, 'bold')).pack(
            fill=tk.BOTH, expand=True)

        frame_schlecht = tk.Frame(frame_preise, bg='#C16B55')
        frame_schlecht.grid(row=0, column=5, sticky='nsew', padx=1, pady=PAD)
        tk.Label(frame_schlecht, text='Schlecht', bg='#C16B55', font=('Arial', 14, 'bold')).pack(
            fill=tk.BOTH, expand=True)

        frame_oben = tk.Frame(frame_preise, bg='gray')
        frame_oben.grid(row=0, column=6, sticky='nsew', padx=(1, PAD), pady=PAD)

        LABEL_DESIGN = {
            'font': ('Arial', 11),
            'bg': '#E6F4D7'
        }

        tk.Label(frame_preise, text=str(int(grenze_0)) + '€', **
                 LABEL_DESIGN).place(relx=1/17 + .01, rely=.02, anchor=tk.N)

        tk.Label(frame_preise, text=str(int(grenze_1)) + '€', **LABEL_DESIGN).place(relx=4/17, rely=.02, anchor=tk.N)

        tk.Label(frame_preise, text=str(int(grenze_2)) + '€', **LABEL_DESIGN).place(relx=7/17, rely=.02, anchor=tk.N)

        tk.Label(frame_preise, text=str(int(grenze_3)) + '€', **LABEL_DESIGN).place(relx=10/17, rely=.02, anchor=tk.N)

        tk.Label(frame_preise, text=str(int(grenze_4)) + '€', **LABEL_DESIGN).place(relx=13/17, rely=.02, anchor=tk.N)

        tk.Label(frame_preise, text=str(int(grenze_5)) + '€', **
                 LABEL_DESIGN).place(relx=16/17 - .01, rely=.02, anchor=tk.N)

        # ////////////////////////////////////////////
        # Restlichen Plots
        LABEL_GREY = {
            'font': ('Arial', 14, 'bold'),
            'bg': '#618A35',
            'fg': 'white'
        }
        plot_frame = tk.Frame(frame, bg='#E2E2E2')
        plot_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)
        hide = ErgebnisSubFrameGrey(plot_frame)
        hide.pack_propagate(False)
        hide.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        tk.Label(hide.inner_frame, text='Premium-Feature',
                 **LABEL_GREY).pack(side=tk.TOP, fill=tk.X, padx=5, pady=5, expand=True)

    def show_plot(self, frame):
        # Ampel mit Preisbereichen
        preis_prognose = int(self.preisprognose)
        preis_std = int(self.filter_df['preis'].std())

        #
        STD_STEP = 0.25 * preis_std
        print('Schrittweite: ' + str(STD_STEP))

        bereich_fair = (int(preis_prognose - 0.5 * STD_STEP), int(preis_prognose + 0.5 * STD_STEP))
        bereich_gut = (int(preis_prognose - 1.5 * STD_STEP), int(preis_prognose - 0.5 * STD_STEP))
        bereich_sehr_gut = (int(preis_prognose - 2.5 * STD_STEP), int(preis_prognose - 1.5 * STD_STEP))
        bereich_erhoeht = (int(preis_prognose + .5 * STD_STEP), int(preis_prognose + 1.5 * STD_STEP))
        bereich_schlecht = (int(preis_prognose + 1.5 * STD_STEP), int(preis_prognose + 2.5 * STD_STEP))

        grenze_0 = bereich_sehr_gut[0]
        grenze_1 = bereich_sehr_gut[1]
        grenze_2 = bereich_fair[0]
        grenze_3 = bereich_fair[1]
        grenze_4 = bereich_schlecht[0]
        grenze_5 = bereich_schlecht[1]

        print('Grenzen: ' + str(grenze_0) + ' __ ' +
              str(grenze_1) + ' __ ' +
              str(grenze_2) + ' __ ' +
              str(grenze_3) + ' __ ' +
              str(grenze_4) + ' __ ' +
              str(grenze_5))

        UEBERSCHRIFT2 = {
            'font': ('Arial', 20),
            'bg': '#E2E2E2'
        }
        tk.Label(frame, text='PREISKLASSEN', **UEBERSCHRIFT2).pack(side=tk.TOP, anchor=tk.NW)

        frame_preise_bg = tk.Frame(frame, bg='#C3E59E', height=120)
        frame_preise_bg.pack_propagate(False)
        frame_preise_bg.grid_propagate(False)
        frame_preise_bg.pack(side=tk.TOP, fill=tk.X)

        frame_preise = tk.Frame(frame_preise_bg, bg='#E6F4D7', height=120)
        frame_preise.pack_propagate(False)
        frame_preise.grid_propagate(False)
        frame_preise.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=3, pady=3)
        frame_preise.grid_rowconfigure(0, weight=1, uniform='row')
        frame_preise.grid_columnconfigure(0, weight=1, uniform='col')
        frame_preise.grid_columnconfigure(1, weight=3, uniform='col')
        frame_preise.grid_columnconfigure(2, weight=3, uniform='col')
        frame_preise.grid_columnconfigure(3, weight=3, uniform='col')
        frame_preise.grid_columnconfigure(4, weight=3, uniform='col')
        frame_preise.grid_columnconfigure(5, weight=3, uniform='col')
        frame_preise.grid_columnconfigure(6, weight=1, uniform='col')

        PAD = 3
        frame_unten = tk.Frame(frame_preise, bg='gray')
        frame_unten.grid(row=0, column=0, sticky='nsew', padx=(PAD, 1), pady=PAD)

        frame_sehrgut = tk.Frame(frame_preise, bg='#92D050')
        frame_sehrgut.grid(row=0, column=1, sticky='nsew', padx=1, pady=PAD)
        tk.Label(frame_sehrgut, text='Sehr\ngut', bg='#92D050', font=('Arial', 14, 'bold')).pack(
            fill=tk.BOTH, expand=True)

        frame_gut = tk.Frame(frame_preise, bg='#C7E7A6')
        frame_gut.grid(row=0, column=2, sticky='nsew', padx=1, pady=PAD)
        tk.Label(frame_gut, text='Gut', bg='#C7E7A6', font=('Arial', 14, 'bold')).pack(
            fill=tk.BOTH, expand=True)

        frame_fair = tk.Frame(frame_preise, bg='#F0CB41')
        frame_fair.grid(row=0, column=3, sticky='nsew', padx=1, pady=PAD)
        tk.Label(frame_fair, text='Fair', bg='#F0CB41', font=('Arial', 14, 'bold')).pack(
            fill=tk.BOTH, expand=True)

        frame_erhoeht = tk.Frame(frame_preise, bg='#D89A4C')
        frame_erhoeht.grid(row=0, column=4, sticky='nsew', padx=1, pady=PAD)
        tk.Label(frame_erhoeht, text='Erhöht', bg='#D89A4C', font=('Arial', 14, 'bold')).pack(
            fill=tk.BOTH, expand=True)

        frame_schlecht = tk.Frame(frame_preise, bg='#C16B55')
        frame_schlecht.grid(row=0, column=5, sticky='nsew', padx=1, pady=PAD)
        tk.Label(frame_schlecht, text='Schlecht', bg='#C16B55', font=('Arial', 14, 'bold')).pack(
            fill=tk.BOTH, expand=True)

        frame_oben = tk.Frame(frame_preise, bg='gray')
        frame_oben.grid(row=0, column=6, sticky='nsew', padx=(1, PAD), pady=PAD)

        LABEL_DESIGN = {
            'font': ('Arial', 11),
            'bg': '#E6F4D7'
        }

        tk.Label(frame_preise, text=str(int(grenze_0)) + '€', **
                 LABEL_DESIGN).place(relx=1/17 + .01, rely=.02, anchor=tk.N)

        tk.Label(frame_preise, text=str(int(grenze_1)) + '€', **LABEL_DESIGN).place(relx=4/17, rely=.02, anchor=tk.N)

        tk.Label(frame_preise, text=str(int(grenze_2)) + '€', **LABEL_DESIGN).place(relx=7/17, rely=.02, anchor=tk.N)

        tk.Label(frame_preise, text=str(int(grenze_3)) + '€', **LABEL_DESIGN).place(relx=10/17, rely=.02, anchor=tk.N)

        tk.Label(frame_preise, text=str(int(grenze_4)) + '€', **LABEL_DESIGN).place(relx=13/17, rely=.02, anchor=tk.N)

        tk.Label(frame_preise, text=str(int(grenze_5)) + '€', **
                 LABEL_DESIGN).place(relx=16/17 - .01, rely=.02, anchor=tk.N)

        # ////////////////////////////////////////////
        # Restlichen Plots
        plot_frame = tk.Frame(frame, bg='yellow')
        plot_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.erstelle_plot(plot_frame)

    ###############
    # Daten Frame
    def layout_daten_frame(self, frame):
        LABEL_BOLD = {
            'font': ('Arial', 14, 'bold'),
            'bg': '#E6F4D7'
        }

        LABEL_BOLD_2 = {
            'font': ('Arial', 18, 'bold'),
            'bg': '#E6F4D7'
        }

        LABEL = {
            'font': ('Arial', 14),
            'bg': '#E6F4D7'
        }

        # Oben
        upper_frame = tk.Frame(frame, bg='#E2E2E2', height=350)
        upper_frame.pack(side=tk.TOP, fill=tk.X)
        upper_frame.pack_propagate(False)

        logo = LogoCanvas(parent=upper_frame, controller=self.controller,
                          image_name='auto_dummy', size=(250, 250))
        logo.pack(side=tk.LEFT, padx=20, pady=20, anchor=tk.CENTER)

        oben_rechts_frame = tk.Frame(upper_frame, bg='#E2E2E2')
        oben_rechts_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 20), pady=20)

        # ////////////////////////////////////////////
        # Deine Angaben Frame
        deine_eingaben_frame = ErgebnisSubFrame(oben_rechts_frame)
        deine_eingaben_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        deine_eingaben_frame.pack_propagate(False)
        tk.Label(deine_eingaben_frame.inner_frame, text='Deine Angaben',
                 **LABEL_BOLD).grid(row=0, column=0, padx=5, pady=2, sticky=tk.W)
        tk.Label(deine_eingaben_frame.inner_frame, text='Erstzulassung:',
                 **LABEL_BOLD).grid(row=1, column=0, padx=5, pady=2, sticky=tk.W)
        tk.Label(deine_eingaben_frame.inner_frame, text='Leistung [PS]:',
                 **LABEL_BOLD).grid(row=2, column=0, padx=5, pady=2, sticky=tk.W)
        tk.Label(deine_eingaben_frame.inner_frame, text='Kilometerstand:',
                 **LABEL_BOLD).grid(row=3, column=0, padx=5, pady=2, sticky=tk.W)
        tk.Label(deine_eingaben_frame.inner_frame, text='Getriebe:',
                 **LABEL_BOLD).grid(row=4, column=0, padx=5, pady=2, sticky=tk.W)
        tk.Label(deine_eingaben_frame.inner_frame, text='Antrieb:',
                 **LABEL_BOLD).grid(row=5, column=0, padx=5, pady=2, sticky=tk.W)
        tk.Label(deine_eingaben_frame.inner_frame, text='Schaden?:',
                 **LABEL_BOLD).grid(row=6, column=0, padx=5, pady=2, sticky=tk.W)

        tk.Label(deine_eingaben_frame.inner_frame, text=str(self.regression_daten_dic['erstzulassung']),
                 **LABEL).grid(row=1, column=1, padx=10, pady=2, sticky=tk.W)
        tk.Label(deine_eingaben_frame.inner_frame, text=str(self.regression_daten_dic['auto_leistung_ps']),
                 **LABEL).grid(row=2, column=1, padx=10, pady=2, sticky=tk.W)
        tk.Label(deine_eingaben_frame.inner_frame, text=str(self.regression_daten_dic['auto_kilometerstand']),
                 **LABEL).grid(row=3, column=1, padx=10, pady=2, sticky=tk.W)
        tk.Label(deine_eingaben_frame.inner_frame, text=str(self.regression_daten_dic['getriebe']),
                 **LABEL).grid(row=4, column=1, padx=10, pady=2, sticky=tk.W)
        tk.Label(deine_eingaben_frame.inner_frame, text=str(self.regression_daten_dic['antriebsart']),
                 **LABEL).grid(row=5, column=1, padx=10, pady=2, sticky=tk.W)
        schaden = 'Nein'
        if self.regression_daten_dic['schaden_vorhanden'] == 1:
            schaden = 'Ja'
        tk.Label(deine_eingaben_frame.inner_frame, text=schaden,
                 **LABEL).grid(row=6, column=1, padx=10, pady=2, sticky=tk.W)

        # ////////////////////////////////////////////
        # Anzahl berücksichtigter Daten FRame
        anzahl_daten_frame = ErgebnisSubFrame(oben_rechts_frame, height=60)
        anzahl_daten_frame.pack(side=tk.TOP, fill=tk.X, pady=(10, 0))
        anzahl_daten_frame.pack_propagate(False)
        tk.Label(anzahl_daten_frame.inner_frame, text='Anzahl berücksichtigter Inserate:',
                 **LABEL_BOLD).pack(side=tk.LEFT, padx=5)
        tk.Label(anzahl_daten_frame.inner_frame, text=str(len(self.filter_df)),
                 **LABEL).pack(side=tk.LEFT, padx=10)

        # ////////////////////////////////////////////
        # Unten
        lower_frame = tk.Frame(frame, bg='#E2E2E2')
        lower_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        preis_anzahl_tage_frame = tk.Frame(lower_frame, bg='#E2E2E2')
        preis_anzahl_tage_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # ////////////////////////////////////////////
        preis_frame = ErgebnisSubFrame(preis_anzahl_tage_frame)
        preis_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        preis_frame.pack_propagate(False)
        tk.Label(preis_frame.inner_frame, text='Preis',
                 **LABEL_BOLD_2).pack(side=tk.TOP, fill=tk.X, padx=5, pady=5, expand=False)
        seperator = tk.Frame(preis_frame.inner_frame, bg=preis_frame.border_color, height=3)
        seperator.pack(side=tk.TOP, fill=tk.X, padx=5, expand=False)

        preis_daten_frame = tk.Frame(preis_frame.inner_frame, bg=preis_frame.frame_color)
        preis_daten_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Prognose
        preis_prognose = tk.Frame(preis_daten_frame, bg=preis_frame.frame_color)
        preis_prognose.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        preis_prognose.pack_propagate(0)
        tk.Label(preis_prognose, text='Prognose',
                 **LABEL_BOLD).pack(side=tk.TOP, fill=tk.BOTH, padx=5, expand=True)
        tk.Label(preis_prognose, text=str(int(self.preisprognose)) + ' €',
                 **LABEL).pack(side=tk.TOP, fill=tk.BOTH, padx=5, expand=True)

        tk.Frame(preis_daten_frame, bg=preis_frame.border_color, width=3).pack(
            side=tk.LEFT, fill=tk.Y, expand=False, pady=5)

        # Durchschnitt
        preis_durchschnitt = tk.Frame(preis_daten_frame, bg=preis_frame.frame_color)
        preis_durchschnitt.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        preis_durchschnitt.pack_propagate(0)

        tk.Label(preis_durchschnitt, text=u'⌀',
                 **LABEL_BOLD).pack(side=tk.TOP, fill=tk.BOTH, padx=5, expand=True)
        tk.Label(preis_durchschnitt, text=str(int(self.filter_df['preis'].mean())) + ' €',
                 **LABEL).pack(side=tk.TOP, fill=tk.BOTH, padx=5, expand=True)

        tk.Frame(preis_daten_frame, bg=preis_frame.border_color, width=3).pack(
            side=tk.LEFT, fill=tk.Y, expand=False, pady=5)

        # Standardabweichung
        preis_standardabweichung = tk.Frame(preis_daten_frame, bg=preis_frame.frame_color)
        preis_standardabweichung.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        preis_standardabweichung.pack_propagate(0)
        tk.Label(preis_standardabweichung, text=u'Std.',
                 **LABEL_BOLD).pack(side=tk.TOP, fill=tk.BOTH, padx=5, expand=True)
        tk.Label(preis_standardabweichung, text=str(int(self.filter_df['preis'].std())) + ' €',
                 **LABEL).pack(side=tk.TOP, fill=tk.BOTH, padx=5, expand=True)

        # ////////////////////////////////////////////
        anzahl_tage_frame = ErgebnisSubFrame(preis_anzahl_tage_frame)
        anzahl_tage_frame.pack_propagate(False)
        anzahl_tage_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        tk.Label(anzahl_tage_frame.inner_frame, text='Inseratsdauer',
                 **LABEL_BOLD_2).pack(side=tk.TOP, fill=tk.X, padx=5, pady=5, expand=False)
        seperator = tk.Frame(anzahl_tage_frame.inner_frame, bg=anzahl_tage_frame.border_color, height=3)
        seperator.pack(side=tk.TOP, fill=tk.X, padx=5, expand=False)

        anzahl_tage_daten_frame = tk.Frame(anzahl_tage_frame.inner_frame, bg=preis_frame.frame_color)
        anzahl_tage_daten_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Durchschnitt
        anzahl_tage_durchschnitt = tk.Frame(anzahl_tage_daten_frame, bg=preis_frame.frame_color)
        anzahl_tage_durchschnitt.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        anzahl_tage_durchschnitt.pack_propagate(0)

        tk.Label(anzahl_tage_durchschnitt, text=u'⌀',
                 **LABEL_BOLD).pack(side=tk.TOP, fill=tk.BOTH, padx=5, expand=True)
        tk.Label(anzahl_tage_durchschnitt, text=str(float(self.filter_df['anzahl_tage_online'].mean().round(1))).replace('.', ','),
                 **LABEL).pack(side=tk.TOP, fill=tk.BOTH, padx=5, expand=True)

        tk.Frame(anzahl_tage_daten_frame, bg=anzahl_tage_frame.border_color, width=3).pack(
            side=tk.LEFT, fill=tk.Y, expand=False, pady=5)

        # Standardabweichung
        anzahl_tage_standardabweichung = tk.Frame(anzahl_tage_daten_frame, bg=preis_frame.frame_color)
        anzahl_tage_standardabweichung.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        anzahl_tage_standardabweichung.pack_propagate(0)
        tk.Label(anzahl_tage_standardabweichung, text=u'Std.',
                 **LABEL_BOLD).pack(side=tk.TOP, fill=tk.BOTH, padx=5, expand=True)
        tk.Label(anzahl_tage_standardabweichung, text=str(float(self.filter_df['anzahl_tage_online'].std().round(1))).replace('.', ','),
                 **LABEL).pack(side=tk.TOP, fill=tk.BOTH, padx=5, expand=True)

        # ////////////////////////////////////////////
        kilometer_leistung_alter = tk.Frame(lower_frame, bg='#E2E2E2')
        kilometer_leistung_alter.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        kilometer_frame = ErgebnisSubFrame(kilometer_leistung_alter)
        kilometer_frame.pack_propagate(False)
        kilometer_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        tk.Label(kilometer_frame.inner_frame, text='Kilometer',
                 **LABEL_BOLD_2).pack(side=tk.TOP, fill=tk.X, padx=5, pady=5, expand=False)
        tk.Frame(kilometer_frame.inner_frame, bg=preis_frame.border_color,
                 height=3).pack(side=tk.TOP, fill=tk.X, padx=5, expand=False)
        kilometer_daten_frame = tk.Frame(kilometer_frame.inner_frame, bg=kilometer_frame.frame_color)
        kilometer_daten_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Durchschnitt
        kilometer_durchschnitt = tk.Frame(kilometer_daten_frame, bg=preis_frame.frame_color)
        kilometer_durchschnitt.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        kilometer_durchschnitt.pack_propagate(0)

        tk.Label(kilometer_durchschnitt, text=u'⌀',
                 **LABEL_BOLD).pack(side=tk.TOP, fill=tk.BOTH, padx=5, expand=True)
        tk.Label(kilometer_durchschnitt, text=str(int(self.filter_df['auto_kilometerstand'].mean())),
                 **LABEL).pack(side=tk.TOP, fill=tk.BOTH, padx=5, expand=True)

        tk.Frame(kilometer_daten_frame, bg=kilometer_frame.border_color, width=3).pack(
            side=tk.LEFT, fill=tk.Y, expand=False, pady=5)

        # Standardabweichung
        kilometer_standardabweichung = tk.Frame(kilometer_daten_frame, bg=preis_frame.frame_color)
        kilometer_standardabweichung.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        kilometer_standardabweichung.pack_propagate(0)
        tk.Label(kilometer_standardabweichung, text=u'Std.',
                 **LABEL_BOLD).pack(side=tk.TOP, fill=tk.BOTH, padx=5, expand=True)
        tk.Label(kilometer_standardabweichung, text=str(int(self.filter_df['auto_kilometerstand'].std())),
                 **LABEL).pack(side=tk.TOP, fill=tk.BOTH, padx=5, expand=True)

        # ////////////////////////////////////////////
        leistung_frame = ErgebnisSubFrame(kilometer_leistung_alter)
        leistung_frame.pack_propagate(False)
        leistung_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        tk.Label(leistung_frame.inner_frame, text='Leistung',
                 **LABEL_BOLD_2).pack(side=tk.TOP, fill=tk.X, padx=5, pady=5, expand=False)
        tk.Frame(leistung_frame.inner_frame, bg=preis_frame.border_color,
                 height=3).pack(side=tk.TOP, fill=tk.X, padx=5, expand=False)
        leistung_daten_frame = tk.Frame(leistung_frame.inner_frame, bg=leistung_frame.frame_color)
        leistung_daten_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Durchschnitt
        leistung_durchschnitt = tk.Frame(leistung_daten_frame, bg=preis_frame.frame_color)
        leistung_durchschnitt.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        leistung_durchschnitt.pack_propagate(0)

        tk.Label(leistung_durchschnitt, text=u'⌀',
                 **LABEL_BOLD).pack(side=tk.TOP, fill=tk.BOTH, padx=5, expand=True)
        tk.Label(leistung_durchschnitt, text=str(int(self.filter_df['auto_leistung_ps'].mean())) + ' PS',
                 **LABEL).pack(side=tk.TOP, fill=tk.BOTH, padx=5, expand=True)

        tk.Frame(leistung_daten_frame, bg=kilometer_frame.border_color, width=3).pack(
            side=tk.LEFT, fill=tk.Y, expand=False, pady=5)

        # Standardabweichung
        leistung_standardabweichung = tk.Frame(leistung_daten_frame, bg=preis_frame.frame_color)
        leistung_standardabweichung.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        leistung_standardabweichung.pack_propagate(0)
        tk.Label(leistung_standardabweichung, text=u'Std.',
                 **LABEL_BOLD).pack(side=tk.TOP, fill=tk.BOTH, padx=5, expand=True)
        tk.Label(leistung_standardabweichung, text=str(int(self.filter_df['auto_leistung_ps'].std())) + ' PS',
                 **LABEL).pack(side=tk.TOP, fill=tk.BOTH, padx=5, expand=True)

        # ////////////////////////////////////////////
        alter_frame = ErgebnisSubFrame(kilometer_leistung_alter)
        alter_frame.pack_propagate(False)
        alter_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        tk.Label(alter_frame.inner_frame, text='Erstzulassung',
                 **LABEL_BOLD_2).pack(side=tk.TOP, fill=tk.X, padx=5, pady=5, expand=False)
        tk.Frame(alter_frame.inner_frame, bg=preis_frame.border_color,
                 height=3).pack(side=tk.TOP, fill=tk.X, padx=5, expand=False)
        ez_daten_frame = tk.Frame(alter_frame.inner_frame, bg=alter_frame.frame_color)
        ez_daten_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Durchschnitt
        ez_durchschnitt = tk.Frame(ez_daten_frame, bg=preis_frame.frame_color)
        ez_durchschnitt.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        ez_durchschnitt.pack_propagate(0)

        tk.Label(ez_durchschnitt, text=u'⌀',
                 **LABEL_BOLD).pack(side=tk.TOP, fill=tk.BOTH, padx=5, expand=True)
        tk.Label(ez_durchschnitt, text=str((self.filter_df['auto_baujahr']).mean().round(1)).replace('.', ','),
                 **LABEL).pack(side=tk.TOP, fill=tk.BOTH, padx=5, expand=True)

        tk.Frame(ez_daten_frame, bg=kilometer_frame.border_color, width=3).pack(
            side=tk.LEFT, fill=tk.Y, expand=False, pady=5)

        # Standardabweichung
        ez_standardabweichung = tk.Frame(ez_daten_frame, bg=preis_frame.frame_color)
        ez_standardabweichung.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        ez_standardabweichung.pack_propagate(0)
        tk.Label(ez_standardabweichung, text=u'Std.',
                 **LABEL_BOLD).pack(side=tk.TOP, fill=tk.BOTH, padx=5, expand=True)
        tk.Label(ez_standardabweichung, text=str((self.filter_df['auto_baujahr']).std().round(1)).replace('.', ','),
                 **LABEL).pack(side=tk.TOP, fill=tk.BOTH, padx=5, expand=True)

    def show_plot(self, frame):
        # Ampel mit Preisbereichen
        preis_prognose = int(self.preisprognose)
        preis_std = int(self.filter_df['preis'].std())

        #
        STD_STEP = 0.25 * preis_std
        print('Schrittweite: ' + str(STD_STEP))

        bereich_fair = (int(preis_prognose - 0.5 * STD_STEP), int(preis_prognose + 0.5 * STD_STEP))
        bereich_gut = (int(preis_prognose - 1.5 * STD_STEP), int(preis_prognose - 0.5 * STD_STEP))
        bereich_sehr_gut = (int(preis_prognose - 2.5 * STD_STEP), int(preis_prognose - 1.5 * STD_STEP))
        bereich_erhoeht = (int(preis_prognose + .5 * STD_STEP), int(preis_prognose + 1.5 * STD_STEP))
        bereich_schlecht = (int(preis_prognose + 1.5 * STD_STEP), int(preis_prognose + 2.5 * STD_STEP))

        grenze_0 = bereich_sehr_gut[0]
        grenze_1 = bereich_sehr_gut[1]
        grenze_2 = bereich_fair[0]
        grenze_3 = bereich_fair[1]
        grenze_4 = bereich_schlecht[0]
        grenze_5 = bereich_schlecht[1]

        print('Grenzen: ' + str(grenze_0) + ' __ ' +
              str(grenze_1) + ' __ ' +
              str(grenze_2) + ' __ ' +
              str(grenze_3) + ' __ ' +
              str(grenze_4) + ' __ ' +
              str(grenze_5))

        UEBERSCHRIFT2 = {
            'font': ('Arial', 20),
            'bg': '#E2E2E2'
        }
        tk.Label(frame, text='PREISKLASSEN', **UEBERSCHRIFT2).pack(side=tk.TOP, anchor=tk.NW)

        frame_preise_bg = tk.Frame(frame, bg='#C3E59E', height=120)
        frame_preise_bg.pack_propagate(False)
        frame_preise_bg.grid_propagate(False)
        frame_preise_bg.pack(side=tk.TOP, fill=tk.X)

        frame_preise = tk.Frame(frame_preise_bg, bg='#E6F4D7', height=120)
        frame_preise.pack_propagate(False)
        frame_preise.grid_propagate(False)
        frame_preise.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=3, pady=3)
        frame_preise.grid_rowconfigure(0, weight=1, uniform='row')
        frame_preise.grid_columnconfigure(0, weight=1, uniform='col')
        frame_preise.grid_columnconfigure(1, weight=3, uniform='col')
        frame_preise.grid_columnconfigure(2, weight=3, uniform='col')
        frame_preise.grid_columnconfigure(3, weight=3, uniform='col')
        frame_preise.grid_columnconfigure(4, weight=3, uniform='col')
        frame_preise.grid_columnconfigure(5, weight=3, uniform='col')
        frame_preise.grid_columnconfigure(6, weight=1, uniform='col')

        PAD = 3
        frame_unten = tk.Frame(frame_preise, bg='gray')
        frame_unten.grid(row=0, column=0, sticky='nsew', padx=(PAD, 1), pady=PAD)

        frame_sehrgut = tk.Frame(frame_preise, bg='#92D050')
        frame_sehrgut.grid(row=0, column=1, sticky='nsew', padx=1, pady=PAD)
        tk.Label(frame_sehrgut, text='Sehr\ngut', bg='#92D050', font=('Arial', 14, 'bold')).pack(
            fill=tk.BOTH, expand=True)

        frame_gut = tk.Frame(frame_preise, bg='#C7E7A6')
        frame_gut.grid(row=0, column=2, sticky='nsew', padx=1, pady=PAD)
        tk.Label(frame_gut, text='Gut', bg='#C7E7A6', font=('Arial', 14, 'bold')).pack(
            fill=tk.BOTH, expand=True)

        frame_fair = tk.Frame(frame_preise, bg='#F0CB41')
        frame_fair.grid(row=0, column=3, sticky='nsew', padx=1, pady=PAD)
        tk.Label(frame_fair, text='Fair', bg='#F0CB41', font=('Arial', 14, 'bold')).pack(
            fill=tk.BOTH, expand=True)

        frame_erhoeht = tk.Frame(frame_preise, bg='#D89A4C')
        frame_erhoeht.grid(row=0, column=4, sticky='nsew', padx=1, pady=PAD)
        tk.Label(frame_erhoeht, text='Erhöht', bg='#D89A4C', font=('Arial', 14, 'bold')).pack(
            fill=tk.BOTH, expand=True)

        frame_schlecht = tk.Frame(frame_preise, bg='#C16B55')
        frame_schlecht.grid(row=0, column=5, sticky='nsew', padx=1, pady=PAD)
        tk.Label(frame_schlecht, text='Schlecht', bg='#C16B55', font=('Arial', 14, 'bold')).pack(
            fill=tk.BOTH, expand=True)

        frame_oben = tk.Frame(frame_preise, bg='gray')
        frame_oben.grid(row=0, column=6, sticky='nsew', padx=(1, PAD), pady=PAD)

        LABEL_DESIGN = {
            'font': ('Arial', 11),
            'bg': '#E6F4D7'
        }

        tk.Label(frame_preise, text=str(int(grenze_0)) + '€', **
                 LABEL_DESIGN).place(relx=1/17 + .01, rely=.02, anchor=tk.N)

        tk.Label(frame_preise, text=str(int(grenze_1)) + '€', **LABEL_DESIGN).place(relx=4/17, rely=.02, anchor=tk.N)

        tk.Label(frame_preise, text=str(int(grenze_2)) + '€', **LABEL_DESIGN).place(relx=7/17, rely=.02, anchor=tk.N)

        tk.Label(frame_preise, text=str(int(grenze_3)) + '€', **LABEL_DESIGN).place(relx=10/17, rely=.02, anchor=tk.N)

        tk.Label(frame_preise, text=str(int(grenze_4)) + '€', **LABEL_DESIGN).place(relx=13/17, rely=.02, anchor=tk.N)

        tk.Label(frame_preise, text=str(int(grenze_5)) + '€', **
                 LABEL_DESIGN).place(relx=16/17 - .01, rely=.02, anchor=tk.N)

        # ////////////////////////////////////////////
        # Restlichen Plots
        plot_frame = tk.Frame(frame, bg='yellow')
        plot_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.erstelle_plot(plot_frame)

        # ////////////////////////////////////////////

    def erstelle_plot(self, frame):
        # ////////////////////////////////////////////
        # PLOTS
        colors = ['#405C23', '#7F926C', '#A9B69D', '#564962', '#C6C2CA', '#9C9E9A']
        last_day = self.filter_df['datum_verschwunden'].max()
        last_30_days = pd.date_range(end=last_day, periods=30).to_pydatetime().tolist()
        last_30_days_date = []
        for x in last_30_days:
            last_30_days_date.append(x.date())

        df_last_30 = self.filter_df[self.filter_df['datum_verschwunden_date'].isin(last_30_days_date)]

        date_dicts = []
        for dat in last_30_days_date:
            date_dicts.append({
                'date': dat,
                'len': len(df_last_30[df_last_30['datum_erstellt_date'] == dat]),
                'len1': len(df_last_30[df_last_30['datum_verschwunden_date'] == dat])
            })

        df_dates = pd.DataFrame(date_dicts)

        plt.style.use('seaborn')
        fig = plt.figure(facecolor='#E2E2E2')
        ax1 = fig.add_subplot(221)
        ax2 = fig.add_subplot(222)
        ax3 = fig.add_subplot(212)

        # PIE Chart
        labels = []
        anzahl = []
        for x in self.filter_df['auto_kraftstoff'].unique():
            labels.append(x.title())
            anzahl.append(len(self.filter_df[self.filter_df['auto_kraftstoff'] == x]))
        patches, texts, _ = ax1.pie(anzahl, explode=None, labels=None, autopct='',
                                    shadow=True, startangle=90, colors=colors[0:len(anzahl)], labeldistance=1.05)
        labels = ['{0} - {1:1.2f} %'.format(i, j) for i, j in zip(labels, 100.*np.array(anzahl)/np.array(anzahl).sum())]
        ax1.legend(patches, labels, loc='left center', bbox_to_anchor=(0.1, 1.),
                   fontsize=10)

        ax1.set_title('Antrieb', fontweight='bold')

        # Boxplots
        data = [self.filter_df['auto_kilometerstand'], self.filter_df['auto_leistung_ps'], self.filter_df['auto_alter']]
        ax2.boxplot(data)
        ax2.yaxis.grid(False)
        ax2.xaxis.grid(False)

        # Timeline Erstellte Anzeigen
        str_dates = []
        for x in last_30_days_date:
            str_dates.append(str(x))
        width = 0.35
        bar1 = ax3.bar(np.array(list(range(1, 31)))-width/2,
                       df_dates['len'], width, label='Reingestellt', color='#ABDB79')
        bar2 = ax3.bar(np.array(list(range(1, 31)))+width/2,
                       df_dates['len1'], width, label='Herausgenommen', color='#618A35')
        #ax3.set_xticks(ticks=np.array(list(range(1, 31))), labels=str_dates)
        ax3.yaxis.grid(True)
        ax3.set_title('Inserate im letzten Monat', fontweight='bold')
        ax3.set_facecolor('#F1F5EF')
        ax3.legend(facecolor='white')
        ax3.set_ylabel('Anzahl Inserate')
        labels = [item.get_text() for item in ax3.get_xticklabels()]
        x = 0
        i = 2
        while x < len(str_dates) + 3:
            try:
                labels[i] = str(str_dates[3+x])
            except:
                pass
            x += 5
            i += 1
        ax3.set_xticklabels(labels)
        ax3.xaxis.grid(False)
        ax3.legend()
        #ax3.tick_params(axis='x', labelrotation=70)

        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, frame)
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        plt.close()
