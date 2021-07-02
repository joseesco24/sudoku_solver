/**
 * this functions is used for print all the logs of the application, using it makes easy to read the logs and find errors taking 
 * into account the hour and date of the log.
 * 
 * @param message {string} the message that is going to be printed as a log.
 * @param script_firm {string} the firm of the file that generates the message.
 */
export default function print_log(message, script_firm = null) {

    message = message.trim().replace(/^\w/, (c) => c.toUpperCase());
    let date_obj = new Date();

    let month = ("0" + (date_obj.getMonth() + 1)).slice(-2);
    let date = ("0" + date_obj.getDate()).slice(-2);
    let year = date_obj.getFullYear();
    let current_date = `${year}-${month}-${date}`;

    let seconds = ("0" + date_obj.getSeconds()).slice(-2);
    let minutes = ("0" + date_obj.getMinutes()).slice(-2);
    let hours = ("0" + date_obj.getHours()).slice(-2);
    let current_time = `${hours}:${minutes}:${seconds}`;

    let current_datetime = `${current_date} ${current_time}`;

    if (script_firm != null) {
        script_firm = script_firm.toUpperCase();
        console.log(`[${current_datetime}][${script_firm}] - ${message}`);
    } else {
        console.log(`[${current_datetime}] - ${message}`);
    }

}