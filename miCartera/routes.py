from flask import Flask, render_template, request, redirect, url_for, flash
import requests
import sqlite3
from datetime import datetime
from .models import Movement, MovementsDAOsqlite
from miCartera.forms import MovementForm
from miCartera import app


dao = MovementsDAOsqlite(app.config.get("PATH_SQLITE"))

@app.route('/', methods=['GET'])
def index():
    try:
        movements = dao.get_all()  # Obtener todos los movimientos de la base de datos
        print(movements)
        the_form = MovementForm()  # Crear una instancia del formulario
        return render_template('index.html', movements=movements, the_form=the_form)
    except ValueError as e:
        flash("Su aplicacion esta corrupta")
        flash(str(e))
        return render_template('index.html', movements=movements, the_form=the_form)

@app.route('/compra', methods=['GET', 'POST'])
def purchase():
    if request.method == 'POST':
        moneda_from = request.form['from']
        cantidad_from = request.form['cantidad_from']
        moneda_to = request.form['to']
        
        # Consulta a la API de CoinAPI para obtener la tasa de conversión
        apikey = app.config.get("API_KEY")
        url = f'https://rest.coinapi.io/v1/exchangerate/{moneda_from}/{moneda_to}?apikey={apikey}'
        response = requests.get(url)
        data = response.json()
        
        if 'rate' in data:
            rate = data['rate']
            cantidad_to = cantidad_from * rate  # Calcula la cantidad_to basada en la tasa de conversión
            
            # Crea y guarda el nuevo movimiento
            movement = Movement(None, datetime.now().strftime('%Y-%m-%d'), datetime.now().strftime('%H:%M:%S'), moneda_from, cantidad_from, moneda_to, cantidad_to)
            dao.insert(movement)
            
            return redirect(url_for('index'))
        
    return render_template('compra.html')

@app.route('/status', methods=['GET'])
def status():
    movements = dao.get_all()  # Obtener todos los movimientos de la base de datos
    # Aquí se debería calcular el estado de la inversión basándose en los movimientos
    # Este es un cálculo más complejo que involucra sumar y restar las cantidades y consultar el valor actual de las criptomonedas.
    # No se ha proporcionado una implementación detallada aquí ya que esto requeriría un análisis más detallado de las necesidades del proyecto.
    return render_template('status.html', status=status)











