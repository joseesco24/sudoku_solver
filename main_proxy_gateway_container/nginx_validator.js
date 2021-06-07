function check_request_mandatory_requirements(request) {
    request.error("starting request body validations");

    // Control vars declarations.

    var sucess_link = request.variables.sucess_link;
    var error_link = request.variables.error_link;
    var valid_request_body = true;

    // Body general validations and use vars declarations.

    try {
        var request_body = JSON.parse(request.variables.request_body);
        var request_body_keys = Object.keys(request_body);
        var necessary_fields_in_request = [
            "board_array",
            "zone_length",
            "zone_height",
        ];
        request.error("request body checked successfully");
    } catch (error) {
        request.error("request body checked unsuccessfully");
        valid_request_body = false;
    }

    // Mandatory parameters existanse validations.

    if (valid_request_body == true) {
        if (
            necessary_fields_in_request.every((elem) =>
                request_body_keys.includes(elem)
            ) == true
        ) {
            request.error("the request body have all necesary labels");
        } else {
            request.error("the request body dosn't have all necessary labels");
            valid_request_body = false;
        }
    }

    // Mandatory parameters type validations.

    if (valid_request_body == true) {
        if (Array.isArray(request_body.board_array) == true) {
            request.error("the variable board_array has the correct data type");
        } else {
            request.error("the variable board_array hasn't the correct data type");
            valid_request_body = false;
        }
    }
    if (valid_request_body == true) {
        if (Number.isInteger(request_body.zone_length) == true) {
            request.error("the variable zone_length has the correct data type");
        } else {
            request.error("the variable zone_length hasn't the correct data type");
            valid_request_body = false;
        }
    }
    if (valid_request_body == true) {
        if (Number.isInteger(request_body.zone_height) == true) {
            request.error("the variable zone_height has the correct data type");
        } else {
            request.error("the variable zone_height hasn't the correct data type");
            valid_request_body = false;
        }
    }

    // Board dimensions validations.

    var board_dimensions = request_body.zone_height * request_body.zone_length;
    if (valid_request_body == true) {
        if (board_dimensions == request_body.board_array.length) {
            request.error("the board columns dimensions are correct");
        } else {
            request.error("the board columns dimensions aren't correct");
            valid_request_body = false;
        }
    }
    if (valid_request_body == true) {
        var board_lenght_summation = 0;
        request_body.board_array.forEach(function (board_row) {
            board_lenght_summation += board_row.length;
        });
        if (board_dimensions == board_lenght_summation / board_dimensions) {
            request.error("the board rows dimensions are correct");
        } else {
            request.error("the board rows dimensions aren't correct");
            valid_request_body = false;
        }
    }

    // Board elements validations.

    if (valid_request_body == true) {
        request_body.board_array.forEach(function (board_row) {
            if (valid_request_body == true) {
                board_row.forEach(function (board_element) {
                    if (valid_request_body == true) {
                        if (Number.isInteger(board_element) == false) {
                            request.error(
                                `the board have an element that isn't a number: ${board_element} isn't a number, data type ${typeof board_element}`
                            );
                            valid_request_body = false;
                        }
                    }
                    if (valid_request_body == true) {
                        if (board_element != 0) {
                            if (board_element > board_dimensions || board_element < 1) {
                                request.error(
                                    `the board have a number out of range: ${board_element} isn't in range of ${1} and ${board_dimensions}`
                                );
                                valid_request_body = false;
                            }
                        }
                    }
                });
            }
        });
    }
    if (valid_request_body == true) {
        request.error("all the board dimensions are correct");
    }

    // Checking if the board can be solved.

    if (valid_request_body == true) {
        for (
            var row_index = 0; row_index < request_body.board_array.length; row_index++
        ) {
            if (valid_request_body == true) {
                var row_dict = new Object();
                for (
                    var column_index = 0; column_index < request_body.board_array.length; column_index++
                ) {
                    var current_number = request_body.board_array[row_index][column_index];
                    if (current_number != 0 && !(current_number in row_dict)) {
                        row_dict[current_number] = [row_index, column_index];
                    } else if (current_number != 0 && current_number in row_dict) {
                        request.error(
                            `the board have a fixed number repeated: ${current_number} is in te position (${row_dict[current_number][0]}, ${row_dict[current_number][1]}) and (${row_index}, ${column_index})`
                        );
                        valid_request_body = false;
                        break;
                    }
                }
            } else {
                break;
            }
        }
    }
    if (valid_request_body == true) {
        for (
            var row_index = 0; row_index < request_body.board_array.length; row_index++
        ) {
            if (valid_request_body == true) {
                var col_dict = new Object();
                for (
                    var column_index = 0; column_index < request_body.board_array.length; column_index++
                ) {
                    var current_number = request_body.board_array[column_index][row_index];
                    if (current_number != 0 && !(current_number in col_dict)) {
                        col_dict[current_number] = [row_index, column_index];
                    } else if (current_number != 0 && current_number in col_dict) {
                        request.error(
                            `the board have a fixed number repeated: ${current_number} is in te position (${col_dict[current_number][0]}, ${col_dict[current_number][1]}) and (${row_index}, ${column_index})`
                        );
                        valid_request_body = false;
                        break;
                    }
                }
            } else {
                break;
            }
        }
    }
    if (valid_request_body == true) {
        request.error("the board can be solved");
    }

    // Routing and end message.

    if (valid_request_body == true) {
        request.error("request body validation end successfully");
        return sucess_link;
    } else if (valid_request_body == false) {
        request.error("request body validation dosn't end successfully");
        return error_link;
    }
}

export default {
    check_request_mandatory_requirements,
};