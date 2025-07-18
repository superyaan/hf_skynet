# utils/config_loader.py
import json

CONFIG_FILE = 'config.json'

def load_config(path: str = CONFIG_FILE):
    with open(path, 'r') as f:
        return json.load(f)