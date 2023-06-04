from flask import Flask, render_template, request, redirect
import json

import connection, mail

run = Flask(__name__)

# run = Flask(__name__, 
#             static_folder=r"D:\PythonProjects\Wi_Projekt_2\Bilder", 
#             template_folder=r"D:\PythonProjects\Wi_Projekt_2")'

current_profile = "02isdo1bwi@hft-stuttgart.de"

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
        return redirect("/booking")
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
    print(current_profile)

    # TODO: switch einbauen zwischen transportschein und Rechnung: vielleicht kann man den "Tab-value" dafür benutzen
    
    mapping = {"abschnitt_eins_a":[False, False, False, False], 
               "abschnitt_eins_b":[False, False, False, False], 
               "abschnitt_drei_a":[False, False, False, False, False], 
               "abschnitt_drei_b":[False, False, False]}
    
    try:
        mapping["abschnitt_eins_a"][int(user_inputs["genehmingungsfrei"])] = True
        mapping["abschnitt_eins_b"][int(user_inputs["genehmingungspflicht"])] = True
        mapping["abschnitt_drei_a"][int(user_inputs["art"])] = True
        mapping["abschnitt_drei_b"][int(user_inputs["ausstatt"])] = True
    except:
        pass
        # TODO: Error shit implementieren, dass alles ausgefühlt ist (hier nen return und dann Einblendung in html)

    # TODO: Fehler abfangen falls Uhrzeit leer ist
    uhrzeit = user_inputs["zeitpunkt"].split("T")
    datum = uhrzeit[0].split("-")
    print(uhrzeit)

    con.fahrtenbuchung(
        email=current_profile, 
        datum = datum[0]+"-"+datum[2]+"-"+datum[1]+" "+uhrzeit[1],
        ort = user_inputs["ort"],

        voll_teilstationaere_Behandlung = mapping["abschnitt_eins_a"][0],
        vor_nachstationaere_Behandlung = mapping["abschnitt_eins_a"][1],
        ambulante_Behandlung = mapping["abschnitt_eins_a"][2], 
        anderer_Grund = mapping["abschnitt_eins_a"][3], 
        anderer_Grund_Kommentar = user_inputs["einsczwei"], 

        hochfrequente_Behandlung = mapping["abschnitt_eins_b"][0], 
        vergleichbarer_Ausnahmefall = mapping["abschnitt_eins_b"][1], 
        dauerhafte_Mobilitätsbeeinträchtigung = mapping["abschnitt_eins_b"][2], 
        anderer_Grund_für_Fahrt = mapping["abschnitt_eins_b"][3],

        Taxi = mapping["abschnitt_drei_a"][0], 
        KTW = mapping["abschnitt_drei_a"][1], 
        KTW_Begründung = user_inputs["zweieinsc"], 
        RTW = mapping["abschnitt_drei_a"][2], 
        NAW = mapping["abschnitt_drei_a"][3], 
        andere = mapping["abschnitt_drei_a"][0], 
        andere_Begründung = user_inputs["zweieinsd"], 
        Rollstuhl = mapping["abschnitt_drei_b"][0], 
        Tragestuhl = mapping["abschnitt_drei_b"][1], 
        liegend = mapping["abschnitt_drei_a"][2],

        begruendung_sonstige = user_inputs["zweivier"]




    )

    # body = json.loads(request.data)
    # print(body)
    
    # con.fahrtenbuchung(
    #     email=current_profile, 
    #     datum = "2023-05-05",
    #     ort = "Stuggi",
    #     voll_teilstationaere_Behandlung = body.get("voll_teilstationaere_Behandlung"),
    #     vor_nachstationaere_Behandlung = body.get("vor_nachstationaere_Behandlung"),
    #     ambulante_Behandlung = body.get("ambulante_Behandlung"), 
    #     anderer_Grund = body.get("anderer_Grund"), 
    #     anderer_Grund_Kommentar = body.get("anderer_Grund_Kommentar"), 
    #     hochfrequente_Behandlung = body.get("hochfrequente_Behandlung"), 
    #     vergleichbarer_Ausnahmefall = body.get("vergleichbarer_Ausnahmefall"), 
    #     dauerhafte_Mobilitätsbeeinträchtigung = body.get("dauerhafte_Mobilitaetsbeeintraechtigung"), 
    #     anderer_Grund_für_Fahrt = body.get("anderer_Grund_KTW"), 
    #     Taxi = body.get("taxi"), 
    #     KTW = body.get("KTW"), 
    #     KTW_Begründung = body.get("KTW_Begruendung"), 
    #     RTW = body.get("RTW"), 
    #     NAW = body.get("NAW"), 
    #     andere = body.get("andere"), 
    #     andere_Begründung = body.get("andere_Begruendung"), 
    #     Rollstuhl = body.get("rollstuhl"), 
    #     Tragestuhl = body.get("tragestuhl"), 
    #     liegend = body.get("liegend"),
    # )
   
    return redirect(r"/main")

@run.route("/main", methods=["GET", "POST"])
def main():
    return render_template(r"mainpage.html")

if __name__ == "__main__":
    global con
    con = connection.Connection()
    run.run(debug=True)
    