import yaml

http_response_messages_dict = dict()
log_messages_dict = dict()

with open(r"./static_messages_files/static_http_response_messages.yaml") as yaml_file:
    http_response_messages_dict = yaml.load(stream=yaml_file, Loader=yaml.FullLoader)

with open(r"./static_messages_files/static_log_messages.yaml") as yaml_file:
    log_messages_dict = yaml.load(stream=yaml_file, Loader=yaml.FullLoader)


def load_http_response_messages_dict() -> dict:
    return http_response_messages_dict


def load_log_messages_dict() -> dict:
    return log_messages_dict
