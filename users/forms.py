# coding=utf-8
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ObjectDoesNotExist

from . import models


class UserRegisterForm(forms.ModelForm):

    class Meta:
        model = models.User
        fields = ['nombre', 'apellido1', 'apellido2', 'dni', 'titulacion',
                  'email', 'telefono', 'password1', 'password2']

    password1 = forms.CharField(widget=forms.PasswordInput, label='Contraseña')
    password2 = forms.CharField(
        widget=forms.PasswordInput, label='Confirme contraseña')

    def clean_dni(self):
        dni = self.cleaned_data.get('dni')
        try:
            dni_check = models.User.objects.get(dni=dni)
        except ObjectDoesNotExist:
            dni_check = None

        if dni_check:
            raise forms.ValidationError("El usuario ya existe en el sistema")

        return dni

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            email_check = models.User.objects.get(email=email)
        except ObjectDoesNotExist:
            email_check = None

        if email_check:
            raise forms.ValidationError("El email ya existe en el sistema")

        return email

    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if len(password1) < 8:
            raise forms.ValidationError(
                "La contraseña ha de tener 8 o más caracteres")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden")

        return self.cleaned_data
