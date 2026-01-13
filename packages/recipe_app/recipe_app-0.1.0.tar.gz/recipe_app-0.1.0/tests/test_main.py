import pytest

from main import Recipe, Tag


@pytest.fixture
def raw_dict() -> dict:
    return {
        "name": "Pancakes",
        "ingredients": [
            {"name": "Flour", "qty": 200, "unit": "gram"},
            {"name": "Milk", "qty": 300, "unit": "milliliter"},
            {"name": "Eggs", "qty": 2, "unit": "ounce"},
        ],
        "steps": [
            {"order": 1, "desc": "Mix all ingredients."},
            {"order": 2, "desc": "Pour batter onto griddle."},
            {"order": 3, "desc": "Cook until golden brown."},
        ],
        "tags": ["breakfast", "easy"],
    }


@pytest.fixture
def recipe(raw_dict) -> Recipe:
    return Recipe.model_validate(raw_dict)


def test_deserialize_recipe(raw_dict, recipe):
    assert recipe.name == "Pancakes"
    assert len(recipe.ingredients) == 3
    assert recipe.ingredients[0].name == "Flour"
    assert recipe.steps[1].desc == "Pour batter onto griddle."
    assert Tag.BREAKFAST in recipe.tags


def test_serialize_to_json(recipe):
    raw_out = recipe.model_dump(mode="json")
    assert raw_out["name"] == "Pancakes"
    assert raw_out["ingredients"][0]["name"] == "Flour"
    assert raw_out["steps"][1]["desc"] == "Pour batter onto griddle."
    assert "breakfast" in raw_out["tags"]


def test_serialize_to_json_string(recipe):
    json_str = recipe.model_dump_json()
    assert (
        json_str
        == '{"name":"Pancakes","ingredients":[{"name":"Flour","qty":200.0,"unit":"gram"},{"name":"Milk","qty":300.0,"unit":"milliliter"},{"name":"Eggs","qty":2.0,"unit":"ounce"}],"steps":[{"order":1,"desc":"Mix all ingredients."},{"order":2,"desc":"Pour batter onto griddle."},{"order":3,"desc":"Cook until golden brown."}],"tags":["breakfast","easy"]}'
    )
