from app.providers import ollama
from app.providers import openai
from app.exception import UnknownProviderError
PROVIDERS = {
    "ollama": ollama,
    "openai": openai,
    #"anthropic": anthropic
}

def get_provider(provider_name) : 

    if provider_name not in PROVIDERS : 
        
        raise UnknownProviderError("Unknown provider")

    return PROVIDERS[provider_name]

