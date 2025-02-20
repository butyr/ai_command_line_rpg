# display_service.py
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.logging import RichHandler
from src.models import GameState, GameCommand
from typing import Optional


class DisplayService:
    def __init__(self):
        self.console = Console()

    def setup_logging(self) -> RichHandler:
        return RichHandler(rich_tracebacks=True, markup=True)

    def create_stats_table(self, state: GameState) -> Table:
        stats_table = Table(title="Character Stats", show_header=True)
        stats_table.add_column("Stat", style="cyan")
        stats_table.add_column("Value", style="magenta")

        stats_dict = state.player_stats.dict()
        for stat, value in stats_dict.items():
            stats_table.add_row(stat.capitalize(), str(value))

        return stats_table

    def create_inventory_table(self, state: GameState) -> Table:
        inventory_table = Table(title="Inventory")
        inventory_table.add_column("Items", style="green")
        for item in state.inventory:
            inventory_table.add_row(item)
        return inventory_table

    def create_quest_table(self, state: GameState) -> Table:
        quest_table = Table(title="Active Quests")
        quest_table.add_column("Quests", style="yellow")
        for quest in state.quest_log:
            quest_table.add_row(quest)
        return quest_table

    def display_game_state(
        self, state: GameState, command: GameCommand
    ) -> Optional[Panel]:
        if command == GameCommand.STATS:
            return Panel(
                self.create_stats_table(state),
                title="Character Stats",
                border_style="bright_blue",
            )
        elif command == GameCommand.INVENTORY:
            return Panel(
                self.create_inventory_table(state),
                title="Inventory",
                border_style="bright_blue",
            )
        elif command == GameCommand.QUESTS:
            return Panel(
                self.create_quest_table(state),
                title="Quest Log",
                border_style="bright_blue",
            )
        elif command == GameCommand.SUMMARY:
            return self.create_summary_display(state)
        return None

    def create_summary_display(self, state: GameState) -> Panel:
        summary = state.summary
        if not summary or summary.strip() == "":
            content = "[italic yellow]No adventures recorded yet... Your tale begins now![/italic yellow]"
        else:
            content = f"[green]Adventure Log:[/green]\n\n{summary}"

        return Panel(
            content,
            title="[bold magenta]Campaign Chronicle[/bold magenta]",
            border_style="bright_magenta",
            title_align="center",
            padding=(1, 2),
            highlight=True,
        )

    def display_dm_response(self, content: str) -> None:
        self.console.print(Panel(content, title="Dungeon Master", style="bright_green"))

    def display_error(self, error: Exception) -> None:
        self.console.print(
            Panel(
                f"[red]An error occurred: {str(error)}[/red]\nThe game state has been preserved.",
                title="Error",
                style="red",
            )
        )
