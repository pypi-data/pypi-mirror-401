import json
import os
from typing import Dict, Optional

CONFIG_FILE_PATH = os.path.expanduser("~/.rectab_config.json")

def load_config() -> Optional[Dict]:
    """Load user configuration from local file"""
    if os.path.exists(CONFIG_FILE_PATH):
        try:
            with open(CONFIG_FILE_PATH, "r") as f:
                return json.load(f)
        except:
            return None
    return None

def save_config(config: Dict):
    """Save user configuration to local file"""
    with open(CONFIG_FILE_PATH, "w") as f:
        json.dump(config, f, indent=4)