import pandas as pd
import re
from datetime import time

def limpiar_dataframe(dataframe_docentes):
    
    #renombrar algunas columnas
    dataframe_docentes = dataframe_docentes.rename(columns={'BASE IPA -2024CARRERAS-ASIGNATURAS POR AÑO-HORAS-DOCENTES.CUPOF-CODIGO CARRERA-- HORARIOS':'MATERIA' , 'Unnamed: 13':'DOCENTE' , 'APELLIDO Y NOMBRE':'DOCENTE SUPLENTE'})

    #eliminar ultimas columnas
    dataframe_docentes = dataframe_docentes.drop(['Unnamed: 31', 'Unnamed: 33','Unnamed: 34','Unnamed: 35','Unnamed: 36'] , axis=1)
    dataframe_docentes = dataframe_docentes.drop(dataframe_docentes.columns[31], axis=1)
    
    # eliminar filas con MATERIA vacía
    dataframe_docentes = dataframe_docentes.dropna(subset=['MATERIA'])

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

    
    # agregar columnas para inicio y fin de la clase en cada dia de la semana
    dias = ['LUNES', 'MARTES', 'MIÉRCOLES', 'JUEVES', 'VIERNES', 'SÁBADO']
    sufijos = ['hora_inicio', 'hora_fin']

    # Eliminar caracteres no numéricos y convertir a entero LAS COLUMNAS DNI , CUIL y AÑO

    dataframe_docentes['D.N.I'] = dataframe_docentes['D.N.I'].fillna(' ').astype(str)
    dataframe_docentes['D.N.I'] = dataframe_docentes['D.N.I'].str.replace(r'\D', '', regex=True)

    dataframe_docentes['CUIL'] = dataframe_docentes['CUIL'].fillna(' ').astype(str)
    dataframe_docentes['CUIL'] = dataframe_docentes['CUIL'].str.replace(r'\D', '', regex=True)

    dataframe_docentes['AÑO'] = dataframe_docentes['AÑO'].fillna(' ').astype(str)
    dataframe_docentes['AÑO'] = dataframe_docentes['AÑO'].str.replace(r'\D', '', regex=True)



    # Crear las nuevas columnas
    for dia in dias:
        for sufijo in sufijos:
            nombre_columna = f"{dia}_{sufijo}"
            dataframe_docentes[nombre_columna] = ' '

    # transformar el texto de horario de inicio y fin a formato horario (time)
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
                hora_inicio_datetime = time(hora_inicio,minutos_inicio)
                hora_fin_datetime = time(hora_fin, minutos_fin)
                dataframe_docentes.loc[i,columna_inicio] = hora_inicio_datetime
                dataframe_docentes.loc[i,columna_fin] = hora_fin_datetime
            else:
                hora_inicio = time(0, 0)
                minutos_inicio = time(0, 0)
                hora_fin = time(0, 0)
                minutos_fin = time(0, 0)
                dataframe_docentes.loc[i,columna_inicio] = hora_inicio
                dataframe_docentes.loc[i,columna_fin] = hora_fin

    return dataframe_docentes
