from pm_hook.schemas.chat import ChatMessageResponse


def acknowledge_message(message: str) -> ChatMessageResponse:
    """
    Acknowledge that the application received a chat message.
    """

    return ChatMessageResponse(
        success=True,
        message=message,
        status="received"
    )