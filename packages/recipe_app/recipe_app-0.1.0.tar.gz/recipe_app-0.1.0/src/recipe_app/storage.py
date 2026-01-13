import json
from recipe_app.models import Recipe

RECIPE_FILE = "recipes.json"


def init() -> list[Recipe]:
    """Loads recipes into memory from .json file at startup"""
    # Recipes are stored in recipes.json in the working directory
    try:
        with open(RECIPE_FILE, "r") as jstream:
            json_dict = json.load(jstream)
            return [Recipe.from_file(item) for item in json_dict]
    except FileNotFoundError:
        return []
    except json.decoder.JSONDecodeError:
        return []


def exit_json_dump(recipe_list: list[dict]) -> None:
    """Pushes the recipe list to file prior to exiting."""
    # Recipes stored in recipes.json in the working directory.
    json_list = [recipe.to_file() for recipe in recipe_list]

    with open(RECIPE_FILE, "w") as json_file:
        json.dump(json_list, json_file)
