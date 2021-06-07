import print_log from "./general_utilities.mjs";

const script_firm = "val";

export default function check_request_mandatory_requirements(request_body) {
    print_log("starting request body validations", script_firm);

    // Control vars declarations.

    var valid_request_body, message;

    // Body general validations and use vars declarations.

    try {
        var request_body_keys = Object.keys(request_body);
        var necessary_fields_in_request = [
            "board_array",
            "zone_length",
            "zone_height",
        ];
        print_log(
            "request body checked successfully, the request body is json",
            script_firm
        );
        valid_request_body = true;
    } catch (error) {
        message = "request body check unsuccessfully, the request body isn't json";
        print_log(message, script_firm);
        valid_request_body = false;
    }

    // Mandatory parameters existanse validations.

    if (valid_request_body == true) {
        if (
            necessary_fields_in_request.every((elem) =>
                request_body_keys.includes(elem)
            ) == true
        ) {
            print_log("the request body have all the necesary labels", script_firm);
        } else {
            message = "the request body dosn't have all the necessary labels";
            print_log(message, script_firm);
            valid_request_body = false;
        }
    }

    // Mandatory parameters type validations.

    if (valid_request_body == true) {
        if (Array.isArray(request_body.board_array) == true) {
            print_log(
                "the variable board_array has the correct data type",
                script_firm
            );
        } else {
            message = "the variable board_array hasn't the correct data type";
            print_log(message, script_firm);
            valid_request_body = false;
        }
    }
    if (valid_request_body == true) {
        if (Number.isInteger(request_body.zone_length) == true) {
            print_log(
                "the variable zone_length has the correct data type",
                script_firm
            );
        } else {
            message = "the variable zone_length hasn't the correct data type";
            print_log(message, script_firm);
            valid_request_body = false;
        }
    }
    if (valid_request_body == true) {
        if (Number.isInteger(request_body.zone_height) == true) {
            print_log(
                "the variable zone_height has the correct data type",
                script_firm
            );
        } else {
            message = "the variable zone_height hasn't the correct data type";
            print_log(message, script_firm);
            valid_request_body = false;
        }
    }

    // Board dimensions validations.

    var board_dimensions = request_body.zone_height * request_body.zone_length;
    if (valid_request_body == true) {
        if (board_dimensions == request_body.board_array.length) {
            print_log("the board columns dimensions are correct", script_firm);
        } else {
            message = "the board columns dimensions aren't correct";
            print_log(message, script_firm);
            valid_request_body = false;
        }
    }
    if (valid_request_body == true) {
        var board_lenght_summation = 0;
        request_body.board_array.forEach(function (board_row) {
            board_lenght_summation += board_row.length;
        });
        if (board_dimensions == board_lenght_summation / board_dimensions) {
            print_log("the board rows dimensions are correct", script_firm);
        } else {
            message = "the board rows dimensions aren't correct";
            print_log(message, script_firm);
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
                            message = `the board have an element that isn't a number: ${board_element} isn't a number, data type ${typeof board_element}`;
                            print_log(message, script_firm);
                            valid_request_body = false;
                        }
                    }
                    if (valid_request_body == true) {
                        if (board_element != 0) {
                            if (board_element > board_dimensions || board_element < 1) {
                                message = `the board have a number out of range: ${board_element} isn't in range of ${1} and ${board_dimensions}`;
                                print_log(message, script_firm);
                                valid_request_body = false;
                            }
                        }
                    }
                });
            }
        });
    }
    if (valid_request_body == true) {
        print_log("all the board dimensions are correct", script_firm);
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
                    var current_number =
                        request_body.board_array[row_index][column_index];
                    if (current_number != 0 && !(current_number in row_dict)) {
                        row_dict[current_number] = [row_index, column_index];
                    } else if (current_number != 0 && current_number in row_dict) {
                        message = `the board have a fixed number repeated: ${current_number} is in the position (${row_dict[current_number][0]}, ${row_dict[current_number][1]}) and (${row_index}, ${column_index})`;
                        print_log(message, script_firm);
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
                    var current_number =
                        request_body.board_array[column_index][row_index];
                    if (current_number != 0 && !(current_number in col_dict)) {
                        col_dict[current_number] = [row_index, column_index];
                    } else if (current_number != 0 && current_number in col_dict) {
                        message = `the board have a fixed number repeated: ${current_number} is in te position (${col_dict[current_number][0]}, ${col_dict[current_number][1]}) and (${row_index}, ${column_index})`;
                        print_log(message, script_firm);
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
        print_log("the board can be solved", script_firm);
    }

    // Routing and end message.

    if (valid_request_body == true) {
        print_log("request body validation end successfully", script_firm);
    } else if (valid_request_body == false) {
        print_log("request body validation dosn't end successfully", script_firm);
    }

    return [valid_request_body, message];
}