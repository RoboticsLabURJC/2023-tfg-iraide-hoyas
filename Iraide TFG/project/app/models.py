from django.db import models

# Create your models here.
class usuario(models.Model):
    nombre = models.CharField(max_length=20)
    edad = models.IntegerField()
    pais = models.CharField(max_length=20)
    sexo = models.CharField(max_length=20)
    so = models.CharField(max_length=20)
