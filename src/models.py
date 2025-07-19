from dataclasses import dataclass
from typing import Literal
from pydantic import BaseModel

@dataclass
class Message(BaseModel):
    user: str
    timestamp: str
    text: str
    reactions: int

    def __repr__(self) -> str:
        return f"{{{self.user} at {self.timestamp}:\n{{ {self.text}}}, number of reactions: {self.reactions}}}"

@dataclass
class ConversationContext():
    focusMessage: Message
    anteriorContext: list[Message]
    posteriorContext: list[Message]

@dataclass
class PointOfInterest(BaseModel):
    type: Literal["question", "fact", "insight", "other"] | str
    short_summary: str
    key_phrases: list[str]

@dataclass
class ConversationClassificationCompletion(BaseModel):
    pointsOfInterest: list[PointOfInterest]

@dataclass
class ConversationClassification():
    context: ConversationContext
    completion: ConversationClassificationCompletion

