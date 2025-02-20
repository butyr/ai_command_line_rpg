# ai_service.py
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, AIMessage, HumanMessage, BaseMessage
from src.models import GameState
from typing import List, Tuple
from langgraph.checkpoint.memory import MemorySaver


class AIService:
    def __init__(self):
        self.model = ChatOllama(model="phi4")
        self.memory = MemorySaver()

    def create_dm_prompt(self, state: GameState) -> str:
        return f"""
        You are an experienced Dungeons & Dragons Dungeon Master. Maintain character as a DM throughout all interactions.
        
        Current game state:
        - Location: {state.current_location}
        - Player Stats: {state.player_stats.dict()}
        - Inventory: {state.inventory}
        - Active Quests: {state.quest_log}
        
        Respond to the player's actions with vivid descriptions and appropriate game mechanics. Include:
        - Descriptive narrative of the environment and NPCs
        - Consequences of player actions
        - Combat mechanics when relevant
        - Skill checks when appropriate
        - Maintain game balance and fairness
        
        Keep the game engaging and responsive to player choices while maintaining the rules and spirit of D&D 5e.
        """

    def get_response(self, state: GameState, user_message: str) -> AIMessage:
        game_state = self.create_dm_prompt(state)

        if state.summary:
            system_message = f"{game_state}\n\nPrevious events: {state.summary}"
        else:
            system_message = game_state

        messages = [SystemMessage(content=system_message)] + state.messages
        messages.append(HumanMessage(content=user_message))

        return self.model.invoke(messages)

    def should_summarize(self, state: GameState) -> bool:
        return len(state.messages) > 6

    def summarize_conversation(self, state: GameState) -> Tuple[str, List[BaseMessage]]:
        summary_message = (
            f"Previous adventure summary: {state.summary}\n\n"
            "Continue the adventure summary with recent events:"
            if state.summary
            else "Summarize the recent adventure events:"
        )

        messages = state.messages + [HumanMessage(content=summary_message)]
        response = self.model.invoke(messages)

        # Keep the last two messages and clear the rest
        kept_messages = (
            state.messages[-2:] if len(state.messages) >= 2 else state.messages
        )

        return response.content, kept_messages
