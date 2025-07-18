from dataclasses import dataclass
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
class ConversationClassificationCompletion(BaseModel):
    questionIfOneExistsInMessage: str | None
    fact: str | None
    otherImportantInfoNotCoveredByOtherProperties: str | None
    keyPhrase: str | None

@dataclass
class ConversationClassification():
    context: ConversationContext
    completion: ConversationClassificationCompletion

