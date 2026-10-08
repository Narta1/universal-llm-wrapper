
from pydantic import BaseModel
class ChatRequest(BaseModel):
    prompt: str
    provider: str
    model: str
    level: str
    length: str


class ChatResponse(BaseModel) :
    output_tokens : int
    input_tokens: int
    response : str
    model : str
    provider : str
    status : str
    cost : int