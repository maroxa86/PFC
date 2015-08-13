# Create your views here.

from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django import forms
from django.http import HttpResponse, HttpResponseRedirect

#Gestio d'usuaris
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

#Bases de Dades
from web.models import *
from django.contrib.auth.models import User

#Formularis
from web.forms import *

#Email
from django.core.mail import EmailMessage

#Conexio S3
from django.conf import settings
from boto.s3.connection import S3Connection
from boto.s3.key import Key

#############################
#							#
#	Pagina de benvinguda i	#
#	Login d'usuari			#
#							#
#############################

#Metode per mostrar la pagina de benvinguda
def home(request):
	if request.method == 'POST':
		formulari = AuthenticationForm(request.POST)
		if formulari.is_valid:
			usuari = request.POST['username']
			clau = request.POST['password']
			access = authenticate(username=usuari, password=clau)
			if access is not None:
				if access.is_active:
					login(request,access)
					return HttpResponseRedirect("/usuari/")
				else:
					return render_to_response('home.html', context_instance=RequestContext(request))
		else:
			return render_to_response('home.html', context_instance=RequestContext(request))
	else:
		formulari = AuthenticationForm()
	return render_to_response('home.html', {'formulari':formulari,}, context_instance=RequestContext(request))

#####################
#					#
#	Alta nou Usuari	#
#					#
#####################

#Metode per mostar la pagina per donar d'alta usuari
def altausu(request):

	usuari=''

	def store_in_S3(username):
		conn = S3Connection(settings.ACCESS_KEY, settings.PASS_KEY)
		b = conn.create_bucket(username)

	if request.method == 'POST':
		formulari = AltaForm(request.POST)
		if formulari.is_valid():
			usuari = formulari.cleaned_data['usuari']
			contrasenya = formulari.cleaned_data['contrasenya']
			repcontrasenya = formulari.cleaned_data['repcontrasenya']
			email = formulari.cleaned_data['email']
			repemail = formulari.cleaned_data['repemail']
			user = User.objects.create_user(
						username = usuari,
						email = email,
						password = contrasenya
					)
			#Marquem l'usuari com a actiu
			user.is_staff = True
			user.save()
			carpeta = Carpetes(
							Nom = user.username,
							Usuari = user,
						)
			carpeta.save()
			store_in_S3(user.username)
			return render_to_response('nouusu.html',{
								'usuari':usuari, 
							}, context_instance=RequestContext(request))
	else:
		formulari = AltaForm()
	return render_to_response('altausu.html', {
					'formulari':formulari, 
					'usuari':usuari,
				}, context_instance=RequestContext(request))

#####################
#					#
#	Logout usuari	#
#					#
#####################

#Metode per controlar la sortida d'un usuari
@login_required(login_url='/')
def salir(request):
	logout(request)
	#Torna a la pagina de benvinguda
	return HttpResponseRedirect("/")

#####################
#					#
#	Seccio d'usuari	#
#					#
#####################		

#Metode per mostrar la pagina pNrincipal del usuari
@login_required(login_url='/')
def usuari(request):
	#Comprobem que l'usuari ha entrar correctament
	usuari = User.objects.get(username=request.user.username)
	carpeta_usu= Carpetes.objects.get(Usuari=usuari.id, Nom = usuari.username)
	carpetes = Carpetes.objects.filter(Usuari=usuari.id, Pare = carpeta_usu.idCarpeta)
	return render_to_response('usuari.html', {'carpetes' : carpetes, 'id': carpeta_usu.idCarpeta}, context_instance=RequestContext(request))

#####################
#					#
#	Seccio Carpeta	#
#					#
#####################

#Metode per insertar una nova carpeta
@login_required(login_url='/')
def novacarpeta(request,id_carpeta):
	def error(pare):
		formulari = NovaCarpeta()
		return render_to_response('novacarpeta.html',{'pare':pare, 'formulari':formulari}, context_instance=RequestContext(request))
	#Comprobem que l'usuari existeix
	try:
		usuari = User.objects.get(username=request.user.username)
	except User.DoesNotExist:
		raise forms.ValidationError("L'usuari no existeix")
		error(request.POST['pare'])

	if request.method == 'POST':
		formulari = NovaCarpeta(request.POST)
		if formulari.is_valid:
			#Comprobem que la carpeta no existeixi
			try:
				carpeta = Carpetes.objects.get(
							Nom = request.POST['nom'], 
							Usuari= usuari, 
							Pare = request.POST['pare']
						)
			except Carpetes.DoesNotExist:
				carpeta = Carpetes(
							Nom = request.POST['nom'],
							Usuari = usuari,
							Pare = request.POST['pare']
						)
				carpeta.save()
				carpeta.Pare = request.POST['pare']
				carpeta.save()
				if usuari.id == carpeta.Pare:
					return HttpResponseRedirect("/usuari/")
				else:
					return HttpResponseRedirect("/carpeta/%d" % int(carpeta.Pare))

	else:
		formulari = NovaCarpeta()
		car_pare = Carpetes.objects.get(idCarpeta = id_carpeta)
		if usuari.id == car_pare.Pare:
			pare = 'usuari'
		else:
			pare = id_carpeta
		return render_to_response('novacarpeta.html',{'pare':pare, 'formulari':formulari}, context_instance=RequestContext(request))

#Metode per accedir a una carpeta
#Metode per accedir a una carpeta
@login_required(login_url='/')
def carpeta(request, id_carpeta):
	usuari = User.objects.get(username=request.user.username)
	car_usu = Carpetes.objects.get(Usuari = usuari.id, Nom = usuari.username)
	pare = Carpetes.objects.get(idCarpeta = id_carpeta)
	if pare.Pare == car_usu.idCarpeta:
		pare = 'usuari'
	carpetes = Carpetes.objects.filter(Pare = id_carpeta)

	return render_to_response('carpeta.html', {'id_carpeta' : id_carpeta, 'carpetes' : carpetes, 'pare' : pare}, context_instance=RequestContext(request))
				
