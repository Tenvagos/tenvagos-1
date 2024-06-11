from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = '6LeoBfIpAAAAAKi8ooFzL8knFiKGwqfCnOQrCF6c'

@app.route('/')
def home():
        if 'loggedin' in session:
                return render_template('home.html', username=session['loggedin'])
        return render_template('home.html', username=None)

@app.route('/habitaciones')
def habitaciones():
        if 'loggedin' in session:
                return render_template('habitaciones.html', username=session['loggedin'])
        return render_template('habitaciones.html', username=None)

@app.route('/login', methods=['GET', 'POST'])
def login():
        if request.method == 'POST' and 'user' in request.form and 'contraseña' in request.form:

                session['loggedin'] = request.form.get("user")

                return redirect(url_for('home'))
        return render_template('login.html')

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