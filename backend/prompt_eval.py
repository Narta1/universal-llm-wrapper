import asyncio
from tests.prompt_cases import TEST_CASES
from app.prompts.tutor import build_tutor_prompt_v1,build_tutor_prompt_v2,build_tutor_prompt_v3
from app.prompts.judge import build_judge_prompt
from app.providers.provider_manager import get_provider
import json


def check_length(message,length):
    size=len(message.split())
    res=0
    if length=="short" and size<80:
        res=1
    return res
def check_correctness(message):
    keywords=["value","variable"]

    for msg in keywords :
        if msg not in message:
            return 0
    return 1

def check_relevance(message):
    keywords = ["variable", "python"]

    for keyword in keywords:
        if keyword not in message.lower():
            return 0

    return 1
def check_beginner_friendly(message):
    difficult_words = ["implementation", "architecture", "abstraction", "instantiation"]

    for word in difficult_words:
        if word in message.lower():
            return 0

    return 1

async def main():
    
    
    provider=get_provider("ollama")
    for case in TEST_CASES:
        prompt=case["prompt"]

        system_prompt = build_tutor_prompt_v2(
            case["level"],
            case["length"]
        )
        messages=[{"role":"system","content":system_prompt},{"role":"user","content":prompt}
                ]
        
        
        #res= await provider.generate(messages,"qwen2.5:0.5b")
        async for chunk in provider.stream(messages,"qwen2.5:0.5b"):
            print(chunk,end="",flush=True)
        print("\nMODEL RESPONSE:")
        #print(res)
        sys_prompt=build_judge_prompt()
        messages_judge=[{"role":"system","content":sys_prompt},{"role":"user","content":res}]

        #judge_res= await provider.generate(messages_judge,"llama3.2:latest")
        print("\nJUDGE RESPONSE:")
        #print(judge_res["response"])    
        #judge_score=json.loads(judge_res["response"])
        #print(judge_score)

        #score = judge_score
       
        #print("\nSCORE:")
        #print(score)
        #total = sum(score.values())

        #print("\nTOTAL:")
        #print(f"{total}/4")

   

if __name__== "__main__" :
    asyncio.run(main())