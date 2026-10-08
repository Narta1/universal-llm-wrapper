from app.providers import provider_manager
async def get_avalaible_models():
    models=[]
    for name,provider in provider_manager.PROVIDERS.items() : 
        res=await provider.get_models()
        models.append({
            "provider":name,
            "models" : res
        })
    return models