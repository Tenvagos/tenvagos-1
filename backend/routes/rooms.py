from flask import jsonify, request, Blueprint
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError


def create_rooms_router(engine):

    roomsRouter = Blueprint('rooms', __name__)

    @roomsRouter.route('/rooms', methods = ['GET'])
    def rooms():
        conn = engine.connect()
        
        query = "SELECT * FROM rooms;"
        try:
            result = conn.execute(text(query))
            conn.close()
        except SQLAlchemyError as err:
            return jsonify(str(err.__cause__))
        

        data = []
        for row in result:
            entity = {}
            entity['id_room'] = row.id_room
            entity['name'] = row.name
            entity['capacity'] = row.capacity
            entity['price'] = row.price
            entity['stars'] = row.stars
            entity['description'] = row.description
            data.append(entity)

        return jsonify(data), 200


    @roomsRouter.route('/rooms', methods = ['POST'])
    def create_room():
        conn = engine.connect()
        new_user = request.get_json()
        query = f"""INSERT INTO rooms (name, capacity, price, stars, description ) VALUES { new_user["name"] ,new_user["capacity"],new_user["price"],new_user["stars"], new_user["description"]};"""
        try:
            conn.execute(text(query))
            conn.commit()
            conn.close()
        except SQLAlchemyError as err:
            return jsonify({'message': 'Se ha producido un error' + str(err.__cause__)})
        
        return jsonify({'message': 'se ha agregado la habitacion correctamente' }), 201



    @roomsRouter.route('/rooms/<id>', methods = ['PATCH'])
    def update_room(id):
        conn = engine.connect()
        mod_user = request.get_json()

        if not mod_user:
            return ValueError("Ingrese los datos a actualizar")

        set_pairs = []

        for key, value in mod_user.items():
            set_pairs.append(f"{key} = '{value}'")

        set_clause = ", ".join(set_pairs)

        query = f"UPDATE rooms SET {set_clause} WHERE id_room = {id}"


        query_validation = f"SELECT * FROM rooms WHERE id_room = {id};"
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

    @roomsRouter.route('/rooms/<id>', methods = ['GET'])
    def get_room(id):
        conn = engine.connect()
        query = f"""SELECT *
                FROM rooms
                WHERE id_room = {id};
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
            data['id_room'] = row[0]
            data['name'] = row[1]
            data['capacity'] = row[2]
            data['price'] = row[3]
            data['stars'] = row[4]
            data['description'] = row[5]
            return jsonify(data), 200
        return jsonify({"message": f"La habitacion con id {id} no existe"}), 404


    @roomsRouter.route('/rooms/<id>', methods = ['DELETE'])
    def delete_room(id):
        conn = engine.connect()
        query = f"""DELETE FROM rooms
                WHERE id_room = {id};
                """
        validation_query = f"SELECT * FROM rooms WHERE id_room = {id}"
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
    
    
    @roomsRouter.route('/rooms/stars/<stars>', methods = ['GET'])
    def room_available(stars):
        conn = engine.connect()
        
        start_date= request.args.get('start_date',type=str)
        end_date= request.args.get('end_date',type=str)
        stars_param= request.args.get('stars',default=0,type=int)
        
        if stars_param is not 0:
            stars = stars_param
        
        query = f"""SELECT * FROM rooms WHERE stars = {stars} AND id_room NOT IN (
            SELECT id_room FROM reserves
            WHERE (
            (start_date <= '{start_date}' AND end_date >= '{start_date}') OR 
            (start_date <= '{end_date}' AND end_date >= '{end_date}') OR 
            (start_date >= '{start_date}' AND end_date <= '{end_date}')
            ) 
        ) """
        try:
            result = conn.execute(text(query))
            conn.close()
        except SQLAlchemyError as err:
            return jsonify(str(err.__cause__))
        
        data = []
        for row in result:
            entity = {}
            entity['id_room'] = row.id_room
            entity['name'] = row.name
            entity['capacity'] = row.capacity
            entity['price'] = row.price
            entity['stars'] = row.stars
            entity['description'] = row.description
            data.append(entity)

        return jsonify(data), 200
                    
    return roomsRouter



        
        
        