const express = require('express');
const app = express();
const port = 3000;

// Endpoint para obtener horarios por docente
app.get('/horarios/docente/:nombre', (req, res) => {
    const nombre = req.params.nombre;
    // Aquí iría la lógica para consultar el dataframe
    res.send(`Horarios para el docente: ${nombre}`);
});

// Endpoint para obtener horarios por carrera y año
app.get('/horarios/carrera/:carrera/ano/:ano', (req, res) => {
    const carrera = req.params.carrera;
    const ano = req.params.ano;
    // Aquí iría la lógica para consultar el dataframe
    res.send(`Horarios para la carrera: ${carrera}, año: ${ano}`);
});

app.listen(port, () => {
    console.log(`Servidor escuchando en http://localhost:${port}`);
});
