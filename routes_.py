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
        flash('Su base de datos esta inoperativa')
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
            else:
                for msg, valor in form.errors.items():
                    flash(valor[0])
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
    # Obtener todos los movimientos de la base de datos
    movements = dao.get_all()

    # Calcular los totales y conversiones para cada criptomoneda
    total_cryptos = {}  # Diccionario para almacenar los totales de cada criptomoneda

    for movement in movements:
        if movement.moneda_to == 'EUR':
            pass
        else:
            moneda_to = movement.moneda_to
            cantidad_to = movement.cantidad_to

        if moneda_to in total_cryptos:
            total_cryptos[moneda_to] += cantidad_to
        else:
            total_cryptos[moneda_to] = cantidad_to

    # Obtener la clave de API de CoinAPI desde la configuración de la aplicación
    api_key = app.config.get("API_KEY")

    # Realizar llamada a la API para obtener los valores de conversión en euros
    conversion_euros = {}
    for moneda in total_cryptos.keys():
        if moneda == 'EUR':
            conversion_euros[moneda] = 1.0  # El valor de 1 euro en euros es 1.0 (1 euro)
        else:
            # Hacer la llamada a la API para obtener el valor de conversión de la criptomoneda a euros
            url = f'https://rest.coinapi.io/v1/exchangerate/{moneda}/EUR?apikey={api_key}'
            response = requests.get(url)
            data = response.json()

            if response.status_code == 200 and 'rate' in data:
                conversion_euros[moneda] = data['rate']
            else:
                # En caso de error, asignamos un valor de conversión predeterminado (puedes modificarlo)
                flash("Error")

    # Crear una lista de tuplas con la información de cada criptomoneda y sus totales y conversiones
    data_cryptos = []
    for moneda, total in total_cryptos.items():
        if moneda in conversion_euros:
            conversion = total * conversion_euros[moneda]
            data_cryptos.append((moneda, total, conversion))

    
    # Calcular el valor total de la inversión en euros
    total_inversion = 0
    for moneda, total in total_cryptos.items():
        if moneda in conversion_euros:
            total_inversion += total * conversion_euros[moneda]

    
    # Calcular el Precio de compra
    euro_retirado_por_venta = 0
    for movement in movements:
        if movement.moneda_to == 'EUR':
            euro_retirado_por_venta += movement.cantidad_to

    precio_compra = total_inversion - euro_retirado_por_venta

    # Calcular el Resultado de la inversión
    resultado_inversion = total_inversion - precio_compra

    # Renderizar la plantilla 'status.html' con la información calculada
    return render_template('status.html', data_cryptos=data_cryptos, total_inversion=total_inversion, precio_compra=precio_compra, resultado_inversion=resultado_inversion, route=request.path, title='Status')













