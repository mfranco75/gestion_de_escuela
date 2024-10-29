from limpiar_datos import limpiar_dataframe 
from reconocer_comisiones import extraer_comision

import pandas as pd
import psycopg2
from datetime import time



# ESTE SISTEMA FUNCIONA A PARTIR DE LA ESTRUCTURA ACTUAL DE EL ARCHIVO EXCEL DE LA INSTITUCION

# Se toman los datos de un archivo excel perteneciente al usuario de SECRETARIA de la cuenta 
# educativa de google de @abc.gob.ar, previamente descargado a la carpeta de este sistema

# LIMPIEZA Y NORMALIZADO DE LOS DATOS : los datos originales no estan normalizados, hay datos inválidos, filas en blanco y columnas que no se utilizan para nada
# se crea la funcion "limpiar_dataframe" para normalizar y limpiar los datos en el modulo limpiar_datos


path = "BASE DOCENTE 2024.xlsx"

#convierte el excel en un DataFrame
dataframe = pd.read_excel(path)

#llama a la funcion para limpiar y formatear el dataframe
df_limpio = limpiar_dataframe(dataframe)

#crea columna para COMISION

df_con_comision = extraer_comision(df_limpio)



#conexion a la BASE DE DATOS
try:
    Connection = psycopg2.connect(
        host = 'localhost',
        user = 'postgres',
        password = '223369',
        database = 'escuela',
        port = '5432'
    )
    print("conexion existosa")
except Exception as ex:
    print(ex)

Connection.autocommit = True

# Crear un cursor para ejecutar las consultas
cursor = Connection.cursor()

#funciones
def convertir_a_numero(valor):
    try:
        return int(valor)
    except ValueError:
        return 0

#insertar materias

def insertar_horario(materia,id_carrera,id_profesor,suplente,dia, hora_inicio,hora_fin, nivel, comision):
    cursor.execute("INSERT INTO horarios(materia, carrera_id, profesor_id, suplente, dia, hora_inicio, hora_fin, nivel, comision) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                       (materia, id_carrera, id_profesor, suplente, dia,hora_inicio, hora_fin, nivel, comision,))
    
# Función para insertar un registro si el apellido_nombre no existe

def insertar_profesor(apellido_nombre, dni, cuil, celular, correo_abc):
    cursor.execute("SELECT EXISTS(SELECT 1 FROM profesores WHERE apellido_nombre = %s)", (apellido_nombre,))
    existe = cursor.fetchone()[0]

    if not existe:
        cursor.execute("INSERT INTO profesores (apellido_nombre, dni, cuil, celular, correo_abc) VALUES (%s, %s, %s, %s, %s)",
                       (apellido_nombre, dni, cuil, celular, correo_abc))


# Función para insertar un registro si la carrera no existe
def insertar_carrera(nombre_carrera):
    cursor.execute("SELECT EXISTS(SELECT 1 FROM carreras WHERE nombre_carrera = %s)", (nombre_carrera,))
    existe = cursor.fetchone()[0]

    if not existe:
        cursor.execute("INSERT INTO carreras (nombre_carrera) VALUES (%s)",(nombre_carrera,))




# Iterar sobre las filas del DataFrame y llamar a la función de inserción
for index, row in df_con_comision.iterrows():
    insertar_profesor(row['DOCENTE'], row['D.N.I'], row['CUIL'], row['CEL'], row['CORREO ABC'])
    profesor = row['DOCENTE']
    query = f"SELECT id FROM profesores WHERE apellido_nombre = '{profesor}'"
    cursor.execute(query)
    id_profesor = cursor.fetchone()
    suplente = row['DOCENTE SUPLENTE']

    insertar_carrera(row['CARRERA'])
    carrera = row['CARRERA']
    query = f"SELECT id FROM carreras WHERE nombre_carrera = '{carrera}'"
    cursor.execute(query)
    id_carrera = cursor.fetchone()
    nivel = row['AÑO']
    nivel = convertir_a_numero(nivel)
    
    if row['LUNES_hora_inicio'] > time(7,0):
        dia = 'LUNES'
        hora_inicio = row['LUNES_hora_inicio']
        hora_fin = row['LUNES_hora_fin']
        materia = row['MATERIA']
        comision = row['COMISION']
        insertar_horario(materia,id_carrera,id_profesor,suplente,dia, hora_inicio,hora_fin, nivel, comision)
    
    if row['MARTES_hora_inicio'] > time(7,0):
        dia = 'MARTES'
        hora_inicio = row['MARTES_hora_inicio']
        hora_fin = row['MARTES_hora_fin']
        materia = row['MATERIA']
        comision = row['COMISION']
        insertar_horario(materia,id_carrera,id_profesor,suplente,dia, hora_inicio,hora_fin, nivel, comision)

                
    if row['MIÉRCOLES_hora_inicio'] > time(7,0):
        dia = 'MIÉRCOLES'
        hora_inicio = row['MIÉRCOLES_hora_inicio']
        hora_fin = row['MIÉRCOLES_hora_fin']
        materia = row['MATERIA']
        comision = row['COMISION']
        insertar_horario(materia,id_carrera,id_profesor,suplente,dia, hora_inicio,hora_fin, nivel, comision)

        

    if row['JUEVES_hora_inicio'] > time(7,0):
        dia = 'JUEVES'
        hora_inicio = row['JUEVES_hora_inicio']
        hora_fin = row['JUEVES_hora_fin']
        materia = row['MATERIA']
        comision = row['COMISION']
        insertar_horario(materia,id_carrera,id_profesor,suplente,dia, hora_inicio,hora_fin, nivel, comision)

        

    
    if row['VIERNES_hora_inicio'] > time(7,0):
        dia = 'VIERNES'
        hora_inicio = row['VIERNES_hora_inicio']
        hora_fin = row['VIERNES_hora_fin']
        materia = row['MATERIA']
        comision = row['COMISION']
        insertar_horario(materia,id_carrera,id_profesor,suplente,dia, hora_inicio,hora_fin, nivel, comision)


    if row['SÁBADO_hora_inicio'] > time(7,0):
        dia = 'SÁBADO'
        hora_inicio = row['SÁBADO_hora_inicio']
        hora_fin = row['SÁBADO_hora_fin']
        materia = row['MATERIA']
        comision = row['COMISION']
        insertar_horario(materia,id_carrera,id_profesor,suplente,dia, hora_inicio,hora_fin, nivel, comision)
    





    
    
    #insertar_materia(row['MATERIA'], row[])

    #recorrer Hora Inicio de lunes a sabado : si es > a 00.00 
    #    insertar_horario



# Confirmar los cambios y cerrar la conexión
Connection.commit()
cursor.close()
Connection.close()






