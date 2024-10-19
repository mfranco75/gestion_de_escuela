import psycopg2

try:
    Connection = psycopg2.connect(
        host = 'localhost',
        user = 'postgres',
        password = '223369',
        database = 'escuela',
        port = '5432'
    )
    print("conexion existosa")
except Exception as ex:
    print(ex)

Connection.autocommit = True

def crearTabla():
    cursor = Connection.cursor()
    query = "CREATE TABLE usuario(nombre varchar(30), correo varchar(30),tipo_usuario varchar(15))"
    cursor.execute(query)
    cursor.close()

crearTabla()