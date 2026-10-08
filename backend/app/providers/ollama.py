import httpx
from openai import AsyncOpenAI,APIConnectionError
from app.exception import ProviderUnavailableError

OLLAMA_URL = "http://localhost:11434"
client=AsyncOpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",
    timeout=60.0
)
async def generate( prompt,model):
    try :
        res=await client.chat.completions.create(
        model=model,
        messages=prompt,
        
        )

        return  {
            "output_tokens" : res.usage.completion_tokens,
            "input_tokens" : res.usage.prompt_tokens,
            "response" : res.choices[0].message.content,
            "provider" : "ollama",
            "model" : model

        }
    except APIConnectionError:
        raise ProviderUnavailableError(
        "Ollama server is unavailable"
    )

async def stream(prompt,model):
    try:
        
        res=await client.chat.completions.create(
            messages=prompt,
            model=model,
            stream=True
        )
        full_res=""
        async for chunk in res : 
           content=chunk.choices[0].delta.content
           if content :
               full_res+=content
               yield content
        
        
    except APIConnectionError:
        raise ProviderUnavailableError("Ollama server is unavalaible")


async def get_models() :
    async with httpx.AsyncClient() as client : 
        res=await client.get(
            f"{OLLAMA_URL}/api/tags"
        )
    data=res.json()

    models=[]

    for model in data["models"]:
        models.append(model["name"])

    return models