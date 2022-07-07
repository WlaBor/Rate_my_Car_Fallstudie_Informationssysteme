# -*- coding: utf-8 -*-
"""
Created on Mon Jul  4 20:07:00 2022

@author: wladi
"""
import sqlite3
import uuid
from datetime import datetime
import pandas as pd


class Suchanfragen:

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

    def init_table(self):
        conn = self.create_connection()
        if conn == None:
            return

        c = conn.cursor()

        try:
            c.execute('''
                      CREATE TABLE IF NOT EXISTS SUCHEN
                      ([id] TEXT NOT NULL PRIMARY KEY,
                       [user_name] TEXT NOT NULL,
                       [zeitpunkt] TEXT NOT NULL,
                       [eingaben_brand] TEXT NOT NULL,
                       [eingaben_model] TEXT NOT NULL,
                       [eingaben_vehicletype] TEXT NOT NULL,
                       [eingaben_kilometerstand] REAL NOT NULL,
                       [eingaben_leistung_ps] REAL NOT NULL,
                       [eingaben_alter] INTEGER NOT NULL,
                       [eingaben_erstzulassung] INTEGER NOT NULL,
                       [eingaben_getriebe] INTEGER NOT NULL,
                       [eingaben_fueltype] TEXT NOT NULL,
                       [eingaben_schaden_vorhanden] INTEGER NOT NULL,
                       [prognose_preis] REAL NOT NULL
                       )
                      ''')
            print('SUCHEN Tabelle erfolgreich')
        except Exception as ex:
            print('Fehler bei SUCHEN Tabelle')
            print(ex)
        conn.close()

    def save_suche(self, user_name,
                   brand,
                   model,
                   vehicletype,
                   kilometer,
                   leistung,
                   alter,
                   getriebe,
                   fuel,
                   schaden,
                   preis):

        insert_tuple = (str(uuid.uuid4()), user_name, datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        brand, model, vehicletype, kilometer, leistung, alter, 2016-alter, getriebe,
                        fuel, schaden, preis)
        print(insert_tuple)

        conn = self.create_connection()
        if conn == None:
            return

        c = conn.cursor()

        try:
            c.execute('''
                      INSERT INTO SUCHEN VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                      ''', insert_tuple)
            conn.commit()
            print('Speichern erfolgreich.')
        except Exception as ex:
            print('Fehler bei SUCHEN Tabelle Insert')
            print(ex)

        conn.close()

    def load_data_from_user_as_df(self, username):
        conn = self.create_connection()
        if conn == None:
            return
        export = pd.read_sql_query("""SELECT * FROM SUCHEN WHERE user_name ="{}" """.format(username), conn)
        conn.close()
        return export
