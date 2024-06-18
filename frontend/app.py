from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from datetime import datetime, date
import os
import requests
from flask_cors import CORS




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

    redirect(url_for('home'))

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

    
@app.route('/habitaciones/<variable>')
def habitacion(variable):
    title,discount = promocion()
    template = '%ss.html' % variable
    api_url = url_api
    response = requests.get(f"{api_url}/rooms/{variable}")
    if response.status_code == 200:
        if 'name' in session:
            user_id = session['id_usuario']
        else:
            user_id=None
        data = response.json()
        price = data.get("price")  # Obtener el precio de la habitación
        # Aplicar el descuento al precio de la habitación
        discounted_price = float(price) - float(price) * (discount / 100)
        capacity = data.get("capacity")
        name = data.get("room_name")
        description = data.get("description")
        stars = data.get("stars")
        id_room = data.get("id_room")
        return render_template(template, titulo=title, descuento=discount, capacidad=capacity, precio=price, precio_con_descuento=discounted_price, nombre=name, descripcion=description, estrellas=stars, id_room = id_room, user_id = user_id)
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

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        api_url = url_api
        registro_route = f"{api_url}/users"
        contraseña = request.form.get("contraseña")
        email = request.form.get("email")
        nombre = request.form.get("name")
        imagen = url_for('static', filename='img/usuario-default.png', _external=True)

        new_user = {
            "password": contraseña,
            "email": email,
            "user_name": nombre,
            "admin": 0,
            "url_imagen": imagen,
        }

        try:
            response = requests.post(registro_route, json=new_user)
        except requests.RequestException as e:
            return jsonify({'error': 'Error al intentar conectar con el servidor externo: ' + str(e)}), 400

        if response.status_code == 201:
            return redirect(url_for('login'))

        elif response.status_code == 400: 
            mensaje = response.json()
            flash(mensaje['message'])
            return render_template('registro.html')

        else:
            flash(f'Error {response.status_code}: {response.text}')
            return render_template('registro.html')

    if 'name' in session:
        return redirect(url_for('home'))

    return render_template('registro.html')


@app.route('/reservar', methods=['GET', 'POST'])
def reservar():

    if 'name' in session:
        user_id = session['id_usuario']
        title,discount = promocion()
    else:
        flash('Debes iniciar sesión para realizar una reserva')
        return redirect(url_for('login'))
    
    return render_template('reservar.html', user_id = user_id, descuento = discount)

@app.errorhandler(404)
def errorhandler(e):
    return render_template('404.html')

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
            return fecha_obj.date()

        def convertir_fecha_actual(fecha):
            fecha_obj = datetime.strptime(fecha, "%Y-%m-%d")
            return fecha_obj.date()

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
            reserva["end_date"] = convertir_fecha(reserva["end_date"])
        return render_template('reservas.html', reserves = reserves, user = user, fecha =  fecha_actual)
    return redirect(url_for('login'))

if __name__ == '__main__':
        app.run(debug=True, port=8080)