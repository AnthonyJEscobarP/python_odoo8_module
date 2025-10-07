# 🏫 Modulo Administracion Estudiantil - Odoo 8

## Nombre Tecnico: **Python_Odoo8_Module**

Un módulo desarrollado para **Odoo 8** que centraliza y optimiza la administración de procesos educativos, incluyendo la gestión de **estudiantes, profesores, materias, aulas, horarios, exámenes y calificaciones**.  

Este sistema proporciona un entorno **escalable, seguro y adaptable**, con reportes PDF personalizados, vistas dinámicas y control de accesos por roles, garantizando un flujo de información claro y confiable dentro de la institución.  

## 📱MODULO IMPLEMENTADO - ODOO8
 - 🌐 **URL DB:** [**AE_TECH_SCHOOL**](http://64.181.217.115/web)
  - ‼️🔐 **PARA ACCESO A LA BASE DE DATOS DEL SERVIDOR/ODOO WEB, SOLICITAR CREDENCIALES AL DESARROLLADOR**

---

## ⚙️ Sistema de Gestión Académica Completa

### 📌📌Caracteristicas especiales:
- **👥 Estudiantes**:  
  - Registro con informacion necesaria completa para inscripcion, con **carnet único automático** segun secuencia por año y posicion.  
  - Vistas **Tree, Form, Graph** para visualizacion de informacion completa y **busquedas filtradas y agrupadas** eficientes. 
  - Generación de **horario de clases semanal o boleta de calificaciones PDF**.  
   - Acceso diferenciado según rol (Administrador, Profesor, Estudiante). 

- **👨‍🏫 Profesores**:  
  - Administración de docentes con datos personales y academicos.  
  - Control exclusivo de su información, relacionados a su materia asignada, como aula,horarios y estudiantes.  
  - Acceso a resultados,examenes de estudiantes inscritos a su curso.  
   - Acceso diferenciado según rol (Administrador, Profesor, Estudiante). 

- **📚 Materias y Aulas**:  
  - Registro y gestión de **materias** con descripciones de clases.  
  - Control de **aulas** con disponibilidad para asignación de clases segun capacidad y horarios.  
  - Acceso diferenciado según rol (Administrador, Profesor, Estudiante). 

- **📝 Exámenes**:  
  - Creación de exámenes con **preguntas y respuestas multiples**.
  - Puntuacion y asignacion de respuestas correctas,   
  - Control de intentos por materia y estudiantes.
  - Acceso diferenciado según rol (Administrador, Profesor, Estudiante).

- **🎯 Resultados / Calificaciones**:  
  - Registro automatizado de notas por estudiante y materia por examen.  
  - Reportes académicos en PDF con detalle por curso,examenes,resultados y alumno. 
  - Acceso diferenciado según rol (Administrador, Profesor, Estudiante). 

- **🗂️ Horarios**:  
  - Control completo de horarios académicos para administrador y profesor.  
  - Horarios en PDF generados mediante wizard para estudiantes y profesores. 
  - Acceso diferenciado según rol (Administrador, Profesor, Estudiante). 

- **Instalable:** ✅ Sí  
- **Aplicación independiente:** ✅ Sí  

### ✅ Modelos Implementados
Cada modelo cuenta con vistas **Tree, Form y Graph**, además de reportes PDF asociados:  

- `student` → Estudiantes  
- `teacher` → Profesores  
- `classroom` → Aulas  
- `subject` → Materias  
- `schedule` → Horarios  
- `exam` → Exámenes  
- `question` → Preguntas de examen  
- `answer` → Respuestas de examen  
- `result` → Resultados o calificaciones  

### ✅ Wizards - Reportes PDF
- `student_transcript_wizard` → **Boleta de calificaciones** por estudiante, con informacion personal y academica. 
- `student_schedule_wizard` → **Horarios** para estudiantes y profesores segun dia,hora,materia y aula.  

---

## 🔐 Roles y Permisos
El modulo define roles y permisos, garantizando que cada perfil acceda únicamente a la información 
relevante con un acceso seguro y restringido:

### 👨‍💼 Administrador  
- Acceso **total** a todos los modelos y funcionalidades.  
- Puede **crear, editar, eliminar y visualizar** cualquier registro (estudiantes, profesores, materias, aulas, horarios, exámenes, resultados).  

### 👨‍🏫 Profesor  
- **Estudiantes**: puede ver, crear, editar y eliminar registros.  
- **Profesor**: solo puede ver y editar su propio perfil.  
- **Horarios**: acceso total a todos, pero solo puede crear/editar/eliminar los suyos.  
- **Materias**: puede ver todas, pero únicamente modificar las asignadas.  
- **Aulas**: acceso de solo lectura.  
- **Exámenes**: puede crear, editar y eliminar únicamente los de sus materias.  
- **Resultados**: acceso a notas de sus estudiantes.  

### 👨‍🎓 Estudiante  
- **Estudiantes**: acceso exclusivo a su propio registro (sin editar ni eliminar).  
- **Horarios**: solo puede visualizar los propios.  
- **Materias y Aulas**: acceso de solo lectura.  
- **Exámenes**: puede presentar únicamente los exámenes de las materias inscritas.  
- **Resultados**: acceso a sus calificaciones finales (sin detalle de preguntas ni respuestas).  

---

## 💻 Tecnologías Utilizadas
| Componente        | Tecnología   | Versión     |
|-------------------|-------------|-------------|
| **Framework**     | Odoo (OpenERP) | 8.0 |
| **Backend** | Python | 2.7 |
| **Frontend** | XML | - |
| **Base de Datos** | PostgreSQL | 9.6 |
| **Arquitectura**  | MVC Pattern | - |
| **Dependencias**  | base, web | - |
| **Reportes PDF**  | ReportLab | 3.0+ |

---

## 🚀 Instalación y Configuración
### 📋 Requisitos Previos
- Instancia funcional de **Odoo 8**.
- **Python 2.7** (ya incluido con Odoo 8).
- Acceso a la carpeta de **addons** de Odoo.

### 🔧 Instalación
#### **Paso 1: Clonar el Repositorio**
**1.1 Navegar a la carpeta de addons de tu instancia Odoo 8**
```
cd /path/to/odoo/addons
```

**1.2 Clonar repositorio del módulo dentro de la carpeta**
```
git clone https://github.com/AnthonyJEscobarP/python_odoo8_module.git
```

#### **Paso 2: Actualizar la Lista de Módulos**
- En la **interfaz de Odoo**: Configuración > Módulos > Actualizar lista de módulos (Settings > Modules > Update Modules List)

#### **Paso 3: Instalar el Módulo**
- **3.1** - En la **interfaz de Odoo**: Configuración > Módulos > Modulos locales (Settings > Modules > Local Modules)
- **3.2** - **Buscar** módulo: **Modulo Administracion Estudiantil** o nombre tecnico: **python_odoo8_module** 
- **3.3** - **Instalar** y recargar la interfaz de odoo

#### **Paso 4: Configuracion de Roles y Permisos**
- **4.1** - En la **interfaz de Odoo**: 
- **4.2** - **Acceder como administrador** (Contar con acceso a *Technical Features*) y (recomendacion) activar modo desarrollador
- **4.3** - Configuración > Usuarios > *Grupos* (Settings > Users > Groups) y 
Verificar que existan los grupos: *Technical Settings / Administrador, Profesor y Estudiante.*
- **4.4** - En la misma ventana Usuarios > Usuarios (Users > Users): editar usuario actual y asignarle permisos de Administrador.

---

### 🔄 Actualización a Nuevas Versiones
- **Paso 1:** - Desinstalar el módulo desde:  Configuración > Módulos > Modulos locales (Settings > Modules > Local Modules)
- **Paso 2:** - **Ingresar a la carpeta del módulo y ejecutar git pull para actualizar a la última versión**.
 ```
 cd addons/python_odoo8_module/
 ```
- **Paso 3:** - Reinstalar el módulo desde la interfaz.

---

## 🔹 Buenas Prácticas y Consideraciones

### Credenciales Iniciales
- Cada profesor o estudiante creado por el sistema tendrá como usuario su correo y como contraseña inicial: `temporal`.
- Se recomienda que cada usuario cambie su contraseña al primer inicio de sesión.

### Permisos de Administrador
- Para la creación completa de registros y pruebas de todas las funcionalidades, se recomienda asignar permisos de **Administrador** al usuario temporal.

---

## 🗂️ Estructura del Proyecto

```
python_odoo8_module/
├── data/
│   ├── sequence_card.xml            # Secuencia para la creación de carnets
│   └── data_classroom.xml           # Datos demo para aulas
│   └── data_student.xml             # Datos demo para estudiantes
│   └── data_teacher.xml             # Datos demo para profesores
│   └── data_subject.xml             # Datos demo para materias
│   └── data_schedule.xml            # Datos demo para horarios
│   └── data_exam.xml                # Datos demo para exámenes
│   └── data_result.xml              # Datos demo para resultados
├── models/
│   ├── __init__.py                  # Importación de todos los modelos y wizards
│   ├── student.py
│   ├── teacher.py
│   ├── classroom.py
│   ├── subject.py
│   ├── schedule.py
│   ├── exam.py
│   ├── question.py
│   ├── answer.py
│   ├── result.py
│   ├── student_transcript_wizard.py
│   └── student_schedule_wizard.py
├── security/
│   ├── auth.xml                     # Reglas y permisos de visualización por rol
│   ├── ir.model.access.csv          # Permisos y reglas CSV para roles y modelos
│   └── roles.xml                    # Grupos de roles existentes (admin, teacher, student)
├── views/
│   ├── student.xml                   # Vistas Tree, Form, Search y Graph para estudiantes
│   ├── teacher.xml                   # Vistas para profesores
│   ├── classroom.xml                 # Vistas para aulas
│   ├── subject.xml                   # Vistas para materias
│   ├── schedule.xml                  # Vistas para horarios
│   ├── exam.xml                      # Vistas para exámenes
│   ├── result.xml                    # Vistas para resultados
│   └── menu.xml                      # Menús y acciones por rol
├── wizard/
│   ├── student_transcript_wizard.xml # Reporte PDF de boleta de calificaciones
│   └── student_schedule_wizard.xml   # Reporte PDF de horarios
├── __init__.py                       # Importación de models
├── __openerp__.py                    # Información del módulo
├── README.md                          # Documentación del módulo
├── LICENSE                            # Licencia MIT
└── .gitignore                         # Archivos y carpetas ignoradas por Git
```
---

## 💡Autoria
- **Modulo Administracion Estudiantil v1.1.2** bajo **AE-Solutions** 🏷️
- ### 📝 **Licencia**
  - **MIT License**

### 🤖 Programador: 
  - **Anthony Josue Escobar Ponce**
  - 👀 **Portafolio Web:** [**CONOCE MAS SOBRE MI**](https://ae--technologies.web.app/index.html)  
  - 🔎 **LinkedIn:** [**TRABAJA CONMIGO**](https://www.linkedin.com/in/anthony-josu%C3%A9-escobar-ponce-71004437b/) 
  ---
### 💡 **Contacto directo:**
  - 📭 **anthonyescobarponce@Outlook.com** / 📨 [**CLICK AQUI**](https://ae--technologies.web.app/pages/contact.html)
