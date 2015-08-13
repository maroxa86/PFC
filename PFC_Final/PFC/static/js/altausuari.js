ok_usuari = false;
ok_passwd1 = false;
ok_passwd2 = false;
ok_repemail = false;
ok_email = false;

//funcio per validar formulari
function validar(){
	if(ok_usuari && ok_passwd1 && ok_passwd2 && ok_email && ok_repemail){
		return true
	}
	else{
		return false
	}
}

//funcio per activar boto alta usuari
function boto_ok(boto){
	if(ok_usuari && ok_passwd1 && ok_passwd2 && ok_email && ok_repemail){
		boto.disabled=false
	}
	else{
		boto.disabled=true
	}
}

//funcions per comprobar si existeix un usuari
function comp_usuari(){
	usu = document.altausuari.usuari.value;
	ok_usuari=true;
	boto_ok(document.getElementById('alta'));
}

function error_usuari_mostrar(){
	document.getElementById('missatge_error_usuari').style.visibility='visible';
}

function error_usuari_ocultar(){
	document.getElementById('missatge_error_usuari').style.visibility='hidden';
}


//funcions per comprobar si la longitud de la contrasenya es correcta
function comp_contra(){
	cont = document.altausuari.contrasenya.value;

	if (cont.length < 6 || cont.length > 12){
		document.getElementById('contrasenya_error').style.visibility='visible';
		document.getElementById('contrasenya_ok').style.visibility='hidden';
		ok_passwd1=false
	}
	else{
		document.getElementById('contrasenya_error').style.visibility='hidden';
		document.getElementById('contrasenya_ok').style.visibility='visible';
		ok_passwd1=true	
	}
	boto_ok(document.getElementById('alta'));
}

function error_contrasenya_mostrar(){
	document.getElementById('missatge_error_contrasenya').style.visibility='visible';
}

function error_contrasenya_ocultar(){
	document.getElementById('missatge_error_contrasenya').style.visibility='hidden';
}

//funcions per comprobar que les contrasenyes coincideixen
function comp_repcontra(){
	cont = document.altausuari.contrasenya.value;
	repcont = document.altausuari.repcontrasenya.value;

	if (cont != repcont){
		document.getElementById('repcontrasenya_error').style.visibility='visible';
		document.getElementById('repcontrasenya_ok').style.visibility='hidden';
		ok_passwd2 = false;
	}
	else{
		document.getElementById('repcontrasenya_error').style.visibility='hidden';
		document.getElementById('repcontrasenya_ok').style.visibility='visible';	
		ok_passwd2 = true;
	}
	boto_ok(document.getElementById('alta'));

}

function error_repcontrasenya_mostrar(){
	document.getElementById('missatge_error_repcontrasenya').style.visibility='visible';
}

function error_repcontrasenya_ocultar(){
	document.getElementById('missatge_error_repcontrasenya').style.visibility='hidden';
}

//funcions per comprobar que email ha estat introduit correctament
function comp_email() {
	email = document.altausuari.email.value;
	emailExp = /^[a-zA-Z]\w*([.-]?\w+)*@[a-zA-Z0-9]\w*([.-]?\w+)*\.[a-zA-Z]{2,3}$/	
	
	if (email.search(emailExp) == -1){	
		ok_email = false;
		document.getElementById('email_error').style.visibility='visible';
		document.getElementById('email_ok').style.visibility='hidden';
	}else{
		ok_email = true;
		document.getElementById('email_error').style.visibility='hidden';
		document.getElementById('email_ok').style.visibility='visible';
	}
	boto_ok(document.getElementById('alta'));
}


function error_email_mostrar(){
	document.getElementById('missatge_error_email').style.visibility='visible';
}

function error_email_ocultar(){
	document.getElementById('missatge_error_email').style.visibility='hidden';
}

//funcions per comprobar que els emails coincideixen
function comp_repemail() {
	email = document.altausuari.email.value;
	repemail = document.altausuari.repemail.value;

	if (email != repemail){
		document.getElementById('repemail_error').style.visibility='visible';
		document.getElementById('repemail_ok').style.visibility='hidden';
		ok_repemail = false;
	}
	else{
		document.getElementById('repemail_error').style.visibility='hidden';
		document.getElementById('repemail_ok').style.visibility='visible';	
		ok_repemail = true;
	}
	boto_ok(document.getElementById('alta'));
}


function error_repemail_mostrar(){
	document.getElementById('missatge_error_repemail').style.visibility='visible';
}

function error_repemail_ocultar(){
	document.getElementById('missatge_error_repemail').style.visibility='hidden';
}
