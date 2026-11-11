# from fastapi import APIRouter


# from pm_hook.schemas.chat import (
#     ChatMessageRequest, # receive
#     ChatMessageResponse # sends 
# )


# router = APIRouter(
#     prefix="/api/chat",
#     tags=["Chat"]
# )


# @router.post(
#     "/messages",
#     response_model=ChatMessageResponse
# )
# async def receive_chat_message(
#     request: ChatMessageRequest
# ):
#     return ChatMessageResponse(
#         success=True,
#         message=request.message,
#         status="received"
#     )

from fastapi import APIRouter

from pm_hook.schemas.chat import (
    ChatMessageRequest,
    ChatMessageResponse
)
from pm_hook.services.chat_service import acknowledge_message


router = APIRouter(
    prefix="/api/chat",
    tags=["Chat"]
)


@router.post(
    "/messages",
    response_model=ChatMessageResponse # This will Tells FastAPI to filter/validate the output.
)
def receive_chat_message(
    request: ChatMessageRequest
) -> ChatMessageResponse: # This is for the Editor Support to know what kind of data will you send to the client.

    print(request.message)
    return acknowledge_message(request.message)