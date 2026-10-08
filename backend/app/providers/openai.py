
from openai import AsyncOpenAI,APIConnectionError,AuthenticationError
from dotenv import load_dotenv
import os
from app.exception import ProviderUnavailableError

load_dotenv()
OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")


client=AsyncOpenAI(
    
    api_key=OPENAI_API_KEY
)

async def generate(prompt,model):
    try : 
        res=await client.chat.completions.create(
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
        raise ValueError("Invalid OpenAI API key")


async def get_models():
    try : 
        res=await client.models.list()
        return [m.id for m in res.data]
    except APIConnectionError as e:
        raise ProviderUnavailableError ("Unable to connect to OpenAI")