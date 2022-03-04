"""
Client service manage user side interaction

User can't directly interacte with authentication and database system
so client service works as medium between these server services and
users.

"""


from flask import Flask, render_template, request, redirect, session
import requests
import hashlib
import json

app = Flask(__name__)
CONFIG_FILE_PATH = "C:/Users/NIrali/Documents/GitHub/distributed-micro-service" + \
                   "/distributed system/config.json"

with open(CONFIG_FILE_PATH, "r") as conf_file:
    conf_data = json.load(conf_file)

BASE_URL = "http://localhost:{}/"
DATABASE_API_URL = BASE_URL.format(conf_data["API_PORTS"]["database"])
AUTHENTICATION_API_URL = BASE_URL.format(
    conf_data["API_PORTS"]["authentication"]
)


@app.route("/")
def home():
    context = {}
    if "username" in session:
        response = requests.get(DATABASE_API_URL+"employee/get")
        employee_records = response.json()["data"]
        context["username"] = session["username"]
        context["employee_data"] = employee_records
        return render_template("home.html", context=context)
    else:
        return redirect("/login")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        hashed_password = hashlib.md5(password.encode("utf-8")).hexdigest()
        params = {"username": username, "password": hashed_password}
        response = requests.post(AUTHENTICATION_API_URL+"login", params=params)
        if response.text == "success":
            session["username"] = username
            return redirect("/")

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password")

        hashed_password = hashlib.md5(password.encode("utf-8")).hexdigest()
        params = {
            "username": username,
            "password": hashed_password,
            "email": email
        }
        response = requests.post(AUTHENTICATION_API_URL+"register",
                                 params=params)
        if response.text == "success":
            return redirect("/login")

    return render_template("register.html")


@app.route("/employee/add", methods=["POST"])
def add_employee():

    emp_name = request.form.get("ename")
    emp_number = request.form.get("enumber")
    emp_role = request.form.get("erole")

    params = {
        "employee_name": emp_name,
        "employee_number": emp_number,
        "employee_role": emp_role
    }
    requests.post(DATABASE_API_URL+"employee/add", params=params)
    return redirect("/")


@app.route("/employee/delete/<int:emp_id>")
def delete_employee(emp_id):
    params = {"employee_id": emp_id}
    requests.post(DATABASE_API_URL+"/employee/delete",
                  params=params)
    return redirect("/")


def start_service(port):
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    print("Client service started")
    app.run(port=port)


if __name__ == "__main__":

    app.run(debug=True, port=78)
