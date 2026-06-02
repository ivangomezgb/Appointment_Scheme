import json
import os

# Rutas absolutas a los archivos de datos separados por módulo
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
PACIENTES_PATH = os.path.join(DATA_DIR, 'pacientes.json')
MEDICOS_PATH = os.path.join(DATA_DIR, 'medicos.json')
CITAS_PATH = os.path.join(DATA_DIR, 'citas.json')

RUTAS_DATOS = {
    "pacientes": PACIENTES_PATH,
    "medicos": MEDICOS_PATH,
    "citas": CITAS_PATH
}


def cargar_datos(rutas: dict = None) -> dict:
    """
    Lee archivos JSON desde las rutas especificadas.
    Si no se especifican rutas, usa RUTAS_DATOS por defecto.
    
    Args:
        rutas: Diccionario con clave: ruta (opcional)
    
    Returns:
        Diccionario con clave: contenido del JSON
    """
    if rutas is None:
        rutas = RUTAS_DATOS
    
    datos = {}
    for clave, ruta in rutas.items():
        try:
            with open(ruta, 'r', encoding='utf-8') as f:
                contenido = json.load(f)
                datos[clave] = contenido if isinstance(contenido, list) else []
        except:
            datos[clave] = []
    
    return datos


def guardar_datos(datos: dict, rutas: dict = None) -> None:
    """
    Guarda datos en archivos JSON en las rutas especificadas.
    Si no se especifican rutas, usa RUTAS_DATOS por defecto.
    
    Args:
        datos: Diccionario con clave: contenido a guardar
        rutas: Diccionario con clave: ruta (opcional)
    """
    if rutas is None:
        rutas = RUTAS_DATOS
    
    for clave, ruta in rutas.items():
        if clave in datos:
            try:
                with open(ruta, 'w', encoding='utf-8') as f:
                    json.dump(datos[clave], f, ensure_ascii=False, indent=4)
            except IOError as e:
                raise IOError(f"Error guardando {ruta}: {e}")