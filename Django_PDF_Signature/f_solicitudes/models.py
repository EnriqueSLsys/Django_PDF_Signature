import re
from django.db import models
from django.core.exceptions import ValidationError

def val_dni(value):
    # Compilo mi expresión regular para validar el formato del DNI
    dni_pattern = re.compile(r'^\d{8}[A-Za-z]$')

    # Verifico si el formato del DNI es válido
    if not dni_pattern.match(value):
        raise ValidationError('El formato del DNI no es válido.')

    # Aqui extraigo los dígitos del DNI
    dni_digits = value[:-1]

    # Calculo la letra esperada para el DNI
    letras_validas = 'TRWAGMYFPDXBNJZSQVHLCKE'
    letra_calculada = letras_validas[int(dni_digits) % 23]

    # Aqui verifico si la letra del DNI es válida
    if value[-1].upper() != letra_calculada:
        raise ValidationError('La letra del DNI proporcionada no es válida.')

class Solicitud(models.Model):
    nom = models.CharField(max_length=55)
    ap1 = models.CharField(max_length=55)
    ap2 = models.CharField(max_length=55, blank=True)
    dni = models.CharField(max_length=9, validators=[val_dni])
    texto = models.TextField(max_length=512)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        epoch_time = int(self.fecha_creacion.timestamp())
        return f'{self.nom} {self.ap1} {self.ap2} - Fecha: {self.fecha_creacion}, Epoch: {epoch_time}'
