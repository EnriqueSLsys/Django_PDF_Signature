from django import forms
from f_solicitudes.models import Solicitud

class SolicitudForm(forms.ModelForm):
    dni = forms.CharField(max_length=9, widget=forms.TextInput(attrs={'placeholder': 'Ej: 12345678A'}))

    class Meta:
        model = Solicitud
        fields = ['nom', 'ap1', 'ap2', 'dni', 'texto']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nom'].error_messages = {'required': 'Por favor, ingresa tu nombre.'}
        self.fields['ap1'].error_messages = {'required': 'Por favor, ingresa al menos tu primer apellido.'}
        self.fields['dni'].error_messages = {'required': 'Por favor, ingresa tu DNI.'}
        self.fields['texto'].error_messages = {'required': 'Por favor, ingresa un texto.'}
