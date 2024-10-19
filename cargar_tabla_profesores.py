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





conn = psycopg2.connect(conn_string)
# Conexión a la base de datos

try:
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    print("Conexión exitosa")

    # Ejecutar una consulta (ejemplo)
    cursor.execute("SELECT * FROM materias")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

except (Exception, psycopg2.Error) as error:
    print("Error al conectar a PostgreSQL", error)

finally:
    # Cerrar la conexión
    if (conn):
        cursor.close()
        conn.close()
        print("Conexión cerrada")




""""
conn_string = "postgresql:// :223369@localhost:5432/escuela"
conn = None
try:
    # Forzar la decodificación a UTF-8
    #conn_string = conn_string.encode('utf-8').decode('utf-8')


    conn = psycopg2.connect(conn_string)

    # Cargar el DataFrame a la tabla
    tabla = 'profesores'
    esquema = 'public'  # Ajusta si tienes un esquema diferente
    df_limpio.to_sql(tabla, conn, if_exists='replace', index=False, schema=esquema)


except UnicodeDecodeError as e:
    print(f"Error de decodificación: {e}")
    print("Verifica la cadena de conexión y la configuración de codificación.")
except psycopg2.Error as e:
    print(f"Error al conectar a la base de datos: {e}")
finally:
    if conn:
        conn.close()





conn_string = 'postgresql://postgre:223369@localhost:5432/escuela'

conn = psycopg2.connect(conn_string)

# Especificar la tabla y el esquema (si aplica)
tabla = 'profesores'
esquema = 'public'  # Ajusta si tienes un esquema diferente

# Cargar el DataFrame a la tabla
df_limpio.to_sql(tabla, conn, if_exists='replace', index=False, schema=esquema)

# Cerrar la conexión
conn.close()

"""