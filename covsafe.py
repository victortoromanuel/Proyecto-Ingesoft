import time
import datetime
import qrcode
import os, os.path
import base64
import sys
import pandas as pd
from pandas import ExcelWriter
import numpy as np
import cv2
from PIL import Image
from flask import Flask, redirect, url_for, render_template, request, flash, send_file, send_from_directory
from werkzeug.utils import secure_filename
from pymongo import MongoClient
from mongoFunctions import *

#C:/Users/Victor Toro/Documents/Proyecto Ingesoft AWS/ingesoft/static/archivosRUT/

UPLOAD_FOLDER = "/home/ubuntu/reportedos/Proyecto-Ingesoft/ingesoft/static/leerCodigosQR/"
UPLOAD_FOLDER2 = "/home/ubuntu/reportedos/Proyecto-Ingesoft/ingesoft/static/archivosRUT/"
UPLOAD_FOLDER3 = "/home/ubuntu/reportedos/Proyecto-Ingesoft/ingesoft/static/excel/"
#@login_required

app = Flask(__name__, static_folder="static", template_folder="templates")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOAD_FOLDER2'] = UPLOAD_FOLDER2
app.config['UPLOAD_FOLDER3'] = UPLOAD_FOLDER3
#app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.secret_key = 'secreto'

@app.route('/')
def inicio():
	return render_template('inicio.html')


@app.after_request
def add_header(response):
	# response.cache_control.no_store = True
	if 'Cache-Control' not in response.headers:
		response.headers['Cache-Control'] = 'no-store'
	return response


@app.route('/iniciarS')
def iniciarS():
	return render_template('iniciarS.html')

@app.route('/registrar')
def registrar():
	return render_template('registrar.html', tipo=['Ciudadano', 'Establecimiento', 'Entidad de salud'])

@app.route('/registroCiudadano')
def registroCiudadano():
	return render_template('registroCiudadano.html')

@app.route('/registroEstablecimiento')
def registroEstablecimiento():
	return render_template('registroEstablecimiento.html')

@app.route('/categorias')
def categorias(data):
	return render_template('categorias.html', data)

@app.route('/categoriasID/<Id>')
def categoriasID(Id):
	data = [[],[]]
	adm = Admin.find_one({"_id":Id})
	data[0].append(adm["Usuario"])
	data[0].append(adm["_id"])
	cat = Categoria.find({})
	for c in cat:
		data[1].append([c["_id"], c["Nombre"]])
	return render_template('categorias.html', data = data)

@app.route('/aceptarCierre/<nit>/<Id>')
def aceptarCierre(nit, Id):
	#sol = Solicitud.find_one({"_id":nit})
	Solicitud.delete_one({"_id":nit})
	Establecimiento.update_one({"_id":nit}, {"$set": {"Usuario":"","Contraseña":""}})
	flash("Establecimiento cerrado satisfactoriamente")
	return redirect('/aprobacionCierreID/' + Id)

@app.route('/denegarCierre/<nit>/<Id>')
def denegarCierre(nit, Id):
	#sol = Solicitud.find_one({"_id":nit})
	Solicitud.delete_one({"_id":nit})
	#Establecimiento.update_one({"_id":nit, "Usuario":"", "Contraseña":""})
	flash("Solicitud de cierre de establecimiento denegada")
	return redirect('/aprobacionCierreID/' + Id)

@app.route('/aceptar/<nit>/<Id>')
def aceptar(nit, Id):
	est = Solicitud.find_one({"_id":nit})
	if est["Categoría"][0] == 1:
		neg = jsonToList2(est)
		insertSalud(neg)
		flash("Entidad de salud registrada satisfactoriamente")
	else:
		neg = jsonToList2(est)
		insertEstablecimiento(neg)
		flash("Establecimiento registrada satisfactoriamente")
	Solicitud.delete_one({"_id":nit})
	return redirect('/aprobacionAperturaID/' + Id)

@app.route('/denegar/<nit>/<Id>')
def denegar(nit, Id):
	est = Solicitud.find_one({"_id":nit})
	if est["Categoría"][0] == 1:
		flash("Entidad de salud rechazada satisfactoriamente")
	else:
		flash("Establecimiento rechazado satisfactoriamente")
	Solicitud.delete_one({"_id":nit})
	return redirect('/aprobacionAperturaID/' + Id)

@app.route('/aprobacionApertura')
def aprobacionApertura(data):
	return render_template('aprobacionApertura.html', data)

@app.route('/aprobacionAperturaID/<Id>')
def aprobacionAperturaID(Id):
	data = [[],[]]
	adm = Admin.find_one({"_id":Id})
	data[0].append(adm["Usuario"])
	data[0].append(adm["_id"])
	sol = Solicitud.find({"Solicitud":"Registro"})
	for s in sol:
		data[1].append([s["_id"], s["Razón_social"], s["Categoría"], s["Correo"]])
	print(data)
	return render_template('aprobacionApertura.html', data = data)

@app.route('/aprobacionCierre')
def aprobacionCierre(data):
	return render_template('aprobacionCierre.html', data)

@app.route('/aprobacionCierreID/<Id>')
def aprobacionCierreID(Id):
	data = [[],[]]
	adm = Admin.find_one({"_id":Id})
	data[0].append(adm["Usuario"])
	data[0].append(adm["_id"])
	sol = Solicitud.find({"Solicitud":"Eliminar"})
	for s in sol:
		data[1].append([s["_id"], s["Razón_social"], s["Categoría"], s["Correo"]])
	print(data)
	return render_template('aprobacionCierre.html', data = data)

@app.route('/aprobacionSolicitudes')
def aprobacionSolicitudes(data):
	return render_template('aprobacionSolicitudes.html', data)

@app.route('/aprobacionSolicitudesID/<Id>')
def aprobacionSolicitudesID(Id):
	data = [[]]
	adm = Admin.find_one({"_id":Id})
	data[0].append(adm["Usuario"])
	data[0].append(adm["_id"])
	return render_template('aprobacionSolicitudes.html', data = data)

@app.route('/seleccionarSolicitud/<Id>', methods=['POST'])
def seleccionarSolicitud(Id):
	if request.method == 'POST':
		select = request.form.get("tipo")
		if select == 'Nuevo negocio/entidad': select = 'AperturaID/'
		elif select == 'Cierre de negocio/entidad': select = 'CierreID/'
	redir = '/aprobacion' + select + Id
	adm = Admin.find_one({"_id":Id})
	data = [[]]
	data[0].append(adm["Usuario"])
	data[0].append(adm["_id"])
	return redirect(redir)

@app.route('/reportesCiudadano')
def reportesCiudadano(data):
	return render_template('reportesCiudadano.html', data)

@app.route('/reportesCiudadanoID/<Id>')
def reportesCiudadanoID(Id):
	ciud = Ciudadano.find_one({"_id":Id})
	data = [ciud["Usuario"], ciud["_id"]]
	data = [data]
	return render_template('reportesCiudadano.html', data = data)

@app.route('/reporteVisitasCiudadano')
def reporteVisitasCiudadano(data):
	return render_template('reporteVisitasCiudadano.html', data)

@app.route('/reporteVisFechaCiudadano')
def reporteVisFechaCiudadano(data):
	return render_template('reporteVisFechaCiudadano.html', data)

@app.route('/reporteVisFechaHoraCiudadano')
def reporteVisFechaHoraCiudadano(data):
	return render_template('reporteVisFechaHoraCiudadano.html', data)

@app.route('/reporteExamenesCiudadano')
def reporteExamenesCiudadano(data):
	return render_template('reporteExamenesCiudadano.html', data)

@app.route('/agregarVisita')
def agregarVisita(data):
	return render_template('agregarVisita.html', data)

@app.route('/agregarVisitaNIT/<nit>')
def agregarVisitaNIT(nit):
	est = Establecimiento.find_one({"_id":nit})
	data = [est["Usuario"], est["_id"]]
	data = [data]
	return render_template('agregarVisita.html', data = data)

@app.route('/reportesEstablecimiento')
def reportesEstablecimiento(data):
	return render_template('reportesEstablecimiento.html', data)

@app.route('/reportesEstablecimientoNIT/<nit>')
def reportesEstablecimientoNIT(nit):
	est = Establecimiento.find_one({"_id":nit})
	data = [est["Usuario"], est["_id"]]
	data = [data]
	return render_template('reportesEstablecimiento.html', data = data)

@app.route('/reporteVisitasEstablecimiento')
def reporteVisitasEstablecimiento(data):
	return render_template('reporteVisitasEstablecimiento.html', data)

@app.route('/reporteFechaEstablecimiento')
def reporteFechaEstablecimiento(data):
	return render_template('reporteFechaEstablecimiento.html', data)

@app.route('/reporteFechaHoraEstablecimiento')
def reporteFechaHoraEstablecimiento(data):
	return render_template('reporteFechaHoraEstablecimiento.html', data)

@app.route('/reporteDocumentoEstablecimiento')
def reporteDocumentoEstablecimiento(data):
	return render_template('reporteDocumentoEstablecimiento.html', data)

@app.route('/reporteNombresEstablecimiento')
def reporteNombresEstablecimiento(data):
	return render_template('reporteNombresEstablecimiento.html', data)

@app.route('/reporteApellidoEstablecimiento')
def reporteApellidoEstablecimiento(data):
	return render_template('reporteApellidoEstablecimiento.html', data)

@app.route('/usrEstablecimiento')
def usrEstablecimiento(data):
	return render_template('usrEstablecimiento.html', data)

@app.route('/usrEstablecimientoNIT/<nit>')
def usrEstablecimientoNIT(nit):
	est = Establecimiento.find_one({"_id":nit})
	data = [est["Usuario"], est["_id"]]
	data = [data]
	print(data)
	return render_template('usrEstablecimiento.html', data = data)

@app.route('/cierreEstablecimiento')
def cierreEstablecimiento(data):
	return render_template('cierreEstablecimiento.html', data)

@app.route('/cierreEstablecimientoNIT/<nit>')
def cierreEstablecimientoNIT(nit):
	est = Establecimiento.find_one({"_id":nit})
	data = [est["Usuario"], est["_id"]]
	data = [data]
	return render_template('cierreEstablecimiento.html', data = data)

@app.route('/registroSalud')
def registroSalud():
	return render_template('registroSalud.html')

@app.route('/reportesSalud')
def reportesSalud(data):
	return render_template('reportesSalud.html', data)

@app.route('/reportesSaludNIT/<nit>')
def reportesSaludNIT(nit):
	sal = Salud.find_one({"_id":nit})
	data = [sal["Usuario"], sal["_id"]]
	data = [data]
	return render_template('reportesSalud.html', data = data)

@app.route('/reporteExamenesSalud')
def reporteExamenesSalud(data):
	return render_template('reporteExamenesSalud.html', data)

@app.route('/reporteFechaSalud')
def reporteFechaSalud(data):
	return render_template('reporteFechaSalud.html', data)

@app.route('/reporteEstadoSalud')
def reporteEstadoSalud(data):
	return render_template('reporteEstadoSalud.html', data)

@app.route('/registroExamen')
def registroExamen(data):
	return render_template('registroExamen.html', data)

@app.route('/registroExamenNIT/<nit>')
def registroExamenNIT(nit):
	sal = Salud.find_one({"_id":nit})
	data = [sal["Usuario"], sal["_id"]]
	data = [data]
	return render_template('registroExamen.html', data = data)

@app.route('/registrarExamenNIT/<nit>', methods=['POST'])
def registrarExamenNIT(nit):
	if request.method == 'POST':
		tipodoc = request.form.get("tipo")
		doc = request.form.get("inputNumDoc")
		resultado = request.form.get("resultado")
		fecha = request.form.get("birthday")
		dias = request.form.get("dias")
		usr = Ciudadano.find_one({"_id":doc})
		ingresar = True
		if usr != None:
			if usr["Tipo_documento"] != tipodoc or usr["_id"] != doc:
				ingresar = False
		else:
			ingresar = False

		if ingresar:
			nro = Examen.count_documents({})
			nro += 1
			exa = [nro, tipodoc, doc, nit, resultado, fecha, dias]
			insertExamen(exa)
			flash('*Exámen registrado satisfactoriamente')
		else:
			flash('*La persona no está registrada en el sistema')
	sal = Salud.find_one({"_id":nit})
	data = [sal["Usuario"], sal["_id"]]
	data = [data]
	redir = '/registroExamenNIT/'+nit
	return redirect(redir)

@app.route('/codigoQR')
def codigoQR(data):
	return render_template('codigoQR.html', data)

@app.route('/infoCiudadano')
def infoCiudadano(data):
	#print(data)
	return render_template('infoCiudadano.html', data)

@app.route('/infoEstablecimiento')
def infoEstablecimiento(data):
	return render_template('infoEstablecimiento.html', data)

@app.route('/infoSalud')
def infoSalud(data):
	return render_template('infoSalud.html', data)

@app.route('/reportesAdministrador')
def reportesAdministrador(data):
	return render_template('reportesAdministrador.html', data)

@app.route('/reportesAdministradorID/<Id>')
def reportesAdministradorID(Id):
	adm = Admin.find_one({"_id":Id})
	data = [adm["Usuario"], adm["_id"]]
	data = [data]
	return render_template('reportesAdministrador.html', data = data)

@app.route('/reporteGeneroAdministrador')
def reporteGeneroAdministrador(data):
	return render_template('reporteGeneroAdministrador.html', data)

@app.route('/reporteCategoriaAdministrador')
def reporteCategoriaAdministrador(data):
	return render_template('reporteCategoriaAdministrador.html', data)

@app.route('/reporteEstablecimientoAdministrador')
def reporteEstablecimientoAdministrador(data):
	return render_template('reporteEstablecimientoAdministrador.html', data)

@app.route('/reporteExamenesAdministrador')
def reporteExamenesAdministrador(data):
	return render_template('reporteExamenesAdministrador.html', data)

@app.route('/reporteDocumentoAdministrador')
def reporteDocumentoAdministrador(data):
	return render_template('reporteDocumentoAdministrador.html', data)

@app.route('/reporteFechaHoraAdministrador')
def reporteFechaHoraAdministrador(data):
	return render_template('reporteFechaHoraAdministrador.html', data)
"""
@app.route('/reporteGeneroAdministradorID/<Id>')
def reporteGeneroAdministradorID(Id):
	adm = Admin.find_one({"_id":Id})
	data = [adm["Usuario"], adm["_id"]]
	data = [data]
	return render_template('reporteGeneroAdministrador.html', data = data)
"""
@app.route('/infoAdministrador')
def infoAdministrador(data):
	return render_template('infoAdministrador.html', data)

@app.route('/registroAdministrador')
def registroAdministrador(data):
	return render_template('registroAdministrador.html', data)

@app.route('/registroAdministradorID/<Id>')
def registroAdministradorID(Id):
	adm = Admin.find_one({"_id":Id})
	data = [adm["Usuario"], adm["_id"]]
	data = [data]
	return render_template('registroAdministrador.html', data = data)

@app.route('/regDatosAdmin/<Id>', methods=['GET', 'POST'])
def regDatosAdmin(Id):
	nombre = request.form.get("inputNom")
	apellido = request.form.get("inputAp")
	tipodoc = request.form.get("tipo")
	doc = request.form.get("inputNumDoc")
	usuario = request.form.get("inputUsr")
	contra = request.form.get("inputPassword")
	datos = [doc, nombre, apellido, tipodoc, usuario, contra]
	insertAdmin(datos)
	flash("*Administrador registrado satisfactoriamente")
	adm = Admin.find_one({"_id":Id})
	adm = orderAdmin(adm)
	data = jsonToList(adm)
	return render_template('/infoAdministrador.html', data = data)

@app.route('/regDatosCiudadano', methods=['GET', 'POST'])
def regDatosCiudadano():
	nombre = request.form.get("inputNom")
	apellido = request.form.get("inputAp")
	tipodoc = request.form.get("tipoDoc")
	doc = request.form.get("inputNumDoc")
	contacto = request.form.get("inputNum")
	genero = request.form.get("tipoGen")
	correo = request.form.get("inputemail")
	fecha = request.form.get("birthday")
	departamento = request.form.get("inputDepart")
	municipio = request.form.get("inputMuni")
	barrio = request.form.get("inputState")
	direccion = request.form.get("inputAddress")
	usuario = request.form.get("inputUsr")
	contra = request.form.get("inputPassword")
	datos = [doc, nombre, apellido, tipodoc, genero, fecha, correo, contacto, departamento, municipio, barrio, direccion, usuario, contra]
	insertCiudadano(datos)
	flash('*Registrado satisfactoriamente')
	return redirect('/iniciarS')

@app.route('/regDatosEstablecimiento', methods=['POST'])
def regDatosEstablecimiento():
	razon = request.form.get("inputNom")
	nit = request.form.get("inputAp")
	categoria = request.form.get("tipo")
	contacto = request.form.get("inputNumDoc")
	correo = request.form.get("inputemail")
	departamento = request.form.get("inputDepart")
	municipio = request.form.get("inputMuni")
	barrio = request.form.get("inputState")
	direccion = request.form.get("inputAddress")
	usuario = request.form.get("inputUsr")
	contra = request.form.get("inputPassword")
	file = request.files['file']
	filename = nit + 'RUT.png'
	file.save(os.path.join(app.config['UPLOAD_FOLDER2'], filename))
	cate = Categoria.find_one({"Nombre": categoria})
	cate = jsonToList2(cate)
	datos = [nit, razon, cate, correo, contacto, departamento, municipio, barrio, direccion, usuario, contra, "Registro"]	
	insertSolicitud(datos)
	flash('*Solicitud de registro enviada')
	#datos = [nit, razon, cate, correo, contacto, departamento, municipio, barrio, direccion, usuario, contra, " "]	
	#insertEstablecimiento(datos)
	return redirect('/iniciarS')

@app.route('/regDatosSalud', methods=['POST'])
def regDatosSalud():
	razon = request.form.get("inputNom")
	nit = request.form.get("inputAp")
	categoria = request.form.get("tipo")
	contacto = request.form.get("inputNumDoc")
	correo = request.form.get("inputemail")
	departamento = request.form.get("inputDepart")
	municipio = request.form.get("inputMuni")
	barrio = request.form.get("inputState")
	direccion = request.form.get("inputAddress")
	usuario = request.form.get("inputUsr")
	contra = request.form.get("inputPassword")
	file = request.files['file']
	filename = nit + 'RUT.png'
	file.save(os.path.join(app.config['UPLOAD_FOLDER2'], filename))
	cate = Categoria.find_one({"Nombre": categoria})
	cate = jsonToList2(cate)
	datos = [nit, razon, cate, correo, contacto, departamento, municipio, barrio, direccion, usuario, contra, "Registro"]	
	insertSolicitud(datos)
	flash('*Solicitud de registro enviada')
	#datos = [nit, razon, cate, correo, contacto, departamento, municipio, barrio, direccion, usuario, contra, " "]	
	#insertSalud(datos)
	return redirect('/iniciarS')

#Selecciona tipo de registro (por rol)
@app.route('/seleccionarTipo', methods=['GET', 'POST'])
def seleccionarTipo():
	select = request.form.get("tipo")
	if select == 'Entidad de salud': select = 'Salud'
	select = 'registro' + select
	return redirect(url_for(select))

@app.route('/ingresar', methods=['GET', 'POST'])
def ingresar():
	usuario = request.form.get("usr")
	contra = request.form.get("answ")
	select = request.form.get("tipoUsr")
	select = str(select)
	redir = 'info'
	if select == 'Ciudadano':
		usr = Ciudadano.find_one({"Usuario":usuario, "Contraseña":contra})
		if usr != None:
			redir += str(select) + '.html'
			usr = orderCiudadano(usr)
			data = jsonToList(usr)
		else:
			flash("No estás registrado o tus datos no coinciden")
			redir = "iniciarS.html"
			return render_template(redir)

	elif select == 'Establecimiento':
		est = Establecimiento.find_one({"Usuario":usuario, "Contraseña":contra})
		if est != None:
			redir += str(select) + '.html'
			est = orderEstablecimiento(est)
			data = jsonToList(est)
			##Categoria
		else:
			flash("No estás registrado o tus datos no coinciden")
			redir = "iniciarS.html"
			return render_template(redir)

	
	elif select == 'Entidad de salud':
		select = 'Salud'
		sal = Salud.find_one({"Usuario":usuario, "Contraseña":contra})
		if sal != None:
			redir += str(select) + '.html'
			sal = orderSalud(sal)
			data = jsonToList(sal)
			##Categori
		else:
			flash("No estás registrado o tus datos no coinciden")
			redir = "iniciarS.html"
			return render_template(redir)

	elif select == 'Administrador':
		adm = Admin.find_one({"Usuario":usuario, "Contraseña":contra})
		if adm != None:
			redir += str(select) + '.html'
			adm = orderAdmin(adm)
			data = jsonToList(adm)
		else:
			flash("No estás registrado o tus datos no coinciden")
			redir = "iniciarS.html"
			return render_template(redir)


	return render_template(redir, data = data)

@app.route('/modInfoAdmin/<Id>', methods=['GET', 'POST'])
def modInfoAdmin(Id):
	if request.method == 'POST':
		contra = request.form.get("inputPassword")
		Admin.update_one({"_id": Id}, {"$set": {"Contraseña":contra}})
		flash('*Información modificada')
	adm = Admin.find_one({"_id": Id})
	adm = orderAdmin(adm)
	data = jsonToList(adm)
	return render_template('/infoAdministrador.html', data = data)

@app.route('/modInfoCiudadano/<Id>', methods=['GET', 'POST'])
def modInfoCiudadano(Id):
	if request.method == 'POST':
		nombre = request.form.get('inputNom')
		apellido = request.form.get("inputAp")
		contacto = request.form.get("inputNum")
		genero = request.form.get("tipoGen")
		correo = request.form.get("inputemail")
		contra = request.form.get("inputPassword")
		departamento = request.form.get("inputDepart")
		municipio = request.form.get("inputMuni")
		barrio = request.form.get("inputBarrio")
		direccion = request.form.get("inputAddress")
		cedula = request.form.get("cedula")
		ciud = [nombre, apellido, correo, contacto, departamento, municipio, barrio, direccion, contra]
		updateCiudadano(Id, ciud)
		flash('*Información modificada')
	usr = Ciudadano.find_one({"_id":Id})
	usr = orderCiudadano(usr)
	data = jsonToList(usr)
	return render_template('/infoCiudadano.html', data = data)

@app.route('/modInfoEstablecimiento/<Id>', methods=['GET', 'POST'])
def modInfoEstablecimiento(Id):
	if request.method == 'POST':
		razon = request.form.get("inputNom")
		nit = request.form.get("inputAp")
		categoria = request.form.get("tipo")
		contacto = request.form.get("inputNumDoc")
		correo = request.form.get("inputemail")
		departamento = request.form.get("inputDepart")
		municipio = request.form.get("inputMuni")
		barrio = request.form.get("inputState")
		direccion = request.form.get("inputAddress")
		usuario = request.form.get("inputUsr")
		contra = request.form.get("inputPassword")
		cate = Categoria.find_one({"Nombre": categoria})
		cate = jsonToList2(cate)
		est = [razon, correo, contacto, departamento, municipio, barrio, direccion, contra]
		updateEstablecimiento(Id, est)
		flash('*Información modificada')
	newdata = Establecimiento.find_one({"_id":Id})
	newdata = orderEstablecimiento(newdata)
	data = jsonToList(newdata)
	return render_template('/infoEstablecimiento.html', data = data)

@app.route('/modInfoSalud/<Id>', methods=['GET', 'POST'])
def modInfoSalud(Id):
	if request.method == 'POST':
		razon = request.form.get("inputNom")
		nit = request.form.get("inputAp")
		categoria = request.form.get("tipo")
		contacto = request.form.get("inputNumDoc")
		correo = request.form.get("inputemail")
		departamento = request.form.get("inputDepart")
		municipio = request.form.get("inputMuni")
		barrio = request.form.get("inputState")
		direccion = request.form.get("inputAddress")
		usuario = request.form.get("inputUsr")
		contra = request.form.get("inputPassword")
		cate = Categoria.find_one({"Nombre": categoria})
		cate = jsonToList2(cate)
		sal = [razon, correo, contacto, departamento, municipio, barrio, direccion, contra]
		updateSalud(Id, sal)
		flash('*Información modificada')
	newdata = Salud.find_one({"_id":Id})
	newdata = orderSalud(newdata)
	data = jsonToList(newdata)
	return render_template('/infoSalud.html', data = data)

@app.route('/img/<img_id>')
def serve_img(img_id):
	return redirect(url_for('/home/ubuntu/reportedos/Proyecto-Ingesoft/ingesoft/codigosQR/', download=img_id), code=301)

@app.route('/genCodigoQR/<Id>')
def genCodigoQR(Id):
	data = Ciudadano.find_one({"_id":Id})
	newdata = [data["Usuario"], data["_id"]]
	value = Id + '.PNG'
	newdata.append(value)
	tipodoc = data["Tipo_documento"]
	data = newdata

	qr = qrcode.QRCode(
		version = 1,
		error_correction = qrcode.constants.ERROR_CORRECT_H,
		box_size = 10,
		border = 4
	)

	info = [tipodoc, Id]
	qr.add_data(info)
	qr.make(fit=True)
	imagen = qr.make_image()
	dir_path = "/home/ubuntu/reportedos/Proyecto-Ingesoft/ingesoft/static/codigosQR/" + str(Id) + ".PNG"
	#dir_path = "C:/Users/Victor Toro/Documents/Proyecto Ingesoft AWS/ingesoft/static/codigosQR/" + str(Id) + ".PNG" 
	imagen.save(dir_path, 'PNG')
	return render_template('/codigoQR.html', data = data)

@app.route('/ingresoDestiempo/<nit>', methods=['POST'])
def ingresoDestiempo(nit):
	tipodoc = request.form.get("tipo")
	doc = request.form.get("inputNumDoc")
	temperatura = request.form.get("inputTemp")
	temperatura = float(temperatura)
	tapabocas = request.form.get("inputTapa")
	fecha = request.form.get("birthday")
	hora = request.form.get("hora")
	newdata = [tipodoc, doc, temperatura, tapabocas, fecha, hora]
	ingresar = True
	for val in range(len(newdata)):
		if newdata[val] == None:
			ingresar = False

	usr = Ciudadano.find_one({"_id":doc})
	if usr != None:
		if usr["Tipo_documento"] != tipodoc or usr["_id"] != doc:
			ingresar = False
	else:
		ingresar = False

	if ingresar:
		nro = Visita.count_documents({})
		nro += 1
		if tapabocas == 'No' or temperatura >= float(38):
			valida = 'Denegado'
		else:
			valida = 'Aceptado'

		vis = [nro, tipodoc, doc, nit, tapabocas, temperatura, fecha, hora, valida]
		insertVisita(vis)
		if valida == 'Aceptado':
			flash("*Se ha registrado la visita satisfactoriamente")
		elif valida == 'Denegado':
			flash("*El usuario no puede ingresar")
	else:
		flash("*Ha ocurrido un problema y no se ha registrado la visita")

	est = Establecimiento.find_one({"_id":nit})
	data = [est["Usuario"], est["_id"]]
	data = [data]
	return render_template('usrEstablecimiento.html', data = data)

@app.route('/solicitudCierreEstablecimiento/<nit>', methods=['POST'])
def solicitudCierreEstablecimiento(nit):
	contra = request.form.get("psw")
	est = Establecimiento.find_one({"_id":nit})
	passw = est["Contraseña"]
	redir = '/modInfoEstablecimiento/' + nit
	if contra == passw:
		est = jsonToList2(est)
		est.pop()
		est.append("Eliminar")
		insertSolicitud(est)
		flash("*Se ha enviado la solicitud satisfactoriamente")
		return redirect(redir)
	else:
		flash("*Las contraseñas no coinciden")
		return redirect(redir)

@app.route('/seleccionarFiltroCiudadano/<Id>', methods=['POST'])
def seleccionarFiltroCiudadano(Id):
	tipo = request.form.get("tipo")
	ciud = Ciudadano.find_one({"_id":Id})
	data = [ciud["Usuario"], ciud["_id"]]
	data = [data]
	if tipo == 'Visitas por fecha': tipo = 'VisFecha'
	elif tipo == 'Visitas por fecha y hora': tipo = 'VisFechaHora'
	redir = '/reporte' + tipo + 'Ciudadano.html'
	return render_template(redir, data = data)

@app.route('/seleccionarFiltroEstablecimiento/<nit>', methods=['POST'])
def seleccionarFiltroEstablecimiento(nit):
	tipo = request.form.get("tipo")
	est = Establecimiento.find_one({"_id":nit})
	data = [est["Usuario"], est["_id"]]
	data = [data]
	if tipo == 'Fecha y hora': tipo = 'FechaHora'
	elif tipo == 'Numero de documento': tipo = 'Documento'
	elif tipo == 'Todas las visitas': tipo  = 'Visitas'
	redir = '/reporte' + tipo + 'Establecimiento.html'
	return render_template(redir, data = data)

@app.route('/seleccionarFiltroSalud/<nit>', methods=['POST'])
def seleccionarFiltroSalud(nit):
	tipo = request.form.get("tipo")
	sal = Salud.find_one({"_id":nit})
	data = [sal["Usuario"], sal["_id"]]
	data = [data]
	if tipo == 'Todos los exámenes': tipo = 'Examenes'
	elif tipo == 'Resultados': tipo = 'Estado'
	redir = '/reporte' + tipo + 'Salud.html'
	return render_template(redir, data = data)

@app.route('/seleccionarFiltroAdmin/<Id>', methods=['POST'])
def seleccionarFiltroAdmin(Id):
	tipo = request.form.get("tipo")
	print(tipo)
	adm = Admin.find_one({"_id":Id})
	data = [adm["Usuario"], adm["_id"]]
	data = [data]
	if tipo == 'Género de ciudadano': tipo = 'Genero'
	elif tipo == 'Categorías de establecimientos': 
		tipo = 'Categoria'
		data = [[],[]]
		adm = Admin.find_one({"_id":Id})
		data[0].append(adm["Usuario"])
		data[0].append(adm["_id"])
		cat = Categoria.find({})
		for c in cat:
			data[1].append([c["_id"], c["Nombre"]])
	elif tipo == 'Establecimientos': tipo = 'Establecimiento'
	elif tipo == 'Resultados de exámenes': tipo = 'Examenes'
	elif tipo == 'Aforo de establecimientos': tipo = 'Aforo'
	elif tipo == 'Número de documento': tipo = 'Documento'
	elif tipo == 'Fecha y hora': tipo = 'FechaHora'
	redir = '/reporte' + tipo + 'Administrador.html'
	return render_template(redir, data = data)

@app.route('/leerCodigoQR/<nit>', methods=['POST'])
def leerCodigo(nit):
	#dir_path = sys.path[0]
	dir_path = "/home/ubuntu/reportedos/Proyecto-Ingesoft/software/ingesoft"
	if request.method == 'POST':
		temperatura = float(request.form.get("inputTemp"))
		tapabocas = request.form.get("inputMuni")
		if 'file' not in request.files:
			print("No mi rey, selecciona un archivo 1")
			return redirect(request.url)
		file = request.files['file']
		if file.filename == '':
			print("No mi rey, selecciona un archivo 2")
			return redirect(request.url)
		ext = file.filename
		nexte = ''
		flag = False
		for i in range(len(ext)): 
			if ext[i] == '.':
				flag = True
			if flag:
				nexte += ext[i]

		if nexte == '.PNG' or nexte == '.png':
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			img = cv2.imread(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			dtector = cv2.QRCodeDetector()
			data, bbox, stight_code = dtector.detectAndDecode(img)
			data = parser(data)
			tipodoc = data[0]
			doc = data[1]
			nro = Visita.count_documents({})
			nro += 1
			if tapabocas == 'No' or temperatura >= float(38):
				valida = 'Denegado'
			else:
				valida = 'Aceptado'

			vis = [nro, tipodoc, doc, nit, tapabocas, temperatura, str(datetime.datetime.now().date()), str(datetime.datetime.now().time()),valida]
			insertVisita(vis)
			if valida == 'Aceptado':
				flash("*Se ha registrado la visita satisfactoriamente")
			elif valida == 'Denegado':
				flash("*El usuario no puede ingresar")
		else:
			flash("*Ha ocurrido un problema y no se ha registrado la visita")
	est = Establecimiento.find_one({"_id":nit})
	data = [est["Usuario"], est["_id"]]
	data = [data]
	return render_template('agregarVisita.html', data = data)

@app.route('/filtroVisitasCiudadano/<Id>', methods=['POST'])
def filtroVisitasCiudadano(Id):
	if request.method == 'POST':
		#descarga = request.form.get("tipo")
		ans = reporteVisitasCiudadanoJson(Id)
		if len(ans) != 0:
			fil = jsonExcel(ans)
			createExcel(fil)
			createPDF(fil)
		else:
			flash("*No se encontraron coincidencias con el filtro")
	ciud = Ciudadano.find_one({"_id":Id})
	data = [ciud["Usuario"], ciud["_id"]]
	data = [data]
	return render_template("reporteVisitasCiudadano.html", data = data)

@app.route('/filtroVisFechaCiudadano/<Id>', methods=['POST'])
def filtroVisFechaCiudadano(Id):
	if request.method == 'POST':
		ini = request.form.get("inicio")
		fin = request.form.get("fin")
		ans = reporteVisFechaCiudadanoJson(Id, ini, fin)
		if len(ans) != 0:
			fil = jsonExcel(ans)
			createExcel(fil)
			createPDF(fil)
		else:
			flash("*No se encontraron coincidencias con el filtro")
	ciud = Ciudadano.find_one({"_id":Id})
	data = [ciud["Usuario"], ciud["_id"]]
	data = [data]
	return render_template("reporteVisFechaCiudadano.html", data = data)

@app.route('/filtroVisFechaHoraCiudadano/<Id>', methods=['POST'])
def filtroVisFechaHoraCiudadano(Id):
	if request.method == 'POST':
		fini = request.form.get("inicio")
		#ffin = request.form.get("fin")
		hini = request.form.get("hinicio")
		hfin = request.form.get("hfin")
		ans = reporteFechaHoraCiudadanoJson(Id, fini, fini, hini, hfin)
		if len(ans) != 0:
			fil = jsonExcel(ans)
			createExcel(fil)
			createPDF(fil)
		else:
			flash("*No se encontraron coincidencias con el filtro")
	ciud = Ciudadano.find_one({"_id":Id})
	data = [ciud["Usuario"], ciud["_id"]]
	data = [data]
	return render_template("reporteVisFechaHoraCiudadano.html", data = data)

@app.route('/filtroVisitasEstablecimiento/<nit>', methods=['POST'])
def filtroVisitasEstablecimiento(nit):
	if request.method == 'POST':
		ans = reporteVisitasEstablecimientoJson(nit)
		if len(ans) != 0:
			fil = jsonExcel(ans)
			createExcel(fil)
			createPDF(fil)
		else:
			flash("*No se encontraron coincidencias con el filtro")
	est = Establecimiento.find_one({"_id":nit})
	data = [est["Usuario"], est["_id"]]
	data = [data]
	return render_template("reporteVisitasEstablecimiento.html", data = data)

@app.route('/filtroFechaEstablecimiento/<nit>', methods=['POST'])
def filtroFechaEstablecimiento(nit):
	if request.method == 'POST':
		ini = request.form.get("inicio")
		fin = request.form.get("fin")
		ans = reporteFechaEstablecimientoJson(nit, ini, fin)
		if len(ans) != 0:
			fil = jsonExcel(ans)
			createExcel(fil)
			createPDF(fil)
		else:
			flash("*No se encontraron coincidencias con el filtro")
	est = Establecimiento.find_one({"_id":nit})
	data = [est["Usuario"], est["_id"]]
	data = [data]
	return render_template("reporteFechaEstablecimiento.html", data = data)

@app.route('/filtroFechaHoraEstablecimiento/<nit>', methods=['POST'])
def filtroFechaHoraEstablecimiento(nit):
	if request.method == 'POST':
		fini = request.form.get("inicio")
		#ffin = request.form.get("fin")
		hini = request.form.get("hinicio")
		hfin = request.form.get("hfin")
		#descarga = request.form.get("tipo")
		ans = reporteFechaHoraEstablecimientoJson(nit, fini, fini, hini, hfin)
		if len(ans) != 0:
			fil = jsonExcel(ans)
			createExcel(fil)
			createPDF(fil)
		else:
			flash("*No se encontraron coincidencias con el filtro")
	est = Establecimiento.find_one({"_id":nit})
	data = [est["Usuario"], est["_id"]]
	data = [data]
	return render_template("reporteFechaHoraEstablecimiento.html", data = data)

@app.route('/filtroDocEstablecimiento/<nit>', methods=['POST'])
def filtroDocEstablecimiento(nit):
	if request.method == 'POST':
		doc = request.form.get("doc")
		#descarga = request.form.get("tipo")
		ans = reporteDocumentoEstablecimientoJson(nit, doc)
		if len(ans) != 0:
			fil = jsonExcel(ans)
			createExcel(fil)
			createPDF(fil)
		else:
			flash("*No se encontraron coincidencias con el filtro")
	est = Establecimiento.find_one({"_id":nit})
	data = [est["Usuario"], est["_id"]]
	data = [data]
	return render_template("reporteDocumentoEstablecimiento.html", data = data)

@app.route('/filtroNomEstablecimiento/<nit>', methods=['POST'])
def filtroNomEstablecimiento(nit):
	if request.method == 'POST':
		nom = request.form.get("nombres")
		#descarga = request.form.get("tipo")
		ans = reporteNombreEstablecimientoJson(nit, nom)
		if len(ans) != 0:
			fil = jsonExcel(ans)
			createExcel(fil)
			createPDF(fil)
		else:
			flash("*No se encontraron coincidencias con el filtro")
	est = Establecimiento.find_one({"_id":nit})
	data = [est["Usuario"], est["_id"]]
	data = [data]
	return render_template("reporteNombresEstablecimiento.html", data = data)

@app.route('/filtroApeEstablecimiento/<nit>', methods=['POST'])
def filtroApeEstablecimiento(nit):
	if request.method == 'POST':
		ape = request.form.get("apellido")
		#descarga = request.form.get("tipo")
		ans = reporteApellidoEstablecimientoJson(nit, ape)
		if len(ans) != 0:
			fil = jsonExcel(ans)
			createExcel(fil)
			createPDF(fil)
		else:
			flash("*No se encontraron coincidencias con el filtro")
	est = Establecimiento.find_one({"_id":nit})
	data = [est["Usuario"], est["_id"]]
	data = [data]
	return render_template("reporteApellidoEstablecimiento.html", data = data)

@app.route('/filtroExamenesSalud/<nit>', methods=['POST'])
def filtroExamenesSalud(nit):
	if request.method == 'POST':
		#descarga = request.form.get("tipo")
		ans = reporteExamenesSaludJson(nit)
		if len(ans) != 0:
			fil = jsonExcelSalud(ans)
			createExcelSalud(fil)
			createPDFSalud(fil)
		else:
			flash("*No se encontraron coincidencias con el filtro")
	sal = Salud.find_one({"_id":nit})
	data = [sal["Usuario"], sal["_id"]]
	data = [data]
	return render_template('reporteExamenesSalud.html', data = data)

@app.route('/filtroFechaSalud/<nit>', methods=['POST'])
def filtroFechaSalud(nit):
	if request.method == 'POST':
		ini = request.form.get("inicio")
		fin = request.form.get("fin")
		#descarga = request.form.get("tipo")
		ans = reporteFechaSaludJson(nit, ini, fin)
		if len(ans) != 0:
			fil = jsonExcelSalud(ans)
			createExcelSalud(fil)
			createPDFSalud(fil)
		else:
			flash("*No se encontraron coincidencias con el filtro")
	sal = Salud.find_one({"_id":nit})
	data = [sal["Usuario"], sal["_id"]]
	data = [data]
	return render_template('reporteFechaSalud.html', data = data)

@app.route('/filtroEstadoSalud/<nit>', methods=['POST'])
def filtroEstadoSalud(nit):
	if request.method == 'POST':
		res = request.form.get("resul")
		#descarga = request.form.get("tipo")
		ans = reporteEstadoSaludJson(nit, res)
		if len(ans) != 0:
			fil = jsonExcelSalud(ans)
			createExcelSalud(fil)
			createPDFSalud(fil)
		else:
			flash("*No se encontraron coincidencias con el filtro")
	sal = Salud.find_one({"_id":nit})
	data = [sal["Usuario"], sal["_id"]]
	data = [data]
	return render_template('reporteEstadoSalud.html', data = data)

@app.route('/filtroGeneroAdmin/<Id>', methods=['POST'])
def filtroGeneroAdmin(Id):
	if request.method == 'POST':
		gen = request.form.get("tipo")
		ans = reporteGeneroAdminJson(gen) 
		if len(ans) != 0:
			fil = jsonExcel(ans)
			createExcel(fil)
			createPDF(fil)
		else:
			flash("*No se encontraron coincidencias con el filtro")
	adm = Admin.find_one({"_id":Id})
	data = [adm["Usuario"], adm["_id"]]
	data = [data]
	return render_template('reporteGeneroAdministrador.html', data = data)

@app.route('/filtroCategoriaAdmin/<Id>', methods=['POST'])
def filtroCategoriaAdmin(Id):
	if request.method == 'POST':
		cat = request.form.get("tipo")
		c = Categoria.find_one({"Nombre":cat})
		ans = reporteCategoriaAdminJson(cat) 
		if len(ans) != 0:
			fil = jsonExcel(ans)
			createExcel(fil)
			createPDF(fil)
		else:
			flash("*No se encontraron coincidencias con el filtro")
	data = [[],[]]
	adm = Admin.find_one({"_id":Id})
	data[0].append(adm["Usuario"])
	data[0].append(adm["_id"])
	cat = Categoria.find({})
	for c in cat:
		data[1].append([c["_id"], c["Nombre"]])
	
	return render_template('reporteCategoriaAdministrador.html', data = data)

@app.route('/filtroEstablecimientoAdmin/<Id>', methods=['POST'])
def filtroEstablecimientoAdmin(Id):
	if request.method == 'POST':
		nom = request.form.get("inputName")
		ans = reporteEstablecimientoAdminJson(nom) 
		if len(ans) != 0:
			fil = jsonExcel(ans)
			createExcel(fil)
			createPDF(fil)
		else:
			flash("*No se encontraron coincidencias con el filtro")
	adm = Admin.find_one({"_id":Id})
	data = [adm["Usuario"], adm["_id"]]
	data = [data]
	return render_template('reporteEstablecimientoAdministrador.html', data = data)

@app.route('/filtroExamenesAdmin/<Id>', methods=['POST'])
def filtroExamenesAdmin(Id):
	if request.method == 'POST':
		#gen = request.form.get("tipo")
		ans = reporteExamenesAdminJson() 
		if len(ans) != 0:
			fil = jsonExcelSalud(ans)
			createExcelSalud(fil)
			createPDFSalud(fil)
		else:
			flash("*No se encontraron coincidencias con el filtro")
	adm = Admin.find_one({"_id":Id})
	data = [adm["Usuario"], adm["_id"]]
	data = [data]
	return render_template('reporteExamenesAdministrador.html', data = data)
"""
@app.route('/filtroAforoAdmin/<Id>', methods=['POST'])
def filtroAforoAdmin(Id):
	if request.method == 'POST':
		num = request.form.get("tipo")
		#ans = reporteGeneroAdminJson(num) 
		if len(ans) != 0:
			fil = jsonExcel(ans)
			createExcel(fil)
			createPDF(fil)
		else:
			flash("*No se encontraron coincidencias con el filtro")
	adm = Admin.find_one({"_id":Id})
	data = [adm["Usuario"], adm["_id"]]
	data = [data]
	return render_template('reporteAforoAdministrador.html', data = data)
"""
@app.route('/filtroDocumentoAdmin/<Id>', methods=['POST'])
def filtroDocumentoAdmin(Id):
	if request.method == 'POST':
		tipodoc = request.form.get("tipo")
		doc = request.form.get("inputNumDoc")
		print(tipodoc, doc)
		ans = reporteDocumentoAdminJson(tipodoc, doc) 
		if len(ans) != 0:
			fil = jsonExcel(ans)
			createExcel(fil)
			createPDF(fil)
		else:
			flash("*No se encontraron coincidencias con el filtro")
	adm = Admin.find_one({"_id":Id})
	data = [adm["Usuario"], adm["_id"]]
	data = [data]
	return render_template('reporteDocumentoAdministrador.html', data = data)

@app.route('/filtroFechaHoraAdmin/<Id>', methods=['POST'])
def filtroFechaHoraAdmin(Id):
	if request.method == 'POST':
		fini = request.form.get("inicio")
		#ffin = request.form.get("fin")
		hini = request.form.get("hinicio")
		hfin = request.form.get("hfin")
		#descarga = request.form.get("tipo")
		ans = reporteFechaHoraAdminJson(fini, fini, hini, hfin)
		if len(ans) != 0:
			fil = jsonExcel(ans)
			createExcel(fil)
			createPDF(fil)
		else:
			flash("*No se encontraron coincidencias con el filtro")
	adm = Admin.find_one({"_id":Id})
	data = [adm["Usuario"], adm["_id"]]
	data = [data]
	return render_template('reporteFechaHoraAdministrador.html', data = data)

@app.route('/download/<path:nom>')
def download_file(nom):
	filename = "/home/ubuntu/reportedos/Proyecto-Ingesoft/ingesoft/static/" + nom
	#filename = "C:/Users/Victor Toro/Documents/Proyecto Ingesoft AWS/ingesoft/static/" + nom
	return send_file(filename, as_attachment=True)

@app.route('/crearCategoria/<Id>', methods=['POST'])
def crearCategoria(Id):
	if request.method == 'POST':
		nombre = request.form.get("inputCat")
		#print(nombre)
		ans = Categoria.find_one({"Nombre":nombre})
		#print(ans == None)
		if ans == None:
			nro = Categoria.count_documents({}) + 1
			dato = [nro, nombre]
			insertCategoria(dato)
			flash("Se ha registrado la categoría con éxito")
		else:
			flash("La categoría ya está registrada en la base de datos, seleccione otro nombre")
	data = [[],[]]
	adm = Admin.find_one({"_id":Id})
	data[0].append(adm["Usuario"])
	data[0].append(adm["_id"])
	cat = Categoria.find({})
	for c in cat:
		data[1].append([c["_id"], c["Nombre"]])
	return render_template("categorias.html", data = data)

if __name__ == '__main__':
	#app.run(debug = True)
	app.run(host='0.0.0.0', port=8080, debug = True)
