
# Uso de and_(): historias clínicas atendidas a partir del 1 de octubre
# de 2026 Y que pertenecen a la clínica "Huellitas Quito"
# Se deben cumplir AMBAS condiciones

from datetime import date

from sqlalchemy import and_
from sqlalchemy.orm import sessionmaker

from crear_base_entidades import engine, HistoriaClinica, Veterinario, Consultorio, Clinica

Session = sessionmaker(bind=engine)
session = Session()

# Se recorre el camino de relaciones con varios join para poder
# filtrar por el nombre de la clínica
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
