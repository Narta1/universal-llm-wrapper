
from openai import AsyncOpenAI,APIConnectionError,AuthenticationError
from dotenv import load_dotenv
import os
from app.exception import ProviderUnavailableError, InvalidAPIKeyError

load_dotenv()
OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")

_client=None
def get_client():
    global _client
    if _client is None:
        if not OPENAI_API_KEY:
            raise InvalidAPIKeyError("OPENAI_API_KEY is not set")
        _client=AsyncOpenAI(
    
    api_key=OPENAI_API_KEY
)
    return _client
        

async def generate(prompt,model):
    try : 
        res=await get_client().chat.completions.create(
            model=model,
            messages=prompt

        )
        return {
            "output_tokens" : res.usage.completion_tokens,
            "input_tokens" : res.usage.prompt_tokens,
            "response" : res.choices[0].message.content,
            "provider" : "openai",
            "model" : model
    
        }
    except APIConnectionError as e:
        raise ProviderUnavailableError(
        "Unable to connect to OpenAI ")
    except AuthenticationError:
        raise InvalidAPIKeyError("Invalid OpenAI API key")


async def get_models():
    try : 
        res=await get_client().models.list()
        return [m.id for m in res.data]
    except APIConnectionError as e:
        raise ProviderUnavailableError ("Unable to connect to OpenAI")
    except AuthenticationError:
        raise InvalidAPIKeyError("Invalid OpenAI API key")


async def stream(prompt, model):
    try:
        res = await get_client().chat.completions.create(
            model=model,
            messages=prompt,
            stream=True,
        )

        async for chunk in res:
            content = chunk.choices[0].delta.content
            if content:
                yield content

    except APIConnectionError:
        raise ProviderUnavailableError("Unable to connect to OpenAI")
    except AuthenticationError:
        raise InvalidAPIKeyError("Invalid OpenAI API key")