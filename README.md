# Tenvagos-1

¡Bienvenido a al proyecto Tenvagos! Esta es una aplicación para reservas de hotel desarrollada con Flask. Esta aplicación permite a los usuarios registrarse para servicios, hacer reserva de habitaciones y más! Apunta a proporcionar una experiencia de usuario completa y funcional, los detalles del proyecto se describen a continuación.

- Se encuentra disponible un informe final de este trabajo grupal en un archivo PFD en este repositorio.

## Características

- Registro y autenticación de usuarios
- Sistema de reserva de habitaciones
- Formulario de contacto con verificación de captcha
- Visualización de promociones actuales basadas en habitaciones y el mes deseado
- Gestión de sesiones de usuario
- Base de datos SQL para almacenar información de usuario, habitaciones, reservas, meses y promociones respectivas.

## Tecnologías utilizadas

- Flask: Un micro framework web escrito en Python.
- Jinja2: Un lenguaje de plantillas para Python, utilizado para generar HTML dinámico en las páginas web de Flask.
- HTML: Se utiliza para la estructura de la página web.
- CSS: Se utiliza para el diseño y la presentación de la página web.
- JavaScript: Utilizado para el desarrollo de frontend.
- SQL: Utilizado para la gestión de bases de datos.
- Python: La lógica de la aplicación tanto en frontend como en backend, está escrita en Python.
- pip: Un instalador de paquetes para Python. Se utiliza para instalar las bibliotecas y frameworks necesarios.

## Uso de la aplicación ya desplegada

La aplicación está desplegada en dos dominios:

- Sitio web de la aplicación: [sogavnet.pythonanywhere.com](http://sogavnet.pythonanywhere.com)
- API: [tenvagoss.pythonanywhere.com](http://tenvagoss.pythonanywhere.com)

Puedes registrarte, iniciar sesión, reservar habitaciones, ver tus reservas, y utilizar el formulario de contacto en el sitio del frontend. La API maneja todas las solicitudes y gestiona la base de datos.

## Uso la aplicacion

- La aplicación comienza con la página de inicio donde se muestran las promociones actuales.
- Los usuarios pueden registrarse o iniciar sesión en la aplicación.
- Una vez iniciada la sesión, los usuarios pueden reservar habitaciones y ver sus reservas.
- El formulario de contacto se puede utilizar para enviar mensajes después de completar la verificación de captcha.

## Uso del código fuente

Si deseas ejecutar el código fuente en tu máquina local, sigue estos pasos:

- Clona el repositorio:
```
git clone https://github.com/<tu-nombre-de-usuario-de-github>/tenvagos-1.git
```

### Configuración del backend

1. Navega al directorio del backend:
```
cd backend
```
2. Crea un entorno virtual:
```
python -m venv env source env/bin/activate
```
3. Navega a la carpeta sql:
```
cd sql
```
4. Encontrarás un archivo llamado `init.sql`. Este archivo contiene las instrucciones SQL para configurar la base de datos. Puedes usar tu método preferido para ejecutar este archivo SQL y configurar la base de datos.

5. El archivo `.env` en el directorio del backend contiene las variables de entorno para la conexión a la base de datos. Asegúrate de configurar estas variables con los detalles de tu conexión a la base de datos.

6. Regresa a la carpeta backend e instala las dependencias necesarias para el proyecto. Estas dependencias están listadas en el archivo `requirements.txt` en el directorio del backend. Puedes instalarlas usando pip:
```
cd ..
pip install -r requirements.txt
```
6. Una vez que hayas configurado la base de datos, las variables de entorno y las dependencias, puedes iniciar el servidor del backend ejecutando el archivo `app.py` en el directorio del backend:
```
flask run
```
Esto iniciará el servidor del backend, que escuchará las solicitudes de la aplicación frontend.

### Configuración del frontend

1. Una vez ejecutada la API, navega al directorio del frontend:
```
cd ..
cd frontend
```
2. Crea un entorno virtual:
```
python -m venv env source env/bin/activate
```
3. Instala las dependencias necesarias:
```
pip install -r requirements.txt
```
4. Ejecuta la aplicación:
```
flask run
```

## Licencia

[MIT](https://choosealicense.com/licenses/mit/)
