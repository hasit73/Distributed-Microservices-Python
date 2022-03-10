"""
Authentication service manage user authorization and verification.

Users can register themselves using this service.
User must be authenticated first then only user can
use other services. 
"""

from flask import Flask, request
import sqlite3
import Authentication.db_queries as auth_query
import os


current_dir_path = os.path.dirname(__file__)
db_path = os.path.join(current_dir_path, "auth-db.sqlite3")
auth_connection = sqlite3.connect(db_path, check_same_thread=False)
auth_cursor = auth_connection.cursor()
auth_cursor.execute(auth_query.CREATE_AUTH_TABLE)
auth_connection.commit()


app = Flask(__name__)


@app.route("/register", methods=["POST"])
def register():
    if request.method == "POST":
        user_args = request.args
        username = user_args["username"]
        password = user_args["password"]
        user_mail_id = user_args["email"]
        register_cursor = auth_connection.cursor()
        register_cursor.execute(auth_query.REGISTER_USER,
                                (username, password, user_mail_id))
        auth_connection.commit()
        return "success"

    return "INVALID METHOD"


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user_args = request.args
        username = user_args["username"]
        password = user_args["password"]
        login_cursor = auth_connection.cursor()
        login_cursor.execute(auth_query.LOGIN_AUTH_USER, (username, password))
        login_results = login_cursor.fetchall()

        if len(login_results) > 0:
            return "success"
        else:
            return "fail"

    return "INVALID METHOD"


def start_service(host, port):
    print("Authentication service started")
    app.run(host=host, port=port)


if __name__ == "__main__":
    app.run(debug=True, port=72)
