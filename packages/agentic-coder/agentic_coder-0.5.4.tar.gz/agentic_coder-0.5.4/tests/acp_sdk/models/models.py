from typing import List, Optional
from pydantic import BaseModel

class MessagePart(BaseModel):
    content: str

class Message(BaseModel):
    parts: List[MessagePart]
