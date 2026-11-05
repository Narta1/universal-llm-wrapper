import pytest
from app.services.llm_services import calculate_cost, gen_prompt
from app.schemas import ChatResponse,ChatRequest

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

def test_system_message_comes_first():
    req = ChatRequest(
        prompt="What is a variable in Python?",
        provider="ollama",
        model="llama3.2",
        level="beginner",
        length="short",
    )

    messages = gen_prompt(req)

    assert [m["role"] for m in messages] == ["system", "user"]