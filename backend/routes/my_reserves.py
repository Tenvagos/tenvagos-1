from flask import jsonify, request, Blueprint
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError


def create_my_reserves_router(engine):

    myReservesRouter = Blueprint('my_reserves', __name__)
    
    @myReservesRouter.route('/my_reserves/<int:id_user>', methods = ['GET'])
    def my_reserves(id_user):
        conn = engine.connect()
        
        sort_by = request.args.get('sort_by', default='id', type=str)
        sort_order = request.args.get('sort_order', default='asc', type=str)
        page = request.args.get('page', default=1, type=int)
        page_size = request.args.get('page_size', default=10, type=int)

        if sort_by not in ['id', 'id_user', 'id_reserve'] or sort_order not in ['asc', 'desc']:
            return jsonify({'error': 'Invalid sort column or direction'}), 400

        if page < 1 or page_size < 1:
            return jsonify({'error': 'Invalid page number or page size'}), 400

        offset = (page - 1) * page_size

        query = f"SELECT * FROM user_reserves WHERE id_user = {id_user} ORDER BY {sort_by} {sort_order} LIMIT {page_size} OFFSET {offset};"
        try:
            result = conn.execute(text(query))
            conn.close()
        except SQLAlchemyError as err:
            return jsonify(str(err.__cause__))
        
        data = []
        for row in result:
            entity = {}
            entity['id'] = row.id
            entity['id_user'] = row.id_user
            entity['id_reserve'] = row.id_reserve
            data.append(entity)

        return jsonify(data), 200

    @myReservesRouter.route('/my_reserves/<int:id_user>/<int:id_reserve>', methods = ['GET'])
    def my_reserve_detail(id_user, id_reserve):
        conn = engine.connect()

        query = f"SELECT * FROM user_reserves WHERE id_user = {id_user} AND id_reserve = {id_reserve};"
        try:
            result = conn.execute(text(query))
            conn.close()
        except SQLAlchemyError as err:
            return jsonify(str(err.__cause__))

        row = result.fetchone()
        if row is None:
            return jsonify({'error': 'Reservation not found'}), 404

        entity = {}
        entity['id'] = row.id
        entity['id_user'] = row.id_user
        entity['id_reserve'] = row.id_reserve
        # Campos adicionales de la reserva

        return jsonify(entity), 200
    
    return myReservesRouter