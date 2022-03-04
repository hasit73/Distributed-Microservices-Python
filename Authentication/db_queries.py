CREATE_AUTH_TABLE = """

CREATE TABLE IF NOT EXISTS USERLOGIN(
    username varchar2(255) primary key,
    password varchar2(500),
    email varchar2(400) unique
);
"""

LOGIN_AUTH_USER = """
SELECT username from USERLOGIN
WHERE username = ? AND password = ?;
"""

REGISTER_USER = """
INSERT INTO USERLOGIN VALUES (?,?,?);
"""

