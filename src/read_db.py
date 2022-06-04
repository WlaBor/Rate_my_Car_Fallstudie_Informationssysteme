# -*- coding: utf-8 -*-
"""
Created on Sat Jun  4 14:02:29 2022

@author: wladi
"""

import os
import sys
import pandas as pd
import sqlite3

db_path = os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), 'sqlite_db.db')

conn = sqlite3.connect(db_path)

USER = pd.read_sql_query("SELECT * FROM USER", conn)

conn.commit()
conn.close()
