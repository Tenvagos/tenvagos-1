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

### CRUD RESERVAS

@app.route('/reservas',methods =['GET'])
def users():
    conn = engine.connect()

    query = "SELECT * FROM reservas;"        
    try:
        result = conn.execute(text(query))
        conn.close()
    except SQLAlchemyError as err:
        return jsonify(str(err.__cause__))
    
    
    data = []
    for row in result:
        entity = {}
        entity['id_reserva'] = row.email
        entity['id_habitacion'] = row.id_habitacion
        entity['id_usuario'] = row.id_usuario
        entity['fecha_entrada']=row.fecha_entrada
        entity['fecha_salida'] = row.fecha_salida
        entity['created_at'] = row.created_at
        data.append(entity)

    return jsonify(data), 200

@app.route('/crear_reserva', methods = ['POST'])
def crear_reserva():
    conn = engine.connect()
    nueva_reserva = request.get_json()
    query = f"""INSERT INTO reservas (email,id_habitacion,fecha_entrada, fecha_salida) VALUES ('{nueva_reserva["email"]}', '{nueva_reserva["id_habitacion"]}', '{nueva_reserva["fecha_entrada"]}', '{nueva_reserva["fecha_salida"]}'); """
    
    try:
        result = conn.execute(text(query))
        conn.commit()
        conn.close()
    except SQLAlchemyError as err:
        return jsonify({'message': 'Se ha producido un error' + str(err.__cause__)})
    
    return jsonify({'message': 'se ha creado la reserva correctamente' }), 201

@app.route('/reservas/<id_reserva>', methods = ['PATCH'])
def update_reserva(id_reserva):
    conn = engine.connect()
    mod_user = request.get_json()
    query = f"""UPDATE reservas SET fecha_entrada = '{mod_user['fecha_entrada']}', fecha_salida = '{mod_user['fecha_salida']}', WHERE id_reserva = {id_reserva};
            """
    query_validation = f"SELECT * FROM habitaciones WHERE id_reserva = {id_reserva};"
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

@app.route('/reservas/<id_reservas>', methods = ['GET'])
def get_reserva(id_reservas):
    conn = engine.connect()
    query = f"""SELECT *
            FROM reservas
            WHERE id_reservas = {id_reservas};
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
        data['nombre'] = row[1]
        data['cantidad'] = row[2]
        data['precio'] = row[3]
        data['estrellas'] = row[4]
        return jsonify(data), 200
    return jsonify({"message": "La reserva no existe"}), 404


@app.route('/reservas/<id_reservas>', methods = ['DELETE'])
def delete_reserva(id_reserva):
    conn = engine.connect()
    query = f"""DELETE FROM reservas
            WHERE id_reserva = {id_reserva};
            """
    validation_query = f"SELECT * FROM reserva WHERE id_reserva = {id_reserva}"
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