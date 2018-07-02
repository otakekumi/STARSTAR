from flask import Flask,Blueprint
from app import config
from admin import admin



app = Flask(__name__)


app.config.from_pyfile("config.py")
app.register_blueprint(admin)


from app import model
from app import view


