from flask import Flask, render_template, request, redirect, url_for, flash, session
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

    if request.method == 'GET':
        session['from_currency'] = ""
        session['cantidad_from'] = 0
        session['to_currency'] = ""
        session['cantidad_to'] = 0
        return render_template('compra.html', form=form, route=request.path, title='Compra')
    

    elif form.calculate.data:
        try:
            if form.validate_on_submit():
                moneda_from = form.from_currency.data
                cantidad_from = form.cantidad_from.data
                moneda_to = form.to_currency.data

                # Consulta a la API de CoinAPI para obtener la tasa de conversión
                url = f'https://rest.coinapi.io/v1/exchangerate/{moneda_from}/{moneda_to}?apikey={app.config.get("API_KEY")}'
                response = requests.get(url)
                data = response.json()
                if response.status_code == 200:

                    if 'rate' in data:
                        rate = data['rate']
                        cantidad_to = cantidad_from * rate  # Calcula la cantidad_to basada en la tasa de conversión
                        form.cantidad_to.data = cantidad_to  # Asigna el valor calculado a form.cantidad_to.data

                        # Almacenar los datos del primer POST en la sesión
                        session['from_currency'] = moneda_from
                        session['cantidad_from'] = cantidad_from
                        session['to_currency'] = moneda_to
                        session['cantidad_to'] = cantidad_to  # Almacena también cantidad_to en la sesión
                        # Renderiza la plantilla "compra.html" con el formulario actualizado y la cantidad convertida en el contexto
                        return render_template('compra.html', form=form, route=request.path, title='Compra')
                else:
                    flash(data["error"])
                    return render_template('compra.html', form=form, route=request.path, title='Compra')



        except ValueError as e:
            flash(str(e))

    else:
        try:
            if form.validate_on_submit():
                if ('from_currency' in session and
                    'cantidad_from' in session and
                    'to_currency' in session and
                    'cantidad_to' in session and
                    form.from_currency.data == session['from_currency'] and
                    form.cantidad_from.data == session['cantidad_from'] and
                    form.to_currency.data == session['to_currency'] and
                    form.cantidad_to.data == str(session['cantidad_to'])):
                    # Crea y guarda el nuevo movimiento
                    movement = Movement(None, datetime.now().strftime('%Y-%m-%d'), datetime.now().strftime('%H:%M:%S'), form.from_currency.data, form.cantidad_from.data, form.to_currency.data, session['cantidad_to'])
                    dao.insert(movement)
                    flash('Compra realizada exitosamente.')
                else:
                    flash('No se permiten cambios después de calcular.')
                    return render_template('compra.html', form=form, route=request.path, title='Compra')
            else:
                flash('Error de validación en el formulario.')

        except ValueError as e:
            flash(str(e), 'danger')

    return redirect('/')

        
@app.route('/status', methods=['GET'])
def status():

    movements = dao.get_all()  # Obtener todos los movimientos de la base de datos
    # Aquí se debería calcular el estado de la inversión basándose en los movimientos
    # Este es un cálculo más complejo que involucra sumar y restar las cantidades y consultar el valor actual de las criptomonedas.
    # No se ha proporcionado una implementación detallada aquí ya que esto requeriría un análisis más detallado de las necesidades del proyecto.
    return render_template('status.html', status=status, movements=movements, route=request.path, title='Status')









