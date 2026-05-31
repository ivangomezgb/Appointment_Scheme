import json
import os

# Ruta absoluta al archivo de datos, relativa a este módulo
DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'datos.json')

ESTRUCTURA_INICIAL = {
    "pacientes": [],
    "medicos": [],
    "citas": []
}


def cargar_datos() -> dict:
    """
    Lee el archivo JSON y retorna el diccionario con todos los datos.
    Si el archivo no existe o está corrupto, retorna la estructura inicial vacía.
    """
    try:
        with open(DATA_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return ESTRUCTURA_INICIAL.copy()
    except json.JSONDecodeError:
        # Archivo corrupto: retorna estructura vacía para no romper la app
        return ESTRUCTURA_INICIAL.copy()


def guardar_datos(datos: dict) -> None:
    """
    Escribe el diccionario completo en el archivo JSON con formato legible.
    """
    try:
        with open(DATA_PATH, 'w', encoding='utf-8') as f:
            json.dump(datos, f, ensure_ascii=False, indent=4)
    except IOError as e:
        raise IOError(f"No se pudo guardar el archivo de datos: {e}")