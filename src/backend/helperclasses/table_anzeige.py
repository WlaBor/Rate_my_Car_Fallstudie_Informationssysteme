# -*- coding: utf-8 -*-
"""
Created on Sat Jun  4 13:08:09 2022

@author: wladi
"""
import sqlite3
import uuid


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
