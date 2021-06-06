const express = require('express');
const app = express();

app.use(express.json());

app.get(
    [
        "/hill_climbing",
        "/genetic_algorithm",
        "/simulated_annealing",
        "/neuronal_network",
    ],
    (request, response) => {
        console.log(request.body);
        response.send(request.body);
    }
);

app.listen(process.env.ACCESS_PORT);