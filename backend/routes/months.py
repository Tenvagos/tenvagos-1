from flask import jsonify, request, Blueprint
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError


def create_months_router(engine):

    monthsRouter = Blueprint('months', __name__)

    @monthsRouter.route('/months', methods = ['GET'])
    def months():
        conn = engine.connect()
        
        query = "SELECT * FROM months;"
        try:
            result = conn.execute(text(query))
            conn.close()
        except SQLAlchemyError as err:
            return jsonify(str(err.__cause__))
        

        data = []
        for row in result:
            entity = {}
            entity['id_month'] = row.id_month
            entity['month_name'] = row.month_name
            entity['id_promotion'] = row.id_promotion
            data.append(entity)

        return jsonify(data), 200


    @monthsRouter.route('/months', methods = ['POST'])
    def create_room():
        conn = engine.connect()
        new_user = request.get_json()
        query = f"""INSERT INTO months (month_name, id_promotion ) VALUES { new_user["month_name"] ,new_user["id_promotion"]};"""
        try:
            conn.execute(text(query))
            conn.commit()
            conn.close()
        except SQLAlchemyError as err:
            return jsonify({'message': 'Se ha producido un error' + str(err.__cause__)})
        
        return jsonify({'message': 'se ha agregado el mes correctamente' }), 201



    @monthsRouter.route('/months/<id>', methods = ['PATCH'])
    def update_room(id):
        conn = engine.connect()
        mod_user = request.get_json()

        if not mod_user:
            return ValueError("Ingrese los datos a actualizar")

        set_pairs = []

        for key, value in mod_user.items():
            set_pairs.append(f"{key} = '{value}'")

        set_clause = ", ".join(set_pairs)

        query = f"UPDATE months SET {set_clause} WHERE id_month = {id}"


        query_validation = f"SELECT * FROM months WHERE id_month = {id};"
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
        return jsonify({'message': 'se ha modificado correctamente la habitacion '}), 200

    @monthsRouter.route('/months/<id>', methods = ['GET'])
    def get_room(id):
        conn = engine.connect()
        query = f"""SELECT *
                FROM months
                WHERE id_month = {id};
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
            data['id_month'] = row[0]
            data['month_name'] = row[1]
            data['id_promotion'] = row[2]
            return jsonify(data), 200
        return jsonify({"message": f"El mes con id {id} no existe"}), 404


    @monthsRouter.route('/months/<id>', methods = ['DELETE'])
    def delete_room(id):
        conn = engine.connect()
        query = f"""DELETE FROM months
                WHERE id_month = {id};
                """
        validation_query = f"SELECT * FROM months WHERE id_month = {id}"
        try:
            val_result = conn.execute(text(validation_query))
            if val_result.rowcount != 0 :
                result = conn.execute(text(query))
                conn.commit()
                conn.close()
            else:
                conn.close()
                return jsonify({"message": f"la habitacion con el id {id} no existe"}), 404
        except SQLAlchemyError as err:
            jsonify(str(err.__cause__))
        return jsonify({'message': 'Se ha eliminado correctamente la habitacion'}), 202
    return monthsRouter