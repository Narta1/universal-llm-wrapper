from app.schemas import ChatRequest, ChatResponse
from app.config import pricing
from app.providers import provider_manager
from app.prompts.tutor import build_tutor_prompt_v1,build_tutor_prompt_v2

def gen_prompt(req : ChatRequest):
    system_prompt =build_tutor_prompt_v2 (req.level,req.length
    
)
    user_prompt=req.prompt
    res=[{
        "role":"user",
        "content" : user_prompt
    },
    {
        "role":"system",
        "content":system_prompt
    }]
    return res

async def gen_response(req : ChatRequest): 
    
    provider=provider_manager.get_provider(req.provider)
    prompt=gen_prompt(req)
    res=await provider.generate(prompt,req.model)
    cost = calculate_cost(
        res["model"],
        res["input_tokens"],
        res["output_tokens"]
    )

    resp = ChatResponse(
        response=res["response"],
        model=res["model"],
        output_tokens=res["output_tokens"],
        input_tokens=res["input_tokens"],
        provider=res["provider"],
        cost=cost,
        status="ok"
    )

    return resp

async def gen_streamed_response(req:ChatRequest):
    provider=provider_manager.get_provider(req.provider)
    prompt=gen_prompt(req)
    async for chunk in provider.stream(prompt,req.model):
        yield chunk


def calculate_cost(model, input_tokens, output_tokens):
    price = pricing.PRICING.get(model,{"input": 0.0, "output": 0.0})

    input_cost = input_tokens * price["input"]
    output_cost = output_tokens * price["output"]

    return input_cost + output_cost