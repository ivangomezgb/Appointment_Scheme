from modules.storage import cargar_datos, guardar_datos
from modules.pacientes import obtener_paciente_por_id
from modules.medicos import obtener_medico_por_id


def _generar_id_cita(citas: list) -> int:
    """Genera un ID único para una nueva cita."""
    if not citas:
        return 1
    return max(c['id'] for c in citas) + 1


def crear_cita(id_paciente: int, id_medico: int, fecha: str, hora: str, motivo: str) -> dict:
    """
    Crea una nueva cita médica.
    Valida que el paciente y el médico existan antes de guardar (lógica relacional).
    Retorna la cita creada o lanza ValueError si las referencias no existen.
    """
    # Validación relacional
    if obtener_paciente_por_id(id_paciente) is None:
        raise ValueError(f"No existe un paciente con ID {id_paciente}.")
    if obtener_medico_por_id(id_medico) is None:
        raise ValueError(f"No existe un médico con ID {id_medico}.")

    datos = cargar_datos()
    nueva = {
        "id": _generar_id_cita(datos['citas']),
        "id_paciente": id_paciente,
        "id_medico": id_medico,
        "fecha": fecha.strip(),
        "hora": hora.strip(),
        "motivo": motivo.strip(),
        "estado": "Pendiente"
    }
    datos['citas'].append(nueva)
    guardar_datos(datos)
    return nueva


def listar_citas() -> list:
    """Retorna la lista completa de citas."""
    datos = cargar_datos()
    return datos['citas']


def obtener_cita_por_id(id_cita: int) -> dict | None:
    """Busca y retorna una cita por su ID. Retorna None si no existe."""
    datos = cargar_datos()
    for cita in datos['citas']:
        if cita['id'] == id_cita:
            return cita
    return None


def actualizar_cita(id_cita: int, fecha: str, hora: str, motivo: str, estado: str) -> bool:
    """
    Actualiza los datos de una cita existente.
    Retorna True si se actualizó, False si no se encontró.
    """
    datos = cargar_datos()
    for cita in datos['citas']:
        if cita['id'] == id_cita:
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
    if len(citas_filtradas) == len(datos['citas']):
        return False
    datos['citas'] = citas_filtradas
    guardar_datos(datos)
    return True


def listar_citas_con_detalle() -> list:
    """
    Retorna las citas enriquecidas con el nombre del paciente y del médico.
    Útil para mostrar en tablas sin que el usuario vea solo IDs.
    """
    datos = cargar_datos()
    resultado = []
    for cita in datos['citas']:
        paciente = obtener_paciente_por_id(cita['id_paciente'])
        medico = obtener_medico_por_id(cita['id_medico'])
        resultado.append({
            **cita,
            "nombre_paciente": paciente['nombre'] if paciente else "Eliminado",
            "nombre_medico": medico['nombre'] if medico else "Eliminado",
            "especialidad_medico": medico['especialidad'] if medico else "N/A"
        })
    return resultado