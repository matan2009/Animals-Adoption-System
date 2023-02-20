from functools import wraps
from flask import Flask, request, make_response

from common.database_helper import DatabaseHelper
from excpetions.connection_system_helper_excpetion import ConnectionSystemHelperException
from service.animals_system_helper import AnimalsSystemHelper
from service.connection_system_helper import ConnectionSystemHelper

app = Flask(__name__)


@app.route('/signup', methods=["POST"])
def signup():
    username = request.json.get("username")
    password = request.json.get("password")
    auth_password = request.json.get("auth_password")
    if not username and not password or password != auth_password:
        return make_response("Bad Request", 400)
    try:
        connection_system_helper.create_new_user_in_db(username, password)
    except Exception as ex:
        return make_response(str(ex), 400)

    return make_response("Signup successful", 201)


@app.route('/login', methods=["POST"])
def login():
    username = request.json.get("username")
    password = request.json.get("password")
    try:
        token = connection_system_helper.verify_user(username, password)
    except ConnectionSystemHelperException as ex:
        exception_args = ex.args[0]
        msg, status_code = exception_args[0], exception_args[1]
        return make_response(msg, status_code)

    return token


def verify_authorization(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return make_response("Authorization header is expected", 401)
        parts = auth_header.split()
        if parts[0].lower() != "bearer":
            return make_response("Authorization header must start with Bearer", 401)
        elif len(parts) == 1:
            return make_response("Token not found", 401)
        elif len(parts) > 2:
            return make_response("Authorization header must be Bearer token", 401)

        token = parts[1]
        try:
            connection_system_helper.verify_token(token)
        except ConnectionSystemHelperException as ex:
            exception_args = ex.args[0]
            msg, status_code = exception_args[0], exception_args[1]
            return make_response(msg, status_code)

        return func(*args, **kwargs)

    return decorated


@app.route('/animal_for_adoption', methods=["POST"])
@verify_authorization
def insert_animal_to_system():
    animal_details = request.json
    animals_system_helper.add_animal(animal_details)
    return make_response("Animal added successfully to the system", 200)


def main():
    connection_database_helper = connection_system_helper.database_helper
    connection_database_helper.verify_db()
    animals_database_helper = animals_system_helper.database_helper
    animals_database_helper.verify_db()

    app.run()


if __name__ == '__main__':
    connection_system_helper = ConnectionSystemHelper()
    animals_system_helper = AnimalsSystemHelper()
    main()

