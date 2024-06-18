from flask import jsonify, request, Blueprint
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
import bcrypt

def create_users_router(engine):

    usersRouter = Blueprint('users', __name__)

    @usersRouter.route('/users', methods=['GET'])
    def users():
        conn = engine.connect()
        
        query = "SELECT * FROM users;"
        try:
            result = conn.execute(text(query))
            conn.close()
        except SQLAlchemyError as err:
            return jsonify(str(err.__cause__))

        data = []
        for row in result:
            entity = {
                'id_user': row.id_user,
                'email': row.email,
                'password': row.password,
                'user_name': row.user_name,
                'admin': row.admin,
                'created_at': row.created_at,
                'url_imagen': row.url_imagen
            }
            data.append(entity)

        return jsonify(data), 200

    @usersRouter.route('/users', methods=['POST'])
    def create_user():
        conn = engine.connect()
        new_user = request.get_json()

        # Hashear la contraseña antes de guardarla
        hashed_password = bcrypt.hashpw(new_user["password"].encode('utf-8'), bcrypt.gensalt())

        query = text("""
            INSERT INTO users (email, password, user_name, admin, url_imagen)
            VALUES (:email, :password, :user_name, :admin, :url_imagen)
        """)
        try:
            conn.execute(query, {
                'email': new_user["email"],
                'password': hashed_password.decode('utf-8'),
                'user_name': new_user["user_name"],
                'admin': new_user["admin"],
                'url_imagen': new_user.get("url_imagen", "")
            })
            conn.commit()
            conn.close()
        except SQLAlchemyError as err:
            return jsonify({'message': 'Se ha producido un error: ' + str(err.__cause__)}), 500

        return jsonify({'message': 'Se ha agregado el usuario correctamente'}), 201

    @usersRouter.route('/users/<id>', methods=['PATCH'])
    def update_user(id):
        conn = engine.connect()
        mod_user = request.get_json()

        if not mod_user:
            return jsonify({"message": "Ingrese los datos a actualizar"}), 400

        set_pairs = []
        for key, value in mod_user.items():
            if key == "password":
                value = bcrypt.hashpw(value.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            set_pairs.append(f"{key} = :{key}")

        set_clause = ", ".join(set_pairs)

        query = text(f"UPDATE users SET {set_clause} WHERE id_user = :id")
        query_validation = text("SELECT * FROM users WHERE id_user = :id")

        try:
            val_result = conn.execute(query_validation, {'id': id})
            if val_result.rowcount != 0:
                conn.execute(query, {'id': id, **mod_user})
                conn.commit()
                conn.close()
            else:
                conn.close()
                return jsonify({'message': "El usuario no existe"}), 404
        except SQLAlchemyError as err:
            return jsonify({'message': str(err.__cause__)}), 500

        return jsonify({'message': 'Se ha modificado correctamente el usuario'}), 200

    @usersRouter.route('/users/<id>', methods=['GET'])
    def get_user(id):
        conn = engine.connect()
        query = text("SELECT * FROM users WHERE id_user = :id")
        try:
            result = conn.execute(query, {'id': id})
            conn.close()
        except SQLAlchemyError as err:
            return jsonify(str(err.__cause__)), 500

        row = result.fetchone()
        if row:
            data = {
                'id_user': row.id_user,
                'user_name': row.user_name,
                'password': row.password,
                'email': row.email,
                'admin': row.admin,
                'created_at': row.created_at,
                'url_imagen': row.url_imagen
            }
            return jsonify(data), 200
        else:
            return jsonify({"message": "El usuario no existe"}), 404

    @usersRouter.route('/users/<id>', methods=['DELETE'])
    def delete_user(id):
        conn = engine.connect()
        query = text("DELETE FROM users WHERE id_user = :id")
        validation_query = text("SELECT * FROM users WHERE id_user = :id")

        try:
            val_result = conn.execute(validation_query, {'id': id})
            if val_result.rowcount != 0:
                conn.execute(query, {'id': id})
                conn.commit()
                conn.close()
            else:
                conn.close()
                return jsonify({"message": "El usuario no existe"}), 404
        except SQLAlchemyError as err:
            return jsonify(str(err.__cause__)), 500

        return jsonify({'message': 'Se ha eliminado correctamente al usuario'}), 202

    return usersRouter
