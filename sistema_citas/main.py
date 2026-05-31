"""main.py  —  raíz del repositorio
Integrante 4 mariam: integración y menú principal
 
Este archivo NO toca el código de nadie.Solo importa lo que cada compañero ya hizo
y lo conecta en un menú con la libreria rich establecida en los requisitos.

RESPONSABILIDAD DE ESTE ARCHIVO:
  Este archivo es el PUNTO DE ENTRADA del sistema. Su única tarea es mostrar el menú principal y delegar el control a cada módulo cuando el usuario elige una opción.
  NO contiene lógica de negocio (eso lo hacen los módulos).
 
CÓMO FUNCIONA EL FLUJO:
  1. El usuario ejecuta:  python main.py
  2. Se ejecuta menu_principal()
  3. El usuario ve las opciones y elige un número
  4. main.py llama a la función del módulo correspondiente
     (menu_pacientes, menu_medicos o menu_citas)
  5. El control pasa al módulo — main.py "espera"
  6. Cuando el usuario escribe 0 en el submenú, la función del módulo termina y el control regresa aquí
  7. El bucle while repite desde el paso 2
 
PRINCIPIO DE RESPONSABILIDAD ÚNICA aplicado aquí:
  Cada función de este archivo tiene UNA SOLA tarea:
    - mostrar_encabezado()  → solo dibuja el banner
    - mostrar_resumen()     → solo muestra los conteos
    - mostrar_opciones()    → solo imprime las opciones
    - buscar_global()       → solo coordina la búsqueda
    - menu_principal()      → solo orquesta el flujo

"""
# Implementacion de libreria rich

from rich.console import Console 
from rich.panel   import Panel  # → caja con borde para el encabezado
from rich.table   import Table  # → tabla con columnas alineadas
from rich.prompt import Prompt

import modules.pacientes.pacientes as pacientes_module
from modules.pacientes.validaciones_pacientes import (
    solicitar_id_paciente,
    solicitar_nombre_paciente,
    solicitar_telefono_paciente,
)

#1 funcion reutilizable para json para leer el archivo y obtener ruta asi:

from modules.shared.archivos import (
    leer_json, #→ lee un archivo .json y devuelve una lista
    obtener_ruta_data, #→ construye la ruta a la carpeta data/
)
# Estas funciones las hizo el equipo en shared/ para que TODOS los módulos las usen sin repetir código (DRY). 

# =========================================================================
#2 funcion / IMPORTAR EL MENU DE CADA MODULO / 
# - cada integrante exporta Una funcion menu_X() DESDE su modulo
# - El try/except permite que el sistema arranque aunque un módulo aún no esté listo: lo marca como "en desarrollo" en lugar de explotar con un ImportError.

try:
    from modules.pacientes.pacientes import menu_pacientes
    _PACIENTES_LISTO = True
except ImportError:
    _PACIENTES_LISTO = False   # módulo pendiente de su integrante
 
try:
    from modules.medicos.medicos import menu_medicos
    _MEDICOS_LISTO = True
except ImportError:
    _MEDICOS_LISTO = False
 
try:
    from modules.citas.citas import menu_citas
    _CITAS_LISTO = True
except ImportError:
    _CITAS_LISTO = False


    
console = Console()

# ==========================================
# INTERFACES VISUALES (PEGA ESTO AL FINAL)
# ==========================================

def mostrar_tabla_pacientes():
    """Muestra la lista de pacientes en una tabla elegante de Rich."""
    # Usamos tu alias: pacientes_module
    pacientes = pacientes_module.listar_pacientes()
    
    if not pacientes:
        console.print("[bold yellow]⚠️ No hay pacientes registrados en el sistema.[/bold yellow]")
        return

    # Creamos la estructura de la tabla con Rich
    tabla = Table(title="📋 LISTADO DE PACIENTES", title_style="bold magenta", header_style="bold cyan")
    tabla.add_column("ID Paciente", justify="center", style="bold green")
    tabla.add_column("Nombre Completo", justify="left")
    tabla.add_column("Teléfono", justify="center")

    # Llenamos la tabla con los datos del JSON
    for p in pacientes:
        tabla.add_row(str(p["id_paciente"]), p["nombre"], p["telefono"])

    console.print(tabla)


def interfaz_actualizar_paciente():
    """Interfaz para solicitar el ID y los nuevos datos de un paciente."""
    console.print(Panel("[bold yellow]🔄 ACTUALIZAR DATOS DE PACIENTE[/bold yellow]"))
    
    id_a_buscar = solicitar_id_paciente("Ingrese el ID del paciente que desea modificar")
    paciente = pacientes_module.obtener_paciente_por_id(id_a_buscar)
    
    if not paciente:
        console.print("[bold red]❌ Error: No se encontró ningún paciente con ese ID.[/bold red]")
        return

    console.print(f"[gray]Modificando a: {paciente['nombre']} (Tel: {paciente['telefono']})[/gray]\n")
    
    nuevo_nombre = solicitar_nombre_paciente()
    nuevo_telefono = solicitar_telefono_paciente()
    
    exito = pacientes_module.actualizar_paciente(id_a_buscar, nuevo_nombre, nuevo_telefono)
    
    if exito:
        console.print("[bold green]✨ ¡Paciente actualizado correctamente! ✨[/bold green]")


def interfaz_eliminar_paciente():
    """Interfaz para eliminar un paciente por ID."""
    console.print(Panel("[bold red]❌ ELIMINAR PACIENTE DEL SISTEMA[/bold red]"))
    
    id_a_borrar = solicitar_id_paciente("Ingrese el ID del paciente que desea eliminar")
    
    confirmacion = Prompt.ask(f"[bold yellow]¿Está seguro de eliminar al paciente ID {id_a_borrar}? (s/n)[/bold yellow]", choices=["s", "n"], default="n")
    
    if confirmacion == "s":
        exito = pacientes_module.eliminar_paciente(id_a_borrar)
        if exito:
            console.print("[bold green]🗑️ El paciente fue eliminado con éxito.[/bold green]")
        else:
            console.print("[bold red]❌ Error: El ID ingresado no existe.[/bold red]")
    else:
        console.print("[bold blue]🚫 Operación cancelada.[/bold blue]")
