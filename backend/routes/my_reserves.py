from flask import jsonify, request, Blueprint
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError


def create_my_reserves_router(engine):

    myReservesRouter = Blueprint('my_reserves', __name__)
    
    @myReservesRouter.route('/my_reserves/<int:id_user>', methods = ['GET'])
    def my_reserves(id_user):
        conn = engine.connect()
        
        sort_by = request.args.get('sort_by', default='id_reserve', type=str)
        sort_order = request.args.get('sort_order', default='asc', type=str)
        page = request.args.get('page', default=1, type=int)
        page_size = request.args.get('page_size', default=10, type=int)

        if sort_by not in ['id_reserve', 'id_user', 'start_date', 'end_date', 'stars'] or sort_order not in ['asc', 'desc']:
            return jsonify({'error': 'Patron de ordenamiento o direccion invalidos.'}), 400

        if page < 1 or page_size < 1:
            return jsonify({'error': 'Numero de pagina o tamanho de pagina invalidos.'}), 400

        offset = (page - 1) * page_size

        query = f"""SELECT reserves.*, rooms.stars, rooms.room_name, rooms.price, rooms.url_imagen, rooms.description, rooms.stars FROM reserves 
                    INNER JOIN rooms ON reserves.id_room = rooms.id_room 
                    WHERE id_user = {id_user} 
                    ORDER BY {sort_by} {sort_order} 
                    LIMIT {page_size} OFFSET {offset};"""
        try:
            result = conn.execute(text(query))
            conn.close()
        except SQLAlchemyError as err:
            return jsonify(str(err.__cause__))
        
        data = []
        for row in result:
            entity = {}
            entity['id_reserve'] = row.id_reserve
            entity['id_user'] = row.id_user
            entity['start_date'] = row.start_date
            entity['end_date'] = row.end_date
            entity['id_room'] = row.id_room
            entity['room_name'] = row.room_name
            entity['price'] = row.price
            entity['amount'] = row.amount
            entity['stars'] = row.stars
            entity['description'] = row.description
            entity['url_imagen'] = row.url_imagen
            data.append(entity)

        return jsonify(data), 200

    @myReservesRouter.route('/my_reserves/<int:id_user>/<int:id_reserve>', methods = ['GET'])
    def my_reserve_detail(id_user, id_reserve):
        conn = engine.connect()

        query = f"""SELECT reserves.*, rooms.stars, rooms.room_name, rooms.description, rooms.price, rooms.url_imagen FROM reserves 
                    INNER JOIN rooms ON reserves.id_room = rooms.id_room 
                    WHERE id_user = {id_user} AND id_reserve = {id_reserve};"""
        try:
            result = conn.execute(text(query))
            conn.close()
        except SQLAlchemyError as err:
            return jsonify(str(err.__cause__))

        row = result.fetchone()
        if row is None:
            return jsonify({'error': 'Reserva no encontrada.'}), 404

        entity = {}
        entity['id_reserve'] = row.id_reserve
        entity['id_user'] = row.id_user
        entity['start_date'] = row.start_date
        entity['end_date'] = row.end_date
        entity['stars'] = row.stars
        entity['room_name'] = row.room_name
        entity['amount'] = row.amount
        entity['description'] = row.description
        entity['url_imagen'] = row.url_imagen
        entity['price'] = row.price


        return jsonify(entity), 200
    
    @myReservesRouter.route('/my_reserves/<int:id_user>/<int:id_reserve>', methods = ['PUT'])
    def update_reserve(id_user, id_reserve):
        conn = engine.connect()

        data = request.get_json()

        validation_query = f"""SELECT * FROM reserves WHERE id_user = :id_user AND id_reserve = :id_reserve;"""
        result = conn.execute(text(validation_query), {"id_user": id_user, "id_reserve": id_reserve}).fetchone()
        if not result:
            conn.close()
            return jsonify({'message': 'Reserva no encontrada.'}), 404

        query = f"""UPDATE reserves SET start_date = :start_date, end_date = :end_date 
                    WHERE id_user = :id_user AND id_reserve = :id_reserve;"""
        try:
            conn.execute(text(query), {"start_date": data['start_date'], "end_date": data['end_date'], "id_user": id_user, "id_reserve": id_reserve})
            conn.commit()
            conn.close()
        except SQLAlchemyError as err:
            return jsonify(str(err.__cause__))

        return jsonify({'message': 'Reserva actualizada exitosamente.'}), 200


    @myReservesRouter.route('/my_reserves/<int:id_user>/<int:id_reserve>', methods = ['DELETE'])
    def delete_reserve(id_user, id_reserve):
        conn = engine.connect()

        validation_query = f"""SELECT * FROM reserves WHERE id_user = :id_user AND id_reserve = :id_reserve;"""
        result = conn.execute(text(validation_query), {"id_user": id_user, "id_reserve": id_reserve}).fetchone()
        if not result:
            conn.close()
            return jsonify({'message': 'Reserva no encontrada.'}), 404

        query = f"""DELETE FROM reserves WHERE id_user = :id_user AND id_reserve = :id_reserve;"""
        try:
            conn.execute(text(query), {"id_user": id_user, "id_reserve": id_reserve})
            conn.commit()
            conn.close()
        except SQLAlchemyError as err:
            return jsonify(str(err.__cause__))

        return jsonify({'message': 'Reserva eliminada exitosamente.'}), 200

    return myReservesRouter