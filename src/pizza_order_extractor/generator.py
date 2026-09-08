from langchain.chat_models import init_chat_model

import ast
import json
from datetime import datetime
from pathlib import Path
import os
import dotenv


if "ANTHROPIC_API_KEY" not in os.environ:
    os.environ["ANTHROPIC_API_KEY"] = getpass.getpass("Introduce tu  AWS Key: ")

def generate_example_orders(model_name, prompt, provider=None):
    model = init_chat_model(
        model_name,
        model_provider=provider,
        max_tokens=1000,
    )
    response = model.invoke(prompt)
    return response

def save_orders_to_file(content: str, output_dir: str = "data/processed") -> Path:
    """Guarda el texto generado en un archivo con timestamp."""
    data_path = Path(output_dir)
    data_path.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = data_path / f"pedidos_pizza_{timestamp}.txt"
    
    output_file.write_text(content, encoding="utf-8")
    return output_file



def load_orders_as_list(file_path: str | Path) -> list[str]:
    """Lee un archivo generado y devuelve las órdenes como una lista de Python."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"El archivo {path} no existe.")
        
    content = path.read_text(encoding="utf-8").strip()
    
    # Intento 1: Parsear como JSON estándar (Recomendado)
    try:
        data = json.loads(content)
        if isinstance(data, dict) and "orders" in data:
            return data["orders"]
        elif isinstance(data, list):
            return data
    except json.JSONDecodeError:
        pass

    # Intento 2: Si el archivo se guardó literalmente como sintaxis de lista Python [...]
    try:
        data = ast.literal_eval(content)
        if isinstance(data, list):
            return data
    except (ValueError, SyntaxError):
        pass

    # Intento 3: Fallback por líneas si el formato no era JSON ni sintaxis Python
    return [line.strip() for line in content.splitlines() if line.strip()]

if __name__ == "__main__":
    result = generate_example_orders()
    print(result)