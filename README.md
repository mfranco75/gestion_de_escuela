<em> Gestión de Escuela </em>

Este proyecto parte de la necesidad de organizar los datos existentes de una Escuela y transformarlos en datos útiles para poder crear aplicaciones de consulta para estudiantes, profesores y directivos de la institucion.
Se parte de la base de que todos los datos estan cargados en planillas de excel que se edita y modifica desde la secretaria de la escuela, y tambien de planillas de excel que son generadas en la mariculación a partir de una carga inicial a traves de distintos formulario de google.
Entonces los datos estan distribuidos en distintos archivos que no estan relacionados y resulta muy dificil poder relaciones y consultas.
</p>PRIMER TAREA: descargar, normalizar y formatear los datos 
</p>El primer paso del proyecto consistió en descargar manualmente el archico "BESE DOCENTE 2024.xlsl" y escribir un codigo en python para transformarlo en un DataFrame con pandas.
</p>ARCHIVO limpiar_datos.py : contiene la funcion limpiar_dataframe que se encarga de normalizar con distintas funciones de texto y
aislar los valores numericos de las horas de inicio y fin de la materia para crear las columnas correspondientes al dia de cursada utilizando el modulo datetime para transformarlos en valores con formato time (Hora y minutos)
</p>ARCHIVO reconocer_comisiones.py : utiliza la funcion word_tokenize del modulo nltk.tokenize para extraer las comisiones de las materias
</p> Se cre la BASE DE DATOS "escuela" en PostgresSQL
</p>ARCHIVO conexion_postgres.py : se prueba la conexion con la Base de Datos
</p>ARCHIVO 
