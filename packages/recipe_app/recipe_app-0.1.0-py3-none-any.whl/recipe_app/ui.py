from rich.console import Console, Group
from rich.columns import Columns
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt
from recipe_app.models import Recipe
from typing import Any


def list_recipes(recipe_collection: list[Recipe]) -> None:
    """Display a list of all recipes onto the terminal."""
    recipes = [recipe.name for recipe in recipe_collection if recipe.active]

    console = Console()
    column_config = Columns(sorted(recipes), expand=True)

    console.print(column_config)


def show_recipe(recipe: Recipe) -> None:
    """Display a single recipe onto the terminal."""
    # Build the ingredients table
    ingredient_table = Table(
        title="Recipe Ingredients", border_style="green", header_style="bold green"
    )

    ingredient_table.add_column("Quantity", justify="center", style="white")
    ingredient_table.add_column("Unit", justify="center", style="white")
    ingredient_table.add_column("Ingredient", justify="center", style="white")

    for item in recipe.ingredients:
        ingredient_table.add_row(str(item.qty), item.unit, item.name)

    # Build the steps table
    steps_table = Table(
        title="Recipe Steps", border_style="green", header_style="bold green"
    )

    steps_table.add_column("Order", justify="center", style="white")
    steps_table.add_column("Description", justify="center", style="white")

    for step in recipe.steps:
        steps_table.add_row(str(step.order), step.desc)

    # Need to combine the two tables into a group before building the panel
    content_group = Group(ingredient_table, steps_table)

    # Build the panel
    panel = Panel(
        content_group,  # Displays the ingredient table and steps table
        title=f"[bold green]{recipe.name}  Cook Time: {recipe.duration}[/bold green]",
        border_style="green",
    )

    # Output the panel to the console
    console = Console()
    console.print(panel)


def prompt_recipe_name() -> str:
    return input("Enter the recipe name: ").title()


def prompt_duration() -> int:
    try:
        duration = int(input("What is the expected cook time (minutes): "))
    except ValueError:
        duration = 0

    return duration


def prompt_ingredients() -> list[dict[str, Any]]:
    """Prompt the user to get the ingredient list."""
    ingredients = []
    while True:
        ingredient_name = input("Ingredient name: ")
        try:
            qty = float(input(f"Quantity for {ingredient_name}: "))
        except ValueError:
            qty = 0.0
        unit = input("Unit (e.g. cup, tsp): ").lower().strip()
        unit = unit if unit else None

        ingredients.append({"name": ingredient_name, "qty": qty, "unit": unit})

        if input("Add another ingredient? (y/n): ").lower() != "y":
            break

    return ingredients


def prompt_steps() -> list[dict[int, str]]:
    """Prompt the user for recipe steps."""
    steps = []
    while True:
        order = len(steps) + 1
        desc = input(f"Step {order} description: ")
        steps.append({"order": order, "desc": desc})

        if input("Add another step? (y/n): ").lower() != "y":
            break

    return steps


def prompt_tags() -> list[str]:
    """Prompt the user for tags to that categorize a recipe."""
    return input("Enter tags separated by spaces: ").lower().split()


def display_menu() -> None:
    """Display a user menu."""

    console = Console()

    table = Table(title="[bold green]Recipe Manager[/bold green]", show_header=False)
    table.add_row("[green]1.[/green]", "List all recipes")
    table.add_row("[green]2.[/green]", "Display a single recipe")
    table.add_row("[green]3.[/green]", "Search recipes by name")
    table.add_row("[green]4.[/green]", "Search recipes by ingredient")
    table.add_row("[green]5.[/green]", "Add recipe")
    table.add_row("[green]6.[/green]", "Edit recipe")
    table.add_row("[green]7.[/green]", "Archive recipe")
    table.add_row("[green]8.[/green]", "Quit")

    console.print(Panel(table, border_style="blue", expand=False))


def prompt_edit_choice(recipe: Recipe) -> str:
    """Prompt the user to determine the recipe section to edit."""
    console = Console()

    while True:
        console.clear()

        # Display the current recipe
        show_recipe(recipe)
        print(f"\nEditing: {recipe.name}")
        print("1. Edit Name")
        print("2. Edit Duration")
        print("3. Edit Ingredients (Add/Clear)")
        print("4. Edit Steps (Add/Clear)")
        print("5. Done / Save")

        return Prompt.ask(
            "Choose an attribute to edit", choices=["1", "2", "3", "4", "5"]
        )
