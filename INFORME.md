# Informe: red de clínicas veterinarias con Python, SQLite y SQLAlchemy

## 1. Objetivo

Modelar e implementar la base de datos de una red de clínicas veterinarias usando:

| Elemento | Herramienta |
|---|---|
| Base de datos | SQLite (un archivo `.db`, no necesita servidor) |
| Lenguaje | Python 3.12 |
| ORM | SQLAlchemy 2.x |
| Control de versiones | Git + GitHub |

Un **ORM** (*Object Relational Mapper*) permite trabajar con las tablas como si fueran clases de Python: cada **clase** es una **tabla**, cada **atributo** una **columna** y cada **objeto** una **fila**. Así no se escribe SQL a mano: SQLAlchemy genera los `CREATE TABLE`, `INSERT` y `SELECT`.

---

## 2. Análisis de la problemática

### 2.1 Entidades y atributos

| Entidad | Atributos |
|---|---|
| **Clinica** | id, nombre, direccion, veterinario_responsable |
| **Consultorio** | id, nombre, especialidad, *clinica_id* |
| **Veterinario** | id, nombres, apellidos, correo, licencia, *consultorio_id* |
| **HistoriaClinica** | id, fecha_atencion, diagnostico, tratamiento, nombre_mascota, *veterinario_id* |

### 2.2 Relaciones

Todas son **uno a muchos (1:N)** y **obligatorias** del lado "muchos":

```
Clinica 1 ──< N Consultorio 1 ──< N Veterinario 1 ──< N HistoriaClinica
```

- "Cada consultorio debe estar asociado obligatoriamente a una sola clínica" → `Consultorio.clinica_id` es clave foránea **NOT NULL**.
- "Cada veterinario debe pertenecer únicamente a un consultorio" → `Veterinario.consultorio_id` es clave foránea **NOT NULL**.
- "Cada historia clínica debe estar asociada obligatoriamente al veterinario que la elaboró" → `HistoriaClinica.veterinario_id` es clave foránea **NOT NULL**.

**Regla práctica:** en una relación 1:N, la clave foránea va siempre en la tabla del lado "N" (el hijo).

> Nota: la historia clínica **no** tiene relación directa con la clínica. Para saber a qué clínica pertenece se sigue el camino historia → veterinario → consultorio → clínica. Esto es importante para la consulta con `all`.

---

## 3. Preparación del entorno local

### Paso 3.1: Instalar Python

Comprobación inicial en la terminal:

```bash
python --version
```

En este equipo respondía *"Python was not found…"*: el comando `python` era solo un acceso directo a la Microsoft Store. Se instaló Python con **winget**, el gestor de paquetes de Windows, solo para el usuario actual (no pide administrador):

```powershell
winget install --id Python.Python.3.12 -e --scope user
```

- `--id Python.Python.3.12`: paquete oficial de python.org.
- `-e`: coincidencia exacta del id.
- `--scope user`: instala en `C:\Users\<usuario>\AppData\Local\Programs\Python\Python312`.

> Si después de instalar `python` sigue sin reconocerse, **cierra y vuelve a abrir la terminal** (o VS Code) para que se recargue el PATH. También puedes desactivar el alias en *Configuración → Aplicaciones → Configuración avanzada → Alias de ejecución de aplicaciones* (apaga `python.exe` y `python3.exe`).

### Paso 3.2: Instalar SQLAlchemy

```bash
python -m pip install sqlalchemy
python -c "import sqlalchemy; print(sqlalchemy.__version__)"   # verificación → 2.1.8
```

SQLite **no** se instala: el módulo `sqlite3` ya viene incluido en Python.

---

## 4. Fork y clonación del repositorio

### Paso 4.1: Ubicar el repositorio

`taw-desarrollo-plataformas-web` es una **organización** de GitHub con muchos repositorios. Se revisó el contenido de cada uno; el que contiene `configuracion.py`, `crear_base_entidades.py`, `poblar_base.py` y los `consulta_*.py` es:

**https://github.com/taw-desarrollo-plataformas-web/ae1bim-oct26-feb27**

Todos sus archivos venían **vacíos**: la plantilla solo fija los nombres de archivo.

### Paso 4.2: Hacer el fork (desde el navegador)

Un **fork** es una copia del repositorio en **tu** cuenta de GitHub, donde sí tienes permiso para subir cambios.

1. Inicia sesión en https://github.com con tu usuario.
2. Abre la URL del repositorio de arriba.
3. Pulsa **Fork** (arriba a la derecha) → deja el nombre `ae1bim-oct26-feb27` → **Create fork**.
4. Quedará en `https://github.com/M-29TEO/ae1bim-oct26-feb27`.

### Paso 4.3: Clonar en el equipo

**Clonar** es descargar el repositorio con todo su historial:

```bash
cd C:\Users\jeyson.astudillo\Documents
git clone https://github.com/taw-desarrollo-plataformas-web/ae1bim-oct26-feb27.git
cd ae1bim-oct26-feb27
```

(Lo habitual es clonar directamente el fork: `git clone https://github.com/M-29TEO/ae1bim-oct26-feb27.git`. Aquí se clonó el original porque el fork aún no existía, y en el paso siguiente se redirige el repositorio hacia el fork.)

### Paso 4.4: Configurar los remotos

Un **remoto** es un alias de una URL de GitHub.

```bash
git remote rename origin upstream          # el original del docente pasa a llamarse "upstream"
git remote add origin https://github.com/M-29TEO/ae1bim-oct26-feb27.git   # tu fork es "origin"
git remote -v                               # verificar
```

- `origin` → tu fork: allí subes (*push*) tu trabajo.
- `upstream` → repositorio del docente: sirve para traer cambios futuros con `git pull upstream main`.

---

## 5. `configuracion.py`: datos de la base

```python
cadena_base_datos = "sqlite:///clinicas_veterinarias.db"
```

**Explicación:**

- Es la **cadena de conexión** que entiende SQLAlchemy: `dialecto:///ruta`.
- `sqlite:///` con **tres** barras indica una ruta relativa: el archivo `clinicas_veterinarias.db` se crea en la carpeta desde donde se ejecuta el script.
- Se guarda en un archivo aparte para que, si mañana se cambia de motor (por ejemplo `mysql+pymysql://usuario:clave@host/bd`), solo se modifique **una línea** y el resto del código siga funcionando.

---

## 6. `crear_base_entidades.py`: definición de las entidades

### Paso 6.1: Engine y Base

```python
from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from configuracion import cadena_base_datos

engine = create_engine(cadena_base_datos)
Base = declarative_base()
```

- `create_engine` crea el objeto que sabe conectarse a la base.
- `declarative_base()` crea la clase `Base`. Toda clase que herede de `Base` será tratada como una tabla.

### Paso 6.2: Definir cada clase

Ejemplo con `Consultorio`, que muestra todos los elementos importantes:

```python
class Consultorio(Base):
    __tablename__ = "consultorio"                         # nombre real de la tabla

    id = Column(Integer, primary_key=True)                # clave primaria autoincremental
    nombre = Column(String(100), nullable=False)          # NOT NULL
    especialidad = Column(String(100), nullable=False)

    clinica_id = Column(Integer, ForeignKey("clinica.id"), nullable=False)  # FK obligatoria
    clinica = relationship("Clinica", back_populates="consultorios")        # navegación al padre

    veterinarios = relationship("Veterinario", back_populates="consultorio") # navegación a los hijos
```

| Elemento | Para qué sirve |
|---|---|
| `__tablename__` | Nombre de la tabla en la base. |
| `Column(Integer, primary_key=True)` | Identificador único; SQLite lo autoincrementa. |
| `nullable=False` | Campo obligatorio (NOT NULL). |
| `ForeignKey("clinica.id")` | Clave foránea hacia la columna `id` de la tabla `clinica`. |
| `relationship(...)` | **No** crea columna; permite navegar en Python: `consultorio.clinica` o `clinica.consultorios`. |
| `back_populates` | Une los dos lados de la relación para que se mantengan sincronizados. |
| `unique=True` | Usado en `correo` y `licencia` del veterinario: no puede haber dos iguales. |
| `__repr__` | Define cómo se imprime el objeto con `print()`. |

Las cuatro clases (`Clinica`, `Consultorio`, `Veterinario`, `HistoriaClinica`) siguen ese mismo patrón; `fecha_atencion` usa el tipo `Date`.

### Paso 6.3: Crear las tablas

```python
if __name__ == "__main__":
    Base.metadata.create_all(engine)
```

- `Base.metadata` contiene la descripción de todas las clases. `create_all` genera y ejecuta los `CREATE TABLE` (solo si las tablas no existen).
- El bloque `if __name__ == "__main__":` hace que las tablas se creen **solo** al ejecutar este archivo directamente. Cuando otros archivos hacen `from crear_base_entidades import ...`, únicamente importan las clases.

**Ejecución:**

```bash
python crear_base_entidades.py
# Base de datos y tablas creadas correctamente.
```

Aparece el archivo `clinicas_veterinarias.db` en la carpeta.

---

## 7. `poblar_base.py`: inserción de datos

### Paso 7.1: Crear la sesión

```python
from sqlalchemy.orm import sessionmaker
from crear_base_entidades import engine, Clinica, Consultorio, Veterinario, HistoriaClinica

Session = sessionmaker(bind=engine)
session = Session()
```

La **sesión** es la "conversación" con la base: guarda los cambios pendientes y los envía todos juntos en una transacción al hacer `commit()`.

### Paso 7.2: Evitar duplicados

```python
if session.query(Clinica).count() > 0:
    print("La base ya tiene datos...")
    raise SystemExit
```

Si el script se ejecuta dos veces, no inserta los datos de nuevo.

### Paso 7.3: Crear objetos enlazados por sus relaciones

```python
c1  = Clinica(nombre="VetSalud Loja", direccion="...", veterinario_responsable="Dra. Paola Jaramillo")
co1 = Consultorio(nombre="Consultorio 101", especialidad="Medicina general", clinica=c1)
v1  = Veterinario(nombres="Luis", apellidos="Torres Cueva", correo="...", licencia="LIC-1001", consultorio=co1)
HistoriaClinica(fecha_atencion=date(2026, 9, 2), diagnostico="Gastroenteritis", ..., veterinario=v1)
```

No se escriben los `id` a mano: al poner `clinica=c1`, SQLAlchemy completa `clinica_id` automáticamente después de insertar la clínica.

### Paso 7.4: Guardar

```python
session.add_all([c1, c2, c3])
session.add_all(historias)
session.commit()
```

Por la *cascada* por defecto (`save-update`) de `relationship`, al agregar clínicas e historias también se guardan los consultorios y veterinarios enlazados.

**Datos cargados:** 3 clínicas, 6 consultorios, 7 veterinarios y 11 historias clínicas.

```bash
python poblar_base.py
# Datos insertados correctamente.
```

> Para empezar de cero: borra `clinicas_veterinarias.db` y vuelve a ejecutar `crear_base_entidades.py` y `poblar_base.py`.

---

## 8. Consultas

Todas siguen la misma estructura: crear sesión → `session.query(Clase)` → encadenar métodos → `.all()` → recorrer resultados.

### 8.1 `consulta_all.py`: `all()`. Clínicas y su número de historias clínicas

```python
clinicas = session.query(Clinica).all()
for clinica in clinicas:
    total_historias = 0
    for consultorio in clinica.consultorios:
        for veterinario in consultorio.veterinarios:
            total_historias += len(veterinario.historias)
    print(clinica)
    print(f"   Número de historias clínicas: {total_historias}")
```

- `all()` ejecuta el `SELECT` y devuelve una **lista** con todos los registros.
- Como la historia no se relaciona directamente con la clínica, se recorre el camino de relaciones clínica → consultorios → veterinarios → historias y se van sumando.

**Resultado:**

```
Clinica: VetSalud Loja | Av. Universitaria y 10 de Agosto, Loja | Resp.: Dra. Paola Jaramillo
   Número de historias clínicas: 5
Clinica: Huellitas Quito | Av. Amazonas N24-56, Quito | Resp.: Dr. Andrés Villacís
   Número de historias clínicas: 4
Clinica: PetCare Cuenca | Calle Larga 8-45, Cuenca | Resp.: Dra. María Ordóñez
   Número de historias clínicas: 2
```

Comprobación: 5 + 4 + 2 = 11, que coincide con las historias insertadas.

### 8.2 `consulta_filter.py`: `filter()`. Veterinarios de consultorios de Cirugía

```python
veterinarios = (session.query(Veterinario)
                .join(Veterinario.consultorio)
                .filter(Consultorio.especialidad == "Cirugía")
                .all())
```

- `filter()` equivale a `WHERE` en SQL.
- `join(Veterinario.consultorio)` une `veterinario` con `consultorio` usando la clave foránea, para poder filtrar por un campo del consultorio.

**Resultado:** Ana Paredes Ruiz (VetSalud Loja) y Diego Vintimilla Paz (PetCare Cuenca).

### 8.3 `consulta_order_by.py`: `order_by()`. Historias por fecha, de la más reciente a la más antigua

```python
historias = (session.query(HistoriaClinica)
             .order_by(HistoriaClinica.fecha_atencion.desc())
             .all())
```

- `order_by()` equivale a `ORDER BY`. Sin `.desc()` el orden es ascendente.

**Resultado:** las 11 historias, de 2026-11-02 (Lola) a 2026-09-02 (Max).

### 8.4 `consulta_or.py`: `or_()`. Diagnóstico de Otitis **o** Gastroenteritis

```python
from sqlalchemy import or_
historias = (session.query(HistoriaClinica)
             .filter(or_(HistoriaClinica.diagnostico.like("%Otitis%"),
                         HistoriaClinica.diagnostico.like("%Gastroenteritis%")))
             .all())
```

- `or_(a, b)` devuelve los registros que cumplen **al menos una** condición.
- `like("%texto%")` busca el texto en cualquier parte de la cadena (`%` = cualquier cantidad de caracteres).

**Resultado:** 4 historias (Max, Luna, Bruno, Lola).

### 8.5 `consulta_and.py`: `and_()`. Historias desde el 1 de octubre de 2026 **y** de la clínica Huellitas Quito

```python
from sqlalchemy import and_
historias = (session.query(HistoriaClinica)
             .join(HistoriaClinica.veterinario)
             .join(Veterinario.consultorio)
             .join(Consultorio.clinica)
             .filter(and_(HistoriaClinica.fecha_atencion >= date(2026, 10, 1),
                          Clinica.nombre == "Huellitas Quito"))
             .all())
```

- `and_(a, b)` exige que se cumplan **ambas** condiciones.
- Se encadenan tres `join` para llegar desde la historia hasta la clínica.

**Resultado:** 3 historias (Coco, Bruno, Lola).

---

## 9. Orden de ejecución

Desde la carpeta del proyecto:

```bash
python crear_base_entidades.py   # 1. crea la base y las tablas
python poblar_base.py            # 2. inserta los datos
python consulta_all.py           # 3. consultas (en cualquier orden)
python consulta_filter.py
python consulta_order_by.py
python consulta_or.py
python consulta_and.py
```

> Si la consola de Windows muestra mal las tildes, ejecuta antes `chcp 65001`.

---

## 10. Subir el trabajo a GitHub

### Paso 10.1: Identidad de Git (una sola vez por repositorio)

```bash
git config user.name "M-29TEO"
git config user.email "tu_correo@ejemplo.com"
```

### Paso 10.2: `.gitignore`

Se creó un `.gitignore` con:

```
__pycache__/
*.db
```

para no subir archivos generados automáticamente. La base `.db` se puede regenerar con los scripts. Si tu docente pide subir la base, elimina la línea `*.db`.

### Paso 10.3: Commit

```bash
git add .
git commit -m "Modelo de clínicas veterinarias con SQLAlchemy, poblado y consultas"
```

- `git add .` prepara todos los archivos modificados.
- `git commit` guarda una "foto" del proyecto en el historial local.

### Paso 10.4: Push al fork

```bash
git push -u origin main
```

La primera vez, Windows (Git Credential Manager) abre una ventana para **iniciar sesión en GitHub desde el navegador**. GitHub ya **no acepta la contraseña** de la cuenta en la terminal; si no aparece la ventana, crea un *Personal Access Token* en *GitHub → Settings → Developer settings → Personal access tokens* y úsalo en lugar de la contraseña.

Al final, los archivos se verán en `https://github.com/M-29TEO/ae1bim-oct26-feb27`.

---

## 11. Estructura final

```
ae1bim-oct26-feb27/
├── .gitignore
├── INFORME.md                 ← este informe
├── README.md
├── configuracion.py           ← cadena de conexión
├── crear_base_entidades.py    ← clases/tablas + create_all
├── poblar_base.py             ← inserción de datos
├── consulta_all.py            ← all(): clínicas y número de historias
├── consulta_filter.py         ← filter()
├── consulta_order_by.py       ← order_by()
├── consulta_or.py             ← or_()
└── consulta_and.py            ← and_()
```
