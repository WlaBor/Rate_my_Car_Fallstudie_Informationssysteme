# -*- coding: utf-8 -*-
"""
Created on Fri Jun  3 19:53:39 2022

@author: wladi
"""

import sqlite3

from backend.helperclasses.table_user import User


class Backend:

    def __init__(self, db_path):
        self.db_path = db_path

        self.User = User(self.db_path)
