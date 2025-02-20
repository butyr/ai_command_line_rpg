# state_manager.py
from typing import List
import logging
from src.models import GameState, PlayerStats
from langchain_core.messages import BaseMessage


class StateManager:
    def __init__(self):
        self.logger = logging.getLogger("state_manager")
        self._state = self._initialize_game_state()

    def _initialize_game_state(self) -> GameState:
        return GameState(
            player_stats=PlayerStats(),
            current_location="The Rusty Dragon Inn in the town of Sandpoint",
            inventory=["simple dagger", "leather armor", "backpack"],
            quest_log=["Investigate the strange noises in the Sandpoint cemetery"],
        )

    def get_state(self) -> GameState:
        return self._state

    def update_state(self, new_state: GameState) -> None:
        self._state = new_state
        self.logger.debug("State updated")

    def update_summary(self, summary: str) -> None:
        self._state.summary = summary
        self.logger.debug("Summary updated")

    def update_messages(self, messages: List[BaseMessage]) -> None:
        self._state.messages = messages
        self.logger.debug("Messages updated")

    def add_message(self, message: BaseMessage) -> None:
        self._state.messages.append(message)
        self.logger.debug("Message added")

    def clear_messages(self) -> None:
        self._state.messages = []
        self.logger.debug("Messages cleared")
