#encodinf:utf-8
from django.conf.urls import patterns, include, url

#Importacions lloc Administrador
from django.contrib import admin
admin.autodiscover()

#Importacion lloc Web
from web import views

#Autentificacio
from django.contrib.auth.views import login, logout

urlpatterns = patterns('',
	#Web Projecte
	#Redireccionament a la pagina de benvinguda
	(r'^$',views.home),
	#Redireccionament a la pagina de nou usuari
	(r'^altausu/$', views.altausu),
	#redireccio cap a la sortida del sistema
	(r'^logout/$', views.salir),
	#redireccio cap a la pagina d'usuari
	(r'^usuari/', views.usuari),
	#redireccio cap a la pagina de crear carpetes
	(r'^carpeta/(?P<id_carpeta>\d+)/$', views.carpeta),
	#redireccio cap al metode d'insertar noves carpetes
	(r'^novacarpeta/(?P<id_carpeta>\d+)/$', views.novacarpeta),
	#redireccio cap al metode per baixar fitxers
	#(r'pujararxiu/(?P<carpeta>\d)/$', views.pujararxiu),
	#redireccio cap al metode per baixar fitxers
	#(r'^download/(?P<file>\d)/$', views.download),
)
