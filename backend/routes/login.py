from flask import jsonify, request, Blueprint, json
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
import bcrypt


def create_login_router(engine):
    loginRouter = Blueprint('login', __name__)

    @loginRouter.route('/login', methods=['POST'])
    def login():
        username = request.json['username']
        password = request.json['password']
        
        conn = engine.connect()
        try:
            query = text(f"SELECT * FROM users WHERE user_name = '{username}'")
            result = conn.execute(query)
            user = result.fetchone()
            print(user)
            print(result)
        except SQLAlchemyError as err:
            conn.close()
            return jsonify({"message": "Error de servidor: " + str(err.__cause__)}), 500
        finally:
            conn.close()

        if user is None:
            return jsonify({"message": "El nombre de usuario o contraseña es incorrecto"}), 401

        hashed_password = user.password.encode('utf-8')
        if not bcrypt.checkpw(password.encode('utf-8'), hashed_password):
            return jsonify({"message": "El nombre de usuario o contraseña es incorrecto"}), 401
               
        data = {}
        row = user
        data['id_user'] = row[0]
        data['user_name'] = row[1]
        data['password'] = row[2]
        data['email'] = row[3]
        data['admin'] = row[4]
        data['created_at'] = row[5]
        data['url_imagen'] = row[6]

        # Si el usuario existe, le devuelve los datos de ese usuario, el front maneja el login de esta manera
        return jsonify(data), 200

    return loginRouter
