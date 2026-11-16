# Consulta con and_(): muestra las historias clinicas desde el 1 de octubre
# de 2026 que sean de la clinica Huellitas Quito. Tiene que cumplir las dos.

from datetime import date

from sqlalchemy import and_
from sqlalchemy.orm import sessionmaker

from crear_base_entidades import engine, HistoriaClinica, Veterinario, Consultorio, Clinica

Session = sessionmaker(bind=engine)
session = Session()

# Con los join llegamos desde la historia hasta la clinica
historias = (session.query(HistoriaClinica)
             .join(HistoriaClinica.veterinario)
             .join(Veterinario.consultorio)
             .join(Consultorio.clinica)
             .filter(and_(HistoriaClinica.fecha_atencion >= date(2026, 10, 1),
                          Clinica.nombre == "Huellitas Quito"))
             .all())

print("Historias desde 2026-10-01 en la clínica Huellitas Quito")
print("-" * 60)
for h in historias:
    print(h)

session.close()
