from flask import Flask
from flask_wtf.csrf import CSRFProtect
import os

app = Flask(__name__)
app.config.from_prefixed_env()

# Configuración de CSRF
csrf = CSRFProtect(app)
