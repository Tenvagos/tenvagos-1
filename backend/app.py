from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
import os
from dotenv import load_dotenv

load_dotenv()

user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
host = os.getenv('DB_HOST')
db =  os.getenv('DB_NAME')


app = Flask(__name__)
engine = create_engine(f'mysql+mysqlconnector://{user}@{host}/{db}')


@app.route('/rooms', methods = ['GET'])
def users():
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
        entity['id'] = row.id
        entity['name'] = row.name
        entity['capacity'] = row.capacity
        entity['price'] = row.price
        entity['stars'] = row.stars
        data.append(entity)

    return jsonify(data), 200


@app.route('/create_room', methods = ['POST'])
def create_user():
    conn = engine.connect()
    new_user = request.get_json()
    query = f"""INSERT INTO rooms (id, name, capacity, price, stars) VALUES {new_user["id"], new_user["name"] ,new_user["capacity"],new_user["price"],new_user["stars"]};"""
    try:
        conn.execute(text(query))
        conn.commit()
        conn.close()
    except SQLAlchemyError as err:
        return jsonify({'message': 'Se ha producido un error' + str(err.__cause__)})
    
    return jsonify({'message': 'se ha agregado la habitacion correctamente' }), 201



@app.route('/room/<id>', methods = ['PATCH'])
def update_user(id):
    conn = engine.connect()
    mod_user = request.get_json()
    query = f"""UPDATE rooms SET name = '{mod_user['name']}'
                WHERE id = {id};
            """
    query_validation = f"SELECT * FROM rooms WHERE id = {id};"
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

@app.route('/rooms/<id>', methods = ['GET'])
def get_user(id):
    conn = engine.connect()
    query = f"""SELECT *
            FROM rooms
            WHERE id = {id};
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
        data['id'] = row[0]
        data['name'] = row[1]
        data['capacity'] = row[2]
        data['price'] = row[3]
        data['stars'] = row[4]
        return jsonify(data), 200
    return jsonify({"message": "La habitacion no existe"}), 404


@app.route('/rooms/<id>', methods = ['DELETE'])
def delete_user(id):
    conn = engine.connect()
    query = f"""DELETE FROM rooms
            WHERE id = {id};
            """
    validation_query = f"SELECT * FROM rooms WHERE id = {id}"
    try:
        val_result = conn.execute(text(validation_query))
        if val_result.rowcount != 0 :
            result = conn.execute(text(query))
            conn.commit()
            conn.close()
        else:
            conn.close()
            return jsonify({"message": "la habitacion no existe"}), 404
    except SQLAlchemyError as err:
        jsonify(str(err.__cause__))
    return jsonify({'message': 'Se ha eliminado correctamente la habitacion'}), 202

### CRUD reserves

@app.route('/reserves',methods =['GET'])
def users():
    conn = engine.connect()

    query = "SELECT * FROM reserves;"        
    try:
        result = conn.execute(text(query))
        conn.close()
    except SQLAlchemyError as err:
        return jsonify(str(err.__cause__))
    
    
    data = []
    for row in result:
        entity = {}
        entity['id_reserve'] = row.id_reserve
        entity['id_room'] = row.id_room
        entity['email'] = row.email
        entity['entry_date']=row.entry_date
        entity['departure_date'] = row.departure_date
        entity['created_at'] = row.created_at
        data.append(entity)

    return jsonify(data), 200

@app.route('/create_reserve', methods = ['POST'])
def create_reserve():
    conn = engine.connect()
    new_reserve = request.get_json()
    query = f"""INSERT INTO reserves (email,id_room,entry_date, departure_date) VALUES ('{new_reserve["email"]}', '{new_reserve["id_room"]}', '{new_reserve["entry_date"]}', '{new_reserve["departure_date"]}'); """
    
    try:
        result = conn.execute(text(query))
        conn.commit()
        conn.close()
    except SQLAlchemyError as err:
        return jsonify({'message': 'Se ha producido un error' + str(err.__cause__)})
    
    return jsonify({'message': 'se ha creado la reserva correctamente' }), 201

@app.route('/reserves/<id_reserve>', methods = ['PATCH'])
def update_reserve(id_reserve):
    conn = engine.connect()
    mod_user = request.get_json()
    query = f"""UPDATE reserves SET entry_date = '{mod_user['entry_date']}', departure_date = '{mod_user['departure_date']}', WHERE id_reserve = {id_reserve};
            """
    query_validation = f"SELECT * FROM rooms WHERE id_reserve = {id_reserve};"
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

@app.route('/reserves/<id_reserve>', methods = ['GET'])
def get_reserve(id_reserve):
    conn = engine.connect()
    query = f"""SELECT *
            FROM reserves
            WHERE id_reserves = {id_reserve};
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
        data['id'] = row[0]
        data['name'] = row[1]
        data['capacity'] = row[2]
        data['price'] = row[3]
        data['stars'] = row[4]
        return jsonify(data), 200
    return jsonify({"message": "La reserva no existe"}), 404


@app.route('/reserves/<id_reserve>', methods = ['DELETE'])
def delete_reserve(id_reserve):
    conn = engine.connect()
    query = f"""DELETE FROM reserves
            WHERE id_reserve = {id_reserve};
            """
    validation_query = f"SELECT * FROM reserve WHERE id_reserve = {id_reserve}"
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



if __name__ == "__main__":
    app.run("127.0.0.1", port="5000", debug=True)