import print_log from "./general_utilities.mjs";

import express from "express";
import axios from "axios";

const script_firm = "api";
const api = express();

api.use(express.json());

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

api.get(
    [
        "/hill_climbing",
        "/genetic_algorithm",
        "/simulated_annealing",
        "/neuronal_network",
    ],
    async (request, response) => {
        print_log(`new request received at ${request.path}`, script_firm);
        const full_url =
            request.protocol + "://" + request.get("host") + request.originalUrl;

        print_log(`request origin ${full_url}`, script_firm);

        try {
            const original_path = request.path;
            let api_response, routing_link, authorization;

            if (original_path == "/hill_climbing") {
                routing_link = process.env.HILL_CLIMBING_SOLVER_LINK;
                authorization = process.env.HILL_CLIMBING_SOLVER_KEY;
                print_log(`making request to ${routing_link}`, script_firm);
                api_response = await proxy_redirect(
                    authorization,
                    request.body,
                    routing_link
                );
                print_log(`receiving response from ${routing_link}`, script_firm);
                print_log(
                    `sending response from ${routing_link} to ${full_url}`,
                    script_firm
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
                routing_link = process.env.GENETIC_ALGORITHM_SOLVER_LINK;
                authorization = process.env.GENETIC_ALGORITHM_SOLVER_KEY;
                print_log(`making request to ${routing_link}`, script_firm);
                api_response = await proxy_redirect(
                    authorization,
                    request.body,
                    routing_link
                );
                print_log(`receiving response from ${routing_link}`, script_firm);
                print_log(
                    `sending response from ${routing_link} to ${full_url}`,
                    script_firm
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
                routing_link = process.env.HILL_CLIMBING_SOLVER_LINK;
                authorization = process.env.HILL_CLIMBING_SOLVER_KEY;
                print_log(`making request to ${routing_link}`, script_firm);
                api_response = await proxy_redirect(
                    authorization,
                    request.body,
                    routing_link
                );
                print_log(`receiving response from ${routing_link}`, script_firm);
                print_log(
                    `sending response from ${routing_link} to ${full_url}`,
                    script_firm
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
                routing_link = process.env.HILL_CLIMBING_SOLVER_LINK;
                authorization = process.env.HILL_CLIMBING_SOLVER_KEY;
                print_log(`making request to ${routing_link}`, script_firm);
                api_response = await proxy_redirect(
                    authorization,
                    request.body,
                    routing_link
                );
                print_log(`receiving response from ${routing_link}`, script_firm);
                print_log(
                    `sending response from ${routing_link} to ${full_url}`,
                    script_firm
                );
                if (api_response.status == 200) {
                    return response.status(api_response.status).json(api_response.data);
                } else {
                    return response
                        .status(api_response.status)
                        .send(api_response.statusText);
                }
            }
        } catch (error) {
            if (typeof error === "object") {
                print_log(
                    `server error ${error.message} in line ${error.lineno}`,
                    script_firm
                );
            }
            return response.status(500).send("internal server error");
        }
    }
);

api.listen(process.env.ACCESS_PORT);