"""main.py  —  raíz del repositorio
Integrante 4 mariam: integración y menú principal
 
Este archivo NO toca el código de nadie.Solo importa lo que cada compañero ya hizo
y lo conecta en un menú con la libreria rich establecida en los requisitos.

RESPONSABILIDAD DE ESTE ARCHIVO:
  Este archivo es el PUNTO DE ENTRADA del sistema. Su única tarea es mostrar el menú principal y delegar el control a cada módulo cuando el usuario elige una opción.
  NO contiene lógica de negocio (eso lo hacen los módulos).
 
CÓMO FUNCIONA EL FLUJO:
  1. El usuario ejecuta:  python main.py
  2. Se ejecuta menu_principal()
  3. El usuario ve las opciones y elige un número
  4. main.py llama a la función del módulo correspondiente
     (menu_pacientes, menu_medicos o menu_citas)
  5. El control pasa al módulo — main.py "espera"
  6. Cuando el usuario escribe 0 en el submenú, la función del módulo termina y el control regresa aquí
  7. El bucle while repite desde el paso 2
 
PRINCIPIO DE RESPONSABILIDAD ÚNICA aplicado aquí:
  Cada función de este archivo tiene UNA SOLA tarea:
    - mostrar_encabezado()  → solo dibuja el banner
    - mostrar_resumen()     → solo muestra los conteos
    - mostrar_opciones()    → solo imprime las opciones
    - buscar_global()       → solo coordina la búsqueda
    - menu_principal()      → solo orquesta el flujo

"""
# Implementacion de libreria rich

from rich.console import Console 
from rich.panel   import Panel  # → caja con borde para el encabezado
from rich.table   import Table  # → tabla con columnas alineadas

#1 funcion reutilizable para json para leer el archivo y obtener ruta asi:

from sistema_citas.modules.shared.archivos import (
    leer_json, #→ lee un archivo .json y devuelve una lista
    obtener_ruta_data, #→ construye la ruta a la carpeta data/
)
# Estas funciones las hizo el equipo en shared/ para que TODOS los módulos las usen sin repetir código (DRY). 

# =========================================================================
#2 funcion / IMPORTAR EL MENU DE CADA MODULO / 
# - cada integrante exporta Una funcion menu_X() DESDE su modulo
# - El try/except permite que el sistema arranque aunque un módulo aún no esté listo: lo marca como "en desarrollo" en lugar de explotar con un ImportError.

try:
    from sistema_citas.modules.pacientes.pacientes import menu_pacientes
    _PACIENTES_LISTO = True
except ImportError:
    _PACIENTES_LISTO = False   # módulo pendiente de su integrante
 
try:
    from sistema_citas.modules.medicos.medicos import menu_medicos
    _MEDICOS_LISTO = True
except ImportError:
    _MEDICOS_LISTO = False
 
try:
    from sistema_citas.modules.citas.citas import menu_citas
    _CITAS_LISTO = True
except ImportError:
    _CITAS_LISTO = False


    
console = Console()
