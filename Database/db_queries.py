CREATE_EMPLOYEE_TABLE = """

CREATE TABLE IF NOT EXISTS EMPLOYEE(
    employee_id integer primary key autoincrement,
    employee_name varchar2(255),
    employee_phonenumber varchar2(500) unique,
    employee_role varchar2(400)
);
"""

GET_EMPLOYEES = """
SELECT * from EMPLOYEE;
"""

INSERT_EMPLOYEE = """
INSERT INTO EMPLOYEE(employee_name, employee_phonenumber,
employee_role) VALUES (?,?,?);
"""

DELETE_EMPLOYEE = """
DELETE FROM EMPLOYEE
WHERE employee_id = ?;
"""
