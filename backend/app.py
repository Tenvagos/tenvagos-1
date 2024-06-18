from flask import Flask
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
from flask_cors import CORS
from routes.rooms import create_rooms_router
from routes.reserves import create_reserves_router
from routes.users import create_users_router
from routes.months import create_months_router
from routes.promotions import create_promotions_router
from routes.my_reserves import create_my_reserves_router
from routes.login import create_login_router

load_dotenv()

user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
host = os.getenv('DB_HOST')
db =  os.getenv('DB_NAME')


app = Flask(__name__)
CORS(app)
engine = create_engine(f'mysql+mysqlconnector://{user}:{password}@{host}/{db}')

app.register_blueprint(create_rooms_router(engine))
app.register_blueprint(create_reserves_router(engine))
app.register_blueprint(create_users_router(engine))
app.register_blueprint(create_months_router(engine))
app.register_blueprint(create_promotions_router(engine))
app.register_blueprint(create_my_reserves_router(engine))
app.register_blueprint(create_login_router(engine))

if __name__ == "__main__":
    app.run("127.0.0.1", port="5000", debug=True)
