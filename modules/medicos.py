from modules.storage import cargar_datos, guardar_datos


def _generar_id_medico(medicos: list) -> int:
    """Genera un ID único para un nuevo médico."""
    if not medicos:
        return 1
    return max(m['id'] for m in medicos) + 1


def crear_medico(nombre: str, especialidad: str, telefono: str) -> dict:
    """
    Crea un nuevo médico y lo guarda en el JSON.
    Retorna el médico creado.
    """
    datos = cargar_datos()
    nuevo = {
        "id": _generar_id_medico(datos['medicos']),
        "nombre": nombre.strip(),
        "especialidad": especialidad.strip(),
        "telefono": telefono.strip()
    }
    datos['medicos'].append(nuevo)
    guardar_datos(datos)
    return nuevo


def listar_medicos() -> list:
    """Retorna la lista completa de médicos."""
    datos = cargar_datos()
    return datos['medicos']


def obtener_medico_por_id(id_medico: int) -> dict | None:
    """Busca y retorna un médico por su ID. Retorna None si no existe."""
    datos = cargar_datos()
    for medico in datos['medicos']:
        if medico['id'] == id_medico:
            return medico
    return None


def actualizar_medico(id_medico: int, nombre: str, especialidad: str, telefono: str) -> bool:
    """
    Actualiza los datos de un médico existente.
    Retorna True si se actualizó, False si no se encontró.
    """
    datos = cargar_datos()
    for medico in datos['medicos']:
        if medico['id'] == id_medico:
            medico['nombre'] = nombre.strip()
            medico['especialidad'] = especialidad.strip()
            medico['telefono'] = telefono.strip()
            guardar_datos(datos)
            return True
    return False


def eliminar_medico(id_medico: int) -> bool:
    """
    Elimina un médico por ID.
    Retorna True si se eliminó, False si no se encontró.
    """
    datos = cargar_datos()
    medicos_filtrados = [m for m in datos['medicos'] if m['id'] != id_medico]
    if len(medicos_filtrados) == len(datos['medicos']):
        return False
    datos['medicos'] = medicos_filtrados
    guardar_datos(datos)
    return True