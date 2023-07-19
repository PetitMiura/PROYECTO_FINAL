                # Marcar los campos como "disabled" para evitar modificaciones después del cálculo
                form.from_currency.render_kw = {'disabled': True}
                form.cantidad_from.render_kw = {'disabled': True}
                form.to_currency.render_kw = {'disabled': True}




    def validate_cantidad_to(form, field):
        # Comprobar si los datos del campo cantidad_to coinciden con los almacenados en la sesión
        if field.data != session['cantidad_to']:
            raise ValidationError('No se permiten cambios después de calcular.')