# Consulta con filter(): muestra los veterinarios que trabajan
# en consultorios de Cirugía.

from sqlalchemy.orm import sessionmaker

from crear_base_entidades import engine, Veterinario, Consultorio

Session = sessionmaker(bind=engine)
session = Session()

# join une veterinario con su consultorio
# filter deja solo los que son de Cirugía
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
