from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from user_app.models import Account

# Create your models here.
class Empresa(models.Model):
    nombre = models.CharField(max_length=250)
    website = models.URLField(max_length=250)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre #MOSTRAMOS LA DIRECCIÓN EN LA TABLA DE REGISTROS DE LA BASE DE DATOS DEL ADMINISTRADOR



class Edificacion(models.Model):
    direccion = models.CharField(max_length=250)
    pais = models.CharField(max_length=150)
    descripcion = models.CharField(max_length=500)
    imagen = models.CharField(max_length=900)
    active = models.BooleanField(default=True)
    avg_calificacion = models.FloatField(default=0)
    number_calificacion = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='edificacionList')

    def __str__(self):
        return self.direccion #MOSTRAMOS LA DIRECCIÓN EN LA TABLA DE REGISTROS DE LA BASE DE DATOS DEL ADMINISTRADOR


class Comentario(models.Model):
    comentario_user =  models.ForeignKey(Account, on_delete=models.CASCADE) #USUARIO QUE CREA CADA COMENTARIO
    calificacion = models.PositiveBigIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    texto = models.CharField(max_length=200, null=True)
    edificacion = models.ForeignKey(Edificacion, on_delete=models.CASCADE, related_name='comentarios')
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.calificacion) + ' ' + self.edificacion.direccion