CREATE TABLE materias (
    id SERIAL PRIMARY KEY,
    nombre TEXT,
    carrera TEXT,
	año INTEGER,
	comision TEXT
);

CREATE TABLE profesores (
    id SERIAL PRIMARY KEY,
    apellido_nombre TEXT,
	dni INTEGER ,
	cuil INTEGER ,
    celular TEXT ,
	correo_abc TEXT,
	fecha_nacimiento TIME 	
);

CREATE TABLE horarios (
    id SERIAL PRIMARY KEY,
    materia_id INTEGER REFERENCES materias(id),
    profesor_id INTEGER REFERENCES profesores(id),
    dia TEXT,
    hora_inicio TIME ,
	hora_fin TIME
);