
from app.providers import provider_manager
from app.exception import ProviderUnavailableError,InvalidAPIKeyError
from openai import AuthenticationError


async def get_avalaible_models():
    models = []

    for name, provider in provider_manager.PROVIDERS.items():
        try:
            res = await provider.get_models()

            models.append({
                "provider": name,
                "models": res,
                "error": None
            })

        except AuthenticationError:
            models.append({
                "provider": name,
                "models": [],
                "error": "Invalid API key"
            })

        except ProviderUnavailableError:
            models.append({
                "provider": name,
                "models": [],
                "error": "Provider unavailable"
            })

        except InvalidAPIKeyError:
            models.append({"provider": name, "models": [], "error": "Invalid API key"})

    return models
