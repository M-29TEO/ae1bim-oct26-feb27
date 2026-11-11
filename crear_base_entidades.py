
# Definimos las entidades (tablas) del problema usando el ORM de SQLAlchemy
# y creando físicamente la base de datos SQLite.
# Modelo:
#   Clinica 1 ──< N Consultorio 1 ──< N Veterinario 1 ──< N HistoriaClinica

from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

# Se importa la cadena de conexión desde configuracion.py
from configuracion import cadena_base_datos

# El engine es el objeto que sabe cómo conectarse a la base de datos.
engine = create_engine(cadena_base_datos)

# Base es la clase de la que heredan todas las entidades.
# SQLAlchemy usa esta herencia para saber qué clases son tablas.
Base = declarative_base()


class Clinica(Base):
    __tablename__ = "clinica"

    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    direccion = Column(String(200), nullable=False)
    veterinario_responsable = Column(String(100), nullable=False)

    # Relación: una clínica tiene muchos consultorios.
    # back_populates enlaza con el atributo clinica de Consultorio.
    consultorios = relationship("Consultorio", back_populates="clinica")

    def __repr__(self):
        return f"Clinica: {self.nombre} | {self.direccion} | Resp.: {self.veterinario_responsable}"


class Consultorio(Base):
    __tablename__ = "consultorio"

    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    especialidad = Column(String(100), nullable=False)

    # Clave foránea obligatoria (nullable=False): todo consultorio
    # pertenece a una sola clínica
    clinica_id = Column(Integer, ForeignKey("clinica.id"), nullable=False)
    clinica = relationship("Clinica", back_populates="consultorios")

    veterinarios = relationship("Veterinario", back_populates="consultorio")

    def __repr__(self):
        return f"Consultorio: {self.nombre} | {self.especialidad}"


class Veterinario(Base):
    __tablename__ = "veterinario"

    id = Column(Integer, primary_key=True)
    nombres = Column(String(100), nullable=False)
    apellidos = Column(String(100), nullable=False)
    correo = Column(String(100), nullable=False, unique=True)
    licencia = Column(String(50), nullable=False, unique=True)

    # Cada veterinario pertenece únicamente a un consultorio
    consultorio_id = Column(Integer, ForeignKey("consultorio.id"), nullable=False)
    consultorio = relationship("Consultorio", back_populates="veterinarios")

    historias = relationship("HistoriaClinica", back_populates="veterinario")

    def __repr__(self):
        return f"Veterinario: {self.nombres} {self.apellidos} | {self.correo} | Lic.: {self.licencia}"


class HistoriaClinica(Base):
    __tablename__ = "historia_clinica"

    id = Column(Integer, primary_key=True)
    fecha_atencion = Column(Date, nullable=False)
    diagnostico = Column(String(200), nullable=False)
    tratamiento = Column(String(300), nullable=False)
    nombre_mascota = Column(String(100), nullable=False)

    # Cada historia clínica está asociada obligatoriamente al veterinario
    # que la elaboró
    veterinario_id = Column(Integer, ForeignKey("veterinario.id"), nullable=False)
    veterinario = relationship("Veterinario", back_populates="historias")

    def __repr__(self):
        return (f"Historia {self.id}: {self.fecha_atencion} | Mascota: {self.nombre_mascota} | "
                f"Dx: {self.diagnostico} | Tx: {self.tratamiento}")


# Este bloque solo se ejecuta si se corre el archivo directamente
# (python crear_base_entidades.py), no cuando otro archivo lo importa
if __name__ == "__main__":
    # create_all genera las sentencias CREATE TABLE de todas las clases
    # que heredan de Base (si las tablas aún no existen)
    Base.metadata.create_all(engine)
    print("Base de datos y tablas creadas correctamente.")
