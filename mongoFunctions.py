
from pymongo import MongoClient
import datetime
import pandas as pd
from pandas import ExcelWriter
import os, os.path
from fpdf import FPDF

MONGO_URI = 'mongodb://localhost'

client = MongoClient(MONGO_URI)

db = client['covsafedb']
Admin = db['Administrador']
Ciudadano = db['Ciudadano']
Establecimiento = db['Establecimiento']
Salud = db['Entidad_salud']
Categoria = db['Categoria']
Examen = db['Examen']
Visita = db['Visita']
Solicitud = db['Solicitud']

def insertCiudadano(data):
	rows = ["_id", "Nombre", "Apellido","Tipo_documento",
	"Género", "Fecha_nacimiento", "Correo", "Teléfono", "Departamento", 
	"Municipio","Barrio", "Dirección", "Usuario", "Contraseña"]

	ciud = {"_id":'', "Nombre":'', "Apellido":'',"Tipo_documento":'',
	"Género":'', "Fecha_nacimiento":'', "Correo":'', "Teléfono":'', "Departamento":'', 
	"Municipio":'',"Barrio":'', "Dirección":'', "Usuario":'', "Contraseña":''}

	for i in range(len(rows)):
		ciud[rows[i]] = data[i]

	Ciudadano.insert_one(ciud)
	return #ciud

def insertEstablecimiento(data):
	rows = ["_id", "Razón_social", "Categoría","Correo",
	"Teléfono", "Departamento", "Municipio","Barrio", 
	"Dirección", "Usuario", "Contraseña", "Visitas"]

	est = {"_id":'', "Razón_social":'', "Categoría":'',"Correo":'',
	"Teléfono":'', "Departamento":'', "Municipio":'',"Barrio":'', 
	"Dirección":'', "Usuario":'', "Contraseña":'', "Visitas":''}

	for i in range(len(rows)):
		est[rows[i]] = data[i]

	Establecimiento.insert_one(est)
	return #est

def insertSalud(data):
	rows = ["_id", "Razón_social", "Categoría","Correo",
	"Teléfono", "Departamento", "Municipio","Barrio", 
	"Dirección", "Usuario", "Contraseña", "Exámenes"]

	sal = {"_id":'', "Razón_social":'', "Categoría":'',"Correo":'',
	"Teléfono":'', "Departamento":'', "Municipio":'',"Barrio":'', 
	"Dirección":'', "Usuario":'', "Contraseña":'', "Exámenes":''}

	for i in range(len(rows)):
		sal[rows[i]] = data[i]

	Salud.insert_one(sal)
	return #sal

def insertAdmin(data):
	ciud = Ciudadano.find_one({"_id":data[0], 
	"Nombre":data[1], "Apellido":data[2],
	"Tipo_documento":data[3]})
	print(ciud)
	if ciud != None:
		rows = ["_id", "Nombre", "Apellido","Tipo_documento",
		"Usuario", "Contraseña"]

		adm = {"_id":'', "Nombre":'', "Apellido":'',"Tipo_documento":'',
		"Usuario":'', "Contraseña":''}

		for i in range(len(rows)):
			adm[rows[i]] = data[i]

		Admin.insert_one(adm)
		print("Agregado")
	else:
		print("No se agregó")
	return 

def insertCategoria(data):
	rows = ["_id", "Nombre"]
	cat = {"_id":'', "Nombre":''}
	for i in range(len(rows)):
		cat[rows[i]] = data[i]

	Categoria.insert_one(cat)
	return 

def insertExamen(data):
	rows = ["_id", "Tipo_documento", "ID_Paciente", "NIT", "Resultado", "Fecha", "Cuarentena"]
	exa = {"_id":'', "Tipo_documento":'', "ID_Paciente":'', "NIT":'', "Resultado":'', "Fecha":'', "Cuarentena":''}
	for i in range(len(rows)):
		exa[rows[i]] = data[i]

	Examen.insert_one(exa)
	return 

def insertVisita(data):
	rows = ["_id", "Tipo_documento", "ID_Visitante", "NIT_Establecimiento", 
	"Tapabocas", "Temperatura", "Fecha", "Hora","Ingreso"]
	vis = {"_id":'', "Tipo_documento":'', "ID_Visitante":'', "NIT_Establecimiento":'', 
	"Tapabocas":'', "Temperatura":'', "Fecha":'', "Hora":'',"Ingreso":''}
	for i in range(len(rows)):
		vis[rows[i]] = data[i]

	Visita.insert_one(vis)
	return 

def insertSolicitud(data):
	rows = ["_id", "Razón_social", "Categoría","Correo",
	"Teléfono", "Departamento", "Municipio","Barrio", 
	"Dirección", "Usuario", "Contraseña", "Solicitud"]

	ent = {"_id":'', "Razón_social":'', "Categoría":'',"Correo":'',
	"Teléfono":'', "Departamento":'', "Municipio":'',"Barrio":'', 
	"Dirección":'', "Usuario":'', "Contraseña":'', "Solicitud":''}

	for i in range(len(rows)):
		ent[rows[i]] = data[i]
	Solicitud.insert_one(ent)
	return

def updateAdmin(id, data):
	rows = ["_id", "Nombre", "Apellido","Tipo_documento",
	"Usuario", "Contraseña"]

	adm = {"_id":'', "Nombre":'', "Apellido":'',"Tipo_documento":'',
	"Usuario":'', "Contraseña":''}

	for i in range(len(rows)):
		adm[rows[i]] = data[i]

	Admin.update_one({"_id": id}, 
	{"$set": adm})
	return

def updateCiudadano(id, data):
	rows = ["Nombre", "Apellido", "Correo", "Teléfono", "Departamento", 
	"Municipio","Barrio", "Dirección", "Contraseña"]

	ciud = {"Nombre":'', "Apellido":'', "Correo":'', "Teléfono":'', "Departamento":'', 
	"Municipio":'',"Barrio":'', "Dirección":'', "Contraseña":''}

	for i in range(len(rows)):
		ciud[rows[i]] = data[i]

	Ciudadano.update_one({"_id": id}, 
	{"$set": ciud})
	return

def updateEstablecimiento(nit, data):
	rows = ["Razón_social", "Correo", "Teléfono", "Departamento", "Municipio","Barrio", 
	"Dirección", "Contraseña"]

	est = {"Razón_social":'', "Correo":'', "Teléfono":'', "Departamento":'', "Municipio":'',"Barrio":'', 
	"Dirección":'', "Contraseña":''}

	for i in range(len(rows)):
		est[rows[i]] = data[i]

	Establecimiento.update_one({"_id": nit}, 
	{"$set": est})
	return #est

def updateSalud(nit, data):
	rows = ["Razón_social", "Correo", "Teléfono", "Departamento", "Municipio","Barrio", 
	"Dirección", "Contraseña"]

	sal = {"Razón_social":'', "Correo":'', "Teléfono":'', "Departamento":'', "Municipio":'',"Barrio":'', 
	"Dirección":'', "Contraseña":''}

	for i in range(len(rows)):
		sal[rows[i]] = data[i]

	Salud.update_one({"_id": nit}, 
	{"$set": sal})
	return #est

def jsonToList(data):
	dat = []
	for d in data:
		dat.append(data[d])
	return [dat]

def jsonToList2(data):
	dat = []
	for d in data:
		dat.append(data[d])
	return dat

def orderCiudadano(data):
	ciud = {"_id":'', "Nombre":'', "Apellido":'',"Tipo_documento":'',
	"Género":'', "Fecha_nacimiento":'', "Correo":'', "Teléfono":'', "Departamento":'', 
	"Municipio":'',"Barrio":'', "Dirección":'', "Usuario":'', "Contraseña":''}

	for d in data:
		ciud[d] = data[d]
	return ciud

def orderEstablecimiento(data):
	est = {"_id":'', "Razón_social":'', "Categoría":'',"Correo":'',
	"Teléfono":'', "Departamento":'', "Municipio":'',"Barrio":'', 
	"Dirección":'', "Usuario":'', "Contraseña":'', "Visitas":''}
	for d in data:
		est[d] = data[d]
	return est

def orderSalud(data):
	sal = {"_id":'', "Razón_social":'', "Categoría":'',"Correo":'',
	"Teléfono":'', "Departamento":'', "Municipio":'',"Barrio":'', 
	"Dirección":'', "Usuario":'', "Contraseña":'', "Exámenes":''}
	for d in data:
		sal[d] = data[d]
	return sal

def orderAdmin(data):
	adm = {"_id":'', "Nombre":'', "Apellido":'',
	"Tipo_documento":'',"Usuario":'', "Contraseña":''}

	for d in data:
		adm[d] = data[d]
	return adm

def parser(data):
	doc = ''
	tipodoc = ""
	flag = False
	i = 0
	while i < len(data):
		#print(data[i])
		if not flag:
			if data[i] == "," and data[i-1] == "'":
				flag = True
				i += 3
			elif data[i] != '[' and data[i] != "'":
				tipodoc += data[i]
			
		if flag:
			if data[i] != "'":
				if data[i] != ']':
					doc += data[i]

		i += 1

	return [tipodoc, doc]

#categoria
#resultado examenes
def reporteVisitasCiudadanoJson(Id):
	results = Visita.find({"ID_Visitante":Id})
	fil = []
	for r in results:
		fil.append(r)
	return fil

def reporteVisFechaCiudadanoJson(Id, ini, fin):
	ini = datetime.datetime.strptime(ini , '%Y-%m-%d')
	fin = datetime.datetime.strptime(fin , '%Y-%m-%d')
	results = Visita.find({"ID_Visitante": Id})
	fil = []
	for r in results:
		tmp = datetime.datetime.strptime(r["Fecha"], '%Y-%m-%d')
		if tmp >= ini and tmp <= fin:
			fil.append(r)
	return fil

def reporteFechaHoraCiudadanoJson(nit, fini, ffin, hini, hfin):
	ini = fini + ' ' + hini
	fin = ffin + ' ' + hfin
	ini = datetime.datetime.strptime(ini , '%Y-%m-%d %H:%M')
	fin = datetime.datetime.strptime(fin , '%Y-%m-%d %H:%M')
	results = Visita.find({"ID_Visitante": nit})
	fil = []
	for r in results:
		fecha = r["Fecha"]
		hora = r["Hora"]
		val = fecha + ' ' + hora
		tmp = datetime.datetime.strptime(val, '%Y-%m-%d %H:%M:%S.%f')
		if tmp >= ini and tmp <= fin:
			fil.append(r)
	return fil

def reporteExamenesCiudadanoJson(Id):
	results = Examen.find({"ID_Paciente":Id})
	fil = []
	for r in results:
		fil.append(r)
	return fil

def reporteVisitasEstablecimientoJson(nit):
	results = Visita.find({"NIT_Establecimiento":nit})
	fil = []
	for r in results:
		fil.append(r)
	return fil

def reporteFechaEstablecimientoJson(nit, ini, fin):
	ini = datetime.datetime.strptime(ini , '%Y-%m-%d')
	fin = datetime.datetime.strptime(fin , '%Y-%m-%d')
	results = Visita.find({"NIT_Establecimiento": nit})
	fil = []
	for r in results:
		tmp = datetime.datetime.strptime(r["Fecha"], '%Y-%m-%d')
		if tmp >= ini and tmp <= fin:
			fil.append(r)
	return fil

def reporteFechaHoraEstablecimientoJson(nit, fini, ffin, hini, hfin):
	ini = fini + ' ' + hini
	fin = ffin + ' ' + hfin
	print(ini)
	print(fin)
	ini = datetime.datetime.strptime(ini , '%Y-%m-%d %H:%M')
	fin = datetime.datetime.strptime(fin , '%Y-%m-%d %H:%M')
	results = Visita.find({"NIT_Establecimiento": nit})
	fil = []
	for r in results:
		fecha = r["Fecha"]
		hora = r["Hora"]
		val = fecha + ' ' + hora
		tmp = datetime.datetime.strptime(val, '%Y-%m-%d %H:%M:%S.%f')
		if tmp >= ini and tmp <= fin:
			fil.append(r)
	return fil

def reporteApellidoEstablecimientoJson(nit, ape):
	results = Visita.find({"NIT_Establecimiento":nit})
	fil = []
	for r in results:
		doc = r["ID_Visitante"]
		ciud = Ciudadano.find({"_id":doc})
		for c in ciud:
			if c["Apellido"] == ape:
				fil.append(r)
	return fil

def reporteNombreEstablecimientoJson(nit, nom):
	results = Visita.find({"NIT_Establecimiento":nit})
	fil = []
	for r in results:
		doc = r["ID_Visitante"]
		ciud = Ciudadano.find({"_id":doc})
		for c in ciud:
			if c["Nombre"] == nom:
				fil.append(r)
	return fil

def reporteDocumentoEstablecimientoJson(nit, doc):
	results = Visita.find({"NIT_Establecimiento":nit})
	ciud = Ciudadano.find({"_id":doc})
	fil = []
	for r in results:
		newdoc = r["ID_Visitante"]
		if newdoc == doc:
			fil.append(r)
	return fil

def reporteExamenesSaludJson(nit):
	results = Examen.find({"NIT":nit})
	fil = []
	for r in results:
		fil.append(r)
	return fil

def reporteFechaSaludJson(nit, ini, fin):
	ini = datetime.datetime.strptime(ini , '%Y-%m-%d')
	fin = datetime.datetime.strptime(fin , '%Y-%m-%d')
	results = Examen.find({"NIT": nit})
	fil = []
	for r in results:
		tmp = datetime.datetime.strptime(r["Fecha"], '%Y-%m-%d')
		if tmp >= ini and tmp <= fin:
			fil.append(r)
	return fil

def reporteEstadoSaludJson(nit, res):
	results = Examen.find({"NIT": nit})
	fil = []
	for r in results:
		tmp = r["Resultado"]
		if tmp == res:
			fil.append(r)
	return fil

def reporteGeneroAdminJson(gen):
	results = Ciudadano.find({"Género":gen})
	fil = []
	for r in results:
		ced = r["_id"]
		vis = Visita.find({})
		for v in vis:	
			if v["ID_Visitante"] == ced:
				fil.append(v)
	return fil

def reporteCategoriaAdminJson(cat):
	c = Categoria.find_one({"Nombre":cat})
	results = Establecimiento.find({"Categoría":[c["_id"], c["Nombre"]]})
	fil = []
	for r in results:
		nit = r["_id"]
		vis = Visita.find({})
		for v in vis:
			if v["NIT_Establecimiento"] == nit:
				fil.append(v)
	return fil

def reporteEstablecimientoAdminJson(nom):
	results = Establecimiento.find({"Razón_social":nom})
	fil = []
	for r in results:
		nit = r["_id"]
		vis = Visita.find({})
		for v in vis:
			if v["NIT_Establecimiento"] == nit:
				fil.append(v)
	return fil

def reporteExamenesAdminJson():
	results = Examen.find({})
	fil = []
	for r in results:
		fil.append(r)
	return fil
"""
def reporteAforoAdminJson(num):
	results = Establecimiento.find({})
	fil = []
	for r in results:
		nit = r["_id"]
		vis = Visita.find({})
		for v in vis:
			if v["NIT_Establecimiento"] == nit:
				fil.append(v)
"""
def reporteDocumentoAdminJson(tipodoc, doc):
	results = Ciudadano.find_one({"_id":doc, "Tipo_documento":tipodoc})
	fil = []
	for r in results:
		ced = r["_id"]
		vis = Visita.find({})
		for v in vis:	
			if v["ID_Visitante"] == ced:
				fil.append(v)
	return fil

def reporteFechaHoraAdminJson(fini, ffin, hini, hfin):
	ini = fini + ' ' + hini
	fin = ffin + ' ' + hfin
	ini = datetime.datetime.strptime(ini , '%Y-%m-%d %H:%M')
	fin = datetime.datetime.strptime(fin , '%Y-%m-%d %H:%M')
	results = Visita.find({})
	fil = []
	for r in results:
		fecha = r["Fecha"]
		hora = r["Hora"]
		val = fecha + ' ' + hora
		tmp = datetime.datetime.strptime(val, '%Y-%m-%d %H:%M:%S.%f')
		if tmp >= ini and tmp <= fin:
			fil.append(r)
	return fil

def jsonExcel(fil):
	col = { "ID Visita":[], 
			"Establecimiento":[],
			"Tipo de documento":[],
			"Nro documento":[],
			"Uso del tapabocas":[],
			"Temperatura":[],
			"Fecha de ingreso":[],
			"Hora de ingreso":[],
			"Ingreso":[],
			"Nombres":[],
			"Apellidos":[]
		  }
	for vis in fil:
		tipodoc = vis["Tipo_documento"]
		doc = vis["ID_Visitante"]
		nit = vis["NIT_Establecimiento"]
		print(tipodoc)
		print(doc)
		ciud = Ciudadano.find_one({"Tipo_documento":tipodoc, "_id":doc})
		print(ciud)
		est = Establecimiento.find_one({"_id":nit})
		col["ID Visita"].append(vis["_id"])
		col["Establecimiento"].append(est["Razón_social"])
		col["Tipo de documento"].append(vis["Tipo_documento"])
		col["Nro documento"].append(vis["ID_Visitante"])
		col["Uso del tapabocas"].append(vis["Tapabocas"])
		col["Temperatura"].append(vis["Temperatura"])
		col["Fecha de ingreso"].append(vis["Fecha"])
		col["Hora de ingreso"].append(vis["Hora"])
		col["Ingreso"].append(vis["Ingreso"])
		col["Nombres"].append(ciud["Nombre"])
		col["Apellidos"].append(ciud["Apellido"])
	return col

def jsonExcelSalud(fil):
	col = { "ID Exámen":[], 
			"Entidad de salud":[],
			"Tipo de documento":[],
			"Nro documento":[],
			"Nombres":[],
			"Apellidos":[],
			"Resultado":[],
			"Fecha del exámen":[],
			"Días de cuarentena":[],
		  }
	for exa in fil:
		tipodoc = exa["Tipo_documento"]
		doc = exa["ID_Paciente"]
		nit = exa["NIT"]
		ciud = Ciudadano.find_one({"Tipo_documento":tipodoc, "_id":doc})
		sal = Salud.find_one({"_id":nit})
		col["ID Exámen"].append(exa["_id"])
		col["Entidad de salud"].append(sal["Razón_social"])
		col["Tipo de documento"].append(exa["Tipo_documento"])
		col["Nro documento"].append(exa["ID_Paciente"])
		col["Nombres"].append(ciud["Nombre"])
		col["Apellidos"].append(ciud["Apellido"])
		col["Resultado"].append(exa["Resultado"])
		col["Fecha del exámen"].append(exa["Fecha"])
		col["Días de cuarentena"].append(exa["Cuarentena"])

	return col

def createExcel(jso):
	df = pd.DataFrame(jso)
	df = df[["ID Visita", 
			"Establecimiento",
			"Tipo de documento", 
			"Nro documento",
			"Uso del tapabocas",
			"Temperatura",
			"Fecha de ingreso",
			"Hora de ingreso",
			"Ingreso",
			"Nombres",
			"Apellidos"]]
	filename = '/home/ubuntu/reportedos/Proyecto-Ingesoft/ingesoft/static/excel/archivo.xlsx'
	#filename = 'C:/Users/Victor Toro/Documents/Proyecto Ingesoft AWS/ingesoft/static/excel/archivo.xlsx'
	writer = ExcelWriter(filename)
	df.to_excel(writer, 'Hoja de datos', index=False)
	writer.save()
	return

def createExcelSalud(jso):
	df = pd.DataFrame(jso)
	df = df[["ID Exámen", 
			"Entidad de salud",
			"Tipo de documento",
			"Nro documento",
			"Nombres",
			"Apellidos",
			"Resultado",
			"Fecha del exámen",
			"Días de cuarentena"]]
	filename = '/home/ubuntu/reportedos/Proyecto-Ingesoft/ingesoft/static/excel/archivo.xlsx'
	#filename = 'C:/Users/Victor Toro/Documents/Proyecto Ingesoft AWS/ingesoft/static/excel/archivo.xlsx'
	writer = ExcelWriter(filename)
	df.to_excel(writer, 'Hoja de datos', index=False)
	writer.save()
	return

def createPDF(col):
	pdf = FPDF(orientation = 'L')
	pdf.add_page()
	pdf.set_xy(0, 0)
	pdf.set_font('arial', 'B', 7)
	pdf.cell(26, 10, 'ID Visita', 1, 0, 'C')
	pdf.cell(32, 10, 'Establecimiento', 1, 0, 'C')
	pdf.cell(28, 10, 'Tipo de documento', 1, 0, 'C')
	pdf.cell(26, 10, 'Nro documento', 1, 0, 'C')
	pdf.cell(26, 10, 'Uso del tapabocas', 1, 0, 'C')
	pdf.cell(26, 10, 'Temperatura', 1, 0, 'C')
	pdf.cell(26, 10, 'Fecha de ingreso', 1, 0, 'C')
	pdf.cell(26, 10, 'Hora de ingreso', 1, 0, 'C')
	pdf.cell(26, 10, 'Ingreso', 1, 0, 'C')
	pdf.cell(28, 10, 'Nombres', 1, 0, 'C')
	pdf.cell(28, 10, 'Apellidos', 1, 1, 'C')
	#pdf.cell(-90)
	acum = 10
	pdf.set_xy(0, acum)

	for i in range(len(col["ID Visita"])):
		col1 = col["ID Visita"][i]
		col2 = col["Establecimiento"][i]
		col3 = col["Tipo de documento"][i]
		col4 = col["Nro documento"][i]
		col5 = col["Uso del tapabocas"][i]
		col6 = col["Temperatura"][i]
		col7 = col["Fecha de ingreso"][i]
		col8 = col["Hora de ingreso"][i]
		col9 = col["Ingreso"][i]
		col10 = col["Nombres"][i]
		col11 = col["Apellidos"][i]

		pdf.cell(26, 10, '%s' % (col1), 1, 0, 'C')
		pdf.cell(32, 10, '%s' % (col2), 1, 0, 'C')
		pdf.cell(28, 10, '%s' % (col3), 1, 0, 'C')
		pdf.cell(26, 10, '%s' % (col4), 1, 0, 'C')
		pdf.cell(26, 10, '%s' % (col5), 1, 0, 'C')
		pdf.cell(26, 10, '%s' % (col6), 1, 0, 'C')
		pdf.cell(26, 10, '%s' % (col7), 1, 0, 'C')
		pdf.cell(26, 10, '%s' % (col8), 1, 0, 'C')
		pdf.cell(26, 10, '%s' % (col9), 1, 0, 'C')
		pdf.cell(28, 10, '%s' % (col10), 1, 0, 'C')
		pdf.cell(28, 10, '%s' % (col11), 1, 1, 'C')
		#pdf.cell(-90)
		acum += 10
		pdf.set_xy(0, acum)
	pdf.output('/home/ubuntu/reportedos/Proyecto-Ingesoft/ingesoft/static/pdf/archivo.pdf', 'F')
	#pdf.output('C:/Users/Victor Toro/Documents/Proyecto Ingesoft AWS/ingesoft/static/pdf/archivo.pdf', 'F')
	return 
		
def createPDFSalud(col):
	pdf = FPDF(orientation = 'L')
	pdf.add_page()
	pdf.set_xy(0, 0)
	pdf.set_font('arial', 'B', 7)
	pdf.cell(26, 10, 'ID Exámen', 1, 0, 'C')
	pdf.cell(80, 10, 'Entidad de salud', 1, 0, 'C')
	pdf.cell(30, 10, 'Tipo de documento', 1, 0, 'C')
	pdf.cell(26, 10, 'Nro documento', 1, 0, 'C')
	pdf.cell(29, 10, 'Nombres', 1, 0, 'C')
	pdf.cell(29, 10, 'Apellidos', 1, 0, 'C')
	pdf.cell(26, 10, 'Resultado', 1, 0, 'C')
	pdf.cell(26, 10, 'Fecha del exámen', 1, 0, 'C')
	pdf.cell(26, 10, 'Días de cuarentena', 1, 1, 'C')
	#pdf.cell(-90)
	acum = 10
	pdf.set_xy(0, acum)
	pdf.set_font('arial', 'B', 7)
	for i in range(len(col["ID Exámen"])):
		col1 = col["ID Exámen"][i]
		col2 = col["Entidad de salud"][i]
		col3 = col["Tipo de documento"][i]
		col4 = col["Nro documento"][i]
		col5 = col["Nombres"][i]
		col6 = col["Apellidos"][i]
		col7 = col["Resultado"][i]
		col8 = col["Fecha del exámen"][i]
		col9 = col["Días de cuarentena"][i]

		pdf.cell(26, 10, '%s' % (col1), 1, 0, 'C')
		pdf.set_font('arial', 'B', 6)
		pdf.cell(80, 10, '%s' % (col2), 1, 0, 'C')
		pdf.set_font('arial', 'B', 7)
		pdf.cell(30, 10, '%s' % (col3), 1, 0, 'C')
		pdf.cell(26, 10, '%s' % (col4), 1, 0, 'C')
		pdf.cell(29, 10, '%s' % (col5), 1, 0, 'C')
		pdf.cell(29, 10, '%s' % (col6), 1, 0, 'C')
		pdf.cell(26, 10, '%s' % (col7), 1, 0, 'C')
		pdf.cell(26, 10, '%s' % (col8), 1, 0, 'C')
		pdf.cell(26, 10, '%s' % (col9), 1, 1, 'C')
		#pdf.cell(-90)
		acum += 10
		pdf.set_xy(0, acum)
	pdf.output('/home/ubuntu/reportedos/Proyecto-Ingesoft/ingesoft/static/pdf/archivo.pdf', 'F')
	#pdf.output('C:/Users/Victor Toro/Documents/Proyecto Ingesoft AWS/ingesoft/static/pdf/archivo.pdf', 'F')
	return 


def edadCiudadano(Id):
	actual = datetime.datetime.now()
	ciud = Ciudadano.find_one({"_id":Id})
	fecha = ciud["Fecha_nacimiento"]
	año = fecha[0:4]
	mes = fecha[5:7]
	dia = fecha[8:10]
	edad = int(actual.year) - int(año)
	if int(actual.month) < int(mes):
		edad -= 1
	elif int(actual.month) == int(mes):
		if int(actual.day) < int(dia):
			edad -= 1
	return int(edad)

def aforo(nit):
	#Numero de visitas en las ultimas 3 horas
	actual = datetime.datetime.now()
	if len(str(actual.month)) < 2: month = '0' + str(actual.month)
	if len(str(actual.day)) < 2: day = '0' + str(actual.day)
	date = str(actual.year) + '-' + month + '-' + day
	hfin = str(actual.hour) + ':' + str(actual.minute)
	hini = str(actual.hour - 3) + ':' + str(actual.minute)
	print(hfin)
	print(hini)
	vis = reporteFechaHoraEstablecimientoJson(nit, date, date, hini, hfin)
	return len(vis)

def riesgoContagio(Id, nit, tapabocas):
	#Riesgo de contagio se va a tomar como un coeficiente de 0 a 1
	#donde 0 no hay riesgo de contagio y 1 es contagio seguro.
	edad = edadCiudadano(Id)
	vis = aforo(nit)
	riesgo = 0
	if tapabocas == 'No':
		riesgo += 0.7
	else:
		riesgo += 0.05 

	if edad > 3 and edad <= 7:
		riesgo += 0.15
	elif edad > 60:
		riesgo += (edad - 60) * 0.006

	riesgo += vis * 0.015

	if riesgo > 1: riesgo = 1
	return riesgo * 100

"""
def createPDF():
	input_file = r'C:/Users/Victor Toro/Desktop/ingesoft/static/excel/archivo.xlsx'
	#give your file name with valid path 
	
	output_file = r'C:/Users/Victor Toro/Desktop/ingesoft/static/pdf/archivo.pdf'
	#give valid output file name and path
	app = client.DispatchEx("Excel.Application")
	app.Interactive = False
	app.Visible = False
	Workbook = app.Workbooks.Open(input_file)
	try:
		Workbook.WorkSheets(1).Select()
		Workbook.ActiveSheet.ExportAsFixedFormat(0, output_file)
	except Exception as e:
		print("Failed to convert in PDF format.Please confirm environment meets all the requirements  and try again")
		print(str(e))
	finally:
		Workbook.Close()
		app.Quit()
	return
#edgings
"""
"""
from win32com import client
import win32api
import os, os.path
import pandas as pd
from pandas import ExcelWriter
import datetime
fini = '2020-12-05'
ffin = '2020-12-05'
hini = '02:38am'
hfin = '02:41am'

ini = '2020-12-05'
fin = '2020-12-05'
nit = "8600788287"
ans = reporteExamenesSaludJson(nit)
fil = jsonExcelSalud(ans)
createPDFSalud(fil)
createExcel(fil)




import datetime
nit = "8909203040"
ans = reporteApellidoEstablecimiento(nit, "Toro Cedeño")
"""


#results = results["Fecha"]
#print(results["Fecha"])

#data = ["1143878531", "Victor Manuel", "Toro Cedeño", "Cédula de ciudadanía", "admin", "admin"]
#insertAdmin(data)
	
#data = Ciudadano.find_one({"_id":"1143878531", "Nombre":"Victor Manuel"})
#print(data)
#print(data["Usuario"])
#print(data["Contraseña"])
"""
for i in data:
	print(i)
data = orderCiudadano(data)



for i in data:
	print(i)

data = jsonToList(data)

print(data)
"""
#print(data)
#Categoria.insert_one({"_id":1, "Nombre": 'Entidad de salud'})
#Categoria.insert_one({"_id":2, "Nombre": 'Almacén'})
#Categoria.insert_one({"_id":3, "Nombre": 'Droguería'})
#Categoria.insert_one({"_id":4, "Nombre": 'Licorera'})
#Categoria.insert_one({"_id":5, "Nombre": 'Restaurante'})
#Categoria.insert_one({"_id":6, "Nombre": 'Tienda'})

#insert_ciudadano(data)
#ciud = insert_ciudadano(data)
#Ciudadano.insert_one()
#Ciudadano.insert_one(insert_ciudadano(data))
#results = Ciudadano.find() #for
#print(results)
#results = Ciudadano.find({"Nombre": "Victor"})
#print(results)
#results = Ciudadano.find_one({"Usuario": "vtoro"})
#print(results)
#data = jsonToList(results)
#print(data)
#collection.delete_many({})
#collection.delete_one({})
#Ciudadano.update_one({"_id": 1143878531}, {"$set": {"Nombre": } })
#Ciudadano.update_one({"_id": 1143878531}, {"$inc": {"Nombre": } }) #incrementar
#n = Visita.count_documents({})
#print(n)


#Establecimiento.delete_one({"Razón_social":"67890"})
#Solicitud.delete_one({"Razón_social":"67890"})
#res= Ciudadano.find({})
#for r in res:
#	print(r)


