from importlib import import_module
from unittest.mock import Mock

import pytest


@pytest.mark.parametrize("structured", [False, True])
def test_openai_extra_params_keep_the_batch_contract(monkeypatch, structured):
    llm = import_module("core.get_ai_result")
    client = Mock()
    client.chat.completions.create.return_value.choices = [Mock()]
    monkeypatch.setattr(llm, "llm_client", client)
    monkeypatch.setattr(llm.config, "llm_provider", "openai")
    monkeypatch.setattr(llm.config, "llm_extra_params", {"temperature": 0.2})

    if structured:
        llm.get_ai_json_result("system", "input", max_output_tokens=200)
    else:
        llm.get_ai_result("system", "input")

    kwargs = client.chat.completions.create.call_args.kwargs
    assert kwargs["temperature"] == 0.2
    assert kwargs["messages"][0] == {"role": "system", "content": "system"}
    if structured:
        assert kwargs["response_format"] == {"type": "json_object"}
        assert kwargs["max_completion_tokens"] == 200
