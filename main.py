from flask import Flask, render_template, request, redirect
import json

import connection, mail

run = Flask(__name__)

# run = Flask(__name__, 
#             static_folder=r"D:\PythonProjects\Wi_Projekt_2\Bilder", 
#             template_folder=r"D:\PythonProjects\Wi_Projekt_2")'

current_profile = None

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

@run.route("/booking")
def booking():
    print(current_profile)
    return render_template(r"profile2.html")

@run.route("/book", methods=["GET", "POST"])
def book():
    body = request.get_data()
    json_data = request.get_json()
    voll_teilstationaere_Behandlung = str(json_data['voll_teilstationaere_Behandlung'])
    vor_nachstationaere_Behandlung = str(json_data['vor_nachstationaere_Behandlung'])
    ambulante_Behandlung = str(json_data['ambulante_Behandlung'])
    anderer_Grund = str(json_data['anderer_Grund'])
    anderer_Grund_Kommentar = str(json_data['anderer_Grund_Kommentar'])
    con.tschein_test(voll_teilstationaere_Behandlung, vor_nachstationaere_Behandlung,
                     ambulante_Behandlung, anderer_Grund, anderer_Grund_Kommentar)
    #print(request.get_json())
    # user_inputs = request.form["asdf"]
    # print("ASDF:", user_inputs)
    # date = user_inputs["datetime"]
    # bef = user_inputs["bef"]
    # print(bef)
    # print(date)
    return render_template(r"profile2.html")

if __name__ == "__main__":
    global con
    con = connection.Connection()
    run.run(debug=True)
    