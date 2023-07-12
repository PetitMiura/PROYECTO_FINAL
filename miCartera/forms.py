from flask_wtf import FlaskForm
from wtforms import DateField, StringField, FloatField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from datetime import date

def date_le_today(form, field):
    if field.data > date.today():
        raise ValidationError("Must be lower than today")
    

class MovementForm(FlaskForm):
    date = DateField("Fecha", validators=[DataRequired("La Fecha es obligatoria"), date_le_today])
    time  = DateField("Hora",validators=[DataRequired("La hora es obligatoria")])
    moneda_from = StringField("Concepto", validators=[DataRequired("Moneda obligatoria")])
    cantidad_from = FloatField("Concepto", validators=[DataRequired("Cantidad obligatoria")])
    moneda_to = StringField("Concepto", validators=[DataRequired("Moneda obligatoria")])
    cantidad_to = FloatField("Concepto", validators=[DataRequired("Cantidad obligatoria")])   


    submit = SubmitField("Enviar")

