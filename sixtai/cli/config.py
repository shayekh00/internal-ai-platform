# sixtai/cli/config.py

import yaml
import os
from pathlib import Path
from dotenv import load_dotenv

def load_config(agent_name: str) -> dict:
    base_path = Path.cwd() / agent_name
    config_path = base_path / "sixtai.yaml"
    env_path = base_path / ".env"

    if not config_path.exists():
        raise FileNotFoundError(f"❌ No sixtai.yaml found for {agent_name}")
    
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    # Load .env if it exists
    if env_path.exists():
        load_dotenv(dotenv_path=env_path)

    return config