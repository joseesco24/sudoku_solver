import yaml


def load_http_response_messages_dict() -> dict:
    file_path = r"./static_messages_files/static_http_response_messages.yaml"
    with open(file_path) as yaml_file:
        dict = yaml.load(stream=yaml_file, Loader=yaml.FullLoader)
    return dict


def load_log_messages_dict() -> dict:
    file_path = r"./static_messages_files/static_log_messages.yaml"
    with open(file_path) as yaml_file:
        dict = yaml.load(stream=yaml_file, Loader=yaml.FullLoader)
    return dict
