from limpiar_datos import limpiar_dataframe 

import pandas as pd
import re
from datetime import datetime , time

# ESTE SISTEMA FUNCIONA A PARTIR DE LA ESTRUCTURA ACTUAL DE EL ARCHIVO EXCEL DE LA INSTITUCION

# Se toman los datos de un archivo excel perteneciente al usuario de SECRETARIA de la cuenta 
# educativa de google de @abc.gob.ar, previamente descargado a la carpeta de este sistema

# LIMPIEZA Y NORMALIZADO DE LOS DATOS : los datos originales no estan normalizados, hay datos inválidos, filas en blanco y columnas que no se utilizan para nada
# se crea la funcion  normalizar y limpiar los datos


path = "BASE DOCENTE 2024.xlsx"

#convierte el excel en un DataFrame
dataframe_docentes = pd.read_excel(path)

df_limpio =limpiar_dataframe(dataframe_docentes)

print(df_limpio)