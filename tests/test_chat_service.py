from pm_hook.schemas.chat import ChatMessageResponse
from pm_hook.services.chat_service import acknowledge_message


def test_acknowledge_message_returns_success_response():
    message = "Create a task for tomorrow"

    result = acknowledge_message(message)

    assert isinstance(result, ChatMessageResponse)
    assert result.success is True
    assert result.message == message
    assert result.status == "received"