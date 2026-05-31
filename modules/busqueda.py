from modules.storage import cargar_datos
from modules.citas import listar_citas_con_detalle


def buscar_paciente_por_nombre(nombre: str) -> list:
    """
    Busca pacientes cuyo nombre contenga el texto dado (sin importar mayúsculas).
    """
    datos = cargar_datos()
    termino = nombre.lower().strip()
    return [p for p in datos['pacientes'] if termino in p['nombre'].lower()]


def buscar_medico_por_especialidad(especialidad: str) -> list:
    """
    Busca médicos por especialidad (búsqueda parcial, sin importar mayúsculas).
    """
    datos = cargar_datos()
    termino = especialidad.lower().strip()
    return [m for m in datos['medicos'] if termino in m['especialidad'].lower()]


def buscar_citas_por_fecha(fecha: str) -> list:
    """
    Retorna todas las citas de una fecha específica (formato YYYY-MM-DD).
    Incluye nombre de paciente y médico para mostrar en tabla.
    """
    termino = fecha.strip()
    citas = listar_citas_con_detalle()
    return [c for c in citas if c['fecha'] == termino]


def buscar_citas_por_paciente(nombre_paciente: str) -> list:
    """
    Retorna todas las citas cuyo paciente contenga el nombre dado.
    """
    termino = nombre_paciente.lower().strip()
    citas = listar_citas_con_detalle()
    return [c for c in citas if termino in c['nombre_paciente'].lower()]


def buscar_citas_por_medico(nombre_medico: str) -> list:
    """
    Retorna todas las citas asignadas a un médico cuyo nombre contenga el texto dado.
    """
    termino = nombre_medico.lower().strip()
    citas = listar_citas_con_detalle()
    return [c for c in citas if termino in c['nombre_medico'].lower()]


def buscar_citas_por_estado(estado: str) -> list:
    """
    Filtra citas por estado: Pendiente, Confirmada, Cancelada, Completada.
    """
    termino = estado.lower().strip()
    citas = listar_citas_con_detalle()
    return [c for c in citas if c['estado'].lower() == termino]