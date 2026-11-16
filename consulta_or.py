
# Uso de or_(): consultorios cuya especialidad es "Cirugía"
# O cuya especialidad es "Dermatología"
# Basta con que se cumpla UNA de las condiciones

from sqlalchemy import or_
from sqlalchemy.orm import sessionmaker

from crear_base_entidades import engine, Consultorio

Session = sessionmaker(bind=engine)
session = Session()

# or_() une las condiciones con OR en el WHERE de la consulta
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
