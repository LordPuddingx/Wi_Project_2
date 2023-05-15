from flask import Flask, render_template, request, redirect

import connection, mail

run = Flask(__name__)

# run = Flask(__name__, 
#             static_folder=r"D:\PythonProjects\Wi_Projekt_2\Bilder", 
#             template_folder=r"D:\PythonProjects\Wi_Projekt_2")'

@run.route("/")
def load():
    return render_template("login.html")

@run.route("/login", methods=["GET", "POST"])
def login():
    user_inputs = request.form.to_dict()
    e_mail = user_inputs["e_mail"]
    pw = user_inputs["pw"]
    
    matching = con.login(e_mail, pw)
   
    if matching:
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

    e_mail_not_exists = con.existing_email(e_mail)

    if e_mail_not_exists and pw_matching == None:
        con.new_profil(e_mail, pw, last_name, first_name, street, postal_code, city, region)
        mail.write_mail(e_mail)
        return redirect("/")
    
    return render_template(r"registration.html", e_mail_exists= None if e_mail_not_exists else "Invalid", pw_matching = pw_matching,
                            e_mail = e_mail, last_name = last_name, first_name = first_name, street = street, 
                            postal_code = postal_code, city = city, region = region)

@run.route("/booking")
def booking():
    return render_template(r"profile.html")

@run.route("/book", methods=["GET", "POST"])
def book():
    #print(request.form.to_dict())
    print(request.json())
    # user_inputs = request.form["asdf"]
    # print("ASDF:", user_inputs)
    # date = user_inputs["datetime"]
    # bef = user_inputs["bef"]
    # print(bef)
    # print(date)

    return render_template(r"profile.html")


if __name__ == "__main__":
    global con
    con = connection.Connection()
    run.run(debug=True)
    