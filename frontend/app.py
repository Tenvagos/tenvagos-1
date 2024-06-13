from flask import Flask, render_template, request, redirect, url_for, session, jsonify
"""from dotenv import load_dotenv"""
import os
import requests
"""from flask_cors import CORS"""

"""load_dotenv()"""


app = Flask(__name__)

"""CORS(app)"""

url_api = "https://testvagos.pythonanywhere.com/rooms"
app.secret_key = '6LeoBfIpAAAAAKi8ooFzL8knFiKGwqfCnOQrCF6c'

@app.route('/')
def home():
    if 'loggedin' in session:
            return render_template('home.html', username=session['loggedin'])
    return render_template('home.html', username=None)

@app.route('/habitaciones', methods = ['GET'])
def habitaciones():
    api_url = url_api
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        if 'loggedin' in session:
                return render_template('habitaciones.html', username=session['loggedin'], rooms = data)
        return render_template('habitaciones.html', username=None, rooms = data)
    else:
        return jsonify({'error': 'No se pudieron obtener los datos externos'}), response.status_code

@app.route('/<variable>')
def habitacion(variable):
    template = '%ss.html' % variable
    return render_template(template)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and 'user' in request.form and 'contraseña' in request.form:
        session['loggedin'] = request.form.get("user")
        return redirect(url_for('home'))
    if 'loggedin' in session:
        return render_template('home.html', username=session['loggedin'])
    return render_template('login.html')

@app.route('/reservar')
def reservar():
      return render_template('reservar.html')

@app.route('/logout')
def logout():
    session.pop('loggedin')
    return redirect(url_for('home'))

@app.route('/reservas')
def reservas():
    if 'loggedin' in session:
        return render_template('reservas.html', username=session['loggedin'])
    return redirect(url_for('login'))

if __name__ == '__main__':
        app.run(debug=True, port=8080)

"""
from flask import Flask, render_template, request, jsonify
from datetime import datetime

app = Flask(__name__)

# Datos simulados
room_prices = {
    'single': 50,
    'double': 80,
    'suite': 150
}

reservations = []

@app.route('/')
def reservar():
    return render_template('reservar.html')

@app.route('/check_availability', methods=['POST'])
def check_availability():
    data = request.get_json()
    room_type = data['roomType']
    check_in_date = datetime.strptime(data['checkInDate'], '%Y-%m-%d')
    check_out_date = datetime.strptime(data['checkOutDate'], '%Y-%m-%d')

    for reservation in reservations:
        if reservation['roomType'] == room_type:
            reserved_check_in = datetime.strptime(reservation['checkInDate'], '%Y-%m-%d')
            reserved_check_out = datetime.strptime(reservation['checkOutDate'], '%Y-%m-%d')
            if (check_in_date < reserved_check_out) and (check_out_date > reserved_check_in):
                return jsonify({'available': False})

    return jsonify({'available': True})

@app.route('/make_reservation', methods=['POST'])
def make_reservation():
    data = request.get_json()
    room_type = data['roomType']
    check_in_date = data['checkInDate']
    check_out_date = data['checkOutDate']

    total_price = calculate_total_price(room_type, check_in_date, check_out_date)
    discounted_price = apply_discount(total_price, 0.30)

    reservation = {
        'roomType': room_type,
        'checkInDate': check_in_date,
        'checkOutDate': check_out_date,
        'totalPrice': total_price,
        'discountedPrice': discounted_price
    }
    reservations.append(reservation)

    return jsonify({
        'success': True,
        'totalPrice': total_price,
        'discountedPrice': discounted_price
    })

def calculate_total_price(room_type, check_in_date, check_out_date):
    check_in = datetime.strptime(check_in_date, '%Y-%m-%d')
    check_out = datetime.strptime(check_out_date, '%Y-%m-%d')
    days = (check_out - check_in).days
    price_per_night = room_prices[room_type]
    return days * price_per_night

def apply_discount(price, discount_rate):
    return price * (1 - discount_rate)

if __name__ == '__main__':
    app.run(debug=True)

"""    