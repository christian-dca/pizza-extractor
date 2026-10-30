import os
import json
from pathlib import Path
from datetime import datetime
import re
from dotenv import load_dotenv

#Contains:
# check_apikeys()
# print_aimessage(ai_message)
# save_orders_to_file(content)
# load_orders_as_list(filename: str)
# save_extractrion_to_file



# Define project root
root_path = Path(__file__).resolve().parents[2]
orders_path = root_path / "data" / "test_orders"

#####################################################################################
# Check for env file and load apikeys
#####################################################################################

def check_apikeys():
    """Check and load apikeys from .env"""
    
    env_path = root_path / ".env"
    
    if not env_path.is_file():
        print(f".env file not found at {root_path}")
    else:
        load_dotenv(dotenv_path=env_path)

        placeholders = {
            "",
            "your_api_key_here",
        }

        api_key_names = sorted(
            name
            for name, value in os.environ.items()
            if "API_KEY" in name.upper()
            and value.strip()
            and value.strip().lower() not in placeholders
        )

        if api_key_names:
            print("Loaded API keys:")
            for name in api_key_names:
                print(f"- {name}")
        else:
            print("No API keys loaded.")


#####################################################################################
# Print out a message object
#####################################################################################

def print_aimessage(ai_message):
    for key, value in ai_message.model_dump().items():                #convert Ai-Message to Python dictionary and get items
        if isinstance(value, (dict, list)):                         #check if the value is a nested structure
            print(f"\n[{key}]:")                                    
            print(json.dumps(value, indent=2, ensure_ascii=False))  #converts a Python object into a JSON-formatted string. It’s commonly used to serialize data for storage or sending
        else:
            print(f"\n[{key}]: {value}")



#####################################################################################
# Save examples orders 
#####################################################################################

def save_orders_to_file(content, model_name) -> Path:
    """Saves the sample orders and returns path"""
    
    orders_path.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_model_name = re.sub(r'[:/\\]', '_', model_name)
        
    output_file = orders_path / f"pedidos_pizza_{safe_model_name}_{timestamp}.json"

    output_file.write_text(
        content.model_dump_json(indent=2),
        encoding="utf-8",
    )

    return output_file

#####################################################################################
# Load examples orders
#####################################################################################

def load_orders_as_list(filename: str) -> list[str]:
    """Loads a JSON file from data/example_orders and returns the orders as a list."""
    
    path = orders_path / filename
    data = json.loads(path.read_text(encoding="utf-8"))

    return [order["pizza_order"] for order in data["order_list"]]


#####################################################################################
# Save extraction results
#####################################################################################


def save_extraction_to_file(response_list, model_name: str) -> Path:
    
    extraction_path = root_path / "data" / "extraction_results"
    extraction_path.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Sanitize model name (no ":")
    safe_model_name = re.sub(r'[:/\\]', '_', model_name)

    filename = f"extraction_{safe_model_name}_{timestamp}.json"

    output_path = extraction_path / filename

    data = [item.model_dump(mode='json') for item in response_list]

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        
    print(f"Results saved under: {output_path}")
    return output_path, filename
