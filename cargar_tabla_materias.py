from limpiar_datos import limpiar_dataframe 

import pandas as pd
import psycopg2




# ESTE SISTEMA FUNCIONA A PARTIR DE LA ESTRUCTURA ACTUAL DE EL ARCHIVO EXCEL DE LA INSTITUCION

# Se toman los datos de un archivo excel perteneciente al usuario de SECRETARIA de la cuenta 
# educativa de google de @abc.gob.ar, previamente descargado a la carpeta de este sistema

# LIMPIEZA Y NORMALIZADO DE LOS DATOS : los datos originales no estan normalizados, hay datos inválidos, filas en blanco y columnas que no se utilizan para nada
# se crea la funcion  normalizar y limpiar los datos en el modulo limpiar_datos


path = "BASE DOCENTE 2024.xlsx"

#convierte el excel en un DataFrame
dataframe = pd.read_excel(path)

#llama a la funcion para limpiar y formatear el dataframe
df_limpio = limpiar_dataframe(dataframe)

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


# MODIFICAR A PARTIR DE ESTE PUNTO
# Función para insertar por cada fila el horario en la tabla 'horarios' y relacionarlo con la tabla 'materias' y la tabla 'profesores'



