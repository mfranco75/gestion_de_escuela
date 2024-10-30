<em> Gestión de Escuela </em>

Este proyecto parte de la necesidad de organizar los datos existentes de una Escuela y transformarlos en datos útiles para poder crear aplicaciones de consulta para estudiantes, profesores y directivos de la institucion.
Se parte de la base de que todos los datos estan cargados en planillas de excel que se editan y modifican desde la secretaria de la escuela, y tambien de otras planillas de excel que son generadas en la mariculación a partir de una carga inicial a traves de distintos formulario de google.
Entonces los datos estan distribuidos en distintos archivos que no estan relacionados y resulta muy difícil poder establecer relaciones y consultas.
</p>PRIMER TAREA: descargar, normalizar y formatear los datos 
</p>El primer paso del proyecto consistió en descargar manualmente el archico "BESE DOCENTE 2024.xlsl" y escribir un codigo en python para transformarlo en un DataFrame con pandas.
</p>ARCHIVO limpiar_datos.py : contiene la funcion limpiar_dataframe que se encarga de normalizar con distintas funciones de texto y aislar los valores numericos de las horas de inicio y fin de la materia para crear las columnas correspondientes al dia de cursada utilizando el modulo datetime para transformarlos en valores con formato time (Hora y minutos)
</p>ARCHIVO reconocer_comisiones.py : utiliza la funcion word_tokenize del modulo nltk.tokenize para extraer del texto las comisiones de las materias
</p> Se cre la BASE DE DATOS "escuela" en PostgresSQL con las tablas : usuario, carreras, profesores y horarios
</p> ARCHIVO ESCUELA SCHEMA POSTGREE SQL.sql : contiene la estructura de las tablas de la base de datos
</p>ARCHIVO conexion_postgres.py : se prueba la conexion con la Base de Datos
</p>ARCHIVO cargar_tabla_carreras.py : contiene la funcion insertar_carrera : que inserta los datos en la tabla 'carreras' (solo si no existe)
</p>ARCHIVO cargar_tabla_profesores.py : contiene la funcion insertar_profesor : que inserta los datos en la tabla 'profesores' (solo si no existe)
</p>ARCHIVO cargar_tabla_materias_con_horarios.py : contiene el procedimiento principal que recorre al dataframe e inserta en la tabla horarios todos los datos de la materia junto con el id del profesor y el id de la carrera utilizando las funciones insertar_profesor e insertar_carrera si es necesario. De esta manera ya se cuenta con una base de datos relacional para empezar a trabajar en la aplicacion de consultas

