from flask import Flask
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
from routes.rooms import create_rooms_router
from routes.reserves import create_reserves_router
from routes.users import create_users_router

load_dotenv()

user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
host = os.getenv('DB_HOST')
db =  os.getenv('DB_NAME')


app = Flask(__name__)
engine = create_engine(f'mysql+mysqlconnector://{user}:{password}@{host}/{db}')

app.register_blueprint(create_rooms_router(engine))
app.register_blueprint(create_reserves_router(engine))
app.register_blueprint(create_users_router(engine))

if __name__ == "__main__":
    app.run("127.0.0.1", port="5000", debug=True)