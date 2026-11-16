# Consulta con or_(): muestra los consultorios que son de Cirugía
# o de Dermatología. Basta con que cumpla una de las dos.

from sqlalchemy import or_
from sqlalchemy.orm import sessionmaker

from crear_base_entidades import engine, Consultorio

Session = sessionmaker(bind=engine)
session = Session()

consultorios = (session.query(Consultorio)
                .filter(or_(Consultorio.especialidad == "Cirugía",
                            Consultorio.especialidad == "Dermatología"))
                .all())

print("Consultorios de Cirugía o Dermatología")
print("-" * 60)
for c in consultorios:
    print(c)
    print(f"   Clínica: {c.clinica.nombre} | Veterinarios: {len(c.veterinarios)}")

session.close()
