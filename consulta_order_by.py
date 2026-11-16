# Consulta con order_by(): muestra las historias clinicas ordenadas
# por fecha, de la mas nueva a la mas antigua.

from sqlalchemy.orm import sessionmaker

from crear_base_entidades import engine, HistoriaClinica

Session = sessionmaker(bind=engine)
session = Session()

# desc() ordena de mayor a menor (fecha mas nueva primero)
historias = (session.query(HistoriaClinica)
             .order_by(HistoriaClinica.fecha_atencion.desc())
             .all())

print("Historias clínicas ordenadas por fecha (más reciente primero)")
print("-" * 60)
for h in historias:
    print(f"{h.fecha_atencion} | {h.nombre_mascota:<6} | {h.diagnostico} | "
          f"Vet.: {h.veterinario.nombres} {h.veterinario.apellidos}")

session.close()
