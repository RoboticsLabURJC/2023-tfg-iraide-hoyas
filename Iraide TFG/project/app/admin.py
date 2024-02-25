from django.contrib import admin
from .models import usuario, clase,actividad, ejercicio

# Register your models here.
admin.site.register(usuario)
admin.site.register(clase)
admin.site.register(ejercicio)
admin.site.register(actividad)