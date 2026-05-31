from modules.shared.archivos import (
    leer_json,
    escribir_json,
    obtener_ruta_data,
    asegurar_archivo_json,
)

# Archivo de datos para pacientes
_RUTA_PACIENTES = obtener_ruta_data("pacientes.json")


def cargar_datos() -> dict:
    """Carga y normaliza la estructura de datos de pacientes.

    Retorna un diccionario con la clave 'pacientes' apuntando a una lista.
    """
    asegurar_archivo_json(_RUTA_PACIENTES, default=[])
    datos = leer_json(_RUTA_PACIENTES, default=[])
    if isinstance(datos, list):
        return {"pacientes": datos}
    if isinstance(datos, dict):
        datos.setdefault("pacientes", [])
        return datos
    return {"pacientes": []}


def guardar_datos(datos: dict) -> bool:
    """Escribe la lista de pacientes en el JSON. Espera un dict con 'pacientes'."""
    lista = datos.get("pacientes") if isinstance(datos, dict) else datos
    return escribir_json(_RUTA_PACIENTES, lista)


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
        "nombre": nombre.strip(),
        "edad": edad,
        "telefono": telefono.strip(),
        "email": email.strip()
    }
    datos['pacientes'].append(nuevo)
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