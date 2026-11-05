import pytest
from app.services.llm_services import calculate_cost
from app.schemas import ChatResponse
def test_cost_uses_per_million():
    cost=calculate_cost("gpt-4o-mini", 100, 200)
    assert cost==pytest.approx(0.000135)



def test_chat_response():
    res=ChatResponse(output_tokens=200,
        input_tokens=100,
        response="Hello",
        model="gpt-4o-mini",
        provider="openai",
        status="ok",
        cost=0.000135)
    assert res.cost==pytest.approx(0.000135)