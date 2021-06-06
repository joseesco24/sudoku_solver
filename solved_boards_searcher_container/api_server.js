const express = require("express");
const axios = require("axios");

const app = express();

app.use(express.json());

async function proxy_redirect(local_authorization, local_body, local_url) {
    const api_response = await axios({
        headers: {
            Authorization: local_authorization,
            "Content-Type": "application/json",
        },
        data: local_body,
        url: local_url,
        method: "get",
    });
    return api_response;
}

app.get(
    [
        "/hill_climbing",
        "/genetic_algorithm",
        "/simulated_annealing",
        "/neuronal_network",
    ],
    async (request, response) => {
        const original_path = request.path;
        let api_response;

        if (original_path == "/hill_climbing") {
            api_response = await proxy_redirect(
                process.env.HILL_CLIMBING_SOLVER_KEY,
                request.body,
                process.env.HILL_CLIMBING_SOLVER_LINK
            );
            if (api_response.status == 200) {
                return response.status(api_response.status).json(api_response.data);
            } else {
                return response
                    .status(api_response.status)
                    .send(api_response.statusText);
            }
        }

        if (original_path == "/genetic_algorithm") {
            api_response = await proxy_redirect(
                process.env.GENETIC_ALGORITHM_SOLVER_KEY,
                request.body,
                process.env.GENETIC_ALGORITHM_SOLVER_LINK
            );
            if (api_response.status == 200) {
                return response.status(api_response.status).json(api_response.data);
            } else {
                return response
                    .status(api_response.status)
                    .send(api_response.statusText);
            }
        }

        if (original_path == "/simulated_annealing") {
            api_response = await proxy_redirect(
                process.env.GENETIC_ALGORITHM_SOLVER_KEY,
                request.body,
                process.env.GENETIC_ALGORITHM_SOLVER_LINK
            );
            if (api_response.status == 200) {
                return response.status(api_response.status).json(api_response.data);
            } else {
                return response
                    .status(api_response.status)
                    .send(api_response.statusText);
            }
        }

        if (original_path == "/neuronal_network") {
            api_response = await proxy_redirect(
                process.env.GENETIC_ALGORITHM_SOLVER_KEY,
                request.body,
                process.env.GENETIC_ALGORITHM_SOLVER_LINK
            );
            if (api_response.status == 200) {
                return response.status(api_response.status).json(api_response.data);
            } else {
                return response
                    .status(api_response.status)
                    .send(api_response.statusText);
            }
        }
    }
);

app.listen(process.env.ACCESS_PORT);