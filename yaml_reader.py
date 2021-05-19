import yaml


def load_http_response_message(message_key: str) -> str:
    yaml_path = r"./static_messages_files/static_http_response_messages.yaml"
    with open(yaml_path) as yaml_file:
        yaml_dict = yaml.load(stream=yaml_file, Loader=yaml.FullLoader)
    return yaml_dict[message_key]


def load_log_message(message_key: str) -> str:
    yaml_path = r"./static_messages_files/static_log_messages.yaml"
    with open(yaml_path) as yaml_file:
        yaml_dict = yaml.load(stream=yaml_file, Loader=yaml.FullLoader)
    return yaml_dict[message_key]
