from django.contrib import admin

# Register your models here.

from .models import User, Centro

class UserAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido1', 'apellido2', 'dni', 'email', 'telefono',
    'centro_asignado', 'estado')
    list_filter = ['centro_asignado', 'titulacion', 'horario_asignado', 'estado']
    search_fields = ['nombre', 'apellido1', 'apellido2', 'dni', 'email', 'telefono']

class UserInline(admin.StackedInline):
    model = User
    extra = 0

class CentroAdmin(admin.ModelAdmin):
    inlines = [UserInline]

admin.site.register(User, UserAdmin)
admin.site.register(Centro, CentroAdmin)
