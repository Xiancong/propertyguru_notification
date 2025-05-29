import os
import yaml

def get_pg_config():
    token = os.getenv("config_path")
    if not token:
        raise EnvironmentError("Config path not found")
    return token

def get_config(config, key, prompt_text, error_message=False):
    config_val = config.get(key)
    if config_val is None:
        if error_message == True:
            print(prompt_text)
            exit()
        else:
            config_val = input(f"{prompt_text}: ")
    return config_val

def load_config(path=get_pg_config()):
    with open(path, "r") as f:
        return yaml.safe_load(f)
