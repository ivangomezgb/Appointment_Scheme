
# 🏥🩺💊Sistema de Gestión de Citas Médicas 🩺💊🏥
---
> *🩺 Proyecto en **consola** desarrollado en **Python** para gestionar pacientes, médicos y la programación de citas en un consultorio*.  
> *🎨 Interfaz de usuario enriquecida con `rich`, persistencia con CSV y JSON, validaciones estrictas (incluida prevención de doble reserva)`*.
---
###### ADSO - Analisis y Desarrollo de Sotfware 💻 - Aplicaciones de Consola con Python / GRUPO 5 de proyecto
---
## 📚 Índice

0️⃣ **Integrantes**  
1️⃣ Descripción general  
2️⃣ Objetivos y alcance  
3️⃣ Entidades y formatos de datos  
4️⃣ Funcionalidades principales  
5️⃣ Estructura del proyecto  
6️⃣ Requisitos e instalación  
7️⃣ Uso — comandos y ejemplos  
8️⃣ Validaciones y reglas de negocio  
9️⃣ Calidad, pruebas y linters  
🔟 Buenas prácticas de Git
 

---

## 🧑‍💻 Integrantes

| Rol | Modulo Responsable |
|-----|--------|
| dv 1 | modules/storage.py & modules/busqueda.py (validacion y organizacion de datos) |
| dv 2| modules/medicos -  modules/storage.py para formato json |
| dv 3| ui/menus.py - Interfaz de usuario rich (reto -modules/citas.pycitas) |
| dv 4| modules/pacientes - modules/storage.py  |
---
 
#### Desarrolladores:
- 👨‍💻 Developer 1 - Backend y Frontend : **IVAN GOMEZ ESTUPIÑAN**  
- 👨‍💻 Developer 2 - Backend y Frontend : **DAVID OCHOA MACIAS**  
- 👨‍💻 Developer 3 - QA y Test : **MARIAM CARLIER ALVARADO**  
- 👨‍💻 Developer 4 - Backend y Fronted : **JULIAN UNIVIO**

**Ficha:** 3321349  
**Programa de Formación:** Análisis y Desarrollo de Software  
**Centro de Formación:** Centro Minero - SENA sede corpoune Sogamoso  

#### Instructores: 
- 🧑‍🏫 Instructor 1: Andres Felipe Sandoval  
---

## 🩺 1. Descripción general

Este proyecto es un **Sistema de Gestión de Citas Médicas** para consola, que permite:

✅ CRUD completo de **pacientes** y **médicos** .  
✅ **Agendar , actualizar y cancelar citas** con validaciones en cadena.  
✅ **Prevención de conflictos de horario** (un médico no puede tener dos citas a la misma hora).
✅ **Búsquedas inteligentes** (exactas y parciales).
✅ Interfaz visual atractiva con tablas, paneles y colores gracias a rich.

---
## 🎯 2. Objetivos y alcance

### 🎯 Objetivo general
Construir un sistema modular, validado y testeable que cumpla con todos los requisitos funcionales de gestión de citas médicas.

### 🎯 Objetivos específicos
* Persistir datos en archivos JSON (estructura simple, sin dependencias externas).
* Implementar CRUD completo para pacientes, médicos y citas.
* Validar horarios para evitar que un médico tenga citas superpuestas.
* Reutilizar lógica entre módulos (ej: listar_citas_con_detalle() enriquece citas con nombres).
* Mantener altos estándares de calidad: type hints, docstrings, linters (ruff) y pruebas unitarias (pytest).

* Proporcionar una interfaz de usuario profesional con rich. 
 
---

## 🧾 3. Entidades y formatos de datos

### 👨‍⚕️1 Entidad: Médicos — `medicos.py`

| Campo | Tipo | Descripción |
|-------|------|--------------|
| `id_medico` | str/int | Identificador único |
| `nombre` | str | Nombre completo |
| `especialidad` | str | Área médica |

#### Ejemplo:
1.1. RESUMEN CRUD COMPLETO


   | OPERACIÓN  |  FUNCIÓN           |         RETORNA         |
   |------------|------|--------------|
   | CREATE      | crear_medico(...)   | dict (el nuevo médico) |
   | READ (all)  | listar_medicos()  | list (todos los médicos) |
   | READ (one)  | obtener_medico_por_id(id)  | dict o None
   | UPDATE      | actualizar_medico(id, ...)| bool|
   | DELETE      | eliminar_medico(id)        | bool|

```json
{
        "id":           1,
        "nombre":       "Dra. Ana López",
        "especialidad": "Cardiología",
        "telefono":     "3209876543"
    }
```
---

### 🧍2 Entidad : Pacientes — `pacientes.py`

    | Campo | Tipo | Descripción |
    |-------|------|--------------|
    | `id_paciente` | str/int | Identificador único |
    | `nombre` | str | Nombre del paciente |
    | `telefono` | str | Teléfono de contacto |

#### Ejemplo:
2.1. RESUMEN CRUD COMPLETO

| OPERACIÓN  |  FUNCIÓN                    |         RETORNA             |
|------------|-----------------------------|-----------------------------|
| CREATE     |  crear_paciente(...)        |dict (el nuevo paciente)     |
|READ (all)  | listar_pacientes()          |list (todos los pacientes)   |
|READ (one)  | obtener_paciente_por_id(id) | dict o None                 |
|UPDATE      | actualizar_paciente(id, ...)| bool (True=ok, False=no encontró)|
|DELETE      | eliminar_paciente(id)|  bool (True=ok, False=no encontró) |

``` json
    {
        "id":       1,
        "nombre":   "Ana Torres",
        "edad":     20,
        "telefono": "3101234567",
        "email":    "ana@correo.com"
    }
```
---

### 📅 3. Entidad: Citas — `citas.json`

| Clave | Tipo | Ejemplo |
|-------|------|----------|
| `id_cita` | str/int | "1" |
| `id_paciente` | str/int | "10" |
| `id_medico` | str/int | "3" |
| `fecha` | str (YYYY-MM-DD) | "2025-12-01" |
| `hora` | str (HH:MM) | "09:30" |
| `motivo_consulta` | str | "Control general" |

#### Ejemplo:
3.1. RESUMEN DE TODAS LAS FUNCIONES
  | FUNCION RETORNA  |  RECIBE           | 
  |-------|------|
  |   _generar_id_cita(lista)     | lista de citas -int (nuevo ID) |
  |_medico_tiene_conflicto(...)   | id,fecha,hora,excluir  bool|
  |crear_cita(ip,im,f,h,m)        | ids + fecha,hora,mot.  dict o ValueError|
  |listar_citas()                 | nada                   list (con IDs)|
  |obtener_cita_por_id(id)        |  id entero              dict o None|
  |actualizar_cita(id,f,h,m,e)    | id + nuevos datos      bool o ValueError|
  |eliminar_cita(id)              | id entero              bool|
  |listar_citas_con_detalle()     | nada                   list (con nombres)|

  >🔍 Nota: Las citas almacenan solo los IDs de paciente y médico. Los nombres se agregan al mostrar mediante listar_citas_con_detalle(), garantizando consistencia ante cambios futuros en los datos de paciente/médico.


```json
[
  {
        "id":          1,
        "id_paciente": 2,
        "id_medico":   1,
        "fecha":       "2024-07-15",
        "hora":        "10:30",
        "motivo":      "Revisión anual",
        "estado":      "Pendiente"
    }
]
```

---

## ⚙️ 4. Funcionalidades principales

### 🧩 Pacientes
- Crear, listar, editar y eliminar pacientes.

### 🧑‍⚕️ Médicos
- CRUD completo + búsqueda por especialidad.

### 📆 Citas
- Agendar y cancelar citas.  
- Listar citas por médico y fecha.  
- Validar disponibilidad de horario (sin solapamientos).

### 🎨 Interfaz visual en consola
- Tablas, paneles y colores usando `rich`.

---

## 🧱 5. Estructura del proyecto

```plaintext
Appointment_Scheme/ (proyecto)
    │
    ├── main.py                   ← PUNTO DE ENTRADA del programa
    │
    ├── requirements.txt          ← Lista de librerías a instalar
    │
    ├── data/                     ← CAPA DE DATOS (archivos JSON)
    │   ├── pacientes.json
    │   ├── medicos.json
    │   └── citas.json
    │
    ├── modules/                  ← CAPA DE LÓGICA
    │   ├── __init__.py           ← Marca la carpeta como paquete Python
    │   ├── storage.py            ← Acceso a archivos JSON
    │   ├── pacientes.py          ← CRUD de pacientes
    │   ├── medicos.py            ← CRUD de médicos
    │   ├── citas.py              ← CRUD de citas + validaciones
    │   └── busqueda.py           ← Consultas y filtros
    │
    └── ui/                       ← CAPA DE INTERFAZ
        ├── __init__.py
        └── menus.py              ← Menús, tablas y formularios Rich

```

---

## 💻 6. Requisitos e instalación

### 🔧 Requisitos
  >pip install -r requeriments

markdown-it-py==4.2.0 /mdurl==0.1.2 /Pygments==2.20.0 / rich==15.0.0

### 🚀 Instalación rápida
```bash
# Clonar el repositorio
git clone https://github.com/ivangomezgb/Appointment_Scheme.git

# Crear entorno virtual
uv venv .venv

# Activar entorno
# Windows
.\.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

# Instalar dependencias
uv sync

# Ejecutar la aplicación
python main.py
```

---

## 🧠 7. Uso — comandos y ejemplos
Al ejecutar python main.py, se mostrará el menú principal:
```text
 🏥 Sistema de Gestión de Citas Médicas 

[1] Gestión de Pacientes
[2] Gestión de Médicos
[3] Gestión de Citas
[4] Búsqueda y Filtros
[0] Salir

Selecciona una opción:
```

### Ejemplo:  🩺 Agendar una cita
1️⃣ Selecciona “Agendar cita”.  
2️⃣ Ingresa el ID del paciente.  
3️⃣ Ingresa el ID del médico.  
4️⃣ Indica la fecha (YYYY-MM-DD).  
5️⃣ Escribe la hora (HH:MM, formato 24h).  
6️⃣ Añade el motivo de la consulta.  

- 🟢 Si la hora está libre → la cita se guarda con estado "Pendiente". 
- 🔴 Si el médico ya tiene una cita en ese horario: se muestra un mensaje de error y no se guarda.
---

## 🧩 8. Validaciones y reglas de negocio
✔️ Validación de formato de fecha y hora.  
✔️ Confirmación de existencia de IDs válidos.  
✔️ Prevención de doble reserva (mismo médico, misma hora y fecha).  
✔️ Manejo robusto de errores (`try/except`)para capturar ValueError y mostrar mensajes amigables sin crashear..  
✔️ Responsabilidad única por función.  

---

## 🧪 9. Calidad, pruebas y linters

### 🧩 Pruebas unitarias
- CRUD de pacientes y médicos.  
- Agendamiento exitoso.  
- Rechazo por conflicto de horario.  
- Eliminación de cita.

---

## 🌿 10. Buenas prácticas de Git

- Mensajes de commit claros y descriptivos.  
- Flujo con ramas por funcionalidad.
- Funciones privadas (con _) para lógica interna.  
- PRs con descripciones detalladas.  

---

💚 **¡Gracias por leer!**  
Proyecto académico — **Grupo 5**  
Desarrollado con ❤️ y Python 🐍
