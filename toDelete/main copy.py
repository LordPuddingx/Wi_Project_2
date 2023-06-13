from flask import Flask, render_template, request, redirect

import sqlalchemy
from sqlalchemy.sql import text
import urllib
import pandas as pd

params = (
        "Driver={ODBC Driver 17 for SQL Server};"
        + "Server=localhost;"
        + "Database=Test;"
        + "Trusted_Connection=yes"
    )

run = Flask(__name__, 
            static_folder=r"C:\Users\Nik\Documents\HFT\6. Semester\WI-Projekt-2\Dummy\Code\Bilder", 
            template_folder=r"C:\Users\Nik\Documents\HFT\6. Semester\WI-Projekt-2\Dummy\Code")

@run.route("/")
def load():
    return render_template(r"index.html")

@run.route("/login", methods=["GET", "POST"])
def login():
    user_inputs = request.form.to_dict()
    name = user_inputs["name"]
    pw = user_inputs["pw"]
    try: 
        db_params = urllib.parse.quote_plus(params)

        engine = sqlalchemy.create_engine(
        "mssql+pyodbc:///?odbc_connect={}".format(db_params), fast_executemany=True
        ).connect()

        sql = text(f"SELECT passwort FROM test WHERE name='{str(name)}';")
        tmp = engine.execute(sql)

        res = pd.DataFrame(tmp.fetchall())
        res.columns = tmp.keys()

        engine.commit()
        engine.close()

        matching = True if res["passwort"][0] == pw else False

        if matching:
            return redirect("/booking")
        else:
            return render_template(r"index.html", matching = "Invalid")
    except Exception as e:
        print("Error while connection to Database: ", e)
        return render_template(r"index.html", matching = "Invalid")

@run.route("/booking")
def booking():
    return render_template(r"profile.html")

if __name__ == "__main__":
    run.run(debug=True)
    