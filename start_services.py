"""
Start all 3 services from this module
- Authentication
- Database backend service
- Client service

Each service run on seprate process
multiprocessing concept used here
"""


from Client import client_app
from Database import db_app
from Authentication import auth_app
import json
import multiprocessing


# read configuration file
CONFIG_FILE_PATH = "C:/Users/NIrali/Documents/GitHub/distributed-micro-service" + \
                   "/distributed system/config.json"
with open(CONFIG_FILE_PATH, "r") as conf_file:
    conf_data = json.load(conf_file)

# configuration file contains port number for each services.
API_PORTS = conf_data["API_PORTS"]


if __name__ == "__main__":
    # start authentication service
    auth_process = multiprocessing.Process(
        target=auth_app.start_service,
        args=(API_PORTS["authentication"],)
    )
    auth_process.start()

    # start Database service
    db_process = multiprocessing.Process(
        target=db_app.start_service,
        args=(API_PORTS["database"],)
    )
    db_process.start()

    # start Client service
    client_process = multiprocessing.Process(
        target=client_app.start_service,
        args=(API_PORTS["client"],)
    )
    client_process.start()

    # join all process with main process.
    auth_process.join()
    db_process.join()
    client_process.join()
