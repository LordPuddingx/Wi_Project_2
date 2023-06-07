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

    def fahrtenbuchung(self, email, datum, ort, auf_rechnung, voll_teilstationaere_Behandlung, vor_nachstationaere_Behandlung, ambulante_Behandlung, anderer_Grund, anderer_Grund_Kommentar, hochfrequente_Behandlung, vergleichbarer_Ausnahmefall, dauerhafte_Mobilitätsbeeinträchtigung, anderer_Grund_für_Fahrt, Taxi, KTW, KTW_Begründung, RTW, NAW, andere, andere_Begründung, Rollstuhl, Tragestuhl, liegend, begruendung_sonstige):
 
        #sqlTest = text(f"INSERT INTO tblTest SELECT '{voll_teilstationaere_Behandlung}', '{vor_nachstationaere_Behandlung}', '{ambulante_Behandlung}', '{anderer_Grund}', '{anderer_Grund_Kommentar}'")
        # sqlTest = text(f"INSERT INTO tblTest (voll_teilstationaere_Behandlung, vor_nachstationaere_Behandlung, vor_nachstationaere_Behandlung, ambulante_Behandlung, anderer_Grund, anderer_Grund_Kommentar) VALUES ('{voll_teilstationaere_Behandlung}', '{vor_nachstationaere_Behandlung}', '{ambulante_Behandlung}', '{anderer_Grund}', '{anderer_Grund_Kommentar}')")
        sql = text(
            """INSERT INTO [tblFahrtenbuchung]
           ([email]
           ,[datum]
           ,[Behandlungsstätte]
           ,[auf_rechnung]
           ,[voll_teilstationaere_Behandlung]
           ,[vor_nachstationaere_BehandlungPw]
           ,[ambulante_Behandlung]
           ,[anderer_Grund]
           ,[anderer_Grund_Kommentar]
           ,[hochfrequente_Behandlung]
           ,[vergleichbarer_Ausnahmefall]
           ,[dauerhafte_Mobilitätsbeeinträchtigung]
           ,[anderer_Grund_für_Fahrt]
           ,[Taxi]
           ,[KTW]
           ,[KTW_Begründung]
           ,[RTW]
           ,[NAW]
           ,[andere]
           ,[andere_Begründung]
           ,[Rollstuhl]
           ,[Tragestuhl]
           ,[liegend]
           ,[begruendung_sonstige])
            VALUES ("""
            + f"'{email}', '{datum}', '{ort}','{auf_rechnung}','{1 if voll_teilstationaere_Behandlung else 0}','{1 if vor_nachstationaere_Behandlung else 0}','{1 if ambulante_Behandlung else 0}','{1 if anderer_Grund else 0}','{anderer_Grund_Kommentar}','{1 if hochfrequente_Behandlung else 0}','{1 if vergleichbarer_Ausnahmefall else 0}','{1 if dauerhafte_Mobilitätsbeeinträchtigung else 0}','{1 if anderer_Grund_für_Fahrt else 0}','{1 if Taxi else 0}','{1 if KTW else 0}','{KTW_Begründung}','{1 if RTW else 0}','{1 if NAW else 0}','{1 if andere else 0}','{andere_Begründung}','{1 if Rollstuhl else 0}','{1 if Tragestuhl else 0}','{1 if liegend else 0}', '{begruendung_sonstige}');"
        )
        self.engine.execute(sql)
        self.engine.commit()

    def my_profile(self, e_mail):
        # sql = text(f"Select * from tblFahrtenbuchung Where email = '{e_mail}'")
        sql = text(f"SELECT Nachname, Vorname, Strasse, PLZ, Stadt, Bundesland from tblProfil WHERE E_Mail = '{e_mail}'")
        q_execute = self.engine.execute(sql)
        profile_data = q_execute.fetchall()
        return profile_data

    def my_bookings(self, e_mail):
        sql = text(f"Select Convert(DATE, datum), CONCAT(Datepart(hh, datum), ':', DATEPART(mi, datum)), Behandlungsstätte from tblFahrtenbuchung Where EMail = '{e_mail}' ORDER BY datum ASC")
        q_execute = self.engine.execute(sql)
        bookings_data = q_execute.fetchall()
        return bookings_data