"""
Database service manage data operations.

Insert, Get and Delete employee data
"""

from flask import Flask, request
import sqlite3
import Database.db_queries as db_query
import os

current_dir_path = os.path.dirname(__file__)
db_path = os.path.join(current_dir_path, "employee-db.sqlite3")

emp_connection = sqlite3.connect(db_path,
                                 check_same_thread=False)
emp_cursor = emp_connection.cursor()
emp_cursor.execute(db_query.CREATE_EMPLOYEE_TABLE)
emp_connection.commit()


app = Flask(__name__)


@app.route("/employee/add", methods=["GET", "POST"])
def add_employee():
    if request.method == "POST":
        user_args = request.args
        employee_name = user_args["employee_name"]
        employee_number = user_args["employee_number"]
        employee_role = user_args["employee_role"]
        emp_cursor = emp_connection.cursor()
        emp_cursor.execute(db_query.INSERT_EMPLOYEE,
                           (employee_name, employee_number,
                            employee_role))
        emp_connection.commit()
        return "success"
    return "INVALID METHOD"


@app.route("/employee/delete", methods=["GET", "POST"])
def remove_employee():
    if request.method == "POST":
        user_args = request.args
        employee_id = user_args["employee_id"]
        emp_cursor = emp_connection.cursor()
        emp_cursor.execute(db_query.DELETE_EMPLOYEE,
                           (employee_id,))
        emp_connection.commit()
        return "success"

    return "INVALID METHOD"


@app.route("/employee/get")
def get_employees():
    emp_cursor = emp_connection.cursor()
    emp_cursor.execute(db_query.GET_EMPLOYEES)
    emp_records = emp_cursor.fetchall()

    if len(emp_records) > 0:
        return {"data": emp_records}
    else:
        return {"data": []}


def start_service(host, port):
    print("Database service started")
    app.run(host=host, port=port)


if __name__ == "__main__":
    app.run(debug=True, port=84)
