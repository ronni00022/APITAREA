import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import json
import urllib.request
import datetime
from datetime import date

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/api')
def read_root():
    return {'detail': 'Welcome to this app'}

@app.get('/api/Registrar_P/{cedula}/{nombre}/{apellido}/{fecha}/{telefono}/{email}/{sangre}/{provincia}/{direccion}/{latitud}/{longitud}/{confirmacion}/{justificacion}')
def Registrar_P(cedula: str, nombre: str, apellido: str,fecha:str, telefono: str,email:str,sangre:str,provincia:str,direccion:str,latitud:float,longitud:float,confirmacion:str,justificacion:str):
    conexion=sqlite3.connect('app.db')
    registro=conexion.cursor()
    try:
        info=(cedula,nombre,apellido,fecha,telefono,email,sangre,provincia,direccion,latitud,longitud,confirmacion,justificacion)
        query = ''' INSERT INTO VACUNADO(CEDULA,NOMBRE,APELLIDO,FECHA,TELEFONO,EMAIL,SANGRE,PROVINCIA,DIRECCION,LATITUD,LONGITUD,CONFIRMACION,JUSTIFICACION) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?) ''' 
        registro.execute(query,info)
        conexion.commit()
        return {"mensaje":"Gracias Por registrarse"}
    except:
        return {"mensaje": "Usuario ya se vacuno"}

@app.get('/api/Registrar_v/{marca}/{cantidad}')
def Registrar_v(marca: str, cantidad: str):
    conexion=sqlite3.connect('app.db')
    registro=conexion.cursor()
    info = (marca.upper(),cantidad)
    query = ''' INSERT INTO VACUNA(MARCA,CANTIDAD) VALUES (?,?) '''
    registro.execute(query,info)
    conexion.commit()
    return {"mensaje":"Registro Completo"}

@app.get('/api/Consultar_V/{campo}/{buscar}')
def Consultar_V(campo: str, buscar: str):
    a=[]
    conexion=sqlite3.connect('app.db')
    registro=conexion.cursor()
    registro.execute("SELECT * FROM VACUNADO WHERE "+campo+" LIKE '%"+buscar.upper()+"%'")
    datos = registro.fetchall()
    for i in datos:
        a.append({"NOMBRE":i[2],"APELLIDO":i[3],"DOSIS":i[10]})
    return a
@app.get('/api/List_Prov/{provincia}')
def List_Prov(provincia: str):
    a=[]
    conexion=sqlite3.connect('app.db')
    registro=conexion.cursor()
    registro.execute("SELECT * FROM VACUNADO WHERE PROVINCIA = '"+provincia+"'")
    conexion.commit()
    datos= registro.fetchall()
    for i in datos:
        a.append({"CEDULA":i[1],"NOMBRE":i[2],"APELLIDO":i[3],"FECHA_P":i[7],"FECHA_S":i[8]})
    return a

@app.get('/api/List_Marca')
def List_Marca():
    a=[]
    conexion=sqlite3.connect('app.db')
    registro=conexion.cursor()
    registro.execute(''' SELECT V.MARCA, COUNT(VO.VACUNA) AS CANTIDAD
        FROM VACUNA V
        LEFT JOIN VACUNADO VO
        ON V.MARCA = VO.VACUNA
        GROUP BY V.MARCA ''')
    conexion.commit()
    datos = registro.fetchall()
    for i in datos:
        a.append({"MARCA":i[0],"CANTIDAD":i[1]})
    return a


@app.get('/api/Vacunas')
def Vacunas():
    a=[]
    conexion=sqlite3.connect('app.db')
    registro=conexion.cursor()
    data = registro.execute("SELECT * FROM VACUNA WHERE CANTIDAD > 0")
    conexion.commit()
    datos = data.fetchall()
    for i in datos:
        a.append({"MARCA": i[1]})
    return a

@app.get('/api/Provinvias')
def Provinvias():
    a=[]
    conexion=sqlite3.connect('app.db')
    registro=conexion.cursor()
    data = registro.execute("SELECT * FROM PROVINCIAS")
    conexion.commit()
    datos = data.fetchall()
    for i in datos:
        a.append({"ID":[0],"NOMBRE": i[1],"LATITUD":i[2],"LONGITUD":i[3]})
    return a


@app.get('/api/Vacunado_Provincia/{provincia}')
def Vacunado_Provincia(provincia: str):
    a = []
    conexion=sqlite3.connect('app.db')
    registro=conexion.cursor()
    registro.execute("SELECT * FROM VACUNADO WHERE PROVINCIA = '"+provincia+"'  ")
    conexion.commit()
    datos = registro.fetchall()
    for I in datos:
        a.append({"ID":I[0],"CEDULA":I[1],"NOMBRE":I[2],"APELLIDO":I[3],"FECHA_N":I[4],"VACUNA":I[5],"SIGNO":I[9]})
        return a

@app.get('/api/Vacunados_Todos')
def Vacunados_Todos():
    a = []
    conexion=sqlite3.connect('app.db')
    registro=conexion.cursor()
    registro.execute("SELECT * FROM VACUNADO")
    conexion.commit()
    datos = registro.fetchall()
    for I in datos:
        a.append({"ID":I[0],"CEDULA":I[1],"NOMBRE":I[2],"APELLIDO":I[3],"FECHA_N":I[4],"TELEFONO":I[5],"EMAIL":I[6],"SANGRE":I[7],"PROVINCIA":I[8],"DIRECCION":I[9],"LATITUD":I[10],"LONGITUD":I[11],"CONFIRMACION":I[12],"JUSTIFICACION":I[13]})
    return a





    




    











            



