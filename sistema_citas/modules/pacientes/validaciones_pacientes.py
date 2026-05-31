from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
import modules.pacientes.pacientes as pacientes_module

console = Console()

def solicitar_nombre_paciente() -> str:
    """Solicita el nombre del paciente y valida que no esté vacío."""
    while True:
        nombre = Prompt.ask("[bold cyan]Ingrese el nombre completo del paciente[/bold cyan]")
        if nombre.strip():
            return nombre.strip()
        console.print("[bold red]❌ El nombre no puede estar vacío. Inténtelo de nuevo.[/bold red]")


def solicitar_telefono_paciente() -> str:
    """Solicita el teléfono del paciente y valida que sea un número válido."""
    while True:
        telefono = Prompt.ask("[bold cyan]Ingrese el teléfono del paciente (ej: 3101234567)[/bold cyan]")
        # Validación simple: que contenga solo números y tenga una longitud lógica
        if telefono.strip().isdigit() and len(telefono.strip()) >= 7:
            return telefono.strip()
        console.print("[bold red]❌ Teléfono inválido. Ingrese solo números (mínimo 7 dígitos).[/bold red]")


def solicitar_id_paciente(mensaje: str = "Ingrese el ID del paciente") -> int:
    """
    Solicita un ID numérico al usuario implementando manejo de errores (try-except)
    para evitar que la aplicación se rompa si ingresan texto.
    """
    while True:
        id_texto = Prompt.ask(f"[bold magenta]{mensaje}[/bold magenta]")
        try:
            id_paciente = int(id_texto)
            if id_paciente > 0:
                return id_paciente
            console.print("[bold red]❌ El ID debe ser un número entero mayor a 0.[/bold red]")
        except ValueError:
            # Aquí capturamos el error si el usuario digita letras en vez de números
            console.print("[bold red]❌ Error de formato: Debe ingresar un número entero válido.[/bold red]")

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