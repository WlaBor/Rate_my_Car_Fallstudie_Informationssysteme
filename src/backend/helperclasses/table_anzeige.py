# -*- coding: utf-8 -*-
"""
Created on Sat Jun  4 13:08:09 2022

@author: wladi
"""
import sqlite3
import uuid
import pandas as pd
from scipy import stats


class Anzeige:

    def __init__(self, db_path):
        self.db_path = db_path

        self.init_table()

    # ////////////////////////////////////////////
    # Verbindung zur Datenbank aufbauen
    def create_connection(self):
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
        except Exception as ex:
            print('Keine Verbindung zur Datenbank möglich')
            print(ex)
        return conn

    # ////////////////////////////////////////////
    # Tabelle initialisieren
    def init_table(self):
        conn = self.create_connection()
        if conn == None:
            return

        c = conn.cursor()

        try:
            # Erklärung der Variablen
            '''
            id - ID der Anzeige

            automodell_id - ID der Automodells

            name - Name der Anzeige

            postleitzahl - PLZ der Anzeige

            datum_erstellt - Datum an dem die Anzeige erstellt wurde

            datum_verschwunden - Datum an dem die Anzeige aus der Plattform genommen wurde (interpretiert als Verkaufsdatum)

            anzahl_tage_online - Anzahl der Online-Tage --> None wenn Anzeige noch online ist

            preis - Preis

            auto_baujahr - Baujahr des Autos

            auto_alter - Alter des Autos zum Zeitpunkt an dem die Anzeige verschwand

            auto_getriebe - Manuell = 0,   Automatik = 1

            auto_leistung_ps - Leistung des Autos in PS

            auto_kilometerstand - Kilometerstand

            auto_kraftstoff - Kraftstofftyp

            auto_schaden - Autoschäden vorhanden? Nein = 0, Ja = 1
            '''

            c.execute('''
                      CREATE TABLE IF NOT EXISTS ANZEIGE
                      ([id] TEXT NOT NULL PRIMARY KEY,
                       [automodell_id] TEXT NOT NULL,
                       [name] TEXT,
                       [postleitzahl] TEXT,
                       [datum_erstellt] TEXT,
                       [datum_verschwunden] TEXT,
                       [anzahl_tage_online] INTEGER,
                       [preis] REAL,
                       [auto_baujahr] INTEGER,
                       [auto_alter] INTEGER,
                       [auto_getriebe] INTEGER,
                       [auto_leistung_ps] INTEGER,
                       [auto_kilometerstand] REAL,
                       [auto_kraftstoff] TEXT,
                       [auto_schaden] INTEGER
                       )
                      ''')
            print('ANZEIGE Tabelle erfolgreich')
        except Exception as ex:
            print('Fehler bei ANZEIGE Tabelle')
            print(ex)
        conn.close()

    # Anzeigen für ein bestimmtes Auto als DataFrame ausgeben
    def load_data_as_df(self, brand, model, vehicletype):

        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''
                  SELECT id FROM AUTOMODELL
                  WHERE (marke, model, fahrzeug_typ) = (?,?,?)
                  ORDER BY model
                  ''', (brand, model, vehicletype))

        auto_id = [element[0] for element in c.fetchall()][0]

        raw_df = pd.read_sql('''
                                  SELECT * FROM ANZEIGE WHERE automodell_id = "{}"
                                  '''.format(auto_id), conn)

        print('Anzahl Daten: ' + str(len(raw_df)))

        conn.close()
        return raw_df

    def load_data_with_filter(self, brand, model, vehicletype):
        df = self.load_data_as_df(brand, model, vehicletype)

        # Datenvorverarbeitung
        # Ausreißer
        z_score = 2
        # Preis
        # df = df[df['preis'] < 500000]
        df = df[df['preis'] > 0]
        df = df[stats.zscore(df.preis) < z_score]

        # Age
        df = df[df['auto_alter'] >= 0]
        df = df[stats.zscore(df['auto_alter']) < z_score]

        # Power
        df = df[df['auto_leistung_ps'] > 20]
        df = df[stats.zscore(df['auto_leistung_ps']) < z_score]

        # Konvertierung
        df = df.join(pd.get_dummies(df['auto_getriebe'], prefix='getriebe'))
        df = df.join(pd.get_dummies(df['auto_kraftstoff'], prefix='fuel'))
        df = df.join(pd.get_dummies(df['auto_schaden'], prefix='schaden'))
        df.sort_values(by='datum_erstellt', inplace=True)
        df['datum_verschwunden_date'] = pd.to_datetime(df['datum_verschwunden']).dt.date
        df['datum_erstellt_date'] = pd.to_datetime(df['datum_erstellt']).dt.date

        # =============================================================================
        #         df = df.drop(columns=['auto_baujahr', 'id', 'automodell_id', 'name',
        #                               'postleitzahl', 'datum_erstellt', 'datum_verschwunden',
        #                               'anzahl_tage_online'])  # Anzahl Tage verschlechter Regression !!
        #
        #         self.columns = [
        #             'auto_alter', 'auto_leistung_ps', 'auto_kilometerstand',
        #             'getriebe_0', 'getriebe_1',
        #             'fuel_benzin', 'fuel_diesel', 'fuel_cng', 'fuel_lpg', 'fuel_hybrid', 'fuel_elektro',
        #             'schaden_0', 'schaden_1',
        #             'preis'
        #         ]
        #
        #         for col in self.columns:
        #             if col not in df.columns:
        #                 df[col] = 0
        #         df = df[self.columns]
        # =============================================================================

        return df
