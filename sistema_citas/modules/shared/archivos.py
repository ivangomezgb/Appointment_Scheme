"""
Módulo compartido para manejo de archivos JSON.
Provee funciones reutilizables para leer, escribir y gestionar archivos JSON
de forma robusta con manejo de errores.
"""

import json
import os
from pathlib import Path
from rich.console import Console

# Instancia global de Console para este módulo
console = Console()


def leer_json(ruta_archivo: str, default=None):
    """
    Lee un archivo JSON y devuelve su contenido.
    
    Args:
        ruta_archivo (str): Ruta al archivo JSON.
        default: Valor por defecto si el archivo no existe o está corrupto.
                 Si no se especifica, usa lista vacía [].
    
    Returns:
        Contenido del JSON (list/dict) o default si falla.
    
    Ejemplos:
        >>> medicos = leer_json("data/medicos.json")
        >>> config = leer_json("config.json", default={})
    """
    if default is None:
        default = []
    
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
            return json.load(archivo)
    
    except FileNotFoundError:
        console.print(f"[yellow]⚠ Archivo no encontrado: {ruta_archivo}. Usando datos por defecto.[/yellow]")
        return default
    
    except json.JSONDecodeError as e:
        console.print(f"[red]✗ Error al leer JSON en {ruta_archivo}: {e}[/red]")
        console.print(f"[yellow]⚠ Usando datos por defecto.[/yellow]")
        return default
    
    except PermissionError:
        console.print(f"[red]✗ Sin permisos para leer: {ruta_archivo}[/red]")
        return default
    
    except Exception as e:
        console.print(f"[red]✗ Error inesperado al leer {ruta_archivo}: {e}[/red]")
        return default


def escribir_json(ruta_archivo: str, datos) -> bool:
    """
    Escribe datos en un archivo JSON con formato legible.
    Crea el directorio automáticamente si no existe.
    
    Args:
        ruta_archivo (str): Ruta al archivo JSON.
        datos (list/dict): Datos a guardar.
    
    Returns:
        bool: True si guardó correctamente, False si falló.
    
    Ejemplos:
        >>> medicos = [{"id": "M001", "nombre": "Dr. García"}]
        >>> escribir_json("data/medicos.json", medicos)
        True
    """
    try:
        # Asegurar que el directorio existe
        Path(ruta_archivo).parent.mkdir(parents=True, exist_ok=True)
        
        with open(ruta_archivo, 'w', encoding='utf-8') as archivo:
            json.dump(datos, archivo, indent=4, ensure_ascii=False)
        
        return True
    
    except PermissionError:
        console.print(f"[red]✗ Sin permisos para escribir en: {ruta_archivo}[/red]")
        return False
    
    except OSError as e:
        console.print(f"[red]✗ Error al escribir en {ruta_archivo}: {e}[/red]")
        return False
    
    except Exception as e:
        console.print(f"[red]✗ Error inesperado al escribir {ruta_archivo}: {e}[/red]")
        return False


def asegurar_archivo_json(ruta_archivo: str, default=None) -> bool:
    """
    Crea un archivo JSON con contenido inicial si no existe.
    Si el archivo ya existe, no hace nada.
    
    Args:
        ruta_archivo (str): Ruta al archivo JSON.
        default (list/dict): Contenido inicial. Por defecto: lista vacía [].
    
    Returns:
        bool: True si el archivo existe o se creó correctamente, False si falló.
    
    Ejemplos:
        >>> asegurar_archivo_json("data/medicos.json", [])
        True
        >>> asegurar_archivo_json("data/config.json", {"version": "1.0"})
        True
    """
    if default is None:
        default = []
    
    if os.path.exists(ruta_archivo):
        return True  # Ya existe, no hacer nada
    
    console.print(f"[cyan]ℹ Creando archivo: {ruta_archivo}[/cyan]")
    return escribir_json(ruta_archivo, default)


def archivo_existe(ruta_archivo: str) -> bool:
    """
    Verifica si un archivo existe.
    
    Args:
        ruta_archivo (str): Ruta al archivo.
    
    Returns:
        bool: True si existe, False si no.
    
    Ejemplos:
        >>> if archivo_existe("data/medicos.json"):
        ...     print("El archivo existe")
    """
    return os.path.exists(ruta_archivo)


def obtener_ruta_data(nombre_archivo: str) -> str:
    """
    Construye la ruta completa a un archivo en la carpeta data/.
    Útil para evitar escribir rutas completas repetidamente.
    
    Args:
        nombre_archivo (str): Nombre del archivo (ej: "medicos.json").
    
    Returns:
        str: Ruta completa (ej: "sistema_citas/data/medicos.json").
    
    Ejemplos:
        >>> ruta = obtener_ruta_data("medicos.json")
        >>> medicos = leer_json(ruta)
    """
    return os.path.join("sistema_citas", "data", nombre_archivo)


def crear_backup(ruta_archivo: str) -> bool:
    """
    Crea una copia de respaldo de un archivo JSON.
    El backup se guarda con extensión .backup.json
    
    Args:
        ruta_archivo (str): Ruta al archivo original.
    
    Returns:
        bool: True si creó el backup, False si falló.
    
    Ejemplos:
        >>> crear_backup("data/medicos.json")
        # Crea: data/medicos.backup.json
    """
    if not os.path.exists(ruta_archivo):
        console.print(f"[yellow]⚠ No se puede hacer backup: {ruta_archivo} no existe[/yellow]")
        return False
    
    try:
        datos = leer_json(ruta_archivo)
        ruta_backup = ruta_archivo.replace(".json", ".backup.json")
        exito = escribir_json(ruta_backup, datos)
        
        if exito:
            console.print(f"[green]✓ Backup creado: {ruta_backup}[/green]")
        
        return exito
    
    except Exception as e:
        console.print(f"[red]✗ Error al crear backup: {e}[/red]")
        return False


def contar_registros(ruta_archivo: str) -> int:
    """
    Cuenta cuántos registros hay en un archivo JSON (asume que es una lista).
    
    Args:
        ruta_archivo (str): Ruta al archivo JSON.
    
    Returns:
        int: Número de registros, 0 si el archivo no existe o está vacío.
    
    Ejemplos:
        >>> total = contar_registros("data/medicos.json")
        >>> print(f"Hay {total} médicos registrados")
    """
    datos = leer_json(ruta_archivo, default=[])
    
    if isinstance(datos, list):
        return len(datos)
    else:
        console.print(f"[yellow]⚠ {ruta_archivo} no contiene una lista[/yellow]")
        return 0


def limpiar_archivo(ruta_archivo: str) -> bool:
    """
    Vacía un archivo JSON (lo deja como lista vacía []).
    Útil para resetear datos en desarrollo/testing.
    
    Args:
        ruta_archivo (str): Ruta al archivo JSON.
    
    Returns:
        bool: True si se limpió correctamente, False si falló.
    
    Ejemplos:
        >>> limpiar_archivo("data/medicos_test.json")
        True
    """
    return escribir_json(ruta_archivo, [])