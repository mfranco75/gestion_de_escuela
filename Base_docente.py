import pandas as pd
from datetime import datetime

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
            print(f"Hora Inicio {hora_inicio} : {minutos_inicio}")
            print(f"Hora Fin {hora_fin} : {minutos_fin}")
        elif len(numeros) == 7: #ejemplo  900 a 1100
            hora_inicio = int(numeros[:1])
            minutos_inicio = int(numeros[1:3])
            hora_fin = int(numeros[3:5])
            minutos_fin = int(numeros[5:]) 
            print(f"Hora Inicio {hora_inicio} : {minutos_inicio}")
            print(f"Hora Fin {hora_fin} : {minutos_fin}")    
        elif len(numeros) == 4: #ejemplo 19 a 23
            hora_inicio = int(numeros[:2])
            minutos_inicio = 0
            hora_fin = int(numeros[2:])
            minutos_fin = 0
            print(f"Hora Inicio {hora_inicio} : {minutos_inicio}")
            print(f"Hora Fin {hora_fin} : {minutos_fin}")
        elif len(numeros) == 3: # #ejemplo 9 a 10
            hora_inicio = int(numeros[:1])
            minutos_inicio = 0
            hora_fin = int(numeros[1:])
            minutos_fin = 0
            print(f"Hora Inicio {hora_inicio} : {minutos_inicio}")
            print(f"Hora Fin {hora_fin} : {minutos_fin}")
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

print(dataframe_docentes.loc[:, ['DOCENTE' , 'MATERIA' , 'LUNES_hora_inicio' , 'LUNES_hora_fin']])



#funcion IA formatear horarios de las cursadas
def limpiar_y_convertir_horario(horario_str):

    """
    Limpia la cadena de texto del horario y la convierte en un objeto datetime.

    Args:
        horario_str (str): Cadena de texto con el horario en formato "HHMM A HHMM".

    Returns:
        datetime.datetime: Objeto datetime representando el horario de inicio.
    """
  

    # Eliminar espacios en blanco y separar la cadena en horas de inicio y fin
    horario_limpio = horario_str.replace(" ", "").upper()
    hora_inicio, hora_fin = horario_limpio[:4], horario_limpio[5:]

    # Crear objetos datetime para el inicio y fin
    formato_hora = "%H%M"
    inicio = datetime.strptime(hora_inicio, formato_hora)
    fin = datetime.strptime(hora_fin, formato_hora)

    return inicio, fin





# Convertir las columnas de horario a tipo cadena (si es necesario)
#for dia in ['LUNES', 'MARTES', 'MIÉRCOLES', 'JUEVES', 'VIERNES', 'SÁBADO']:
#   dataframe_docentes[dia] = dataframe_docentes[dia].astype(str)
#   dataframe_docentes[dia] = dataframe_docentes[dia].fillna('').apply(limpiar_y_convertir_horario)

# Aplicar funcion al DataFrame
#for dia in ['LUNES', 'MARTES', 'MIERCOLES', 'JUEVES', 'VIERNES', 'SABADO']:
#    dataframe_docentes[dia] = dataframe_docentes[dia].astype(str)
#    dataframe_docentes[dia] = dataframe_docentes[dia].fillna('').apply(limpiar_y_convertir_horario)

#print(dataframe_docentes.dtypes)

#for dia in ['LUNES', 'MARTES', 'MIÉRCOLES', 'JUEVES', 'VIERNES', 'SÁBADO']:
#    if dataframe_docentes[dia].notnull :
#        print(dataframe_docentes[dia])

