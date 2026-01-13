from rich.prompt import Prompt
from recipe_app.models import Recipe, Ingredient, Step, Unit
from recipe_app.ui import (
    prompt_recipe_name,
    prompt_duration,
    prompt_ingredients,
    prompt_steps,
    prompt_tags,
    prompt_edit_choice,
)


def add_recipe(recipe_list: list[Recipe], name=None) -> list[Recipe]:
    """Prompt user for recipe info and add new recipe to the existing list."""

    # prompt the user for recipe information
    if name is None:
        name = prompt_recipe_name()
    duration = prompt_duration()
    ingredients = prompt_ingredients()
    steps = prompt_steps()
    tags = prompt_tags()

    # Combine the user input data into a dictionary
    new_recipe_data = {
        "name": name,
        "duration": duration,
        "ingredients": ingredients,
        "steps": steps,
        "tags": tags,
    }

    # Convert the dict to a Recipe instance and append it to the existing list
    new_recipe_obj = Recipe.from_file(new_recipe_data)
    recipe_list.append(new_recipe_obj)

    return recipe_list


def archive_recipe(recipe: Recipe) -> None:
    """Unsets the Recipe active flag."""
    recipe.active = False


def search_recipe_name(value: str, recipe_list: list[Recipe]) -> list[Recipe]:
    """Returns a recipe names matching a user entered value."""
    return [recipe for recipe in recipe_list if value.lower() in recipe.name.lower()]


def search_ingredient(value: str, recipe_list: list[Recipe]) -> list[Recipe]:
    """Searches for recipes containing a specified ingredient."""
    results = [item for item in recipe_list if (value in item) and item.active]
    return results


def edit_recipe(recipe: Recipe) -> Recipe:
    """Modifies the contents of an existing recipe using interactive prompts."""

    while True:
        choice = prompt_edit_choice(recipe)

        if choice == "1":
            new_name = Prompt.ask("Enter new name", default=recipe.name)
            recipe.name = new_name

        elif choice == "2":
            new_dur = Prompt.ask("Enter new duration", default=str(recipe.duration))
            recipe.duration = int(new_dur)

        elif choice == "3":
            # Simple approach: ask to add more or reset
            sub_choice = Prompt.ask(
                "Add (a)nditional ingredients or (c)lear and restart?",
                choices=["a", "c"],
            )
            if sub_choice == "c":
                recipe.ingredients = []

            # Use logic similar to add_recipe to populate
            while True:
                name = Prompt.ask("Ingredient name (or 'done')")
                if name.lower() == "done":
                    break
                qty = float(Prompt.ask(f"Quantity for {name}", default="1"))
                unit = Prompt.ask(
                    "Unit", choices=[u.value for u in Unit], default=Unit.GRAM.value
                )
                recipe.ingredients.append(Ingredient(name=name, qty=qty, unit=unit))

        elif choice == "4":
            sub_choice = Prompt.ask(
                "Add (a)nditional steps or (c)lear and restart?", choices=["a", "c"]
            )
            if sub_choice == "c":
                recipe.steps = []

            curr_order = len(recipe.steps) + 1
            while True:
                desc = Prompt.ask(f"Step {curr_order} (or 'done')")
                if desc.lower() == "done":
                    break
                recipe.steps.append(Step(order=curr_order, desc=desc))
                curr_order += 1

        elif choice == "5":
            break

    return recipe
