from flask_wtf import FlaskForm
from wtforms import DateField, StringField, FloatField, SelectField, SubmitField, HiddenField
from wtforms.validators import DataRequired, Length, ValidationError
from datetime import date

def compra_validations():
    pass

class CompraForm(FlaskForm):
    from_currency = SelectField('From:', choices=[('EUR', 'Euros'), ('BTC', 'BTC'), ('ETH', 'ETH'),
                                                ('BNB', 'BNB'), ('ADA', 'ADA'), ('DOT', 'DOT'),
                                                ('XRP', 'XRP'), ('SOL', 'SOL'), ('USDT', 'USDT'),
                                                ('MATIC', 'MATIC')],validators=[DataRequired()])
    cantidad_from = FloatField('Cantidad From:', validators=[DataRequired()])
    to_currency = SelectField('To:', choices=[('EUR', 'EUR'), ('BTC', 'BTC'), ('ETH', 'ETH'),
                                                ('BNB', 'BNB'), ('ADA', 'ADA'), ('DOT', 'DOT'),
                                                ('XRP', 'XRP'), ('SOL', 'SOL'), ('USDT', 'USDT'),
                                                ('MATIC', 'MATIC')], validators=[DataRequired()])
    cantidad_to = HiddenField()
    calculate = SubmitField('calcular')
    submit = SubmitField('Enviar')
    


