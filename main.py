from flask import Flask, render_template, request, redirect
import json

import connection, mail

run = Flask(__name__)

# run = Flask(__name__, 
#             static_folder=r"D:\PythonProjects\Wi_Projekt_2\Bilder", 
#             template_folder=r"D:\PythonProjects\Wi_Projekt_2")'

global current_profile

@run.route("/")
def load():
    return render_template("login.html")

@run.route("/login", methods=["GET", "POST"])
def login():
    global current_profile
    
    user_inputs = request.form.to_dict()
    e_mail = user_inputs["e_mail"]
    pw = user_inputs["pw"]
    
    matching = con.login(e_mail, pw)
   
    if matching:
        current_profile = e_mail
        print(current_profile)
        return redirect("/main")
    else:
        return render_template(r"login.html", matching = "Invalid", e_mail = e_mail)
    
@run.route("/reg")
def reg():
    return render_template(r"registration.html")

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

    pw_matching = None
    if pw != pw_w:
        pw_matching = "Invalid"
        # return render_template(r"registration.html", pw_matching = "Invalid", 
        #                        e_mail = e_mail, last_name = last_name, first_name = first_name, street = street, 
        #                        postal_code = postal_code, city = city, region = region)

    e_mail_not_exists = con.existing_email(e_mail) and mail.check_mail(e_mail)

    if e_mail_not_exists and pw_matching == None:
        con.new_profil(e_mail, pw, last_name, first_name, street, postal_code, city, region)
        mail.write_mail(e_mail)
        return redirect("/reg_log")
    
    return render_template(r"registration.html", e_mail_exists= None if e_mail_not_exists else "Invalid", pw_matching = pw_matching,
                            e_mail = e_mail, last_name = last_name, first_name = first_name, street = street, 
                            postal_code = postal_code, city = city, region = region)

@run.route("/reg_log")
def reg_log():
    return render_template(r"after_registration.html")

@run.route("/booking", methods=["GET", "POST"])
def booking():
    return render_template(r"profile2.html")

@run.route("/book", methods=["GET", "POST"])
def book():
    user_inputs = request.form.to_dict()
    print(user_inputs)

    mapping = {"abschnitt_eins_a":[False, False, False, False], 
            "abschnitt_eins_b":[False, False, False, False], 
            "abschnitt_drei_a":[False, False, False, False, False], 
            "abschnitt_drei_b":[False, False, False]}
    
    if user_inputs["tabs-two"] == "1":
        try:
            mapping["abschnitt_eins_a"][int(user_inputs["genehmingungsfrei"])] = True
        except:
            pass
        try:
            mapping["abschnitt_eins_b"][int(user_inputs["genehmingungspflicht"])] = True
        except:
            pass
        try:
            mapping["abschnitt_drei_a"][int(user_inputs["art"])] = True
        except:
            pass
        try:   
            mapping["abschnitt_drei_b"][int(user_inputs["ausstatt"])] = True
        except:
            pass
            # TODO: Error shit implementieren, dass alles ausgefühlt ist (hier nen return und dann Einblendung in html)

    # TODO: Fehler abfangen falls Uhrzeit leer ist
    uhrzeit = user_inputs["zeitpunkt"].split("T")
    datum = uhrzeit[0].split("-")
    # TODO: Fehler abfangen leere Behandlungsstätte

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



@run.route("/main", methods=["GET", "POST"])
def main():
    bookings_data = con.my_bookings(current_profile)
    bookings_list = []
    for row in bookings_data:
        full_date = row[0].strftime("%d/%m/%Y")
        print(row[0])
        column_dic = {'date': full_date, 'time': row[1], 'behandlungsstaette': row[2]}
        bookings_list.append(column_dic)
    print(bookings_list)
    return render_template(r"mainpage.html", bookings_list=bookings_list)

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

@run.route("/myprof", methods=["GET", "POST"])
def my_prof():
    profile_data = con.my_profile(current_profile)
    last_name = profile_data[0][0]
    first_name = profile_data[0][1]
    street = profile_data[0][2]
    postal_code = profile_data[0][3]
    city = profile_data[0][4]
    region = profile_data[0][5]

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
        return redirect("/main")
    elif "old_pw" in user_inputs:
        if con.login(current_profile, user_inputs["old_pw"]):
            con.change_pw(email=current_profile, pw=user_inputs["new_pw"])
            return redirect("/main")
        else:
            return render_template(r"my_profile.html", last_name = last_name, first_name = first_name, street = street, 
                            postal_code = postal_code, city = city, region = region, matching = "Invalid")
        
    return render_template(r"my_profile.html", last_name = last_name, first_name = first_name, street = street, 
                            postal_code = postal_code, city = city, region = region)
    

if __name__ == "__main__":
    global con
    con = connection.Connection()
    run.run(debug=True)
    