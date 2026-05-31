"""utils/menu.py  —  Herramientas visuales reutilizables
RESPONSABLE : Integrante 4 mariam — Integración y estructura general
UBICACIÓN   : sistema_citas/utils/menu.py

OBJETIVO DE ESTE ARCHIVO:
  Centralizar todas las funciones de presentación visual
  que los módulos necesitan repetidamente.
  Sin este archivo, cada módulo (pacientes, médicos, citas)
  tendría que escribir su propio código para mostrar mensajes
  de error, éxito, pausas, etc. Eso viola el principio DRY
  (Don't Repeat Yourself — no te repitas).
  
  Con este archivo, cualquier módulo hace:
      from modules.utils.menu import msg_exito, pausar
        y ya tiene las funciones listas.

PRINCIPIO DE RESPONSABILIDAD ÚNICA aplicado aquí:
  Cada función tiene UNA SOLA tarea visual:
    - limpiar_pantalla()  → solo limpia la consola
    - pausar()            → solo espera un Enter
    - msg_exito()         → solo muestra mensaje verde
    - msg_error()         → solo muestra mensaje rojo
    - msg_advertencia()   → solo muestra mensaje amarillo
    - mostrar_tabla()     → solo construye y muestra una tabla
    - confirmar()         → solo pide confirmación s/n

QUIÉN USA ESTE ARCHIVO:
  - main.py               importa limpiar_pantalla, pausar
  - módulo pacientes      importa msg_exito, msg_error, pausar
  - módulo médicos        importa msg_exito, msg_error, pausar
  - módulo citas          importa msg_exito, msg_error, pausar
  -Todos importan desde el mismo lugar → sin código duplicado.
════════════════════════════════════════════════════════════════
"""

import os # Proporciona funciones para interactuar con el sistema operativo
import subprocess # Permite crear nuevos procesos, ejecutar comandos del sistema


from rich.console import Console #→ objeto principal para imprimir con colores
from rich.table import Table #→ construye tablas con columnas alineadas
from rich.panel import Panel #→ caja con borde decorativo
from rich import box as rich_box
from rich.prompt import Prompt

import modules.pacientes.pacientes as pacientes_module
from modules.pacientes.validaciones_pacientes import (
    solicitar_id_paciente,
    solicitar_nombre_paciente,
    solicitar_telefono_paciente,
)

# Instancia compartida de Console para todo este archivo
console = Console()

# ════════════════════════════════════════════════════════════════
# FUNCIÓN 1: limpiar_pantalla
# ════════════════════════════════════════════════════════════════
def limpiar_pantalla() -> None:
    """ Limpia la consola según el sistema operativo utilizando subprocess con manejo de errorres.
    
    Esta función detecta automáticamente el sistema operativo y 
    ejecuta el comando apropiado para limpiar la pantalla de la terminal/consola. el(.name) retorna:
    - Windows: ["cmd", "/c", "cls"] ='nt'
      * "cmd"  : Invoca el intérprete de comandos de Windows
      * "/c"   : Ejecuta el comando y termina (Carry out)
      * "cls"  : Limpia la pantalla (CLear Screen)
    
    - Linux/macOS: ["clear"] ='posix'
      * "clear": Comando nativo que limpia la terminal
    """
    try:
        if os.name == "nt":  # Si es Windows
            subprocess.run(["cmd", "/c", "cls"], check=True)
        else:  # Si es Linux, macOS o cualquier Unix-like
            subprocess.run(["clear"],check=True)
    except subprocess.SubprocessError as error:
        console.print(f"[red]Error al limpiar pantalla: {error}[/red]")
   
# ════════════════════════════════════════════════════════════════
# FUNCIÓN 2: pausar
# ════════════════════════════════════════════════════════════════
def pausar() -> None:
    """ Pausa la ejecución del programa hasta que el usuario presione enter
    'Presione Enter para continuar...' y espera input.
    """
    console.print("\n[dim]  Presione Enter para continuar...[/dim]", end="")
    input() # Espera silenciosamente la entrada del usuario

# ════════════════════════════════════════════════════════════════
# FUNCIÓN 3: msg_exito 🦸🏼‍♂️ Muestra: " ✓ Archivo guardado correctamente" en verde y negrita
# ════════════════════════════════════════════════════════════════
def msg_exito(texto: str) -> None:
    console.print(f"\n[bold green]  ✔  {texto}[/bold green]")

# ════════════════════════════════════════════════════════════════
# FUNCIÓN 4: msg_error 🚫 Para errores esperados y controlables /contrario a msg exito
# ════════════════════════════════════════════════════════════════
def msg_error(texto: str) -> None:
    console.print(f"\n[bold red]  ✘  {texto}[/bold red]")

# ════════════════════════════════════════════════════════════════
# FUNCIÓN 5: msg_advertencia ☣️ 
# ════════════════════════════════════════════════════════════════
def msg_advertencia(texto: str) -> None:
    """Muestra un mensaje de advertencia en color amarillo.
    Consejos de uso 
    - Acciones que podrían tener consecuencias
    - Estado inesperado pero no crítico
    - Recordatorios importantes
    - Pasos que requieren confirmación
    """
    console.print(f"\n[bold yellow]  ⚠  {texto}[/bold yellow]")

# ════════════════════════════════════════════════════════════════
# FUNCIÓN 6: confirmar :)
# ════════════════════════════════════════════════════════════════
def confirmar(pregunta: str = "¿Confirmar esta acción?") -> bool:
    """
    Muestra una pregunta de confirmación y espera s o n. = retorna con boleanos
    es muy parecido cuando se usa la libreria de prompt rich .ask
    """
    respuesta = input(f"\n  [?] {pregunta} (s/n): ").strip().lower() 
    #elimina los espacios y pone la respuesta ingresada en miniscula
    return respuesta == "s" #: Compara si es exactamente 's'

# ════════════════════════════════════════════════════════════════
# FUNCIÓN 7: mostrar_tabla
# ════════════════════════════════════════════════════════════════
def mostrar_tabla(
    titulo: str,
    columnas: list[str],
    filas: list[list[str]],
    color_borde: str = "cyan",
) -> None:
    
    """"🤘🏼🙏🏼🫱🏽‍🫲🏽CONSEJOS DE USO PARA NUESTROS EJERCICIOS: 
    título : str
        Título que aparecerá sobre la tabla
        
    columnas : list[str] / Lista con nombres de las columnas 
    ej: ["ID", "Nombre", "Edad"] / columnas = ["Producto", "Precio", "Stock"]
        
    filas : list[list[str]] / Lista de listas con los datos de cada fila
        ej: [["1", "Ana", "25"], ["2", "Luis", "30"]]
        >>> filas = [
    ...     ["Laptop", "$800", "5"],
    ...     ["Mouse", "$25", "12"]
    ... ]
    >>> mostrar_tabla("Inventario", columnas, filas, "green")

    --------------------  Flujo de la función:  --------------------
    1. Validar si hay datos / 2. Crear objeto Table 
    / 3. Agregar columnas / 4. Agregar filas /5. Mostrar la tabla """

    if not filas:
        msg_advertencia(f"No hay datos para mostrar en '{titulo}'.")
        return #- Si no hay filas, muestra advertencia en lugar de tabla vacía

    # Construir la tabla con rich
    tabla = Table(
        title=titulo,
        border_style=color_borde,
        box=rich_box.ROUNDED,
        show_lines=False,
    )

    # Agregar cada columna- + ... enumerate es como se usa range y len asi :
    # for i in range(len(columnas)): / nombre_col = columnas[i]
    for i, nombre_col in enumerate(columnas):
        if i == 0:
            tabla.add_column(nombre_col, style=f"bold {color_borde}", justify="center")
        else:
            tabla.add_column(nombre_col)

    # Agregar cada fila
    for fila in filas:
        tabla.add_row(*[str(celda) for celda in fila])
    
    # 2. Metemos la tabla dentro de un panel decorativo
    panel = Panel(tabla, title="[bold yellow]Sistema Médico[/]", expand=False)
    console.print(panel)

# ════════════════════════════════════════════════════════════════
# FUNCIÓN 8: mostrar_titulo_seccion -  Muestra una línea de título para separar secciones.
# ════════════════════════════════════════════════════════════════
def mostrar_titulo_seccion(titulo: str, color: str = "cyan") -> None:
    console.print(f"\n[bold {color}]── {titulo} ──[/bold {color}]")

    

    