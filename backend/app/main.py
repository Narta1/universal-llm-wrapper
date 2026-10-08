from fastapi import FastAPI, HTTPException

from app.schemas import ChatRequest
from app.services.llm_services import gen_response,gen_streamed_response
from app.services.model_service import get_avalaible_models
from app.exception import ProviderUnavailableError, UnknownProviderError
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

app=FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
def get_root():
    return {"status":"running"}



@app.post("/chat")
async def send_req(req : ChatRequest):
    try :
        response=await gen_response(req)
        return response
    except ProviderUnavailableError as e :
        raise HTTPException(
            status_code=503,
            detail=str(e)
        )
    except UnknownProviderError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

@app.post("/chat/stream")
async def send_stream(req:ChatRequest):
    try :
        
        return StreamingResponse(
            gen_streamed_response(req),
            media_type="text/plain"
        )
    except ProviderUnavailableError as e:
        raise HTTPException(
            status_code=503,
            detail=str(e)
        )
    except UnknownProviderError as e:
            raise HTTPException(
                status_code=400,
                detail=str(e)
            )
@app.get("/models")
async def get_models() : 

    return await get_avalaible_models()