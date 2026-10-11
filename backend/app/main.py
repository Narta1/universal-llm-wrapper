from fastapi import FastAPI, HTTPException

from app.schemas import ChatRequest
from app.services.llm_services import gen_response,gen_streamed_response
from app.services.model_service import get_avalaible_models
from app.exception import ProviderUnavailableError, UnknownProviderError,InvalidAPIKeyError
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
    except InvalidAPIKeyError as e:
        raise HTTPException(status_code=401, detail=str(e))

@app.post("/chat/stream")

@app.post("/chat/stream")
async def send_stream(req: ChatRequest):
    stream = gen_streamed_response(req)

    try:
        first_chunk = await anext(stream)
    except StopAsyncIteration:
        return StreamingResponse(
            iter(()),
            media_type="text/plain"
        )
    except InvalidAPIKeyError as e:
        await stream.aclose()
        raise HTTPException(status_code=401, detail=str(e))
    except ProviderUnavailableError as e:
        await stream.aclose()
        raise HTTPException(status_code=503, detail=str(e))
    except UnknownProviderError as e:
        await stream.aclose()
        raise HTTPException(status_code=400, detail=str(e))

    async def response_stream():
        yield first_chunk
        async for chunk in stream:
            yield chunk

    return StreamingResponse(
        response_stream(),
        media_type="text/plain"
    )

@app.get("/models")
async def get_models() : 

    return await get_avalaible_models()