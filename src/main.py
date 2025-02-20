# main.py
from src.models import GameCommand
from src.state_manager import StateManager
from src.display_service import DisplayService
from src.ai_service import AIService
from src.game_engine import GameEngine
import logging
from rich.traceback import install
from rich.panel import Panel


def main():
    # Set up rich traceback handling
    install(show_locals=True)

    # Initialize services
    display_service = DisplayService()

    # Configure logging
    logging.basicConfig(
        level="INFO",
        format="%(message)s",
        datefmt="[%X]",
        handlers=[display_service.setup_logging()],
    )
    logger = logging.getLogger("main")

    # Initialize other services
    state_manager = StateManager()
    ai_service = AIService()
    game_engine = GameEngine(state_manager, ai_service)

    # Display welcome message
    display_service.console.print(
        Panel.fit(
            """Welcome to the D&D Adventure!
        Available commands: 
        - /inventory - Check your items
        - /stats - View your character stats
        - /quests - Review active quests
        - /summary - Recall recent adventures
        - quit - Exit the game""",
            title="Game Start",
            style="bright_yellow",
        )
    )

    display_service.console.print(
        Panel(
            "You find yourself in the town of Sandpoint, standing outside the Rusty Dragon Inn...",
            title="Starting Location",
            style="bright_blue",
        )
    )

    # Main game loop
    while True:
        try:
            user_input = display_service.console.input(
                "\n[bright_cyan]What would you like to do?[/] "
            )
            logger.debug(f"Received input: {user_input}")

            if user_input.lower() == GameCommand.QUIT.value:
                display_service.console.print(
                    Panel.fit(
                        "Thank you for playing! Your adventure has been saved.",
                        title="Farewell",
                        style="bright_yellow",
                    )
                )
                break

            # Process commands or game input
            try:
                command = GameCommand(user_input.lower())
                state = state_manager.get_state()
                display = display_service.display_game_state(state, command)
                if display:
                    display_service.console.print(display)
                    continue
            except ValueError:
                # Not a command, process as game input
                pass

            # Process game input through engine
            result = game_engine.process_turn(user_input)
            for message in result["messages"]:
                display_service.display_dm_response(message.content)

        except Exception as e:
            logger.exception("An error occurred during game execution")
            display_service.display_error(e)


if __name__ == "__main__":
    main()
