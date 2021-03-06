# coding=utf-8
import csv, pprint
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError

from . import models


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=30, widget=forms.TextInput(
        attrs={'class': 'form-control', 'name': 'username', 'style': 'margin-bottom:10px;', 'placeholder': 'Usuario'}))
    password = forms.CharField(label="Password", max_length=30, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'name': 'password', 'style': 'margin-bottom:10px;', 'placeholder': 'Contraseña'}))


class UploadCSVForm(forms.Form):
    csv_file_field = forms.FileField(label='Seleccione un fichero CSV',
                                     help_text='Se aceptan ficheros CSV que sigan el formato indicado.')

    def clean_csv_file_field(self):
        csv_file = self.cleaned_data.get('csv_file_field')
        if not csv_file.name.endswith('.csv'):
            raise ValidationError(u'Solo se aceptan ficheros CSV')
        reader = csv.reader(csv_file)
        new_users = []
        pp = pprint.PrettyPrinter(indent=4)
        if new_users:
            print("Esto no deberia verse NUNCA")
        for index, row in enumerate(reader):
            if not row[8]:
                row[8] = None
            new_user = models.User(estado=row[2][:1], dni=row[3], apellido1=row[4], apellido2=row[5],
                                   nombre=row[6], email=row[7], telefono=row[8], titulacion=row[11])

            try:
                new_user.full_clean()
                new_user.save()
            except ValidationError as e:
                print "Error en linea", (index + 1)
                # print e.error_dict[0]
                new_users.append("Error en linea " +
                                 str(index + 1) + ": " + pp.pformat(e.error_dict))
        if new_users:
            raise forms.ValidationError(new_users)
        return csv_file


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
