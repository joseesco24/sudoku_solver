import check_request_mandatory_requirements from "./validator.mjs";
import print_log from "./general_utilities.mjs";

import express from "express";
import axios from "axios";

const script_firm = "api";
const api = express();

api.use(express.json());

async function proxy_redirect(
    authorization,
    body,
    destination_url,
    origin_url,
    response
) {
    print_log(`making request to ${destination_url}`, script_firm);
    const api_response = await axios({
        headers: {
            "Content-Type": "application/json",
            "Authorization": authorization,
        },
        url: destination_url,
        method: "get",
        data: body,
    });
    print_log(`receiving response from ${destination_url}`, script_firm);
    print_log(`routing from ${destination_url} to ${origin_url}`, script_firm);
    if (api_response.status == 200) {
        return response.status(api_response.status).json(api_response.data);
    } else {
        return response.status(api_response.status).send(api_response.statusText);
    }
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
        const origin_server = request.protocol + "://" + request.get("host");
        const origin_url = origin_server + request.originalUrl;
        print_log(`request origin ${origin_url}`, script_firm);
        const [valid_request_body, message] = check_request_mandatory_requirements(
            request.body
        );
        print_log(
            `request body validation status: ${valid_request_body}`,
            script_firm
        );
        if (valid_request_body == true) {
            try {
                const original_path = request.path;
                let destination_url, authorization;
                if (original_path == "/hill_climbing") {
                    destination_url = process.env.HILL_CLIMBING_SOLVER_LINK;
                    authorization = process.env.HILL_CLIMBING_SOLVER_KEY;
                    return await proxy_redirect(
                        authorization,
                        request.body,
                        destination_url,
                        origin_url,
                        response
                    );
                }
                if (original_path == "/genetic_algorithm") {
                    destination_url = process.env.GENETIC_ALGORITHM_SOLVER_LINK;
                    authorization = process.env.GENETIC_ALGORITHM_SOLVER_KEY;
                    return await proxy_redirect(
                        authorization,
                        request.body,
                        destination_url,
                        origin_url,
                        response
                    );
                }
                if (original_path == "/simulated_annealing") {
                    destination_url = process.env.HILL_CLIMBING_SOLVER_LINK;
                    authorization = process.env.HILL_CLIMBING_SOLVER_KEY;
                    return await proxy_redirect(
                        authorization,
                        request.body,
                        destination_url,
                        origin_url,
                        response
                    );
                }
                if (original_path == "/neuronal_network") {
                    destination_url = process.env.HILL_CLIMBING_SOLVER_LINK;
                    authorization = process.env.HILL_CLIMBING_SOLVER_KEY;
                    return await proxy_redirect(
                        authorization,
                        request.body,
                        destination_url,
                        origin_url,
                        response
                    );
                }
            } catch (error) {
                if (typeof error === "object") {
                    print_log(`server error ${error.message}`, script_firm);
                }
                return response.status(500).send("internal server error");
            }
        } else if (valid_request_body == false) {
            print_log(`request body validation failed: ${message}`, script_firm);
            return response.status(415).send(message);
        }
    }
);

api.listen(process.env.ACCESS_PORT);