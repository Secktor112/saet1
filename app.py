from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Configuration
from flask_login import LoginManager



app = Flask(__name__)
app.secret_key = 'secret aga'
app.config.from_object(Configuration)

db = SQLAlchemy(app)
manager = LoginManager(app)
