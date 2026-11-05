import pytest
from app.services.llm_services import calculate_cost, gen_prompt
from app.schemas import ChatResponse,ChatRequest
from app.exception import InvalidAPIKeyError
from app.providers import openai as openai_provider

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


def test_missing_key_raises_clear_error(monkeypatch):
    monkeypatch.setattr(openai_provider, "OPENAI_API_KEY", None)
    monkeypatch.setattr(openai_provider, "_client", None)

    with pytest.raises(InvalidAPIKeyError):
        openai_provider.get_client()