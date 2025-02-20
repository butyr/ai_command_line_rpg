# game_engine.py
from src.state_manager import StateManager
from src.ai_service import AIService
from typing import Dict, Any
from langchain_core.messages import HumanMessage


class GameEngine:
    def __init__(self, state_manager: StateManager, ai_service: AIService):
        self.state_manager = state_manager
        self.ai_service = ai_service

    def process_turn(self, user_input: str) -> Dict[str, Any]:
        state = self.state_manager.get_state()

        # Add user input to messages
        user_message = HumanMessage(content=user_input)
        self.state_manager.add_message(user_message)

        # Get AI response
        ai_response = self.ai_service.get_response(state, user_input)
        self.state_manager.add_message(ai_response)

        # Check if we should summarize
        if self.ai_service.should_summarize(state):
            new_summary, kept_messages = self.ai_service.summarize_conversation(state)
            self.state_manager.update_summary(new_summary)
            self.state_manager.update_messages(kept_messages)

        return {"messages": [ai_response]}
