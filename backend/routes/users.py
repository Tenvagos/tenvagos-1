from flask import jsonify, request, Blueprint
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

def create_users_router(engine):

    usersRouter = Blueprint('users', __name__)
    
    @usersRouter.route('/users', methods = ['GET'])
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
            entity = {}
            entity['id_user'] = row.id_user
            entity['email'] = row.email
            entity['password'] = row.password
            entity['name'] = row.name
            entity['admin'] = row.admin
            entity['created_at'] = row.created_at
            data.append(entity)

        return jsonify(data), 200


    @usersRouter.route('/users', methods = ['POST'])
    def create_user():
        conn = engine.connect()
        new_user = request.get_json()
        query = f"""INSERT INTO users (email, password, name, admin) VALUES { new_user["email"] ,new_user["password"],new_user["name"],new_user["admin"]};"""
        try:
            conn.execute(text(query))
            conn.commit()
            conn.close()
        except SQLAlchemyError as err:
            return jsonify({'message': 'Se ha producido un error' + str(err.__cause__)})
        
        return jsonify({'message': 'se ha agregado el usuario correctamente' }), 201



    @usersRouter.route('/users/<id>', methods = ['PATCH'])
    def update_user(id):
        conn = engine.connect()
        mod_user = request.get_json()

        if not mod_user:
            return ValueError("Ingrese los datos a actualizar")

        set_pairs = []

        for key, value in mod_user.items():
            set_pairs.append(f"{key} = '{value}'")

        set_clause = ", ".join(set_pairs)

        query = f"UPDATE users SET {set_clause} WHERE id_user = {id}"

        query_validation = f"SELECT * FROM users WHERE id_user = {id};"
        try:
            val_result = conn.execute(text(query_validation))
            if val_result.rowcount!=0:
                result = conn.execute(text(query))
                conn.commit()
                conn.close()
            else:
                conn.close()
                return jsonify({'message': "El usuario no existe"}), 404
        except SQLAlchemyError as err:
            return jsonify({'message': str(err.__cause__)})
        return jsonify({'message': 'se ha modificado correctamente el usuario '}), 200

    @usersRouter.route('/users/<id>', methods = ['GET'])
    def get_user(id):
        conn = engine.connect()
        query = f"""SELECT *
                FROM users
                WHERE id_user = {id};
                """
        try:
            result = conn.execute(text(query))
            conn.commit()
            conn.close()
        except SQLAlchemyError as err:
            return jsonify(str(err.__cause__))
        if result.rowcount !=0:
            data = {}
            row = result.first()
            data['id_user'] = row[0]
            data['name'] = row[1]
            data['password'] = row[2]
            data['email'] = row[3]
            data['admin'] = row[4]
            data['created_at'] = row[5]
            return jsonify(data), 200
        return jsonify({"message": "El usuario no existe"}), 404


    @usersRouter.route('/users/<id>', methods = ['DELETE'])
    def delete_user(id):
        conn = engine.connect()
        query = f"""DELETE FROM users
                WHERE id_user = {id};
                """
        validation_query = f"SELECT * FROM users WHERE id_user = {id}"
        try:
            val_result = conn.execute(text(validation_query))
            if val_result.rowcount != 0 :
                result = conn.execute(text(query))
                conn.commit()
                conn.close()
            else:
                conn.close()
                return jsonify({"message": "El usuario no existe"}), 404
        except SQLAlchemyError as err:
            jsonify(str(err.__cause__))
        return jsonify({'message': 'Se ha eliminado correctamente al usuario'}), 202

    return usersRouter