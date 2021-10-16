import os

from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)
##postgress
engine = create_engine("mysql+pymysql://root:IRfan18--@localhost:3306/V_M_S")


db = scoped_session(sessionmaker(bind=engine))


@app.route("/", methods=['GET'])
def index():
    return render_template("index.html")

@app.route("/intro", methods=['POST', 'GET'])
def intro():
    if request.method == "POST":

        fname = request.form.get("f_name")
        lname = request.form.get("l_name")
        FatherName = request.form.get("fathername")
        CNIC = request.form.get("cnic")
        Phone = request.form.get("p_num")
        Dossage = request.form.get("dose")
        AGE = request.form.get("age")
        CITY = request.form.get("city")
        Vaccine = request.form.get("V_name")
        gender = request.form.get("sex")
        db.execute("INSERT into persons(f_name, l_name, fathername, cnic, p_num, dose, age, city, V_name, sex) VALUES (:f_name, :l_name, :fathername, :cnic, :p_num, :dose, :age, :city, :V_name, :sex)",
                {"f_name":fname, "l_name": lname, "fathername":FatherName, "cnic":CNIC, "p_num":Phone, "dose":Dossage, "age":AGE, "city":CITY, "V_name":Vaccine, "sex":gender})
        db.commit()

        # Get all records again
        students = db.execute("SELECT * FROM persons").fetchall()
        return render_template("intro.html", students=students)
    else:
        students = db.execute("SELECT * FROM persons").fetchall()
        return render_template("intro.html", students=students)

@app.route("/update/<int:id>/", methods=['POST','GET'])
def update(id):
    if request.method=="POST":
        fname = request.form.get("f_name")
        lname = request.form.get("l_name")
        FatherName = request.form.get("fathername")
        CNIC = request.form.get("cnic")
        Phone = request.form.get("p_num")
        Dossage = request.form.get("dose")
        AGE = request.form.get("age")
        CITY = request.form.get("city")
        Vaccine = request.form.get("V_name")
        gender = request.form.get("sex")
        db.execute("Update persons SET f_name = :fname, l_name = :lname, fathername = :FatherName, cnic = :CNIC, p_num = :Phone, dose = :Dossage, age = :AGE, city = :CITY, V_name = :Vaccine, sex = :gender where id = :id",
                {"fname":fname, "lname": lname, "FatherName":FatherName, "CNIC":CNIC, "Phone":Phone, "Dossage":Dossage, "AGE":AGE, "CITY":CITY, "Vaccine":Vaccine, "gender":gender, "id":id})
        db.commit()
        return redirect(url_for('intro'))
    else:
        stud = db.execute("SELECT * FROM persons WHERE id = :id", {"id": id}).fetchone()
        return render_template("update.html", stud=stud, id=id)


@app.route("/delete/<int:id>/")
def delete(id):
    stud = db.execute("SELECT * FROM persons WHERE id = :id", {"id": id}).fetchone()
    if stud is None:
        return "No record found by ID = " + str(id) +". Kindly go back to <a href='/intro'> Intro </a>"
    else:
        stud = db.execute("delete FROM persons WHERE id = " + str(id))
        db.commit()
        return redirect(url_for('intro'))

@app.route("/ir", methods=['GET'])
def insert_new_student():
    return render_template("insert_new_record.html")

if __name__ == "__main__":
    app.run(debug=True)
