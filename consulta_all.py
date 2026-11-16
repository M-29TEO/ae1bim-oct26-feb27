# Consulta con all(): muestra cada clinica y cuantas historias clinicas tiene.

from sqlalchemy.orm import sessionmaker

from crear_base_entidades import engine, Clinica

Session = sessionmaker(bind=engine)
session = Session()

# all() trae todas las clinicas en una lista
clinicas = session.query(Clinica).all()

print("Clínicas y número de historias clínicas asociadas")
print("-" * 60)
for clinica in clinicas:
    # Contamos las historias de cada veterinario de cada consultorio de la clinica
    total_historias = 0
    for consultorio in clinica.consultorios:
        for veterinario in consultorio.veterinarios:
            total_historias += len(veterinario.historias)

    print(clinica)
    print(f"   Número de historias clínicas: {total_historias}")

session.close()
