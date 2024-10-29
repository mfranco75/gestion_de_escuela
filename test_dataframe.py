import pandas as pd

from limpiar_datos import limpiar_dataframe 
from reconocer_comisiones import extraer_comision



# ESTE SISTEMA FUNCIONA A PARTIR DE LA ESTRUCTURA ACTUAL DE EL ARCHIVO EXCEL DE LA INSTITUCION

# Se toman los datos de un archivo excel perteneciente al usuario de SECRETARIA de la cuenta 
# educativa de google de @abc.gob.ar, previamente descargado a la carpeta de este sistema

# LIMPIEZA Y NORMALIZADO DE LOS DATOS : los datos originales no estan normalizados, hay datos inválidos, filas en blanco y columnas que no se utilizan para nada
# se crea la funcion  normalizar y limpiar los datos

# nombre del archivo excel
path = "BASE DOCENTE 2024.xlsx"

#convierte el excel en un DataFrame
dataframe = pd.read_excel(path)
print(dataframe.info())

#llama a la funcion para limpiar y normalizar
df_limpio = limpiar_dataframe(dataframe)

df_con_comisiones = extraer_comision(df_limpio)

df_muestra = df_con_comisiones[['MATERIA', 'DOCENTE SUPLENTE', 'AÑO']].sample(n=150)

#Imprimir el DataFrame resultante
print(df_muestra)









