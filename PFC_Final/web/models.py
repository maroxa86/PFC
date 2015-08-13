#encoding:utf-8

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Carpetes(models.Model):
	idCarpeta = models.AutoField(primary_key=True)
	Nom = models.CharField(max_length=45)
	Usuari = models.ForeignKey(User)
	Pare = models.IntegerField(null=True)

	def __unicode__(self):
		return self.Nom

class Fitxers(models.Model):
	idFitxers = models.AutoField(primary_key=True)
	Nom = models.CharField(max_length=45)
	Tamany = models.IntegerField()
	Modificacio = models.DateField()

	def __unicode__(self):
		return self.Nom

class Amics(models.Model):
	idUsuari1 = models.ManyToManyField(User,related_name='usuari')
	idUsuari2 = models.ManyToManyField(User,related_name='amic')
	confirmacio = models.BooleanField()

class Comparteix(models.Model):
	idUsuari1 = models.ManyToManyField(User,related_name='propietari')
	idUsuari2 = models.ManyToManyField(User,related_name='receptor')
	idCarpeta = models.ManyToManyField(Carpetes,related_name='carpeta')

class Conte(models.Model):
	idCarpeta = models.ManyToManyField(Carpetes,related_name='contenidor')
	idFitxers = models.ManyToManyField(Fitxers,related_name='contingut')
