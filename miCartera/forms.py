from flask_wtf import FlaskForm
from wtforms import DateField, StringField, FloatField, SelectField, SubmitField, HiddenField
from wtforms.validators import DataRequired, Length, ValidationError
from datetime import date



# Valores diferentes en los SelectFields
def validate_different_values(form, field):
    # Obtiene el valor seleccionado en el campo "from_currency"
    from_currency = form.from_currency.data

    # Obtiene el valor seleccionado en el campo "to_currency"
    to_currency = field.data

    # Verifica si los valores son iguales y si lo son, lanza una excepción
    if from_currency == to_currency:
        raise ValidationError('Los campos "From" y "To" deben ser diferentes.')


# moneda from
def mfrom(form, field):
    valid_options = ['EUR', 'BTC', 'ETH', 'BNB', 'ADA', 'DOT', 'XRP', 'SOL', 'USDT', 'MATIC']
    if field.data not in valid_options:
        raise ValidationError('Moneda "From" inválida.')
# moneda to
def mto(form, field):
    valid_options = ['EUR', 'BTC', 'ETH', 'BNB', 'ADA', 'DOT', 'XRP', 'SOL', 'USDT', 'MATIC']
    if field.data not in valid_options:
        raise ValidationError('Moneda "To" inválida.')

#cantidad from
def cfrom(form, field):
    # Menor a cero no es válido
    if field.data <= 0:
        raise ValidationError('La cantidad debe ser mayor que cero.')
         

class CompraForm(FlaskForm):

    from_currency = SelectField('From:', choices=[('EUR', 'EUR'), ('BTC', 'BTC'), ('ETH', 'ETH'),
                                                ('BNB', 'BNB'), ('ADA', 'ADA'), ('DOT', 'DOT'),
                                                ('XRP', 'XRP'), ('SOL', 'SOL'), ('USDT', 'USDT'),
                                                ('MATIC', 'MATIC')],validators=[DataRequired(), mfrom])
    cantidad_from = FloatField('Cantidad From:', validators=[DataRequired(), cfrom])
    to_currency = SelectField('To:', choices=[('EUR', 'EUR'), ('BTC', 'BTC'), ('ETH', 'ETH'),
                                                ('BNB', 'BNB'), ('ADA', 'ADA'), ('DOT', 'DOT'),
                                                ('XRP', 'XRP'), ('SOL', 'SOL'), ('USDT', 'USDT'),
                                                ('MATIC', 'MATIC')], validators=[DataRequired(), mto])
    cantidad_to = HiddenField()
    calculate = SubmitField('calcular')
    submit = SubmitField('Enviar')

