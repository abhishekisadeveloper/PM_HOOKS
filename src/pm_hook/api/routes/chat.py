from fastapi import APIRouter


from pm_hook.schemas.chat import (
    ChatMessageRequest, # receive
    ChatMessageResponse # sends 
)


router = APIRouter(
    prefix="/api/chat",
    tags=["Chat"]
)


@router.post(
    "/messages",
    response_model=ChatMessageResponse
)
async def receive_chat_message(
    request: ChatMessageRequest
):
    return ChatMessageResponse(
        success=True,
        message=request.message,
        status="received"
    )