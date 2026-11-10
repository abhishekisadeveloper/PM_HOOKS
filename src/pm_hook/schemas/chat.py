from pydantic import BaseModel, Field

# This is for client req. format verification.
class ChatMessageRequest(BaseModel):
    message: str = Field(
        min_length=1,
        max_length=2000,
        description="The user's chat message"
    )

# This is for server res. format verification.
class ChatMessageResponse(BaseModel):
    success: bool
    message: str
    status: str
    