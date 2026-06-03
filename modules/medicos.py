from modules.storage import cargar_datos, guardar_datos

# Módulo de operaciones CRUD para médicos.
# Todas las funciones utilizan `cargar_datos()` y `guardar_datos()`
# para interactuar con el almacenamiento JSON central.


def _generar_id_medico(medicos: list) -> int:
    # Genera un ID único incremental para un nuevo médico.
    # Si no hay médicos registrados, el primer ID será 1.
    if not medicos:
        return 1
    return max(m['id'] for m in medicos) + 1


def crear_medico(nombre: str, especialidad: str, telefono: str) -> dict:
    # Crea un nuevo registro de médico y lo persiste en el JSON.
    # Parámetros: nombre, especialidad y teléfono (strings).
    # Retorna: diccionario con el médico creado.
    datos = cargar_datos()  # carga la estructura completa desde el storage
    # Construye el diccionario del nuevo médico limpiando espacios en blanco
    nuevo = {
        "id": _generar_id_medico(datos['medicos']),
        "nombre": nombre.strip(),
        "especialidad": especialidad.strip(),
        "telefono": telefono.strip()
    }
    datos['medicos'].append(nuevo)  # agrega al listado en memoria
    guardar_datos(datos)  # persiste los cambios en el archivo JSON
    return nuevo


def listar_medicos() -> list:
    # Devuelve la lista completa de médicos desde el storage.
    datos = cargar_datos()
    return datos['medicos']


def obtener_medico_por_id(id_medico: int) -> dict | None:
    # Busca en la lista el médico cuyo 'id' coincide con `id_medico`.
    # Si lo encuentra retorna el diccionario, si no, retorna None.
    datos = cargar_datos()
    for medico in datos['medicos']:
        if medico['id'] == id_medico:
            return medico
    return None


def actualizar_medico(id_medico: int, nombre: str, especialidad: str, telefono: str) -> bool:
    # Actualiza los campos de un médico existente identificado por ID.
    # Retorna True si se realizó la actualización, False si no se encontró el médico.
    datos = cargar_datos()
    for medico in datos['medicos']:
        if medico['id'] == id_medico:
            medico['nombre'] = nombre.strip()
            medico['especialidad'] = especialidad.strip()
            medico['telefono'] = telefono.strip()
            guardar_datos(datos)  # guarda los cambios realizados
            return True
    return False


def eliminar_medico(id_medico: int) -> bool:
    # Elimina un médico del listado por su ID.
    # Retorna True si se eliminó, False si no existía.
    datos = cargar_datos()
    # Filtra la lista excluyendo el id objetivo
    medicos_filtrados = [m for m in datos['medicos'] if m['id'] != id_medico]
    if len(medicos_filtrados) == len(datos['medicos']):
        # No se eliminó ninguno -> el ID no existía
        return False
    datos['medicos'] = medicos_filtrados
    guardar_datos(datos)  # persiste la lista actualizada
    return True