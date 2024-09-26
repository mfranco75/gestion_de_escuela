import pandas as pd

path = "BASE DOCENTE 2024.xlsx"

#convierte el excel en un DataFrame
dataframe_docentes = pd.read_excel(path)

#renombrar algunas columnas


data = dataframe_docentes.rename(columns={'BASE IPA -2024CARRERAS-ASIGNATURAS POR AÑO-HORAS-DOCENTES.CUPOF-CODIGO CARRERA-- HORARIOS':'MATERIA' , 'Unnamed: 13':'DOCENTE' , 'APELLIDO Y NOMBRE':'DOCENTE SUPLENTE'})
print(data.info())


data2 = data['DOCENTE']
print(data2.sample(30))

#formatear horarios de las cursadas






