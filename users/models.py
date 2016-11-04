#coding=utf-8
from __future__ import unicode_literals

from django.db import models
from django.core.exceptions import ValidationError
from django.core import validators
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from django.contrib.auth.models import Group
from django.db.models.signals import post_save, post_init

from notifications.signals import notify

def dni_validator(dni):
    if len(dni) == 8:
        if (dni[0].isalpha() and dni[1:].isdigit()) or dni.isdigit():
            return
    raise ValidationError(
        _('Introduzca un DNI válido'),
        params={'value': dni},
    )

def telefono_validator(telefono):
    if len(str(telefono)) != 9:
        raise ValidationError(
            _('Introduzca un número de teléfono válido'),
            params={'value': telefono},
        )

# Se almacena el grupo staff en una variable para poder enviarle notificaciones
staff = Group.objects.get(name='staff')

# Create your models here.

class Centro(models.Model):
    nombre = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre

class User(models.Model):
    regex = r'^(?i)([a-zñáéíóú]{2,60})$'
    ESTADOS = (
        ('A', 'Asignado'),
        ('S', 'Suplente'),
        ('R', 'Renuncia'),
        ('E', 'Excluido'),
        ('N', 'No asignado')
    )
    HORARIOS = (
        ('M', 'Mañana'),
        ('T', 'Tarde'),
        ('N', 'No asignado'),
    )
    nombre = models.CharField(max_length=200,
        validators=[validators.RegexValidator(regex)])
    apellido1 = models.CharField(max_length=200)
    apellido2 = models.CharField(max_length=200)
    dni = models.CharField(primary_key=True, validators=[dni_validator],
        max_length=8)
    estado = models.CharField(max_length=1, choices=ESTADOS, default='N')
    titulacion = models.CharField(max_length=200)
    centro_asignado = models.ForeignKey(Centro, on_delete=models.SET_NULL,
        blank=True, null=True)
    horario_asignado = models.CharField(max_length=1, choices=HORARIOS,
        default="N")
    email = models.EmailField(unique=True)
    telefono = models.PositiveIntegerField(validators=[telefono_validator])

    #para redirigir al crear o editar un usuario en un form
    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.nombre + ' ' + self.apellido1 + ' ' + self.apellido2

    def __unicode__(self):
        return self.nombre + ' ' + self.apellido1 + ' ' + self.apellido2

    @staticmethod
    def cambio_estado(sender, **kwargs):
        instance = kwargs.get('instance')
        created = kwargs.get('created')
        if instance.estado == 'A' and instance.prev_estado != 'A':
            print('AAAAAAAAHHHHH')
            notify.send(instance, recipient=staff, verb='ha pasado a estar asignado')

    @staticmethod
    def recordar_estado(sender, **kwargs):
        instance = kwargs.get('instance')
        instance.prev_estado = instance.estado

post_save.connect(User.cambio_estado, sender=User)
post_init.connect(User.recordar_estado, sender=User)
