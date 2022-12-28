from django.db import models

# Create your models here. Estos modelos se aplican directamente a la base de datos.
class Usuario(models.Model):
    name = models.CharField(max_length=50)
    lastname = models.CharField(max_length=100)
    username = models.CharField(max_length=50, unique=True)
    email = models.CharField(max_length=50, unique=True)
    password = models.BinaryField()
    bank_account = models.CharField(max_length=20)



class Monedero(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField()
    limite = models.PositiveIntegerField()
    descuento = models.PositiveIntegerField()
