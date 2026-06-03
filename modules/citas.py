from modules.storage import cargar_datos, guardar_datos
from modules.pacientes import obtener_paciente_por_id
from modules.medicos import obtener_medico_por_id

# siempre se importaran los modulos relacionados para validar las relaciones entre entidades
#Para verificar que el paciente y el médico existan ANTES de crear la cita (validación relacional)
   # → Para obtener los nombres cuando se muestran las citas

def _generar_id_cita(citas: list) -> int:
    """Genera un ID único para una nueva cita."""
    if not citas:
        return 1
    return max(c['id'] for c in citas) + 1
    #1. Si no hay citas → retorna 1 (primera cita)
        #2. Si hay citas → busca el ID más alto y suma 1

def _existe_conflicto_horario(id_medico: int, fecha: str, hora: str, excluir_id_cita: int = None) -> bool:
    """
    Verifica si ya existe una cita para el mismo médico en la misma fecha y hora.
    Si se pasa excluir_id_cita (ej. al actualizar), se omite esa cita de la comprobación.
    - True si ya existe una cita activa en ese horario, False si está libre.
    """
    datos = cargar_datos()
    for cita in datos['citas']:
        # Al actualizar, ignoramos la propia cita que se está editando
         if excluir_id_cita is not None and cita['id'] == excluir_id_cita:
            continue
        # Comparamos médico + fecha + hora.
        # Las citas Canceladas se consideran libres (el slot queda disponible).
         if (cita['id_medico'] == id_medico
                and cita['fecha'] == fecha.strip()
                and cita['hora'] == hora.strip()
                and cita.get('estado', '') != 'Cancelada'):
            return True          # ← conflicto encontrado
    return False                 # ← horario libre

def crear_cita(id_paciente: int, id_medico: int, fecha: str, hora: str, motivo: str) -> dict:
    """
    Crea una nueva cita médica.
    Valida que el paciente y el médico existan antes de guardar (lógica relacional).
    Retorna la cita creada o lanza ValueError si las referencias no existen.

    - raises ValueError SI alguna falla
    """
    # Validación relacional
    if obtener_paciente_por_id(id_paciente) is None:
        raise ValueError(f"No existe un paciente con ID {id_paciente}.")
    if obtener_medico_por_id(id_medico) is None:
        raise ValueError(f"No existe un médico con ID {id_medico}.")
        #→ Es lanzar un error con un mensaje descriptivo.
        #→ El menú lo captura con try-except y lo muestra en rojo.
        #→ Se usa cuando los datos de entrada son inválidos.

    # Validar conflicto de horario - RETO FINAL
    if _existe_conflicto_horario(id_medico, fecha, hora):
        medico = obtener_medico_por_id(id_medico)
        raise ValueError(
            f"El Dr. {medico['nombre']} ya tiene una cita el {fecha.strip()} "
            f"a las {hora.strip()}. Por favor elige otra hora."
        )

    datos = cargar_datos()
    nueva = { #→ Crear el diccionario de la cita
        "id": _generar_id_cita(datos['citas']),
        "id_paciente": id_paciente,
        "id_medico": id_medico,
        "fecha": fecha.strip(),
        "hora": hora.strip(),
        "motivo": motivo.strip(),
        "estado": "Pendiente"
        #El estado siempre empieza en "Pendiente" por defecto
    }
    datos['citas'].append(nueva)
    guardar_datos(datos)
    return nueva
    #→ Guardar y retornar : Agrega la cita a la lista, guarda en JSON, retorna la cita creada


def listar_citas() -> list:
    """Retorna la lista completa de citas."""
    datos = cargar_datos()
    return datos['citas']


def obtener_cita_por_id(id_cita: int) -> dict | None:
    """Busca y retorna una cita por su ID. Retorna None si no existe.
     → Usada por los formularios de actualizar y eliminar para cargar los datos actuales de la cita antes de modificarla o eliminarla."""
    datos = cargar_datos()
    for cita in datos['citas']:
        if cita['id'] == id_cita:
            return cita
    return None


def actualizar_cita(id_cita: int, fecha: str, hora: str, motivo: str, estado: str) -> bool:
    """
    Actualiza los datos de una cita existente.

    ⏳Si se cambia la fecha O hora, vuelve a validar el conflicto de horario
    del médico asignado (excluyendo la propia cita para no bloquearse).

    Retorna True si se actualizó, False si no se encontró.
    """
    datos = cargar_datos()
    for cita in datos['citas']:
        if cita['id'] == id_cita:

            # Validar conflicto (excluyendo esta misma cita)
 # ── Reto Final: Revalidar conflicto al cambiar fecha/hora ─────────
            if fecha.strip() != cita['fecha'] or hora.strip() != cita['hora']:
                if _existe_conflicto_horario(cita['id_medico'], fecha, hora,
                                           excluir_id_cita=id_cita):
                    medico = obtener_medico_por_id(cita['id_medico'])
                    raise ValueError(
                        f"El Dr. {medico['nombre']} ya tiene una cita el "
                        f"{fecha.strip()} a las {hora.strip()}. "
                        f"Por favor elige otra hora."
                    )
            cita['fecha'] = fecha.strip()
            cita['hora'] = hora.strip()
            cita['motivo'] = motivo.strip()
            cita['estado'] = estado.strip()
            guardar_datos(datos)
            return True
    return False              



def eliminar_cita(id_cita: int) -> bool:
    """
    Elimina una cita por ID.
    Retorna True si se eliminó, False si no se encontró.
    """
    datos = cargar_datos()
    citas_filtradas = [c for c in datos['citas'] if c['id'] != id_cita]
     #→ Crea una NUEVA lista para filtrar con todas las citas EXCEPTO si ya se tiene ese ID
    if len(citas_filtradas) == len(datos['citas']):
        return False
    datos['citas'] = citas_filtradas
    guardar_datos(datos)
    return True
    #→ Si el tamaño no cambió → el ID no existía → retorna False
    #→ Si cambió → se eliminó → guarda y retorna True
    #→ Mismo patrón que en pacientes y médicos



def listar_citas_con_detalle() -> list:
    """
    Retorna las citas enriquecidas con el nombre del paciente y del médico.
    Útil para mostrar en tablas sin que el usuario vea solo IDs.
    El usuario no quiere ver números, quiere ver nombres.

    Esta función resuelve eso: por cada cita, busca el paciente y el médico
    correspondientes y agrega sus nombres al diccionario de la cita.
    """
    datos = cargar_datos()
    resultado = []
    for cita in datos['citas']:
        paciente = obtener_paciente_por_id(cita['id_paciente'])
        #→ Busca el paciente con ese ID en la lista de pacientes       
        medico = obtener_medico_por_id(cita['id_medico'])
                #→ Busca el médico con ese ID en la lista de médicos

        #Crea un diccionario nuevo con:
        resultado.append({
            **cita,#→ copia TODOS los campos de la cita original
            #  (el ** significa "desempaquetar" el diccionario)
            
            "nombre_paciente": paciente['nombre'] if paciente else "Eliminado",
            "nombre_medico": medico['nombre'] if medico else "Eliminado",
            "especialidad_medico": medico['especialidad'] if medico else "N/A"
        })
    return resultado