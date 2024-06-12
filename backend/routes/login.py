from flask import jsonify, request, Blueprint
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError


def create_login_router(engine):
    loginRouter = Blueprint('login', __name__)

    @loginRouter.route('/login', methods = ['POST'])
    def login():
        username = request.json['username']
        password = request.json['password']

        if not username or not password:
            return jsonify({"message": "El nombre de usuario o contraseña son necesarios"}), 401

        conn = engine.connect()
        try:
            query = text("SELECT * FROM users WHERE name = :username AND password = :password")
            query = text("SELECT * FROM users WHERE user_name = :username AND password = :password")
            result = conn.execute(query, {'username': username, 'password': password})
            user = result.fetchone()
        except SQLAlchemyError as err:
            conn.close()
            return jsonify({"message": "Error de servidor: " + str(err.__cause__)}), 500
        finally:
            conn.close()

        if user is None:
            return jsonify({"message": "El nombre de usuario o contraseña es incorrecto"}), 401

        return jsonify({"message": "Inicio de sesión exitoso"}), 200

    return loginRouter
