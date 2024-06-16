from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from datetime import datetime, date
"""from dotenv import load_dotenv"""
import os
import requests
from flask_cors import CORS
from flask_recaptcha import ReCaptcha

"""load_dotenv()"""


app = Flask(__name__)

CORS(app)

url_api = "https://tenvagoss.pythonanywhere.com"
app.secret_key = '6LeoBfIpAAAAAKi8ooFzL8knFiKGwqfCnOQrCF6c'


def obtener_mes_actual():
    fecha_actual = datetime.now()
    return fecha_actual.month

def promocion(): #podemos extraer la promocion del la estacion segun querramos usarla
    mesactual = obtener_mes_actual()
    if mesactual == 12 or mesactual == 1 or mesactual == 2 :
        id = 3
    elif mesactual == 3 or mesactual == 4 or mesactual == 5:
        id = 4
    elif mesactual == 6 or mesactual == 7 or mesactual == 8:
        id = 1
    elif mesactual == 9 or mesactual == 10 or mesactual == 11:
        id = 2
    api_url = url_api
    response = requests.get(f"{api_url}/promotions/{id}")
    if response.status_code == 200:
        data = response.json()
        title = data.get("title")
        discount = data.get("last_date")
        return title,discount
    else:
        return jsonify({'error': 'No se pudieron obtener los datos externos'}), response.status_code  

def verificar_captcha(captcha_response):
    """ Valida el captcha desde el servidor de google
        retorna true si es correcto o false si no
    """
    secret = "6LdA0_UpAAAAAEjzhk363bZfGDwgt8GCtvAMFZi2"
    payload = {'response':captcha_response, 'secret':secret}
    response = requests.post("https://www.google.com/recaptcha/api/siteverify", payload)
    respuesta = response.json()
    return respuesta['success']

@app.route('/')
def home():
    title,discount = promocion()
    if 'name' in session:
            return render_template('home.html', username=session['name'],titulo=title,descuento=discount)
    return render_template('home.html', username=None,titulo=title,descuento=discount)

@app.route('/contact', methods = ['POST'])
def contacto():
 
    if request.method == "POST":

        captcha_response = request.form.get('g-recaptcha-response')
         
        if verificar_captcha(captcha_response):
            flash("Mensaje enviado")
        else:
            flash("Completa el desafio reCaptcha")
            return redirect(url_for('home')+"#contacto")
 
        return redirect("https://formsubmit.co/c692c80bc93633c1c420822f2cee9914", code=307)


        


@app.route('/habitaciones', methods = ['GET'])
def habitaciones():
    api_url = url_api
    response = requests.get(f"{api_url}/rooms")
    if response.status_code == 200:
        data = response.json()
        if 'name' in session:
                return render_template('habitaciones.html', username=session['name'], rooms = data)
        return render_template('habitaciones.html', username=None, rooms = data)
    else:
        return jsonify({'error': 'No se pudieron obtener los datos externos'}), response.status_code

    
@app.route('/<variable>')
def habitacion(variable):
    title,discount = promocion()
    template = '%ss.html' % variable
    api_url = url_api
    response = requests.get(f"{api_url}/rooms/{variable}")
    if response.status_code == 200:
        data = response.json()
        price = data.get("price")  # Obtener el precio de la habitación
        # Aplicar el descuento al precio de la habitación
        discounted_price = float(price) * (discount / 100)
        capacity = data.get("capacity")
        name = data.get("room_name")
        description = data.get("description")
        stars = data.get("stars")
        return render_template(template, titulo=title, descuento=discount, capacidad=capacity, precio=price, precio_con_descuento=discounted_price, nombre=name, descripcion=description, estrellas=stars)
    else:
        return jsonify({'error': 'No se pudieron obtener los datos externos'}), response.status_code

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        api_url = url_api
        login_route = f"{api_url}/login"
        usuario = request.form.get("user")
        contraseña = request.form.get("contraseña")

        user = {"username": usuario, "password": contraseña}
        
        response = requests.post(login_route, json = user)

        if response.status_code == 200:
            datos = response.json()
            session['id_usuario'] = datos['id_user']
            session['name'] = datos['user_name']
            session['email'] = datos['email']
            session['image'] = datos['url_imagen']

        elif response.status_code == 401:
            mensaje = response.json()
            flash(mensaje['message'])
            return render_template('login.html')

        else:
            return jsonify({'error': 'No se pudieron obtener los datos externos'}), response.status_code

        return redirect(url_for('home'))

    if 'name' in session:
        return render_template('home.html', username=session['name'])

    return render_template('login.html')

@app.route('/reservar', methods=['GET', 'POST'])
def reservar():
    if request.method == 'POST':
        checkin = request.form.get('checkin')
        checkout = request.form.get('checkout')

        if 'name' in session:
            user_id = session['id_usuario']
        else:
            flash('Debes iniciar sesión para realizar una reserva')
            return redirect(url_for('login'))

        reserva = {
            "user_id": user_id,
            "checkin": checkin,
            "checkout": checkout,
        }

        api_url = f"{url_api}/reservations"
        response = requests.post(api_url, json=reserva)

        if response.status_code == 200:
            flash('Reserva realizada con éxito')
            return redirect(url_for('reservas'))
        else:
            flash('Error al realizar la reserva')
            return render_template('reservar.html')
        

    return render_template('reservar.html')

@app.route('/logout')
def logout():
    if 'name' in session:
        session.clear()
    
    return redirect(url_for('home'))

@app.route('/reservas')
def reservas():
    if 'name' in session:

        def convertir_fecha(fecha):
            fecha_obj = datetime.strptime(fecha, "%a, %d %b %Y %H:%M:%S %Z")
            return fecha_obj.strftime("%d-%m-%Y")
        
        def convertir_fecha_actual(fecha):
            fecha_obj = datetime.strptime(fecha, "%Y-%m-%d")
            return fecha_obj.strftime("%d-%m-%Y")
        
        fechita = f"{date.today()}"
        fecha_actual = convertir_fecha_actual(fechita)

        user = {
             "user_name" : session['name'],
             "email": session['email'],
             "id_user": session['id_usuario'],
             "image": session['image'],
        }
        
        response = requests.get(f"{url_api}/my_reserves/{session['id_usuario']}")
        reserves = response.json()
        for reserva in reserves:
            reserva["start_date"] = convertir_fecha(reserva["start_date"])
            print(reserva["start_date"])
            reserva["end_date"] = convertir_fecha(reserva["end_date"])
        return render_template('reservas.html', reserves = reserves, user = user, fecha =  fecha_actual)
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