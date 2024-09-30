
import json
import os

class Config:
    def __init__(self, config_file='config.json'):
        config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), config_file)
        try:
            with open(config_path, 'r') as f:
                config_data = json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"File configuration {config_file} not found.")
        except json.JSONDecodeError as e:
            raise ValueError(f"Error in reading {config_file}: {e}")
        
        self.DATABASE_URL = config_data.get('DATABASE_URL')
        if not self.DATABASE_URL:
            raise ValueError("DATABASE_URL not found.")

json = Config()
