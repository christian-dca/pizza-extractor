from typing import List, Literal, Optional
from pydantic import BaseModel, Field
import json


class ToppingModifier(BaseModel):
    ingredient: str = Field(
        ..., 
        description="Base name of the topping only, without quantities (e.g., 'pepperoni', 'mushrooms')."
    )
    modifier_level: Optional[Literal["light", "normal", "extra"]] = Field(
        default="normal",
        description="Amount of the topping requested."
    )
    action: Literal["add", "remove"] = Field(
        ..., 
        description=(
            "Use 'add' for initial toppings on a custom pizza OR extra toppings added to a preset. "
            "Use 'remove' for toppings held, removed from a preset."
        )
    )
    target: Literal["whole", "half_1", "half_2"] = Field(
        default="whole", 
        description="Applies to whole pizza or a specific half in split orders."
    )


class Pizza(BaseModel):
    is_split: bool = Field(
        default=False, 
        description="Set to true if the pizza has two distinct half-and-half styles."
    )
    preset_name: Optional[str] = Field(
        default=None, 
        description=(
            "Base pizza recipe name (e.g., 'Margherita', 'Meat Lovers') if the pizza is not a split pizza."
            "Leave null if unspecified or ambiguous."
        )
    )
    size: Optional[Literal["small", "medium", "large"]] = Field(
        default=None,
        description=(
            "Standard size category. Map synonyms to 'small', 'medium', or 'large'. "
            "Leave null if unspecified or ambiguous."
        )
    )
    crust_type: Optional[str] = Field(
        default=None, 
        description="Type of crust (e.g., 'thin', 'thick', 'stuffed'). Leave null if omitted by customer."
    )
    sauce_type: Optional[str] = Field(
        default=None, 
        description="Base sauce type. Leave null if omitted by customer."
    )
    sauce_level: Optional[Literal["light", "normal", "extra", "no_sauce"]] = Field(
        default=None, 
        description="Desired amount of sauce if specified by customer. Choose no_sauce if customer requests explicitly  no sauce"
    )
    first_half_preset: Optional[str] = Field(
            default=None, 
            description="Base recipe name for the first half if this is a split pizza."
        )
    second_half_preset: Optional[str] = Field(
        default=None, 
        description="Base recipe name for the second half if this is a split pizza."
    )
    topping_modifiers: List[ToppingModifier] = Field(
        default_factory=list, 
        description="List of topping additions or removals."
    )
    special_instructions: list[str] = Field(
    default_factory=list,
    description=(
        "Use ONLY for custom requests that cannot fit standard fields "
        "Do NOT place standard toppings, sizes, or crust choices here."
    )
)

class PizzaOrder(BaseModel):
    
    pizzas: List[Pizza] = Field(
        default_factory=list, 
        description="List of all pizza items in the order."
    )





def get_flattened_json_schema() -> dict:
    """Generiert das JSON-Schema aus PizzaOrder und löst alle $ref-Referenzen inline auf."""
    schema = PizzaOrder.model_json_schema()
    defs = schema.pop("$defs", {})

    def _resolve_refs(obj):
        if isinstance(obj, dict):
            if "$ref" in obj:
                # Extrahiere den Klassennamen aus "#/$defs/Pizza"
                ref_name = obj["$ref"].split("/")[-1]
                resolved = defs.get(ref_name, {}).copy()
                return _resolve_refs(resolved)
            return {k: _resolve_refs(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [_resolve_refs(item) for item in obj]
        return obj

    return _resolve_refs(schema)

if __name__ == "__main__":
    json_schema = get_flattened_json_schema()
    #json_schema = json.dumps(PizzaOrder.model_json_schema(), indent=2)
    print(json_schema)
    
