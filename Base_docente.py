import pandas as pd

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
print(dataframe_docentes.info())

# agregar columnas para inicio y fin de la clase en cada dia de la semana
dias = ['LUNES', 'MARTES', 'MIÉRCOLES', 'JUEVES', 'VIERNES', 'SÁBADO']
sufijos = ['hora_inicio', 'hora_fin']

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


## FUNCIONES para buscar y filtrar

# mostrar las materias dictadas por un docente espesífico

#def buscar_materias_de_docente

# no anda!!!!
#for dia in [dias]:
#    for i in range(len(dataframe_docentes)):
#        hora =dataframe_docentes.iloc[i , f'{dia}_hora_inicio']
#        print(hora)
#
# 
#print(dataframe_docentes.dtypes)


# Suponiendo que tienes tu DataFrame cargado en una variable llamada df
# Y que las columnas tienen el formato "DIA_horario_inicio" y "DIA_horario_fin"

print(dataframe_docentes.info())
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
imprimir_clases(dataframe_docentes)
