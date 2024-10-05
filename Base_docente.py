import pandas as pd
import psycopg2
import re


from datetime import datetime , time
#from flask import Flask, request, render_template_string

path = "BASE DOCENTE 2024.xlsx"

#convierte el excel en un DataFrame
dataframe_docentes = pd.read_excel(path)

#renombrar algunas columnas
dataframe_docentes = dataframe_docentes.rename(columns={'BASE IPA -2024CARRERAS-ASIGNATURAS POR AÑO-HORAS-DOCENTES.CUPOF-CODIGO CARRERA-- HORARIOS':'MATERIA' , 'Unnamed: 13':'DOCENTE' , 'APELLIDO Y NOMBRE':'DOCENTE SUPLENTE'})

#eliminar ultimas columnas
dataframe_docentes = dataframe_docentes.drop(['Unnamed: 31', 'Unnamed: 33','Unnamed: 34','Unnamed: 35','Unnamed: 36'] , axis=1)
dataframe_docentes = dataframe_docentes.drop(dataframe_docentes.columns[31], axis=1)
# eliminar filas con MATERIA vacía
dataframe_docentes = dataframe_docentes.dropna(subset=['MATERIA'])

# agregar columnas para inicio y fin de la clase en cada dia de la semana
dias = ['LUNES', 'MARTES', 'MIÉRCOLES', 'JUEVES', 'VIERNES', 'SÁBADO']
sufijos = ['hora_inicio', 'hora_fin']

# Eliminar caracteres no numéricos y convertir a entero LAS COLUMNAS DNI Y CUIL

dataframe_docentes['D.N.I'] = dataframe_docentes['D.N.I'].fillna(' ').astype(str)
dataframe_docentes['D.N.I'] = dataframe_docentes['D.N.I'].str.replace(r'\D', '', regex=True)

dataframe_docentes['CUIL'] = dataframe_docentes['CUIL'].fillna(' ').astype(str)
dataframe_docentes['CUIL'] = dataframe_docentes['CUIL'].str.replace(r'\D', '', regex=True)


print(dataframe_docentes[['DOCENTE', 'SUPLENTE', 'D.N.I' , 'CUIL']])
print(dataframe_docentes.info())

#print(dataframe_docentes['CUIL'])

# Crear las nuevas columnas
for dia in dias:
    for sufijo in sufijos:
        nombre_columna = f"{dia}_{sufijo}"
        dataframe_docentes[nombre_columna] = ' '

# transformar el texto de horario de inicio y fin a formato horario (datetime)
#se recorre los campos de dia y se extrae de la cadena de caracteres solo los caracteres numericos para luego transformarlos en hora de inicio y hora de fin
formato_hora = "%H%M"
for dia in ['LUNES', 'MARTES', 'MIÉRCOLES', 'JUEVES', 'VIERNES', 'SÁBADO']:
    for i in range(len(dataframe_docentes)):
        cadena = str(dataframe_docentes.iloc[i] [dia]) 
        numeros= ''.join(filter(str.isdigit, cadena))
        columna_inicio = f"{dia}_hora_inicio"
        columna_fin = f"{dia}_hora_fin"

        if len(numeros) == 8: #ej 1840 a 2040
            hora_inicio = int(numeros[:2])
            minutos_inicio = int(numeros[2:4])
            hora_fin = int(numeros[4:6])
            minutos_fin = int(numeros[6:]) 
            
        elif len(numeros) == 7: #ejemplo  900 a 1100
            hora_inicio = int(numeros[:1])
            minutos_inicio = int(numeros[1:3])
            hora_fin = int(numeros[3:5])
            minutos_fin = int(numeros[5:]) 
             
        elif len(numeros) == 4: #ejemplo 19 a 23
            hora_inicio = int(numeros[:2])
            minutos_inicio = 0
            hora_fin = int(numeros[2:])
            minutos_fin = 0
            
        elif len(numeros) == 3: # #ejemplo 9 a 10
            hora_inicio = int(numeros[:1])
            minutos_inicio = 0
            hora_fin = int(numeros[1:])
            minutos_fin = 0
            
        else:
            hora_inicio = 0
            minutos_inicio = 0
            hora_fin = 0
            minutos_fin = 0


        #guardar en las columas de lunes_hora_inicio y lunes_hora fin etc)
        if hora_inicio <=24 and hora_fin <=24 and minutos_inicio <=60 and minutos_fin<=60:
            hora_inicio_datetime = datetime.strptime(f"{hora_inicio:02d}:{minutos_inicio:02d}", "%H:%M")
            hora_fin_datetime = datetime.strptime(f"{hora_fin:02d}:{minutos_fin:02d}", "%H:%M")
            dataframe_docentes.loc[i,columna_inicio] = hora_inicio_datetime
            dataframe_docentes.loc[i,columna_fin] = hora_fin_datetime
        else:
            hora_inicio = time(0, 0)
            minutos_inicio = time(0, 0)
            hora_fin = time(0, 0)
            minutos_fin = time(0, 0)
            dataframe_docentes.loc[i,columna_inicio] = hora_inicio
            dataframe_docentes.loc[i,columna_fin] = hora_fin


## Limpiar apellidos y nombres de DOCENTE y SUPLENTE
dataframe_docentes['DOCENTE'] = dataframe_docentes['DOCENTE'].astype(str)  # Convert to string if necessary
dataframe_docentes['DOCENTE'] = dataframe_docentes['DOCENTE'].fillna('')  # Fill missing values

dataframe_docentes['DOCENTE SUPLENTE'] = dataframe_docentes['DOCENTE SUPLENTE'].astype(str)  # Convert to string if necessary
dataframe_docentes['DOCENTE SUPLENTE'] = dataframe_docentes['DOCENTE SUPLENTE'].fillna('')  # Fill missing values


dataframe_docentes['DOCENTE'] = dataframe_docentes['DOCENTE'].str.rstrip()
dataframe_docentes['DOCENTE SUPLENTE'] = dataframe_docentes['DOCENTE SUPLENTE'].str.rstrip()

# eliminar la coma entre apellido y nombre
dataframe_docentes['DOCENTE'] = dataframe_docentes['DOCENTE'].str.replace(',', '')
dataframe_docentes['DOCENTE SUPLENTE'] = dataframe_docentes['DOCENTE SUPLENTE'].str.replace(',', '')

lista_docentes_unicos = dataframe_docentes['DOCENTE'].unique().tolist()
lista_suplentes_unicos = dataframe_docentes['DOCENTE SUPLENTE'].unique().tolist()

#for docente in lista_docentes_unicos:
#    print(docente)

#for suplente in lista_suplentes_unicos:
#    print(suplente)





## FUNCIONES para buscar y filtrar


#print(dataframe_docentes.info())

def imprimir_clases(df):
    """Imprime las materias, docentes y horarios de las clases que comienzan después de las 00:00.

    Args:
        df (pandas.DataFrame): El DataFrame con los datos.
    """

    dias_semana = ['LUNES', 'MARTES', 'MIÉRCOLES', 'JUEVES', 'VIERNES', 'SÁBADO']
    for index, row in df.iterrows():
        for dia in dias_semana:
            hora_inicio = row[f"{dia}_hora_inicio"]
            if hora_inicio.hour > 0:
                print(f"Materia: {row['MATERIA']}, Docente: {row['DOCENTE']}, Día: {dia}, Hora inicio: {hora_inicio.strftime("%H:%M")}")

# Ejemplo de uso:
#imprimir_clases(dataframe_docentes)


def obtener_materias_con_horario(df):
    """Devuelve un DataFrame con las materias, docentes, días y horas de inicio  y hora de fin.

    Args:
        df (pandas.DataFrame): El DataFrame con los datos.

    Returns:
        pandas.DataFrame: Un DataFrame con las columnas 'MATERIA', 'DOCENTE', 'DIA', '{DIA}HORA_INICIO', '{DIA}HORA_FIN'.
    """

    # Creamos una lista vacía para almacenar los datos de las clases
    clases = []

    dias_semana = ['LUNES', 'MARTES', 'MIÉRCOLES', 'JUEVES', 'VIERNES', 'SÁBADO']
    for index, row in df.iterrows():
        for dia in dias_semana:
            hora_inicio = row[f"{dia}_hora_inicio"]
            hora_fin = row[f"{dia}_hora_fin"]
            if hora_inicio.hour > 0:
                clases.append({
                    'MATERIA': row['MATERIA'],
                    'DOCENTE': row['DOCENTE'],
                    'DIA': dia,
                    f'{dia}_HORA_INICIO': hora_inicio.strftime("%H:%M"),
                    f'{dia}_HORA_FIN' : hora_fin.strftime("%H:%M")
                                })

    # Convertimos la lista de diccionarios en un DataFrame
    return pd.DataFrame(clases)

# Ejemplo de uso: devuelve dataframe con horarios, se deben mostrar solo los horarios mayores a 00:00
#dataframe_con_clases = obtener_materias_con_horario(dataframe_docentes)
#print(dataframe_con_clases)

def obtener_agenda_clases_detalle(df):
    """Devuelve un DataFrame con las clases en formato de agenda, incluyendo horarios de inicio y fin.

    Args:
        df (pandas.DataFrame): El DataFrame con los datos.

    Returns:
        pandas.DataFrame: Un DataFrame con las columnas 'MATERIA', 'DOCENTE', 'LUNES_INICIO', 'LUNES_FIN', ..., 'SÁBADO_INICIO', 'SÁBADO_FIN'.
    """

    # Creamos un nuevo DataFrame con las columnas deseadas
    agenda = df[['MATERIA', 'DOCENTE']].copy()

    # Agregamos las columnas para los días de la semana, tanto para inicio como para fin
    dias_semana = ['LUNES', 'MARTES', 'MIÉRCOLES', 'JUEVES', 'VIERNES', 'SÁBADO']
    for dia in dias_semana:
        agenda[f"{dia}_INICIO"] = df[f"{dia}_hora_inicio"].apply(lambda x: x.strftime("%H:%M") if x.hour > 0 else "")
        agenda[f"{dia}_FIN"] = df[f"{dia}_hora_fin"].apply(lambda x: x.strftime("%H:%M") if x.hour > 0 else "")

    return agenda

# Ejemplo de uso:
#dataframe_agenda_detalle = obtener_agenda_clases_detalle(dataframe_docentes)
#print(dataframe_agenda_detalle)



