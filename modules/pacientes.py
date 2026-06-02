from modules.storage import cargar_datos, guardar_datos


def _generar_id_paciente(pacientes: list) -> int:
    """Genera un ID único para un nuevo paciente."""
    if not pacientes:
        return 1
    return max(p['id'] for p in pacientes) + 1


def crear_paciente(nombre: str, edad: int, telefono: str, email: str) -> dict:
    """
    Crea un nuevo paciente y lo guarda en el JSON.
    Retorna el paciente creado.
    """
    datos = cargar_datos()
    nuevo = {
        "id": _generar_id_paciente(datos['pacientes']),
        "nombre": nombre.strip(),# elimina caracteres al principio y al final de string
        "edad": edad,
        "telefono": telefono.strip(),
        "email": email.strip()
    }
    datos['pacientes'].append(nuevo)#agrega un elemento al final de la lista
    guardar_datos(datos)
    return nuevo


def listar_pacientes() -> list:
    """Retorna la lista completa de pacientes."""
    datos = cargar_datos()
    return datos['pacientes']


def obtener_paciente_por_id(id_paciente: int) -> dict | None:
    """Busca y retorna un paciente por su ID. Retorna None si no existe."""
    datos = cargar_datos()
    for paciente in datos['pacientes']:
        if paciente['id'] == id_paciente:
            return paciente
    return None


def actualizar_paciente(id_paciente: int, nombre: str, edad: int, telefono: str, email: str) -> bool:
    """
    Actualiza los datos de un paciente existente.
    Retorna True si se actualizó, False si no se encontró.
    """
    datos = cargar_datos()
    for paciente in datos['pacientes']:
        if paciente['id'] == id_paciente:
            paciente['nombre'] = nombre.strip()
            paciente['edad'] = edad
            paciente['telefono'] = telefono.strip()
            paciente['email'] = email.strip()
            guardar_datos(datos)
            return True
    return False


def eliminar_paciente(id_paciente: int) -> bool:
    """
    Elimina un paciente por ID.
    Retorna True si se eliminó, False si no se encontró.
    """
    datos = cargar_datos()
    pacientes_filtrados = [p for p in datos['pacientes'] if p['id'] != id_paciente]
    if len(pacientes_filtrados) == len(datos['pacientes']):
        return False  # No se encontró el paciente
    datos['pacientes'] = pacientes_filtrados
    guardar_datos(datos)
    return True