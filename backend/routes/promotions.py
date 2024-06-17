from flask import jsonify, request, Blueprint
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError


def create_promotions_router(engine):

    promotionsRouter = Blueprint('promotions', __name__)

    @promotionsRouter.route('/promotions', methods = ['GET'])
    def promotions():
        conn = engine.connect()
        
        query = "SELECT * FROM promotions;"
        try:
            result = conn.execute(text(query))
            conn.close()
        except SQLAlchemyError as err:
            return jsonify(str(err.__cause__))
        

        data = []
        for row in result:
            entity = {}
            entity['id_promotion'] = row.id_promotion
            entity['title'] = row.title
            entity['description'] = row.description
            entity['first_date'] = row.first_date
            entity['last_date'] = row.last_date
            entity['discount'] = row.discount
            data.append(entity)

        return jsonify(data), 200


    @promotionsRouter.route('/promotions', methods = ['POST'])
    def create_room():
        conn = engine.connect()
        new_user = request.get_json()
        query = f"""INSERT INTO promotions (title, description, first_date, last_date ) VALUES { new_user["title"] ,new_user["description"], new_user["first_date"], new_user["last_date"]};"""
        try:
            conn.execute(text(query))
            conn.commit()
            conn.close()
        except SQLAlchemyError as err:
            return jsonify({'message': 'Se ha producido un error' + str(err.__cause__)})
        
        return jsonify({'message': 'se ha agregado el mes correctamente' }), 201



    @promotionsRouter.route('/promotions/<id>', methods = ['PATCH'])
    def update_room(id):
        conn = engine.connect()
        mod_user = request.get_json()

        if not mod_user:
            return ValueError("Ingrese los datos a actualizar")

        set_pairs = []

        for key, value in mod_user.items():
            set_pairs.append(f"{key} = '{value}'")

        set_clause = ", ".join(set_pairs)

        query = f"UPDATE promotions SET {set_clause} WHERE id_promotion = {id}"


        query_validation = f"SELECT * FROM promotions WHERE id_promotion = {id};"
        try:
            val_result = conn.execute(text(query_validation))
            if val_result.rowcount!=0:
                result = conn.execute(text(query))

                conn.commit()
                conn.close()
            else:
                conn.close()
                return jsonify({'message': "La habitacion no existe"}), 404
        except SQLAlchemyError as err:
            return jsonify({'message': str(err.__cause__)})
        return jsonify({'message': 'Promocion actualizada '}), 200

    @promotionsRouter.route('/promotions/<id>', methods = ['GET'])
    def get_room(id):
        conn = engine.connect()
        query = f"""SELECT *
                FROM promotions
                WHERE id_promotion = {id};
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
            data['id_promotion'] = row[0]
            data['title'] = row[1]
            data['description'] = row[2]
            data['first_date'] = row[3]
            data['last_date'] = row[4]
            return jsonify(data), 200
        return jsonify({"message": f"La promocion con id {id} no existe"}), 404


    @promotionsRouter.route('/promotions/<id>', methods = ['DELETE'])
    def delete_room(id):
        conn = engine.connect()
        query = f"""DELETE FROM promotions
                WHERE id_promotion = {id};
                """
        validation_query = f"SELECT * FROM promotions WHERE id_promotion = {id}"
        try:
            val_result = conn.execute(text(validation_query))
            if val_result.rowcount != 0 :
                result = conn.execute(text(query))
                conn.commit()
                conn.close()
            else:
                conn.close()
                return jsonify({"message": f"la promocion con el id {id} no existe"}), 404
        except SQLAlchemyError as err:
            jsonify(str(err.__cause__))
        return jsonify({'message': 'Se ha eliminado correctamente la promocion'}), 202
    return promotionsRouter