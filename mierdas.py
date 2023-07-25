                # Marcar los campos como "disabled" para evitar modificaciones después del cálculo
                form.from_currency.render_kw = {'disabled': True}
                form.cantidad_from.render_kw = {'disabled': True}
                form.to_currency.render_kw = {'disabled': True}




    def validate_cantidad_to(form, field):
        # Comprobar si los datos del campo cantidad_to coinciden con los almacenados en la sesión
        if field.data != session['cantidad_to']:
            raise ValidationError('No se permiten cambios después de calcular.')
        

def get_conversion_euros():
    # Establecer la conexión a la base de datos
    conn = sqlite3.connect('data/movements.db')
    cursor = conn.cursor()

    # Consulta para obtener la cantidad total de cada criptomoneda en euros
    query = """
    SELECT moneda_to, SUM(cantidad_to) AS total_euros
    FROM movements
    WHERE moneda_to != 'EUR'
    GROUP BY moneda_to
    """

    # Ejecutar la consulta
    cursor.execute(query)

    # Obtener los resultados de la consulta
    conversion_euros = {moneda: total for moneda, total in cursor.fetchall()}

    # Cerrar la conexión a la base de datos
    cursor.close()
    conn.close()

    return conversion_euros



def saldo(self):
    lista_saldo= []
    cryptos = ['EUR', 'BTC', 'ETH', 'BNB', 'ADA', 'DOT', 'XRP', 'SOL', 'USDT', 'MATIC']

    for crypto in cryptos:
        quantity_from = 0
        quantity_to = 0
        lista_to = self.quantity_to(crypto)
        if lista_to == [(None, None)]:
            pass
        else:
            quantity_to = lista_to[0][1]
        
        lista_from = self.quantity_from(crypto)
        if lista_from == [(None, None)]:
            pass
        else:
            quantityt_from = lista_from[0][1]

        total = quantity_to - quantity_from

        if total != 0 or crypto == "EUR":
            lista_saldo.append([crypto, total])

    return lista_saldo