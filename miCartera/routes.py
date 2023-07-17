from flask import Flask, render_template, request, redirect, url_for, flash
import requests
import sqlite3
from datetime import datetime
from .models import Movement, MovementsDAOsqlite
from miCartera.forms import CompraForm
from miCartera import app


dao = MovementsDAOsqlite(app.config.get("PATH_SQLITE"))

@app.route('/', methods=['GET'])
def index():
    try:
        movements = dao.get_all()  # Obtener todos los movimientos de la base de datos
        form = CompraForm()  # Crear una instancia del formulario
        return render_template('index.html', movements=movements, route=request.path, title='Index')
    except ValueError as e:
        flash("Su aplicacion esta corrupta")
        flash(str(e))
        return render_template('index.html', movements=movements, route=request.path, title='Index')

@app.route('/compra', methods=['GET', 'POST'])
def purchase():
    form = CompraForm()
    moneda_from = ''
    cantidad_from = 0
    moneda_to = ''
    cantidad_to = 0
    
    if request.method == 'GET':
        return render_template('compra.html', form=form, route=request.path, title='Compra')
    elif form.calculate.data:
        if form.validate():
            moneda_from = form.from_currency.data
            cantidad_from = form.cantidad_from.data
            moneda_to = form.to_currency.data
            
            # Consulta a la API de CoinAPI para obtener la tasa de conversión
            url = f'https://rest.coinapi.io/v1/exchangerate/{moneda_from}/{moneda_to}?apikey={app.config.get("API_KEY")}'
            response = requests.get(url)
            data = response.json()

            if 'rate' in data:
                rate = data['rate']
                cantidad_to = cantidad_from * rate  # Calcula la cantidad_to basada en la tasa de conversión
                form.cantidad_to.data = cantidad_to  # Asigna el valor calculado a form.cantidad_to.data

        # Renderiza la plantilla "compra.html" con el formulario actualizado y la cantidad convertida en el contexto
        return render_template('compra.html', form=form, route=request.path, title='Compra')

    else:
        # Crea y guarda el nuevo movimiento
        movement = Movement(None, datetime.now().strftime('%Y-%m-%d'), datetime.now().strftime('%H:%M:%S'), moneda_from, cantidad_from, moneda_to, cantidad_to)
        dao.insert(movement)

        return redirect('/')
        
@app.route('/status', methods=['GET'])
def status():
    movements = dao.get_all()  # Obtener todos los movimientos de la base de datos
    # Aquí se debería calcular el estado de la inversión basándose en los movimientos
    # Este es un cálculo más complejo que involucra sumar y restar las cantidades y consultar el valor actual de las criptomonedas.
    # No se ha proporcionado una implementación detallada aquí ya que esto requeriría un análisis más detallado de las necesidades del proyecto.
    return render_template('status.html', status=status, movements=movements, route=request.path, title='Status')











