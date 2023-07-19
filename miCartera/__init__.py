from flask import Flask
from flask_session import Session
import os

app = Flask(__name__)

# Configuración de Flask-Session
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'


app.config.from_prefixed_env()


Session(app)