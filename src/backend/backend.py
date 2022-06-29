# -*- coding: utf-8 -*-
"""
Created on Fri Jun  3 19:53:39 2022

@author: wladi
"""

import sqlite3

from backend.helperclasses.table_user import User
from backend.helperclasses.table_automodell import Automodel
from backend.helperclasses.table_anzeige import Anzeige


class Backend:

    def __init__(self, db_path):
        self.db_path = db_path

        # Benutzermodul
        self.User = User(self.db_path)

        # Automodell Modul
        self.Automodel = Automodel(self.db_path)

        # Anzeige Modul
        self.Anzeige = Anzeige(self.db_path)
