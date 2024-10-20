from limpiar_datos import limpiar_dataframe 
#from cargar_tabla_profesores import cargar_tabla
import pandas as pd


# ESTE SISTEMA FUNCIONA A PARTIR DE LA ESTRUCTURA ACTUAL DE EL ARCHIVO EXCEL DE LA INSTITUCION

# Se toman los datos de un archivo excel perteneciente al usuario de SECRETARIA de la cuenta 
# educativa de google de @abc.gob.ar, previamente descargado a la carpeta de este sistema

# LIMPIEZA Y NORMALIZADO DE LOS DATOS : los datos originales no estan normalizados, hay datos inválidos, filas en blanco y columnas que no se utilizan para nada
# se crea la funcion  normalizar y limpiar los datos

# nombre del archivo excel
path = "BASE DOCENTE 2024.xlsx"

#convierte el excel en un DataFrame
dataframe = pd.read_excel(path)

# llama a la funcion para limpiar y normalizar
df_limpio =limpiar_dataframe(dataframe)

print(df_limpio)

carreras = df_limpio['CARRERA'].unique()
print(carreras)



