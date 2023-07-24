from flask_wtf import FlaskForm
from wtforms import DateField, StringField, FloatField, SelectField, SubmitField, HiddenField
from wtforms.validators import DataRequired, Length, ValidationError
from datetime import date


# Valores diferentes en los SelectFields
def validate_different_values(form, field):
    # Verifica si los valores son iguales y si lo son, lanza una excepción
    if form.from_currency.data == field.data:
        raise ValidationError('Los campos "From" y "To" deben ser diferentes.')
#cantidad from
def cfrom(form, field):
    # Menor a cero no es válido
    if field.data <= 0:
        raise ValidationError('La cantidad debe ser mayor que cero.')
         

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



class CompraForm(FlaskForm):

    from_currency = SelectField('From:', choices=[('EUR', 'EUR'), ('BTC', 'BTC'), ('ETH', 'ETH'),
                                                ('BNB', 'BNB'), ('ADA', 'ADA'), ('DOT', 'DOT'),
                                                ('XRP', 'XRP'), ('SOL', 'SOL'), ('USDT', 'USDT'),
                                                ('MATIC', 'MATIC')],validators=[DataRequired(), mfrom])
    cantidad_from = FloatField('Cantidad From:', validators=[cfrom, DataRequired('Letras o Cantidad <= 0 no permitidas en el campo cantidad')])
    to_currency = SelectField('To:', choices=[('EUR', 'EUR'), ('BTC', 'BTC'), ('ETH', 'ETH'),
                                                ('BNB', 'BNB'), ('ADA', 'ADA'), ('DOT', 'DOT'),
                                                ('XRP', 'XRP'), ('SOL', 'SOL'), ('USDT', 'USDT'),
                                                ('MATIC', 'MATIC')], validators=[DataRequired(), mto, validate_different_values])
    cantidad_to = HiddenField()
    calculate = SubmitField('calcular')
    submit = SubmitField('✔')

