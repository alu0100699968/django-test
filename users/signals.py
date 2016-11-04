from django.db.models.signals import post_save, post_init
from django.contrib.auth.models import Group

from notifications.signals import notify
from . import models

print('SUP')
staff = Group.objects.get(name='staff')
def cambio_estado(sender, **kwargs):
    instance = kwargs.get('instance')
    created = kwargs.get('created')
    if instance.estado == 'A' and instance.prev_estado != 'A':
        print('AAAAAAAAHHHHH')
        notify.send(instance, recipient=staff, verb='ha pasado a estar asignado')

def recordar_estado(sender, **kwargs):
    instance = kwargs.get('instance')
    instance.prev_estado = instance.estado

post_save.connect(cambio_estado, sender=models.User)
post_init.connect(recordar_estado, sender=models.User)
