import csv
from .models import User
from django.core.exceptions import ValidationError


def import_csv(csv_file):
    reader = csv.reader(csv_file)
    for index, row in enumerate(reader):
        if row[8] == '':
            row[8] = None
        new_user = User(estado=row[2][:1], dni=row[3], apellido1=row[4], apellido2=row[5],
        nombre=row[6], email=row[7], telefono=row[8], titulacion=row[11])

        try:
            new_user.full_clean()
            new_user.save()
        except ValidationError as e:
            print "Error en linea", (index + 1)
            print e
