
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

Admin.insert_one({"_id":"1143878531","Nombre":"Victor Manuel","Apellido":"Toro Cedeño","Tipo_documento":"Cédula de ciudadanía","Usuario":"admin","Contraseña":"admin"})
Categoria.insert_one({"_id":1, "Nombre": 'Entidad de salud'})
Categoria.insert_one({"_id":2, "Nombre": 'Almacén'})
Categoria.insert_one({"_id":3, "Nombre": 'Droguería'})
Categoria.insert_one({"_id":4, "Nombre": 'Licorera'})
Categoria.insert_one({"_id":5, "Nombre": 'Restaurante'})
Categoria.insert_one({"_id":6, "Nombre": 'Tienda'})
Establecimiento.insert_one({"_id":"8909203040","Razón_social":"PepsiCo, Inc.","Categoría":[2,"Almacén"],"Correo":"pepsico@gmail.com","Teléfono":"018000911053","Departamento":"Valle del Cauca","Municipio":"Cali","Barrio":"Siloe","Dirección":"Cl. 45 ##6-133","Usuario":"pepsico","Contraseña":"pepsico","Visitas":" "})
Salud.insert_one({"_id":"8600788287","Razón_social":"COMPAÑIA DE MEDICINA PREPAGADA COLSANITAS S A","Categoría":[1,"Entidad de salud"],"Correo":"impuestoscol@colsanitas.com","Teléfono":"6466060","Departamento":"Valle del Cauca","Municipio":"Cali","Barrio":"Siloe","Dirección":"Ac 100 No. 11B-67","Usuario":"colsanitas","Contraseña":"colsanitas","RUT":"8600788287","Exámenes":" "})
