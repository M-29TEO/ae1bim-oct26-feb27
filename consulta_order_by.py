# consulta_order_by.py
# Uso de order_by(): listar las historias clínicas ordenadas por
# fecha de atención, de la más reciente a la más antigua.

from sqlalchemy.orm import sessionmaker

from crear_base_entidades import engine, HistoriaClinica

Session = sessionmaker(bind=engine)
session = Session()

# order_by() agrega ORDER BY. .desc() invierte el orden (descendente);
# sin él, el orden es ascendente.
historias = (session.query(HistoriaClinica)
             .order_by(HistoriaClinica.fecha_atencion.desc())
             .all())

print("Historias clínicas ordenadas por fecha (más reciente primero)")
print("-" * 60)
for h in historias:
    print(f"{h.fecha_atencion} | {h.nombre_mascota:<6} | {h.diagnostico} | "
          f"Vet.: {h.veterinario.nombres} {h.veterinario.apellidos}")

session.close()
