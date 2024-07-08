from enum import Enum
from settings import get_config, ConfigContract
from langchain_community.chat_models.ollama import ChatOllama

config = get_config()
print("Config:", config)  # Add this line to debug

def get_ollama_model(model_name: str, temperature: float, **kwargs) -> ChatOllama:
    url = config[ConfigContract.OLLAMA_BASE_URL]  # Correct access using enum
    ollama_llm = ChatOllama(model=model_name, base_url=url, temperature=temperature, **kwargs)
    return ollama_llm
