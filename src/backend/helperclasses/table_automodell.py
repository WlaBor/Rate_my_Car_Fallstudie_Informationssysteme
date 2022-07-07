# -*- coding: utf-8 -*-
"""
Created on Sat Jun  4 13:08:09 2022

@author: wladi
"""
import sqlite3
import uuid


class Automodel:

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
            c.execute('''
                      CREATE TABLE IF NOT EXISTS AUTOMODELL
                      ([id] TEXT NOT NULL PRIMARY KEY,
                       [marke] TEXT NOT NULL,
                       [model] TEXT NOT NULL,
                       [fahrzeug_typ] TEXT NOT NULL
                       )
                      ''')
            print('AUTOMODELL Tabelle erfolgreich')
        except Exception as ex:
            print('Fehler bei AUTOMODELL Tabelle')
            print(ex)
        conn.close()

    # ////////////////////////////////////////////
    # Automodell speichern
    def save_Automodell(self, marke, model, fahrzeug_typ):
        insert_tuple = (str(uuid.uuid4()), marke, model, fahrzeug_typ)

        conn = self.create_connection()
        if conn == None:
            return

        c = conn.cursor()

        try:
            c.execute('''
                      INSERT INTO AUTOMODELL (id, marke, model, fahrzeug_typ) VALUES (?,?,?,?)
                      ''', insert_tuple)
            conn.commit()
        except Exception as ex:
            print('Fehler bei AUTOMODELL Tabelle Insert')
            print(ex)

        conn.close()

    # ////////////////////////////////////////////
    # gebe alle unterschiedlichen Automarken
    def get_unqiue_marken(self):
        conn = self.create_connection()
        if conn == None:
            return

        c = conn.cursor()

        results = []

        try:
            c.execute('''
                      SELECT DISTINCT marke FROM AUTOMODELL
                      ORDER BY marke
                      ''')
            results = [element[0] for element in c.fetchall()]
        except Exception as ex:
            print('Fehler bei AUTOMODELL Tabelle get_unqiue_marken')
            print(ex)

        conn.close()

        return results

    # ////////////////////////////////////////////
    # Gebe alle unterschiedlichen Modelle einer Automarke
    def get_unique_models_from_brand(self, brand):
        conn = self.create_connection()
        if conn == None:
            return

        c = conn.cursor()

        results = []

        try:
            c.execute('''
                      SELECT DISTINCT model FROM AUTOMODELL
                      WHERE marke = ?
                      ORDER BY model
                      ''', (brand,))
            results = [element[0] for element in c.fetchall()]
        except Exception as ex:
            print('Fehler bei AUTOMODELL Tabelle get_unique_models_from_brand')
            print(ex)

        conn.close()

        return results

    # ////////////////////////////////////////////
    # Gebe alle unterschiedlichen Fahrzeugtypen einer Marke-Model Kombination
    def get_unique_cartype_from_brand_model(self, brand, model):
        conn = self.create_connection()
        if conn == None:
            return

        c = conn.cursor()

        results = []

        try:
            c.execute('''
                      SELECT DISTINCT fahrzeug_typ FROM AUTOMODELL
                      WHERE (marke, model) = (?,?)
                      ORDER BY fahrzeug_typ
                      ''', (brand, model,))
            results = [element[0] for element in c.fetchall()]
        except Exception as ex:
            print('Fehler bei AUTOMODELL Tabelle get_unique_cartype_from_brand_model')
            print(ex)

        conn.close()

        return results

    # ////////////////////////////////////////////
    # get id
    def get_id(self, brand, model, vehicletype):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''
                  SELECT id FROM AUTOMODELL
                  WHERE (marke, model, fahrzeug_typ) = (?,?,?)
                  ORDER BY model
                  ''', (brand, model, vehicletype))

        auto_id = [element[0] for element in c.fetchall()][0]
        conn.close()
        return auto_id

    # ////////////////////////////////////////////
    # Gebe alle unterschiedlichen Getriebe einer Marke-Model-vehicle Kombination
    def get_unique_getriebe(self, brand, model, vehicletype):
        auto_id = self.get_id(brand, model, vehicletype)

        conn = self.create_connection()
        if conn == None:
            return

        c = conn.cursor()

        results = []

        try:
            print('test1')
            c.execute('''
                      SELECT DISTINCT auto_getriebe FROM ANZEIGE
                      WHERE (automodell_id) = (?)
                      ''', (auto_id,))
            print('test2')
            results = [element[0] for element in c.fetchall()]
            new_labels = []
            for x in results:
                if x == 0:
                    new_labels.append('Manuell')
                elif x == 1:
                    new_labels.append('Automatik')
            results = new_labels
        except Exception as ex:
            print('Fehler bei AUTOMODELL Tabelle get_unique_getriebe')
            print(ex)

        conn.close()

        return results
