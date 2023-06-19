#Importe
import sqlalchemy
from sqlalchemy.sql import text
import urllib
import pandas as pd
import hashlib

# Klasse die ein Verbindung zur Datenbank herstellt. Über diese werden die Inputdaten abgeglichen, 
# in die DB geladen und Outputdaten aus der Datenbank geladen.

class Connection():
    # Parameter zu einer lokalen Microsoft SQL Server-Datenbank. Die Datenbank muss über die "Windows Authentication"
    # und den localhost erreichbar sein. Der MS SQL Server muss den ODBC Driver 17 unterstützen.
    # Der Name der Datenbank muss "Kunden_DB" sein.
    params = (
        "Driver={ODBC Driver 17 for SQL Server};"
        + "Server=localhost;"
        + "Database=Kunden_DB;"
        + "Trusted_Connection=yes"
    )

    # Konstruktor um die Paramter zu parsen und die Verbindung zur Datenbank aufzubauen
    def __init__(self):
        try: 
            db_params = urllib.parse.quote_plus(self.params)

            self.engine = sqlalchemy.create_engine(
            "mssql+pyodbc:///?odbc_connect={}".format(db_params), fast_executemany=True
            ).connect()
        except Exception as e:
            print("Error while connection to Database: ", e)

    # Auslesen des zugehörigen gehashten Passworts zur übergebenen Email. Die Methode gibt "True" zurück wenn 
    # das überebene Passwort und das Passwort in der Datenbank identisch sind, ansonsten wird "False" zurückgegeben
    def login(self, e_mail, pw):
        sql = text(f"SELECT pw FROM tblLogin WHERE e_mail='{e_mail}';")
        res = pd.read_sql(sql, self.engine)
        return True if not res.empty and res["pw"][0] == hashlib.sha256(pw.encode("UTF-8")).hexdigest() else False
    
    # Überprüft ob die übergebene E-Mail in der Datenbank existiert
    def existing_email(self, e_mail):
        sql = text(f"SELECT COUNT(1) AS result FROM tblLogin WHERE e_mail='{e_mail}'")
        res = pd.read_sql(sql, self.engine)
        return True if res["result"][0] == 0 else False
    
    # Anlegen eines neuen Profiles: es wird das Passwort und die Email in der tblLogin-Tabelle abgelegt und
    # in der tblProfile-Tabelle werden die Benutzerdaten gespeichert
    def new_profil(self, e_mail, pw, last_name, first_name, street, postal_code, city, region):
        pw_hash = hashlib.sha256(pw.encode("UTF-8")).hexdigest()
        sqlLogin = text(f"INSERT INTO tblLogin (E_Mail, PW) VALUES ('{e_mail}', '{pw_hash}')")
        self.engine.execute(sqlLogin)

        sqlProfil = text(f"INSERT INTO tblProfil (E_Mail, Nachname, Vorname, Strasse, PLZ, Stadt, Bundesland) VALUES ('{e_mail}', '{last_name}', '{first_name}', '{street}', '{postal_code}', '{city}', '{region}')")
        self.engine.execute(sqlProfil)

        self.engine.commit()

    # Fahrt in die tblFahrtenbuchung-Tabelle schreiben 
    def fahrtenbuchung(self, email, datum, ort, auf_rechnung, voll_teilstationaere_Behandlung, vor_nachstationaere_Behandlung, ambulante_Behandlung, anderer_Grund, anderer_Grund_Kommentar, hochfrequente_Behandlung, vergleichbarer_Ausnahmefall, dauerhafte_Mobilitätsbeeinträchtigung, anderer_Grund_für_Fahrt, Taxi, KTW, KTW_Begründung, RTW, NAW, andere, andere_Begründung, Rollstuhl, Tragestuhl, liegend, begruendung_sonstige):
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

    # Auslesen der Profildaten zu der zugehörigen E-Mail
    def my_profile(self, e_mail):
        sql = text(f"SELECT Nachname, Vorname, Strasse, PLZ, Stadt, Bundesland from tblProfil WHERE E_Mail = '{e_mail}'")
        q_execute = self.engine.execute(sql)
        profile_data = q_execute.fetchall()
        return profile_data

    # Auslesen der Buchungen die zu der übergeben E-Mail gehören und noch in der Zukunft liegen (also noch nicht stattgefunden haben)
    def my_bookings(self, e_mail):
        sql = text(f"SELECT ID, Datum, Behandlungsstätte from tblFahrtenbuchung WHERE EMail = '{e_mail}' AND datum > GETDATE() ORDER BY datum ASC")
        q_execute = self.engine.execute(sql)
        bookings_data = q_execute.fetchall()
        return bookings_data
    
    # Buchung wird storniert und aus der tblFahrtenbuchung entfernen
    def delete_booking(self, id):
        sql = text(f"DELETE FROM tblFahrtenbuchung WHERE ID = '{id}'")
        self.engine.execute(sql)
        self.engine.commit()
    
    # Profildaten aktualisieren
    def change_profile_data(self, e_mail, nachname, vorname, strasse, plz, stadt, bundesland):
        sql = text(f"UPDATE tblProfil SET Nachname = '{nachname}', Vorname = '{vorname}', Strasse = '{strasse}', PLZ = '{plz}', Stadt = '{stadt}', Bundesland = '{bundesland}' WHERE E_Mail LIKE '{e_mail}'")
        self.engine.execute(sql)
        self.engine.commit()

    # Passwort ändern
    def change_pw(self, email, pw):
        pw_hash = hashlib.sha256(pw.encode("UTF-8")).hexdigest()
        sql = text(f"UPDATE tblLogin SET Pw = '{pw_hash}' WHERE E_Mail LIKE '{email}'")
        self.engine.execute(sql)
        self.engine.commit()