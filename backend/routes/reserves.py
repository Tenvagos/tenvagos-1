from flask import jsonify, request, Blueprint
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

def create_reserves_router(engine):

    reservesRouter = Blueprint('reserves', __name__)

    @reservesRouter.route('/reserves',methods =['GET'])
    def reserves():
        conn = engine.connect()
        
        query = f"""SELECT reserves.*, u.email, u.user_name, r.room_name,r.capacity, r.price, r.stars, r.description 
        FROM reserves
        INNER JOIN rooms r ON reserves.id_room = r.id_room
        INNER JOIN users u ON reserves.id_user = u.id_user
        """ 
        try:
            result = conn.execute(text(query))
            conn.close()
        except SQLAlchemyError as err:
            return jsonify(str(err.__cause__))
        
        
        data = []
        for row in result:
            entity = {}
            entity['id_reserve'] = row.id_reserve
            entity['start_date']=row.start_date
            entity['end_date'] = row.end_date
            entity['created_at'] = row.created_at
            entity['modified_at'] = row.modified_at
            entity['amount'] = row.amount
            
            entity['id_user'] = row.id_user
            entity['email'] = row.email
            entity['user_name'] = row.user_name
           
            entity['id_room'] = row.id_room
            entity['room_name'] = row.room_name
            entity['capacity'] = row.capacity
            entity['room_price'] = row.price
            entity['stars'] = row.stars
            entity['description'] = row.description
            
            data.append(entity)

        return jsonify(data), 200

    @reservesRouter.route('/reserves', methods = ['POST'])
    def create_reserve():
        conn = engine.connect()
        new_reserve = request.get_json()
   
        id_room=new_reserve["id_room"]
        id_user=new_reserve["id_user"] 
        start_date=new_reserve["start_date"]
        end_date=new_reserve["end_date"]
        amount=new_reserve["amount"]
        
        query_check_availability = f"""
        SELECT COUNT(*) FROM reserves 
        WHERE id_room = {id_room} AND (
            (start_date <= '{start_date}' AND end_date >= '{start_date}') OR 
            (start_date <= '{end_date}' AND end_date >= '{end_date}') OR 
            (start_date >= '{start_date}' AND end_date <= '{end_date}')
        )
        """

        try:
            availability_result = conn.execute(
                text(query_check_availability)
            ).fetchone()
            
            if availability_result[0] != 0:
                conn.close()
                return jsonify({'message': 'La habitación no está disponible en las fechas seleccionadas'}), 400
            
            query_insert_reserve = f"""
            INSERT INTO reserves (id_user, id_room, start_date, end_date, amount) 
            VALUES ({id_user}, {id_room}, '{start_date}', '{end_date}', '{amount}')
            """
            
            result = conn.execute(
                text(query_insert_reserve)
            )
            conn.commit()
            conn.close()
            
        except SQLAlchemyError as err:
            conn.close()
            return jsonify({'message': 'Se ha producido un error: ' + str(err.__cause__)}), 500
        
        return jsonify({'message': 'Se ha creado la reserva correctamente'}), 201

    @reservesRouter.route('/reserves/<id_reserve>', methods = ['PATCH'])
    def update_reserve(id_reserve):
        conn = engine.connect()
        mod_user = request.get_json()

        if not mod_user:
            return ValueError("Ingrese los datos a actualizar")

        set_pairs = []

        for key, value in mod_user.items():
            set_pairs.append(f"{key} = '{value}'")

        set_clause = ", ".join(set_pairs)

        query = f"UPDATE reserves SET {set_clause} WHERE id_reserve = {id_reserve}"

        query_validation = f"SELECT * FROM reserves WHERE id_reserve = {id_reserve};"
        try:
            val_result = conn.execute(text(query_validation))
            if val_result.rowcount!=0:
                result = conn.execute(text(query))
                conn.commit()
                conn.close()
            else:
                conn.close()
                return jsonify({'message': "El numero de reserva no existe"}), 404
        except SQLAlchemyError as err:
            return jsonify({'message': str(err.__cause__)})
        return jsonify({'message': 'Se ha modificado la reserva correctamente'}), 200

    @reservesRouter.route('/reserves/<id_reserve>', methods = ['GET'])
    def get_reserve(id_reserve):
        conn = engine.connect()
        query = f"""SELECT reserves.*, u.email, u.user_name, r.room_name,r.capacity, r.price, r.stars, r.description 
        FROM reserves
        INNER JOIN rooms r ON reserves.id_room = r.id_room
        INNER JOIN users u ON reserves.id_user = u.id_user
        WHERE id_reserve = {id_reserve}; """
        
        try:
            result = conn.execute(text(query))
            conn.close()
        except SQLAlchemyError as err:
            return jsonify(str(err.__cause__))
        
        row = result.fetchone()
        if row is None:
            return jsonify({'error': 'Reserva no encontrada'}), 404
       
        
        data = {}
        data['id_reserve'] = row.id_reserve 
        data['start_date'] = row.start_date
        data['end_date'] = row.end_date
        data['created_at'] = row.created_at
        data['modified_at'] = row.modified_at
        data['amount'] = row.amount
        
        data['id_user'] = row.id_user
        data['email'] = row.email
        data['user_name'] = row.user_name
                    
        data['id_room'] = row.id_room
        data['room_name'] = row.room_name
        data['capacity'] = row.capacity
        data['room_price'] = row.price
        data['stars'] = row.stars
        data['description'] = row.description
            
        return jsonify(data), 200


    @reservesRouter.route('/reserves/<id_reserve>', methods = ['DELETE'])
    def delete_reserve(id_reserve):
        conn = engine.connect()
        query = f"""DELETE FROM reserves
                WHERE id_reserve = {id_reserve};
                """
        validation_query = f"SELECT * FROM reserves WHERE id_reserve = {id_reserve}"
        try:
            val_result = conn.execute(text(validation_query))
            if val_result.rowcount != 0 :
                result = conn.execute(text(query))
                conn.commit()
                conn.close()
            else:
                conn.close()
                return jsonify({"message": "La reserva no existe."}), 404
        except SQLAlchemyError as err:
            jsonify(str(err.__cause__))
        return jsonify({'message': 'Se ha eliminado correctamente'}), 202

    return reservesRouter
