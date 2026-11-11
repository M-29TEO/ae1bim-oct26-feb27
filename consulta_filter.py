# consulta_filter.py
# Uso de filter(): obtener los veterinarios que trabajan en
# consultorios cuya especialidad es "Cirugía".

from sqlalchemy.orm import sessionmaker

from crear_base_entidades import engine, Veterinario, Consultorio

Session = sessionmaker(bind=engine)
session = Session()

# join(Veterinario.consultorio) une la tabla veterinario con consultorio
# usando la clave foránea, para poder filtrar por un campo del consultorio
# filter() agrega la condición WHERE.
veterinarios = (session.query(Veterinario)
                .join(Veterinario.consultorio)
                .filter(Consultorio.especialidad == "Cirugía")
                .all())

print("Veterinarios de consultorios de Cirugía")
print("-" * 60)
for v in veterinarios:
    print(v)
    print(f"   {v.consultorio} | Clínica: {v.consultorio.clinica.nombre}")

session.close()
