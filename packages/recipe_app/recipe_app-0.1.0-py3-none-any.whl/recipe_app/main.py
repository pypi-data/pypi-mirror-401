import typer
from typing import Optional
from rich.console import Console
from rich.prompt import Prompt
from recipe_app.services import (
    search_recipe_name,
    search_ingredient,
    add_recipe,
    edit_recipe,
    archive_recipe,
)
from recipe_app.ui import display_menu, show_recipe, list_recipes
from recipe_app.storage import init, exit_json_dump

app = typer.Typer()


@app.command()
def show(name: str):
    recipe_list = init()
    result = next(
        (recipe for recipe in recipe_list if name.lower() == recipe.name.lower()), None
    )
    if result:
        show_recipe(result)
    else:
        print(f"{name} doesn't exist in the recipe database.")


@app.command()
def add(rec_name: str):
    recipe_list = init()
    add_recipe(recipe_list, name=rec_name)


@app.command()
def search(
    recipe: Optional[str] = typer.Option(
        None, "--recipe", "-r", help="Search by recipe name"
    ),
    ingredient: Optional[str] = typer.Option(
        None, "--ingredient", "-i", help="Search by ingredient name"
    ),
):
    recipe_list = init()
    if recipe is not None:
        list_recipes(search_recipe_name(recipe, recipe_list))
    if ingredient is not None:
        list_recipes(search_ingredient(ingredient, recipe_list))


# This is applied to run main() when no command-line args are provided.
@app.callback(invoke_without_command=True)
def main(cmd: typer.Context) -> None:
    # This avoids running main() if a command is entered at the command line
    if cmd.invoked_subcommand:
        return

    # Initialize the program by recipes.json to a list of Recipe objects
    recipe_list = init()

    console = Console()
    while True:
        # Clear the screen before displaying the menu
        console.clear()
        display_menu()

        choice = Prompt.ask(
            "Choose an option",
            choices=["1", "2", "3", "4", "5", "6", "7", "8"],
            default="8",
        )

        if choice == "1":
            console.print("[yellow]Listing all recipes...[/yellow]")
            list_recipes(recipe_list)
        elif choice == "2":
            reply = Prompt.ask("Enter the recipe to display: ").lower()
            console.print("[yellow]Displaying recipe...[/yellow]")
            result = next(
                (recipe for recipe in recipe_list if reply == recipe.name.lower()), None
            )
            if result:
                show_recipe(result)
            else:
                console.print(f"{reply} doesn't exist in the recipe database.")
        elif choice == "3":
            reply = Prompt.ask("Enter search term")
            console.print(f"[yellow]Searching for '{reply}'...[/yellow]")
            list_recipes(search_recipe_name(reply, recipe_list))
        elif choice == "4":
            reply = Prompt.ask("Enter the ingredient to search")
            console.print(f"[yellow]Searching for '{reply}'...[/yellow]")
            list_recipes(search_ingredient(reply, recipe_list))
        elif choice == "5":
            console.print("[yellow]Adding a new recipe...[/yellow]")
            add_recipe(recipe_list)
        # Inside your main while loop:
        elif choice == "6":
            name_to_edit = Prompt.ask(
                "Enter the exact name of the recipe to edit"
            ).title()
            try:
                # Find the recipe object
                target_recipe = search_recipe_name(name_to_edit.lower(), recipe_list)
                # Edit it in place (it's a reference to the object in recipe_list)
                edit_recipe(target_recipe)
                console.print(
                    f"[bold green]Recipe '{target_recipe.name}' updated![/bold green]"
                )
            except StopIteration:
                console.print("[bold red]Recipe not found.[/bold red]")
                input("\nPress Enter to return to menu...")
        elif choice == "7":
            reply = Prompt.ask("Enter the recipe to archive").lower()
            console.print("[yellow]Archiving/Deleting recipe...[/yellow]")
            archive_recipe(search_recipe_name(reply, recipe_list))
        elif choice == "8":
            console.print("[bold red]Exiting...[/bold red]")
            break

        input("\nPress Enter to return to menu...")

    # Dump the Recipe objects back to file at exit
    exit_json_dump(recipe_list)


if __name__ == "__main__":
    app()
