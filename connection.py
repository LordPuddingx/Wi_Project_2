import sqlalchemy
from sqlalchemy.sql import text
import urllib
import pandas as pd
import hashlib

class Connection():
    params = (
        "Driver={ODBC Driver 17 for SQL Server};"
        + "Server=localhost;"
        + "Database=Kunden_DB;"
        + "Trusted_Connection=yes"
    )


    def __init__(self):
        try: 
            db_params = urllib.parse.quote_plus(self.params)

            self.engine = sqlalchemy.create_engine(
            "mssql+pyodbc:///?odbc_connect={}".format(db_params), fast_executemany=True
            ).connect()
        except Exception as e:
            print("Error while connection to Database: ", e)

    def login(self, e_mail, pw):
        sql = text(f"SELECT pw FROM tblLogin WHERE e_mail='{e_mail}';")
        res = pd.read_sql(sql, self.engine)
       
        return True if not res.empty and res["pw"][0] == hashlib.sha256(pw.encode("UTF-8")).hexdigest() else False
    
    def new_profil(self, e_mail, pw, last_name, first_name, street, postal_code, city, region):
        # Insert new Profil in Login Table
        pw_hash = hashlib.sha256(pw.encode("UTF-8")).hexdigest()
        sqlLogin = text(f"INSERT INTO tblLogin (E_Mail, PW) VALUES ('{e_mail}', '{pw_hash}')")
        self.engine.execute(sqlLogin)

        # Insert new Profil in Profil Table
        sqlProfil = text(f"INSERT INTO tblProfil (E_Mail, Nachname, Vorname, Strasse, PLZ, Stadt, Bundesland) VALUES ('{e_mail}', '{last_name}', '{first_name}', '{street}', '{postal_code}', '{city}', '{region}')")
        self.engine.execute(sqlProfil)

        self.engine.commit()

    def existing_email(self, e_mail):
        sql = text(f"SELECT COUNT(1) AS result FROM tblLogin WHERE e_mail='{e_mail}'")
        res = pd.read_sql(sql, self.engine)
        return True if res["result"][0] == 0 else False

    def tschein_test(self, voll_teilstationaere_Behandlung, vor_nachstationaere_Behandlung, ambulante_Behandlung, anderer_Grund, anderer_Grund_Kommentar):
        voll_teilstationaere_Behandlung = voll_teilstationaere_Behandlung
        vor_nachstationaere_Behandlung = vor_nachstationaere_Behandlung
        ambulante_Behandlung = ambulante_Behandlung
        anderer_Grund = anderer_Grund
        anderer_Grund_Kommentar = anderer_Grund_Kommentar
        sqlTest = text(f"INSERT INTO tblTest SELECT '{voll_teilstationaere_Behandlung}', '{vor_nachstationaere_Behandlung}', '{ambulante_Behandlung}', '{anderer_Grund}', '{anderer_Grund_Kommentar}'")
        # sqlTest = text(f"INSERT INTO tblTest (voll_teilstationaere_Behandlung, vor_nachstationaere_Behandlung, vor_nachstationaere_Behandlung, ambulante_Behandlung, anderer_Grund, anderer_Grund_Kommentar) VALUES ('{voll_teilstationaere_Behandlung}', '{vor_nachstationaere_Behandlung}', '{ambulante_Behandlung}', '{anderer_Grund}', '{anderer_Grund_Kommentar}')")
        self.engine.execute(sqlTest)
        self.engine.commit()

