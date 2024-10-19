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

# Función para insertar un registro si el apellido_nombre no existe
def insertar_profesor(apellido_nombre, dni, cuil, celular, correo_abc):
    cursor.execute("SELECT EXISTS(SELECT 1 FROM profesores WHERE apellido_nombre = %s)", (apellido_nombre,))
    existe = cursor.fetchone()[0]

    if not existe:
        cursor.execute("INSERT INTO profesores (apellido_nombre, dni, cuil, celular, correo_abc) VALUES (%s, %s, %s, %s, %s)",
                       (apellido_nombre, dni, cuil, celular, correo_abc))

# Iterar sobre las filas del DataFrame y llamar a la función de inserción
for index, row in df_limpio.iterrows():
    insertar_profesor(row['DOCENTE'], row['D.N.I'], row['CUIL'], row['CEL'], row['CORREO ABC'])

# Confirmar los cambios y cerrar la conexión
Connection.commit()
cursor.close()
Connection.close()

