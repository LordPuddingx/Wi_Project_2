# Importe
from flask import Flask, render_template, request, redirect, Response
from datetime import datetime, timedelta
import re

import connection, mail

# Flask-Instanz
run = Flask(__name__)

# globale Variable: speichert das Profil, welches sich gerade angemeldet hat
global current_profile

# Startseite - Login
@run.route("/")
def load():
    current_profile = ""
    return render_template("login.html")

# Überprüfung Login-Daten
@run.route("/login", methods=["GET", "POST"])
def login():
    global current_profile
    
    user_inputs = request.form.to_dict()
    e_mail = user_inputs["e_mail"]
    pw = user_inputs["pw"]
    
    matching = con.login(e_mail, pw)
   
    if matching:
        current_profile = e_mail
        return redirect("/main")
    else:
        return render_template(r"login.html", matching = "Invalid", e_mail = e_mail)

# Registrierungsseite-aufruf  
@run.route("/reg")
def reg():
    return render_template(r"registration.html")

# Registrierungsseite
@run.route("/registration", methods=["GET", "POST"])
def registration():
    user_inputs = request.form.to_dict()
    e_mail = user_inputs["e_mail"]
    pw = user_inputs["pw"]
    pw_w = user_inputs["pw_w"]
    last_name = user_inputs["last_name"]
    first_name = user_inputs["first_name"]
    street = user_inputs["street"]
    postal_code = user_inputs["postal_code"]
    city = user_inputs["city"]
    region = user_inputs["region"]

    # Fehlermeldung: Alle Felder müssen ausgefüllt sein
    if e_mail == "" or last_name == "" or first_name == "" or street == "" or postal_code == "" or city == "" or region == "":
        return render_template(r"registration.html", vollstaendig = "Invalid", vollstaendig_2 = "Invalid", 
                               e_mail = e_mail, last_name = last_name, first_name = first_name, street = street, 
                               postal_code = postal_code, city = city, region = region)

    # Fehlermeldung: Passwörter stimmen nicht überein
    if pw != pw_w:
        return render_template(r"registration.html", pw_matching = "Invalid", 
                               e_mail = e_mail, last_name = last_name, first_name = first_name, street = street, 
                               postal_code = postal_code, city = city, region = region)
    # Fehlermeldung: Passwortanfoderungen wurden nicht erfüllt
    elif len(pw) < 5 or re.search(r"[A-Z]", pw) is None or re.search(r"[a-z]", pw) is None or re.search(r"\d", pw) is None:
        return render_template(r"registration.html", pw_length = "Invalid", 
                               e_mail = e_mail, last_name = last_name, first_name = first_name, street = street, 
                               postal_code = postal_code, city = city, region = region)

    # Überprüfung, ob angegebene E-Mail bereits existiert. Falls true, dann entsprechende Fehlermeldung
    e_mail_not_exists = con.existing_email(e_mail) and mail.check_mail(e_mail)

    # Neues Profil wird angelegt
    if e_mail_not_exists:
        con.new_profil(e_mail, pw, last_name, first_name, street, postal_code, city, region)
        mail.write_mail(e_mail)
        return redirect("/reg_log")
    
    return render_template(r"registration.html", e_mail_exists= None if e_mail_not_exists else "Invalid",
                            e_mail = e_mail, last_name = last_name, first_name = first_name, street = street, 
                            postal_code = postal_code, city = city, region = region)

# Login-Seite aufruf nach Registrierung
@run.route("/reg_log")
def reg_log():
    return render_template(r"login.html")

# Fahrtbuchungsseite
@run.route("/booking", methods=["GET", "POST"])
def booking():
    return render_template(r"booking.html")

# Fahrt buchen
@run.route("/book", methods=["GET", "POST"])
def book():
    user_inputs = request.form.to_dict()
    mapping = {"abschnitt_eins_a":[False, False, False, False], 
            "abschnitt_eins_b":[False, False, False, False], 
            "abschnitt_drei_a":[False, False, False, False, False], 
            "abschnitt_drei_b":[False, False, False]}

    # Checken ob ein Datum eingegeben wurde, ansonsten Seite neuladen mit Fehlermeldung
    if user_inputs["zeitpunkt"] == "":
        return render_template(r"booking.html", datum_check = "Invalid")
    elif user_inputs["zeitpunkt"] < str(datetime.now() + timedelta(days=7)):
        return render_template(r"booking.html", datum_check_2 = "Invalid")

    else:
        uhrzeit = user_inputs["zeitpunkt"].split("T")
        datum = uhrzeit[0].split("-")

    # Checken ob ein Ort eingegeben wurde, ansonsten Seite neuladen mit Fehlermeldung
    if user_inputs["ort"] == "":
        return render_template(r"booking.html", ort_check = "Invalid")

    # Mapping der markierten Inputfelder in die mapping-matrix
    if user_inputs["tabs-two"] == "1":
        if "genehmingungsfrei" in user_inputs and "genehmingungspflicht" in user_inputs and "art" in user_inputs and "ausstatt":
            mapping["abschnitt_eins_a"][int(user_inputs["genehmingungsfrei"])] = True
            mapping["abschnitt_eins_b"][int(user_inputs["genehmingungspflicht"])] = True
            mapping["abschnitt_drei_a"][int(user_inputs["art"])] = True
            mapping["abschnitt_drei_b"][int(user_inputs["ausstatt"])] = True
        else:
            return render_template(r"booking.html", tp_schein_check = "Invalid")

    if user_inputs["tabs-two"] != "1" and "check" not in user_inputs:
        return render_template(r"booking.html", rechnung_check = "Invalid", tab_two = "checked")

    # Fahrt in der Datenbank anlegen
    con.fahrtenbuchung(
        email=current_profile, 
        datum = datum[0]+"-"+datum[2]+"-"+datum[1]+" "+uhrzeit[1],
        ort = user_inputs["ort"],

        auf_rechnung = "Nein" if user_inputs["tabs-two"] == "1" else user_inputs["check"],

        voll_teilstationaere_Behandlung = mapping["abschnitt_eins_a"][0],
        vor_nachstationaere_Behandlung = mapping["abschnitt_eins_a"][1],
        ambulante_Behandlung = mapping["abschnitt_eins_a"][2], 
        anderer_Grund = mapping["abschnitt_eins_a"][3], 
        anderer_Grund_Kommentar = user_inputs["einsczwei"] if user_inputs["tabs-two"] == "1" else "", 

        hochfrequente_Behandlung = mapping["abschnitt_eins_b"][0], 
        vergleichbarer_Ausnahmefall = mapping["abschnitt_eins_b"][1], 
        dauerhafte_Mobilitätsbeeinträchtigung = mapping["abschnitt_eins_b"][2], 
        anderer_Grund_für_Fahrt = mapping["abschnitt_eins_b"][3],

        Taxi = mapping["abschnitt_drei_a"][0], 
        KTW = mapping["abschnitt_drei_a"][1], 
        KTW_Begründung = user_inputs["zweieinsc"] if user_inputs["tabs-two"] == "1" else "", 
        RTW = mapping["abschnitt_drei_a"][2], 
        NAW = mapping["abschnitt_drei_a"][3], 
        andere = mapping["abschnitt_drei_a"][4], 
        andere_Begründung = user_inputs["zweieinsd"] if user_inputs["tabs-two"] == "1" else "", 
        Rollstuhl = mapping["abschnitt_drei_b"][0], 
        Tragestuhl = mapping["abschnitt_drei_b"][1], 
        liegend = mapping["abschnitt_drei_b"][2],

        begruendung_sonstige = user_inputs["zweivier"] if user_inputs["tabs-two"] == "1" else user_inputs["kommentarfeld"])
    
    return redirect(r"/main")

# Hauptseite - Uebersicht Fahrtbuchungen
@run.route("/main", methods=["GET", "POST"])
def main():
    # Auflistung der Fahrtbuchungen
    bookings_data = con.my_bookings(current_profile)
    bookings_list = []
    for row in bookings_data:
        full_date = row[1].strftime("%d/%m/%Y")
        time = row[1].strftime("%H:%M")
        column_dic = {'id': row[0],'date': full_date, 'time': time, 'behandlungsstaette': row[2]}
        bookings_list.append(column_dic)
    user_inputs = request.form.to_dict()

    # Stornierfunktion
    if "cancel" in user_inputs:
        id = user_inputs["cancel"]
        con.delete_booking(id)
        return redirect("/main")
    return render_template(r"mainpage.html", bookings_list=bookings_list)

# Mein Profil
@run.route("/my_profile", methods=["GET", "POST"])
def my_profile():
    profile_data = con.my_profile(current_profile)
    last_name = profile_data[0][0]
    first_name = profile_data[0][1]
    street = profile_data[0][2]
    postal_code = profile_data[0][3]
    city = profile_data[0][4]
    region = profile_data[0][5]

    return render_template(r"my_profile.html", last_name = last_name, first_name = first_name, street = street, 
                            postal_code = postal_code, city = city, region = region)

# Profilseite nach Änderung der Profildaten
@run.route("/myprof", methods=["GET", "POST"])
def my_prof():
    profile_data = con.my_profile(current_profile)
    last_name = profile_data[0][0]
    first_name = profile_data[0][1]
    street = profile_data[0][2]
    postal_code = profile_data[0][3]
    city = profile_data[0][4]
    region = profile_data[0][5]

    # Profildaten speichern
    user_inputs = request.form.to_dict()

    if "speichern" in user_inputs:
        con.change_profile_data(
            e_mail = current_profile,
            nachname = user_inputs["last_name"],
            vorname = user_inputs["first_name"],
            strasse = user_inputs["street"], 
            plz = user_inputs["postal_code"], 
            stadt = user_inputs["city"], 
            bundesland = user_inputs["region"])
        return redirect("/myprof")
    
    # Passwort ändern
    elif "old_pw" in user_inputs:
        if con.login(current_profile, user_inputs["old_pw"]):
            if len(user_inputs["new_pw"]) < 5 or re.search(r"[A-Z]", user_inputs["new_pw"]) is None or re.search(r"[a-z]", user_inputs["new_pw"]) is None or re.search(r"\d", user_inputs["new_pw"]) is None:
                return render_template(r"my_profile.html", last_name = last_name, first_name = first_name, street = street, 
                            postal_code = postal_code, city = city, region = region,  pw_neu_check= "Invalid")
            con.change_pw(email=current_profile, pw=user_inputs["new_pw"])
            return redirect("/myprof")
        else:
            return render_template(r"my_profile.html", last_name = last_name, first_name = first_name, street = street, 
                            postal_code = postal_code, city = city, region = region, matching = "Invalid")
        
    return render_template(r"my_profile.html", last_name = last_name, first_name = first_name, street = street, 
                            postal_code = postal_code, city = city, region = region)
    

if __name__ == "__main__":
    global con
    con = connection.Connection()
    run.run(debug=True)
    