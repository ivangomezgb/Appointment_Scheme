"""
Sistema de Gestión de Citas Médicas
Punto de entrada principal del sistema
"""

from rich.console import Console
from rich.prompt import Prompt

console = Console()


def menu_principal():
    """Menú principal del sistema."""
    
    while True:
        console.print("\n[bold green]╔════════════════════════════════════════╗[/bold green]")
        console.print("[bold green]║  SISTEMA DE GESTIÓN DE CITAS MÉDICAS  ║[/bold green]")
        console.print("[bold green]╚════════════════════════════════════════╝[/bold green]\n")
        
        console.print("[cyan]1.[/cyan] Gestión de Pacientes")
        console.print("[cyan]2.[/cyan] Gestión de Médicos")
        console.print("[cyan]3.[/cyan] Gestión de Citas")
        console.print("[cyan]0.[/cyan] Salir")
        
        try:
            opcion = Prompt.ask("\n[green]Seleccione una opción[/green]", choices=["0", "1", "2", "3"])
            
            if opcion == "1":
                console.print("\n[yellow]Módulo de Pacientes en desarrollo...[/yellow]")
                Prompt.ask("\n[dim]Presione Enter para continuar[/dim]", default="")
            elif opcion == "2":
                console.print("\n[yellow]Módulo de Médicos en desarrollo...[/yellow]")
                Prompt.ask("\n[dim]Presione Enter para continuar[/dim]", default="")
            elif opcion == "3":
                console.print("\n[yellow]Módulo de Citas en desarrollo...[/yellow]")
                Prompt.ask("\n[dim]Presione Enter para continuar[/dim]", default="")
            elif opcion == "0":
                console.print("\n[green]¡Hasta luego![/green]\n")
                break
        
        except KeyboardInterrupt:
            console.print("\n\n[yellow]Saliendo del sistema...[/yellow]\n")
            break
        except Exception as e:
            console.print(f"\n[red]✗ Error: {e}[/red]")


if __name__ == "__main__":
    menu_principal()
