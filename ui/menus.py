import time  # 1. Importamos la librería encargada del tiempo
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt
from rich import box
from rich.text import Text
from rich.align import Align

from rich.progress import track

from modules import pacientes, medicos, citas, busqueda

console = Console()

ESTADOS_VALIDOS = ["Pendiente", "Confirmada", "Cancelada", "Completada"]



#UTILIDADES

def mostrar_exito(mensaje: str) -> None:
    console.print(f"\n[bold green]✔ {mensaje}[/bold green]\n")


def mostrar_error(mensaje: str) -> None:
    console.print(f"\n[bold red]✘ {mensaje}[/bold red]\n")


def mostrar_info(mensaje: str) -> None:
    console.print(f"\n[bold yellow]ℹ {mensaje}[/bold yellow]\n")


def pausar() -> None:
    console.input("\n[dim]Presiona Enter para continuar...[/dim]")


# TABLAS

def tabla_pacientes(lista: list) -> None:

    # 2. Envolvemos nuestro rango con track() de rich
    for paso in track(range(100), description="Cargando pacientes..."):
                
        # 3. Pausamos el código 0.01 segundos en cada iteración para simular trabajo
        time.sleep(0.01) 
    console.print(" [bold green]\n¡Carga completada con éxito!  [/bold green]", justify="center")
   
    if not lista:
        mostrar_info("No hay pacientes registrados.")
        return
    tabla = Table(title="\nPacientes Registrados", box=box.ROUNDED, highlight=True)
    tabla.add_column("ID", style="cyan", justify="center")
    tabla.add_column("Nombre", style="white")
    tabla.add_column("Edad", justify="center")
    tabla.add_column("Teléfono", style="green")#table.add_column : agrega columnas,color,alineacion,
    tabla.add_column("Email", style="blue")
    for p in lista:
        tabla.add_row(str(p['id']), p['nombre'], str(p['edad']), p['telefono'], p['email']) #tabla.add_row:crea linea horizontal reglas: 3columnas 3 datos
    console.print(tabla , justify="center")



def tabla_medicos(lista: list) -> None:
    for paso in track(range(100), description="Cargando médicos disponibles..."):
       #  Pausamos el código 0.01 segundos en cada iteración para simular trabajo
        time.sleep(0.01) 
    console.print(" [bold green]\n¡Carga completada con éxito!  [/bold green]", justify="center")
    
    if not lista:
        mostrar_info("No hay médicos registrados.")
        return
    tabla = Table(title="Médicos Registrados", box=box.ROUNDED, highlight=True)
    tabla.add_column("ID", style="cyan", justify="center")
    tabla.add_column("Nombre", style="white")
    tabla.add_column("Especialidad", style="magenta")
    tabla.add_column("Teléfono", style="green")
    for m in lista:
        tabla.add_row(str(m['id']), m['nombre'], m['especialidad'], m['telefono'])
    console.print(tabla , justify="center")


def tabla_citas(lista: list) -> None:
    
    if not lista:
        mostrar_info("No hay citas registradas.")
        return
    tabla = Table(title="Citas Médicas", box=box.ROUNDED, highlight=True)
    tabla.add_column("ID", style="cyan", justify="center")
    tabla.add_column("Paciente", style="white")
    tabla.add_column("Médico", style="white")
    tabla.add_column("Especialidad", style="magenta")
    tabla.add_column("Fecha", style="yellow")
    tabla.add_column("Hora", style="yellow")
    tabla.add_column("Motivo")
    tabla.add_column("Estado", style="bold")
    for c in lista:
        estado_color = {
            "Pendiente": "yellow",
            "Confirmada": "green",
            "Cancelada": "red",
            "Completada": "blue"
        }.get(c.get('estado', ''), 'white')
        tabla.add_row(
            str(c['id']),
            c.get('nombre_paciente', str(c['id_paciente'])), #.get: Busca una clave: si está, te da su valor; si no, te da None sin romper el código.
            c.get('nombre_medico', str(c['id_medico'])),
            c.get('especialidad_medico', 'N/A'),
            c['fecha'],
            c['hora'],
            c['motivo'],
            f"[{estado_color}]{c['estado']}[/{estado_color}]"
        )
    console.print(tabla , justify="center")


# MENÚ PRINCIPAL

def menu_principal() -> None:
    while True:
        console.clear()
        console.print(Panel(
            Text("🏥  Sistema de Gestión de Citas Médicas", justify="center", style="bold white"),
            style="bold blue",
            padding=(1, 4), 
        ))
        console.print("[1] Gestión de Pacientes")
        console.print("[2] Gestión de Médicos")
        console.print("[3] Gestión de Citas")
        console.print("[4] Búsqueda y Filtros")
        console.print("[0] Salir\n")

        opcion = Prompt.ask("Selecciona una opción", choices=["0", "1", "2", "3", "4"])

        if opcion == "1":
            menu_pacientes()
        elif opcion == "2":
            menu_medicos()
        elif opcion == "3":
            menu_citas()
        elif opcion == "4":
            menu_busqueda()
        elif opcion == "0":
            console.print(Panel("[bold green]¡Hasta luego![/bold green]", style="green"))
            break


# MENÚ PACIENTES

def menu_pacientes() -> None:
    while True:
        console.clear()
        console.print(Panel("[bold cyan]👤 Gestión de Pacientes[/bold cyan]", style="cyan" ))
        console.print("[1] Listar pacientes")
        console.print("[2] Crear paciente")
        console.print("[3] Actualizar paciente")
        console.print("[4] Eliminar paciente")
        console.print("[0] Volver\n")

        opcion = Prompt.ask("Selecciona una opción", choices=["0", "1", "2", "3", "4"])

        if opcion == "1":
            tabla_pacientes(pacientes.listar_pacientes())            
            pausar()

        elif opcion == "2":
            _form_crear_paciente()
        elif opcion == "3":
            _form_actualizar_paciente()
        elif opcion == "4":
            _form_eliminar_paciente()
        elif opcion == "0":
            break


def _form_crear_paciente() -> None:
    console.print(Panel("[bold]Nuevo Paciente[/bold]", style="cyan"))
    try:
        nombre = Prompt.ask("Nombre completo")
        if not nombre.strip():
            mostrar_error("El nombre no puede estar vacío.")
            pausar()
            return
        edad = IntPrompt.ask("Edad")
        if edad <= 0 or edad > 120:
            mostrar_error("Edad inválida.")
            pausar()
            return
        telefono = Prompt.ask("Teléfono")
        email = Prompt.ask("Email")
        nuevo = pacientes.crear_paciente(nombre, edad, telefono, email)
        mostrar_exito(f"Paciente '{nuevo['nombre']}' creado con ID {nuevo['id']}.")
    except Exception as e: #Evita que el programa se rompa si el usuario ingresa texto en lugar de un número (guarda el error en e)
        mostrar_error(f"Error al crear paciente: {e}")
    pausar()


def _form_actualizar_paciente() -> None:
    tabla_pacientes(pacientes.listar_pacientes())
    try:
        id_p = IntPrompt.ask("ID del paciente a actualizar")
        paciente = pacientes.obtener_paciente_por_id(id_p)
        if not paciente:  # Sirve para verificar si algo está vacío (o no existe) y mostrar un error.
            mostrar_error(f"No existe paciente con ID {id_p}.")
            pausar()
            return
        console.print(f"[dim]Editando: {paciente['nombre']} | Deja en blanco para mantener el valor actual[/dim]")
        nombre = Prompt.ask("Nuevo nombre", default=paciente['nombre'])
        edad_str = Prompt.ask("Nueva edad", default=str(paciente['edad']))
        telefono = Prompt.ask("Nuevo teléfono", default=paciente['telefono'])
        email = Prompt.ask("Nuevo email", default=paciente['email']) # Sirve para pedir un texto al usuario con colores y estilos atractivos en la terminal.

        edad = int(edad_str)
        if edad <= 0 or edad > 120:
            mostrar_error("Edad inválida.")
            pausar()
            return

        pacientes.actualizar_paciente(id_p, nombre, edad, telefono, email)
        mostrar_exito("Paciente actualizado correctamente.")
    except ValueError:
        mostrar_error("La edad debe ser un número entero.")
    except Exception as e:
        mostrar_error(f"Error: {e}")
    pausar()


def _form_eliminar_paciente() -> None:
    tabla_pacientes(pacientes.listar_pacientes())
    try:
        id_p = IntPrompt.ask("ID del paciente a eliminar")
        paciente = pacientes.obtener_paciente_por_id(id_p)
        if not paciente:
            mostrar_error(f"No existe paciente con ID {id_p}.")
            pausar()
            return
        confirmar = Prompt.ask(
            f"¿Eliminar a '{paciente['nombre']}'? Esta acción no se puede deshacer",
            choices=["s", "n"]
        )
        if confirmar == "s":
            pacientes.eliminar_paciente(id_p)
            mostrar_exito("Paciente eliminado.")
        else:
            mostrar_info("Operación cancelada.")
    except Exception as e:
        mostrar_error(f"Error: {e}")
    pausar()


# MENÚ MÉDICOS

def menu_medicos() -> None:
    while True:
        console.clear()
        console.print(Panel("[bold magenta]🩺 Gestión de Médicos[/bold magenta]", style="magenta"))
        console.print("[1] Listar médicos")
        console.print("[2] Crear médico")
        console.print("[3] Actualizar médico")
        console.print("[4] Eliminar médico")
        console.print("[0] Volver\n")

        opcion = Prompt.ask("Selecciona una opción", choices=["0", "1", "2", "3", "4"])

        if opcion == "1":
            tabla_medicos(medicos.listar_medicos())
            pausar()
        elif opcion == "2":
            _form_crear_medico()
        elif opcion == "3":
            _form_actualizar_medico()
        elif opcion == "4":
            _form_eliminar_medico()
        elif opcion == "0":
            break


def _form_crear_medico() -> None:
    console.print(Panel("[bold]Nuevo Médico[/bold]", style="magenta"))
    try:
        nombre = Prompt.ask("Nombre completo")
        if not nombre.strip():
            mostrar_error("El nombre no puede estar vacío.")
            pausar()
            return
        especialidad = Prompt.ask("Especialidad")
        telefono = Prompt.ask("Teléfono")
        nuevo = medicos.crear_medico(nombre, especialidad, telefono)
        mostrar_exito(f"Médico '{nuevo['nombre']}' creado con ID {nuevo['id']}.")
    except Exception as e:
        mostrar_error(f"Error al crear médico: {e}")
    pausar()


def _form_actualizar_medico() -> None:
    tabla_medicos(medicos.listar_medicos())
    try:
        id_m = IntPrompt.ask("ID del médico a actualizar")
        medico = medicos.obtener_medico_por_id(id_m)
        if not medico:
            mostrar_error(f"No existe médico con ID {id_m}.")
            pausar()
            return
        nombre = Prompt.ask("Nuevo nombre", default=medico['nombre'])
        especialidad = Prompt.ask("Nueva especialidad", default=medico['especialidad'])
        telefono = Prompt.ask("Nuevo teléfono", default=medico['telefono'])
        medicos.actualizar_medico(id_m, nombre, especialidad, telefono)
        mostrar_exito("Médico actualizado correctamente.")
    except Exception as e:
        mostrar_error(f"Error: {e}")
    pausar()


def _form_eliminar_medico() -> None:
    tabla_medicos(medicos.listar_medicos())
    try:
        id_m = IntPrompt.ask("ID del médico a eliminar")
        medico = medicos.obtener_medico_por_id(id_m)
        if not medico:
            mostrar_error(f"No existe médico con ID {id_m}.")
            pausar()
            return
        confirmar = Prompt.ask(
            f"¿Eliminar al Dr. '{medico['nombre']}'? Esta acción no se puede deshacer",
            choices=["s", "n"]
        )
        if confirmar == "s":
            medicos.eliminar_medico(id_m)
            mostrar_exito("Médico eliminado.")
        else:
            mostrar_info("Operación cancelada.")
    except Exception as e:
        mostrar_error(f"Error: {e}")
    pausar()


# MENÚ CITAS

def menu_citas() -> None:
    while True:
        console.clear()
        console.print(Panel("[bold yellow]📅 Gestión de Citas[/bold yellow]", style="yellow"))
        console.print("[1] Listar citas")
        console.print("[2] Crear cita")
        console.print("[3] Actualizar cita")
        console.print("[4] Eliminar cita")
        console.print("[0] Volver\n")

        opcion = Prompt.ask("Selecciona una opción", choices=["0", "1", "2", "3", "4"])

        if opcion == "1":
            tabla_citas(citas.listar_citas_con_detalle())
            pausar()
        elif opcion == "2":
            _form_crear_cita()
        elif opcion == "3":
            _form_actualizar_cita()
        elif opcion == "4":
            _form_eliminar_cita()
        elif opcion == "0":
            break


def _form_crear_cita() -> None:
    console.print(Panel("[bold]Nueva Cita[/bold]", style="yellow"))
    # Mostrar pacientes y médicos disponibles para facilitar la selección
    tabla_pacientes(pacientes.listar_pacientes())
    tabla_medicos(medicos.listar_medicos())
    try:
        id_p = IntPrompt.ask("ID del paciente")
        id_m = IntPrompt.ask("ID del médico")
        fecha = Prompt.ask("Fecha (YYYY-MM-DD)")
        hora = Prompt.ask("Hora (HH:MM)")
        motivo = Prompt.ask("Motivo de la consulta")
        nueva = citas.crear_cita(id_p, id_m, fecha, hora, motivo)
        mostrar_exito(f"Cita #{nueva['id']} creada para el {nueva['fecha']} a las {nueva['hora']}.")
    except ValueError as e:
        mostrar_error(str(e))
    except Exception as e:
        mostrar_error(f"Error al crear cita: {e}")
    pausar()


def _form_actualizar_cita() -> None:
    tabla_citas(citas.listar_citas_con_detalle())
    try:
        id_c = IntPrompt.ask("ID de la cita a actualizar")
        cita = citas.obtener_cita_por_id(id_c)
        if not cita:
            mostrar_error(f"No existe cita con ID {id_c}.")
            pausar()
            return
        fecha = Prompt.ask("Nueva fecha (YYYY-MM-DD)", default=cita['fecha'])
        hora = Prompt.ask("Nueva hora (HH:MM)", default=cita['hora'])
        motivo = Prompt.ask("Nuevo motivo", default=cita['motivo'])
        console.print(f"Estados válidos: {', '.join(ESTADOS_VALIDOS)}")
        estado = Prompt.ask("Nuevo estado", default=cita['estado'], choices=ESTADOS_VALIDOS)
        citas.actualizar_cita(id_c, fecha, hora, motivo, estado)
        mostrar_exito("Cita actualizada correctamente.")
    except Exception as e:
        mostrar_error(f"Error: {e}")
    pausar()


def _form_eliminar_cita() -> None:
    tabla_citas(citas.listar_citas_con_detalle())
    try:
        id_c = IntPrompt.ask("ID de la cita a eliminar")
        cita = citas.obtener_cita_por_id(id_c)
        if not cita:
            mostrar_error(f"No existe cita con ID {id_c}.")
            pausar()
            return
        confirmar = Prompt.ask(
            f"¿Eliminar la cita #{id_c}? Esta acción no se puede deshacer",
            choices=["s", "n"]
        )
        if confirmar == "s":
            citas.eliminar_cita(id_c)
            mostrar_exito("Cita eliminada.")
        else:
            mostrar_info("Operación cancelada.")
    except Exception as e:
        mostrar_error(f"Error: {e}")
    pausar()


# MENÚ BÚSQUEDA

def menu_busqueda() -> None:
    while True:
        console.clear()
        console.print(Panel("[bold green]🔍 Búsqueda y Filtros[/bold green]", style="green"))
        console.print("[1] Buscar paciente por nombre")
        console.print("[2] Buscar médico por especialidad")
        console.print("[3] Buscar citas por fecha")
        console.print("[4] Buscar citas por paciente")
        console.print("[5] Buscar citas por médico")
        console.print("[6] Filtrar citas por estado")
        console.print("[0] Volver\n")

        opcion = Prompt.ask("Selecciona una opción", choices=["0", "1", "2", "3", "4", "5", "6"])

        if opcion == "1":
            termino = Prompt.ask("Nombre del paciente")
            tabla_pacientes(busqueda.buscar_paciente_por_nombre(termino))
            pausar()
        elif opcion == "2":
            termino = Prompt.ask("Especialidad")
            tabla_medicos(busqueda.buscar_medico_por_especialidad(termino))
            pausar()
        elif opcion == "3":
            fecha = Prompt.ask("Fecha (YYYY-MM-DD)")
            tabla_citas(busqueda.buscar_citas_por_fecha(fecha))
            pausar()
        elif opcion == "4":
            termino = Prompt.ask("Nombre del paciente")
            tabla_citas(busqueda.buscar_citas_por_paciente(termino))
            pausar()
        elif opcion == "5":
            termino = Prompt.ask("Nombre del médico")
            tabla_citas(busqueda.buscar_citas_por_medico(termino))
            pausar()
        elif opcion == "6":
            console.print(f"Estados disponibles: {', '.join(ESTADOS_VALIDOS)}")
            estado = Prompt.ask("Estado", choices=ESTADOS_VALIDOS)
            tabla_citas(busqueda.buscar_citas_por_estado(estado))
            pausar()
        elif opcion == "0":
            break
