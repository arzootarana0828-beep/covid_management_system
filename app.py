from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="my password",
        database="covidmanagement"
    )

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/patients")
def patients():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM patients")
    patients = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template("patients.html", patients=patients)

@app.route("/add", methods=["GET", "POST"])
def add_patient():

    if request.method == "POST":

        name = request.form["name"]
        age = request.form["age"]
        gender = request.form["gender"]
        phone = request.form["phone"]
        address = request.form["address"]
        test_result = request.form["test_result"]
        vaccination_status = request.form["vaccination_status"]

        connection = get_connection()
        cursor = connection.cursor()

        query = """
        INSERT INTO patients
        (name, age, gender, phone, address, test_result, vaccination_status)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        values = (
            name,
            age,
            gender,
            phone,
            address,
            test_result,
            vaccination_status
        )

        cursor.execute(query, values)
        connection.commit()

        cursor.close()
        connection.close()

        return redirect("/patients")

    return render_template("add_patient.html")

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_patient(id):

    connection = get_connection()
    cursor = connection.cursor()

    if request.method == "POST":

        name = request.form["name"]
        age = request.form["age"]
        gender = request.form["gender"]
        phone = request.form["phone"]
        address = request.form["address"]
        test_result = request.form["test_result"]
        vaccination_status = request.form["vaccination_status"]

        query = """
        UPDATE patients
        SET name=%s,
            age=%s,
            gender=%s,
            phone=%s,
            address=%s,
            test_result=%s,
            vaccination_status=%s
        WHERE id=%s
        """

        values = (
            name,
            age,
            gender,
            phone,
            address,
            test_result,
            vaccination_status,
            id
        )

        cursor.execute(query, values)
        connection.commit()

        cursor.close()
        connection.close()

        return redirect("/patients")

    cursor.execute(
        "SELECT * FROM patients WHERE id=%s",
        (id,)
    )

    patient = cursor.fetchone()

    cursor.close()
    connection.close()

    return render_template("edit_patient.html", patient=patient)

@app.route("/delete/<int:id>")
def delete_patient(id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM patients WHERE id=%s",
        (id,)
    )

    connection.commit()

    cursor.close()
    connection.close()

    return redirect("/patients")

@app.route("/search")
def search_patient():

    search = request.args.get("search", "")
    test_result = request.args.get("test_result", "")
    vaccination_status = request.args.get("vaccination_status", "")

    connection = get_connection()
    cursor = connection.cursor()

    query = """
    SELECT * FROM patients
    WHERE (name LIKE %s OR phone LIKE %s)
    """

    value = "%" + search + "%"

    values = [value, value]

    if test_result:
        query += " AND test_result = %s"
        values.append(test_result)

    if vaccination_status:
        query += " AND vaccination_status = %s"
        values.append(vaccination_status)

    cursor.execute(query, values)

    patients = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template("patients.html", patients=patients)

@app.route("/view/<int:id>")
def view_patient(id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM patients WHERE id=%s",
        (id,)
    )

    patient = cursor.fetchone()

    cursor.close()
    connection.close()

    return render_template(
        "view_patient.html",
        patient=patient
    )
    
@app.route("/dashboard")
def dashboard():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM patients")
    total = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM patients WHERE test_result='Positive'"
    )
    positive = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM patients WHERE test_result='Negative'"
    )
    negative = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM patients WHERE vaccination_status='Vaccinated'"
    )
    vaccinated = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM patients WHERE vaccination_status='Not Vaccinated'"
    )
    not_vaccinated = cursor.fetchone()[0]

    cursor.close()
    connection.close()

    return render_template(
        "dashboard.html",
        total=total,
        positive=positive,
        negative=negative,
        vaccinated=vaccinated,
        not_vaccinated=not_vaccinated
    )

if __name__ == "__main__":
    app.run(debug=True)
