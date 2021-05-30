function check_request_mandatory_requirements(request) {
    try {
        if (request.variables.request_body) {
            JSON.parse(request.variables.request_body);
            request.error("request body checked successfully");
            return request.variables.sucess_link;

        } else {
            request.error("request body not found");
            return request.variables.error_link;
        }

    } catch (error) {
        request.error("request body checked unsuccessfully");
        return request.variables.error_link;
    }
}

export default {
    check_request_mandatory_requirements,
};