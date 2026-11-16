# En este archivo se crean las tablas de la base de datos.
# Las tablas son: Clinica, Consultorio, Veterinario y HistoriaClinica.
# Una clinica tiene varios consultorios, un consultorio tiene varios
# veterinarios y un veterinario tiene varias historias clinicas.

from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

# Traemos el nombre de la base desde configuracion.py
from configuracion import cadena_base_datos

# engine sirve para conectarse a la base de datos
engine = create_engine(cadena_base_datos)

# Todas las clases que hereden de Base se convierten en tablas
Base = declarative_base()


class Clinica(Base):
    __tablename__ = "clinica"

    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    direccion = Column(String(200), nullable=False)
    veterinario_responsable = Column(String(100), nullable=False)

    # Una clinica tiene muchos consultorios
    consultorios = relationship("Consultorio", back_populates="clinica")

    def __repr__(self):
        return f"Clinica: {self.nombre} | {self.direccion} | Resp.: {self.veterinario_responsable}"


class Consultorio(Base):
    __tablename__ = "consultorio"

    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    especialidad = Column(String(100), nullable=False)

    # Cada consultorio tiene que estar en una clinica
    clinica_id = Column(Integer, ForeignKey("clinica.id"), nullable=False)
    clinica = relationship("Clinica", back_populates="consultorios")

    # Un consultorio tiene muchos veterinarios
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

    # Cada veterinario trabaja en un solo consultorio
    consultorio_id = Column(Integer, ForeignKey("consultorio.id"), nullable=False)
    consultorio = relationship("Consultorio", back_populates="veterinarios")

    # Un veterinario hace muchas historias clinicas
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

    # Cada historia clinica tiene que tener el veterinario que la hizo
    veterinario_id = Column(Integer, ForeignKey("veterinario.id"), nullable=False)
    veterinario = relationship("Veterinario", back_populates="historias")

    def __repr__(self):
        return (f"Historia {self.id}: {self.fecha_atencion} | Mascota: {self.nombre_mascota} | "
                f"Dx: {self.diagnostico} | Tx: {self.tratamiento}")


# Esto solo se ejecuta cuando corremos este archivo
if __name__ == "__main__":
    # Crea todas las tablas en la base de datos
    Base.metadata.create_all(engine)
    print("Base de datos y tablas creadas correctamente.")
