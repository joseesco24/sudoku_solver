import check_header_request_mandatory_requirements from "./header_validator.mjs";

import check_body_request_mandatory_requirements from "./body_validator.mjs";

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
    response,
    health_test_url
) {
    print_log(
        `making server health test using the path ${health_test_url}`,
        script_firm
    );
    let resume;
    try {
        const health_test_response = await axios({
            url: health_test_url,
            method: "get",
            timeout: 1000,
        });
        print_log(`reciving response from ${health_test_url}`, script_firm);
        print_log(`health test code: ${health_test_response.status}`, script_firm);
        if (health_test_response.status == 200) {
            resume = true;
        }
    } catch (error) {
        if (typeof error === "object") {
            print_log(`health test error ${error.message}`, script_firm);
        }
        print_log(`health test to ${health_test_url} failed`, script_firm);
        resume = false;
    }
    if (resume == true) {
        print_log(`starting to solve using ${destination_url} solver`, script_firm);
        print_log(`making request to ${destination_url}`, script_firm);
        const solver_response = await axios({
            headers: {
                "Content-Type": "application/json",
                "Authorization": authorization,
            },
            url: destination_url,
            method: "get",
            data: body,
        });
        print_log(`reciving response from ${destination_url}`, script_firm);
        print_log(`routing from ${destination_url} to ${origin_url}`, script_firm);
        if (solver_response.status == 200) {
            response.statusMessage = "OK";
            return response.status(solver_response.status).json(solver_response.data);
        } else {
            response.statusMessage = solver_response.statusText;
            return response.status(solver_response.status).end();
        }
    } else {
        print_log(`failed to solve using ${destination_url} solver`, script_firm);
        response.statusMessage = `the requested solver is not currently working, please use other solver or request it later`;
        return response.status(500).end();
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
        const origin_url =
            request.protocol + "://" + request.get("host") + request.originalUrl;
        print_log(`request origin url ${origin_url}`, script_firm);
        const [valid_request_header, header_validation_message] =
        check_header_request_mandatory_requirements(request.headers);
        print_log(
            `request header validation status: ${valid_request_header}`,
            script_firm
        );
        if (valid_request_header == true) {
            const [valid_request_body, body_validation_message] =
            check_body_request_mandatory_requirements(request.body);
            print_log(
                `request body validation status: ${valid_request_body}`,
                script_firm
            );
            if (valid_request_body == true) {
                try {
                    const original_path = request.path;
                    let destination_url, authorization, health_test_url;
                    if (original_path == "/hill_climbing") {
                        health_test_url = process.env.HILL_CLIMBING_SOLVER_HEALTH_TEST_LINK;
                        destination_url = process.env.HILL_CLIMBING_SOLVER_LINK;
                        authorization = process.env.HILL_CLIMBING_SOLVER_KEY;
                        return await proxy_redirect(
                            authorization,
                            request.body,
                            destination_url,
                            origin_url,
                            response,
                            health_test_url
                        );
                    }
                    if (original_path == "/genetic_algorithm") {
                        health_test_url = process.env.GENETIC_ALGORITHM_SOLVER_HEALTH_TEST_LINK;
                        destination_url = process.env.GENETIC_ALGORITHM_SOLVER_LINK;
                        authorization = process.env.GENETIC_ALGORITHM_SOLVER_KEY;
                        return await proxy_redirect(
                            authorization,
                            request.body,
                            destination_url,
                            origin_url,
                            response,
                            health_test_url
                        );
                    }
                    if (original_path == "/simulated_annealing") {
                        health_test_url = process.env.HILL_CLIMBING_SOLVER_HEALTH_TEST_LINK;
                        destination_url = process.env.HILL_CLIMBING_SOLVER_LINK;
                        authorization = process.env.HILL_CLIMBING_SOLVER_KEY;
                        return await proxy_redirect(
                            authorization,
                            request.body,
                            destination_url,
                            origin_url,
                            response,
                            health_test_url
                        );
                    }
                    if (original_path == "/neuronal_network") {
                        health_test_url = process.env.HILL_CLIMBING_SOLVER_HEALTH_TEST_LINK;
                        destination_url = process.env.HILL_CLIMBING_SOLVER_LINK;
                        authorization = process.env.HILL_CLIMBING_SOLVER_KEY;
                        return await proxy_redirect(
                            authorization,
                            request.body,
                            destination_url,
                            origin_url,
                            response,
                            health_test_url
                        );
                    }
                } catch (error) {
                    if (typeof error === "object") {
                        print_log(`server error ${error.message}`, script_firm);
                    }
                    response.statusMessage = "internal server error";
                    return response.status(500).end();
                }
            } else if (valid_request_body == false) {
                print_log(
                    `request body validation failed: ${body_validation_message}`,
                    script_firm
                );
                response.statusMessage = body_validation_message;
                return response.status(400).end();
            }
        } else if (valid_request_header == false) {
            print_log(
                `request header validation failed: ${header_validation_message}`,
                script_firm
            );
            response.statusMessage = header_validation_message;
            return response.status(400).end();
        }
    }
);

api.listen(process.env.ACCESS_PORT);