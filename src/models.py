# models.py
from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum
from langchain_core.messages import BaseMessage


class PlayerStats(BaseModel):
    health: int = Field(default=20, ge=0)
    max_health: int = Field(default=20, ge=0)
    level: int = Field(default=1, ge=1)
    exp: int = Field(default=0, ge=0)
    gold: int = Field(default=10, ge=0)


class GameCommand(str, Enum):
    INVENTORY = "/inventory"
    STATS = "/stats"
    QUESTS = "/quests"
    SUMMARY = "/summary"
    QUIT = "quit"


class GameState(BaseModel):
    player_stats: PlayerStats
    current_location: str
    inventory: List[str]
    quest_log: List[str]
    summary: Optional[str] = None
    messages: List[BaseMessage] = Field(default_factory=list)

    class Config:
        arbitrary_types_allowed = True
