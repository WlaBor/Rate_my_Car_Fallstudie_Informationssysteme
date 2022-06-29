import sqlite3


class User:

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
                      CREATE TABLE IF NOT EXISTS USER
                      ([username] TEXT NOT NULL PRIMARY KEY,
                       [passwort] TEXT NOT NULL,
                       [straße] TEXT,
                       [postleitzahl] INTEGER,
                       [is_premium] INTEGER NOT NULL
                       )
                      ''')
            print('USER Tabelle erfolgreich')
        except Exception as ex:
            print('Fehler bei USER Tabelle')
            print(ex)
        conn.close()

    # ////////////////////////////////////////////
    # User abspeichern
    def save_User(self, username, passwort, strasse=None, plz=None):
        export = (username, passwort, strasse, plz)

        conn = self.create_connection()
        if conn == None:
            return

        c = conn.cursor()

        try:
            c.execute('''
                      INSERT INTO USER (username, passwort, straße, postleitzahl, is_premium)
                      VALUES (?,?,?,?, 0)
                      ''', export)
            conn.commit()
            print('USER INSERT erfolgreich')

        except Exception as ex:
            print('Fehler bei USER Tabelle - INSERT')
            print(ex)

        conn.close()

    # ////////////////////////////////////////////
    # Checken, ob ein User bereits hinterlegt ist
    def check_User(self, username):
        conn = self.create_connection()
        if conn == None:
            return True

        c = conn.cursor()

        result = True

        try:
            c.execute('''
                      SELECT * FROM USER WHERE username = ?
                      ''', (username,))
            records = c.fetchall()
            if len(records) == 0:
                result = False

        except Exception as ex:
            print('Fehler bei USER Tabelle - check User')
            print(ex)

        conn.close()
        print('User ' + str(username) + ' vorhanden? - ' + str(result))
        return result

    # ////////////////////////////////////////////
    # check premium
    def check_UserPremium(self, username):
        conn = self.create_connection()
        if conn == None:
            return True

        c = conn.cursor()

        try:
            c.execute('''
                      SELECT is_premium FROM USER WHERE username = ?
                      ''', (username,))
            records = c.fetchall()
            try:
                records = records[0][0]
            except:
                pass

        except Exception as ex:
            print('Fehler bei USER Tabelle - check User Premium')
            print(ex)
            records = []

        conn.close()
        return records

    # ////////////////////////////////////////////
    # aktiviere premium
    def activate_premium(self, username):
        conn = self.create_connection()
        if conn == None:
            return True

        c = conn.cursor()

        try:
            c.execute('''
                      UPDATE USER
                      SET is_premium = 1
                      WHERE username = ?
                      ''', (username,))

            conn.commit()
        except Exception as ex:
            print('Fehler bei Premium Aktivierung:')
            print(ex)

    # ////////////////////////////////////////////
    # aktiviere premium
    def deactivate_premium(self, username):
        conn = self.create_connection()
        if conn == None:
            return True

        c = conn.cursor()

        try:
            c.execute('''
                      UPDATE USER
                      SET is_premium = 0
                      WHERE username = ?
                      ''', (username,))

            conn.commit()
        except Exception as ex:
            print('Fehler bei Premium Aktivierung:')
            print(ex)

    # ////////////////////////////////////////////
    # Check Passwort von User

    def give_Password_from_User(self, username, password):
        conn = self.create_connection()
        if conn == None:
            return False

        c = conn.cursor()

        result = False

        try:
            c.execute('''
                      SELECT passwort FROM USER WHERE username = ?
                      ''', (username,))
            records = c.fetchall()
            # print(records)
            if records != []:
                # print(records[0])
                if records[0][0] == password:
                    result = True

        except Exception as ex:
            print('Fehler bei USER Tabelle - check User')
            print(ex)

        conn.close()
        print('Passwort von ' + str(username) + ' gleich ' + password + '? - ' + str(result))
        return result
