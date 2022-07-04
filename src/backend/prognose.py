# -*- coding: utf-8 -*-
"""
Prognose und sonstige Auswertungen
"""

import sqlite3
import pandas as pd
from scipy import stats
import numpy as np
from catboost import CatBoostRegressor
from sklearn.metrics import r2_score


class Prognose:

    def __init__(self, controller,
                 brand, model, vehicletype,
                 auto_alter,
                 auto_leistung_ps,
                 auto_kilometerstand,
                 getriebe,
                 antriebsart,
                 schaden_vorhanden, *args, **kwargs):
        self.controller = controller
        self.db_path = controller.db_path
        self.brand = brand
        self.model = model
        self.vehicletype = vehicletype
        self.auto_alter = auto_alter
        self.auto_leistung_ps = auto_leistung_ps
        self.auto_kilometerstand = auto_kilometerstand
        self.getriebe = getriebe
        self.antriebsart = antriebsart
        self.schaden_vorhanden = schaden_vorhanden
        self.erszulassung = kwargs.pop('erstzulassung', None)

        print('Regression für {}-{}-{}'.format(self.brand, self.model, self.vehicletype))
        print('Alter: ' + str(self.auto_alter))
        print('Leistung: ' + str(self.auto_leistung_ps))
        print('Kilometerstand: ' + str(self.auto_kilometerstand))
        print('Getriebe: ' + str(self.getriebe))
        print('Antriebsart: ' + str(self.antriebsart))
        print('Schaden vorhanden?: ' + str(self.schaden_vorhanden))

        # Reihenfolge Spalten
        self.columns = [
            'auto_alter', 'auto_leistung_ps', 'auto_kilometerstand',
            'getriebe_0', 'getriebe_1',
            'fuel_benzin', 'fuel_diesel', 'fuel_cng', 'fuel_lpg', 'fuel_hybrid', 'fuel_elektro',
            'schaden_0', 'schaden_1',
            'preis'
        ]

        # Daten aus Datenbank laden und als Dataframe abspeichern
        self.load_data()

        # Prognosemodell erstellen
        self.create_model()

    def load_data(self):

        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''
                  SELECT id FROM AUTOMODELL
                  WHERE (marke, model, fahrzeug_typ) = (?,?,?)
                  ORDER BY model
                  ''', (self.brand, self.model, self.vehicletype))

        self.auto_id = [element[0] for element in c.fetchall()][0]

        self.raw_df = pd.read_sql('''
                                  SELECT * FROM ANZEIGE WHERE automodell_id = "{}"
                                  '''.format(self.auto_id), conn)

        print('Anzahl Daten ungefiltert: ' + str(len(self.raw_df)))

        conn.close()

    def create_model(self):
        df = self.raw_df.copy()

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
        df = df.join(pd.get_dummies(df['auto_getriebe'], prefix='getriebe')).drop(columns=['auto_getriebe'])
        df = df.join(pd.get_dummies(df['auto_kraftstoff'], prefix='fuel')).drop(columns=['auto_kraftstoff'])
        df = df.join(pd.get_dummies(df['auto_schaden'], prefix='schaden')).drop(columns=['auto_schaden'])
        df.sort_values(by='datum_erstellt', inplace=True)
        df = df.drop(columns=['auto_baujahr', 'id', 'automodell_id', 'name',
                              'postleitzahl', 'datum_erstellt', 'datum_verschwunden',
                              'anzahl_tage_online'])  # Anzahl Tage verschlechter Regression !!

        for col in self.columns:
            if col not in df.columns:
                df[col] = 0
        df = df[self.columns]

        self.df_model = df
        print('Anzahl Daten gefiltert: ' + str(len(df)))

        self.std_preis = df['preis'].std()
        print('Standardabweichung: ' + str(self.std_preis))

        # Split Test Train
        train_set, test_set = np.split(df, [int(.85 * len(df))])
        print('\nModellvariablen:')
        print(train_set.drop(columns='preis').dtypes)

        X_train = train_set.drop(columns='preis').to_numpy()
        Y_train = train_set.preis.to_numpy()
        X_test = test_set.drop(columns='preis').to_numpy()
        Y_test = test_set.preis.to_numpy()

        # Modelbildung und Validierung
        # CatboostRegressor
        self.model = CatBoostRegressor(iterations=1000, learning_rate=0.02, silent=True)
        self.model.fit(
            X_train, Y_train,
            eval_set=(X_test, Y_test),
        )
        test_prediction = self.model.predict(X_test)
        print('R-Wert CatboostRegressor: ' + str(r2_score(y_true=Y_test, y_pred=test_prediction)))
        self.r_score = r2_score(y_true=Y_test, y_pred=test_prediction)

    # ////////////////////////
    # Prognose durchführen
    def make_prediction(self):
        auto_alter = self.auto_alter
        auto_leistung_ps = self.auto_leistung_ps
        auto_kilometerstand = self.auto_kilometerstand

        if self.getriebe == 'Automatik':
            getriebe_1 = 1
            getriebe_0 = 0
        else:
            getriebe_0 = 1
            getriebe_1 = 0

        fuel_benzin = 0
        fuel_diesel = 0
        fuel_cng = 0
        fuel_lpg = 0
        fuel_hybrid = 0
        fuel_elektro = 0
        if self.antriebsart == 'Benzin':
            fuel_benzin = 1
        elif self.antriebsart == 'Diesel':
            fuel_diesel = 1
        elif self.antriebsart == 'CNG':
            fuel_cng = 1
        elif self.antriebsart == 'LPG':
            fuel_lpg = 1
        elif self.antriebsart == 'Hybrid':
            fuel_hybrid = 1
        elif self.antriebsart == 'Elektro':
            fuel_elektro = 1

        if self.schaden_vorhanden == 1:
            schaden_1 = 1
            schaden_0 = 0
        else:
            schaden_0 = 1
            schaden_1 = 0

        eingabetupel = (
            auto_alter,
            auto_leistung_ps,
            auto_kilometerstand,
            getriebe_0,
            getriebe_1,
            fuel_benzin,
            fuel_diesel,
            fuel_cng,
            fuel_lpg,
            fuel_hybrid,
            fuel_elektro,
            schaden_0,
            schaden_1,
        )

        return self.model.predict(np.array(eingabetupel))
