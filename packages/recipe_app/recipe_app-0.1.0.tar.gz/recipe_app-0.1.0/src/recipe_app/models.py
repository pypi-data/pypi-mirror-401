from enum import Enum
from typing import List, Any, Optional
from pydantic import BaseModel


class Unit(str, Enum):
    """Units for ingredients (gram, liter, etc)."""

    GRAM = "gram"
    CUP = "cup"
    OUNCE = "ounce"
    POUND = "pound"
    LITER = "liter"
    MILLILITER = "milliliter"
    PINT = "pint"
    TEASPOON = "teaspoon"
    TABLESPOON = "tablespoon"
    QUART = "quart"
    GALLON = "gallon"


class Tag(str, Enum):
    """A way to label a recipe (dinner, breakfast, easy, etc)."""

    DINNER = "dinner"
    BREAKFAST = "breakfast"
    DESSERT = "dessert"
    SNACK = "snack"
    COCKTAIL = "cocktail"
    EASY = "easy"
    SPICY = "spicy"
    HOT = "hot"
    COLD = "cold"
    VEGETARIAN = "vegetarian"


class Step(BaseModel):
    order: int
    desc: str


class Ingredient(BaseModel):
    name: str
    qty: float
    unit: Optional[Unit] = None


class Recipe(BaseModel):
    """Represents a complete recipe: ingredients, steps, duration, and tag."""

    # Uncomment lines to test adding recipes with name only.
    name: str
    ingredients: List[Ingredient]  # = Field(default_factory=list)
    steps: List[Step]  # = Field(default_factory=list)
    tags: List[Tag]  # = Field(default_factory=list)
    duration: int = 30  # Default value handled automatically
    active: bool = True

    def __str__(self) -> str:
        """Simple string representation of the recipe."""
        return f"Recipe: {self.name} | {self.duration} minutes"

    def __contains__(self, item: str) -> bool:
        """Checks if an ingredient is listed in the recipe."""
        return any(ingredient.name == item for ingredient in self.ingredients)

    def to_file(self) -> dict[str, Any]:
        """Converts the Recipe to a dictionary for file output."""
        return self.model_dump()

    @classmethod
    def from_file(cls, data: dict[str, Any]) -> "Recipe":
        """Converts a stored dictionary into a Recipe instance."""
        return cls.model_validate(data)

