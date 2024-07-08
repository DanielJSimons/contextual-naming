from enum import Enum, unique
from typing import Dict, Union

@unique
class ConfigContract(Enum):
    OLLAMA_BASE_URL = 'OLLAMA_BASE_URL'
    DATABASE_FILE = 'DATABASE_FILE'
    
ConfigType = Dict[ConfigContract, Union[int, str, float]]

def get_config() -> ConfigType:
    _dev_config = {
        ConfigContract.OLLAMA_BASE_URL: 'http://127.0.0.1:11434',
        ConfigContract.DATABASE_FILE: 'C:/Users/dansi/Desktop/contextual_naming/database_handling/contextual_naming.db'
    }
    return _dev_config
